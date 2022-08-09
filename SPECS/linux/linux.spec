%global security_hardening none
Summary:        Kernel
Name:           linux
Version:        4.9.321
Release:        3%{?kat_build:.%kat_build}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

%define uname_r %{version}-%{release}

Source0:        http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{version}.tar.xz
%define sha1 linux=6bbda736a8fae4bcc7808cb29cf09fcea22a1df0
Source1:        config
Source2:        initramfs.trigger
%define ena_version 1.1.3
Source3:       https://github.com/amzn/amzn-drivers/archive/ena_linux_1.1.3.tar.gz
%define sha1 ena_linux=84138e8d7eb230b45cb53835edf03ca08043d471
Source4:        pre-preun-postun-tasks.inc

# common
Patch0:         x86-vmware-read-tsc_khz-only-once-at-boot-time.patch
Patch1:         x86-vmware-use-tsc_khz-value-for-calibrate_cpu.patch
Patch2:         x86-vmware-add-basic-paravirt-ops-support.patch
Patch3:         x86-vmware-add-paravirt-sched-clock.patch
Patch4:         x86-vmware-log-kmsg-dump-on-panic.patch
Patch5:         double-tcp_mem-limits.patch
Patch6:         linux-4.9-sysctl-sched_weighted_cpuload_uses_rla.patch
Patch7:         linux-4.9-watchdog-Disable-watchdog-on-virtual-machines.patch
Patch8:         Implement-the-f-xattrat-family-of-functions.patch
Patch9:         SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch10:        SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch11:        vsock-transport-for-9p.patch
Patch12:        x86-vmware-sta.patch
#HyperV patches
Patch13:        0004-vmbus-Don-t-spam-the-logs-with-unknown-GUIDs.patch
Patch14:        0005-Drivers-hv-utils-Fix-the-mapping-between-host-versio.patch
Patch15:        0006-Drivers-hv-vss-Improve-log-messages.patch
Patch16:        0007-Drivers-hv-vss-Operation-timeouts-should-match-host-.patch
Patch17:        0008-Drivers-hv-vmbus-Use-all-supported-IC-versions-to-ne.patch
Patch18:        0009-Drivers-hv-Log-the-negotiated-IC-versions.patch
Patch19:        0010-vmbus-fix-missed-ring-events-on-boot.patch
Patch20:        0011-vmbus-remove-goto-error_clean_msglist-in-vmbus_open.patch
Patch21:        0012-vmbus-dynamically-enqueue-dequeue-the-channel-on-vmb.patch
Patch23:        0014-hv_sock-introduce-Hyper-V-Sockets.patch
#FIPS patches - allow some algorithms
Patch24:        0001-Revert-crypto-testmgr-Disable-fips-allowed-for-authe.patch
Patch25:        0002-allow-also-ecb-cipher_null.patch
Patch26:        add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by-default.patch
# Fix CVE-2017-1000252
Patch28:        kvm-dont-accept-wrong-gsi-values.patch
Patch30:        vmxnet3-avoid-xmit-reset-due-to-a-race-in-vmxnet3.patch
Patch31:        vmxnet3-use-correct-flag-to-indicate-LRO-feature.patch
# To fix kernel PANIC in cascade
Patch32:        netfilter-ipset-pernet-ops-must-be-unregistered-last.patch
Patch33:        vmxnet3-fix-incorrect-dereference-when-rxvlan-is-disabled.patch
# Fix for CVE-2019-20811
Patch34:        0001-net-sysfs-call-dev_hold-if-kobject_init_and_add-succ.patch
Patch35:        0001-net-sysfs-Call-dev_hold-always-in-netdev_queue_add_k.patch
Patch36:        0002-net-sysfs-Call-dev_hold-always-in-rx_queue_add_kobje.patch

#Fix for CVE-2019-20908
Patch37:        efi-Restrict-efivar_ssdt_load-when-the-kernel-is-locked-down.patch
#Fix for CVE-2019-19338
Patch38:        0001-KVM-vmx-implement-MSR_IA32_TSX_CTRL-disable-RTM-func.patch
Patch39:        0001-KVM-vmx-use-MSR_IA32_TSX_CTRL-to-hard-disable-TSX-on.patch

Patch42:        0001-hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
# Fix for CVE-2017-18232
Patch43:        0001-scsi-libsas-direct-call-probe-and-destruct.patch

# Fix for CVE-2018-10322
Patch46:        0001-xfs-move-inode-fork-verifiers-to-xfs-dinode-verify.patch
Patch47:        0002-xfs-verify-dinode-header-first.patch
Patch48:        0003-xfs-enhance-dinode-verifier.patch
# Fix for CVE-2018-16882
Patch49:        0001-KVM_Fix_UAF_in_nested_posted_interrupt_processing.patch

# HyperV PCI patches to Use vPCI_protocol_version_1.2
Patch51:        0001_PCI_hv_Allocate_physically_contiguous_hypercall_params_buffer.patch
Patch52:        0002_PCI_hv_Add_vPCI_version_protocol_negotiation.patch
Patch53:        0003_PCI_hv_Use_vPCI_protocol_version_1.2_v4.9.patch
# HyperV PCI patches to solve IRQ no handler problem
Patch54:        0004-PCI-hv-Use-effective-affinity-mask.patch
Patch55:        0005-x86-irq-implement-irq_data_get_effective_affinity.patch
#Fix CVE-2019-8912
Patch56:        fix_use_after_free_in_sockfs_setattr.patch
# Fix for CVE-2019-12456
Patch57:        0001-scsi-mpt3sas_ctl-fix-double-fetch-bug-in-_ctl_ioctl_.patch
# Fix for CVE-2019-12379
Patch58:        0001-consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch
# Fix for CVE-2019-12381
Patch59:        0001-ip_sockglue-Fix-missing-check-bug-in-ip_ra_control.patch
# Fix for CVE-2019-12382
Patch60:        0001-drm-edid-Fix-a-missing-check-bug-in-drm_load_edid_fi.patch
# Fix for CVE-2019-12378
Patch61:        0001-ipv6_sockglue-Fix-a-missing-check-bug-in-ip6_ra_cont.patch
#Fix for CVE-2019-3900
Patch63: 0001-vhost-vsock-add-weight-support.patch
#Fix for CVE-2021-33909
Patch64:        CVE-2021-33909.patch
# Fix CVE-2019-18885
Patch65:        0001-btrfs-merge-btrfs_find_device-and-find_device.patch
Patch66:        0002-btrfs-Detect-unbalanced-tree-with-empty-leaf-before-.patch

