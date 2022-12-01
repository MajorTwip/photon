Summary:        X11 font utilities.
Name:           font-util
Version:        1.3.2
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/font/font-util-1.3.2.tar.bz2
%define sha512  font-util=7cac529b12ae71185b89c72c1569b9826f52eeaecc1c76010338e7c42c4078ae339f18220b580bbd68fb5dc09df6ecf169a47c32e6104d8ee53bd443fa21d167

%description
The Xorg font utilities.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/
%{_datadir}/*

%changelog
*   Thu Oct 20 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.2-1
-   Upgrade version to 1.3.2
*   Wed May 20 2015 Alexey Makhalov <amakhalov@vmware.com> 1.3.1-1
-   initial version
