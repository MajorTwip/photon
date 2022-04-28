%global git_commit e95ef6bc43daeda16451ad4ef20979d8e07a5299

Summary:        C++ L7 proxy and communication bus
Name:           envoy
Version:        1.15.5
Release:        4%{?dist}
License:        Apache-2.0
URL:            https://github.com/lyft/envoy
Source0:        %{name}-v%{version}.tar.gz
%define sha1    envoy=16e1332d81e03eed6b88d147a990112a6cb6b760
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon


BuildRequires:  backward-cpp
BuildRequires:  c-ares-devel >= 1.11.0
BuildRequires:  cmake
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  clang
BuildRequires:  gcovr
BuildRequires:  python3
BuildRequires:  gcc
BuildRequires:  go >= 1.11
BuildRequires:  git
BuildRequires:  gmp
BuildRequires:  gmp-devel
BuildRequires:  gmock
BuildRequires:  gmock-devel
BuildRequires:  gmock-static
BuildRequires:  gtest
BuildRequires:  gtest-devel
BuildRequires:  gtest-static
BuildRequires:  gperftools-devel
BuildRequires:  http-parser-devel
BuildRequires:  libevent-devel
BuildRequires:  libstdc++-devel
BuildRequires:  lightstep-tracer-cpp-devel
BuildRequires:  nghttp2-devel
BuildRequires:  openssl-devel
BuildRequires:  protobuf3-devel
BuildRequires:  rapidjson-devel
BuildRequires:  spdlog
BuildRequires:  tclap
BuildRequires:  which
BuildRequires:  ninja-build
BuildRequires:  bazel
BuildRequires:  curl
Requires:       c-ares >= 1.11.0
Requires:       gperftools
Requires:       http-parser
Requires:       libevent
Requires:       libstdc++
Requires:       lightstep-tracer-cpp
Requires:       nghttp2
Requires:       openssl
Requires:       protobuf3

%description
Envoy is a L7 proxy and communication bus designed for large modern service oriented architectures.

%prep
%setup -q -c -n %{name}-v%{version}

%build
cd envoy-%{version}
echo -n "%{git_commit}" > SOURCE_VERSION
bazel build //source/exe:envoy-static
bazel  shutdown

%install
cd envoy-%{version}
mkdir -p %{buildroot}%{_sysconfdir}/envoy
mkdir -p %{buildroot}%{_bindir}
cp -pav bazel-bin/source/exe/envoy-static %{buildroot}/%{_bindir}/envoy
cp -rf configs/* %{buildroot}%{_sysconfdir}/envoy

%files
%defattr(-,root,root)
%{_bindir}/envoy
%config(noreplace) %{_sysconfdir}/envoy/*

%changelog
*   Wed Apr 27 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.15.5-4
-   Bump up release to build with c-ares updated
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.15.5-3
-   Bump up version to compile with new go
*   Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 1.15.5-2
-   Bump up version to compile with new go
*   Mon Jun 14 2021 Harinadh D <hdommaraju@vmware.com> 1.15.5-1
-   Fix CVE-2021-29492
*   Fri Feb 19 2021 Harinadh D <hdommaraju@vmware.com> 1.15.2-2
-   Fix CVE-2020-35471
*   Fri Oct 16 2020 Harinadh D <hdommaraju@vmware.com> 1.15.2-1
-   Fix CVE-2020-25018 and CVE-2020-25027
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.15.0-2
-   Bump up version to compile with new go
*   Fri Jul 17 2020 Harinadh D <hdommaraju@vmware.com> 1.15.0-1
-   Fix CVE-2020-12604
*   Fri Apr 24 2020 Harinadh D <hdommaraju@vmware.com> 1.13.1-2
-   Bump up version to compile with new go version
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.13.1-1
-   Update package to v1.13.1.
-   Fix for CVE-2020-8664,CVE-2020-8661,CVE-2020-8659,CVE-2019-18838,
-   CVE-2019-18836,CVE-2019-15226,CVE-2019-15225
*   Wed Apr 01 2020 Harinadh D <hdommaraju@vmware.com> 1.10.0-8
-   Cleanup bazel server after build
*   Fri Jan 31 2020 Harinadh D <hdommaraju@vmware.com> 1.10.0-7
-   Fix for CVE-2020-8660 and build errors
*   Fri Jan 31 2020 Harinadh D <hdommaraju@vmware.com> 1.10.0-6
-   Fix for CVE-2019-18801
*   Wed Jan 29 2020 Harinadh D <hdommaraju@vmware.com> 1.10.0-5
-   Fix for CVE-2019-18801
*   Fri Jan 03 2020 Ashwin H <ashwinh@vmware.com> 1.10.0-4
-   Bump up version to compile with new go
*   Fri Nov 22 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.10.0-3
-   Fix build failure due to non-existent tclap repo.
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.10.0-2
-   Bump up version to compile with new go
*   Mon Jun 03 2019 Harinadh Dommaraju <hdommaraju@vmware.c0m> 1.10.0-1
-   Upgraded envoy package from 1.2.0 to 1.10.0 to fix CVE-2019-9901 & CVE-2019-9900
*   Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2.0-1
-   Initial version of envoy package for Photon.
