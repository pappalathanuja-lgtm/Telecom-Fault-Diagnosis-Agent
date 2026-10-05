"""Smoke workflows for Streamlit navigation, simulation and replay pages."""
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"

class StreamlitWorkflowTests(unittest.TestCase):
    def test_all_pages_load_and_fault_can_be_replayed(self):
        app = AppTest.from_file(str(APP)).run(timeout=90)
        self.assertEqual(len(app.exception), 0, [item.message for item in app.exception])
        pages = ["NETWORK NOC", "FAULT DIAGNOSIS", "FAULT SIMULATION", "WHAT-IF SIMULATION", "SIMULATED REAL-TIME", "AI EXPLANATION", "ANALYTICS", "ACADEMIC SUBJECTS", "TRACEABILITY MATRIX", "VIVA MODE", "SYSTEM LOGS", "ABOUT PROJECT"]
        for page in pages:
            with self.subTest(page=page):
                app.sidebar.radio[0].set_value(page).run(timeout=90)
                self.assertEqual(len(app.exception), 0, [item.message for item in app.exception])
                if page == "SIMULATED REAL-TIME":
                    next(button for button in app.button if button.label == "Start Simulation").click().run(timeout=90)
                    self.assertEqual(len(app.exception), 0, [item.message for item in app.exception])
                    next(button for button in app.button if button.label == "Refresh / Generate Next Sample").click().run(timeout=90)
                    next(button for button in app.button if button.label == "Stop Simulation").click().run(timeout=90)
                if page == "WHAT-IF SIMULATION":
                    next(button for button in app.button if button.label == "RUN WHAT-IF ANALYSIS").click().run(timeout=90)
                    self.assertEqual(len(app.exception), 0, [item.message for item in app.exception])
        app.sidebar.radio[0].set_value("FAULT SIMULATION").run(timeout=90)
        next(widget for widget in app.multiselect if widget.label == "Fault conditions to inject simultaneously").set_value(["Fiber Link Failure", "Signal Degradation", "Network Congestion"]).run(timeout=90)
        next(button for button in app.button if button.label == "INJECT FAULT & DIAGNOSE").click().run(timeout=90)
        self.assertEqual(len(app.exception), 0, [item.message for item in app.exception])
        app.sidebar.radio[0].set_value("SYSTEM LOGS").run(timeout=90)
        self.assertTrue(any("INC-" in expander.label for expander in app.expander))
        next(button for button in app.button if button.label == "Replay Incident").click().run(timeout=90)
        self.assertEqual(len(app.exception), 0, [item.message for item in app.exception])

    def test_analytics_empty_state_generates_real_demo_incidents(self):
        app = AppTest.from_file(str(APP)).run(timeout=90)
        app.sidebar.radio[0].set_value("ANALYTICS").run(timeout=90)
        next(button for button in app.button if button.label == "Generate demo incident dataset").click().run(timeout=120)
        self.assertEqual(len(app.exception), 0, [item.message for item in app.exception])
        self.assertFalse(any("No simulated incidents" in item.value for item in app.info))

if __name__ == "__main__":
    unittest.main()
