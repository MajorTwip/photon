Summary:        Management tools and libraries relating to cryptography
Name:           openssl
Version:        1.0.2ze
Release:        1%{?dist}
License:        OpenSSL
URL:            http://www.openssl.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://www.openssl.org/source/vmware-OpenSSL_1_0_2ze.tar.gz
%define sha1    vmware-OpenSSL_1_0_2ze=2002e2aa0a49b8b8bfec153596269e7ecb02f4ae
Source1:        rehash_ca_certificates.sh

Patch0:         c_rehash.patch
Patch1:         openssl-ipv6apps.patch
Patch2:         openssl-init-conslidate.patch
Patch3:         openssl-drbg-default-read-system-fips.patch
Patch4:         fips-2.20-vmw.patch
Patch5:         openssl-optimized-curves.patch

%if %{with_check}
BuildRequires: zlib-devel
%endif

Requires:       bash
Requires:       glibc
Requires:       libgcc

%description
The OpenSSL package contains management tools and libraries relating
to cryptography. These are useful for providing cryptography
functions to other packages, such as OpenSSH, email applications and
web browsers (for accessing HTTPS sites).

%package devel
Summary: Development Libraries for openssl
Group: Development/Libraries
Requires: openssl = %{version}-%{release}
Obsoletes:  nxtgn-openssl-devel
%description devel
Header files for doing development with openssl.

%package perl
Summary: openssl perl scripts
Group: Applications/Internet
Requires: perl
Requires: openssl = %{version}-%{release}
%description perl
Perl scripts that convert certificates and keys to various formats.

%package c_rehash
Summary: openssl perl scripts
Group: Applications/Internet
Requires: perl
Requires: perl-DBI
Requires: perl-DBIx-Simple
Requires: perl-DBD-SQLite
Requires: openssl = %{version}-%{release}
%description c_rehash
Perl scripts that convert certificates and keys to various formats.

%prep
# Using autosetup is not feasible
%setup -q -n vmware-OpenSSL_1_0_2ze
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%if 0%{?_with_fips:1}
%patch4 -p1
%endif
%patch5 -p1

%build
export CFLAGS="%{optflags}"
./config \
    --prefix=%{_prefix} \
    --libdir=lib \
    --openssldir=/%{_sysconfdir}/ssl \
    shared \
    zlib-dynamic \
    %{?_with_fips} \
    -Wl,-z,noexecstack \
    -Wa,--noexecstack "${CFLAGS}" "${LDFLAGS}"
# make doesn't support _smp_mflags
make

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
# make doesn't support _smp_mflags
make INSTALL_PREFIX=%{buildroot} MANDIR=/usr/share/man MANSUFFIX=ssl install
install -p -m 755 -D %{SOURCE1} %{buildroot}%{_bindir}/
ln -sf libssl.so.1.0.0 %{buildroot}%{_libdir}/libssl.so.1.0.2
ln -sf libcrypto.so.1.0.0 %{buildroot}%{_libdir}/libcrypto.so.1.0.2

