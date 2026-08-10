import time
import platform
import psutil
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

START_TIME = time.time()

class SystemStats(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    battery_percent: Optional[float] = None
    battery_charging: Optional[bool] = None
    volume: Optional[int] = None
    network_connected: bool = True
    processes: int
    uptime_sec: float

def get_system_telemetry() -> SystemStats:
    # CPU & Memory
    cpu_pct = psutil.cpu_percent(interval=None)
    mem_pct = psutil.virtual_memory().percent
    
    # Disk
    disk_pct = psutil.disk_usage('/').percent

    # Battery
    battery_pct = None
    battery_charging = None
    try:
        battery = psutil.sensors_battery()
        if battery:
            battery_pct = round(battery.percent, 1)
            battery_charging = battery.power_plugged
    except Exception:
        pass

    # Network status
    net_connected = False
    try:
        stats = psutil.net_if_stats()
        for name, stat in stats.items():
            if stat.isup and not name.startswith(('Loopback', 'lo')):
                net_connected = True
                break
    except Exception:
        net_connected = True

    # Process count & Uptime
    procs = len(psutil.pids())
    uptime = round(time.time() - START_TIME, 1)

    return SystemStats(
        cpu_percent=cpu_pct,
        memory_percent=mem_pct,
        disk_percent=disk_pct,
        battery_percent=battery_pct,
        battery_charging=battery_charging,
        volume=50, # default telemetry volume estimate
        network_connected=net_connected,
        processes=procs,
        uptime_sec=uptime
    )
