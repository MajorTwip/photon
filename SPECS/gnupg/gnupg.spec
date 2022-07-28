Summary:	OpenPGP standard implementation used for encrypted communication and data storage.
Name:		gnupg
Version:	2.2.18
Release:	2%{?dist}
License:	GPLv3+
URL:		https://gnupg.org/index.html
Group:		Applications/Cryptography.
Source0:        https://gnupg.org/ftp/gcrypt/gnupg/%{name}-%{version}.tar.bz2
%define sha1 gnupg=2f95d6aa409f666c61c1526641fd609f1a50c4c4
Vendor:		VMware, Inc.
Distribution:	Photon
Patch0:         CVE-2022-34903.patch
BuildRequires:	zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  readline-devel
BuildRequires:  npth
BuildRequires:  npth-devel
BuildRequires:  libassuan
BuildRequires:  libksba >= 1.0.7
BuildRequires:  libgcrypt >= 1.7.0
BuildRequires:  libgcrypt-devel
BuildRequires:  libgpg-error >= 1.24
BuildRequires:  libassuan >= 2.5.0
Requires:       libksba
Requires:       libgcrypt >= 1.7.0
Requires:       npth
Requires:       libassuan >= 2.5.0
Requires:       pinentry
Provides:       gpg

%description
GnuPG is a complete and free implementation of the OpenPGP standard as defined
by RFC4880 (also known as PGP). GnuPG allows to encrypt and sign your data and
communication, features a versatile key management system as well as access
modules for all kinds of public key directories. GnuPG, also known as GPG, is
a command line tool with features for easy integration with other applications.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%configure --with-libusb=no

make
%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/locale/*/*/*
%{_mandir}/*
%{_infodir}/gnupg*
%{_libexecdir}/*
%{_datadir}/gnupg/*
%exclude %{_infodir}/dir
%exclude /usr/share/doc/*

%changelog
*   Tue Jul 19 2022 Shivani Agarwal <shivania2@vmware.com> 2.2.18-2
-   Fix CVE-2022-34903
*   Thu Apr 02 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 2.2.18-1
-   Upgrade to 2.2.18 to fix CVE-2019-14855
*   Tue Jul 16 2019 Ashwin H <ashwinh@vmware.com> 2.2.17-1
-   2.2.17 released to fix CVE-2019-13050
*   Thu Mar 28 2019 Ashwin H <ashwinh@vmware.com> 2.2.15-1
-   Update to 2.2.15 which has Fix for CVE-2018-1000858
*   Thu Jan 31 2019 Ashwin H <ashwinh@vmware.com> 2.1.20-4
-   Fix CVE-2018-12020
*   Wed Aug 30 2017 Alexey Makhalov <amakhalov@vmware.com> 2.1.20-3
-   Add requires libgcrypt
*   Wed Jun 07 2017 Danut Moraru <dmoraru@vmware.com> 2.1.20-2
-   Add pinentry dependency
*   Tue Apr 11 2017 Danut Moraru <dmoraru@vmware.com> 2.1.20-1
-   Update to 2.1.20
*   Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 2.0.30-1
-   Initial Build.
