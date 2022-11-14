Summary:        CoreDNS
Name:           coredns
Version:        1.7.1
Release:        3%{?dist}
License:        Apache License 2.0
URL:            https://github.com/coredns/coredns/archive/v%{version}.tar.gz
Source0:        coredns-%{version}.tar.gz
%define sha1    coredns-%{version}.tar.gz=8a61f2346ced4f16eaeb80c2748a3e3022de4cfe
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
%define debug_package %{nil}

%description
CoreDNS is a DNS server that chains plugins

%prep -p exit
%setup -qn coredns-%{version}

%build
export ARCH=amd64
export VERSION=%{version}
export PKG=github.com/%{name}/%{name}
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export GOBIN=/usr/share/gocode/bin
export PATH=$PATH:$GOBIN
mkdir -p ${GOPATH}/src/${PKG}
cp -rf . ${GOPATH}/src/${PKG}
pushd ${GOPATH}/src/${PKG}
# Just download (do not compile), since it's not compilable with go-1.9.
# TODO: use prefetched tarball instead.
sed -i 's#go get -u github.com/mholt/caddy#go get -u -d github.com/mholt/caddy#' Makefile
sed -i 's#go get -u github.com/miekg/dns#go get -u -d github.com/miekg/dns#' Makefile
make %{?_smp_mflags}

%install
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/coredns

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/coredns

%changelog
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-3
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-2
- Bump up version to compile with new go.
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-1
- Upgrade to 1.7.1.
* Sat Sep 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.6-15
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.6-14
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.6-13
- Bump up version to compile with new go
*   Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.6-12
-   Bump up version to compile with new go
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.6-11
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.6-10
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.6-9
-   Bump up version to compile with new go
*   Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.6-8
-   Bump up version to compile with new go
*   Thu Dec 17 2020 Ankit Jain <ankitja@vmware.com> 1.2.6-7
-   Repo changed from github.com/mholt/caddy to github.com/caddyserver/caddy
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.2.6-6
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.6-5
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.2.6-4
-   Bump up version to compile with new go
*   Sun Sep 22 2019 Alexey Makhalov <amakhalov@vmware.com> 1.2.6-3
-   Fix compilation issue (do not compile mholt/caddy).
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.2.6-2
-   Bump up version to compile with new go
*   Fri Dec 14 2018 Emil John <ejohn@vmware.com> 1.2.6-1
-   Update CoreDNS to v1.2.6
*   Fri Aug 03 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.2.0-1
-   Initial version of coredns 1.2.0.
