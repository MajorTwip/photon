%define        with_boost     1
%define        with_crash     1
%define        with_docs      0
%define        with_grapher   0
%define        with_pie       1
%define        with_rpm       0
%define        with_sqlite    1

Name:          systemtap
Version:       4.5
Release:       5%{?dist}
Summary:       Programmable system-wide instrumentation system
Group:         Development/System
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           http://sourceware.org/systemtap
License:       GPLv2+

Source0:       http://sourceware.org/systemtap/ftp/releases/systemtap-%{version}.tar.gz
%define sha512  %{name}=8136779a9f5cb0fbaae565eab1ab6fa307f1024dfc2c6c3845acfadff0eecc684ba89aa5d442c7b90c2c73edaab41ca07bae2bad8361f80fe8e9928b40466cd3

BuildRequires: elfutils-devel
BuildRequires: glibc-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: libgcc
BuildRequires: nspr-devel
BuildRequires: nss-devel
BuildRequires: sqlite-devel
BuildRequires: libstdc++-devel
BuildRequires: libtirpc-devel
BuildRequires: libxml2-devel
BuildRequires: perl
BuildRequires: python3-setuptools
BuildRequires: nss
BuildRequires: shadow
BuildRequires: curl-devel
BuildRequires: python3-devel
BuildRequires: pkg-config

%if %{with_boost}
BuildRequires: boost-devel
%endif

%if %{with_crash}
BuildRequires: crash-devel
BuildRequires: zlib-devel
Requires:      crash
%endif

%if %{with_rpm}
BuildRequires: rpm-devel
%endif

Requires:         gcc
Requires:         linux-devel
Requires:         make
Requires:         elfutils
Requires:         %{name}-runtime = %{?epoch:%epoch:}%{version}-%{release}
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

BuildRoot:        %{_tmppath}/%{name}-%{version}-root

%description
SystemTap is an instrumentation system for systems running Linux.
Developers can write instrumentation scripts to collect data on
the operation of the system.  The base %{name} package contains/requires
the components needed to locally develop and execute %{name} scripts.

%package initscript
Group:         System/Tools
Summary:       Systemtap Initscript
Requires:      %{name}-runtime = %{?epoch:%epoch:}%{version}-%{release}
Requires:      initscripts

%description initscript
Initscript for Systemtap scripts.

%package runtime
Group:         System/Tools
Summary:       Instrumentation System Runtime
Requires:      linux-devel

%description runtime
SystemTap runtime is the runtime component of an instrumentation system for systems running Linux.

%package sdt-devel
Group:         System/Tools
Summary:       Static probe support tools
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description sdt-devel
Support tools to allow applications to use static probes.

%package server
Group:         System/Tools
Summary:       Instrumentation System Server
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}
Requires:      %{name}-runtime = %{?epoch:%epoch:}%{version}-%{release}
Requires:      (coreutils or coreutils-selinux)
Requires:      nss
Requires:      unzip
Requires:      gzip

%description server
SystemTap server is the server component of an instrumentation system for systems running Linux.

%prep
%autosetup -p1
sed -i "s#"kernel"#"linux"#g" stap-prep
sed -i "s#"devel"#"dev"#g" stap-prep

%build
%configure \
%if %{with_crash}
    --enable-crash \
%else
    --disable-crash \
%endif
    --disable-docs \
%if %{with_sqlite}
    --enable-sqlite \
%else
    --disable-sqlite \
%endif
%if %{with_rpm}
    --with-rpm \
%else
    --without-rpm \
%endif
%if %{with_pie}
    --enable-pie \
%else
    --disable-pie \
%endif
    --disable-grapher \
    --disable-virt \
    --disable-silent-rules

%make_build

%install
%make_install mandir=%{_mandir} %{?_smp_mflags}

mv %{buildroot}%{_datadir}/%{name}/examples examples

find examples -type f -name '*.stp' -print0 | xargs -0 sed -i -r -e '1s@^#!.+stap@#!%{_bindir}/stap@'

chmod 755 %{buildroot}%{_bindir}/staprun

install -c -m 755 stap-prep %{buildroot}%{_bindir}/stap-prep

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d/ \
         %{buildroot}%{_sysconfdir}/%{name} \
         %{buildroot}%{_sysconfdir}/%{name}/conf.d \
         %{buildroot}%{_sysconfdir}/%{name}/script.d \
         %{buildroot}%{_localstatedir}/cache/%{name} \
         %{buildroot}%{_localstatedir}/run/%{name}

install -m 755 initscript/%{name} %{buildroot}%{_sysconfdir}/rc.d/init.d/
install -m 644 initscript/config.%{name} %{buildroot}%{_sysconfdir}/%{name}/config

