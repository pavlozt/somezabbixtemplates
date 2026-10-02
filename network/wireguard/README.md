# Ansible Roles for WireGuard Monitoring

This repository contains two Ansible roles designed to monitor WireGuard VPN implementations using Zabbix.
They cover both the classic WireGuard and AmneziaWG (AWG) variants.

- [pavlozt.awgmon](pavlozt.awgmon/) — Monitors AmneziaWG (AWG) peers via Zabbix.
- [pavlozt.wgclassicmon](pavlozt.wgclassicmon/) — Monitors classic WireGuard peers via Zabbix.

# Zabbix Templates

The Zabbix templates are stored inside each role’s `zabbix_templates` directory:

- [AmneziaWG (AWG) template](pavlozt.awgmon/zabbix_templates/awg_template.yaml)
- [Classic WireGuard template](pavlozt.wgclassicmon/zabbix_templates/wireguard_peers.yaml)

Import the appropriate template into your Zabbix frontend to start monitoring.