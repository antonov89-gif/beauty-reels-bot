"""Motion prompts for clips c02..c12 (c01 done). Veo 3.1 Fast via gen_clip.py, $0.18 each. Run: python3 clips_tristan.py [c02 c05 ...]"""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
TAIL = " Realistic motion, game-engine CG look unchanged, steady frame, no text, no captions, no logos."
M = {
 "c02": "Slow push-in over the crowd on the beach: islanders hurry along the shore carrying bundles and leading a few sheep toward the boats, boats are pushed into the water, smoke from the volcano drifts upward with a flicker of orange glow, wind and distant rumble.",
 "c03": "First-person POV in a packed open boat at night: the boat rocks on heavy swell, the narrator's hands grip the side, huddled islanders sway under grey blankets, spray flies, the faint orange glow far behind on the horizon flickers, creaking wood and sea sound.",
 "c04": "First-person POV from a small boat: the large ship slowly drifts closer, a rope ladder swings against the hull, men on the boat stand to reach for it, the narrator's hands tighten on the boat's edge, calm grey sea, low engine sound.",
 "c05": "First-person POV on the main deck of the ship: gentle forward motion toward the harbour city under the flat-topped mountain, seagulls fly past, cranes in the harbour slowly turn, the narrator's hands stay on the rail, soft wind and ship hum.",
 "c06": "First-person POV walking forward on wet tarmac toward the rows of grey huts, handheld walking bob, the islanders ahead glance around at the buildings and look lost, light rain, bare trees sway in the wind, distant traffic hum.",
 "c07": "First-person POV on the metal bed: slow camera tilt up from the narrator's hands in her lap to the closed door, a ceiling bulb flickers once, rain runs down the small window, a quiet room tone, her hands slowly clasp.",
 "c08": "Close view: the narrator's hand slowly scratches a new tally mark into the wooden window frame with a nail, wood dust falls, rain streams on the window glass behind, the camera makes a slight handheld drift, quiet scratching sound.",
 "c09": "First-person POV on the ship deck at dawn: slow forward motion toward the green island with the calm volcano, mist drifts across the water, small boats row out to meet the ship, the narrator's hands tighten on the rail, seabirds and low engine hum.",
 "c10": "First-person POV walking slowly forward along the grass lane between the stone cottages, her hands drift at her sides, wind moves the grass and a loose sheet of corrugated metal, a little cloud sits on the calm volcano, quiet village ambience.",
 "c11": "First-person POV at the beach: the narrator rests her hands on the boat, slow gentle push-in, small waves lap on the pebbles, the silent volcano stands calm behind with a slow drift of cloud, soft wind, the scene is peaceful and still.",
 "c12": "Low angle tracking behind running rubber boots on wet grey stones, splashes with each step, other boots ahead of them, dawn light, handheld shake, fast footsteps and heavy breathing.",
}
def run(k):
    n = k[1:]
    r = subprocess.run([sys.executable, "gen_clip.py", f"/home/claude/v74/s{n}.jpg", f"/home/claude/v74/{k}.mp4", M[k] + TAIL], capture_output=True, text=True)
    return k, "url http" in r.stdout, (r.stdout + r.stderr)[-250:]
if __name__ == "__main__":
    ks = sys.argv[1:] or sorted(M)
    with ThreadPoolExecutor(4) as ex:
        for k, ok, tail in ex.map(run, ks): print(k, "OK" if ok else "FAIL " + tail, flush=True)
