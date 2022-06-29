Summary:        An URL retrieval utility and library
Name:           curl
Version:        7.83.1
Release:        2%{?dist}
License:        MIT
URL:            http://curl.haxx.se
Group:          System Environment/NetworkingLibraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://curl.haxx.se/download/%{name}-%{version}.tar.gz
%define sha1    %{name}=0073c0eb2d5199688334b8bd9f49e46c1f4ea35c
Patch0:         curl-CVE-2022-32205.patch
Patch1:         curl-CVE-2022-32206.patch
Patch2:         curl-CVE-2022-32207.patch
Patch3:         curl-libcurl-fix-for-Curl_fopen.patch
Patch4:         curl-CVE-2022-32208.patch

BuildRequires:  ca-certificates
BuildRequires:  openssl-devel
BuildRequires:  krb5-devel
BuildRequires:  libssh2-devel

Requires:       ca-certificates
Requires:       openssl
Requires:       krb5
Requires:       libssh2
Requires:       curl-libs = %{version}-%{release}

%description
The cURL package contains an utility and a library used for
transferring files with URL syntax to any of the following
protocols: FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET,
DICT, LDAP, LDAPS and FILE. Its ability to both download and
upload files can be incorporated into other programs to support
functions like streaming media.

%package devel
Summary:    Libraries and header files for curl
Requires:   %{name} = %{version}-%{release}
%description devel
Static libraries and header files for the support library for curl

