Summary:    Wayland Compositor Infrastructure
Name:       wayland
Version:    1.20.0
Release:    2%{?dist}
License:    MIT
URL:        http://wayland.freedesktop.org
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution: Photon

Source0: https://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
%define sha512 %{name}=e8a1f410994b947f850799bdd0d95a2429d8467f853e62a0ab3915a4e9fe130f8aa977e03715114ab740c6ec546edea63d275ce7f927d4f3029ea126e6a7d215

BuildRequires: libxml2-devel
BuildRequires: meson
BuildRequires: ninja-build
BuildRequires: libffi-devel
BuildRequires: expat-devel
BuildRequires: libxslt-devel

%description
Wayland is a protocol for a compositor to talk to its clients as well as a C library implementation of that protocol. The compositor can be a standalone display server running on Linux kernel modesetting and evdev input devices, an X application, or a Wayland client itself. The clients can be traditional applications, X servers (rootless or fullscreen) or other display servers.

%package    devel
Summary:    Development files for wayland
Requires:   libwayland-client = %{version}-%{release}
Requires:   libwayland-cursor = %{version}-%{release}
Requires:   libwayland-egl = %{version}-%{release}
Requires:   libwayland-server = %{version}-%{release}

%description devel
It contains the libraries and header files for developing applications that use wayland.

%package    -n libwayland-client
Summary:    wayland client library for wayland
Requires:   libffi

%description -n libwayland-client
It contains the wayland client libraries

%package    -n libwayland-cursor
Summary:    wayland cursor library for wayland
Requires:   libwayland-client = %{version}-%{release}

%description -n libwayland-cursor
It contains the wayland cursor libraries

%package    -n libwayland-egl
Summary:    wayland egl library for wayland

%description -n libwayland-egl
It contains the wayland egl libraries

%package    -n libwayland-server
Summary:    wayland server library for wayland
Requires:   libffi

%description -n libwayland-server
It contains the wayland server libraries

%prep
%autosetup

%build
CONFIGURE_OPTS=(
    -Ddocumentation=false
    )
%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%if 0%{?with_check}
%check
%meson_test
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-scanner
%{_includedir}/%{name}-*.h
%{_libdir}/pkgconfig/%{name}-*.pc
%{_libdir}/libwayland-*.so
%{_datadir}/aclocal/%{name}-scanner.m4
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}-scanner.mk
%{_datadir}/%{name}/%{name}.xml
%{_datadir}/%{name}/%{name}.dtd

%files -n libwayland-client
%defattr(-,root,root)
%license COPYING
%{_libdir}/libwayland-client.so.0*

%files -n libwayland-cursor
%defattr(-,root,root)
%license COPYING
%{_libdir}/libwayland-cursor.so.0*

%files -n libwayland-egl
%defattr(-,root,root)
%license COPYING
%{_libdir}/libwayland-egl.so.1*

%files -n libwayland-server
%defattr(-,root,root)
%license COPYING
%{_libdir}/libwayland-server.so.0*

%changelog
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.20.0-2
- Bump version as a part of libxslt upgrade
* Tue Jun 14 2022 Tejaswini Jayaramaiah <jtejaswini@vmware.com> 1.20.0-1
- Initial build. First version
