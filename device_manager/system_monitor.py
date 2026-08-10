import psutil
import platform
import time
import os
from typing import Dict, Any

START_TIME = time.time()

def get_system_metrics() -> Dict[str, Any]:
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_freq = psutil.cpu_freq()
    freq_mhz = round(cpu_freq.current, 0) if cpu_freq else 0

    # Memory
    mem = psutil.virtual_memory()
    mem_total_gb = round(mem.total / (1024 ** 3), 2)
    mem_used_gb = round(mem.used / (1024 ** 3), 2)
    mem_percent = mem.percent

    # Disk
    disk = psutil.disk_usage('/')
    disk_total_gb = round(disk.total / (1024 ** 3), 2)
    disk_used_gb = round(disk.used / (1024 ** 3), 2)
    disk_percent = disk.percent

    # System Info
    uptime_sec = round(time.time() - START_TIME, 0)
    process_count = len(psutil.pids())

    return {
        "os": f"{platform.system()} {platform.release()}",
        "processor": platform.processor() or platform.machine(),
        "cpu": {
            "percent": cpu_percent,
            "cores": cpu_count,
            "freq_mhz": freq_mhz
        },
        "memory": {
            "total_gb": mem_total_gb,
            "used_gb": mem_used_gb,
            "percent": mem_percent
        },
        "disk": {
            "total_gb": disk_total_gb,
            "used_gb": disk_used_gb,
            "percent": disk_percent
        },
        "processes": process_count,
        "uptime_sec": uptime_sec
    }

if __name__ == "__main__":
    import json
    print(json.dumps(get_system_metrics(), indent=2))
