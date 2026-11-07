import csv
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import ticket_manager


class TestTicketManager(unittest.TestCase):

    def test_incident_ticket_creation(self):
        with TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            alert_file = temp_path / "security_alerts.csv"
            ticket_file = temp_path / "incident_tickets.csv"

            with alert_file.open("w", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["source_ip", "attack_type", "severity"]
                )
                writer.writeheader()
                writer.writerow({
                    "source_ip": "203.0.113.50",
                    "attack_type": "Brute Force",
                    "severity": "HIGH"
                })

            with patch.object(ticket_manager, "ALERT_FILE", alert_file), \
                 patch.object(ticket_manager, "TICKET_FILE", ticket_file):

                ticket_manager.create_incident_tickets()

            self.assertTrue(ticket_file.exists())

            with ticket_file.open("r", newline="") as file:
                tickets = list(csv.DictReader(file))

            self.assertEqual(len(tickets), 1)

            ticket = tickets[0]

            self.assertEqual(ticket["ticket_id"], "INC-0001")
            self.assertEqual(ticket["source_ip"], "203.0.113.50")
            self.assertEqual(ticket["severity"], "HIGH")
            self.assertEqual(ticket["priority"], "P2 - High")
            self.assertEqual(ticket["status"], "OPEN")


if __name__ == "__main__":
    unittest.main()