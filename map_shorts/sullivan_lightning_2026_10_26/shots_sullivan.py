"""Storyboard frames for the Sullivan Short (STYLE v2 + SB-v1). Run: python3 shots_sullivan.py [ids] (Nano Banana 2.1 via APIpod, $0.02 each at 1K)."""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
# SCENE_LOCK / character card, word for word in every shot with the ranger
RANGER = ("The ranger: a tall lean white man in his late fifties, short grey hair, clean-shaven, long face, "
          "wearing a plain grey-green park ranger uniform shirt with rolled sleeves, dark green trousers, brown leather work boots, "
          "a flat-brimmed tan ranger campaign hat; no badges with text, no name tags, no logos.")
SB = ("SB-v1: 1960s-70s Appalachian Blue Ridge mountains, Virginia, summer thunderstorms; dark slate-blue storm sky, wet green forest, "
      "grey rock; lightning is a single thin bright white-violet branching bolt that lights the whole scene; rain streaks. ")
TRUCK = "a plain 1960s dark green pickup truck with no text or emblem"
SHOTS = {
 "s01": SB + f"High aerial wide shot over forested mountain ridges in a thunderstorm at dusk: a narrow winding mountain road, {TRUCK} driving on it, a branching lightning bolt striking the truck's roof, a bright flash lighting the road and trees, rain.",
 "s02": SB + f"Medium shot from the passenger seat inside the cab of {TRUCK}: the ranger drives with both hands on a thin steering wheel, rain on the windshield, the road ahead, a blinding white flash outside lighting his face and the cab. " + RANGER,
 "s03": SB + "Close-up inside the dark truck cab: the ranger slumped unconscious against the seat back, eyes closed, mouth slightly open, thin wisps of smoke rising from his singed grey hair, eyebrows burned away, his hat fallen on the seat, no wounds, no blood, no gore, dim blue storm light through the rain-streaked window. " + RANGER,
 "s04": SB + f"Exterior wide side shot: {TRUCK} rolling slowly off the gravel shoulder of a mountain road toward a rocky cliff edge, a deep misty forested valley below, heavy rain, the headlights on, no driver visible.",
 "s05": SB + f"Low-angle detail shot at ground level: the front tire of {TRUCK} stops on loose gravel at the very edge of a rocky cliff, a few pebbles falling into the misty valley below, rain splashing.",
 "s06": SB + f"Medium-wide shot: the ranger stands in the rain beside {TRUCK} stopped at the cliff edge, bare-headed, hat in his hand, looking up at the dark sky as distant lightning flickers, calm stunned expression. " + RANGER,
 "s07": SB + "Wide night shot of a tall wooden fire lookout tower on a bare rocky mountain top, a lightning bolt striking the tower, the cabin windows glowing from the flash, storm clouds.",
 "s08": SB + "Extreme close-up detail: a worn brown leather work boot on wooden floorboards with a burnt hole at the toe, thin smoke curling from the hole, soft lamp light.",
 "s09": SB + "Wide shot at dusk of a small white wooden house with a front lawn in the mountains: a lightning arc jumps from a utility pole transformer toward the ranger standing on the lawn, bright flash, sparks, rain. " + RANGER,
 "s10": SB + "Interior of a small wooden ranger station with a desk, map board without readable text and a radio set: a bright white flash bursts through the window, the ranger at the desk flinches, a thin wisp of smoke from his hair. " + RANGER,
 "s11": SB + "Medium-wide shot: the ranger stands at the edge of a small clear freshwater mountain pool holding a fishing rod, a lightning bolt strikes the water surface a few metres from him, splash and white flash, dark sky. " + RANGER,
 "s12": SB + "Medium shot in a wet forest after the storm: the ranger stands calm, hat in hand, sunlight breaking through parting clouds behind him, rain drops on leaves, a faint relieved half-smile. " + RANGER,
 "s13": SB + "Wide shot on a rocky mountain overlook: the ranger in full uniform puts his ranger hat on and looks toward a huge dark thunderstorm rolling over the ridges toward him, first lightning in the distance. " + RANGER,
}
def run(k):
    r = subprocess.run([sys.executable, "gen_frame.py", f"/home/claude/v77/{k}.jpg", SHOTS[k]], capture_output=True, text=True)
    ok = "url http" in r.stdout
    return k, ok, r.stdout[-300:] + r.stderr[-300:] if not ok else ""
if __name__ == "__main__":
    only = sys.argv[1:] or list(SHOTS)
    with ThreadPoolExecutor(4) as ex:
        for k, ok, tail in ex.map(run, only): print(k, "OK" if ok else "FAIL " + tail)
