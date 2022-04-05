Summary:	Crypto Libraries
Name:		libgcrypt
Version:	1.8.8
Release:	1%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            http://www.gnu.org/software/libgcrypt/
Source0:        ftp://ftp.gnupg.org/gcrypt/libgcrypt/%{name}-%{version}.tar.bz2
%define sha1 libgcrypt=ec927f6e85fe776482c84ec837ef2d9b83dc9c88
Patch0:         libgcrypt-00-ac_cv_sys_symbol_underscore.patch
Patch1:         libgcrypt-CVE-2019-12904-aes-move-tables.patch
Patch2:         libgcrypt-CVE-2019-12904-prefetch-gcm-table.patch
Patch3:         libgcrypt-CVE-2019-12904-gcm-move-tables.patch
Patch4:		libgcrypt-exponent-binding.patch
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
BuildRequires:	libgpg-error-devel
Requires:	libgpg-error
Distribution:	Photon
%description
The libgcrypt package contains a general purpose crypto library based on the code used in GnuPG. The library provides a high level interface to cryptographic building blocks using an extendable and flexible API.

%package devel
Summary:	Development libraries and header files for libgcrypt
Requires:	%{name} = %{version}-%{release}
Requires:	libgpg-error-devel

%description devel
The package contains libraries and header files for
developing applications that use libgcrypt.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_mandir}/man1/*
%{_libdir}/*.la
/usr/share/aclocal/libgcrypt.m4
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libgcrypt.pc
%changelog
*   Fri Feb 18 2022 Ankit Jain <ankitja@vmware.com> 1.8.8-1
-   Update to 1.8.8 and Fix exponent blinding issue
*   Mon Jun 21 2021 Ankit Jain <ankitja@vmware.com> 1.8.1-4
-   Fix for CVE-2021-33560
*   Thu Apr 02 2020 Ankit Jain <ankitja@vmware.com> 1.8.1-3
-   Fix for CVE-2019-12904
*   Mon Sep 03 2018 Ankit Jain <ankitja@vmware.com> 1.8.1-2
-   Fix for CVE-2018-0495
*   Tue Oct 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.1-1
-   Udpated to v1.8.1 to address CVE-2017-0379
*   Tue Apr 04 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.7.6-1
-   Udpated to version 1.7.6
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6.5-3
-   Required libgpg-error-devel.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.5-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  1.6.5-1
-   Upgrade to 1.6.5
*   Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 1.6.3-1
-   Initial build. First version
