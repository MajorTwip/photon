%define debug_package %{nil}
Summary:        Device trees and overlays for Raspberry Pi
Name:           dtb-raspberrypi
Version:        5.10.4.2021.01.07
# Version Scheme: {kernel_ver}.{year}.{month}.{day}
Release:        3%{?dist}
License:        GPLv2
%define rpi_linux_branch rpi-5.10.y
%define rpi_linux_req 5.10.4
URL:            https://github.com/raspberrypi/linux
Source0:        https://github.com/raspberrypi/linux/archive/rpi-linux-%{version}.tar.gz
%define sha512  rpi-linux=8e176075f30fa4c6847c0bc11c3d9207929247bacd518e45aeff85a3eaffce229699d953f16cd8e948b37326cea2adaa2cf518858c3813a3b30565c97af8b2fc
Group:          System/Boot
Vendor:         VMware, Inc.
Distribution:   Photon

# enable fb to fix HDMI issue
Patch1:         0001-upstream-pi4-overlay-enable-fb.patch
# spi and audio overlays
Patch2:         0001-spi0-overlays-files.patch
Patch3:         0002-audio-overlays-files.patch

BuildRequires:  dtc
BuildRequires:  bison
Requires:       dtb-rpi3 = %{version}-%{release}
Requires:       dtb-rpi4 = %{version}-%{release}
Requires:       dtb-rpi-overlay = %{version}-%{release}
BuildArch:      aarch64

%description
Metapackage to install all Kernel Device Tree and Overlay Blobs for Raspberry Pi

%package -n dtb-rpi3
Summary:        Kernel Device Tree Blob files for Raspberry Pi3
Group:          System Environment/Kernel
Conflicts:      linux < %{rpi_linux_req}
Conflicts:      dtb-rpi-overlay < %{version}-%{release}
Conflicts:      dtb-rpi-overlay > %{version}-%{release}
%description -n dtb-rpi3
Kernel Device Tree Blob files for Raspberry Pi3

%package -n dtb-rpi4
Summary:        Kernel Device Tree Blob files for Raspberry Pi4
Group:          System Environment/Kernel
Conflicts:      linux < %{rpi_linux_req}
Conflicts:      dtb-rpi-overlay < %{version}-%{release}
Conflicts:      dtb-rpi-overlay > %{version}-%{release}
%description -n dtb-rpi4
Kernel Device Tree Blob files for Raspberry Pi4

%package -n dtb-rpi-overlay
Summary:        Kernel Device Tree Overlay Blob files for Raspberry Pi
Group:          System Environment/Kernel
Conflicts:      linux < %{rpi_linux_req}
%description -n dtb-rpi-overlay
Kernel Device Tree Overlay Blob files for Raspberry Pi

%prep
%autosetup -p1 -n rpi-linux-%{version}

%build
make %{?_smp_mflags} mrproper
make %{?_smp_mflags} bcm2711_defconfig
make %{?_smp_mflags} dtbs

%install
make dtbs_install INSTALL_DTBS_PATH=%{buildroot}/boot/efi %{?_smp_mflags}
pushd %{buildroot}/boot/efi
mv broadcom excluded
mv excluded/bcm2837-rpi-3-*.dtb ./
mv excluded/bcm2711-rpi-4-*.dtb ./
rm -rf excluded
popd

%files
%defattr(-,root,root)

%files -n dtb-rpi3
%defattr(-,root,root)
/boot/efi/bcm2837-rpi-3-*.dtb

%files -n dtb-rpi4
%defattr(-,root,root)
/boot/efi/bcm2711-rpi-4-*.dtb

%files -n dtb-rpi-overlay
%defattr(-,root,root,0755)
/boot/efi/overlays

%changelog
*   Thu Oct 13 2022 Piyush Gupta <gpiyush@vmware.com> 5.10.4.2021.01.07-3
-   Added bison as BuildRequires.
*   Thu Jan 21 2021 Ajay Kaher <akaher@vmware.com> 5.10.4.2021.01.07-2
-   Adding audio and spi overlay
*   Thu Jan 07 2021 Ajay Kaher <akaher@vmware.com> 5.10.4.2021.01.07-1
-   Update to v5.10.4.2021.01.07
-   Enable fb in upstream-pi4 overlay
*   Fri Sep 11 2020 Bo Gan <ganb@vmware.com> 5.9.0.2020.09.23-1
-   Initial packaging
