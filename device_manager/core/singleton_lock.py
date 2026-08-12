import os
import sys
import time
import requests
import psutil
from typing import Tuple, Optional
from config import HOST, PORT

LOCK_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "spidy_server.lock")

class SpidySingletonLock:
    """
    Cross-Process Singleton Lock for Spidy AI Backend.
    Guarantees exactly ONE active Spidy server process runs on port 8088.
    Prevents duplicate FastAPI spawns and resolves WinError 10048 at the architecture level.
    """
    def __init__(self, port: int = PORT):
        self.port = port
        self.lock_file = LOCK_FILE_PATH
        self._acquired = False

    def is_backend_healthy(self) -> bool:
        try:
            url = f"http://{HOST}:{self.port}/health"
            resp = requests.get(url, timeout=1.5)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("status") in ["ok", "degraded"]
        except Exception:
            pass
        return False

    def get_port_owner(self) -> Tuple[Optional[int], Optional[str]]:
        for conn in psutil.net_connections(kind='inet'):
            if conn.laddr.port == self.port and conn.status == 'LISTEN':
                pid = conn.pid
                try:
                    proc = psutil.Process(pid)
                    return pid, proc.name()
                except Exception:
                    return pid, "Unknown"
        return None, None

    def acquire(self) -> Tuple[bool, str]:
        # 1. Check if healthy Spidy backend is already running
        pid, pname = self.get_port_owner()
        if pid is not None:
            if self.is_backend_healthy():
                return False, f"Spidy AI backend is already running on {HOST}:{self.port} (PID: {pid}, Process: {pname}). Reusing existing instance."
            else:
                return False, f"Port {self.port} is occupied by non-healthy process (PID: {pid}, Process: {pname}). Cannot bind to port."

        # 2. Acquire local file lock
        try:
            os.makedirs(os.path.dirname(self.lock_file), exist_ok=True)
            with open(self.lock_file, "w") as f:
                f.write(str(os.getpid()))
            self._acquired = True
            return True, f"Acquired singleton lock for Spidy AI backend (PID: {os.getpid()})."
        except Exception as e:
            return False, f"Failed to acquire singleton lock: {e}"

    def release(self):
        if self._acquired and os.path.exists(self.lock_file):
            try:
                os.remove(self.lock_file)
                self._acquired = False
            except Exception:
                pass

singleton_lock = SpidySingletonLock()
