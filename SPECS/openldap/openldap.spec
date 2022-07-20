%global _default_patch_fuzz 2
Summary:        OpenLdap-2.4.43
Name:           openldap
Version:        2.4.57
Release:        3%{?dist}
License:        OpenLDAP
URL:            http://cyrusimap.web.cmu.edu/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{name}-%{version}.tgz
%define sha1 openldap=1cffa70a3ea8545948041fd113f8f53bc24d6d87

Patch0:         openldap-2.4.51-consolidated-2.patch
Patch1:         openldap-2.4.40-gssapi-1.patch
Patch2:         openldap-CVE-2021-27212.patch
Patch3:         openldap-CVE-2022-29155.patch

Requires:       openssl >= 1.0.1, cyrus-sasl >= 2.1

BuildRequires:  cyrus-sasl >= 2.1
BuildRequires:  openssl-devel >= 1.0.1
BuildRequires:  groff
BuildRequires:  e2fsprogs-devel

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%prep
%autosetup -p1

%build
autoconf

sed -i '/6.0.20/ a\\t__db_version_compat' configure

CPPFLAGS="-D_REENTRANT -DLDAP_CONNECTIONLESS -D_GNU_SOURCE -D_AVL_H" \
sh ./configure \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --libdir=%{_libdir} \
        --sysconfdir=/etc   \
        --disable-static    \
        --disable-debug     \
        --disable-slapd     \
        --with-tls=openssl

make depend %{?_smp_mflags}
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*

%check
make -k check %{?_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
/etc/openldap/*

%changelog
* Tue Jul 19 2022 Mukul Sikka <msikka@vmware.com> 2.4.57-3
- Fix CVE-2022-29155
* Tue Mar 02 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.57-2
- Fix CVE CVE-2021-27212
* Mon Feb 01 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.57-1
- Upgrade to 2.4.57 to fix several crtical CVEs
* Mon Dec 14 2020 Dweep Advani <dadvani@vmware.com> 2.4.43-5
- Patched for CVE-2020-25692
* Tue May 12 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.4.43-4
- Fix CVE-2020-12243
* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 2.4.43-3
- Applied patch for CVE-2017-9287
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.43-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.43-1
- Updated to version 2.4.43
* Fri Aug 14 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.40-2
- Patches for CVE-2015-1545 and CVE-2015-1546.
* Wed Oct 08 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.40-1
- Initial build.        First version
