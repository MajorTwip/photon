Summary:        Calico networking for CNI
Name:           calico-cni
Version:        3.21.0
Release:        7%{?dist}
License:        ASL 2.0
URL:            https://github.com/projectcalico/cni-plugin
Source0:        %{name}-%{version}.tar.gz
%define sha1 calico-cni=fa803b8e69a9228df3442b55c4e4f5c6e188778e
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  git
BuildRequires:  go
Requires:       cni
%define debug_package %{nil}

%description
Project Calico network plugin for CNI. This allows kubernetes to use Calico networking. This repository includes a top-level CNI networking plugin, as well as a CNI IPAM plugin which makes use of Calico IPAM.

%prep
%setup -n cni-plugin-%{version}

%build
mkdir -p dist
go build -v -o dist/calico -ldflags "-X main.VERSION= -s -w" ./cmd/calico
go build -v -o dist/calico-ipam -ldflags "-X main.VERSION= -s -w" ./cmd/calico
go build -v -o dist/install -ldflags "-X main.VERSION= -s -w" ./cmd/calico

%install
install -vdm 755 %{buildroot}/opt/cni/bin
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ dist/calico
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ dist/calico-ipam
install -vpm 0755 -t %{buildroot}/opt/cni/bin/ dist/install

%files
%defattr(-,root,root)
/opt/cni/bin/calico
/opt/cni/bin/calico-ipam
/opt/cni/bin/install

%changelog
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-7
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-6
- Bump up version to compile with new go
* Sat Sep 17 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-5
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-4
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-3
- Bump up version to compile with new go
*   Fri May 27 2022 Piyush Gupta <gpiyush@vmware.com> 3.21.0-2
-   Bump up version to compile with new go
*   Fri May 13 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.21.0-1
-   Update to 3.21.0
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-5
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-4
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 3.15.2-3
-   Bump up version to compile with new go
*   Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 3.15.2-2
-   Bump up version to compile with new go
*   Tue May 25 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.15.2-1
-   Update to version 3.15.2
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 3.6.1-6
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 3.6.1-5
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 3.6.1-4
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-3
-   Bump up version to compile with new go
*   Tue Aug 27 2019 Harinadh Dommaraju <hdommaraju@vmware.com> 3.6.1-2
-   version bump to build using go-1.9.4-6
*   Thu Apr 11 2019 Ashwin H <ashwinh@vmware.com> 3.6.1-1
-   Update to 3.6.1
*   Mon Aug 06 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.11.2-2
-   Build using go version 1.9.4
*   Tue Mar 20 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.11.2-1
-   calico-cni v1.11.2.
*   Thu Dec 07 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.11.0-2
-   Cache build dependencies in our repo.
*   Fri Nov 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.11.0-1
-   calico-cni v1.11.0.
*   Mon Aug 14 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.10.0-1
-   calico-cni for PhotonOS.