%if %{with_docs}
mkdir docs.installed
mv %{buildroot}%{_datadir}/%{name}/*.pdf \
   %{buildroot}%{_datadir}/%{name}/tapsets \
   docs.installed/
%if %{with_publican}
mv %{buildroot}%{_datadir}/%{name}/SystemTap_Beginners_Guide docs.installed/
%endif
%endif

install -m 755 initscript/stap-server %{buildroot}%{_sysconfdir}/rc.d/init.d/

mkdir -p %{buildroot}%{_sysconfdir}/stap-server \
         %{buildroot}%{_sysconfdir}/stap-server/conf.d \
         %{buildroot}%{_sysconfdir}/sysconfig \
         %{buildroot}%{_localstatedir}/log \
         %{buildroot}%{_localstatedir}/opt/stap-server/log \
         %{buildroot}%{_sysconfdir}/logrotate.d

install -m 644 initscript/config.stap-server %{buildroot}%{_sysconfdir}/sysconfig/stap-server
ln -sfv %{_localstatedir}/opt/stap-server/log %{buildroot}%{_localstatedir}/log/stap-server
touch %{buildroot}%{_localstatedir}/opt/stap-server/log/log
install -m 644 initscript/logrotate.stap-server %{buildroot}%{_sysconfdir}/logrotate.d/stap-server

%find_lang %{name}

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}

%pre
getent group stap-server >/dev/null || groupadd -g 155 -r stap-server || groupadd -r stap-server

%pre runtime
getent group stapdev >/dev/null || groupadd -r stapdev
getent group stapusr >/dev/null || groupadd -r stapusr
exit 0

%pre server
getent passwd stap-server >/dev/null || \
/usr/sbin/useradd -c "Systemtap Compile Server" -u 155 -g stap-server -d %{_localstatedir}/lib/stap-server -m -r -s /sbin/nologin stap-server || \
/usr/sbin/useradd -c "Systemtap Compile Server" -g stap-server -d %{_localstatedir}/lib/stap-server -m -r -s /sbin/nologin stap-server
test -e ~stap-server && chmod 755 ~stap-server
exit 0

%post server
if [ $1 -eq 1 ] ; then
  test -e %{_localstatedir}/log/stap-server/log || {
    touch %{_localstatedir}/log/stap-server/log
    chmod 664 %{_localstatedir}/log/stap-server/log
    chown stap-server:stap-server %{_localstatedir}/log/stap-server/log
  }

  if test ! -e ~stap-server/.%{name}/ssl/server/stap.cert; then
      runuser -s /bin/sh - stap-server -c %{_libexecdir}/%{name}/stap-gen-cert >/dev/null
      %{_bindir}/stap-authorize-server-cert ~stap-server/.%{name}/ssl/server/stap.cert
      %{_bindir}/stap-authorize-signing-cert ~stap-server/.%{name}/ssl/server/stap.cert
  fi
  /sbin/chkconfig --add stap-server
  exit 0
fi

%preun server
if [ $1 = 0 ] ; then
    /sbin/service stap-server stop >/dev/null 2>&1
    /sbin/chkconfig --del stap-server
fi
exit 0

%postun server
if [ "$1" -ge "1" ] ; then
    /sbin/service stap-server condrestart >/dev/null 2>&1 || :
fi
exit 0

%post initscript
if [ $1 -eq 1 ] ; then
    /sbin/chkconfig --add %{name}
    exit 0
fi

%preun initscript
if [ $1 = 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
exit 0

%postun initscript
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
exit 0

%post
if [ $1 -eq 1 ] ; then
    (make -C %{_datadir}/%{name}/runtime/linux/uprobes clean) >/dev/null 3>&1 || true
    (/sbin/rmmod uprobes) >/dev/null 2>&1 || true
fi

%preun
if [ $1 -eq 0 ] ; then
    (make -C %{_datadir}/%{name}/runtime/linux/uprobes clean) >/dev/null 3>&1 || true
    (/sbin/rmmod uprobes) >/dev/null 2>&1 || true
fi

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/stap
%{_bindir}/stap-merge
%{_bindir}/stap-prep
%{_bindir}/stap-report
%{_bindir}/stapsh
%{_bindir}/stapbpf
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/runtime
%{_datadir}/%{name}/runtime/*.h
%{_datadir}/%{name}/runtime/*.c
%{_datadir}/%{name}/runtime/transport
%{_datadir}/%{name}/runtime/unwind
%dir %{_datadir}/%{name}/runtime/linux
%{_datadir}/%{name}/runtime/linux/*.c
%{_datadir}/%{name}/runtime/linux/*.h
%dir %attr(0775,root,stap-server) %{_datadir}/%{name}/runtime/linux/uprobes
%{_datadir}/%{name}/runtime/linux/uprobes/*
%dir %{_datadir}/%{name}/runtime/linux/uprobes2
%{_datadir}/%{name}/runtime/linux/uprobes2/*
%{_datadir}/%{name}/tapset
%dir %{_datadir}/%{name}/runtime/softfloat
%{_datadir}/%{name}/runtime/softfloat/*.h
%{_mandir}/man1
%{_mandir}/man3/stap*.3stap*
%{_mandir}/man7/warning::symbols.7stap*
%{_mandir}/man7/warning::buildid.7stap*
%{_mandir}/man7/stappaths.7*
%{_mandir}/man8/stapsh.8*
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/stapbpf.8*
%{_bindir}/dtrace

%files initscript
%defattr(-,root,root)
%{_sysconfdir}/rc.d/init.d/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/conf.d
%dir %{_sysconfdir}/%{name}/script.d
%config(noreplace) %{_sysconfdir}/%{name}/config
%dir %{_localstatedir}/cache/%{name}
%dir %{_localstatedir}/run/%{name}

%files runtime
%defattr(-,root,root)
%attr(4111,root,root) %{_bindir}/staprun
%{_libexecdir}/%{name}/stapio
%{_libexecdir}/%{name}/stap-env
%{_libexecdir}/%{name}/stap-authorize-cert
%if %{with_crash}
%{_libdir}/%{name}/staplog.so*
%endif
%{_mandir}/man8/staprun.8*

%files sdt-devel
%defattr(-,root,root)
%{_includedir}/sys/sdt.h
%{_includedir}/sys/sdt-config.h

%files server
%defattr(-,root,root)
%{_bindir}/stap-server
%{_libexecdir}/%{name}/stap-serverd
%{_libexecdir}/%{name}/stap-start-server
%{_libexecdir}/%{name}/stap-stop-server
%{_libexecdir}/%{name}/stap-gen-cert
%{_libexecdir}/%{name}/stap-sign-module
%{_sysconfdir}/rc.d/init.d/stap-server
%config(noreplace) %{_sysconfdir}/logrotate.d/stap-server
%dir %{_sysconfdir}/stap-server
%dir %{_sysconfdir}/stap-server/conf.d
%config(noreplace) %{_sysconfdir}/sysconfig/stap-server
%dir %attr(0755,stap-server,stap-server) %{_localstatedir}/opt/stap-server/log
%attr(0755,stap-server,stap-server) %{_localstatedir}/log/stap-server
%ghost %config %attr(0644,stap-server,stap-server) %{_localstatedir}/opt/stap-server/log/log
%{_mandir}/man7/error::*.7stap*
%{_mandir}/man7/warning::debuginfo.7stap*
%{_mandir}/man8/stap-server.8*
%{_mandir}/man8/%{name}-service.8*

%changelog
* Sat Apr 29 2023 Harinadh D <hdommaraju@vmware.com> 4.5-5
- Fix for requires
* Tue Jun 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.5-4
- Bump version as a part of sqlite upgrade
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 4.5-3
- Bump up to compile with python 3.10
* Mon Aug 09 2021 Ankit Jain <ankitja@vmware.com> 4.5-2
- Fix spec with autosetup and make smp flag
* Mon Aug 02 2021 Ankit Jain <ankitja@vmware.com> 4.5-1
- Updated to version 4.5
- Fixes Null pointer exception issue
* Thu Nov 12 2020 Ankit Jain <ankitja@vmware.com> 4.4-1
- Updated to version 4.4
* Wed Aug 19 2020 Ankit Jain <ankitja@vmware.com> 4.3-3
- BuildRequires curl-devel, required by libdebuginfod.so
* Fri Jul 17 2020 Tapas Kundu <tkundu@vmware.com> 4.3-2
- Mass removal python2
* Thu Jun 25 2020 Gerrit Photon <photon-checkins@vmware.com> 4.3-1
- Automatic Version Bump
* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 4.0-2
- Added BuildRequires python2-devel
* Tue Dec 04 2018 Keerthana K <keerthanak@vmware.com> 4.0-1
- Updated to version 4.0
* Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 3.3-1
- Updated to version 3.3
* Tue Jan 23 2018 Divya Thaluru <dthaluru@vmware.com>  3.2-1
- Updated to version 3.2
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  3.1-5
- Fixed the log file directory structure
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1-4
- Remove shadow from requires and use explicit tools for post actions
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1-3
- Requires coreutils or toybox
* Thu Aug 10 2017 Alexey Makhalov <amakhalov@vmware.com> 3.1-2
- systemtap-sdt-devel requires systemtap
* Tue Apr 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.1-1
- Update to version 3.1
* Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0-4
- add shadow to requires
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.0-3
- Use sqlite-{devel,libs}
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 3.0-2
- Modified %check
* Fri Jul 22 2016 Divya Thaluru <dthaluru@vmware.com> 3.0-1
- Updated version to 3.0
- Removing patch to enable kernel (fix is present in upstream)
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-5
- GA - Bump release of all rpms
* Mon May 23 2016 Harish Udaiya KUmar <hudaiyakumar@vmware.com> 2.9-4
- Added the patch to enable kernel building with Kernel 4.4
* Fri May 20 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9-3
- Fixed the stap-prep script to be compatible with Photon
* Wed May 4 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9-2
- Fix for upgrade issues
* Wed Dec 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9-1
- Updated version to 2.9
* Fri Dec 11 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7-2
- Move dtrace to the main package.
* Wed Nov 18 2015 Anish Swaminathan <anishs@vmware.com> 2.7-1
- Initial build. First version
