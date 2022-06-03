Summary:	cifs client utils
Name:		cifs-utils
Version:	6.7
Release:	4%{?dist}
License:	GPLv3
URL:		http://wiki.samba.org/index.php/LinuxCIFS_utils
Group:		Applications/Nfs-utils-client
Source0:        https://ftp.samba.org/pub/linux-cifs/cifs-utils/cifs-utils-%{version}.tar.bz2
%define sha1 cifs-utils=9ba5091d7c2418a90773c861f04a3f4a36854c14
Vendor:		VMware, Inc.
Distribution:	Photon

Patch0:         0001-CVE-2020-14342-mount.cifs-fix-shell-command-injectio.patch

# fix for CVE-2021-20208
Patch1:         0001-cifs-upcall-try-to-use-container-ipc-uts-net-pid-mnt-user.patch

# fix for CVE-2022-27239
Patch2:         0001-CVE-2022-27239_mount_cifs_fix_length_check_for_ip_option_parsing.patch

# fix for CVE-2022-29869
Patch3:         0001-mount.cifs_fix_verbose_messages_on_option_parsing.patch

BuildRequires:  libcap-ng-devel
BuildRequires:  libtalloc-devel
Requires:       libcap-ng

%description
Cifs-utils, a package of utilities for doing and managing mounts of the Linux CIFS filesystem.


%package devel
Summary:    The libraries and header files needed for Cifs-Utils development.
Group:      Development/Libraries
Requires:   cifs-utils = %{version}-%{release}

%description devel
Provides header files needed for Cifs-Utils development.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
autoreconf -fiv &&./configure --prefix=%{_prefix}
make

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
/sbin/mount.cifs
%{_mandir}/man8/mount.cifs.8.gz

%files devel
%defattr(-,root,root)
%{_includedir}/cifsidmap.h

%changelog
*       Wed Jun 01 2022 Ajay Kaher <akaher@vmware.com> 6.7-4
-       Fix for CVE-2022-27239, CVE-2022-29869
*       Tue May 11 2021 Ajay Kaher <akaher@vmware.com> 6.7-3
-       Fix for CVE-2021-20208
*       Tue Sep 15 2020 Ajay Kaher <akaher@vmware.com> 6.7-2
-       Fix for CVE-2020-14342
*       Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 6.7-1
-       Upgraded to version 6.7
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.4-2
-	GA - Bump release of all rpms
*	Mon Jan 25 2016 Divya Thaluru <dthaluru@vmware.com> 6.4-1
-	Initial build.	First version
