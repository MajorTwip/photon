%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.9.27
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.ansible.com
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
%define sha1 %{name}=eb84eda6ab4d66e7fdd77db514410cd30dc32264

Patch0: Add-Photon-OS-tdnf-support.patch

BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools

Requires: python2
Requires: python-jinja2
Requires: PyYAML
Requires: python-xml
Requires: paramiko

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
python2 setup.py build

%install
python2 setup.py install -O1 --skip-build --root "%{buildroot}"

%files
%defattr(-, root, root)
%{_bindir}/*
%{python2_sitelib}/*

%changelog
* Wed Oct 12 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.9.27-1
- Fix CVE-2021-20178.patch, CVE-2021-20180.patch, CVE-2021-20191.patch
* Mon Apr 20 2020 Shreenidhi Shedi <<sshedi@vmware.com> 2.7.16-2
- Fix CVE-2020-1733, CVE-2020-1739
* Fri Apr 03 2020 Shreenidhi Shedi <<sshedi@vmware.com> 2.7.16-1
- Upgrade to version 2.7.16 & various CVE fixes
* Thu Feb 06 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.7.9-3
- Fix for CVE-2019-14864
* Mon Aug 12 2019 Shreenidhi Shedi <sshedi@vmware.com> 2.7.9-2
- Fix for CVE-2019-10156
* Fri Apr 19 2019 Siju Maliakkal <smaliakkal@vmware.com> 2.7.9-1
- Upgrading to 2.7.9 to mitigate CVE-2019-3828
* Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0.0-1
- Version update to 2.4.0.0
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.2.0-2
- Use python2 explicitly
* Thu Apr 6 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.2.0-1
- Version update
* Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.1.0-1
- Initial build. First version
