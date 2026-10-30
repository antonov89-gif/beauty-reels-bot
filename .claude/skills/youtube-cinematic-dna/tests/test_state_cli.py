import json
import subprocess
import tempfile
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
class StateCLITests(unittest.TestCase):
    def test_init_update_resume(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'state.json'
            patch=Path(td)/'patch.json'
            cmd=['python',str(BASE/'scripts'/'state_cli.py')]
            self.assertEqual(subprocess.run(cmd+['init',str(p)],capture_output=True).returncode,0)
            patch.write_text(json.dumps({'active_stage':'PILOT_SPEC','next_action':'verify estimated budget','reference':{'url':'https://youtu.be/X','access_level':'L1','coverage':[]}}))
            self.assertEqual(subprocess.run(cmd+['update',str(p),str(patch)],capture_output=True).returncode,0)
            output=subprocess.run(cmd+['next',str(p)],capture_output=True,text=True)
            self.assertIn('PILOT_SPEC',output.stdout)
            self.assertIn('verify estimated budget',output.stdout)
            loaded=json.loads(p.read_text())
            self.assertEqual(loaded['reference']['access_level'],'L1')
            self.assertFalse(loaded['cost_authorization']['approved'])
            self.assertEqual(subprocess.run(cmd+['init',str(p)],capture_output=True).returncode,1)

if __name__=='__main__': unittest.main()
