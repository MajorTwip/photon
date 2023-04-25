---
title:  Photon Packer Template
weight: 3
---

The Photon Packer template folder has the following structure:

```
photon-packer-templates/
.
├── README.md
├── packer-photon.json
├── scripts
│   ├── photon-kickstart.json
│   ├── photon-package_provisioning.sh
│   ├── photon-security_check.sh
│   ├── photon-sharedfolders_prep.sh
│   ├── photon-vagrant-user_provisioning.sh
│   ├── photon-vagrant-vbox_additions.sh
│   ├── photon-vagrantfile.rb
│   └── photon-virtualbox-load-module.conf
└── vars
    └── iso-4.0GA.json

2 directories, 11 files
```

## packer-photon.json

The following are the contents of the `photon-packer-templates/packer-photon.json` file:

```json
{
  "variables": {
    "iso_file": "",
    "iso_sha1sum": "",
    "product_version": "",
    "root_password": "changeme"
  },
  "builders": [
    {
      "name": "vagrant-vmware_desktop",
      "vm_name": "photon",
      "vmdk_name": "photon-disk1",
      "type": "vmware-iso",
      "headless": false,
      "disk_size": 20480,
      "disk_type_id": 0,
      "guest_os_type": "other3xlinux-64",
      "iso_url": "{{user `iso_file`}}",
      "iso_checksum": "{{user `iso_sha1sum`}}",
      "iso_checksum_type": "sha1",
      "ssh_username": "root",
      "ssh_password": "{{user `root_password`}}",
      "ssh_wait_timeout": "60m",
      "boot_wait": "5s",
      "shutdown_command": "shutdown -h now",
      "http_directory": "scripts",
      "version": 11,
      "vmx_data": {
        "scsi0.virtualDev": "pvscsi",
        "ethernet0.virtualDev": "vmxnet3"
        },
      "vmx_data_post": {
        "displayname": "VMware Photon",
        "usb.present": "false"
        },
        "boot_command": [
          "<esc><wait>",
          "vmlinuz initrd=initrd.img root=/dev/ram0 loglevel=3 ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/photon-kickstart.json photon.media=cdrom",
          "<enter>"
        ]
    },
    {
      "name": "vagrant-virtualbox",
      "vm_name": "photon",
      "type": "virtualbox-iso",
      "headless": false,
      "hard_drive_interface": "scsi",
      "disk_size": 20480,
      "guest_os_type": "Linux_64",
      "iso_url": "{{user `iso_file`}}",
      "iso_checksum": "{{user `iso_sha1sum`}}",
      "iso_checksum_type": "sha1",
      "ssh_username": "root",
      "ssh_password": "{{user `root_password`}}",
      "ssh_wait_timeout": "60m",
      "boot_wait": "5s",
      "http_directory": "scripts",
      "shutdown_command": "shutdown -h now",
      "boot_command": [
        "<esc><wait>",
        "vmlinuz initrd=initrd.img root=/dev/ram0 loglevel=3 ks=http://{{ .HTTPIP }}:{{ .HTTPPort }}/photon-kickstart.json",
        "<enter>"
      ]
    }
  ],
    "provisioners": [
    {
      "type": "shell",
      "script": "scripts/photon-package_provisioning.sh"
    },
    {
      "type": "shell",
      "only": ["vagrant-vmware_desktop", "vagrant-virtualbox"],
      "script": "scripts/photon-vagrant-user_provisioning.sh"
    },
    {
      "type": "shell",
      "only": ["vagrant-vmware_desktop"],
      "script": "scripts/photon-sharedfolders_prep.sh"
    },
    {
      "type": "shell",
      "only": ["vagrant-virtualbox"],
      "script": "scripts/photon-vagrant-vbox_additions.sh"
    },
    {
      "type": "file",
      "only": ["vagrant-virtualbox"],
      "source": "scripts/photon-virtualbox-load-module.conf",
      "destination": "/etc/modules-load.d/virtualbox.conf"
    },
    {
      "type": "shell",
      "inline": ["sed -i '/linux/ s/$/ net.ifnames=0/' /boot/grub2/grub.cfg"]
    },
    {
      "type": "shell",
      "inline": ["echo 'GRUB_CMDLINE_LINUX=\"net.ifnames=0\"' >> /etc/default/grub"]
    },
    {
      "type": "shell",
      "script": "scripts/photon-security_check.sh"
    },
    {
      "type": "shell",
      "inline": ["sed -i 's/OS/Linux/' /etc/photon-release"]
    }
  ],
  "post-processors": [
    {
      "type": "vagrant",
      "only": ["vagrant-vmware_desktop", "vagrant-virtualbox"],
      "compression_level": 9,
      "vagrantfile_template": "scripts/photon-vagrantfile.rb",
      "output": "photon-{{user `product_version`}}-{{.BuildName}}.box"
    }
  ]
  }
```

## photon-kickstart.json

The following are the contents of the `photon-packer-templates/scripts/photon-kickstart.json` file:

```json
{
    "hostname": "photon",
    "password":
        {
            "crypted": false,
            "text": "2RQrZ83i79N6szpvZNX6"
        },
    "disk": "/dev/sda",
    "packagelist_file": "packages_minimal.json",
    "postinstall": [
                    "#!/bin/sh",
                    "sed -i 's/PermitRootLogin no/PermitRootLogin yes/g' /etc/ssh/sshd_config",
                    "systemctl restart sshd.service"
                   ]
}
```

## iso-4.0GA.json

The following are the contents of the `photon-packer-templates/vars/iso-4.0GA.json` file:

```json
{
   "product_version" : "4.0GA",
   "iso_sha1sum" : "2221ab214b517a15c60bd5e2aacdb9388581bcd9",
   "iso_file" : "https://packages.vmware.com/photon/4.0/GA/iso/photon-4.0-1526e30ba.iso"
}
```

For more information about the template, see [Photon Packer Template](https://github.com/vmware/photon-packer-templates)
