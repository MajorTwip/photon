Summary:        Replication Manager for PostgreSQL Clusters
Name:           repmgr
Version:        5.2.1
Release:        2%{?dist}
License:        GNU Public License (GPL) v3
URL:            https://repmgr.org/
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://repmgr.org/download/%{name}-%{version}.tar.gz
%define sha1    %{name}=2368a114934e78e5b316bed535b2794f4a3e81e9

BuildRequires: postgresql-devel
BuildRequires: readline-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: cpio

Requires: postgresql-libs
Requires: readline
Requires: openssl
Requires: zlib

%description
repmgr is an open-source tool suite for managing replication and failover in a cluster of PostgreSQL servers.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_libdir}/postgresql/*
%exclude %dir %{_libdir}/debug

%changelog
* Sat Mar 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.2.1-2
- Exclude debug symbols properly
* Thu Aug 26 2021 Sujay G <gsujay@vmware.com> 5.2.1-1
- Bump version to 5.2.1 as requested in PR#2824906
* Mon May 04 2020 Sujay G <gsujay@vmware.com> 5.1.0-1
- Bump to version 5.1.0
* Thu Apr 09 2020 Stanislav Paskalev <spaskalev@vmware.com> 5.0.0-1
- Initial build.  First version
