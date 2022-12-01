Summary:        Mesa is an OpenGL compatible 3D graphics library.
Name:           mesa
Version:        22.1.1
Release:        2%{?dist}
License:        MIT
URL:            http://www.mesa3d.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.freedesktop.org/pub/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=04f827ac800e22c24923606fa5a3b6707db876ee973b2442efbd439675596f7481fb4eefcb94bc013afa7b223663324af8592af566d379bbb9c0601f2b700807

BuildRequires:  libdrm-devel >= 2.4.88
BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  elfutils-libelf-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-markupsafe
BuildRequires:  python3-mako
BuildRequires:  libffi-devel
BuildRequires:  llvm-devel
BuildRequires:  expat-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libwayland-client
BuildRequires:  libwayland-server
BuildRequires:  libwayland-egl
BuildRequires:  libpciaccess-devel
BuildRequires:  bison

Requires:       libllvm
Requires:       expat-libs
Provides:       pkg-config(dri)

%description
Mesa is an OpenGL compatible 3D graphics library.

%package        vulkan-drivers
Summary:        Mesa Vulkan drivers

%description     vulkan-drivers
The drivers with support for the Vulkan API.

%package        libgbm
Summary:        Mesa gbm runtime library
Requires:       expat
Requires:       libdrm
Requires:       libwayland-server
Provides:       libgbm

%description    libgbm
Mesa gbm runtime library.

%package        libgbm-devel
Summary:        Mesa libgbm development package
Requires:       %{name}-libgbm = %{version}-%{release}
Provides:       libgbm-devel

%description    libgbm-devel
Mesa libgbm development package.

%prep
%autosetup -n %{name}-%{name}-%{version} -p1

%build
meson --prefix=%{_prefix} build/ \
        -Dgallium-vdpau=disabled \
        -Dgallium-xvmc=disabled \
        -Dgallium-omx=disabled \
        -Dgallium-va=disabled \
        -Dgallium-xa=disabled \
        -Dgallium-nine=false \
        -Dgallium-opencl=disabled \
        -Dvulkan-drivers=amd \
        -Dplatforms=wayland \
        -Dosmesa=false \
        -Dvulkan-layers=device-select \
        -Dshared-glapi=disabled \
        -Dgles1=disabled \
        -Dopengl=false \
        -Dgbm=enabled \
        -Dglx=disabled \
        -Degl=disabled \
        -Dglvnd=false \
        -Dllvm=enabled \
        -Dshared-llvm=enabled \
        -Dvalgrind=disabled \
        -Dbuild-tests=false \
        -Dselinux=false \
        -Dvulkan-drivers=auto \
        -Dintel-clc=disabled \
        -Dgles2=disabled \
        -Ddri3=disabled \
        -Dmicrosoft-clc=disabled \
        %{nil}

%install
DESTDIR=%{buildroot}/ ninja -C build install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)

%files vulkan-drivers
%defattr(-,root,root)
%{_libdir}/libvulkan_lvp.so
%{_datadir}/vulkan/icd.d/lvp_icd.*.json
%{_datadir}/vulkan/implicit_layer.d/VkLayer_MESA_device_select.json
%{_libdir}/libVkLayer_MESA_device_select.so
%{_datadir}/drirc.d/00-mesa-defaults.conf
%ifarch x86_64
%{_libdir}/libvulkan_radeon.so
%{_libdir}/libvulkan_intel.so
%{_datadir}/drirc.d/00-radv-defaults.conf
%{_datadir}/vulkan/icd.d/intel_icd.x86_64.json
%{_datadir}/vulkan/icd.d/radeon_icd.x86_64.json
%endif

%files libgbm
%defattr(-,root,root)
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*

%files libgbm-devel
%defattr(-,root,root)
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%changelog
* Mon Sep 19 2022 Shivani Agarwal <shivania2@vmware.com> 22.1.1-2
- Enable libgbm
* Fri Jun 10 2022 Shivani Agarwal <shivania2@vmware.com> 22.1.1-1
- Initial Version
