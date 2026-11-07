import csv
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "data" / "security_logs.csv"

THRESHOLD = 5
WINDOW_SECONDS = 60


def detect_brute_force():
    failed_logins = defaultdict(list)

    with LOG_FILE.open("r", newline="") as file:
        reader = csv.DictReader(file)

        for event in reader:
            if event["event_type"] == "LOGIN_FAILED":
                failed_logins[event["source_ip"]].append(
                    datetime.fromisoformat(event["timestamp"])
                )

    alerts = []

    for ip, timestamps in failed_logins.items():
        window = deque()

        for timestamp in sorted(timestamps):
            window.append(timestamp)

            while (
                window
                and (timestamp - window[0]).total_seconds() > WINDOW_SECONDS
            ):
                window.popleft()

            if len(window) >= THRESHOLD:
                alerts.append({
                    "source_ip": ip,
                    "failed_attempts": len(window),
                    "severity": "HIGH",
                    "attack_type": "Brute Force"
                })
                break

    return alerts


if __name__ == "__main__":
    alerts = detect_brute_force()

    print("SOC Threat Detection Results")
    print("----------------------------")

    if alerts:
        for alert in alerts:
            print(f"Suspicious IP: {alert['source_ip']}")
            print(f"Attack Type: {alert['attack_type']}")
            print(f"Failed Attempts: {alert['failed_attempts']}")
            print(f"Severity: {alert['severity']}")
    else:
        print("No suspicious activity detected.")