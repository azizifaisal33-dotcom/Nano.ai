"""
🔌 System Plugin - Comprehensive monitoring
"""
import subprocess
import psutil
from typing import Dict
from core.engine import engine

def register():
    return {
        'name': 'system',
        'description': 'System monitoring & control',
        'commands': {
            'cpu': cpu_info,
            'ram': memory_info,
            'disk': disk_info,
            'processes': top_processes,
            'load': system_load
        }
    }

def cpu_info() -> Dict:
    """CPU usage + stats"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        return {
            'cpu_percent': cpu_percent,
            'cpu_count': cpu_count,
            'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
        }
    except:
        result = engine.run("top -bn1 | head -20")
        return {'raw': result['output']}

def memory_info() -> Dict:
    """Memory + swap"""
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        'total': f"{memory.total / (1024**3):.1f}GB",
        'used': f"{memory.used / (1024**3):.1f}GB", 
        'available': f"{memory.available / (1024**3):.1f}GB",
        'percent': memory.percent,
        'swap': f"{swap.percent}%"
    }

def disk_info() -> Dict:
    """Disk usage"""
    disks = {}
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disks[partition.device] = {
                'total': f"{usage.total / (1024**3):.1f}GB",
                'used': f"{usage.used / (1024**3):.1f}GB",
                'free': f"{usage.free / (1024**3):.1f}GB"
            }
        except:
            pass
    return disks

def top_processes(limit: int = 10) -> List[Dict]:
    """Top CPU processes"""
    processes = []
    for proc in sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                      key=lambda p: p.info['cpu_percent'], reverse=True)[:limit]:
        processes.append(proc.info)
    return processes

def system_load() -> Dict:
    """System load average"""
    with open('/proc/loadavg', 'r') as f:
        loadavg = f.read().split()[:3]
    return {
        '1min': loadavg[0],
        '5min': loadavg[1],
        '15min': loadavg[2]
    }