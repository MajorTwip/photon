%define debug_package %{nil}
%define __os_install_post %{nil}

Summary:    GRand Unified Bootloader
Name:       grub2
Version:    2.06
Release:    2%{?dist}
License:    GPLv3+
URL:        http://www.gnu.org/software/grub
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://ftp.gnu.org/gnu/grub/grub-%{version}.tar.xz
%define sha512 grub=4f11c648f3078567e53fc0c74d5026fdc6da4be27d188975e79d9a4df817ade0fe5ad2ddd694238a07edc45adfa02943d83c57767dd51548102b375e529e8efe

Patch0:     Tweak-grub-mkconfig.in-to-work-better-in-Photon.patch

BuildRequires:  device-mapper-devel
BuildRequires:  xz-devel
BuildRequires:  systemd-devel
BuildRequires:  bison

Requires:   xz
Requires:   device-mapper

%description
The GRUB package contains the GRand Unified Bootloader.

%package lang
Summary:    Additional language files for grub
Group:      System Environment/Programming
Requires:   %{name} = %{version}
%description lang
These are the additional language files of grub.

%ifarch x86_64
%package pc
Summary:    GRUB Library for BIOS
Group:      System Environment/Programming
Requires:   %{name} = %{version}
%description pc
Additional library files for grub
%endif

%package efi
Summary:    GRUB Library for UEFI
Group:      System Environment/Programming
Requires:   %{name} = %{version}
%description efi
Additional library files for grub

%prep
%autosetup -p1 -n grub-%{version}

%build
sh ./autogen.sh
%ifarch x86_64
mkdir build-for-pc
pushd build-for-pc
sh ../configure \
    --prefix=%{_prefix} \
    --sbindir=/sbin \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=pc \
    --target=i386 \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"
make %{?_smp_mflags}
make DESTDIR=$PWD/../install-for-pc install %{?_smp_mflags}
popd
%endif

mkdir build-for-efi
pushd build-for-efi
sh ../configure \
    --prefix=%{_prefix} \
    --sbindir=/sbin \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=efi \
    --target=%{_arch} \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"
make %{?_smp_mflags}
make DESTDIR=$PWD/../install-for-efi install %{?_smp_mflags}
popd

# make sure all files are same between two configure except the /usr/lib/grub
%check
%ifarch x86_64
diff -sr install-for-efi/sbin install-for-pc/sbin && \
diff -sr install-for-efi%{_bindir} install-for-pc%{_bindir} && \
diff -sr install-for-efi%{_sysconfdir} install-for-pc%{_sysconfdir} && \
diff -sr install-for-efi%{_datarootdir} install-for-pc%{_datarootdir}
%endif

%install
mkdir -p %{buildroot}
cp -a install-for-efi/. %{buildroot}/.
%ifarch x86_64
cp -a install-for-pc/. %{buildroot}/.
%endif
mkdir %{buildroot}%{_sysconfdir}/default
touch %{buildroot}%{_sysconfdir}/default/grub
mkdir %{buildroot}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub %{buildroot}%{_sysconfdir}/sysconfig/grub
mkdir -p %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
rm -rf %{buildroot}%{_infodir}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/grub.d
%config() %{_sysconfdir}/bash_completion.d/grub
%config() %{_sysconfdir}/grub.d/00_header
%config() %{_sysconfdir}/grub.d/10_linux
%config() %{_sysconfdir}/grub.d/20_linux_xen
%config() %{_sysconfdir}/grub.d/30_os-prober
%config() %{_sysconfdir}/grub.d/30_uefi-firmware
%config(noreplace) %{_sysconfdir}/grub.d/40_custom
%config(noreplace) %{_sysconfdir}/grub.d/41_custom
%{_sysconfdir}/grub.d/README
/sbin/*
%{_bindir}/*
%{_datarootdir}/grub/*
%{_sysconfdir}/sysconfig/grub
%{_sysconfdir}/default/grub
%ghost %config(noreplace) /boot/%{name}/grub.cfg

%ifarch x86_64
%files pc
%{_libdir}/grub/i386-pc
%files efi
%{_libdir}/grub/x86_64-efi
%endif

%ifarch aarch64
%files efi
%{_libdir}/grub/*
%endif

%files lang
%defattr(-,root,root)
%{_datarootdir}/locale/*

%changelog
*   Wed Aug 18 2021 Ankit Jain <ankitja@vmware.com> 2.06-2
-   Remove prompt message for default -o option
-   in grub2-mkconfig
*   Wed Jun 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.06-1
-   Upgrade to version 2.06
*   Mon Mar 15 2021 Ajay Kaher <akaher@vmware.com> 2.06~rc1-1
-   upgrade to 2.06.rc1-1
*   Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 2.04-2
-   Fixes for CVE-2020-14372, CVE-2020-25632, CVE-2020-25647,
    CVE-2020-27749, CVE-2020-27779, CVE-2021-3418, CVE-2021-20225,
    CVE-2021-20233.
*   Tue Jul 21 2020 Alexey Makhalov <amakhalov@vmware.com> 2.04-1
-   Fixes for CVE-2020-10713, CVE-2020-14308, CVE-2020-14309,
    CVE-2020-14310, CVE-2020-14311, CVE-2020-15705, CVE-2020-15706
    CVE-2020-15707.
*   Wed Aug 14 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-13
-   Add one more patch from fc30 to fix arm64 build.
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-12
-   Update grub version from ~rc3 to release.
-   Enhance SB + TPM support (19 patches from grub2-2.02-70.fc30)
-   Remove i386-pc modules from grub2-efi
*   Fri Jan 25 2019 Alexey Makhalov <amakhalov@vmware.com> 2.02-11
-   Disable efinet for aarch64 to workwround NXP ls1012a frwy PFE bug.
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.02-10
-   Aarch64 support
*   Fri Jun 2  2017 Bo Gan <ganb@vmware.com> 2.02-9
-   Split grub2 to grub2 and grub2-pc, remove grub2-efi spec
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com>  2.02-8
-   Version update to 2.02~rc2
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02-7
-   Add fix for CVE-2015-8370
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02-6
-   Change systemd dependency
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.02-5
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.02-4
-   GA - Bump release of all rpms
*   Fri Oct 02 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-3
-   Adding patch to boot entries with out password.
*   Wed Jul 22 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-2
-   Changing program name from grub to grub2.
*   Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> 2.02-1
-   Updating grub to 2.02
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.00-1
-   Initial build.  First version
