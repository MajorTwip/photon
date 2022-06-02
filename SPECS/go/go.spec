%global goroot          /usr/lib/golang
%global gopath          %{_datadir}/gocode
%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif
%define debug_package %{nil}
%define __strip /bin/true

Summary:        Go
Name:           go
Version:        1.18.1
Release:        1%{?dist}
License:        BSD
URL:            https://golang.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://golang.org/dl/%{name}%{version}.src.tar.gz
%define sha512  go=baa053e2d713b235b9285c946b4f0842085a5224d1f4cbe92a446fbf97ed9f7289c8d4ba212fb31dd2e4eac39bb4c015f478543a1856594c2d1fc331c946f571
Requires:       glibc

%define ExtraBuildRequires go

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.

%prep
%autosetup -p1 -n %{name}

%build
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOROOT_BOOTSTRAP=%{goroot}

export GOROOT="`pwd`"
export GOPATH=%{gopath}
export GOROOT_FINAL=%{_bindir}/go
rm -f  %{gopath}/src/runtime/*.c
pushd src
./make.bash --no-clean
popd

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{goroot}

cp -R api bin doc lib pkg src misc VERSION %{buildroot}%{goroot}

# remove the unnecessary zoneinfo file (Go will always use the system one first)
rm -rfv %{buildroot}%{goroot}/lib/time

# remove the doc Makefile
rm -rfv %{buildroot}%{goroot}/doc/Makefile

# put binaries to bindir, linked to the arch we're building,
# leave the arch independent pieces in %{goroot}
mkdir -p %{buildroot}%{goroot}/bin/linux_%{gohostarch}
ln -sfv ../go %{buildroot}%{goroot}/bin/linux_%{gohostarch}/go
ln -sfv ../gofmt %{buildroot}%{goroot}/bin/linux_%{gohostarch}/gofmt
ln -sfv %{goroot}/bin/gofmt %{buildroot}%{_bindir}/gofmt
ln -sfv %{goroot}/bin/go %{buildroot}%{_bindir}/go

# ensure these exist and are owned
mkdir -p %{buildroot}%{gopath}/src/github.com/
mkdir -p %{buildroot}%{gopath}/src/bitbucket.org/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/p/
install -vdm755 %{buildroot}/etc/profile.d
cat >> %{buildroot}/etc/profile.d/go-exports.sh <<- "EOF"
export GOROOT=%{goroot}
export GOPATH=%{_datadir}/gocode
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOOS=linux
EOF
#chown -R root:root %{buildroot}/etc/profile.d/go-exports.sh
#%%{_fixperms} %{buildroot}/*

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  #This is uninstall
  rm /etc/profile.d/go-exports.sh
  rm -rf /opt/%{name}
  exit 0
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%exclude %{goroot}/src/*.rc
%exclude %{goroot}/include/plan9
/etc/profile.d/go-exports.sh
%{goroot}/*
%{gopath}/src
%exclude %{goroot}/src/pkg/debug/dwarf/testdata
%exclude %{goroot}/src/pkg/debug/elf/testdata
%ifarch aarch64
%exclude %{goroot}/src/debug/dwarf/testdata
%exclude %{goroot}/src/debug/elf/testdata
%endif
%{_bindir}/*

%changelog
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.1-1
- Upgrade to 1.18.1.
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.2-3
- Fix for CVE-2022-23806, CVE-2022-23772, CVE-2022-23773.
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.2-2
- Fix for CVE-2021-44716, CVE-2021-44717.
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.2-1
- Upgrade to 1.17.2
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.7-1
- Upgrade to 1.16.7
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.5-1
- Update to 1.16.5
* Thu Mar 25 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.2-1
- Update to 1.16.2
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.15.8-1
- Update to 1.15.8
* Fri Jan 15 2021 Piyush Gupta <gpiyush@vmware.com> 1.15.6-1
- Update to 1.15.6
* Wed Oct 28 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.14.8-2
- Fix glibc dependency on aarch64
* Tue Oct 06 2020 Ashwin H <ashwinh@vmware.com> 1.14.8-1
- Update to 1.14.8
* Thu Mar 05 2020 <ashwinh@vmware.com> 1.14-1
- Initial build for 1.14
