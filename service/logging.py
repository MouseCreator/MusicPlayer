import os
import platform
from typing import List

import psutil
from datetime import datetime

LOG_FILE = "user.log"

def _write(line: str):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def create_log():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== USER SYSTEM LOG ===\n")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = platform.platform()
    processor = platform.processor() or "Unknown"
    ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)

    _write(f"Timestamp: {timestamp}")
    _write(f"Operating System: {os_info}")
    _write(f"Processor: {processor}")
    _write(f"Total RAM: {ram_gb} GB")
    _write("=" * 40)


def _append_log(file_path: str):
    if not os.path.exists(file_path):
        _write(f"[ERROR] Tried to load non-existent file: {file_path}")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = os.path.basename(file_path)
    extension = os.path.splitext(file_name)[1].lower()
    size_mb = round(os.path.getsize(file_path) / (1024**2), 3)

    _write(f"File loaded: {file_name}")
    _write(f"Timestamp: {timestamp}")
    _write(f"Extension: {extension}")
    _write(f"Size: {size_mb} MB")
    _write("-" * 40)

def log_files(loaded: List[str]):
    if not loaded:
        return
    for s in loaded:
        _append_log(s)
