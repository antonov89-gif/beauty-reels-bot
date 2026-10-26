"""Storyboard frames for the liver Short (STYLE v2 + SB-v1 medical cyan). Run: python3 shots_liver.py [ids] (Nano Banana 2.1 via APIpod, $0.02 each at 1K)."""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
SB = ("SB-v1: clean medical 3D animation look on a flat bright cyan studio background with a faint light grid, soft even studio light, "
      "translucent frosted-glass human body with visible organs, the liver is glossy reddish-brown with a soft inner glow; "
      "no blood, no gore, no wounds, no surgical instruments, no text. ")
BODY = "an abstract translucent frosted-glass mannequin figure (upper body, smooth featureless surface like a glass anatomy model)"
SHOTS = {
 "s01": SB + f"Front medium shot of {BODY}; inside it the liver glows warm reddish-brown under the right ribs, other organs faint and grey.",
 "s02": SB + "Close-up of a glossy reddish-brown human liver floating alone in the air; a thin bright white glowing line runs across it dividing it into a larger right part and a smaller left part, no blood.",
 "s03": SB + f"Wide shot of two {BODY}s standing side by side facing each other; a glowing half of a liver floats in the air between them from the left body toward the right body, connected by a soft light trail.",
 "s04": SB + "Close-up of the remaining left half of a glossy reddish-brown liver floating in the air, its flat cut face softly glowing white, clean and smooth, no blood.",
 "s05": SB + "Extreme macro inside liver tissue: a honeycomb of hexagonal liver lobules made of glossy reddish-brown cells, a small central vein in each hexagon, soft glow, shallow depth of field.",
 "s06": SB + "Extreme macro: one glossy round liver cell splitting into two cells, a pinched waist between them, warm glow, other cells around softly blurred.",
 "s07": SB + "Medium shot of a half liver floating in the air while new glossy reddish-brown tissue swells outward from its glowing cut face, a faint white ghost outline shows the full original liver size around it.",
 "s08": SB + f"Medium shot of {BODY} on the right; inside it a small half liver glows and is growing larger, soft rings of light around it.",
 "s09": SB + "Two glossy reddish-brown livers floating side by side at the same size: the left one with the classic liver shape, the right one rounder and slightly different in shape, a thin white outline traced around each.",
 "s10": SB + f"Wide shot of {BODY} standing; its full-size liver glows warmly; the camera is pulled back, a lot of cyan space above the head.",
}
def run(k):
    r = subprocess.run([sys.executable, "gen_frame.py", f"/home/claude/v80/{k}.jpg", SHOTS[k]], capture_output=True, text=True)
    ok = "url http" in r.stdout
    return k, ok, "" if ok else (r.stdout + r.stderr)[-300:]
if __name__ == "__main__":
    only = sys.argv[1:] or list(SHOTS)
    with ThreadPoolExecutor(4) as ex:
        for k, ok, tail in ex.map(run, only): print(k, "OK" if ok else "FAIL " + tail)
