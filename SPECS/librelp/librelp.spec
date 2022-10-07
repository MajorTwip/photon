Summary:    RELP Library
Name:       librelp
Version:    1.2.18
Release:    2%{?dist}
License:    GPLv3+
URL:        http://www.librelp.com
Source0:    http://download.rsyslog.com/librelp/%{name}-%{version}.tar.gz
%define sha512 librelp=7193438238b7019e7a4944d6d900a1fa5a369ff8a6b97a6dca7e82b6637c0f391ec3554eeeaa285881457cb2abe72fa1a893244ec9a36cc9d2e2592d58c5462a
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
BuildRequires:  gnutls-devel
BuildRequires:  autogen
Requires:   gnutls
%description
Librelp is an easy to use library for the RELP protocol. RELP (stands
for Reliable Event Logging Protocol) is a general-purpose, extensible
logging protocol.

%package devel
Summary:    Development libraries and header files for librelp
Requires:   %{name} = %{version}-%{release}

%description devel
The package contains libraries and header files for
developing applications that use librelp.

%prep
%autosetup -p1
autoreconf -fiv

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
#There are two tests(out of 16) which run under valgrind.
#Currently these two tests just greps for a message output after test.
#If we need to enable valgrind, it needs 'unstripped' version of ld.so
#This is available in glibc-debuginfo which needs to be installed in
#sandbox environment. This needs tdnf package which in turn needs to
#install glibc-debuginfo package (which has unstripped version of ld.so).
#Due to above dependecy overhead which needs more analysis
#and since tests are not using any valgrind functionality,
#disabling valgrind.
sed -ie 's/export valgrind=.*/export valgrind""/' tests/test-framework.sh

# * TODO *
# tls-basic-brokencert test is broken and it is mentioned in the official git
# repo (https://github.com/rsyslog/librelp/blob/master/tests/Makefile.am)
# Comment says:
# reenable tests when stable tls-basic-brokencert.sh. This holds good till
# librelp-1.4.0 release.
sed -i '/tls-basic-brokencert.sh \\/d' tests/Makefile.am

make check %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.18-2
- Remove .la files
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.18-1
- Automatic Version Bump
* Mon Aug 19 2019 Shreenidhi Shedi <sshedi@vmware.com> 1.2.17-3
- Further fix for make check
* Tue Nov 20 2018 Ashwin H <ashwinh@vmware.com> 1.2.17-2
- Fix librelp %check
* Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 1.2.17-1
- Updated to version 1.2.17
* Tue Apr 11 2017 Harish Udaiy Kumar <hudaiyakumar@vmware.com> 1.2.13-1
- Updated to version 1.2.13
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.9-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.2.9-1
- Upgrade to 1.2.9
* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.2.7-1
- Initial build. First version
