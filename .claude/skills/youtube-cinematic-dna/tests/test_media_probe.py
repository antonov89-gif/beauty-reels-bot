import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'requires ffmpeg')
class MediaProbeTests(unittest.TestCase):
    def test_audio_extraction_and_no_stale_frames_on_reuse(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            source=root/'sample.mp4'
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                '-f','lavfi','-i','testsrc=size=128x72:rate=12',
                '-f','lavfi','-i','sine=frequency=440:sample_rate=16000',
                '-t','3','-c:v','mpeg4','-q:v','10','-c:a','aac',str(source)], check=True)
            target=root/'evidence'
            script=str(BASE/'scripts'/'inspect_media.py')
            base=['python',script,str(source),'--out',str(target)]
            first=subprocess.run(base+['--duration','2','--fps','4'],capture_output=True,text=True)
            self.assertEqual(first.returncode,0,first.stderr)
            m=json.loads((target/'manifest.json').read_text())
            self.assertEqual(m['frame_count'],8)
            self.assertTrue((target/'sample_audio.wav').stat().st_size>0)
            self.assertIsNotNone(m['audio_extracted'])
            second=subprocess.run(base+['--duration','1','--fps','2'],capture_output=True,text=True)
            self.assertNotEqual(second.returncode,0)
            third=subprocess.run(base+['--duration','1','--fps','2','--overwrite'],capture_output=True,text=True)
            self.assertEqual(third.returncode,0,third.stderr)
            m=json.loads((target/'manifest.json').read_text())
            self.assertEqual(m['frame_count'],2)
            self.assertEqual(len(list((target/'frames').glob('frame_*.jpg'))),2)

if __name__ == '__main__': unittest.main()
