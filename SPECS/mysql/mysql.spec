Summary:        MySQL.
Name:           mysql
Version:        5.7.40
Release:        1%{?dist}
License:        GPLv2
Group:          Applications/Databases
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://www.mysql.com

Source0: https://cdn.mysql.com/Downloads/MySQL-5.7/mysql-boost-%{version}.tar.gz
%define sha1 mysql-boost=002410b8422b7eed1af330a678440fb5ffdfdcbe

BuildRequires:  cmake
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel

Requires: openssl
Requires: zlib
Requires: perl
Requires: ncurses-libs
Requires: libgcc-atomic
Requires: glibc

%description
MySQL is a free, widely used SQL engine. It can be used as a fast database as well as a rock-solid DBMS using a modular engine architecture.

%package devel
Summary:        Development headers for mysql
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for developing applications linking to maridb

%prep
%autosetup -p1 %{name}-boost-%{version}

%build
cmake . \
      -DCMAKE_INSTALL_PREFIX=%{_prefix}   \
      -DWITH_BOOST=boost/boost_1_59_0 \
      -DINSTALL_MANDIR=%{_mandir} \
      -DINSTALL_DOCDIR=%{_docdir} \
      -DINSTALL_DOCREADMEDIR=%{_docdir} \
      -DINSTALL_SUPPORTFILESDIR=share/support-files \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DWITH_EMBEDDED_SERVER=OFF

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
make test %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%doc LICENSE  README
%{_libdir}/plugin/*
%{_libdir}/libmysqlclient.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/support-files/*
%exclude %{_usr}/mysql-test
%exclude %{_usr}/docs
%exclude %{_datadir}

%files devel
%defattr(-,root,root)
%{_libdir}/libmysqlclient.so
%{_libdir}/*.a
%{_includedir}/*
%{_libdir}/pkgconfig/mysqlclient.pc

%changelog
* Mon Oct 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.7.40-1
- Upgrade to v5.7.40
* Wed May 04 2022 Nitesh Kumar <kunitesh@vmware.com> 5.7.38-1
- Upgrade version to 5.7.38 to fix bunch of CVE's
* Mon Jan 31 2022 Nitesh Kumar <kunitesh@vmware.com> 5.7.37-1
- Upgrade version to 5.7.37 to fix following CVE's:
- CVE-2022-21245, CVE-2022-21304, CVE-2022-21270,
- CVE-2022-21367, CVE-2022-21344 and CVE-2022-21303
* Mon Nov 08 2021 Tapas Kundu <tkundu@vmware.com> 5.7.36-1
- Update to 5.7.36
* Mon Aug 16 2021 Shreyas B <shreyasb@vmware.com> 5.7.35-1
- Upgrade to version 5.7.35
* Mon May 03 2021 Shreyas B <shreyasb@vmware.com> 5.7.34-1
- Upgrade to version 5.7.34
* Mon Feb 01 2021 Shreyas B <shreyasb@vmware.com> 5.7.33-1
- Upgrade to version 5.7.33
* Mon Nov 02 2020 Shreyas B <shreyasb@vmware.com> 5.7.32-1
- Upgrade to version 5.7.32
* Tue Jul 21 2020 Shreyas B <shreyasb@vmware.com> 5.7.31-1
- Upgrade to version 5.7.31
* Tue May 05 2020 Tapas Kundu <tkundu@vmware.com> 5.7.30-1
- Upgrade to version 5.7.30
* Fri Mar 13 2020 Tapas Kundu <tkundu@vmware.com> 5.7.29-1
- Upgrade to version 5.7.29
* Tue Aug 06 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.7.27-1
- Upgrade to version 5.7.27 to fix CVE-2019-2800, CVE-2019-2822 and more
* Tue May 07 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.7.26-1
- Update to version 5.7.26 to fix CVE-2019-2632 and more
* Thu Feb 14 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.7.25-1
- Update to version 5.7.25 to fix CVE-2019-2534, CVE-2018-3155
* Mon Jul 30 2018 Ajay Kaher <akaher@vmware.com> 5.7.23-1
- Update to version 5.7.23 to fix CVE-2018-3070, CVE-2018-3073,
- CVE-2018-3062, CVE-2018-3074, CVE-2018-3081, CVE-2018-3054,
- CVE-2018-3061, CVE-2018-3077, CVE-2018-3067, CVE-2018-3075,
- CVE-2018-3078, CVE-2018-3079, CVE-2018-3080, CVE-2018-3056,
- CVE-2018-3058, CVE-2018-3071, CVE-2018-3054, CVE-2018-3064,
- CVE-2018-3060, CVE-2018-3065
* Thu Apr 26 2018 Xiaolin Li <xiaolinl@vmware.com> 5.7.22-1
- Update to version 5.7.22 to fix CVE-2018-2755
* Tue Apr 17 2018 Xiaolin Li <xiaolinl@vmware.com> 5.7.21-1
- Update to version 5.7.21 to fix CVE-2018-2583, CVE-2018-2665,
- CVE-2018-2573, CVE-2018-2612, CVE-2018-2622, CVE-2018-2640
* Thu Jan 25 2018 Divya Thaluru <dthaluru@vmware.com> 5.7.20-2
- Added patch for CVE-2018-2696
* Wed Oct 25 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.20-1
- Update to version 5.7.20
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 5.7.18-3
- Fix typo in description
* Fri Jul 14 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.18-2
- Run make test in the %check section
* Tue Jun 13 2017 Xiaolin Li <xiaolinl@vmware.com> 5.7.18-1
- Initial packaging for Photon
