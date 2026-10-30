import copy
import importlib.util
import json
import unittest
from pathlib import Path
BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pilot", BASE / "scripts" / "validate_pilot.py")
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)

class PilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan=json.loads((BASE / "examples" / "sample-pilot.json").read_text(encoding="utf-8"))
    def test_connected_timeline(self):
        self.assertEqual(pilot.check(self.plan), [])
    def test_gap_is_rejected(self):
        plan=copy.deepcopy(self.plan)
        plan["shots"][2]["start_sec"]+=1
        self.assertTrue(any("gap/overlap" in s for s in pilot.check(plan)))
    def test_missing_sound_rejected(self):
        plan=copy.deepcopy(self.plan)
        plan["shots"][3]["sound"]=""
        self.assertTrue(any("missing sound" in s for s in pilot.check(plan)))

if __name__ == "__main__": unittest.main()
