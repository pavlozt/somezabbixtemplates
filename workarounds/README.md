# Wrappers for smartctl

Unfortunately, the new smart zabbix agent2 plugin has several bugs that are slowly being fixed.
I suggest a simple workaround using wrapper scripts.

There are two fixes:
- [smartctl-ioctl](smartctl-ioctl/) for incorrect triggering during disk surface testing [ZBX-22770](https://support.zabbix.com/projects/ZBX/issues/ZBX-22770).   This solution requires installation оf **jq** program installed for transform json output.

- [smart-test](smartctl-test/) - fix polling with incorrect drivers leading to multiple kernel error messages [ZBX-25632](https://support.zabbix.com/browse/ZBX-25632)
  When using some drivers, the arguments are filtered and the program does not execute.
  Please note that arguments for calling scsi are also filtered.


And there is a combined both things wrapper script:
- [smartctl-combined](smartctl-combined/)


Among other things, you need to configure the agent (/etc/zabbix/zabbix_agent2.d/plugins.d):
```
Plugins.Smart.Path=/usr/local/sbin/smartctlwrapper
Plugins.Smart.Timeout = 20
```


Please remember that these scripts still require usual configuration of sudo.
