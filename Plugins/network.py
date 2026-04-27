"""
🔌 Network Plugin v2 - Comprehensive Network Diagnostics
WiFi, IP, DNS, Speedtest, Port Scanner
"""
import subprocess
import socket
import json
import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import requests
from core.engine import engine
from rich.table import Table
from rich.console import Console
import threading
import time

console = Console()

def register():
    """Plugin registration"""
    return {
        'name': 'network',
        'description': 'Network diagnostics & monitoring',
        'version': '2.0.0',
        'commands': {
            'ip': get_ip_info,
            'wifi': wifi_status,
            'ping': ping_host,
            'dns': dns_info,
            'ports': scan_ports,
            'speed': speed_test,
            'connections': active_connections,
            'route': routing_table
        },
        'entities': ['ip', 'host', 'port', 'dns']
    }

def get_ip_info(host: Optional[str] = None) -> Dict[str, Any]:
    """Complete IP configuration"""
    result = {}
    
    # Local IP addresses
    try:
        ip_result = engine.run("ip addr show | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1")
        if ip_result['success']:
            result['local_ips'] = ip_result['output'].split('\n')
    except:
        result['local_ips'] = []
    
    # Public IP
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text.strip()
        result['public_ip'] = public_ip
    except:
        result['public_ip'] = 'Unknown'
    
    # Hostname
    try:
        hostname = socket.gethostname()
        result['hostname'] = hostname
        result['fqdn'] = socket.getfqdn()
    except:
        result['hostname'] = 'Unknown'
    
    # Network interfaces
    interfaces = engine.run("ip link show | grep 'state UP' | awk '{print $2}'")
    result['active_interfaces'] = interfaces['output'].split('\n') if interfaces['success'] else []
    
    return result

def wifi_status() -> Dict[str, Any]:
    """WiFi connection details"""
    wifi_info = {}
    
    # Termux WiFi (Android)
    try:
        # Check WiFi status
        status = engine.run("termux-wifi-connectioninfo")
        if status['success'] and status['output']:
            wifi_info = json.loads(status['output'])
        else:
            # Fallback
            wifi_info['ssid'] = 'Unknown'
            wifi_info['strength'] = 'Unknown'
    except:
        wifi_info = {'status': 'Not available'}
    
    # Signal strength fallback
    iw_result = engine.run("iwconfig 2>/dev/null | grep -E 'ESSID|Signal'")
    if iw_result['success']:
        wifi_info['raw_iwconfig'] = iw_result['output']
    
    return wifi_info

def ping_host(host: str = "8.8.8.8", count: int = 4) -> Dict[str, Any]:
    """Ping with statistics"""
    cmd = f"ping -c {count} {host}"
    result = engine.run(cmd)
    
    stats = {}
    if result['success']:
        # Parse ping output
        lines = result['output'].split('\n')
        for line in lines:
            if 'packet loss' in line:
                match = re.search(r'(\d+)% packet loss', line)
                if match:
                    stats['packet_loss'] = int(match.group(1))
            if 'rtt' in line:
                match = re.search(r'rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)', line)
                if match:
                    stats.update({
                        'rtt_min': float(match.group(1)),
                        'rtt_avg': float(match.group(2)),
                        'rtt_max': float(match.group(3)),
                        'rtt_mdev': float(match.group(4))
                    })
    
    stats['target'] = host
    stats['reachable'] = stats.get('packet_loss', 100) < 100
    return stats

def dns_info(domain: str = "google.com") -> Dict[str, Any]:
    """DNS resolution + records"""
    dns_result = {}
    
    # A Record
    cmd = f"nslookup {domain} 2>/dev/null | grep 'Address:'"
    result = engine.run(cmd)
    if result['success']:
        dns_result['A'] = [line.strip().split()[-1] for line in result['output'].split('\n') if 'Address:' in line]
    
    # Nameservers
    ns_cmd = f"cat /etc/resolv.conf | grep nameserver"
    ns_result = engine.run(ns_cmd)
    if ns_result['success']:
        dns_result['nameservers'] = ns_result['output'].strip().split('\n')
    
    return dns_result

def scan_ports(host: str = "localhost", ports: str = "22,80,443,8080") -> Dict[str, Any]:
    """Basic port scanner"""
    port_list = ports.split(',')
    open_ports = []
    
    def check_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, int(port)))
        sock.close()
        return result == 0
    
    # Threaded scan
    threads = []
    for port in port_list:
        t = threading.Thread(target=lambda p=port: open_ports.append((p, check_port(p))))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    return {
        'host': host,
        'ports_scanned': len(port_list),
        'open_ports': [p for p, open in open_ports if open],
        'scan_time': time.time()  # Placeholder
    }

def speed_test() -> Dict[str, Any]:
    """Internet speed test"""
    try:
        # Speedtest CLI fallback
        result = engine.run("speedtest-cli --simple 2>/dev/null || echo 'speedtest not available'")
        return {'raw': result['output']}
    except:
        return {'status': 'Speedtest CLI not installed', 'install': 'pkg install speedtest-cli'}

def active_connections() -> Dict[str, Any]:
    """Active network connections"""
    result = engine.run("ss -tuln | head -20")
    if result['success']:
        connections = []
        for line in result['output'].split('\n')[1:]:
            if line.strip():
                parts = line.split()
                connections.append({
                    'proto': parts[0] if len(parts) > 0 else '',
                    'local': parts[3] if len(parts) > 3 else '',
                    'remote': parts[4] if len(parts) > 4 else ''
                })
        return {'connections': connections}
    return {}

def routing_table() -> Dict[str, Any]:
    """IP routing table"""
    result = engine.run("ip route show | head -15")
    if result['success']:
        routes = []
        for line in result['output'].split('\n'):
            if line.strip():
                routes.append(line.strip())
        return {'routes': routes}
    return {}

def show_network_table(info: Dict):
    """Rich network status table"""
    table = Table(title="🌐 Network Status")
    table.add_column("Interface", style="cyan")
    table.add_column("IP", style="green")
    table.add_column("Status", justify="right")
    
    # Example data formatting
    if 'local_ips' in info:
        for ip in info['local_ips'][:3]:
            table.add_row("eth0/wlan0", ip.strip(), "UP")
    
    console.print(table)

# Auto-register plugin
network_plugin = register()