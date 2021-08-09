import os
import threading
import copy
from PackageBuildDataGenerator import PackageBuildDataGenerator
from Logger import Logger
from constants import constants
from CommandUtils import CommandUtils
from PackageUtils import PackageUtils
from ToolChainUtils import ToolChainUtils
from Scheduler import Scheduler
from ThreadPool import ThreadPool
from SpecData import SPECS
from StringUtils import StringUtils
from Sandbox import Chroot, Container

class PackageManager(object):

    def __init__(self, logName=None, logPath=None, pkgBuildType="chroot"):
        if logName is None:
            logName = "PackageManager"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logLevel = constants.logLevel
        self.logger = Logger.getLogger(logName, logPath, constants.logLevel)
        self.mapCyclesToPackageList = {}
        self.mapPackageToCycle = {}
        self.sortedPackageList = []
        self.listOfPackagesAlreadyBuilt = set()
        self.pkgBuildType = pkgBuildType
        if self.pkgBuildType == "container":
            import docker
            self.dockerClient = docker.from_env(version="auto")
        cmdUtils = CommandUtils()
        # if rpm doesnt have zstd support
        if cmdUtils.runCommandInShell('rpm --showrc | grep -i "rpmlib(PayloadIsZstd)"', logfn=self.logger.debug):
            constants.hostRpmIsNotUsable = True
            self.createZstdBuilderImage()

    def createZstdBuilderImage(self):
        import docker
        self.dockerClient = docker.from_env(version="auto")
        self.logger.info("creating photon builder docker image")
        try:
            image = self.dockerClient.images.build(tag='photon_builder:latest',
                                       path=os.path.dirname(os.path.realpath(__file__)),
                                       rm=True,
                                       dockerfile="Dockerfile.photon_builder")
            self.logger.debug("Created Image {0}".format(image))
        except Exception as e:
            self.logger.info("Non-zero tdnf code? Try running `docker pull photon:latest`")
            raise e


    def buildToolChain(self):
        self.logger.info("Step 1 : Building the core toolchain packages for " + constants.currentArch)
        self.logger.info(constants.listCoreToolChainPackages)
        self.logger.info("")

        pkgCount = 0
        pkgUtils = PackageUtils(self.logName, self.logPath)
        coreToolChainYetToBuild = []
        doneList = []
        for package in constants.listCoreToolChainPackages:
            version = SPECS.getData().getHighestVersion(package)
            rpmPkg = pkgUtils.findRPMFile(package, version)
            self.sortedPackageList.append(package+"-"+version)
            if rpmPkg is not None:
                doneList.append(package+'-'+version)
                continue
            else:
                coreToolChainYetToBuild.append(package)

        self.listOfPackagesAlreadyBuilt = set(doneList)
        pkgCount = len(coreToolChainYetToBuild)
        if coreToolChainYetToBuild:
            self.logger.info("The following core toolchain packages need to be built :")
            self.logger.info(coreToolChainYetToBuild)
        else:
            self.logger.info("Core toolchain packages are already available")
            self.logger.info("")
            return pkgCount

        Scheduler.coreToolChainBuild = True
        self._buildPackages(1)
        Scheduler.coreToolChainBuild = False
        self.logger.debug("Successfully built core toolchain")
        self.logger.info("-" * 45 + "\n")
        return pkgCount

    def buildToolChainPackages(self, buildThreads):
        pkgCount = self.buildToolChain()
        # Stage 2 makes sence only for native tools
        if not constants.crossCompiling:
            if self.pkgBuildType == "container":
                # Stage 1 build container
                #TODO image name constants.buildContainerImageName
                if pkgCount > 0 or not self.dockerClient.images.list(constants.buildContainerImage):
                    self._createBuildContainer(True)
            self.logger.info("Step 2 : Building stage 2 of the toolchain...")
            self.logger.info(constants.listToolChainPackages)
            self.logger.info("")
            self._buildGivenPackages(constants.listToolChainPackages, buildThreads)
            self.logger.info("The entire toolchain is now available")
            self.logger.info(45 * '-')
            self.logger.info("")
        if self.pkgBuildType == "container":
            # Stage 2 build container
            #TODO: rebuild container only if anything in listToolChainPackages was built
            self._createBuildContainer(False)

    def buildPackages(self, listPackages, buildThreads):
        if constants.rpmCheck:
            constants.rpmCheck = False
            constants.addMacro("with_check", "0")
            self.buildToolChainPackages(buildThreads)
            self._buildTestPackages(buildThreads)
            constants.rpmCheck = True
            constants.addMacro("with_check", "1")
            self._buildGivenPackages(listPackages, buildThreads)
        else:
            self.buildToolChainPackages(buildThreads)
            self.logger.info("Step 3 : Building the following package(s) and dependencies...")
            self.logger.info(listPackages)
            self.logger.info("")
            self._buildGivenPackages(listPackages, buildThreads)
        self.logger.info("Package build has been completed")
        self.logger.info("")

    def _readPackageBuildData(self, listPackages):
        try:
            pkgBuildDataGen = PackageBuildDataGenerator(self.logName, self.logPath)
            self.mapCyclesToPackageList, self.mapPackageToCycle, self.sortedPackageList = (
                pkgBuildDataGen.getPackageBuildData(listPackages))

        except Exception as e:
            self.logger.exception(e)
            self.logger.error("unable to get sorted list")
            return False
        return True

    # Returns list of base package names which spec file has all subpackages built
    # Returns set of package name and version like
    # ["name1-vers1", "name2-vers2",..]
    def _readAlreadyAvailablePackages(self):
        listAvailablePackages = set()
        pkgUtils = PackageUtils(self.logName, self.logPath)
        listPackages = SPECS.getData().getListPackages()
        for package in listPackages:
            for version in SPECS.getData().getVersions(package):
                # Mark package available only if all subpackages are available
                packageIsAlreadyBuilt=True
                listRPMPackages = SPECS.getData().getRPMPackages(package, version)
                for rpmPkg in listRPMPackages:
                    if pkgUtils.findRPMFile(rpmPkg, version) is None:
                        packageIsAlreadyBuilt=False
                        break;
                if packageIsAlreadyBuilt:
                    listAvailablePackages.add(package+"-"+version)

        return listAvailablePackages

    def _calculateParams(self, listPackages):
        self.mapCyclesToPackageList.clear()
        self.mapPackageToCycle.clear()
        self.sortedPackageList = []

        self.listOfPackagesAlreadyBuilt = self._readAlreadyAvailablePackages()
        if self.listOfPackagesAlreadyBuilt:
            self.logger.debug("List of already available packages:")
            self.logger.debug(self.listOfPackagesAlreadyBuilt)

        listPackagesToBuild = copy.copy(listPackages)
        for pkg in listPackages:
            if (pkg in self.listOfPackagesAlreadyBuilt and
                    not constants.rpmCheck):
                listPackagesToBuild.remove(pkg)

        if constants.rpmCheck:
            self.sortedPackageList = listPackagesToBuild
        else:
            if not self._readPackageBuildData(listPackagesToBuild):
                return False

        if self.sortedPackageList:
            self.logger.info("List of packages yet to be built...")
            self.logger.info(str(set(self.sortedPackageList) - set(self.listOfPackagesAlreadyBuilt)))
            self.logger.info("")

        return True

    def _buildTestPackages(self, buildThreads):
        self.buildToolChain()
        self._buildGivenPackages(constants.listMakeCheckRPMPkgtoInstall, buildThreads)

    def _initializeThreadPool(self, statusEvent):
        ThreadPool.clear()
        ThreadPool.mapPackageToCycle = self.mapPackageToCycle
        ThreadPool.logger = self.logger
        ThreadPool.statusEvent = statusEvent
        ThreadPool.pkgBuildType = self.pkgBuildType

    def _initializeScheduler(self, statusEvent):
        Scheduler.setLog(self.logName, self.logPath, self.logLevel)
        Scheduler.setParams(self.sortedPackageList, self.listOfPackagesAlreadyBuilt)
        Scheduler.setEvent(statusEvent)
        Scheduler.stopScheduling = False

    def _buildGivenPackages(self, listPackages, buildThreads):
        # Extend listPackages from ["name1", "name2",..] to ["name1-vers1", "name2-vers2",..]
        listPackageNamesAndVersions=set()
        for pkg in listPackages:
            base = SPECS.getData().getSpecName(pkg)
            for version in SPECS.getData().getVersions(base):
                listPackageNamesAndVersions.add(base+"-"+version)

        returnVal = self._calculateParams(listPackageNamesAndVersions)
        if not returnVal:
            self.logger.error("Unable to set parameters. Terminating the package manager.")
            raise Exception("Unable to set parameters")
        self._buildPackages(buildThreads)

    def _buildPackages(self, buildThreads):
        if constants.startSchedulerServer:
            import SchedulerServer
            self._initializeScheduler(None)
            SchedulerServer.mapPackageToCycle = self.mapPackageToCycle
            serverThread = threading.Thread(target=SchedulerServer.startServer, name="serverthread")
            serverThread.start()
            serverThread.join()
        else:
            statusEvent = threading.Event()
            self._initializeScheduler(statusEvent)
            self._initializeThreadPool(statusEvent)
            for i in range(0, buildThreads):
                workerName = "WorkerThread" + str(i)
                ThreadPool.addWorkerThread(workerName)
                ThreadPool.startWorkerThread(workerName)

            statusEvent.wait()
            Scheduler.stopScheduling = True
            self.logger.debug("Waiting for all remaining worker threads")
            ThreadPool.join_all()

        setFailFlag = False
        allPackagesBuilt = False
        if Scheduler.isAnyPackagesFailedToBuild():
            setFailFlag = True

        if Scheduler.isAllPackagesBuilt():
            allPackagesBuilt = True

        if setFailFlag:
            self.logger.error("Some of the packages failed:")
            self.logger.error(Scheduler.listOfFailedPackages)
            raise Exception("Failed during building package")

        if not setFailFlag:
            if allPackagesBuilt:
                self.logger.debug("All packages built successfully")
            else:
                self.logger.error("Build stopped unexpectedly.Unknown error.")
                raise Exception("Unknown error")

    def _createBuildContainer(self, usePublishedRPMs):
        self.logger.debug("Generating photon build container..")
        try:
            #TODO image name constants.buildContainerImageName
            self.dockerClient.images.remove(constants.buildContainerImage, force=True)
        except Exception as e:
            #TODO - better handling
            self.logger.debug("Photon build container image not found.")

        # Create toolchain chroot and install toolchain RPMs
        chroot = None
        try:
            #TODO: constants.tcrootname
            chroot = Chroot(self.logger)
            chroot.create("toolchain-chroot")
            tcUtils = ToolChainUtils("toolchain-chroot", self.logPath)
            tcUtils.installToolchainRPMS(chroot, usePublishedRPMS=usePublishedRPMs)
        except Exception as e:
            if chroot:
                chroot.destroy()
            raise e
        self.logger.debug("createBuildContainer: " + chroot.getID())

        # Create photon build container using toolchain chroot
        chroot.unmountAll()
        #TODO: Coalesce logging
        cmdUtils = CommandUtils()
        cmd = "cd " + chroot.getID() + " && tar -czf ../tcroot.tar.gz ."
        cmdUtils.runCommandInShell(cmd, logfn=self.logger.debug)
        cmd = "mv " + chroot.getID() + "/../tcroot.tar.gz ."
        cmdUtils.runCommandInShell(cmd, logfn=self.logger.debug)
        #TODO: Container name, docker file name from constants.
        self.dockerClient.images.build(tag=constants.buildContainerImage,
                                       path=".",
                                       rm=True,
                                       dockerfile="Dockerfile.photon_build_container")

        # Cleanup
        cmd = "rm -f ./tcroot.tar.gz"
        cmdUtils.runCommandInShell(cmd, logfn=self.logger.debug)
        chroot.destroy()
        self.logger.debug("Photon build container successfully created.")
