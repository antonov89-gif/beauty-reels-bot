import copy
import importlib.util
import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", BASE / "scripts" / "validate_project.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class ProjectValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads((BASE / "examples" / "sample-project.json").read_text(encoding="utf-8"))
    def test_empty_scaffold_passes(self):
        self.assertEqual(validator.validate(copy.deepcopy(self.base)), [])
    def test_observed_camera_must_have_real_av_evidence(self):
        obj = copy.deepcopy(self.base)
        obj["evidence"] = [{"id":"E1","source":"metadata","modality":"metadata","method":"read webpage","observation":"title","confirmed":True,"source_type":"reference"}]
        obj["claims"] = [{"id":"C1","status":"OBSERVED","claim_type":"camera","evidence_ids":["E1"]}]
        self.assertTrue(any("camera claim" in issue for issue in validator.validate(obj)))
    def test_approved_shot_without_artifact_fails(self):
        obj = copy.deepcopy(self.base)
        obj["shots"][0]["status"] = "APPROVED"
        self.assertTrue(validator.validate(obj))
    def test_paid_job_rejected_without_approval(self):
        obj = copy.deepcopy(self.base)
        obj["render_jobs"] = [{"id":"R1","paid":True,"status":"STARTED","provider":"provider","model":"model","resolution":"720p"}]
        self.assertTrue(any("paid render started" in issue for issue in validator.validate(obj)))
    def test_paid_job_approved_scope(self):
        obj = copy.deepcopy(self.base)
        obj["cost_authorization"] = {"approved": True,"approval_source":"user confirmed this batch","budget_cap":100,"provider":"P","model":"M","resolution":"720p"}
        obj["render_jobs"] = [{"id":"R1","paid":True,"status":"STARTED","provider":"P","model":"M","resolution":"720p"}]
        self.assertEqual(validator.validate(obj), [])
    def test_stage_cannot_claim_generated_without_artifacts(self):
        obj = copy.deepcopy(self.base)
        obj["active_stage"] = "PILOT_GENERATED"
        self.assertTrue(any("ledger has no verified artifact" in issue for issue in validator.validate(obj)))

if __name__ == "__main__":
    unittest.main()
