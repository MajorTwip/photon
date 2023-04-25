---
title: Using Network Event Broker
weight: 18
---

`network-event-broker` is a daemon that configures network and executes scripts on network events such as `systemd-networkd`'s DBus events, `dhclient` lease gains, and so on. 

`network-event-broker` also detects the following events:

- An IP address is added/removed/modified
- A link is added or removed


In the `/etc/network-event-broker` directory, `network-event-broker` creates the link state directories such as `carrier.d`, `configured.d`, `degraded.d`, `no-carrier.d`, `routable.d` and manager state directory such as `manager.d` . You can also keep the executable scripts in these directories.

## Use Case: Running command when a new address is acquired via DHCP. ##


1. `systemd-networkd`: `systemd-networkd`'s scripts are executed when the daemon receives the relevant event from `systemd-networkd`. 


		May 14 17:08:13 Zeus cat[273185]: OperationalState="routable"  
		May 14 17:08:13 Zeus cat[273185]: LINK=ens33


2. `dhclient`: For `dhclient`, scripts are executed in the `routable.d` directory when `dhclient` modifies the `/var/lib/dhclient/dhclient.leases` file and lease information is passed to the scripts as environmental arguments.

Environment variables such as `LINK`, `LINKINDEX=` and DHCP lease information `DHCP_LEASE=` are passed to the scripts. 


## Configuration ##

To manage the `network-event-broker` configuration, use the configuration file named `network-broker.toml` located in the following directory: `/etc/network-broker/` 


### [System] section ###
You can set values for the following keys in the `[System]` section:



`LogLevel=`  
Specifies the log level. The key takes one of the following values: `info`, `warn`, `error`, `debug` and `fatal`. Default is `info`.


`Generator=`  
Specifies the network event generator source. The key takes one of the following values: `systemd-networkd` or `dhclient`. Default is `systemd-networkd`.


### [Network] section
You can set values for the following keys in the `[Network]` section:

`Links=`  
A whitespace-separated list of links whose events should be monitored. No default value is set for this key.

`RoutingPolicyRules=`  
A whitespace-separated list of links for which you want to configure the routing policy rules per address. When you set this configuration, `network-event-broker` automatically adds the `to` and  `from` routing policy rules in another routing table `(ROUTE_TABLE_BASE = 9999 + ifindex)`. When these addresses are removed, the routing policy rules are dropped. No default value is set for this key.

`UseDNS=`  
Specifies whether you want to send the DNS server details to `systemd-resolved`. The key takes one of the following values: `true`, `false`. When set to `true`, the DNS server details are sent to `systemd-resolved` via DBus. This is applicable only to the DHClient. Default is false.


`UseDomain=`  
Specifies whether you want to send the DNS domain details to `systemd-resolved`. The key takes one of the following values: `true`, `false`. When set to `true`, the DNS domain details are sent to `systemd-resolved` via DBus. This is applicable only to the DHClient. Default is false.


`UseHostname=`  
Specifies whether you want to send the host name to `systemd-hostnamed`. The key takes one of the following values: `true`, `false`. When set to `true`, the host name is sent to `systemd-hostnamed` via DBus. This is applicable only to the DHClient. Default is false.

<<<<<<< HEAD:content/en/docs-v5/administration-guide/managing-network-configuration/using-network-event-broker.md
<<<<<<< HEAD:content/en/docs-v5/administration-guide/managing-network-configuration/using-network-event-broker.md
The following example shows a sample configuration of the key values in the `network-broker.toml` file:
=======
>>>>>>> 4944dd62b (New Topic added (Network Event)):content/en/docs/administration-guide/managing-network-configuration/using-network-event-broker.md
=======
The following example shows a sample configuration of the key values in the `network-broker.toml` file:
>>>>>>> 4740bd238 (Fixed comments from @ssahani):content/en/docs/administration-guide/managing-network-configuration/using-network-event-broker.md

	❯ sudo cat /etc/network-broker/network-broker.toml 
	[System]
	LogLevel="debug"
	Generator="dhclient"
	
	[Network]
	Links="ens33 ens37"
	RoutingPolicyRules="ens33 ens37"
	UseDNS="true"
	UseDomain="true"
<<<<<<< HEAD:content/en/docs-v5/administration-guide/managing-network-configuration/using-network-event-broker.md
<<<<<<< HEAD:content/en/docs-v5/administration-guide/managing-network-configuration/using-network-event-broker.md
=======

<br />

	❯ systemctl status network-broker.service
	● network-broker.service - A daemon configures network upon events
	     Loaded: loaded (/usr/lib/systemd/system/network-broker.service; disabled; vendor preset: disabled)
	     Active: active (running) since Thu 2021-06-03 22:22:38 CEST; 3h 13min ago
	       Docs: man:networkd-broker.conf(5)
	   Main PID: 572392 (network-broker)
	      Tasks: 7 (limit: 9287)
	     Memory: 6.2M
	        CPU: 319ms
	     CGroup: /system.slice/network-broker.service
	             └─572392 /usr/bin/network-broker

	Jun 04 01:36:04 Zeus network-broker[572392]: [info] 2021/06/04 01:36:04 Link='ens33' 	ifindex='2' changed state 'OperationalState'="carrier"
	Jun 04 01:36:04 Zeus network-broker[572392]: [info] 2021/06/04 01:36:04 Link='' ifindex='1' changed state 'OperationalState'="carrier"


`systemd-networkd` generates DBus signals as shown in the following sample:
	
	&{:1.683 /org/freedesktop/network1/link/_32 org.freedesktop.DBus.Properties.PropertiesChanged [org.freedesktop.network1.Link map[AdministrativeState:"configured"] []] 10}

<br />

	‣ Type=signal  Endian=l  Flags=1  Version=1 Cookie=24  Timestamp="Sun 2021-05-16 08:06:05.905781 UTC"
 	  Sender=:1.292  Path=/org/freedesktop/network1  Interface=org.freedesktop.DBus.Properties  Member=PropertiesChanged
 	  UniqueName=:1.292
 	  MESSAGE "sa{sv}as" {
 	          STRING "org.freedesktop.network1.Manager";
 	          ARRAY "{sv}" {
 	                  DICT_ENTRY "sv" {
 	                          STRING "OperationalState";
 	                          VARIANT "s" {
  	                                 STRING "degraded";
 	                          };
 	                  };
 	          };
 	          ARRAY "s" {
 	          };
 	  };


>>>>>>> 4944dd62b (New Topic added (Network Event)):content/en/docs/administration-guide/managing-network-configuration/using-network-event-broker.md
=======
>>>>>>> ceb7fbbd9 (Update using-network-event-broker.md):content/en/docs/administration-guide/managing-network-configuration/using-network-event-broker.md
