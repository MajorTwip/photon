Summary:        Fast incremental file transfer.
Name:           rsync
Version:        3.2.4
Release:        1%{?dist}
License:        GPLv3+
URL:            https://rsync.samba.org
Group:          Appication/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://download.samba.org/pub/rsync/src/%{name}-%{version}.tar.gz
%define sha512 %{name}=96318e2754fbddf84d16df671c721e577766969dfa415925c4dc1be2e4e60a51246623747a8aec0c6e9c0824e6aa7335235ccd07f3d6fd901f8cf28e2d6e91b6

Patch0: CVE-2022-29154-1.patch
Patch1: CVE-2022-29154-2.patch

BuildRequires:  zlib-devel
BuildRequires:  systemd-devel
BuildRequires:  lz4-devel
BuildRequires:  xxhash-devel

Requires:       zlib
Requires:       systemd
Requires:       lz4
Requires:       xxhash

%description
Rsync is a fast and extraordinarily versatile file copying tool.
It can copy locally, to/from another host over any remote shell,
or to/from a remote rsync daemon.
It offers a large number of options that control every aspect of its
behavior and permit very flexible specification of the set of files
to be copied. It is famous for its delta-transfer algorithm, which
reduces the amount of data sent over the network by sending only the
differences between the source files and the existing files in the
destination.
Rsync is widely used for backups and mirroring and as an improved
copy command for everyday use.

%prep
%autosetup -p1

%build
%configure \
    --with-included-zlib=no \
    --enable-openssl \
    --enable-xxhash \
    --enable-zstd \
    --enable-lz4 \
    --enable-ipv6

%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/rsyncd.conf

mkdir -p %{buildroot}%{_unitdir}
cat << EOF >> %{buildroot}%{_unitdir}/rsyncd.service
[Unit]
Description=Rsync Server
After=local-fs.target
ConditionPathExists=%{_sysconfdir}/rsyncd.conf

[Service]
ExecStart=%{_bindir}/%{name} --daemon --no-detach

[Install]
WantedBy=multi-user.target
EOF

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_unitdir}/rsyncd.service
%{_sysconfdir}/rsyncd.conf
%exclude %dir %{_libdir}/debug
%exclude %{_usrsrc}/debug

%changelog
* Wed Aug 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.4-1
- Fix CVE-2022-29154
* Sat Mar 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.1.3-4
- Exclude debug symbols properly
* Wed Oct 28 2020 Tapas Kundu <tkundu@vmware.com> 3.1.3-3
- Fix iconv crash
* Mon Oct 15 2018 Ankit Jain <ankitja@vmware.com> 3.1.3-2
- Building rsync with system zlib instead of outdated zlib in rsync source
* Tue May 01 2018 Xiaolin Li <xiaolinl@vmware.com> 3.1.3-1
- Updated to version 3.1.3, fix CVE-2018-5764
* Wed Dec 27 2017 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-5
- Fix CVE-2017-17433, CVE-2017-17434
* Wed Nov 29 2017 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-4
- Fix CVE-2017-16548
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.1.2-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.2-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-1
- Updated to version 3.1.2
* Mon Dec 14 2015 Xiaolin Li < xiaolinl@vmware.com> 3.1.1-1
- Initial build. First version
