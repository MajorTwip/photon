%global VER 3.6

Summary:        A high-level scripting language
Name:           python3
Version:        3.6.9
Release:        14%{?dist}
License:        PSF
URL:            http://www.python.org/
Group:          System Environment/Programming
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
%define sha1    Python=3cd8b0e814b753fcce4fdf7edc823d8fb0da9208
Source1:        pip-setuptools-whl.tar.gz
%define sha1    pip-setuptools-whl=1e932912469c04ed2188d638b68ba4a2eb210510

Patch0:         cgi3.patch
Patch1:         python3-support-photon-platform.patch
Patch2:         python3-CVE-2017-18207.patch
Patch3:         python3-CVE-2019-16056.patch
Patch4:         python3-CVE-2019-16935.patch
Patch5:         python3-CVE-2019-17514.patch
Patch6:         python3-CVE-2019-18348.patch
Patch7:         python3-CVE-2019-9674.patch
Patch8:         python3-CVE-2020-8492.patch
Patch9:         python3-CVE-2020-14422.patch
Patch10:        python3-CVE-2019-20907.patch
Patch11:        python3-CVE-2020-26116.patch
Patch12:        python3-CVE-2020-27619.patch
Patch13:        CVE-2021-3177.patch
Patch14:        CVE-2021-23336.patch
Patch15:        pip-setuptools-update.patch
Patch16:        CVE-2022-0391-1.patch
Patch17:        CVE-2022-0391-2.patch
Patch18:        CVE-2021-3737-1.patch
Patch19:        CVE-2021-3737-2.patch
Patch20:        python3-CVE-2015-20107.patch
Patch21:        CVE-2021-28861.patch
Patch22:        CVE-2021-4189.patch

BuildRequires:  pkg-config >= 0.28
BuildRequires:  bzip2-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  readline-devel
BuildRequires:  xz-devel
BuildRequires:  expat-devel >= 2.1.0
BuildRequires:  libffi-devel >= 3.0.13
BuildRequires:  ncurses-devel
BuildRequires:  sqlite-devel

Requires:       ncurses
Requires:       openssl
Requires:       python3-libs = %{version}-%{release}
Requires:       readline
Requires:       xz
Provides:       python-sqlite
Provides:       python(abi)
Provides:       /usr/bin/python
Provides:       /bin/python
Provides:       /bin/python3

%description
The Python 3 package contains a new version of Python development environment.
Python 3 brings more efficient ways of handling dictionaries, better unicode
strings support, easier and more intuitive syntax, and removes the deprecated
code. It is incompatible with Python 2.x releases.

%package libs
Summary: The libraries for python runtime
Group: Applications/System
Requires:       (coreutils or toybox)
Requires:       expat >= 2.1.0
Requires:       libffi >= 3.0.13
Requires:       ncurses
Requires:       sqlite-libs
Requires:       bzip2-libs

%description    libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python-libs package
provides the libraries needed for python 3 applications.

%package        xml
Summary:        XML libraries for python3 runtime
Group:          Applications/System
Requires:       python3-libs = %{version}-%{release}
Requires:       python3 = %{version}-%{release}

%description    xml
The python3-xml package provides the libraries needed for XML manipulation.

%package        curses
Summary:        Python module interface for NCurses Library
Group:          Applications/System
Requires:       python3-libs = %{version}-%{release}
Requires:       ncurses

%description    curses
The python3-curses package provides interface for ncurses library.

%package        devel
Summary: The libraries and header files needed for Python development.
Group:          Development/Libraries
Requires:       python3 = %{version}-%{release}
Requires:       expat-devel >= 2.1.0
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: python3 < %{version}-%{release}

%description    devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package        tools
Summary:        A collection of development tools included with Python.
Group:          Development/Tools
Requires:       python3 = %{version}-%{release}

%description    tools
The Python package includes several development tools that are used
to build python programs.

%package        setuptools
Summary:        Download, build, install, upgrade, and uninstall Python packages.
Group:          Development/Tools
BuildArch:      noarch
Requires:       python3 = %{version}-%{release}

%description    setuptools
setuptools is a collection of enhancements to the Python distutils that allow you to more easily build and distribute Python packages, especially ones that have dependencies on other packages.

%package test
Summary: Regression tests package for Python.
Group: Development/Tools
Requires: python3 = %{version}-%{release}

%description test
The test package contains all regression tests for Python as well as the modules test.support and test.regrtest. test.support is used to enhance your tests while test.regrtest drives the testing suite.

%prep
# Using autosetup is not feasible
%setup -q -n Python-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1

