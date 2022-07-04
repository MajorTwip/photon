Summary:        Linux Pluggable Authentication Modules
Name:           Linux-PAM
Version:        1.4.0
Release:        5%{?dist}
License:        BSD and GPLv2+
URL:            https://github.com/linux-pam/linux-pam/releases
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/linux-pam/linux-pam/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512  %{name}=26eda95c45598a500bc142da4d1abf93d03b3bbb0f2390fa87c72dcbffa208dbfa115c0b411095c31ee9955e36422ccf3e2df3bd486818fafffef8c4310798c4

Source1:        pamtmp.conf

Patch0:         faillock-add-support-to-print-login-failures.patch

BuildRequires: libselinux-devel
BuildRequires: gdbm-devel

Requires: libselinux
Requires: gdbm

%define ExtraBuildRequires systemd-rpm-macros

%description
The Linux PAM package contains Pluggable Authentication Modules used to
enable the local system administrator to choose how applications authenticate users.

%package        lang
Summary:        Additional language files for Linux-PAM
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}
%description    lang
These are the additional language files of Linux-PAM.

%package        devel
Summary:        Development files for Linux-PAM
Group:          System Environment/Base
Requires:       %{name} = %{version}-%{release}

%description    devel
The Linux-PAM-devel package contains libraries, header files and documentation
for developing applications that use Linux-PAM.

%prep
%autosetup -p1

%build
sh ./configure --host=%{_host} --build=%{_build} \
    $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}") \
    CFLAGS="%{optflags}" \
    CXXFLAGS="%{optflags}" \
    --disable-dependency-tracking \
    --prefix=%{_prefix} \
    --exec-prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir}/security \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-selinux \
    --docdir=%{_docdir}/%{name}-%{version} \
    --enable-securedir=%{_libdir}/security \
    --enable-db=ndbm

%make_build

%install
%make_install %{?_smp_mflags}
chmod -v 4755 %{buildroot}%{_sbindir}/unix_chkpwd
install -v -dm755 %{buildroot}%{_docdir}/%{name}-%{version}
ln -sfv pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_auth.so
ln -sfv pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_acct.so
ln -sfv pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_passwd.so
ln -sfv pam_unix.so %{buildroot}%{_libdir}/security/pam_unix_session.so
find %{buildroot}%{_libdir} -name '*.la' -delete

install -d -m 755 %{buildroot}/var/run/faillock
install -m644 -D %{SOURCE1} %{buildroot}%{_libdir}/tmpfiles.d/pam.conf

%{find_lang} %{name}

%{_fixperms} %{buildroot}/*

%check
%if 0%{?with_check}
install -v -m755 -d /etc/pam.d
cat > /etc/pam.d/other << "EOF"
auth     required       pam_deny.so
account  required       pam_deny.so
password required       pam_deny.so
session  required       pam_deny.so
EOF
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/security/*.conf
%{_sysconfdir}/environment
%{_sysconfdir}/security
%{_sbindir}/*
%{_lib}/security/*
%{_libdir}/*.so*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_unitdir}/pam_namespace.service
%dir /var/run/faillock
%{_libdir}/tmpfiles.d/pam.conf

%files lang -f Linux-PAM.lang
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_docdir}/%{name}-%{version}/*

%changelog
* Thu Jun 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.0-5
- Further fixes to faillock patch
* Wed Mar 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.0-4
- Remove db support from pam
* Tue Mar 08 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.0-3
- create /var/run/faillock during install
* Fri Sep 25 2020 Ankit Jain <ankitja@vmware.com> 1.4.0-2
- pam_cracklib has been deprecated.
* Fri Aug 07 2020 Vikash Bansal <bvikas@vmware.com> 1.4.0-1
- Version bump up to 1.4.0
* Mon Apr 20 2020 Alexey Makhalov <amakhalov@vmware.com> 1.3.0-3
- Enable SELinux support
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.3.0-2
- Cross compilation support
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.0-1
- Version update.
* Fri Feb 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-5
- Added pam_unix_auth.so, pam_unix_acct.so, pam_unix_passwd.so,
- and pam_unix_session.so.
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-4
- Added devel subpackage.
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com> 1.2.1-3
- Packaging pam cracklib module
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-2
- GA - Bump release of all rpms
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-1
- Updated to version 1.2.1
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.1.8-2
- Update according to UsrMove.
* Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.8-1
- Initial build.  First version
