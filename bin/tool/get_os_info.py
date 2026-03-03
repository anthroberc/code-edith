import platform
import os
import sys

def get_os_info():
    return (
        f"OS: {platform.system()} {platform.release()} ({platform.version()}) | "
        f"Machine: {platform.machine()} | "
        f"CPU Cores: {os.cpu_count()} | "
        f"Python: {sys.version.split()[0]} | "
        f"Executable: {sys.executable}"
    )