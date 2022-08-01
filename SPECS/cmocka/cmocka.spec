Summary:       unit testing framework for C
Name:          cmocka
Version:       1.1.5
Release:       3%{?dist}
Group:         Development/Libraries
Vendor:        VMware, Inc.
License:       Apache 2.0
URL:           https://cmocka.org
Distribution:  Photon

Source0:       https://cmocka.org/files/1.1/%{name}-%{version}.tar.xz
%define sha512 %{name}=cad7f04757183d004f6eaad39036fc0e24c5e0e987f80e85bc43bc66dba22389cb02b08e25531cc28a541d0a24a86b29be134a2d6fc339128e87d66952f502bd

BuildRequires: cmake

%description
an elegant unit testing framework for C with support for mock objects. It only requires the standard C library, works on a range of computing platforms (including embedded) and with different compilers.

%package devel
Summary:    Develeopment headers and libraries for %{name}.
Requires:   %{name} = %{version}-%{release}

%description     devel
Develeopment headers and libraries for %{name}.

%prep
%autosetup -p1

%build
mkdir build && cd build
cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    ..

%make_build

%install
cd build
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libcmocka.*

%files devel
%defattr(-,root,root)
%{_libdir}/cmake
%{_libdir}/pkgconfig/cmocka.pc
%{_includedir}/*

%changelog
* Mon Aug 01 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.5-3
- Add devel sub package
* Thu Jun 25 2020 Ajay Kaher <akaher@vmware.com> 1.1.5-2
- Corrected include file path
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.5-1
- Automatic Version Bump
* Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 1.1.2-1
- Upgraded to version 1.1.2
* Fri Jun 29 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.1-1
- Initial
