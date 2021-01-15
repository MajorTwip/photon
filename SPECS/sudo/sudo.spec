Summary:	Sudo
Name:		sudo
Version:	1.9.5
Release:	1%{?dist}
License:	ISC
URL:		https://www.kernel.org/pub/linux/libs/pam/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.sudo.ws/sudo/dist/%{name}-%{version}.tar.gz
%define sha1 sudo=1e9fccda4beccca811ecb48866776388c9c377ae
BuildRequires:	man-db
BuildRequires:	Linux-PAM
Requires:	Linux-PAM
Requires:	shadow

%description
The Sudo package allows a system administrator to give certain users (or groups of users)
the ability to run some (or all) commands as root or another user while logging the commands and arguments.

%prep
%setup -q

%build

./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libexecdir=%{_libdir} \
    --docdir=%{_docdir}/%{name}-%{version} \
    --with-all-insults \
    --with-env-editor \
    --with-pam \
    --with-pam-login \
    --with-passprompt="[sudo] password for %p"

make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}
install -v -dm755 %{buildroot}/%{_docdir}/%{name}-%{version}
find %{buildroot}/%{_libdir} -name '*.la' -delete
find %{buildroot}/%{_libdir} -name '*.so~' -delete
cat >> %{buildroot}/etc/sudoers << EOF
%wheel ALL=(ALL) ALL
%sudo   ALL=(ALL) ALL
EOF
install -vdm755 %{buildroot}/etc/pam.d
cat > %{buildroot}/etc/pam.d/sudo << EOF
#%%PAM-1.0
auth       include      system-auth
account    include      system-account
password   include      system-password
session    include      system-session
session    required     pam_env.so
EOF

%find_lang %{name}
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
  groupadd wheel
fi
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files -f %{name}.lang
%defattr(-,root,root)
%attr(0440,root,root) %config(noreplace) %{_sysconfdir}/sudoers
%attr(0640,root,root) %config(noreplace) /etc/sudo.conf
%attr(0640,root,root) %config(noreplace) /etc/sudo_logsrvd.conf
%attr(0750,root,root) %dir %{_sysconfdir}/sudoers.d/
%config(noreplace) %{_sysconfdir}/pam.d/sudo
%{_bindir}/*
%{_includedir}/*
%{_libdir}/sudo/*.so
%{_libdir}/sudo/*.so.*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_docdir}/%{name}-%{version}/*
%{_datarootdir}/locale/*
%exclude  /etc/sudoers.dist

%changelog
*   Fri Jan 15 2021 Sujay G <gsujay@vmware.com> 1.9.5-1
-   Bump version to 1.9.5 to fix CVE-2021-23240
*   Mon Jan 06 2020 Shreyas B. <shreyasb@vmware.com> 1.8.30-1
-   Upgrade sudo to v1.8.30 for fixing the CVE-2019-19232 & CVE-2019-19234.
*   Tue Oct 15 2019 Shreyas B. <shreyasb@vmware.com> 1.8.20p2-2
-   Fix for CVE-2019-14287.
*   Thu Jun 15 2017 Kumar Kaushik <kaushikk@vmware.com> 1.8.20p2-1
-   Udating version to 1.8.20p2, fixing CVE-2017-1000367 and CVE-2017-1000368
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-3
-   GA - Bump release of all rpms
*   Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-2
-   Fix for upgrade issues
*   Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.15-1
-   Update to 1.8.15-1.
*   Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.8.11p1-5
-   Edit post script.
*   Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-4
-   Fixing permissions on /etc/sudoers file
*   Fri May 29 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-3
-   Adding sudo configuration and PAM config file
*   Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-2
-   Adding PAM support
*   Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-1
-   Initial build.	First version
