Summary:        GNU Parted manipulates partition tables
Name:           parted
Version:        3.2
Release:        10%{?dist}
License:        GPLv3+
URL:            http://ftp.gnu.org/gnu/parted/parted-3.2.tar.xz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnu.org/gnu/parted/%{name}-%{version}.tar.xz
%define sha512 parted=b51c6f067496591f0231f642a222ca2f368e9690bd4114bac76da543f32980864c1c71f0213be08f610bcdfb940f202bdd58dce7ddde8b5b2ec9120e8efc798e

Conflicts:      toybox < 0.8.2-2

%description
This is useful for creating space for new operating systems,
reorganizing disk usage, copying data on hard disks and disk imaging.
The package contains a library, libparted, as well as well as a
command-line frontend, parted, which can also be used in scripts.

%prep
%autosetup -p1

%build
#Add a header to allow building with glibc-2.28 or later
sed -i '/utsname.h/a#include <sys/sysmacros.h>' libparted/arch/linux.c

%configure --without-readline \
    --disable-debug \
	--disable-nls \
    --disable-device-mapper

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_infodir}/*
%{_datadir}/*
%exclude %{_infodir}/dir

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2-10
- Remove .la files
* Tue Oct 27 2020 Dweep Advani <dadvani@vmware.com> 3.2-9
- Remove conflict causing /usr/share/info/dir from packaging
* Fri Jul 03 2020 Prashant S Chauhan <psinghchauha@vmware.com> 3.2-8
- Do not conflict with toybox >= 0.8.2-2
* Tue Oct 2 2018 Michelle Wang <michellew@vmware.com> 3.2-7
- Add conflict toybox.
* Sun Sep 09 2018 Alexey Makhalov <amakhalov@vmware.com> 3.2-6
- Fix compilation issue against glibc-2.28.
* Wed Aug 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-5
- Fix summary and description.
* Tue Jun 06 2017 ChangLee <changlee@vmware.com> 3.2-4
- Remove %check.
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 3.2-3
- Modified %check.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2-2
- GA Bump release of all rpms.
* Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.2-1
- Initial version.