#Fix CVE-2022-2586
Patch67:        0001-netfilter-nf_tables-do-not-allow-SET_ID-to-refer-to-.patch

#Fix CVE-2022-2588
Patch68:        0001-net_sched-cls_route-remove-from-list-when-handle-is-.patch

# Out-of-tree patches from AppArmor:
Patch71: 0001-UBUNTU-SAUCE-AppArmor-basic-networking-rules.patch
Patch72: 0002-apparmor-Fix-quieting-of-audit-messages-for-network-.patch
Patch73: 0003-UBUNTU-SAUCE-apparmor-Add-the-ability-to-mediate-mou.patch

# Fix use-after-free issue in network stack
Patch76: 0001-inet-rename-netns_frags-to-fqdir.patch
Patch77: 0002-net-rename-inet_frags_exit_net-to-fqdir_exit.patch
Patch78: 0003-net-rename-struct-fqdir-fields.patch
Patch79: 0004-ipv4-no-longer-reference-init_net-in.patch
Patch80: 0005-ipv6-no-longer-reference-init_net-in.patch
Patch81: 0006-netfilter-ipv6-nf_defrag-no-longer-reference-init_ne.patch
Patch82: 0007-ieee820154-6lowpan-no-longer-reference-init_net-in.patch
Patch83: 0008-net-rename-inet_frags_init_net-to-fdir_init.patch
Patch84: 0009-net-add-a-net-pointer-to-struct-fqdir.patch
Patch85: 0010-net-dynamically-allocate-fqdir-structures.patch
Patch86: 0011-netns-add-pre_exit-method-to-struct-pernet_operation.patch
Patch87: 0012-inet-frags-uninline-fqdir_init.patch
Patch88: 0013-inet-frags-rework-rhashtable-dismantle.patch
Patch89: 0014-inet-frags-fix-use-after-free-read-in-inet_frag_dest.patch
Patch90: 0015-inet-fix-various-use-after-free-in-defrags-units.patch
Patch91: 0016-netns-restore-ops-before-calling-ops_exit_list.patch

#Fix CVE-2019-19813 and CVE-2019-19816
Patch92:	0001-btrfs-Move-btrfs_check_chunk_valid-to-tree-check.-ch.patch
Patch93:	0002-btrfs-tree-checker-Make-chunk-item-checker-messages-.patch
Patch94:	0003-btrfs-tree-checker-Make-btrfs_check_chunk_valid-retu.patch
Patch95:	0004-btrfs-tree-checker-Check-chunk-item-at-tree-block-re.patch
Patch96:	0005-btrfs-tree-checker-Verify-dev-item.patch
Patch97:	0006-btrfs-tree-checker-Enhance-chunk-checker-to-validate.patch
Patch98:	0007-btrfs-tree-checker-Verify-inode-item.patch

# Fix for CVE-2020-16119
Patch100:       0001-timer-Prepare-to-change-timer-callback-argument-type.patch
Patch101:       0002-net-dccp-Convert-timers-to-use-timer_setup.patch
Patch102:       0003-dccp-ccid-move-timers-to-struct-dccp_sock.patch
Patch103:       0004-Revert-dccp-don-t-free-ccid2_hc_tx_sock-struct-in-dc.patch

#Fix for CVE-2020-16120
Patch104:       0001-ovl-pass-correct-flags-for-opening-real-directory.patch
Patch105:       0002-ovl-switch-to-mounter-creds-in-readdir.patch
Patch106:       0003-ovl-verify-permissions-in-ovl_path_open.patch

Patch111:       9p-trans_fd-extend-port-variable-to-u32.patch
# Fix dummy console function definitions
Patch112:       0001-console-Expand-dummy-functions-for-CFI.patch

#Fix for CVE-2020-36385
Patch117:       0001-RDMA-ucma-Put-a-lock-around-every-call-to-the-rdma_c.patch
Patch118:       0001-RDMA-cma-Add-missing-locking-to-rdma_accept.patch
Patch119:       0001-RDMA-ucma-Rework-ucma_migrate_id-to-avoid-races-with.patch

# Fix for CVE-2018-25020
Patch120:       0001-bpf-fix-truncated-jump-targets-on-heavy-expansions.patch

# Fix for CVE-2021-4204
Patch123:       0002-bpf-Disallow-unprivileged-bpf-by-default.patch

# Fix for CVE-2021-20322
Patch124:       0001-ipv4-use-siphash-instead-of-Jenkins-in-fnhe_hashfun.patch

%if 0%{?kat_build:1}
Patch1000:	%{kat_build}.patch
%endif
BuildRequires:  bc
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:	audit-devel
Requires:       filesystem kmod
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post):(coreutils or toybox)
Requires(postun):(coreutils or toybox)

%description
The Linux package contains the Linux kernel.

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Obsoletes:      linux-dev
Requires:       %{name} = %{version}-%{release}
Requires:       python2 gawk
%description devel
The Linux package contains the Linux kernel dev files

%package drivers-gpu
Summary:        Kernel GPU Drivers
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description drivers-gpu
The Linux package contains the Linux kernel drivers for GPU

%package sound
Summary:        Kernel Sound modules
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description sound
The Linux package contains the Linux kernel sound support

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python2
%description docs
The Linux package contains the Linux kernel doc files

%package oprofile
Summary:        Kernel driver for oprofile, a statistical profiler for Linux systems
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
%description oprofile
Kernel driver for oprofile, a statistical profiler for Linux systems

%package tools
Summary:        This package contains the 'perf' performance analysis tools for Linux kernel
Group:          System/Tools
Requires:       (%{name} = %{version} or linux-esx = %{version} or linux-aws = %{version})
Requires:       audit
Obsoletes:      linux-aws-tools <= 4.9.182-1
Provides:       linux-aws-tools
%description tools
This package contains the 'perf' performance analysis tools for Linux kernel.


