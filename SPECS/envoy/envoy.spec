%global git_commit e95ef6bc43daeda16451ad4ef20979d8e07a5299

Summary:        C++ L7 proxy and communication bus
Name:           envoy
Version:        1.14.4
Release:        11%{?dist}
License:        Apache-2.0
URL:            https://github.com/lyft/envoy
Source0:        %{name}-v%{version}.tar.gz
%define sha1    envoy=227008aa97cd2b2fdad57b847f4ace62051b57f7
Patch0:         envoy1.14.4-CVE-2020-35471.patch
Patch1:         envoy-1.14-healthcheck-fix-grpc-inline-removal-crashes.patch
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:	bazel
BuildRequires:  backward-cpp
BuildRequires:  c-ares-devel >= 1.11.0
BuildRequires:  cmake
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  clang
BuildRequires:	go
BuildRequires:  gcovr
BuildRequires:  python3-gcovr
BuildRequires:  gcc
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
BuildRequires:  lightstep-tracer-cpp
BuildRequires:  nghttp2-devel
BuildRequires:  openssl-devel
BuildRequires:  protobuf-devel
BuildRequires:  rapidjson-devel
BuildRequires:  spdlog
BuildRequires:  tclap
BuildRequires:  which
BuildRequires:	ninja-build
BuildRequires:	curl
Requires:       c-ares >= 1.11.0
Requires:       gperftools
Requires:       http-parser
Requires:       libevent
Requires:       libstdc++
Requires:       lightstep-tracer-cpp
Requires:       nghttp2
Requires:       openssl
Requires:       protobuf

%description
Envoy is a L7 proxy and communication bus designed for large modern service oriented architectures.

%prep
%setup -q -c -n %{name}-v%{version}
pushd %{name}-%{version}
%patch0 -p1
%patch1 -p1
popd

%build
cd envoy-%{version}
echo -n "%{git_commit}" > SOURCE_VERSION
bazel build //source/exe:envoy-static
bazel shutdown

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
* Sat Sep 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.14.4-11
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.14.4-10
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.14.4-9
- Bump up version to compile with new go
*   Mon Jun 06 2022 Bo Gan <ganb@vmware.com> 1.14.4-8
-   Fix CVE-2022-29224
*   Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.14.4-7
-   Bump up version to compile with new go
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.14.4-6
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.14.4-5
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.14.4-4
-   Bump up version to compile with new go
*   Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 1.14.4-3
-   Bump up version to compile with new go
*   Fri Feb 19 2021 Harinadh Dommaraju <hdommaraju@vmware.com> 1.14.4-2
-   Fix CVE-2020-35471
*   Tue Sep 15 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 1.14.4-1
-   Update envoy to 1.14.4
-   Fix for CVE-2020-8663,CVE-2020-12063,CVE-2020-12065,CVE-2020-15104
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.13.1-4
-   Bump up version to compile with new go
*   Fri Jul 17 2020 Harinadh D <hdommaraju@vmware.com> 1.13.1-3
-   Fix CVE-2020-12064
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.13.1-2
-   Bump up version to compile with go 1.13.5-2
*   Fri Apr 10 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 1.13.1-1
-   Update envoy to 1.13.1
-   Fix for CVE-2020-8664,CVE-2020-8661,CVE-2020-8659,CVE-2019-18838,
-   CVE-2019-18836,CVE-2019-15226,CVE-2019-15225
*   Mon Mar 23 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 1.10.0-8
-   Cleanup bazel server after build
*   Mon Mar 23 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 1.10.0-7
-   Fix for CVE-2020-8660
*   Thu Jan 30 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 1.10.0-6
-   Fix for CVE-2019-18802
*   Mon Jan 20 2020 Harinadh Dommaraju <hdommaraju@vmware.com> 1.10.0-5
-   Fix for CVE-2019-18801
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.10.0-4
-   Bump up version to compile with new go
*   Fri Nov 22 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.10.0-3
-   Fix build failure due to non-existent tclap repo.
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.10.0-2
-   Bump up version to compile with new go
*   Tue May 07 2019 Harinadh Dommaraju <hdommaraju@vmware.c0m> 1.10.0-1
-   Upgraded package from 1.2.0 to 1.10.0 to fix CVE-2019-9901
*   Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.2.0-1
-   Initial version of envoy package for Photon.
