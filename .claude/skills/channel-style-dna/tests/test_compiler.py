import copy
import json
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "scripts"))
from compile_shot_prompt import compile_shot
P = json.loads((BASE / "examples" / "sample-project.json").read_text(encoding="utf-8"))

class TestCompiler(unittest.TestCase):
    def test_inherits_brand_and_scene(self):
        s = compile_shot(P, "SH02")
        self.assertIn("GLOBAL BRAND CORE", s)
        self.assertIn("SCENE LOCK", s)
        self.assertIn("dark waxed jacket", s)
        self.assertIn("SHOT DELTA", s)
        self.assertIn("BRAND-NATIVE TRANSFER", s)
        self.assertIn("EVIDENCE WARNING", s)
    def test_missing_shot(self):
        with self.assertRaises(KeyError): compile_shot(P, "SH99")
    def test_rejects_unverified_approved_brand(self):
        q = copy.deepcopy(P); q["brand"]["status"] = "APPROVED"
        with self.assertRaises(ValueError): compile_shot(q, "SH01")
    def test_no_competitor_brand_override(self):
        s = compile_shot(P, "SH04")
        self.assertIn("do not borrow competitor branding", s)

if __name__ == "__main__": unittest.main()
