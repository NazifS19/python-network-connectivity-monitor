#!/usr/bin/env python3

import csv
import json
import platform
import subprocess
from datetime import datetime
from pathlib import Path

DEVICE_FILE = Path("devices.json")
LOG_FILE = Path("logs/connectivity_log.csv")
PING_TIMEOUT_SECONDS = 2


def load_devices(file_path: Path) -> list[dict]:
    """Load and validate devices from a JSON file."""
    with file_path.open("r", encoding="utf-8") as file:
        devices = json.load(file)

    if not isinstance(devices, list):
        raise ValueError("devices.json must contain a list.")

    for device in devices:
        if "name" not in device or "address" not in device:
            raise ValueError("Each device needs 'name' and 'address'.")

    return devices


def build_ping_command(address: str) -> list[str]:
    """Build a one-packet ping command for the current operating system."""
    if platform.system().lower() == "windows":
        return ["ping", "-n", "1", address]

    return ["ping", "-c", "1", address]


def ping_device(address: str, timeout: int = PING_TIMEOUT_SECONDS) -> bool:
    """Return True when one ping succeeds; otherwise False."""
    try:
        result = subprocess.run(
            build_ping_command(address),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 1,
            check=False,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def check_device(device: dict) -> dict:
    """Ping one device and create a timestamped result."""
    reachable = ping_device(device["address"])

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "name": device["name"],
        "address": device["address"],
        "status": "ONLINE" if reachable else "OFFLINE",
    }


def log_result(result: dict, log_file: Path = LOG_FILE) -> None:
    """Append one result to the CSV log file."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_exists = log_file.exists()

    with log_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["timestamp", "name", "address", "status"],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(result)


def print_result(result: dict) -> None:
    """Print one device result."""
    print(
        f'{result["timestamp"]} | '
        f'{result["name"]:<20} | '
        f'{result["address"]:<15} | '
        f'{result["status"]}'
    )


def print_summary(results: list[dict]) -> None:
    """Print total, online, and offline counts."""
    online = sum(result["status"] == "ONLINE" for result in results)
    offline = len(results) - online

    print("\nSummary")
    print("-" * 30)
    print(f"Total devices : {len(results)}")
    print(f"Online        : {online}")
    print(f"Offline       : {offline}")


def main() -> None:
    print("Python Network Connectivity Monitor")
    print("=" * 45)

    try:
        devices = load_devices(DEVICE_FILE)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        print(f"Configuration error: {error}")
        return

    results = []

    for device in devices:
        result = check_device(device)
        results.append(result)
        log_result(result)
        print_result(result)

    print_summary(results)
    print(f"\nResults saved to: {LOG_FILE}")


if __name__ == "__main__":
    main()
