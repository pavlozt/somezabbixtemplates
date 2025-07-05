# Zabbix Template: Monthly Traffic Accounting

Monitors monthly traffic consumption on a single interface per host. Creates items via autodiscovery with triggers for traffic limit warnings.

## Requirements
- Standard Zabbix network interface templates applied to host (`Linux by Zabbix agent` or `Windows by Zabbix agent`)

## Configuration
1. **Import Template**:
   Import [zbx_template_monthly_traffic_7.0.yaml](zbx_template_monthly_traffic_7.0.yaml)) into Zabbix.

2. **Set Macros**:
   Configure these host-level macros:
   - `{$BW_MONTHLY_INTERFACE}`: Network interface name (e.g. `eth0`)
   - `{$BW_MONTHLY_LIMIT_MB_IN}`: Incoming traffic monthly limit in MB (default `102400` for `100GB`)
   - `{$BW_MONTHLY_LIMIT_MB_OUT}`: Outgoint traffic monthly limit in MB (default `102400` for `100GB`)

## Features

- **Autodiscovery**: Creates monthly counters for specified interface or choose `eth0` as default
- **Uses previously collected data**: That is, it will start working in the current month.

- **Optimal non-overloading calculation**:  Works fast because it calculates only by trends data. For the same reason, the information is updated rarely - once an hour.

- **Triggers**:
  - `Monthly limit reached for incoming traffic` when incoming traffic reaches limits
  - `Monthly limit reached for outgoing traffic` when outgoing traffic reaches limits


- **Items**:
  - Incoming traffic counter
  - Outgoing traffic counter

## Usage
Attach template to hosts with traffic-limited interfaces. Values reset automatically at monthly boundaries.