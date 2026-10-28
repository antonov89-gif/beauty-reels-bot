import copy
import json
import sys
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / "scripts"))
from validate_channel_project import validate

P = json.loads((BASE / "examples" / "sample-project.json").read_text(encoding="utf-8"))

class TestValidation(unittest.TestCase):
    def test_example(self): self.assertEqual(validate(P), [])
    def test_no_invented_brand_approval(self):
        q = copy.deepcopy(P); q["brand"]["status"] = "APPROVED"
        self.assertTrue(any("approval_evidence" in e for e in validate(q)))
    def test_competitor_not_brand_source(self):
        q = copy.deepcopy(P); q["brand"]["source_ids"] = ["REF01"]
        self.assertTrue(any("must be OWN" in e for e in validate(q)))
    def test_own_not_competitor_reference(self):
        q = copy.deepcopy(P); q["competitor"]["reference_ids"] = ["OWN01"]
        self.assertTrue(any("must be COMPETITOR" in e for e in validate(q)))
    def test_no_fake_video_generated(self):
        q = copy.deepcopy(P); q["pilot"]["status"] = "GENERATED"
        self.assertTrue(any("actual_media_path" in e for e in validate(q)))
    def test_no_fake_inspection(self):
        q = copy.deepcopy(P); q["pilot"]["status"] = "INSPECTED"; q["pilot"]["actual_media_path"] = "not-real.mp4"
        self.assertTrue(any("inspected_evidence" in e for e in validate(q)))
    def test_no_fake_qc(self):
        q = copy.deepcopy(P); q["pilot"]["status"] = "QC_PASSED"; q["pilot"]["actual_media_path"] = "not-real.mp4"
        q["pilot"]["inspected_evidence"] = ["t=00:02 inspected"]
        self.assertTrue(any("BRAND_FIT" in e for e in validate(q)))
    def test_missing_cost_approval(self):
        q = copy.deepcopy(P); q["cost_approval"]["approved"] = True
        self.assertTrue(any("approval" in e for e in validate(q)))
    def test_duration(self):
        q = copy.deepcopy(P); q["pilot"]["duration_s"] = 40
        self.assertTrue(any("duration_s differs" in e for e in validate(q)))
    def test_explicit_valid_approval(self):
        q = copy.deepcopy(P); q["brand"]["status"] = "APPROVED"; q["brand"]["approval_evidence"] = "user approved this specific draft"
        self.assertEqual(validate(q), [])

if __name__ == "__main__": unittest.main()