rm -r Lib/ensurepip/_bundled/*
tar -xf %{SOURCE1} -C Lib/ensurepip/_bundled

%build
export OPT="${CFLAGS}"
%configure \
    --enable-shared \
    --with-system-expat \
    --with-system-ffi \
    --with-dbmliborder=gdbm:ndbm
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
chmod -v 755 %{buildroot}%{_libdir}/libpython%{VER}m.so.1.0
%{_fixperms} %{buildroot}/*
ln -sf libpython%{VER}m.so %{buildroot}%{_libdir}/libpython%{VER}.so

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete
rm %{buildroot}%{_bindir}/2to3

%check
make %{?_smp_mflags} test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-, root, root)
%doc LICENSE README.rst
%{_bindir}/pydoc*
%{_bindir}/pyvenv*
%{_bindir}/python3
%{_bindir}/python%{VER}
%{_bindir}/python%{VER}m
%{_mandir}/*/*

%dir %{_libdir}/python%{VER}
%dir %{_libdir}/python%{VER}/site-packages

%{_libdir}/libpython3.so
%{_libdir}/libpython%{VER}.so
%{_libdir}/libpython%{VER}m.so.1.0

%exclude %{_libdir}/python%{VER}/ctypes/test
%exclude %{_libdir}/python%{VER}/distutils/tests
%exclude %{_libdir}/python%{VER}/sqlite3/test
%exclude %{_libdir}/python%{VER}/idlelib/idle_test
%exclude %{_libdir}/python%{VER}/test
%exclude %{_libdir}/python%{VER}/lib-dynload/_ctypes_test.*.so
%exclude %{_bindir}/pip3
%exclude %{_bindir}/pip%{VER}
%exclude %{_libdir}/python%{VER}/site-packages/pip/*
%exclude %{_libdir}/python%{VER}/site-packages/pip-21.2.4.dist-info/*

%files libs
%defattr(-,root,root)
%doc LICENSE README.rst
%{_libdir}/python%{VER}/*
%{_libdir}/python%{VER}/site-packages/README.txt
%exclude %{_libdir}/python%{VER}/site-packages/
%exclude %{_libdir}/python%{VER}/ctypes/test
%exclude %{_libdir}/python%{VER}/distutils/tests
%exclude %{_libdir}/python%{VER}/distutils/command/wininst*exe
%exclude %{_libdir}/python%{VER}/sqlite3/test
%exclude %{_libdir}/python%{VER}/idlelib/idle_test
%exclude %{_libdir}/python%{VER}/test
%exclude %{_libdir}/python%{VER}/lib-dynload/_ctypes_test.*.so
%exclude %{_libdir}/python%{VER}/xml
%exclude %{_libdir}/python%{VER}/lib-dynload/pyexpat*.so
%exclude %{_libdir}/python%{VER}/curses
%exclude %{_libdir}/python%{VER}/lib-dynload/_curses*.so

%files  xml
%{_libdir}/python%{VER}/xml/*
%{_libdir}/python%{VER}/lib-dynload/pyexpat*.so

%files  curses
%{_libdir}/python%{VER}/curses/*
%{_libdir}/python%{VER}/lib-dynload/_curses*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/python-%{VER}.pc
%{_libdir}/pkgconfig/python-%{VER}m.pc
%{_libdir}/pkgconfig/python3.pc
%{_libdir}/libpython%{VER}m.so
%{_bindir}/python3-config
%{_bindir}/python%{VER}-config
%{_bindir}/python%{VER}m-config

%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-,root,root,755)
%doc Tools/README
%{_bindir}/2to3-%{VER}
%exclude %{_bindir}/idle*

%files setuptools
%defattr(-,root,root,755)
%{_libdir}/python%{VER}/site-packages/pkg_resources/*
%{_libdir}/python%{VER}/site-packages/_distutils_hack/*
%{_libdir}/python%{VER}/site-packages/distutils-precedence.pth
%{_libdir}/python%{VER}/site-packages/setuptools/*
%{_libdir}/python%{VER}/site-packages/setuptools-57.4.0.dist-info/*
%exclude %{_libdir}/python%{VER}/site-packages/setuptools/*.exe

%files test
%{_libdir}/python%{VER}/test/*

%changelog
* Tue Sep 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.6.9-14
- Fix CVE-2021-28861 & CVE-2021-4189
* Mon Aug 29 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.6.9-13
- Fix CVE-2015-20107
* Fri Mar 18 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.6.9-12
- Fix CVE-2021-3737
* Thu Mar 03 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.6.9-11
- Fix CVE-2022-0391
* Thu Dec 02 2021 Tapas Kundu <tkundu@vmware.com> 3.6.9-10
- Do not package /usr/lib/python3.7/lib2to3 in tools
* Wed Sep 29 2021 Piyush Gupta <gpiyush@vmware.com> 3.6.9-9
- Remove packaging python3-pip and create seperate spec.
* Sat Mar 27 2021 Tapas Kundu <tkundu@vmware.com> 3.6.9-8
- Remove packaging exe files in python3-pip and setuptools
* Tue Mar 02 2021 Piyush Gupta <gpiyush@vmware.com> 3.6.9-7
- Fix CVE-2021-23336
* Mon Feb 01 2021 Shreyas B. <shreyasb@vmware.com> 3.6.9-6
- Fix CVE-2021-3177
* Thu Nov 05 2020 Tapas Kundu <tkundu@vmware.com> 3.6.9-5
- Fix CVE-2020-27619
* Mon Oct 12 2020 Tapas Kundu <tkundu@vmware.com> 3.6.9-4
- Fix CVE-2020-26116
* Mon Jul 20 2020 Tapas Kundu <tkundu@vmware.com> 3.6.9-3
- Address CVE-2019-20907
* Wed Jul 01 2020 Tapas Kundu <tkundu@vmware.com> 3.6.9-2
- Address CVE-2020-14422
* Fri Apr 17 2020 Tapas Kundu <tkundu@vmware.com> 3.6.9-1
- Update to release 3.6.9
* Fri Apr 03 2020 Tapas Kundu <tkundu@vmware.com> 3.6.5-14
- Fix for CVE-2020-8492
* Tue Mar 31 2020 Tapas Kundu <tkundu@vmware.com> 3.6.5-13
- Fix for CVE-2019-9674
* Thu Mar 26 2020 Tapas Kundu <tkundu@vmware.com> 3.6.5-12
- Fix for CVE-2019-18348
* Tue Nov 05 2019 Tapas Kundu <tkundu@vmware.com> 3.6.5-11
- Fix for CVE-2019-17514
- Fix conflict of libpython3.so
* Fri Oct 11 2019 Tapas Kundu <tkundu@vmware.com> 3.6.5-10
- Fix for CVE-2019-16935
* Wed Sep 11 2019 Tapas Kundu <tkundu@vmware.com> 3.6.5-9
- Fix CVE-2019-16056
* Fri Jul 19 2019 Tapas Kundu <tkundu@vmware.com> 3.6.5-8
- Fix for CVE-2018-20852
* Mon Jun 17 2019 Tapas Kundu <tkundu@vmware.com> 3.6.5-7
- Fix for CVE-2019-10160
* Wed Mar 13 2019 Tapas Kundu <tkundu@vmware.com> 3.6.5-6
- Fix for CVE-2019-5010
- Fix for CVE-2019-9740
* Wed Mar 13 2019 Tapas Kundu <tkundu@vmware.com> 3.6.5-5
- Fix for CVE-2019-9636.patch
* Mon Feb 11 2019 Tapas Kundu <tkundu@vmware.com> 3.6.5-4
- Fix for CVE-2018-20406
* Mon Dec 31 2018 Tapas Kundu <tkundu@vmware.com> 3.6.5-3
- Fix for CVE-2018-14647
* Thu Oct 25 2018 Sujay g <gsujay@vmware.com> 3.6.5-2
- Remove vulnerable Windows installers from python3-libs rpm
* Thu Apr 19 2018 Xiaolin Li <xiaolinl@vmware.com> 3.6.5-1
- Update to version 3.6.5 to fix CVE-2018-1000117
- Apply patch for CVE-2017-18207
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.6.1-9
- Requires coreutils or toybox
- Requires bzip2-libs
* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 3.6.1-8
- Remove devpts mount in check
* Mon Aug 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-7
- Add pty for tests to pass
* Wed Jul 12 2017 Xiaolin Li <xiaolinl@vmware.com> 3.6.1-6
- Add python3-test package.
* Fri Jun 30 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-5
- Remove the imaplib tests.
* Mon Jun 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.6.1-4
- Added pip, setuptools, xml, and curses sub packages.
* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 3.6.1-3
- Fix symlink and script
* Wed May 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.6.1-2
- Exclude idle3.
* Wed Apr 26 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.1-1
- Updating to latest
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.5.3-3
- Python3-devel requires expat-devel.
* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-2
- Provides /bin/python3.
* Tue Feb 28 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-1
- Updated to version 3.5.3.
* Fri Jan 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.5.1-10
- Added patch to support Photon OS
* Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 3.5.1-9
- Move easy_install-3.5 to devel subpackage.
* Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 3.5.1-8
- Use sqlite-{devel,libs}
* Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-7
- Patch for CVE-2016-5636
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 3.5.1-6
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-5
- GA - Bump release of all rpms
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-4
- Edit scriptlets.
* Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-3
- update python to require python-libs
* Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.5.1-2
- Providing python3 binaries instead of the minor versions.
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.5.1-1
- Updated to version 3.5.1
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.4.3-3
- Edit post script.
* Mon Aug 17 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3-2
- Remove python.o file, and minor cleanups.
* Wed Jul 1 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3
- Add Python3 package to Photon.
