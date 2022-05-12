Summary:    advanced key-value store
Name:       redis
Version:    6.2.7
Release:    1%{?dist}
License:    BSD
URL:        http://redis.io
Group:      Applications/Databases
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://download.redis.io/releases/%{name}-%{version}.tar.gz
%define sha1 %{name}=d1e412f99fed7349825f2cf4d4fc39f1b7f40d8a

Patch0:         redis-conf.patch

BuildRequires:  gcc
BuildRequires:  systemd-devel
BuildRequires:  make
BuildRequires:  which
BuildRequires:  tcl
BuildRequires:  tcl-devel

Requires:   systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
Redis is an in-memory data structure store, used as database, cache and message broker.

%prep
%autosetup -p1

%build
make BUILD_TLS=yes %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}
make PREFIX=%{buildroot}%{_usr} install %{?_smp_mflags}
install -D -m 0640 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf

mkdir -p %{buildroot}%{_sharedstatedir}/%{name} \
          %{buildroot}/var/log \
          %{buildroot}/var/opt/%{name}/log \
          %{buildroot}%{_unitdir}

ln -sfv /var/opt/%{name}/log %{buildroot}/var/log/%{name}

cat << EOF >>  %{buildroot}%{_unitdir}/redis.service
[Unit]
Description=Redis in-memory key-value database
After=network.target

[Service]
ExecStart=%{_bindir}/redis-server %{_sysconfdir}/redis.conf --daemonize no
ExecStop=%{_bindir}/redis-cli shutdown
User=redis
Group=redis

[Install]
WantedBy=multi-user.target
EOF

%check
%if 0%{?with_check}
make check %{?_smp_mflags}
%endif

%pre
getent group %{name} &> /dev/null || groupadd -r %{name} &> /dev/null

getent passwd %{name} &> /dev/null || \
useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
-c 'Redis Database Server' %{name} &> /dev/null

%post
/sbin/ldconfig
%systemd_post  redis.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart redis.service

%files
%defattr(-,root,root)
%dir %attr(0750, redis, redis) /var/lib/redis
%dir %attr(0750, redis, redis) /var/opt/%{name}/log
%attr(0750, redis, redis) %{_var}/log/%{name}
%{_bindir}/*
%{_unitdir}/*
%config(noreplace) %attr(0640, %{name}, %{name}) %{_sysconfdir}/redis.conf

%changelog
* Wed May 11 2022 Shreenidhi Shedi <sshedi@vmware.com> 6.2.7-1
- Upgrade to v6.2.7
- This fixes CVE-2022-24735, CVE-2022-24736
* Wed Oct 13 2021 Nitesh Kumar <kunitesh@vmware.com> 4.0.14-5
- Fix for CVE-2021-32672
* Fri Apr 09 2021 Shreyas B <shreyasb@vmware.com> 4.0.14-4
- Fix for CVE-2021-3470
* Tue Aug 25 2020 Anisha Kumari <kanisha@vmware.com> 4.0.14-3
- Fix for CVE-2020-7105.patch in hiredis
* Wed Jun 24 2020 Shreyas B <shreyasb@vmware.com> 4.0.14-2
- Fix for CVE-2020-14147
* Wed Aug 14 2019 Kuladeep Rayalla <krayalla@vmware.com> 4.0.14-1
- Upgrade redis to 4.0.14 to fix CVE-2019-10193
- Deleting the path for CVE-2019-10192, redis-4.0.14 includes the fix
* Thu Jul 25 2019 Kuladeep Rayalla <krayalla@vmware.com> 4.0.10-2
- Add patch for CVE-2019-10192
* Mon Jul 09 2018 Ajay Kaher <akaher@vmware.com> 4.0.10-1
- Upgrade redis to 4.0.10 to include CVE-2018-11218, and CVE-2018-11219.
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.8-4
- Remove shadow from requires and use explicit tools for post actions
* Wed May 31 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.8-3
- Fix DB persistence,log file,grace-ful shutdown issues
* Tue May 16 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.8-2
- Added systemd service unit
* Wed Apr 5 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.2.8-1
- Updating to latest version
* Mon Oct 3 2016 Dheeraj Shetty <dheerajs@vmware.com> 3.2.4-1
- initial version
