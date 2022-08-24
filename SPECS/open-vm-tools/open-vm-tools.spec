%global gosc_scripts gosc-scripts
%define gosc_ver 1.3.2

Summary:        Usermode tools for VMware virts
Name:           open-vm-tools
Version:        11.3.5
Release:        3%{?dist}
License:        LGPLv2+
URL:            https://github.com/vmware/open-vm-tools
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/vmware/open-vm-tools/archive/%{name}-stable-%{version}.tar.gz
%define sha1 open-vm-tools=842aa660b301aeb8d1fd18346fb14c0de74b9c95
Source1:        https://gitlab.eng.vmware.com/photon-gosc/gosc-scripts/-/archive/%{gosc_ver}/gosc-scripts-%{gosc_ver}.tar.gz
%define sha1 gosc-scripts-%{gosc_ver}=eb90b74e9282bc5b80f1f8ae358cb7e9bfdda4cb
Source2:        vmtoolsd.service
Source3:        vgauthd.service

# If patch is taken from open-vm-tools repo, prefix it with 'ovt-'
# If patch is taken from gosc-scripts repo, prefix it with 'gosc-'
Patch0:     ovt-linux-deployment.patch
Patch1:     CVE-2022-31676.patch

BuildRequires:  glib-devel
BuildRequires:  libxml2-devel
BuildRequires:  xmlsec1-devel
BuildRequires:  libltdl-devel
BuildRequires:  libmspack-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  fuse-devel
BuildRequires:  systemd
BuildRequires:  libtirpc-devel

Requires:       fuse
Requires:       libmspack
Requires:       glib
Requires:       openssl
Requires:       libstdc++
Requires:       libtirpc
Requires:       xmlsec1
Requires:       which
Requires:       systemd

%description
VMware virtualization user mode tools

%package        devel
Summary:        Header and development files for open-vm-tools
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%package        sdmp
Summary:        Service Discovery plugin for open-vm-tools
Requires:       %{name} = %{version}-%{release}

%description    sdmp
The "open-vm-tools-sdmp" package contains a plugin for Service Discovery.

%prep
%autosetup -n %{name}-stable-%{version} -a0 -a1 -p1

%build
cd %{name}
autoreconf -i
%configure --enable-photon-gosc \
        --without-x \
        --without-kernel-modules \
        --without-icu \
        --disable-static \
        --with-tirpc \
        --enable-servicediscovery

make %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}/%{_unitdir}
install -vdm 755 %{buildroot}/usr/share/open-vm-tools
cp -r %{gosc_scripts} %{buildroot}/usr/share/open-vm-tools
install -p -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}
install -p -m 644 %{SOURCE3} %{buildroot}/%{_unitdir}

cd %{name}
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm -f %{buildroot}/sbin/mount.vmhgfs
chmod -x %{buildroot}/etc/pam.d/vmtoolsd
find %{buildroot}/usr/lib/ -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post vgauthd.service vmtoolsd.service

%preun
%systemd_preun vmtoolsd.service vgauthd.service
# Tell VMware that open-vm-tools is being uninstalled
if [ "$1" = "0" -a                      \
     -e %{_bindir}/vmware-checkvm -a    \
     -e %{_bindir}/vmware-rpctool ] &&  \
     %{_bindir}/vmware-checkvm &> /dev/null; then
  %{_bindir}/vmware-rpctool 'tools.set.version 0' &> /dev/null || /bin/true
fi

%postun
/sbin/ldconfig
%systemd_postun_with_restart vmtoolsd.service vgauthd.service

