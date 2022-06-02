%global security_hardening nopie
%define debug_package %{nil}
%define __os_install_post %{nil}
Summary:        EdgeX Foundry Go Services
Name:           edgex
Version:        1.2.1
Release:        14%{?dist}
License:        Apache-2.0
URL:            https://github.com/edgexfoundry/edgex-go
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:	edgex-%{version}.tar.gz
%define sha512  edgex=7b97edbbad6c4786d70d7adc232d1d3b3ba20e14c23cfdc03beda2713a602454b9677ee24e481150a9a6abb95478e5ade56ab0a7ac1f4ae716b5e7cbbd556921
Source1:	edgex-template.service

BuildRequires:  go
BuildRequires:  make
BuildRequires:  systemd-devel
BuildRequires:  zeromq-devel
Requires:       systemd
Requires:       zeromq
Requires:       redis

%description
EdgeX Foundry Go Services:
- core-command
- core-data
- core-metadata
- export-client
- export-distro
- support-logging
- support-notifications
- support-scheduler
- sys-mgmt-agent

%prep
%autosetup -p1 -c -T -a 0 -n src/github.com/edgexfoundry
mv %{_builddir}/src/github.com/edgexfoundry/edgex-go-%{version} %{_builddir}/src/github.com/edgexfoundry/edgex-go

%build
cd %{_builddir}/src/github.com/edgexfoundry/edgex-go

go mod tidy
export GO111MODULE=auto

# Disable consul [Registry] section for all services
find cmd -name configuration.toml | xargs sed -i "/^\[Registry\]/,+3 s/^/#/"

make build %{?_smp_mflags}

%install
# edgex-go
cd %{_builddir}/src/github.com/edgexfoundry/edgex-go

install -d -m755 %{buildroot}%{_bindir}
install -d -m755 %{buildroot}%{_datadir}/%{name}
install -d -m755 %{buildroot}%{_var}/log/%{name}
install -d -m755 %{buildroot}%{_libdir}/systemd/system

# install binary
for srv in core-command core-data core-metadata security-proxy-setup security-secrets-setup security-secretstore-read security-secretstore-setup support-logging support-notifications support-scheduler sys-mgmt-agent ; do
install -p -m755 cmd/${srv}/${srv} %{buildroot}%{_bindir}/edgex-${srv}
install -d -m755 %{buildroot}%{_datadir}/%{name}/${srv}/res
install -p -m644 cmd/${srv}/res/configuration.toml %{buildroot}%{_datadir}/%{name}/${srv}/res/configuration.toml
sed "s/SERVICE_NAME/${srv}/" %{SOURCE1} > %{buildroot}%{_libdir}/systemd/system/edgex-${srv}.service
done
install -p -m755 cmd/security-file-token-provider/security-file-token-provider %{buildroot}%{_bindir}/edgex-security-file-token-provider
sed "s/SERVICE_NAME/security-file-token-provider/" %{SOURCE1} > %{buildroot}%{_libdir}/systemd/system/edgex-security-file-token-provider.service
install -p -m755 cmd/sys-mgmt-executor/sys-mgmt-executor %{buildroot}%{_bindir}/edgex-sys-mgmt-executor
sed "s/SERVICE_NAME/sys-mgmt-executor/" %{SOURCE1} > %{buildroot}%{_libdir}/systemd/system/edgex-sys-mgmt-executor.service

# core data does not stop on SIGINT, so use SIGKILL instead.
# It allows `systemctl stop edgex-core-data` to work properly.
sed -i "s/SIGINT/SIGKILL/" %{buildroot}%{_libdir}/systemd/system/edgex-core-data.service

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*
%{_libdir}/*
%{_var}/log/*

%changelog
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.1-14
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.1-13
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.1-12
-   Bump up version to compile with new go
*   Thu Oct 28 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.1-11
-   Bump up version to compile with new go
*   Tue Oct 26 2021 Nitesh Kumar <kunitesh@vmware.com> 1.2.1-10
-   Bump up to consume redis v6.0.16.
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.1-9
-   Bump up version to compile with new go
*   Wed Aug 18 2021 Shreyas B<shreyasb@vmware.com> 1.2.1-8
-   Bump up to consume redis v6.0.15
*   Mon Jun 21 2021 Shreyas B<shreyasb@vmware.com> 1.2.1-7
-   Bump up version to consume redis v6.0.14
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.1-6
-   Bump up version to compile with new go
*   Tue May 25 2021 Shreyas B<shreyasb@vmware.com> 1.2.1-5
-   Bump up version to consume redis v6.0.13
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.1-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.2.1-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.1-2
-   Bump up version to compile with new go
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.1-1
-   Automatic Version Bump
*   Mon Feb 04 2019 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-2
-   Remove consul dependency.
-   Use SIGKILL for core-data to terminate the service.
*   Wed Jan 16 2019 Alexey Makhalov <amakhalov@vmware.com> 0.7.1-1
-   Version update. Use redis db.
*   Wed Dec 05 2018 Alexey Makhalov <amakhalov@vmware.com> 0.6.0-2
-   Remove 'Requires: mongodb'. But edgex still depends on mongo.
*   Fri Jul 06 2018 Alexey Makhalov <amakhalov@vmware.com> 0.6.0-1
-   Initial version
