import sys
import unittest
from pathlib import Path

# Allow the test to import files from the src folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from detect_threats import detect_brute_force


class TestThreatDetection(unittest.TestCase):

    def test_brute_force_detection(self):
        alerts = detect_brute_force()

        self.assertGreater(
            len(alerts), 0,
            "Expected at least one brute-force alert"
        )

        suspicious_ips = [alert["source_ip"] for alert in alerts]

        self.assertIn(
            "203.0.113.50",
            suspicious_ips,
            "Expected suspicious IP was not detected"
        )

    def test_normal_login_activity(self):
        from unittest.mock import patch
        from io import StringIO

        normal_logs = StringIO(
            "timestamp,source_ip,event_type\n"
            "2026-11-07T10:00:00,192.168.1.10,LOGIN_FAILED\n"
            "2026-11-07T10:00:10,192.168.1.10,LOGIN_FAILED\n"
            "2026-11-07T10:00:20,192.168.1.10,LOGIN_SUCCESS\n"
        )

        with patch("builtins.open"):
            with patch("pathlib.Path.open", return_value=normal_logs):
                alerts = detect_brute_force()

        self.assertEqual(
            len(alerts),
            0,
            "Normal login activity should not trigger an alert"
        )

if __name__ == "__main__":
    unittest.main()
