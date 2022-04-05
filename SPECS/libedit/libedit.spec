%define libedit_version 3.1
%define libedit_release 20180525

Summary:	The NetBSD Editline library
Name:		libedit
Version:	3.1.20180525
Release:	2%{?dist}
Vendor:		VMware, Inc.
Distribution:	Photon
License:	BSD
Url:		http://www.thrysoee.dk/editline
Group:		Applications/Libraries

Source0:	libedit-%{libedit_release}-%{libedit_version}.tar.gz
%define sha1 %{name}=cf6eb4f32c0336f0f3de68afbcdbeaa4d70b42b6

Requires:       ncurses

BuildRequires:  ncurses-devel

%description
Libedit is an autotool- and libtoolized port of the NetBSD
Editline library. It provides generic line editing, history, and
tokenization functions, similar to those found in GNU Readline.

%package        devel
Summary:        The NetBSD Editline library
Group:          Development/Libraries
Requires:       libedit = %{version}-%{release}

%description devel
Development files for libedit

%prep
%autosetup -p1 -n libedit-%{libedit_release}-%{libedit_version}

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
# Remove history.3, a solftlink to editline, which conflicts with readline-devel
rm -f %{buildroot}%{_mandir}/man3/history.3

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,0755)
%{_mandir}/*
%{_libdir}/%{name}.so.*
%exclude %dir %{_libdir}/debug

%files devel
%defattr(-,root,root,0755)
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_includedir}/*

%changelog
* Tue Oct 27 2020 Dweep Advani <dadvani@vmware.com> 3.1.20180525-2
- Fix conflict of /usr/share/man/man3/history.3 with readline-devel
* Tue Aug 14 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.20180525-1
- Initial