%package libs
Summary: Libraries for curl
Group:      System Environment/Libraries
Requires:       ca-certificates-pki
%description libs
This package contains minimal set of shared curl libraries.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --enable-threaded-resolver \
    --with-ssl \
    --with-gssapi \
    --with-libssh2 \
    --with-ca-bundle=/etc/pki/tls/certs/ca-bundle.crt
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -v -d -m755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_mandir}/man3/*
%{_datarootdir}/aclocal/libcurl.m4
%{_docdir}/%{name}-%{version}

%files libs
%{_libdir}/libcurl.so.*

%changelog
* Tue Jun 28 2022 Dweep Advani <dadvani@vmware.com> 7.83.1-2
- Fixed CVE-2022-32205, CVE-2022-32206, CVE-2022-32207, CVE-2022-32208
* Thu Jun 16 2022 Dweep Advani <dadvani@vmware.com> 7.83.1-1
- Upgrade to 7.83.1 to fix multiple CVEs
* Thu May 19 2022 Dweep Advani <dadvani@vmware.com> 7.82.0-3
- Fix of curl issue 8559 causing OOM error in CN check
* Wed Apr 20 2022 Dweep Advani <dadvani@vmware.com> 7.82.0-2
- Fix CVE-2022-22576 and CVE-2022-27774
* Tue Mar 29 2022 Harinadh D <hdommaraju@vmware.com> 7.82.0-1
- Fix CVE-2022-22623
* Tue Sep 14 2021 Dweep Advani <dadvani@vmware.com> 7.78.0-2
- Fixed CVE-2021-22945, CVE-2021-22946, CVE-2021-22947
* Thu Aug 12 2021 Harinadh D <hdommaraju@vmware.com> 7.78.0-1
- Version update
* Thu Jul 22 2021 Harinadh D <hdommaraju@vmware.com> 7.75.0-4
- Fix CVE-2021-22924,CVE-2021-22925
- Disabled metalink to fix CVE-2021-22922,CVE-2021-22923
* Wed Jun 30 2021 Nitesh Kumar <kunitesh@vmware.com> 7.75.0-3
- Fix CVE-2021-22897
* Fri May 21 2021 Harinadh D <hdommaraju@vmware.com> 7.75.0-2
- Fix CVE-2021-22901,CVE-2021-22898
* Mon Mar 29 2021 Harinadh D <hdommaraju@vmware.com> 7.75.0-1
- Fix CVE-2021-22876,CVE-2021-22890
* Mon Dec 07 2020 Dweep Advani <dadvani@vmware.com> 7.59.0-12
- Patched for  CVE-2020-8284, CVE-2020-8285 and CVE-2020-8286
* Tue Aug 18 2020 Harinadh D <hdommaraju@vmware.com> 7.59.0-11
- Fix for CVE-2020-8231
* Wed Jun 17 2020 Ankit Jain <ankitja@vmware.com> 7.59.0-10
- Fix for CVE-2020-8177
* Mon Sep 23 2019 Dweep Advani <dadvani@vmware.com> 7.59.0-9
- Fix for CVE-2019-5481 and CVE-2019-5482
* Thu Jul 11 2019 Siddharth Chandrasekaran <csiddharth@vmware.com> 7.59.0-8
- Add patch for CVE-2018-16890
* Wed May 29 2019 Siju Maliakkal <smaliakkal@vmware.com> 7.59.0-7
- Patch for CVE-2019-5436
* Wed Feb 27 2019 Tapas Kundu <tkundu@vmware.com> 7.59.0-6
- Fix for CVE-2019-3822
* Thu Feb 14 2019 Dweep Advani <dadvani@vmware.com> 7.59.0-5
- Fix for CVE-2019-3823
* Tue Jan 29 2019 Dweep Advani <dadvani@vmware.com> 7.59.0-4
- Fix for CVE-2018-16839, CVE-2018-16840, CVE-2018-16842 and CVE-2018-14618
* Tue Sep 18 2018 Keerthana K <keerthanak@vmware.com> 7.59.0-3
- Fix for CVE-2018-0500
* Thu Jul 05 2018 Keerthana K <keerthanak@vmware.com> 7.59.0-2
- Fix for CVE-2018-1000300, CVE-2018-1000301.
* Wed Apr 04 2018 Dheeraj Shetty <dheerajs@vmware.com> 7.59.0-1
- Update to version 7.59.0
* Thu Feb 08 2018 Xiaolin Li <xiaolinl@vmware.com> 7.58.0-1
- Fix CVE-2017-8817.
* Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> 7.56.1-2
- Fix CVE-2017-8818.
* Wed Dec 13 2017 Xiaolin Li <xiaolinl@vmware.com> 7.56.1-1
- Update to version 7.56.1
* Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> 7.54.1-4
- Fix CVE-2017-1000257
* Mon Nov 06 2017 Xiaolin Li <xiaolinl@vmware.com> 7.54.1-3
- Fix CVE-2017-1000254
* Thu Nov 02 2017 Xiaolin Li <xiaolinl@vmware.com> 7.54.1-2
- Fix CVE-2017-1000099, CVE-2017-1000100, CVE-2017-1000101
* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 7.54.1-1
- Update to 7.54.1
* Mon Apr 24 2017 Bo Gan <ganb@vmware.com> 7.54.0-1
- Update to 7.54.0
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.51.0-5
- Added -libs subpackage
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 7.51.0-4
- Added -devel subpackage.
* Wed Nov 30 2016 Xiaolin Li <xiaolinl@vmware.com> 7.51.0-3
- Enable sftp support.
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 7.51.0-2
- Required krb5-devel.
* Wed Nov 02 2016 Anish Swaminathan <anishs@vmware.com> 7.51.0-1
- Upgrade curl to 7.51.0
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 7.50.3-2
- Modified %check
* Thu Sep 15 2016 Xiaolin Li <xiaolinl@vmware.com> 7.50.3-1
- Update curl to version 7.50.3.
* Tue Aug 23 2016 Xiaolin Li <xiaolinl@vmware.com> 7.47.1-3
- Enable gssapi in curl.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.47.1-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 7.47.1-1
- Updated to version 7.47.1
* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 7.46.0-1
- Updated to version 7.46.0
* Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 7.43.0-1
- Update to version 7.43.0.
* Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.41.0-1
- Update to version 7.41.0.