%prep
%setup -q -n linux-%{version}
%setup -D -b 3 -n linux-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch28 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch42 -p1
%patch43 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1

%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch68 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch87 -p1
%patch88 -p1
%patch89 -p1
%patch90 -p1
%patch91 -p1
%patch92 -p1
%patch93 -p1
%patch94 -p1
%patch95 -p1
%patch96 -p1
%patch97 -p1
%patch98 -p1
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1

%patch111 -p1
%patch112 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch123 -p1
%patch124 -p1

%if 0%{?kat_build:1}
%patch1000 -p1
%endif

%build
make mrproper
cp %{SOURCE1} .config
sed -i 's/CONFIG_LOCALVERSION=""/CONFIG_LOCALVERSION="-%{release}"/' .config
# add extra config options
echo "CONFIG_HYPERV_SOCK=m" >> .config
make LC_ALL= oldconfig
make VERBOSE=1 KBUILD_BUILD_VERSION="1-photon" KBUILD_BUILD_HOST="photon" ARCH="x86_64" %{?_smp_mflags}
make -C tools perf
# build ENA module
bldroot=`pwd`
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make -C $bldroot M=`pwd` VERBOSE=1 modules %{?_smp_mflags}
popd

%define __modules_install_post \
for MODULE in `find %{buildroot}/lib/modules/%{uname_r} -name *.ko` ; do \
    ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
    rm -f $MODULE.{sig,dig} \
    xz $MODULE \
    done \
%{nil}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post\
    %{?__debug_package:%{__debug_install_post}}\
    %{__arch_install_post}\
    %{__os_install_post}\
    %{__modules_install_post}\
%{nil}

%install
install -vdm 755 %{buildroot}/etc
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}/etc/modprobe.d
install -vdm 755 %{buildroot}/usr/src/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}
make INSTALL_MOD_PATH=%{buildroot} modules_install
# install ENA module
bldroot=`pwd`
pushd ../amzn-drivers-ena_linux_%{ena_version}/kernel/linux/ena
make -C $bldroot M=`pwd` INSTALL_MOD_PATH=%{buildroot} modules_install
popd

# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=`readelf -n vmlinux | grep "Build ID"`
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=`readelf -n extracted-vmlinux | grep "Build ID"`
if [ "$ID1" != "$ID2" ] ; then
	echo "Build IDs do not match"
	echo $ID1
	echo $ID2
	exit 1