%check
# make doesn't support _smp_mflags
make tests

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sysconfdir}/ssl/certs
%{_sysconfdir}/ssl/misc/CA.sh
%{_sysconfdir}/ssl/misc/c_hash
%{_sysconfdir}/ssl/misc/c_info
%{_sysconfdir}/ssl/misc/c_issuer
%{_sysconfdir}/ssl/misc/c_name
%{_sysconfdir}/ssl/openssl.cnf
%{_sysconfdir}/ssl/private
%{_bindir}/openssl
%{_libdir}/*.so.*
%{_libdir}/engines/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files devel
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_libdir}/*.so

%files perl
/%{_sysconfdir}/ssl/misc/tsget
/%{_sysconfdir}/ssl/misc/CA.pl

%files c_rehash
/%{_bindir}/c_rehash
/%{_bindir}/rehash_ca_certificates.sh

%changelog
* Wed May 04 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.2ze-1
- Update to openssl 1.0.2ze
* Wed Mar 16 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.2zc-1
- Update to openssl 1.0.2zc
* Thu Mar 10 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.2za-2
- Fix CVE-2022-0778
* Tue Aug 24 2021 Srinidhi Rao <srinidhir@vmware.com> 1.0.2za-1
- Update to openssl 1.0.2za
* Thu Feb 25 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.2y-1
- update openssl to 1.0.2y
* Mon Dec 21 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.2x-2
- modify FIPS EC list to only use optimized curves
* Fri Dec 11 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.2x-1
- Update to openssl 1.0.2x
* Fri Dec 04 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.0.2w-2
- Fix CVE-2020-1971
* Sat Sep 12 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2w-1
- Update to 1.0.2w
- Fix CVE-2020-1968
* Wed Jul 29 2020 Srinidhi Rao <srinidhir@vmware.com> 1.0.2v-2
- Improve the patch openssl-drbg-default-read-system-fips
- Modifies RAND_get_rand_method() to supply default FIPS RNG.
* Tue May 26 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2v-1
- Update to 1.0.2v.
- Included fix for Implement blinding for scalar multiplication.
* Fri Feb 07 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2u-3
- Use fips 2.0.20
* Fri Jan 31 2020 Anish Swaminathan <anishs@vmware.com> 1.0.2u-2
- Configure with Wl flag.
* Thu Jan 09 2020 Tapas Kundu <tkundu@vmware.com> 1.0.2u-1
- Updated to 1.0.2u
- Fix CVE-2019-1551
* Thu Sep 26 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2t-2
- OpenSSL devel conflicts nextgen-OpenSSL-devel
* Thu Sep 19 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2t-1
- Updated to 1.0.2t
- Fix multiple CVEs
* Fri Jun 07 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2s-1
- Updated to 1.0.2s
* Mon Mar 25 2019 Tapas Kundu <tkundu@vmware.com> 1.0.2r-1
- Updated to 1.0.2r for CVE-2019-1559
* Thu Dec 06 2018 Sujay G <gsujay@vmware.com> 1.0.2q-1
- Bump version to 1.0.2q
* Fri Aug 17 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.0.2p-1
- Upgrade to 1.0.2p
* Mon Aug 13 2018 Ankit Jain <ankitja@vmware.com> 1.0.2o-3
- Fix of CVE-2018-0732
* Wed Jul 25 2018 Ankit Jain <ankitja@vmware.com> 1.0.2o-2
- Fix of CVE-2018-0737
* Tue Apr 03 2018 Anish Swaminathan <anishs@vmware.com> 1.0.2o-1
- Upgrade to 1.0.2o- Fixes CVE-2017-3738, CVE-2018-0733, CVE-2018-0739
* Wed Mar 21 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.0.2n-2
- Add script which rehashes the certificates
* Tue Jan 02 2018 Xiaolin Li <xiaolinl@vmware.com> 1.0.2n-1
- Upgrade to 1.0.2n
* Tue Nov 07 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2m-1
- Upgrade to 1.0.2m
* Tue Oct 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.2l-2
- Fix CVE-2017-3735 OOB read.
* Fri Aug 11 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2l-1
- Upgrade to 1.0.2l
* Thu Aug 10 2017 Chang Lee <changlee@vmware.com> 1.0.2k-4
- Add zlib-devel for %check
* Fri Jul 28 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2k-3
- Patch to support enabling FIPS_mode through kernel parameter
* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 1.0.2k-2
- Fix symlink
* Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2k-1
- Upgrade to 1.0.2k
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.2j-3
- Moved man3 to devel subpackage.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.0.2j-2
- Modified %check
* Mon Sep 26 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2j-1
- Update to 1.0.2.j
* Wed Sep 21 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.2h-5
- Security bug fix, CVE-2016-2182.
* Tue Sep 20 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.2h-4
- Security bug fix, CVE-2016-6303.
* Wed Jun 22 2016 Anish Swaminathan <anishs@vmware.com> 1.0.2h-3
- Add patches for using openssl_init under all initialization and changing default RAND
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.2h-2
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.0.2h-1
- Upgrade to 1.0.2h
* Mon Mar 07 2016 Anish Swaminathan <anishs@vmware.com> 1.0.2g-1
- Upgrade to 1.0.2g
* Wed Feb 03 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.2f-1
- Update to version 1.0.2f
* Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 1.0.2e-3
- Add symlink for libcrypto
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.2e-2
- Move c_rehash to a seperate subpackage.
* Fri Dec 04 2015 Xiaolin Li <xiaolinl@vmware.com> 1.0.2e-1
- Update to 1.0.2e.
* Wed Dec 02 2015 Anish Swaminathan <anishs@vmware.com> 1.0.2d-3
- Follow similar logging to previous openssl versions for c_rehash.
* Fri Aug 07 2015 Sharath George <sharathg@vmware.com> 1.0.2d-2
- Split perl scripts to a different package.
* Fri Jul 24 2015 Chang Lee <changlee@vmware.com> 1.0.2d-1
- Update new version.
* Wed Mar 25 2015 Divya Thaluru <dthaluru@vmware.com> 1.0.2a-1
- Initial build.  First version
