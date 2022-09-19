%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        CoreDNS
Name:           coredns
Version:        1.2.0
Release:        20%{?dist}
License:        Apache License 2.0
URL:            https://github.com/coredns/coredns/releases/v%{version}.tar.gz
Source0:        coredns-%{version}.tar.gz
%define sha512  coredns=c4b9c18337f4b55ed90b0c48ce278042c540017b556587075d4bb74666f98a7e2317416d1105cdb92e7fc0111d4bb953473e8ab25798b67da75b9114868394e3
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
%define debug_package %{nil}

%description
CoreDNS is a DNS server that chains plugins

%prep -p exit
%autosetup -n coredns-%{version}

%build
export ARCH=%{gohostarch}
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
export GO111MODULE=auto
mkdir -p ${GOPATH}/src/${PKG}
cp -rf . ${GOPATH}/src/${PKG}
pushd ${GOPATH}/src/${PKG}
# Just download (do not compile), since it's not compilable with go-1.9.
# TODO: use prefetched tarball instead.
find . -type f -exec sed -i 's|github.com/mholt/caddy|github.com/caddyserver/caddy|' {} +
sed -i 's#go get -u github.com/caddyserver/caddy#go get -u -d github.com/caddyserver/caddy#' Makefile
sed -i 's#v0.10.11#v0.10.11 \&\& find . -type f -exec sed -i "s\|github.com/mholt/caddy\|github.com/caddyserver/caddy\|" {} + #g' Makefile
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
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-20
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-19
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-18
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-17
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-16
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-15
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.0-14
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.0-13
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.0-12
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.0-11
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.0-10
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.2.0-9
- Bump up version to compile with new go
* Thu Dec 17 2020 Ankit Jain <ankitja@vmware.com> 1.2.0-8
- Repo changed from github.com/mholt/caddy to github.com/caddyserver/caddy
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.2.0-7
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.0-6
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.2.0-5
- Bump up version to compile with go 1.13.3
* Sun Sep 22 2019 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-4
- Fix compilation issue (do not compile mholt/caddy).
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.2.0-3
- Bump up version to compile with new go
* Sun Sep 23 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-2
- Fix compilation issue.
- aarch64 support.
* Fri Aug 03 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.2.0-1
- Initial version of coredns 1.2.0.
