Summary:        Cmake-3.13.5
Name:           cmake
Version:        3.13.5
Release:        2%{?dist}
License:        BSD and LGPLv2+
URL:            http://www.cmake.org/
Source0:        http://www.cmake.org/files/v3.13/%{name}-%{version}.tar.gz
%define sha512 cmake=99e3a8f5bc147dd90b9cab11f06892d87f289aa1354ad323711fe96ebc9c32b1e887e8f9d3575a37831c4d2153a070ff9115c5e27a185d54170bad9dbbaabc26
Source1:        macros.cmake
Patch0:         disableUnstableUT.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ncurses-devel
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  curl
BuildRequires:  curl-devel
BuildRequires:  expat-libs
BuildRequires:  expat-devel
BuildRequires:  zlib
BuildRequires:  zlib-devel
BuildRequires:  libarchive
BuildRequires:  libarchive-devel
BuildRequires:  bzip2
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
BuildRequires:  xz-libs
BuildRequires:  libarchive
BuildRequires:  libuv-devel
BuildRequires:  libuv
Requires:       ncurses
Requires:       expat
Requires:       zlib
Requires:       libarchive
Requires:       bzip2
Requires:       xz-libs
Requires:       libarchive
Requires:       libuv
Requires:       curl-libs

%description
CMake is an extensible, open-source system that manages the build process in an
operating system and in a compiler-independent manner.
%prep
%autosetup -p1

%build
ncores="$(/usr/bin/getconf _NPROCESSORS_ONLN)"
./bootstrap \
  --prefix=%{_prefix} \
  --system-expat \
  --system-zlib \
  --system-curl \
  --system-libarchive \
  --system-bzip2 \
  --system-liblzma \
  --system-libarchive \
  --system-libuv \
  --parallel=$ncores
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
install -Dpm0644 %{SOURCE1} %{buildroot}%{_libdir}/rpm/macros.d/macros.cmake

%check
make  %{?_smp_mflags} test

%files
%defattr(-,root,root)
/usr/share/%{name}-*/*
%{_bindir}/*
/usr/doc/%{name}-*/*
/usr/share/aclocal/*
%{_libdir}/rpm/macros.d/macros.cmake

%changelog
*       Fri Jun 16 2023 Anmol Jain <anmolja@vmware.com> 3.13.5-2
-       build using system curl
*       Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 3.13.5-1
-       Upgrade to 3.13.5
*       Fri Mar 20 2020 Dweep Advani <dadvani@vmware.com> 3.12.1-5
-       Add system provided libs.
*       Thu Jan 17 2019 Ankit Jain <ankitja@vmware.com> 3.12.1-4
-       Removed unnecessary libgcc-devel buildrequires
*       Thu Dec 06 2018 <ashwinh@vmware.com> 3.12.1-3
-       Bug Fix 2243672. Add system provided libs.
*       Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 3.12.1-2
-       smp make (make -jN)
-       specify /usr/lib as CMAKE_INSTALL_LIBDIR
*       Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 3.12.1-1
-       Upgrading version to 3.12.1
-       Adding macros.cmake
*       Fri Sep 29 2017 Kumar Kaushik <kaushikk@vmware.com> 3.8.0-4
-       Building using system expat libs.
*       Thu Aug 17 2017 Kumar Kaushik <kaushikk@vmware.com> 3.8.0-3
-       Fixing make check bug # 1632102.
*       Tue May 23 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.8.0-2
-       bug 1448414: Updated to build in parallel
*       Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  3.8.0-1
-       Upgrade to 3.8.0
*       Thu Oct 06 2016 ChangLee <changlee@vmware.com> 3.4.3-3
-       Modified %check
*       Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.3-2
-       GA - Bump release of all rpms
*       Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.4.3-1
-       Updated version.
*       Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 3.2.1.2
-       Updated group.
*       Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.1-1
-       Update to 3.2.1
*       Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.2-1
-       Initial build. First version
