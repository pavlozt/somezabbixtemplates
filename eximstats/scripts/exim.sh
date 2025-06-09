#!/bin/bash
# Zabbix Exim script.
#
# Settings
EXIMLOG=/var/log/exim4/mainlog
EXIMSTATS=/usr/sbin/eximstats
LOGTAIL=/usr/sbin/logtail2
ZABBIX_SENDER=/usr/bin/zabbix_sender
ZABBIX_CONF=/etc/zabbix/zabbix_agent2.conf

set -e

convert_to_bytes() {
    local value=$1
    local clean_value=${value// /}
    clean_value=${clean_value^^}

    if [[ $clean_value =~ ^([0-9]+)([A-Z]*)$ ]]; then
        local num=${BASH_REMATCH[1]}
        local suffix=${BASH_REMATCH[2]}

        case $suffix in
            ""|"B")    multiplier=1 ;;
            "KB")      multiplier=1024 ;;
            "MB")      multiplier=$((1024*1024)) ;;
            "GB")      multiplier=$((1024*1024*1024)) ;;
            "TB")      multiplier=$((1024*1024*1024*1024)) ;;
            *)
                echo "unknown suffix '$suffix'" >&2
                return 1
                ;;
        esac

        echo $((num * multiplier))
    else
        # Bad format? return 0
        return 0
    fi
}



REPORTFILE=$(mktemp)
# auto delete temp file:
trap 'rm -f "$REPORTFILE"' EXIT

"$LOGTAIL" "$EXIMLOG" | "$EXIMSTATS" -emptyok > "$REPORTFILE"

exit_codes=("${PIPESTATUS[@]}")  # save exit codes


if [ "${exit_codes[0]}" -eq 0 ]; then

  received=$(grep -m 1 Received "$REPORTFILE" | awk '{print $3}')
  delivered=$(grep -m 1 Delivered "$REPORTFILE" | awk '{print $3}')
  rejects=$(grep -m 1 Rejects "$REPORTFILE" | awk '{print $2}')
  bytes_received_txt=$(grep -m 1 "Received" "$REPORTFILE" | awk '{print $2}')
  bytes_delivered_txt=$(grep -m 1 "Delivered" "$REPORTFILE" | awk '{print $2}')
  remote_delivered=$(grep -m 1 "remote_smtp" "$REPORTFILE" | awk '{print $3}')
  remote_bytes_delivered_txt=$(grep -m 1 "remote_smtp" "$REPORTFILE" | awk '{print $2}')

  bytes_received=$(convert_to_bytes "$bytes_received_txt")
  bytes_delivered=$(convert_to_bytes "$bytes_delivered_txt")
  remote_bytes_delivered=$(convert_to_bytes "$remote_bytes_delivered_txt")

  # Send data to Zabbix
  "$ZABBIX_SENDER" -c "$ZABBIX_CONF" -i <(
    for var in received delivered rejects bytes_received bytes_delivered remote_delivered remote_bytes_delivered; do
      printf '%s\n' "- exim.$var ${!var:-0}"
    done
  ) > /dev/null 2>&1

fi
# exim queue will work regardless of other possible errors (logtail2, eximstats)
queue=$(/usr/sbin/exim -bpc)
"$ZABBIX_SENDER" -c "$ZABBIX_CONF" -k exim.queue -o "$queue" > /dev/null 2>&1