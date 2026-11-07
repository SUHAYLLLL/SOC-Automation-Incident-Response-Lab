import csv
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ALERT_FILE = BASE_DIR / "alerts" / "security_alerts.csv"
REPORT_FILE = BASE_DIR / "reports" / "incident_report.txt"


def generate_incident_report():
    if not ALERT_FILE.exists():
        print("No security alerts found.")
        return

    with ALERT_FILE.open("r", newline="") as file:
        alerts = list(csv.DictReader(file))

    if not alerts:
        print("No incidents to investigate.")
        return

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open("w") as report:
        report.write("SOC INCIDENT RESPONSE REPORT\n")
        report.write("=" * 40 + "\n")
        report.write(
            f"Generated: {datetime.now(timezone.utc).isoformat()}\n"
        )
        report.write(f"Total Incidents: {len(alerts)}\n\n")

        for number, alert in enumerate(alerts, start=1):
            severity = alert["severity"].upper()

            priority_levels = {
                "CRITICAL": "P1 - Immediate",
                "HIGH": "P2 - High",
                "MEDIUM": "P3 - Moderate",
                "LOW": "P4 - Low"
            }
            priority = priority_levels.get(severity, "P4 - Low")
            report.write(f"INCIDENT {number}\n")
            report.write("-" * 40 + "\n")
            report.write(f"Source IP: {alert['source_ip']}\n")
            report.write(f"Attack Type: {alert['attack_type']}\n")
            report.write(f"Severity: {alert['severity']}\n")
            report.write(f"Priority: {priority}\n")
            report.write(f"Failed Attempts: {alert['failed_attempts']}\n")
            report.write(f"Status: {alert['status']}\n\n")

            report.write("RECOMMENDED RESPONSE ACTIONS:\n")
            report.write("1. Investigate authentication logs.\n")
            report.write("2. Review activity from the suspicious IP.\n")
            report.write("3. Consider temporarily blocking the IP after verification.\n")
            report.write("4. Check affected accounts for compromise.\n")
            report.write("5. Escalate to a SOC analyst for review.\n\n")

    print(f"Incident response report generated: {REPORT_FILE}")


if __name__ == "__main__":
    generate_incident_report()