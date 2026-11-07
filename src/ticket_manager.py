import csv
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ALERT_FILE = BASE_DIR / "alerts" / "security_alerts.csv"
TICKET_FILE = BASE_DIR / "reports" / "incident_tickets.csv"

PRIORITIES = {
    "CRITICAL": "P1 - Immediate",
    "HIGH": "P2 - High",
    "MEDIUM": "P3 - Moderate",
    "LOW": "P4 - Low",
}


def create_incident_tickets():
    if not ALERT_FILE.exists():
        print("No security alerts found.")
        return

    with ALERT_FILE.open("r", newline="") as file:
        alerts = list(csv.DictReader(file))

    if not alerts:
        print("No incidents require tickets.")
        return

    TICKET_FILE.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "ticket_id",
        "created_at",
        "source_ip",
        "attack_type",
        "severity",
        "priority",
        "status",
    ]

    with TICKET_FILE.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for number, alert in enumerate(alerts, start=1):
            severity = alert["severity"].upper()

            writer.writerow({
                "ticket_id": f"INC-{number:04d}",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "source_ip": alert["source_ip"],
                "attack_type": alert["attack_type"],
                "severity": severity,
                "priority": PRIORITIES.get(severity, "P4 - Low"),
                "status": "OPEN",
            })

    print(f"Created {len(alerts)} incident ticket(s).")
    print(f"Tickets saved to: {TICKET_FILE}")


if __name__ == "__main__":
    create_incident_tickets()
