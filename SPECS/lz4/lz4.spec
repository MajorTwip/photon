Summary:        Extremely fast compression.
Name:           lz4
Version:        1.9.3
Release:        2%{?dist}
License:        BSD 2-Clause and GPLv2
URL:            http://lz4.github.io/lz4
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/lz4/lz4/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=c246b0bda881ee9399fa1be490fa39f43b291bb1d9db72dba8a85db1a50aad416a97e9b300eee3d2a4203c2bd88bda2762e81bc229c3aa409ad217eb306a454c

Patch0: CVE-2021-3520.patch

%description
LZ4 is lossless compression algorithm, providing compression speed
at 400 MB/s per core, scalable with multi-cores CPU.

It features an extremely fast decoder, with speed in multiple GB/s
per core, typically reaching RAM speed limits on multi-core systems.

%package devel
Summary:        Libraries and header files for lz4
Requires:       %{name} = %{version}-%{release}

%description    devel
Static libraries and header files for the support library for lz4.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX="%{_usr}" %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblz4.so.*
%{_datadir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/liblz4.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Mon Jun 14 2021 Michelle Wang <michellew@vmware.com> 1.9.3-2
- Add Patch CVE-2021-3520
* Thu Dec 17 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.3-1
- Automatic Version Bump
* Mon Apr 20 2020 Michelle Wang <michellew@vmware.com> 1.9.2-1
- Update lz4 to 1.9.2 for CVE-2019-17543
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.8.2-1
- Update to version 1.8.2
* Wed Mar 29 2017 Michelle Wang <michellew@vmware.com> 1.7.5-1
- Update lz4 package to 1.7.5.
* Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.4-1
- Add lz4 package.
