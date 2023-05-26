%global debug_package %{nil}
%define __os_install_post %{nil}

Summary:        Build software of any size, quickly and reliably, just as engineers do at Google.
Name:           bazel
Version:        6.1.2
Release:        1%{?dist}
License:        Apache License 2.0
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://bazel.build/
Source:         https://github.com/bazelbuild/bazel/releases/download/%{version}/%{name}-%{version}-dist.zip
%define sha512  bazel=3b84139d383f47607db92f3f59504b2e07409140ebfad7d540a81638619ba67eb870285c9b9c6db8dd50a8971ba871365d583bdf9754ff0038d5b6c39af9d013
BuildRequires:  openjdk11 zlib-devel which findutils tar gzip zip unzip
BuildRequires:  gcc
BuildRequires:  python3
Requires:       openjdk11

%description
Bazel is Google's own build tool, now publicly available in Beta. Bazel has
built-in support for building both client and server software, including client
applications for both Android and iOS platforms. It also provides an extensible
framework that you can use to develop your own build rules.

%prep
%autosetup -c

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
mkdir /usr/tmp
export TMPDIR=/usr/tmp
# some modules in bazel just expecting python to be exist
ln -sf %{_bindir}/python3 %{_bindir}/python
./compile.sh
pushd output
./bazel
popd

%install
mkdir -p %{buildroot}%{_bindir}
cp output/bazel %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/bazel

%changelog
* Tue May 23 2023 Harinadh Dommaraju <hdommaraju@vmware.com> 6.1.2-1
- Upgrade bazel version
* Fri Mar 11 2022 Harinadh Dommaraju <hdommaraju@vmware.com> 4.2.2-1
- Update bazel version
* Mon Sep 21 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 3.5.0-1
- Update bazel version
* Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 2.0.0-2
- Changed openjdk install directory name
* Fri Feb 7 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 2.0.0-1
- Initial release
