Summary:        Handle Common Gateway Interface requests and responses
Name:           perl-CGI
Version:        4.50
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        https://cpan.metacpan.org/authors/id/L/LE/LEEJO/CGI-%{version}.tar.gz
URL:            http://search.cpan.org/dist/CGI
%define sha512  CGI=c8f898404ef8fb341ea741229939748b82ca94b231591b67f29ca2f06cfbab363653753289a795a2eb0b0a145eafc8e8a303e92fd90795071b123e0fb8cb79c6
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  (coreutils or coreutils-selinux)
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  sed
Requires:       perl

%{?perl_default_filter}
# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((File::Spec)\\)$
# Remove false dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Fh)\\)
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(MultipartBuffer\\)$
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Fh\\)

%description
CGI.pm is a stable, complete and mature solution for processing and preparing
HTTP requests and responses. Major features including processing form
submissions, file uploads, reading and writing cookies, query string
generation and manipulation, and processing and preparing HTTP headers. Some
HTML generation utilities are included as well.

CGI.pm performs very well in in a vanilla CGI.pm environment and also comes
with built-in support for mod_perl and mod_perl2 as well as FastCGI.

%prep
%autosetup -p1 -n CGI-%{version}
iconv -f iso8859-1 -t utf-8 < Changes > Changes.1
mv Changes.1 Changes
sed -i 's?usr/bin perl?usr/bin/perl?' t/init.t
chmod -c -x examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%install
make pure_install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot} -type f -name .packlist -delete
%{_fixperms} %{buildroot}/*

%if 0%{?with_check}
%check
export PERL_MM_USE_DEFAULT=1
cpan local::lib
cpan Test::Deep
cpan HTML::Entities
cpan Test::Warn
cpan Test::NoWarnings
make %{?_smp_mflags} test
%endif

%files
%defattr(-,root,root)
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sat Apr 29 2023 Harinadh D <hdommaraju@vmware.com> 4.50-2
- Fix for requires
* Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 4.50-1
- Automatic Version Bump
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 4.40-1
- Update to version 4.40
* Mon Apr 3 2017 Robert Qi <qij@vmware.com> 4.35-1
- Upgraded to 4.35
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 4.26-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.26-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.26-1
- Updated to version 4.26
* Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 4.25-1
- Initial version.
