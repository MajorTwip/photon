Summary:       Docker libnetwork plugin for Calico
Name:          calico-libnetwork
Version:       1.1.0
Release:       17%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/projectcalico/libnetwork-plugin
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: git
BuildRequires: glide
BuildRequires: go
%define sha1 calico-libnetwork=bed540d714a7b2e0d0138556894541109dc7b792
%define debug_package %{nil}

%description
Docker libnetwork plugin for Calico.

%prep
%setup -q -n libnetwork-plugin-1.1.0

%build
export GO111MODULE=off
mkdir -p /root/.glide
mkdir -p ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin
cp -r * ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin/.
pushd ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin
mkdir -p dist
glide install --strip-vendor
CGO_ENABLED=0 go build -v -i -o dist/libnetwork-plugin -ldflags "-X main.VERSION=%{version} -s -w" main.go

%install
pushd ${GOPATH}/src/github.com/projectcalico/libnetwork-plugin
install -vdm 0755 %{buildroot}/usr/share/calico/docker
install -vpm 0755 -t %{buildroot}/usr/share/calico/docker/ dist/libnetwork-plugin

%files
%defattr(-,root,root)
/usr/share/calico/docker/libnetwork-plugin

%changelog
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-17
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-16
- Bump up version to compile with new go
* Sat Sep 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-15
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-14
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-13
- Bump up version to compile with new go
*   Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-12
-   Bump up version to compile with new go
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-11
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-10
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.1.0-9
-   Bump up version to compile with new go
*   Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 1.1.0-8
-   Bump up version to compile with new go
*   Sat Aug 22 2020 Ashwin H <ashwinh@vmware.com> 1.1.0-7
-   Remove hardcoded go dependecy
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.1.0-6
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.1.0-5
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.1.0-4
-   Bump up version to compile with new go
*    Tue Aug 27 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 1.1.0-3
-    version bump to build using go version 1.9.4-6
*    Mon Aug 06 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.1.0-2
-    Build using go version 1.9.4
*    Fri Aug 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.0-1
-    Calico libnetwork plugin for PhotonOS.