fi
install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/*        %{buildroot}%{_defaultdocdir}/%{name}-%{uname_r}
install -vm 644 vmlinux %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}/usr/lib/debug/lib/modules/%{uname_r}/vmlinux

cat > %{buildroot}/boot/%{name}-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet no-vmw-sta
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}/%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}/%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "tmem xen-scsifront xen-blkfront xen-acpi-processor xen-evtchn xen-gntalloc xen-gntdev xen-privcmd xen-pciback xenfs hv_utils hv_vmbus hv_storvsc hv_netvsc hv_sock hv_balloon cn"
EOF

#    Cleanup dangling symlinks
rm -rf %{buildroot}/lib/modules/%{uname_r}/source
rm -rf %{buildroot}/lib/modules/%{uname_r}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/x86/include include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find $(find arch/x86 -name include -o -name scripts -type d) -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
find arch/x86/include Module.symvers include scripts -type f | xargs  sh -c 'cp --parents "$@" %{buildroot}/usr/src/%{name}-headers-%{uname_r}' copy
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}/usr/src/%{name}-headers-%{uname_r}/tools/objtool/

cp .config %{buildroot}/usr/src/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "/usr/src/%{name}-headers-%{uname_r}" "%{buildroot}/lib/modules/%{uname_r}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

# disable (JOBS=1) parallel build to fix this issue:
# fixdep: error opening depfile: ./.plugin_cfg80211.o.d: No such file or directory
# Linux version that was affected is 4.4.26
make -C tools JOBS=1 DESTDIR=%{buildroot} prefix=%{_prefix} perf_install

%include %{SOURCE2}
%include %{SOURCE4}

%post
/sbin/depmod -a %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%post drivers-gpu
/sbin/depmod -a %{uname_r}

%post sound
/sbin/depmod -a %{uname_r}

%post oprofile
/sbin/depmod -a %{uname_r}

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
/lib/firmware/*
%defattr(0644,root,root)
/lib/modules/%{uname_r}/*
%exclude /lib/modules/%{uname_r}/build
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu
%exclude /lib/modules/%{uname_r}/kernel/sound
%exclude /lib/modules/%{uname_r}/kernel/arch/x86/oprofile/

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{uname_r}/*

%files devel
%defattr(-,root,root)
/lib/modules/%{uname_r}/build
/usr/src/%{name}-headers-%{uname_r}

%files drivers-gpu
%defattr(-,root,root)
%exclude /lib/modules/%{uname_r}/kernel/drivers/gpu/drm/cirrus/
/lib/modules/%{uname_r}/kernel/drivers/gpu

%files sound
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/sound

%files oprofile
%defattr(-,root,root)
/lib/modules/%{uname_r}/kernel/arch/x86/oprofile/

%files tools
%defattr(-,root,root)
/usr/libexec
%exclude %{_libdir}/debug
/usr/lib64/traceevent
%{_bindir}
/etc/bash_completion.d/*
/usr/share/perf-core/strace/groups/file
/usr/share/doc/*

%changelog
*   Fri Aug 05 2022 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.321-3
-   Fix for CVE-2022-2586 and CVE-2022-2588
*   Tue Jul 05 2022 Ankit Jain <ankitja@vmware.com> 4.9.321-2
-   Fix for CVE-2021-20322
*   Tue Jul 05 2022 Ankit Jain <ankitja@vmware.com> 4.9.321-1
-   Update to version 4.9.321
*   Tue Jun 14 2022 Ajay Kaher <akaher@vmware.com> 4.9.318-1
-   Update to version 4.9.318
*   Wed Jun 01 2022 Ajay Kaher <akaher@vmware.com> 4.9.315-2
-   Fix for CVE-2022-1966
*   Tue May 24 2022 Sharan Turlapati <sturlapati@vmware.com> 4.9.315-1
-   Update to version 4.9.315
*   Tue Apr 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.9.311-1
-   Update to version 4.9.311
*   Mon Mar 21 2022 Ajay Kaher <akaher@vmware.com> 4.9.304-2
-   Fix for CVE-2022-1016
*   Mon Mar 07 2022 srinidhira0 <srinidhir@vmware.com> 4.9.304-1
-   Update to version 4.9.304
*   Fri Feb 11 2022 Sharan Turlapati <sturlapati@vmware.com> 4.9.301-1
-   Update to version 4.9.301
*   Wed Feb 09 2022 Sharan Turlapati <sturlapati@vmware.com> 4.9.297-4
-   Fix for CVE-2022-0435
*   Tue Feb 08 2022 Sharan Turlapati <sturlapati@vmware.com> 4.9.297-3
-   Fix for CVE-2022-0492
*   Tue Jan 25 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.297-2
-   Fix CVE-2022-0330
*   Fri Jan 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.297-1
-   Update to version 4.9.297
*   Sat Jan 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.296-2
-   Fix CVE-2021-4155 and CVE-2021-4204
*   Wed Jan 05 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.296-1
-   Update to version 4.9.296
-   Backport patch to fix CVE-2018-25020
*   Mon Nov 29 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.290-2
-   Fix for CVE-2020-36385
*   Wed Nov 24 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.290-1
-   Update to version 4.9.290
*   Wed Nov 10 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.9.288-2
-   Fix for CVE-2020-36322/CVE-2021-28950
*   Thu Oct 28 2021 Sharan Turlapati <sturlapati@vmware.com> 4.9.288-1
-   Update to version 4.9.288
*   Thu Oct 21 2021 Sharan Turlapati <sturlapati@vmware.com> 4.9.286-2
-   Fix for CVE-2021-38199
*   Wed Oct 13 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.9.286-1
-   Update to version 4.9.286
*   Fri Sep 17 2021 Keerthana K <keerthanak@vmware.com> 4.9.283-1
-   Update to version 4.9.283
*   Mon Aug 30 2021 Srinidhi Rao <srinidhir@vmware.com> 4.9.276-2
-   Fix for CVE-2021-22543
*   Tue Jul 27 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.276-1
-   Update to version 4.9.276
*   Thu Jul 15 2021 Him Kalyan Bordoloi <@vmware.com> 4.9.273-2
-   Fix for CVE-2021-33909
*   Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 4.9.273-1
-   Update to version 4.9.273
*   Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 4.9.270-2
-   Fix for CVE-2021-3609
*   Tue Jun 01 2021 Keerthana K <keerthanak@vmware.com> 4.9.270-1
-   Update to version 4.9.270
*   Sat May 22 2021 Ajay Kaher <akaher@vmware.com> 4.9.269-1
-   Update to version 4.9.269
*   Tue May 11 2021 Keerthana K <keerthanak@vmware.com> 4.9.268-2
-   Fix dummy console function definitions.
*   Thu Apr 29 2021 Ankit Jain <ankitja@vmware.com> 4.9.268-1
-   Update to version 4.9.268
*   Thu Apr 15 2021 srinidhira0 <srinidhir@vmware.com> 4.9.266-1
-   Update to version 4.9.266
*   Wed Mar 24 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.263-1
-   Update to version 4.9.263
*   Tue Feb 23 2021 Sharan Turlapati <sturlapati@vmware.com> 4.9.258-1
-   Update to version 4.9.258
*   Wed Jan 20 2021 Keerthana K <keerthanak@vmware.com> 4.9.252-1
-   Update to version 4.9.252
*   Mon Jan 04 2021 Ankit Jain <ankitja@vmware.com> 4.9.249-1
-   Update to version 4.9.249
*   Mon Dec 14 2020 Vikash Bansal <bvikas@vmware.com> 4.9.248-1
-   Update to version 4.9.248
*   Tue Nov 24 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.246-1
-   Update to version 4.9.246
-   Fix CVE-2019-19338 and CVE-2019-20908
*   Fri Nov 13 2020 Vikash Bansal <bvikas@vmware.com> 4.9.243-2
-   Fixes on top of CVE-2019-20811 fix
*   Fri Nov 13 2020 Keerthana K <keerthanak@vmware.com> 4.9.243-1
-   Update to version 4.9.243
*   Thu Nov 12 2020 Vikash Bansal <bvikas@vmware.com> 4.9.241-6
-   Add patch to fix CVE-2019-20811
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.9.241-5
-   Fix slab-out-of-bounds read in fbcon
*   Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 4.9.241-4
-   Fix CVE-2020-8694
*   Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 4.9.241-3
-   Fix CVE-2020-25704
*   Tue Nov 03 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.241-2
-   Fix CVE-2020-25645
*   Mon Nov 02 2020 Keerthana K <keerthanak@vmware.com> 4.9.241-1
-   Update to version 4.9.241
*   Mon Oct 19 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.240-1
-   Update to version 4.9.240
*   Mon Oct 12 2020 Ajay Kaher <akaher@vmware.com> 4.9.237-4
-   Fix for CVE-2020-16120
*   Mon Oct 12 2020 Ankit Jain <ankitja@vmware.com> 4.9.237-3
-   Fix for CVE-2020-16119
*   Wed Oct 07 2020 Ajay Kaher <akaher@vmware.com> 4.9.237-2
-   Fix mp_irqdomain_activate crash
*   Thu Oct 01 2020 Ankit Jain <ankitja@vmware.com> 4.9.237-1
-   Update to version 4.9.237
*   Wed Sep 23 2020 Ajay Kaher <akaher@vmware.com> 4.9.236-2
-   Fix for CVE-2020-14390
*   Wed Sep 23 2020 Vikash Bansal <bvikas@vmware.com> 4.9.236-1
-   Update to version 4.9.236
*   Wed Sep 23 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.228-8
-   Fix for CVE-2019-19813 and CVE-2019-19816
*   Tue Sep 22 2020 Ajay Kaher <akaher@vmware.com> 4.9.228-7
-   Fix for CVE-2020-25211
*   Thu Sep 10 2020 Vikash Bansal <bvikas@vmware.com> 4.9.228-6
-   Fix for CVE-2020-14356
*   Thu Sep 10 2020 Vikash Bansal <bvikas@vmware.com> 4.9.228-5
-   Fix for CVE-2020-14386
*   Thu Aug 13 2020 Vikash Bansal <bvikas@vmware.com> 4.9.228-4
-   Fix network stack for use-after-free issue in case timeout happens
-   on fragment queue and ip_expire is called
*   Thu Aug 06 2020 Ashwin H <ashwinh@vmware.com> 4.9.228-3
-   Fix CVE-2020-16166
*   Sun Jul 26 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.228-2
-   Fix CVE-2020-14331
*   Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.9.228-1
-   Update to version 4.9.228
*   Mon Jun 08 2020 Vikash Bansal <bvikas@vmware.com> 4.9.226-1
-   Update to version 4.9.226
*   Thu Jun 04 2020 Ajay Kaher <akaher@vmware.com> 4.9.224-3
-   Fix for CVE-2020-10757
*   Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.9.224-2
-   Keep modules of running kernel till next boot
*   Fri May 22 2020 Ajay Kaher <akaher@vmware.com> 4.9.224-1
-   Update to version 4.9.224
*   Fri May 15 2020 Vikash Bansal <bvikas@vmware.com> 4.9.221-3
-   Fix for CVE-2019-18885
*   Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.9.221-2
-   Add patch to fix CVE-2020-10711
*   Tue May 05 2020 ashwin-h <ashwinh@vmware.com> 4.9.221-1
-   Update to version 4.9.221
*   Thu Apr 30 2020 ashwin-h <ashwinh@vmware.com> 4.9.220-1
-   Update to version 4.9.220
*   Mon Apr 13 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.219-1
-   Update to version 4.9.219
*   Mon Mar 30 2020 Vikash Bansal <bvikas@vmware.com> 4.9.217-2
-   Fix for CVE-2018-13094 & CVE-2019-3900
*   Mon Mar 23 2020 Keerthana K <keerthanak@vmware.com> 4.9.217-1
-   Update to version 4.9.217
*   Tue Mar 17 2020 Ajay Kaher <akaher@vmware.com> 4.9.216-1
-   Update to version 4.9.216
*   Tue Mar 03 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.9.214-1
-   Update to version 4.9.214
*   Tue Feb 25 2020 Ajay Kaher <akaher@vmware.com> 4.9.210-3
-   Fix CVE-2019-16234
*   Fri Jan 31 2020 Ajay Kaher <akaher@vmware.com> 4.9.210-2
-   Fix CVE-2019-16233
*   Fri Jan 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.210-1
-   Update to version 4.9.210
*   Fri Dec 20 2019 Siddharth Chandrasekran <csiddharth@vmware.com> 4.9.205-2
-   Fix CVE-2019-10220
*   Wed Dec 04 2019 Ajay Kaher <akaher@vmware.com> 4.9.205-1
-   Update to version 4.9.205
*   Tue Nov 26 2019 Ajay Kaher <akaher@vmware.com> 4.9.202-2
-   Fix CVE-2019-19066
*   Tue Nov 19 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.202-1
-   Update to version 4.9.202
*   Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.201-1
-   Update to version 4.9.201
*   Thu Nov 07 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.199-1
-   Update to version 4.9.199
*   Mon Oct 21 2019 Ajay Kaher <akaher@vmware.com> 4.9.197-1
-   Update to version 4.9.197, Fix CVE-2019-17133
*   Wed Sep 18 2019 bvikas <bvikas@vmware.com> 4.9.193-1
-   Update to version 4.9.193
*   Mon Aug 12 2019 Alexey Makhalov <amakhalov@vmware.com> 4.9.189-1
-   Update to version 4.9.189 to fix CVE-2019-1125
*   Thu Jul 25 2019 Keerthana K <keerthanak@vmware.com> 4.9.185-2
-   Fix postun scriplet.
*   Thu Jul 11 2019 VIKASH BANSAL <bvikas@vmware.com> 4.9.185-1
-   Update to version 4.9.185
*   Tue Jul 02 2019 Alexey Makhalov <amakhalov@vmware.com> 4.9.182-3
-   Fix 9p vsock 16bit port number issue.
*   Thu Jun 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.182-2
-   Deprecate linux-aws-tools in favor of linux-tools.
*   Mon Jun 17 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.182-1
-   Update to version 4.9.182
-   Fix CVE-2019-12456, CVE-2019-12379, CVE-2019-12381, CVE-2019-12382,
-   CVE-2019-12378
*   Fri Jun 07 2019 Tapas Kundu <tkundu@vmware.com> 4.9.180-2
-   Enabled CONFIG_I2C_CHARDEV to support lm-sensors
*   Mon Jun 03 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.180-1
-   Update to version 4.9.180
*   Thu May 30 2019 Ajay Kaher <akaher@vmware.com> 4.9.178-4
-   Fix CVE-2019-11487
*   Thu May 30 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.178-3
-   Change default I/O scheduler to 'deadline' to fix performance issue.
*   Tue May 28 2019 Keerthana K <keerthanak@vmware.com> 4.9.178-2
-   Fix to parse through /boot folder and update symlink (/boot/photon.cfg) if
-   mulitple kernels are installed and current linux kernel is removed.
*   Fri May 24 2019 srinidhira0 <srinidhir@vmware.com> 4.9.178-1
-   Update to version 4.9.178
*   Tue May 14 2019 Ajay Kaher <akaher@vmware.com> 4.9.173-2
-   Fix CVE-2019-11599
*   Wed May 08 2019 Ajay Kaher <akaher@vmware.com> 4.9.173-1
-   Update to version 4.9.173
*   Fri Apr 05 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.168-1
-   Update to version 4.9.168
*   Wed Mar 27 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.166-1
-   Update to version 4.9.166
*   Thu Mar 14 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.163-1
-   Update to version 4.9.163
*   Mon Feb 25 2019 Ajay Kaher <akaher@vmware.com> 4.9.154-3
-   Fix CVE-2018-16882
*   Thu Feb 21 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.9.154-2
-   Fix CVE-2019-8912
*   Mon Feb 04 2019 Ajay Kaher <akaher@vmware.com> 4.9.154-1
-   Update to version 4.9.154
*   Wed Jan 23 2019 Ajay Kaher <akaher@vmware.com> 4.9.140-6
-   Fix IRQ issue by using effective_affinity
-   Remove nvme_io_irq_without_affinity.patch
*   Thu Jan 17 2019 Ajay Kaher <akaher@vmware.com> 4.9.140-5
-   Fix IRQ issues with NVMe on Azure.
*   Tue Jan 15 2019 Alexey Makhalov <amakhalov@vmware.com> 4.9.140-4
-   .config: disable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
*   Thu Dec 20 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.140-3
-   .config: CONFIG_FANOTIFY_ACCESS_PERMISSIONS=y
-   Removed deprecated -q option for depmod
*   Mon Dec 17 2018 Ajay Kaher <akaher@vmware.com> 4.9.140-2
-   Enable pci-hyperv support and apply relevant patches
*   Mon Nov 26 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.140-1
-   Update to version 4.9.140
*   Fri Nov 16 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.9.137-1
-   Update to version 4.9.137
*   Tue Oct 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.130-2
-   Improve error-handling of rdrand-rng kernel driver.
*   Mon Oct 01 2018 srinidhira0 <srinidhir@vmware.com> 4.9.130-1
-   Update to version 4.9.130
*   Mon Sep 10 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.124-2
-   Fix for CVE-2018-13053
*   Fri Aug 24 2018 Bo Gan <ganb@vmware.com> 4.9.124-1
-   Update to version 4.9.124
*   Fri Aug 17 2018 Bo Gan <ganb@vmware.com> 4.9.120-1
-   Update to version 4.9.120 (l1tf fixes)
*   Thu Aug 09 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.118-2
-   Fix CVE-2018-12233
*   Tue Aug 07 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.118-1
-   Update to version 4.9.118
*   Mon Jul 30 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.116-1
-   Update to version 4.9.116 and clear stack on fork.
*   Wed Jul 25 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.114-2
-   .config: usb_serial_pl2303=m,wlan=y,can=m,gpio=y,pinctrl=y,iio=m
*   Mon Jul 23 2018 srinidhira0 <srinidhir@vmware.com> 4.9.114-1
-   Update to version 4.9.114
*   Thu Jul 19 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.111-5
-   Apply out-of-tree patches needed for AppArmor.
*   Tue Jul 17 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.111-4
-   Fix CVE-2018-10322
*   Thu Jul 12 2018 Srinidhi Rao <srinidhir@vmware.com> 4.9.111-3
-   Fix CVE-2017-18232, CVE-2017-18249 and CVE-2018-10323
*   Wed Jul 11 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.111-2
-   Enable and use AppArmor security module by default.
*   Sat Jul 07 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.111-1
-   Update to version 4.9.111
*   Sun Jul 01 2018 Ron Jaegers <ron.jaegers@gmail.com> 4.9.109-3
-   Enable USB_ACM support in the config.
*   Wed Jun 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.109-2
-   Add rdrand-based RNG driver to enhance kernel entropy.
*   Thu Jun 21 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.109-1
-   Update to version 4.9.109
*   Mon May 21 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.101-2
-   Add the f*xattrat family of syscalls.
*   Mon May 21 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.101-1
-   Update to version 4.9.101 and fix CVE-2018-3639.
*   Wed May 09 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.99-1
-   Update to version 4.9.99
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.98-2
-   Fix CVE-2017-18216, CVE-2018-8043, CVE-2018-8087, CVE-2017-18241,
-   CVE-2017-18224.
*   Fri May 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.98-1
-   Update to version 4.9.98
*   Wed May 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.97-3
-   Fix CVE-2017-18255.
*   Tue May 01 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.97-2
-   Fix CVE-2018-1000026.
*   Mon Apr 30 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.97-1
-   Update to version 4.9.97. Apply 3rd vmxnet3 patch.
*   Mon Apr 23 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.94-2
-   Add full retpoline support by building with retpoline-enabled gcc.
*   Wed Apr 18 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.94-1
-   Update to version 4.9.94. Fix panic in ip_set.
-   .config: disable XEN_BALLOON_MEMORY_HOTPLUG
*   Mon Apr 02 2018 Alexey Makhalov <amakhalov@vmware.com> 4.9.92-1
-   Update to version 4.9.92. Apply vmxnet3 patches.
*   Tue Mar 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.90-1
-   Update to version 4.9.90
*   Thu Mar 22 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.89-1
-   Update to version 4.9.89
*   Mon Feb 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.80-1
-   Update to version 4.9.80
*   Wed Jan 31 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.79-1
-   Update version to 4.9.79
*   Fri Jan 26 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.78-1
-   Update version to 4.9.78.
*   Wed Jan 10 2018 Bo Gan <ganb@vmware.com> 4.9.76-1
-   Version update
*   Sun Jan 07 2018 Bo Gan <ganb@vmware.com> 4.9.75-3
-   Second Spectre fix, clear user controlled registers upon syscall entry
*   Sun Jan 07 2018 Bo Gan <ganb@vmware.com> 4.9.75-2
-   Initial Spectre fix
*   Fri Jan 05 2018 Anish Swaminathan <anishs@vmware.com> 4.9.75-1
-   Version update to 4.9.75
*   Thu Jan 04 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-3
-   Update vsock transport for 9p with newer version.
*   Wed Jan 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-2
-   Fix SMB3 mount regression.
*   Tue Jan 02 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.74-1
-   Version update
-   Add patches to fix CVE-2017-8824, CVE-2017-17448 and CVE-2017-17450.
*   Thu Dec 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.71-1
-   Version update
*   Tue Dec 05 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.66-2
-   Sign and compress modules after stripping. fips=1 requires signed modules
*   Mon Dec 04 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.66-1
-   Version update
*   Tue Nov 21 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.64-1
-   Version update
*   Mon Nov 06 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.60-1
-   Version update
*   Wed Oct 11 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-3
-   Add patch "KVM: Don't accept obviously wrong gsi values via
    KVM_IRQFD" to fix CVE-2017-1000252.
*   Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.53-2
-   Build hang (at make oldconfig) fix.
*   Thu Oct 05 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.53-1
-   Version update
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-3
-   Allow privileged CLONE_NEWUSER from nested user namespaces.
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-2
-   Fix CVE-2017-11472 (ACPICA: Namespace: fix operand cache leak)
*   Mon Oct 02 2017 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 4.9.52-1
-   Version update
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-2
-   Requires coreutils or toybox
*   Mon Sep 04 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.47-1
-   Fix CVE-2017-11600
*   Tue Aug 22 2017 Anish Swaminathan <anishs@vmware.com> 4.9.43-2
-   Add missing xen block drivers
*   Mon Aug 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.43-1
-   Version update
-   [feature] new sysctl option unprivileged_userns_clone
*   Wed Aug 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-2
-   Fix CVE-2017-7542
-   [bugfix] Added ccm,gcm,ghash,lzo crypto modules to avoid
    panic on modprobe tcrypt
*   Mon Aug 07 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.41-1
-   Version update
*   Fri Aug 04 2017 Bo Gan <ganb@vmware.com> 4.9.38-6
-   Fix initramfs triggers
*   Tue Aug 01 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-5
-   Allow some algorithms in FIPS mode
-   Reverts 284a0f6e87b0721e1be8bca419893902d9cf577a and backports
-   bcf741cb779283081db47853264cc94854e7ad83 in the kernel tree
-   Enable additional NF features
*   Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-4
-   Add patches in Hyperv codebase
*   Fri Jul 21 2017 Anish Swaminathan <anishs@vmware.com> 4.9.38-3
-   Add missing hyperv drivers
*   Thu Jul 20 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-2
-   Disable scheduler beef up patch
*   Tue Jul 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.38-1
-   Fix CVE-2017-11176 and CVE-2017-10911
*   Mon Jul 03 2017 Xiaolin Li <xiaolinl@vmware.com> 4.9.34-3
-   Add libdnet-devel, kmod-devel and libmspack-devel to BuildRequires
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 4.9.34-2
-   Added obsolete for deprecated linux-dev package
*   Wed Jun 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.34-1
-   [feature] 9P FS security support
-   [feature] DM Delay target support
-   Fix CVE-2017-1000364 ("stack clash") and CVE-2017-9605
*   Thu Jun 8 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.31-1
-   Fix CVE-2017-8890, CVE-2017-9074, CVE-2017-9075, CVE-2017-9076
    CVE-2017-9077 and CVE-2017-9242
-   [feature] IPV6 netfilter NAT table support
*   Fri May 26 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.30-1
-   Added ENA driver for AMI
-   Fix CVE-2017-7487 and CVE-2017-9059
*   Wed May 17 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.9.28-2
-   Enable IPVLAN module.
*   Tue May 16 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.28-1
-   Version update
*   Wed May 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.27-1
-   Version update
*   Sun May 7 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.26-1
-   Version update
-   Removed version suffix from config file name
*   Thu Apr 27 2017 Bo Gan <ganb@vmware.com> 4.9.24-2
-   Support dynamic initrd generation
*   Tue Apr 25 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.24-1
-   Fix CVE-2017-6874 and CVE-2017-7618.
-   Fix audit-devel BuildRequires.
-   .config: build nvme and nvme-core in kernel.
*   Mon Mar 6 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-2
-   .config: NSX requirements for crypto and netfilter
*   Tue Feb 28 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.13-1
-   Update to linux-4.9.13 to fix CVE-2017-5986 and CVE-2017-6074
*   Thu Feb 09 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.9-1
-   Update to linux-4.9.9 to fix CVE-2016-10153, CVE-2017-5546,
    CVE-2017-5547, CVE-2017-5548 and CVE-2017-5576.
-   .config: added CRYPTO_FIPS support.
*   Tue Jan 10 2017 Alexey Makhalov <amakhalov@vmware.com> 4.9.2-1
-   Update to linux-4.9.2 to fix CVE-2016-10088
-   Move linux-tools.spec to linux.spec as -tools subpackage
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 4.9.0-2
-   BuildRequires Linux-PAM-devel
*   Mon Dec 12 2016 Alexey Makhalov <amakhalov@vmware.com> 4.9.0-1
-   Update to linux-4.9.0
-   Add paravirt stolen time accounting feature (from linux-esx),
    but disable it by default (no-vmw-sta cmdline parameter)
*   Thu Dec  8 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-3
-   net-packet-fix-race-condition-in-packet_set_ring.patch
    to fix CVE-2016-8655
*   Wed Nov 30 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-2
-   Expand `uname -r` with release number
-   Check for build-id matching
-   Added syscalls tracing support
-   Compress modules
*   Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.35-1
-   Update to linux-4.4.35
-   vfio-pci-fix-integer-overflows-bitmask-check.patch
    to fix CVE-2016-9083
*   Tue Nov 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-4
-   net-9p-vsock.patch
*   Thu Nov 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-3
-   tty-prevent-ldisc-drivers-from-re-using-stale-tty-fields.patch
    to fix CVE-2015-8964
*   Tue Nov 15 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-2
-   .config: add cgrup_hugetlb support
-   .config: add netfilter_xt_{set,target_ct} support
-   .config: add netfilter_xt_match_{cgroup,ipvs} support
*   Thu Nov 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.31-1
-   Update to linux-4.4.31
*   Fri Oct 21 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.26-1
-   Update to linux-4.4.26
*   Wed Oct 19 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-6
-   net-add-recursion-limit-to-GRO.patch
-   scsi-arcmsr-buffer-overflow-in-arcmsr_iop_message_xfer.patch
*   Tue Oct 18 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-5
-   ipip-properly-mark-ipip-GRO-packets-as-encapsulated.patch
-   tunnels-dont-apply-GRO-to-multiple-layers-of-encapsulation.patch
*   Mon Oct  3 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-4
-   Package vmlinux with PROGBITS sections in -debuginfo subpackage
*   Tue Sep 27 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-3
-   .config: CONFIG_IP_SET_HASH_{IPMARK,MAC}=m
*   Tue Sep 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-2
-   Add -release number for /boot/* files
-   Use initrd.img with version and release number
-   Rename -dev subpackage to -devel
*   Wed Sep  7 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.20-1
-   Update to linux-4.4.20
-   apparmor-fix-oops-validate-buffer-size-in-apparmor_setprocattr.patch
-   keys-fix-asn.1-indefinite-length-object-parsing.patch
*   Thu Aug 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-11
-   vmxnet3 patches to bumpup a version to 1.4.8.0
*   Wed Aug 10 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-10
-   Added VSOCK-Detach-QP-check-should-filter-out-non-matching-QPs.patch
-   .config: pmem hotplug + ACPI NFIT support
-   .config: enable EXPERT mode, disable UID16 syscalls
*   Thu Jul 07 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-9
-   .config: pmem + fs_dax support
*   Fri Jun 17 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-8
-   patch: e1000e-prevent-div-by-zero-if-TIMINCA-is-zero.patch
-   .config: disable rt group scheduling - not supported by systemd
*   Wed Jun 15 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-7
-   fixed the capitalization for - System.map
*   Thu May 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-6
-   patch: REVERT-sched-fair-Beef-up-wake_wide.patch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.8-5
-   GA - Bump release of all rpms
*   Mon May 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-4
-   Fixed generation of debug symbols for kernel modules & vmlinux.
*   Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> 4.4.8-3
-   Added patches to fix CVE-2016-3134, CVE-2016-3135
*   Wed May 18 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.8-2
-   Enabled CONFIG_UPROBES in config as needed by ktap
*   Wed May 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.4.8-1
-   Update to linux-4.4.8
-   Added net-Drivers-Vmxnet3-set-... patch
*   Tue May 03 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-27
-   Compile Intel GigE and VMXNET3 as part of kernel.
*   Thu Apr 28 2016 Nick Shi <nshi@vmware.com> 4.2.0-26
-   Compile cramfs.ko to allow mounting cramfs image
*   Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-25
-   Revert network interface renaming disable in kernel.
*   Tue Mar 29 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-24
-   Support kmsg dumping to vmware.log on panic
-   sunrpc: xs_bind uses ip_local_reserved_ports
*   Mon Mar 28 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-23
-   Enabled Regular stack protection in Linux kernel in config
*   Thu Mar 17 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-22
-   Restrict the permissions of the /boot/System.map-X file
*   Fri Mar 04 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-21
-   Patch: SUNRPC: Do not reuse srcport for TIME_WAIT socket.
*   Wed Mar 02 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-20
-   Patch: SUNRPC: Ensure that we wait for connections to complete
    before retrying
*   Fri Feb 26 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-19
-   Disable watchdog under VMware hypervisor.
*   Thu Feb 25 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-18
-   Added rpcsec_gss_krb5 and nfs_fscache
*   Mon Feb 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-17
-   Added sysctl param to control weighted_cpuload() behavior
*   Thu Feb 18 2016 Divya Thaluru <dthaluru@vmware.com> 4.2.0-16
-   Disabling network renaming
*   Sun Feb 14 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-15
-   veth patch: don’t modify ip_summed
*   Thu Feb 11 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-14
-   Full tickless -> idle tickless + simple CPU time accounting
-   SLUB -> SLAB
-   Disable NUMA balancing
-   Disable stack protector
-   No build_forced no-CBs CPUs
-   Disable Expert configuration mode
-   Disable most of debug features from 'Kernel hacking'
*   Mon Feb 08 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-13
-   Double tcp_mem limits, patch is added.
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  4.2.0-12
-   Fixes for CVE-2015-7990/6937 and CVE-2015-8660.
*   Tue Jan 26 2016 Anish Swaminathan <anishs@vmware.com> 4.2.0-11
-   Revert CONFIG_HZ=250
*   Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-10
-   Fix for CVE-2016-0728
*   Wed Jan 13 2016 Alexey Makhalov <amakhalov@vmware.com> 4.2.0-9
-   CONFIG_HZ=250
*   Tue Jan 12 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-8
-   Remove rootfstype from the kernel parameter.
*   Mon Jan 04 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-7
-   Disabled all the tracing options in kernel config.
-   Disabled preempt.
-   Disabled sched autogroup.
*   Thu Dec 17 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-6
-   Enabled kprobe for systemtap & disabled dynamic function tracing in config
*   Fri Dec 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-5
-   Added oprofile kernel driver sub-package.
*   Fri Nov 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 4.2.0-4
-   Change the linux image directory.
*   Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-3
-   Added the build essential files in the dev sub-package.
*   Mon Nov 09 2015 Vinay Kulkarni <kulkarniv@vmware.com> 4.2.0-2
-   Enable Geneve module support for generic kernel.
*   Fri Oct 23 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.0-1
-   Upgraded the generic linux kernel to version 4.2.0 & and updated timer handling to full tickless mode.
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.9-5
-   Added driver support for frame buffer devices and ACPI
*   Wed Sep 2 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-4
-   Added mouse ps/2 module.
*   Fri Aug 14 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-3
-   Use photon.cfg as a symlink.
*   Thu Aug 13 2015 Alexey Makhalov <amakhalov@vmware.com> 4.0.9-2
-   Added environment file(photon.cfg) for grub.
*   Wed Aug 12 2015 Sharath George <sharathg@vmware.com> 4.0.9-1
-   Upgrading kernel version.
*   Wed Aug 12 2015 Alexey Makhalov <amakhalov@vmware.com> 3.19.2-5
-   Updated OVT to version 10.0.0.
-   Rename -gpu-drivers to -drivers-gpu in accordance to directory structure.
-   Added -sound package/
*   Tue Aug 11 2015 Anish Swaminathan<anishs@vmware.com> 3.19.2-4
-   Removed Requires dependencies.
*   Fri Jul 24 2015 Harish Udaiya Kumar <hudaiyakumar@gmail.com> 3.19.2-3
-   Updated the config file to include graphics drivers.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 3.13.3-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.13.3-1
-   Initial build. First version

