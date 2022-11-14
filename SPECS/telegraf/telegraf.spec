Summary:        agent for collecting, processing, aggregating, and writing metrics.
Name:           telegraf
Version:        1.10.0
Release:        15%{?dist}
License:        MIT
URL:            https://github.com/influxdata/telegraf
Source0:        https://github.com/influxdata/telegraf/archive/%{name}-%{version}.tar.gz
%define sha1    telegraf=e02d4c1319099f4111ab06a4fa6c4e47b8e70742
Source1:        https://github.com/wavefrontHQ/telegraf/archive/telegraf-plugin-1.4.0.zip
%define sha1    telegraf-plugin=51d2bedf6b7892dbe079e7dd948d60c31a2fc436
Source2:        https://raw.githubusercontent.com/wavefrontHQ/integrations/master/telegraf/telegraf.conf
Source3:       golang-dep-0.5.0.tar.gz
%define sha1 golang-dep-0.5.0=b8bb441fe3a4445e6cd4fa263dd2112e8566a734
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
BuildRequires:  systemd-devel
BuildRequires:  unzip
BuildRequires:  elfutils
Requires:       systemd
Requires:       logrotate
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

%description
Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics.

Design goals are to have a minimal memory footprint with a plugin system so that developers in
the community can easily add support for collecting metrics from well known services (like Hadoop,
Postgres, or Redis) and third party APIs (like Mailchimp, AWS CloudWatch, or Google Analytics).

%prep
%setup
mkdir -p ${GOPATH}/src/github.com/golang/dep
tar xf %{SOURCE3} --no-same-owner --strip-components 1 -C ${GOPATH}/src/github.com/golang/dep/
mkdir -p ${GOPATH}/src/github.com/influxdata/telegraf
tar xf %{SOURCE0} --no-same-owner --strip-components 1 -C ${GOPATH}/src/github.com/influxdata/telegraf
cat << EOF >>%{SOURCE2}
[[outputs.wavefront]]
host = "localhost"
port = 2878
metric_separator = "."
source_override = ["hostname", "snmp_host", "node_host"]
convert_paths = true
use_regex = false
EOF

pushd ..
unzip %{SOURCE1}
popd

%build
export GO111MODULE=off
pushd ${GOPATH}/src/github.com/golang/dep
CGO_ENABLED=0 GOOS=linux go build -v -ldflags "-s -w" -o ${GOPATH}/bin/dep ./cmd/dep/
popd
mkdir -p ${GOPATH}/src/github.com/wavefronthq/telegraf/plugins/outputs/wavefront
pushd ../telegraf-1.4.0
cp -r *  ${GOPATH}/src/github.com/wavefronthq/telegraf/
popd
pushd ${GOPATH}/src/github.com/influxdata/telegraf
sed -i '/import (/ a \\t_ "github.com/wavefronthq/telegraf/plugins/outputs/wavefront"' ${GOPATH}/src/github.com/influxdata/telegraf/plugins/outputs/all/all.go
sed -i 's/m.UnixNano()/m.Time().UnixNano()/g' ${GOPATH}/src/github.com/wavefronthq/telegraf/plugins/outputs/wavefront/wavefront.go
sed -i 's/github.com\/golang\/lint\/golint/golang.org\/x\/lint\/golint/g' ${GOPATH}/src/github.com/influxdata/telegraf/Makefile
make
popd

%install
install -m 755 -D ${GOPATH}/src/github.com/influxdata/telegraf/telegraf %{buildroot}%{_bindir}/telegraf
install -m 755 -D ${GOPATH}/src/github.com/influxdata/telegraf/scripts/telegraf.service %{buildroot}%{_unitdir}/telegraf.service
install -m 755 -D ${GOPATH}/src/github.com/influxdata/telegraf/etc/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 755 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}/telegraf.conf

%clean
rm -rf %{buildroot}/*

%pre
getent group telegraf >/dev/null || groupadd -r telegraf
getent passwd telegraf >/dev/null || useradd -c "Telegraf" -d %{_localstatedir}/lib/%{name} -g %{name} \
        -s /sbin/nologin -M -r %{name}

%post
chown -R telegraf:telegraf /etc/telegraf
%systemd_post %{name}.service
systemctl daemon-reload

%preun
%systemd_preun %{name}.service

%postun
if [ $1 -eq 0 ] ; then
    getent passwd telegraf >/dev/null && userdel telegraf
    getent group telegraf >/dev/null && groupdel telegraf
fi
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%{_bindir}/telegraf
%{_unitdir}/telegraf.service
%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/telegraf.conf

%changelog
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-15
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-14
- Bump up version to compile with new go
* Sat Sep 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-13
- Bump up version to compile with new go
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-12
- Bump up version to compile with new go
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-11
- Bump up version to compile with new go
*   Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-10
-   Bump up version to compile with new go
*   Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-9
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-8
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.10.0-7
-   Bump up version to compile with new go
*   Mon Oct 25 2021 Piyush Gupta <gpiyush@vmware.com> 1.10.0-6
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.10.0-5
-   Bump up version to compile with go 1.13.5-2
*   Tue Jan 07 2020 Ashwin H <ashwinh@vmware.com> 1.10.0-4
-   Bump up version to compile with new go
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.10.0-3
-   Bump up version to compile with new go
*   Fri Mar 29 2019 Keerthana K <keerthanak@vmware.com> 1.10.0-2
-   Fix conf file source number.
*   Thu Mar 14 2019 Keerthana K <keerthanak@vmware.com> 1.10.0-1
-   Update to 1.10.0 and its plugin version to 1.4.0.
*   Fri Apr 20 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.5.3-1
-   upgrade to 1.5.3
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
-   Remove shadow from requires and use explicit tools for post actions
*   Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
-   first version
