Summary:        An XML parser library
Name:           expat
Version:        2.2.9
Release:        9%{?dist}
License:        MIT
URL:            http://expat.sourceforge.net/
Group:          System Environment/GeneralLibraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.xz
%define sha1 expat=90a361e4c97f8c469479ffadc0de0b121a911fb5

Patch0:         CVE-2022-22822-27.patch
Patch1:         CVE-2021-45960-46143.patch
Patch2:         CVE-2022-23852.patch
Patch3:         CVE-2022-23990.patch
Patch4:         CVE-2022-25235_25236.patch
Patch5:         CVE-2022-25314_25315.patch
Patch6:         CVE-2022-25313.patch
patch7:         expat-CVE-2022-40674.patch

%description
The Expat package contains a stream oriented C library for parsing XML.

%prep
# Using autosetup is not feasible
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
sh ./configure \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --disable-static
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}/%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/%{_docdir}/%{name}
%{_fixperms} %{buildroot}/*

%check
make -k check %{?_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%doc AUTHORS Changes
%{_bindir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_includedir}/*

## TODO: There's some change in man page build path according to release notes.
## https://github.com/libexpat/libexpat/blob/R_2_2_7/expat/Changes
## #158 #263  CMake: Build man page in PROJECT_BINARY_DIR not _SOURCE_DIR
#%%{_mandir}/man1/*

%changelog
* Wed Sep 28 2022 Harinadh D <hdommaraju@vmware.com> 2.2.9-9
- Fix CVE-2022-40674
* Fri Mar 04 2022 Tapas Kundu <tkundu@vmware.com> 2.2.9-8
- Fix CVE-2022-25313
* Mon Feb 28 2022 Tapas Kundu <tkundu@vmware.com> 2.2.9-7
- Fix CVE-2022-25314 and CVE-2022-25315
* Fri Feb 25 2022 Tapas Kundu <tkundu@vmware.com> 2.2.9-6
- Fix CVE-2022-25235 and CVE-2022-25236
* Thu Feb 03 2022 Tapas Kundu <tkundu@vmware.com> 2.2.9-5
- Fix CVE-2022-23990
* Mon Jan 31 2022 Tapas Kundu <tkundu@vmware.com> 2.2.9-4
- Fix CVE-2022-23852
* Wed Jan 19 2022 Tapas Kundu <tkundu@vmware.com> 2.2.9-3
- Fix CVE-2021-45960 and CVE-2021-46143
* Mon Jan 17 2022 Tapas Kundu <tkundu@vmware.com> 2.2.9-2
- Fix CVE-2022-22822, CVE-2022-22823, CVE-2022-22824
- CVE-2022-22825, CVE-2022-22826, CVE-2022-22827
* Tue Jun 09 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 2.2.9-1
- Update to version 2.2.9 to fix CVE-2019-15903
* Mon Jul 8 2019 Siddharth Chandrasekaran <csiddharth@vmware.com> 2.2.4-2
- Add patch for CVE-2018-20843
* Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 2.2.4-1
- Updating version, fixes CVE-2017-9233,  CVE-2016-9063, CVE-2016-0718
* Fri Oct 21 2016 Kumar Kaushik <kaushikk@vmware.com> 2.2.0-1
- Updating Source/Fixing CVE-2015-1283.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.0-2
- GA - Bump release of all rpms
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.0-1
- Initial build.  First version
