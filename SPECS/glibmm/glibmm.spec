Summary:    C++ interface to the glib
Name:       glibmm
Version:    2.56.0
Release:    2%{?dist}
License:    LGPLv2+
URL:        http://ftp.gnome.org/pub/GNOME/sources/glibmm
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://ftp.gnome.org/pub/GNOME/sources/glibmm/2.53/%{name}-%{version}.tar.xz
%define sha512 glibmm=65e577009019e30e340ae5fe6e4c854e5a75551b2eb83ad85403d73eb4e77879783162d4c3c354bc37be0be842f0ddffc1977021a5e0c32985fb596d86929c08
BuildRequires:  python2 >= 2.7
BuildRequires:  libsigc++ >= 2.10.0
BuildRequires:  glib-devel glib-schemas
%if %{with_check}
BuildRequires: glib-networking
%endif

Requires:   libsigc++ >= 2.10.0
Requires:   glib >= 2.50.0
Requires:   gobject-introspection >= 1.50.0
Requires:   XML-Parser

%description
gtkmm provides a C++ interface to the GTK+ GUI library. gtkmm2 wraps GTK+ 2.
Highlights include typesafe callbacks, widgets extensible via inheritance and
a comprehensive set of widget classes that can be freely combined to quickly create complex user interfaces.

%package devel
Summary: Header files for glibmm
Group: Applications/System
Requires: %{name} = %{version}
Requires:   glib-devel libsigc++
%description devel
These are the header files of glibmm.

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
#need read content from /etc/fstab, which couldn't be empty
echo '#test' > /etc/fstab
export GIO_EXTRA_MODULES=/usr/lib/gio/modules; make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/glibmm-2.4/proc/*
%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/glibmm-2.4/include/*
%{_libdir}/giomm-2.4/include/*
%{_includedir}/*
%{_datadir}/*

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.56.0-2
- Remove .la files
* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 2.56.0-1
- Update to version 2.56.0
* Thu Aug 24 2017 Rongrong Qiu <rqiu@vmware.com> 2.50.1-2
- add buildrequires for make check for bug 1900286
* Fri May 26 2017 Harish Udaiya Kumar <hudaiykumar@vmware.com> 2.50.1-1
- Downgrade to stable version 2.50.1
* Mon Apr 10 2017 Danut Moraru <dmoraru@vmware.com> 2.53.1-1
- Update to version 2.53.1
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 2.48.1-2
- Modified %check
* Tue Sep 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.48.1-1
- Updated to version 2.48.1-1
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.47.3.1-2
- GA - Bump release of all rpms
* Thu Apr 14 2016   Harish Udaiya Kumar<hudaiyakumar@vmware.com> 2.47.3.1-1
- Updated to version 2.47.3.1
* Mon Feb 22 2016 XIaolin Li <xiaolinl@vmware.com> 2.46.3-1
- Updated to version 2.46.3
* Tue Jul 7 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-3
- Created devel subpackage. Added Summary.
* Tue Jun 23 2015 Alexey Makhalov <amakhalov@vmware.com> 2.42.0-2
- Added glib-schemas to build requirements.
* Wed Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.42.0-1
- Initial version
