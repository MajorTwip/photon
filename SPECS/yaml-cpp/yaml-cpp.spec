Summary:        YAML parser and emitter in C++
Name:           yaml-cpp
Version:        0.7.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries/C and C++
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/jbeder/yaml-cpp/
Source0:        https://github.com/jbeder/yaml-cpp/archive/%{name}-%{version}.tar.gz
%define sha512 yaml-cpp=2de0f0ec8f003cd3c498d571cda7a796bf220517bad2dc02cba70c522dddde398f33cf1ad20da251adaacb2a07b77844111f297e99d45a7c46ebc01706bbafb5
BuildRequires:  cmake
BuildRequires:  gcc

%description
A YAML parser and emitter in C++ matching the YAML 1.2 spec.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries/C and C++
Requires: %{name} = %{version}-%{release}

%description devel
Development files for %{name} library.

%prep
%autosetup -n %{name}-%{name}-%{version} -p1

%build
%cmake \
    -DYAML_BUILD_SHARED_LIBS=ON \
    -DYAML_CPP_BUILD_TESTS=OFF \
    -DCMAKE_C_COMPILER=gcc \
    -DCMAKE_CXX_COMPILER=g++

make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc CONTRIBUTING.md README.md
%license LICENSE
%{_libdir}/libyaml-cpp.so.*

%files devel
%defattr(-, root, root)
%{_datadir}/pkgconfig/yaml-cpp.pc
%{_datadir}/cmake/%{name}/
%{_includedir}/yaml-cpp/
%{_libdir}/libyaml-cpp.so

%changelog
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.7.0-1
- yaml-cpp initial build