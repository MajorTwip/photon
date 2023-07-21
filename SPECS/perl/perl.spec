%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)
# Filter dependencies on private modules. Generator:
# for F in $(find lib -type f); do perl -e '$/ = undef; $_ = <>; if (/^package #\R([\w:]*);/m) { print qq{|^perl\\\\($1\\\\)} }' "$F"; done
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Locale::Codes::Country_Retired\\)|^perl\\(Locale::Codes::LangFam_Retired\\)|^perl\\(Locale::Codes::Script_Retired\\)|^perl\\(Locale::Codes::LangExt_Codes\\)|^perl\\(Locale::Codes::LangFam_Codes\\)|^perl\\(Locale::Codes::Script_Codes\\)|^perl\\(Locale::Codes::Language_Codes\\)|^perl\\(Locale::Codes::LangExt_Retired\\)|^perl\\(Locale::Codes::Currency_Codes\\)|^perl\\(Locale::Codes::LangVar_Retired\\)|^perl\\(Locale::Codes::Language_Retired\\)|^perl\\(Locale::Codes::Country_Codes\\)|^perl\\(Locale::Codes::LangVar_Codes\\)|^perl\\(Locale::Codes::Currency_Retired\\)

Summary:        Practical Extraction and Report Language
Name:           perl
Version:        5.28.0
Release:        8%{?dist}
License:        GPLv1+
URL:            http://www.perl.org/
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.cpan.org/src/5.0/%{name}-%{version}.tar.gz
%define sha512  %{name}=61b62fdc0e473fe45c62f403d06daa3f0c20730e0a4b29762bccf353e060db812ea5bb9245e32a8706cb3e29b67bcbc23cb922fd1d32f2b0a54b177826b13f36
Patch0:         perl-CVE-2018-18311.patch
Patch1:         perl-CVE-2018-18312.patch
%if 0%{?with_check}
Patch2:         make-check-failure.patch
Patch3:         make-check-failure2.patch
%endif
Patch4:         perl-CVE-2020-10543.patch
Patch5:         perl-CVE-2020-10878.patch
Patch6:         perl-CVE-2020-12723.patch
Patch7: CVE-2023-31486.patch
Provides:       perl >= 0:5.003000
Provides:       perl(getopts.pl)
Provides:       perl(s)
Provides:       /bin/perl
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  gdbm-devel
Requires:       zlib
Requires:       gdbm
Requires:       glibc
Requires:       libgcc
%description
The Perl package contains the Practical Extraction and
Report Language.
%prep
# Using autosetup is not feasible
%setup -q
%patch0 -p1
%patch1 -p1
%if 0%{?with_check}
%patch2 -p1
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
sed -i 's/-fstack-protector/&-all/' Configure

%build
export BUILD_ZLIB=False
export BUILD_BZIP2=0
CFLAGS="%{_optflags}"

sh Configure -des \
    -Dprefix=%{_prefix} \
    -Dvendorprefix=%{_prefix} \
    -Dman1dir=%{_mandir}/man1 \
    -Dman3dir=%{_mandir}/man3 \
    -Dpager=%{_bindir}"/less -isR" \
    -Duseshrplib \
    -Dusethreads \
        -DPERL_RANDOM_DEVICE="/dev/erandom"

make VERBOSE=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
unset BUILD_ZLIB BUILD_BZIP2
%check
sed -i '/02zlib.t/d' MANIFEST
sed -i '/cz-03zlib-v1.t/d' MANIFEST
sed -i '/cz-06gzsetp.t/d' MANIFEST
sed -i '/porting\/podcheck.t/d' MANIFEST
make test TEST_SKIP_VERSION_CHECK=1 %{?_smp_mflags}
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_libdir}/perl5
%dir %{_libdir}/perl5/%{version}
%{_libdir}/perl5/%{version}/*
%{_mandir}/*/*

%changelog
*   Mon Jul 17 2023 Kuntal Nayak <nkuntal@vmware.com> 5.28.0-8
-   Patch fixed CVE-2023-31486
*   Tue Jun 16 2020 Prashant S Chauhan <psinghchauha@vmware.com> 5.28.0-7
-   Added patches, Fix CVE-2020-10878, Fix CVE-2020-12723
*   Mon Jun 15 2020 Dweep Advani <dadvani@vmware.com> 5.28.0-6
-   Patched for fixing CVE-2020-10543
*   Tue Feb 25 2020 Prashant S Chauhan <psinghchauha@vmware.com> 5.28.0-5
-   Added a patch to fix make check
*   Tue Oct 22 2019 Prashant S Chauhan <psinghchauha@vmware.com> 5.28.0-4
-   Fix for make check failure added a patch
*   Tue Feb 26 2019 Dweep Advani <dadvani@vmware.com> 5.28.0-3
-   Fixed CVE-2018-18311 and CVE-2018-18312
*   Wed Oct 24 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.28.0-2
-   Add provides perl(s)
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 5.28.0-1
-   Upgrade to version 5.28.0
*   Tue Oct 03 2017 Dheeraj Shetty <dheerajs@vmware.com> 5.24.1-4
-   CVE-2017-12837 and CVE-2017-12883 patch from
-   https://perl5.git.perl.org/perl.git/commitdiff/2be4edede4ae226e2eebd4eff28cedd2041f300f#patch1
*   Wed Jul 05 2017 Xiaolin Li <xiaolinl@vmware.com> 5.24.1-3
-   Rebuild perl after adding gdbm-devel package.
*   Thu Jun 15 2017 Chang Lee <changlee@vmware.com> 5.24.1-2
-   Updated %check
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 5.24.1-1
-   Update to 5.24.1.
*   Thu Oct 20 2016 Xiaolin Li <xiaolinl@vmware.com> 5.22.1-5
-   CVE-2016-1238 patch from http://perl5.git.perl.org/perl.git/commit/cee96d52c39b1e7b36e1c62d38bcd8d86e9a41ab.
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 5.22.1-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.22.1-3
-   GA - Bump release of all rpms
*   Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 5.22.1-2
-   Enable threads
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com> 5.22.1-1
-   Update version
*   Thu Jun 4 2015 Touseef Liaqat <tliaqat@vmware.com> 5.18.2-2
-   Provide /bin/perl.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.18.2-1
-   Initial build. First version
