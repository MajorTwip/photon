Summary:        unbound dns server
Name:           unbound
Version:        1.16.2
Release:        1%{?dist}
Group:          System/Servers
Vendor:         VMware, Inc.
License:        BSD
Distribution:   Photon
URL:            http://www.unbound.net
Source0:        https://www.unbound.net/downloads/%{name}-%{version}.tar.gz
%define sha512  unbound=0ea65ea63265be677441bd2a28df12098ec5e86c3372240c2874f9bd13752b8b818da81ae6076cf02cbeba3d36e397698a4c2b50570be1a6a8e47f57a0251572
Source1:        %{name}.service
Requires:       systemd
BuildRequires:  systemd
BuildRequires:  expat-devel
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package    devel
Summary:    unbound development libs and headers
Group:      Development/Libraries
Requires:   expat-devel

%description devel
Development files for unbound dns server

%package    docs
Summary:    unbound docs
Group:      Documentation

%description docs
unbound dns server docs

%prep
%autosetup -p1

%build
%configure \
    --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \
    --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
install -vdm755 %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
make check %{?_smp_mflags}

%pre
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || \
useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin \
-c "Unbound DNS resolver" unbound

%post
    /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_sbindir}/*
%{_sysconfdir}/*
%{_unitdir}/%{name}.service

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files docs
%{_mandir}/*

%changelog
*  Wed Aug 17 2022 Srish Srinivasan <ssrish@vmware.com> 1.16.2-1
-  Update to 1.16.2 for fixing CVE-2022-30698 and CVE-2022-30699
*  Fri Jul 30 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.12.0-2
-  Fix openssl 3.0.0 beta2 compatibility with unbound
*  Fri Jul 23 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.12.0-1
-  Update to 1.12.0 for openssl 3.0 compatibility
*  Tue Feb 02 2021 Shreyas B. <shryasb@vmware.com> 1.11.0-2
-  Fix for CVE-2020-28935
*  Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 1.11.0-1
-  Automatic Version Bump
*  Sun May 24 2020 Shreyas B. <shryasb@vmware.com> 1.8.0-4
-  Fix for CVE-2020-12662 & CVE-2020-12663
*  Fri Dec 20 2019 Shreyas B. <shryasb@vmware.com> 1.8.0-3
-  Fix for vulnerability CVE-2019-18934 that can cause shell code
-  execution after receiving a specially crafted answer.
*  Mon Oct 14 2019 Shreyas B. <shryasb@vmware.com> 1.8.0-2
-  Fix for CVE-2019-16866.
*  Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 1.8.0-1
-  Update to version 1.8.0.
*  Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-3
-  Remove shadow from requires and use explicit tools for post actions
*  Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-2
-  Requires expat-devel
*  Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.6.1-1
-  Updated to version 1.6.1
*  Fri Jan 06 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-1
-  Initial
