import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)

output_file = Path(__file__).resolve().parent.parent / "data" / "security_logs.csv"
output_file.parent.mkdir(parents=True, exist_ok=True)

users = ["admin", "james", "sarah", "michael", "emma"]
normal_ips = ["192.0.2.10", "192.0.2.20", "192.0.2.30"]
suspicious_ip = "203.0.113.50"

start_time = datetime(2026, 11, 7, 9, 0, tzinfo=timezone.utc)
events = []

# Normal authentication activity
for i in range(100):
    events.append({
        "timestamp": (start_time + timedelta(seconds=i * 30)).isoformat(),
        "source_ip": random.choice(normal_ips),
        "username": random.choice(users),
        "event_type": random.choices(
            ["LOGIN_SUCCESS", "LOGIN_FAILED"],
            weights=[85, 15]
        )[0]
    })

# Simulated brute-force attack
for i in range(20):
    events.append({
        "timestamp": (start_time + timedelta(minutes=10, seconds=i * 2)).isoformat(),
        "source_ip": suspicious_ip,
        "username": "admin",
        "event_type": "LOGIN_FAILED"
    })

events.sort(key=lambda event: event["timestamp"])

with output_file.open("w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["timestamp", "source_ip", "username", "event_type"]
    )
    writer.writeheader()
    writer.writerows(events)

print(f"Generated {len(events)} security events.")
print(f"Saved to {output_file}")