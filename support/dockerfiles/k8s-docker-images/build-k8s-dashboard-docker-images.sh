#!/bin/bash

set -e

DIST_TAG=$1
DIST_VER=$2
SPEC_DIR=$3
STAGE_DIR=$4
PH_BUILDER_TAG=$5
ARCH=x86_64

source common.sh

# Docker images for kubernetes-dashboard
K8S_DASH_VER=`cat ${SPEC_DIR}/kubernetes-dashboard/kubernetes-dashboard.spec | grep Version: | cut -d: -f2 | tr -d ' '`
K8S_DASH_VER_REL=${K8S_DASH_VER}-`cat ${SPEC_DIR}/kubernetes-dashboard/kubernetes-dashboard.spec | grep Release: | cut -d: -f2 | tr -d ' ' | cut -d% -f1`
K8S_DASH_RPM=kubernetes-dashboard-${K8S_DASH_VER_REL}${DIST_TAG}.${ARCH}.rpm
K8S_DASH_RPM_FILE=${STAGE_DIR}/RPMS/x86_64/${K8S_DASH_RPM}
K8S_DASH_TAR=kubernetes-dashboard-v${K8S_DASH_VER_REL}.tar

if [ ! -f ${K8S_DASH_RPM_FILE} ]; then
  echo "Kubernetes Dashboard RPM ${K8S_DASH_RPM_FILE} not found. Exiting.."
  exit 1
fi

IMG_NAME=vmware/photon-${DIST_VER}-kubernetes-dashboard-amd64:v${K8S_DASH_VER}

IMG_ID=`docker images -q ${IMG_NAME} 2> /dev/null`
if [[ ! -z "${IMG_ID}" ]]; then
  echo "Removing image ${IMG_NAME}"
  docker rmi -f ${IMG_NAME}
fi

mkdir -p tmp/k8dash

cp ${K8S_DASH_RPM_FILE} tmp/k8dash

basedir="${PWD}"

start_repo_server

pushd ./tmp/k8dash
cmd="cd '${PWD}' && rpm2cpio '${K8S_DASH_RPM}' | cpio -vid"
if ! rpmSupportsZstd; then
  docker run --rm --privileged -v ${PWD}:${PWD} $PH_BUILDER_TAG bash -c "${cmd}"
else
  eval "${cmd}"
fi

mkdir -p img

cp -pr usr/bin/dashboard \
       opt/k8dashboard/* \
       "${basedir}"/Dockerfile.kubernetes-dashboard \
       "${basedir}"/stage-rpms-tdnf.conf \
       "${basedir}"/tmp/stage-rpms.repo \
       img/

pushd img
docker build --rm -t ${IMG_NAME} -f ./Dockerfile.kubernetes-dashboard .
docker save -o ${K8S_DASH_TAR} ${IMG_NAME}
gzip ${K8S_DASH_TAR}
mv -f ${K8S_DASH_TAR}.gz ${STAGE_DIR}/docker_images/
popd # img
popd # ./tmp/k8dash

rm -rf ./tmp
