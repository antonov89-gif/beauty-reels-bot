"""Motion prompts for Sullivan clips c01..c13 (Veo 3.1 Fast via gen_clip.py, $0.18 each). Run: python3 clips_sullivan.py [c01 c05 ...]
Act 1 (c01-c05) camera keeps moving forward so the clips join as one continuous camera with whip/blur transitions."""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
TAIL = " Physically plausible motion, the same game-engine CG look as the start frame, the same man, no new people, no text, no captions, no logos."
M = {
 "c01": "Aerial drone shot descending toward the truck on the winding mountain road in the rain; the lightning bolt hits the truck roof with a bright flash, the flash fades, the truck keeps rolling slowly, sparks fade, thunder crack, rain.",
 "c02": "Camera slowly pushes in from the passenger seat toward the ranger driving; a blinding white flash fills the windshield, his head jerks back, the cab interior flickers, rain on the glass, loud thunder.",
 "c03": "Slow push-in on the unconscious ranger slumped in the cab; thin smoke curls up from his singed hair, his head sways gently as the truck rolls, rain streaks on the window, faint lightning flicker outside, no blood.",
 "c04": "Camera tracks sideways with the empty pickup as it rolls slowly off the gravel shoulder toward the cliff edge, a slight tilted Dutch angle, gravel crunches, headlights shine into the rain and the misty valley below.",
 "c05": "Low ground-level camera: the front tire rolls the last few centimetres and stops at the very edge of the cliff, small pebbles tumble down into the misty valley, the truck rocks once and holds still, rain splashes.",
 "c06": "Slow push-in on the ranger standing beside the stopped truck at the cliff edge in the rain, he slowly looks up at the dark sky as distant lightning flickers, raindrops run off his hat in his hand.",
 "c07": "Slow push-in on the fire lookout tower on the mountain top at night; a lightning bolt strikes the tower, the cabin windows flash white, sparks fall, thunder.",
 "c08": "Very slow push-in on the burnt boot on the floorboards, thin smoke curls from the hole at the toe and drifts upward, soft lamp light flickers once.",
 "c09": "Static wide shot: the electric arc jumps from the utility pole transformer toward the ranger on the lawn, sparks fly, he staggers back one step but stays on his feet, the flash fades, rain, loud crackle.",
 "c10": "Slow push-in inside the ranger station: a bright flash bursts through the window, the ranger at the desk flinches and raises his arm, a thin wisp of smoke rises from his hat, papers flutter.",
 "c11": "Static medium-wide: the lightning bolt hits the pool next to the ranger, water bursts up in a white splash, he flinches back holding the fishing rod, the flash fades, rain falls on the water.",
 "c12": "Slow push-in on the ranger standing calm in the wet forest after the storm, sunbeams widen through the parting clouds behind him, he gives a small tired smile, drops fall from the leaves.",
 "c13": "Camera slowly rises behind the ranger on the rocky overlook as he settles his hat on his head and faces the thunderstorm rolling toward him over the ridges, distant lightning, wind in the trees.",
}
def run(k):
    n = k[1:]
    r = subprocess.run([sys.executable, "gen_clip.py", f"/home/claude/v77/s{n}.jpg", f"/home/claude/v77/{k}.mp4", M[k] + TAIL], capture_output=True, text=True)
    return k, "url http" in r.stdout, (r.stdout + r.stderr)[-300:]
if __name__ == "__main__":
    ks = sys.argv[1:] or sorted(M)
    with ThreadPoolExecutor(4) as ex:
        for k, ok, tail in ex.map(run, ks): print(k, "OK" if ok else "FAIL " + tail, flush=True)
