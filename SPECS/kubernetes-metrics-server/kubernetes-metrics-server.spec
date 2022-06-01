Summary:        Kubernetes Metrics Server
Name:           kubernetes-metrics-server
Version:        0.2.1
Release:        10%{?dist}
License:        Apache License 2.0
URL:            https://github.com/kubernetes-incubator/metrics-server/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    kubernetes-metrics-server-%{version}.tar.gz=ac18b1360aede4647c9dbaa72bddf735b228daf3
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go

%description
In Kubernetes, resource usage metrics, such as container CPU and memory usage, are available through the Metrics API.
These metrics can be either accessed directly by user, for example by using kubectl top command, or used by a controller
in the cluster, e.g. Horizontal Pod Autoscaler, to make decisions.

%prep -p exit
%setup -qn metrics-server-%{version}

%build
export ARCH=amd64
export VERSION=%{version}
export PKG=k8s.io/dns
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export CGO_ENABLED=0
export GO111MODULE=off
mkdir -p ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server
cp -r * ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server/
pushd ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server
make build

%install
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/kubernetes-incubator/metrics-server/metrics-server


%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/metrics-server

%changelog
*   Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-10
-   Bump up version to compile with new go
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-9
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-8
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 0.2.1-7
-   Bump up version to compile with new go
*   Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 0.2.1-6
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 0.2.1-5
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 0.2.1-4
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 0.2.1-3
-   Bump up version to compile with new go
*   Fri May 03 2019 Bo Gan <ganb@vmware.com> 0.2.1-2
-   Fix CVE-2018-17846 and CVE-2018-17143
*   Tue Jul 10 2018 Dheeraj Shetty <dheerajs@vmware.com> 0.2.1-1
-   kubernetes-metrics-server 0.2.1
