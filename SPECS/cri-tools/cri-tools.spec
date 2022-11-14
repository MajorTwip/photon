%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.11.1
Release:        14%{?dist}
License:        Apache License Version 2.0
URL:            https://github.com/kubernetes-incubator/cri-tools/archive/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}.tar.gz=ba8064bcac65239a9c9e0e21c7d576c6b39f4089
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%setup -qn %{name}-%{version}

%build
export GO111MODULE=off
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/lib/.build-id
mkdir -p %{buildroot}/usr/share/doc/cri-tools
mkdir -p %{buildroot}/usr/share/licenses/cri-tools
mkdir -p %{buildroot}/man/man1

make install DESTDIR=%{buildroot}
cp /usr/local/bin/crictl %{buildroot}/usr/bin
cp /usr/local/bin/critest %{buildroot}/usr/bin
cp CHANGELOG.md %{buildroot}/usr/share/doc/cri-tools
cp LICENSE %{buildroot}/usr/share/licenses/cri-tools
cp CHANGELOG.md %{buildroot}/usr/share/doc/cri-tools
cp CONTRIBUTING.md %{buildroot}/usr/share/doc/cri-tools
cp OWNERS %{buildroot}/usr/share/doc/cri-tools
cp README.md %{buildroot}/usr/share/doc/cri-tools
cp code-of-conduct.md %{buildroot}/usr/share/doc/cri-tools
cp docs/validation.md %{buildroot}/usr/share/doc/cri-tools
cp docs/roadmap.md %{buildroot}/usr/share/doc/cri-tools

%files
%defattr(-,root,root)
%{_datadir}/%{name}
/usr/bin
/usr/share/doc/*
/usr/share/licenses/*
/man/man1/

%clean
rm -rf %{buildroot}/*

%changelog
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-14
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-13
- Bump up version to compile with new go
* Sat Sep 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-12
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-11
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-10
- Bump up version to compile with new go
*   Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-9
-   Bump up version to compile with new go
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-8
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-7
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.11.1-6
-   Bump up version to compile with new go
*   Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 1.11.1-5
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.11.1-4
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.11.1-3
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.11.1-2
-   Bump up version to compile with new go
*    Thu Jul 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.1-1
-    Initial build added for Photon.
