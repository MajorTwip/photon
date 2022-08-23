Name:           kpatch
Summary:        Dynamic kernel patching
Version:        0.9.6
Release:        3%{?dist}
URL:            http://github.com/dynup/kpatch
License:        GPLv2
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/dynup/kpatch/archive/refs/tags/kpatch-v%{version}.tar.gz
%define sha512 kpatch=898c5704098c473187f2eab9bccd5fb3cfc31f4211492d658abcd0b7cac6d03f11a27df19a56ad17c20163803084ddf54a27defcf12b4975a8a8eb5dbad73f21

Source1:        scripts/auto_livepatch.sh
Source2:        scripts/gen_livepatch.sh
Source3:        scripts/README.txt
Source4:        scripts/dockerfiles/Dockerfile.ph3
Source5:        scripts/dockerfiles/Dockerfile.ph4

BuildArch:      x86_64

Patch0:         0001-Added-support-for-Photon-OS.patch
Patch1:         0001-adding-option-to-set-description-field-of-module.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  elfutils
BuildRequires:  elfutils-devel
BuildRequires:  systemd

Requires:       kmod
Requires:       bash
Requires:       rpm-build
Requires:       (coreutils or toybox or coreutils-selinux)
Requires:       gawk
Requires:       util-linux
Requires:       binutils
Requires:       (sed or toybox)
Requires:       (findutils or toybox)

%description
Contains the kpatch utility, which allows loading of kernel livepatches.
kpatch is a Linux dynamic kernel patching tool which allows you to patch a
running kernel without rebooting or restarting any processes.  It enables
sysadmins to apply critical security patches to the kernel immediately, without
having to wait for long-running tasks to complete, users to log off, or
for scheduled reboot windows.  It gives more control over up-time without
sacrificing security or stability.

%package build
Requires: %{name} = %{version}-%{release}
Requires: build-essential
Requires: tar
Summary: Dynamic kernel patching

%description build
Contains the kpatch-build tool, to enable creation of kernel livepatches.

%package devel
Summary: Development files for kpatch

%description devel
Contains files for developing with kpatch.

%package utils
Requires: %{name} = %{version}-%{release}
Requires: %{name}-build = %{version}-%{release}
Requires: docker
Summary: Tools to automate livepatch building.

%description utils
Contains auto_livepatch and gen_livepatch scripts.

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX=%{_usr} %{?_smp_mflags}
mkdir -p %{buildroot}%{_sysconfdir}/auto_livepatch/dockerfiles
cp %{SOURCE4} %{SOURCE5} %{buildroot}%{_sysconfdir}/auto_livepatch/dockerfiles
cp %{SOURCE1} %{SOURCE2} %{buildroot}%{_bindir}
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/auto_livepatch

#%check
# make check require shellcheck package, which is not in photon

%files
%defattr(-,root,root,-)
%license COPYING
%{_sbindir}/kpatch
%{_usr}%{_unitdir}/*
%{_sysconfdir}/init/kpatch.conf

%files build
%defattr(-,root,root,-)
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root,-)
%doc README.md doc/patch-author-guide.md
%{_mandir}/man1/kpatch-build.1*
%{_mandir}/man1/kpatch.1*

%files utils
%defattr(-,root,root,-)
%doc %{_sysconfdir}/auto_livepatch/README.txt
%{_bindir}/auto_livepatch.sh
%{_bindir}/gen_livepatch.sh
%{_sysconfdir}/auto_livepatch/dockerfiles/*

%changelog
* Mon Aug 22 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-3
- Fixed issue where auto_livepatch.sh keeps description file around
- and alwasy copies into container.
* Mon Aug 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-2
- Adding option both in kpatch-utils scripts and kpatch-build itself for
- setting the description field of a livepatch module.
* Tue Aug 9 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 0.9.6-1
- Initial addition to photon. Modified from provided kpatch.spec on GitHub.
- Also includes automated livepatch building subpackage as kpatch-utils.
