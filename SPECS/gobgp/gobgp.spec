Summary:       BGP implementation in Go
Name:          gobgp
Version:       2.9.0
Release:       6%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/osrg/gobgp
Source0:       %{name}-%{version}.tar.gz
%define sha1 gobgp=24228859d09fa63492e2d8fb26de9cb93bbd5f3b
Distribution:  Photon
BuildRequires: git
BuildRequires: go
%define debug_package %{nil}

%description
GoBGP is an open source BGP implementation designed from scratch for modern environment and implemented in a modern programming language, the Go Programming Language.

%prep
%setup -q

%build
mkdir -p ${GOPATH}/src/github.com/osrg/gobgp
cp -r * ${GOPATH}/src/github.com/osrg/gobgp/.
pushd ${GOPATH}/src/github.com/osrg/gobgp
go mod download
mkdir -p dist
pushd cmd/gobgp
go build -v -o ../../dist/gobgp -ldflags "-X main.VERSION=%{version} -s -w"
popd
pushd cmd/gobgpd
go build -v -o ../../dist/gobgpd -ldflags "-X main.VERSION=%{version} -s -w"
popd
popd

%install
pushd ${GOPATH}/src/github.com/osrg/gobgp
install -vdm 755 %{buildroot}%{_bindir}
install ${GOPATH}/src/github.com/osrg/gobgp/dist/gobgp %{buildroot}%{_bindir}/
install ${GOPATH}/src/github.com/osrg/gobgp/dist/gobgpd %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/gobgp
%{_bindir}/gobgpd
%doc LICENSE README.md

%changelog
*   Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 2.9.0-6
-   Bump up version to compile with new go
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 2.9.0-5
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 2.9.0-4
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 2.9.0-3
-   Bump up version to compile with new go
*   Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 2.9.0-2
-   Bump up version to compile with new go
*   Wed Aug 19 2020 Ashwin H <ashwinh@vmware.com> 2.9.0-1
-   Update to 2.9.0 to work with go 1.13
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.23-6
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.23-5
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.23-4
-   Bump up version to compile with new go
*   Wed Aug 14 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 1.23-3
-   Version bump to build using go version 1.9.4-6
*   Mon Aug 06 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.23-2
-   Build using go version 1.9.4
*   Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.23-1
-   Go BGP daemon for PhotonOS.
