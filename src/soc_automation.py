import csv
from datetime import datetime, timezone
from pathlib import Path

from detect_threats import detect_brute_force
from incident_response import generate_incident_report
from ticket_manager import create_incident_tickets
from dashboard import generate_dashboard

BASE_DIR = Path(__file__).resolve().parent.parent
ALERT_FILE = BASE_DIR / "alerts" / "security_alerts.csv"


def main():
    print("SOC Automation & Incident Response Lab")
    print("--------------------------------------")
    print("Running automated threat detection...")

    alerts = detect_brute_force()

    if not alerts:
        print("No suspicious activity detected.")
        return

    ALERT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with ALERT_FILE.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "source_ip",
                "attack_type",
                "failed_attempts",
                "severity",
                "status"
            ]
        )
        writer.writeheader()

        for alert in alerts:
            writer.writerow({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source_ip": alert["source_ip"],
                "attack_type": alert["attack_type"],
                "failed_attempts": alert["failed_attempts"],
                "severity": alert["severity"],
                "status": "OPEN"
            })

            print(f"ALERT: {alert['attack_type']} detected!")
            print(f"Suspicious IP: {alert['source_ip']}")
            print(f"Severity: {alert['severity']}")

    print(f"\nSecurity alerts saved to: {ALERT_FILE}")
    print("\nStarting automated incident response...")
    generate_incident_report()

    print("\nCreating automated incident tickets...")
    create_incident_tickets()

    print("\nGenerating SOC security dashboard...")
    generate_dashboard()

    print("\nSOC automation workflow completed successfully.")


if __name__ == "__main__":
    main()