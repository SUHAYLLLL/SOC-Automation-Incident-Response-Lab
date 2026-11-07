import csv
import html
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TICKET_FILE = BASE_DIR / "reports" / "incident_tickets.csv"
DASHBOARD_FILE = BASE_DIR / "reports" / "soc_dashboard.html"


def generate_dashboard():
    if not TICKET_FILE.exists():
        print("No incident tickets found. Run SOC automation first.")
        return

    with TICKET_FILE.open("r", newline="", encoding="utf-8") as file:
        tickets = list(csv.DictReader(file))

    severity_counts = Counter(
        ticket["severity"].upper() for ticket in tickets
    )
    open_tickets = sum(
        ticket["status"].upper() == "OPEN" for ticket in tickets
    )

    rows = ""
    for ticket in tickets:
        cells = "".join(
            f"<td>{html.escape(ticket.get(field, ''))}</td>"
            for field in [
                "ticket_id", "source_ip", "attack_type",
                "severity", "priority", "status"
            ]
        )
        rows += f"<tr>{cells}</tr>"

    dashboard = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SOC Incident Dashboard</title>
<style>
body {{
    background: #0b1220;
    color: #e5e7eb;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 35px;
}}
h1 {{ color: #38bdf8; }}
.subtitle {{ color: #94a3b8; }}
.cards {{
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin: 30px 0;
}}
.card {{
    background: #1e293b;
    padding: 25px;
    border-radius: 12px;
    min-width: 160px;
    flex: 1;
}}
.card h2 {{
    font-size: 32px;
    margin: 10px 0;
}}
.card p {{ color: #94a3b8; }}
table {{
    width: 100%;
    border-collapse: collapse;
    background: #1e293b;
}}
th, td {{
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #334155;
}}
th {{ color: #38bdf8; }}
tr:hover {{ background: #334155; }}
</style>
</head>
<body>
<h1>SOC Security Operations Dashboard</h1>
<p class="subtitle">Automated Threat Detection & Incident Response</p>
<p class="subtitle">Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>

<div class="cards">
    <div class="card">
        <p>Total Incidents</p>
        <h2>{len(tickets)}</h2>
    </div>
    <div class="card">
        <p>Open Tickets</p>
        <h2>{open_tickets}</h2>
    </div>
    <div class="card">
        <p>High Severity</p>
        <h2>{severity_counts.get("HIGH", 0)}</h2>
    </div>
    <div class="card">
        <p>Critical Severity</p>
        <h2>{severity_counts.get("CRITICAL", 0)}</h2>
    </div>
</div>

<h2>Incident Ticket Overview</h2>
<table>
<thead>
<tr>
<th>Ticket ID</th>
<th>Source IP</th>
<th>Attack Type</th>
<th>Severity</th>
<th>Priority</th>
<th>Status</th>
</tr>
</thead>
<tbody>{rows}</tbody>
</table>
</body>
</html>"""

    DASHBOARD_FILE.parent.mkdir(parents=True, exist_ok=True)
    DASHBOARD_FILE.write_text(dashboard, encoding="utf-8")
    print(f"SOC dashboard generated: {DASHBOARD_FILE}")


if __name__ == "__main__":
    generate_dashboard()
