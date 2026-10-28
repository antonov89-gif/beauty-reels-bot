import importlib.util
import sys
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "scripts" / "route_intent.py"
spec = importlib.util.spec_from_file_location("router", PATH)
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)

class RouterTests(unittest.TestCase):
    def test_bare_link_triggers_creative_autopilot(self):
        self.assertEqual(router.classify("https://youtu.be/abc123"), "ONE_LINK_STUDIO")
        self.assertEqual(router.classify("https://youtube.com/shorts/qwerty"), "ONE_LINK_STUDIO")
    def test_multiple_references(self):
        self.assertEqual(router.classify("https://youtu.be/A https://youtu.be/B"), "MULTI_REF")
    def test_explicit_analysis_wins(self):
        self.assertEqual(router.classify("https://youtu.be/A Разбери только монтаж"), "ANALYZE")
    def test_create(self):
        self.assertEqual(router.classify("https://youtu.be/A Сделай мне новый фильм"), "CREATE")
    def test_continue_and_repair(self):
        self.assertEqual(router.classify("Дальше"), "CONTINUE")
        self.assertEqual(router.classify("исправь зум на 0:12"), "REPAIR")
    def test_non_youtube_url(self):
        self.assertEqual(router.classify("https://example.com"), "UNSPECIFIED")

if __name__ == "__main__":
    unittest.main()
