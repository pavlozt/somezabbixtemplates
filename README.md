# Some Zabbix templates

My original zabbix templates for different systems.

If you use these templates and have something to add — contributions are welcome.

- [LVM Cache](lvmcache/) - linux LVM cache commonly used to speed up disks
- [Firebird simple](firebird-simple/) - simple Firebird monitoring template
- [Exim Statistics](eximstats/) -  solution for parsing Exim logs and sending data to Zabbix
- [Monthly Traffic Accounting](monthly-traffic/) - monitors monthly traffic consumption. Also example of advanced trends calculation

## Templates in separate repositories

Additionally, some complex scripted templates are designed as separate repositories for easy import:

- [Postfix Stats](https://github.com/pavlozt/ansible-role-zabbixmon_postfix) - Ansible role for Postfix Statistics.


## Workarounds

  [Workarounds](workarounds/README.md) . Zabbix does not always work correctly. Here are some temporary solutions that allow you to bypass some errors.
