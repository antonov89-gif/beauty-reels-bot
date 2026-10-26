"""Motion prompts for liver clips (Veo 3.1 Fast via gen_clip.py, $0.18 each). Run: python3 clips_liver.py [c01 c07 ...]"""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
TAIL = " Smooth medical 3D animation, the same clean cyan studio look as the start frame, no blood, no text, no captions, no logos, no new objects."
M = {
 "c01": "Slow camera push-in toward the glowing liver inside the translucent figure, the liver pulses with a soft warm glow, the other organs stay still and faint.",
 "c02": "The bright white line glows stronger and the liver gently separates along it into two parts that drift slightly apart in the air, slow rotation, no blood.",
 "c03": "The glowing half liver floats slowly along the light trail from the left figure to the right figure, the camera tracks sideways with it.",
 "c04": "Slow orbit around the remaining half liver, its smooth cut face glows softly and gently pulses.",
 "c05": "The camera glides forward over the honeycomb of hexagonal liver lobules, cells inside gently shimmer, slow dive toward the central vein of one hexagon.",
 "c06": "The glossy liver cell slowly pinches in the middle and splits into two round cells that drift apart, warm glow, nearby cells start to divide too.",
 "c07": "Time-lapse growth: the liver smoothly swells and grows until it fills the dotted white outline of its original size, the glow increases as it grows, the camera holds steady.",
 "c08": "Time-lapse: the small half liver inside the right translucent figure smoothly grows to full size, soft rings of light pulse outward.",
 "c09": "The two livers slowly rotate side by side, the white outlines trace around them, showing the same size but a different shape.",
 "c10": "Slow camera pull-back from the translucent figure, its full-size liver glows warmly, lots of cyan space above.",
}
def run(k):
    n = k[1:]
    r = subprocess.run([sys.executable, "gen_clip.py", f"/home/claude/v80/s{n}.jpg", f"/home/claude/v80/{k}.mp4", M[k] + TAIL], capture_output=True, text=True)
    return k, "url http" in r.stdout, (r.stdout + r.stderr)[-300:]
if __name__ == "__main__":
    ks = sys.argv[1:] or sorted(M)
    with ThreadPoolExecutor(4) as ex:
        for k, ok, tail in ex.map(run, ks): print(k, "OK" if ok else "FAIL " + tail, flush=True)
