#!/usr/bin/env python3
import json
import re
import subprocess
import time

def run_docker_cmd(cmd):
    """Execute command in docker container (without -it flag)"""
    full_cmd = ["sudo", "docker", "exec", "amnezia-awg2"] + cmd
    return subprocess.check_output(full_cmd, text=True)

def load_clients_table():
    """Load client names from /opt/amnezia/awg/clientsTable"""
    raw = run_docker_cmd(["cat", "/opt/amnezia/awg/clientsTable"])
    clients_data = json.loads(raw)

    # Create mapping: publicKey -> userData
    clients_map = {}
    for client in clients_data:
        public_key = client.get("clientId")
        user_data = client.get("userData", {})
        if public_key:
            clients_map[public_key] = user_data

    return clients_map

def parse_bytes(value):
    """Convert '1.83 KiB' to bytes"""
    if not value or value in ("0", ""):
        return 0

    value = str(value).strip()
    units = {
        "B": 1,
        "KiB": 1024,
        "MiB": 1024 ** 2,
        "GiB": 1024 ** 3,
        "TiB": 1024 ** 4,
    }

    match = re.match(r"([\d.]+)\s*([A-Za-z]+)", value)
    if not match:
        return 0

    num = float(match.group(1))
    unit = match.group(2)
    multiplier = units.get(unit, 1)
    return int(num * multiplier)

def parse_relative_time(value):
    """Convert '1 minute, 22 seconds ago' to Unix timestamp"""
    if not value or value in ("0", "Never", ""):
        return None

    now = int(time.time())
    total = 0

    # Parse all time components (d, h, m, s)
    for num, unit in re.findall(r"(\d+)\s*([dhms])", str(value)):
        num = int(num)
        if unit == "d":
            total += num * 86400
        elif unit == "h":
            total += num * 3600
        elif unit == "m":
            total += num * 60
        elif unit == "s":
            total += num

    if total > 0:
        return now - total

    return None

def parse_transfer(transfer_str):
    """Parse '47.36 GiB received, 31.70 GiB sent' -> (rx_bytes, tx_bytes, rx_str, tx_str)"""
    received = 0
    received_str = ""
    sent = 0
    sent_str = ""

    if not transfer_str:
        return received, sent, received_str, sent_str

    match_rx = re.search(r"([\d.]+\s*[A-Za-z]+)\s+received", transfer_str)
    if match_rx:
        received_str = match_rx.group(1).strip()
        received = parse_bytes(received_str)

    match_tx = re.search(r"([\d.]+\s*[A-Za-z]+)\s+sent", transfer_str)
    if match_tx:
        sent_str = match_tx.group(1).strip()
        sent = parse_bytes(sent_str)

    return received, sent, received_str, sent_str

def parse_wg_show():
    """Parse 'wg show' output"""
    raw = run_docker_cmd(["wg", "show"])

    interfaces = {}
    current_interface = None
    current_peer = None
    peer_counter = 0

    lines = raw.split('\n')

    for line in lines:
        line = line.rstrip()

        # Interface line (no leading spaces)
        if line.startswith("interface:"):
            current_interface = line.split(":", 1)[1].strip()
            interfaces[current_interface] = {
                "publicKey": None,
                "listenPort": None,
                "peers": []
            }
            current_peer = None
            peer_counter = 0
            continue

        # Peer line (no leading spaces)
        if line.startswith("peer:"):
            public_key = line.split(":", 1)[1].strip()
            peer_counter += 1
            current_peer = {
                "publicKey": public_key,
                "peerNo": str(peer_counter),
                "endpoint": None,
                "latestHandshakeStr": None,
                "latestHandshake": None,
                "transferRx": 0,
                "transferTx": 0,
                "dataReceived": None,
                "dataSent": None,
                "persistentKeepalive": None,
                "peerName": None,
                "allowedIps": []
            }
            interfaces[current_interface]["peers"].append(current_peer)
            continue

        # Skip empty lines and non-indented lines
        if not line or not line.startswith("  "):
            continue

        # Parse indented fields
        line = line.lstrip()

        if current_peer is None:
            # Interface-level fields
            if line.startswith("public key:"):
                key = line.split(":", 1)[1].strip()
                if key != "(hidden)":
                    interfaces[current_interface]["publicKey"] = key

            elif line.startswith("listening port:"):
                try:
                    interfaces[current_interface]["listenPort"] = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass

        else:
            # Peer-level fields
            if line.startswith("endpoint:"):
                current_peer["endpoint"] = line.split(":", 1)[1].strip()

            elif line.startswith("allowed ips:"):
                ips_str = line.split(":", 1)[1].strip()
                ips = [ip.strip() for ip in ips_str.split(",")]
                current_peer["allowedIps"] = ips

            elif line.startswith("latest handshake:"):
                hs_str = line.split(":", 1)[1].strip()
                if hs_str and hs_str != "Never":
                    current_peer["latestHandshakeStr"] = hs_str
                    current_peer["latestHandshake"] = parse_relative_time(hs_str)

            elif line.startswith("transfer:"):
                transfer_str = line.split(":", 1)[1].strip()
                rx, tx, rx_str, tx_str = parse_transfer(transfer_str)
                current_peer["transferRx"] = rx
                current_peer["transferTx"] = tx
                current_peer["dataReceived"] = rx_str if rx_str else None
                current_peer["dataSent"] = tx_str if tx_str else None

            elif line.startswith("persistent keepalive:"):
                try:
                    current_peer["persistentKeepalive"] = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass

    return interfaces

def enrich_peers_with_client_data(interfaces, clients_map):
    """Add client names from clientsTable to peers"""
    for interface_name, interface_data in interfaces.items():
        for peer in interface_data.get("peers", []):
            public_key = peer.get("publicKey")
            if public_key in clients_map:
                user_data = clients_map[public_key]
                peer["peerName"] = user_data.get("clientName")

    return interfaces

def main():
    # Load client information from clientsTable
    clients_map = load_clients_table()

    # Parse wg show output
    interfaces = parse_wg_show()

    # Enrich with client names
    interfaces = enrich_peers_with_client_data(interfaces, clients_map)

    # Output final JSON
    print(json.dumps(interfaces, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()