%files
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins/common
%dir %{_libdir}/%{name}/plugins/vmsvc
%{_libdir}/%{name}/plugins/vmsvc/libdeployPkgPlugin.so
%{_libdir}/%{name}/plugins/vmsvc/libguestInfo.so
%{_libdir}/%{name}/plugins/vmsvc/libpowerOps.so
%{_libdir}/%{name}/plugins/vmsvc/libresolutionKMS.so
%{_libdir}/%{name}/plugins/vmsvc/libtimeSync.so
%{_libdir}/%{name}/plugins/vmsvc/libvmbackup.so
%{_libdir}/%{name}/plugins/common/libhgfsServer.so
%{_libdir}/%{name}/plugins/common/libvix.so
%{_libdir}/%{name}/plugins/vmsvc/libappInfo.so
%{_libdir}/%{name}/plugins/vmsvc/libgdp.so
%{_libdir}/%{name}/plugins/vmsvc/libguestStore.so
%{_libdir}/*.so.*
%{_bindir}/*
%{_sysconfdir}/*
%{_datadir}/*
%{_unitdir}/*
/lib/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so

%files sdmp
%defattr(-,root,root)
%{_libdir}/%{name}/plugins/vmsvc/libserviceDiscovery.so
%{_libdir}/%{name}/serviceDiscovery/scripts/get-versions.sh
%{_libdir}/%{name}/serviceDiscovery/scripts/get-connection-info.sh
%{_libdir}/%{name}/serviceDiscovery/scripts/get-listening-process-info.sh
%{_libdir}/%{name}/serviceDiscovery/scripts/get-listening-process-perf-metrics.sh

%changelog
* Wed Aug 17 2022 Shivani Agarwal <shivania2@vmware.com> 11.3.5-3
- Fix CVE-2022-31676
* Tue Nov 09 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.3.5-2
- Remove cloud-init from Requires
* Tue Sep 28 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.3.5-1
- Upgrade to version 11.3.5
* Tue Jun 22 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.3.0-1
- Upgrade to version 11.3.0
* Wed Jun 09 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.2.5-3
- Fix missing patch
* Mon Mar 01 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.2.5-2
- Fixed an issue with gosc
* Sat Feb 27 2021 Shreenidhi Shedi <sshedi@vmware.com> 11.2.5-1
- Upgrade to version 11.2.5 & enabled sdmp plugin support
* Sun Jan 24 2021 Shreyas B. <shreyasb@vmware.com> 10.3.10-5
- Start vmtoolsd after dbus service.
* Fri Oct 11 2019 Anish Swaminathan <anishs@vmware.com> 10.3.10-4
- Update memory leak fix patch to include
- https://github.com/vmware/open-vm-tools/commit/26b9edbeb79d1c67b9ae73a0c97c48999c1fb503
* Thu Sep 26 2019 Ankit Jain <ankitja@vmware.com> 10.3.10-3
- Added requires xmlsec1
* Sun Sep 15 2019 Keerthana K <keerthanak@vmware.com> 10.3.10-2
- Fix memory leak issues in vix.
* Tue May 07 2019 Ankit Jain <ankitja@vmware.com> 10.3.10-1
- Updating version to 10.3.10
* Wed Mar 27 2019 Anish Swaminathan <anishs@vmware.com> 10.2.5-2
- Start vmtoolsd before cloud-init
* Fri Feb 01 2019 Ankit Jain <ankitja@vmware.com> 10.2.5-1
- Updating version to 10.2.5
* Fri Jun 22 2018 Keerthana K <keerthanak@vmware.com> 10.2.0-4
- Fix for post custom script failure.
* Mon Apr 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 10.2.0-3
- Revert regex changes to gosc scripts.
* Wed Mar 21 2018 Anish Swaminathan <anishs@vmware.com> 10.2.0-2
- Fix gosc patch to call customization
* Wed Jan 24 2018 Kumar Kaushik <kaushikk@vmware.com> 10.2.0-1
- Updating version to 10.2.0.
* Tue Aug 22 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.10-1
- Updating version to 10.1.10, removing upstream patches.
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 10.1.5-6
- Add libdnet-devel and libmspack-devel to BuildRequires, add devel package.
* Mon Jun 05 2017 Bo Gan <ganb@vmware.com> 10.1.5-5
- Fix dependency
* Thu Apr 20 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.5-4
- Timezone customization, PR # 1684889
* Fri Apr 07 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.5-3
- Applying tmp race condition patch, PR #1733669
* Fri Mar 24 2017 Alexey Makhalov <amakhalov@vmware.com> 10.1.5-2
- Added *-sysmacros.patch to fix build issue with glibc-2.25
* Fri Mar 03 2017 Kumar Kaushik <kaushikk@vmware.com> 10.1.5-1
- Updating version to 10.1.5
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 10.1.0-2
- BuildRequires Linux-PAM-devel
* Mon Nov 21 2016 Kumar Kaushik <kaushikk@vmware.com> 10.1.0-1
- Updating version to 10.1.0
* Wed Oct 05 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-14
- Adding proper entry to /etc/hosts for IPv6.
* Tue Oct 04 2016 ChangLee <changLee@vmware.com> 10.0.5-13
- Modified %check
* Thu Jun 23 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-12
- Avoiding recustomization of hostname, bug#1678537.
* Mon Jun 13 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-11
- Adding IPv6 Support for VCHA in customization.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 10.0.5-10
- GA - Bump release of all rpms
* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-9
- Edit scriptlets.
* Fri Apr 29 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-8
- Combining all GOSC scripts patches and fixing bug#1648133.
* Tue Apr 19 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-7
- Fixing libDeploy not to overwrite for SRM cust needs.
* Tue Mar 29 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-6
- Replacing timedatectl with systemd patch..
* Fri Mar 25 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-5
- Time data ctl fix for ignoring message print in stderr.
* Tue Feb 09 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 10.0.5-4
- Preserve network onboot config.
* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-3
- Add vgauthd service.
* Tue Feb 02 2016 Kumar Kaushik <kaushikk@vmware.com> 10.0.5-2
- Making interface file name according to convention.
* Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 10.0.5-1
- Upgrade version.
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 10.0.0-13
- Edit post script.
* Fri Nov 27 2015 Sharath George <sharathg@vmware.com> 10.0.0-12
- Correcting path of pam file.
* Tue Sep 15 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-11
- Adding ssh RSA public support for password-less login.
* Wed Sep 09 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-10
- Adding option to modify /etc/hosts for lightwave on optional basis.
* Wed Sep 09 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-9
- Fixing once in while issue related to customization failure.
* Wed Sep 02 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-8
- Fixing systemd cloud-init and GOSC cloud-init race.
* Tue Sep 01 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-7
- Fixing GOSC counter bug.
* Wed Aug 26 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-6
- Avoiding reboot after successful customization.
* Tue Aug 25 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-5
- Adding support for NFS mount in GOSC scripts.
* Thu Aug 20 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-4
- Fixing GOSC-libdeploy return code problem.
* Thu Aug 13 2015 Kumar Kaushik <kaushikk@vmware.com> 10.0.0-3
- Combining all GOSC patches and adding support for lightwave.
* Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-2
- Build with fuse support.
* Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 10.0.0-1
- Update version to 10.0.0.
* Tue Aug 11 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-7
- VCA initial login password issue fix.
* Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-6
- Adding preun and post install commands.
* Thu Jul 30 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-5
- Adding Blob configuation support to GOSC scripts.
* Thu Jul 09 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-4
- Fixing GOSC to work on VCA.
* Tue Apr 21 2015 Kumar Kaushik <kaushikk@vmware.com> 9.10.0-3
- Adding guest optimizations support for photon.
* Tue Apr 21 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.0-2
- Added open-vm-tools-stderr_r-fix upstream patch and removed glibc patch.
* Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 9.10.0-1
- Initial version
