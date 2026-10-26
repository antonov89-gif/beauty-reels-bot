"""12 key frames for the Tristan Short (STYLE v2, game-engine CG). Run: python3 shots_tristan.py (Nano Banana 2.1 via APIpod, $0.02 each at 1K)."""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
CAST = ("Islanders: a man in a cream wool sweater and black rubber boots; a woman in a dark green wool cardigan with a grey headscarf; "
        "a boy in a navy wool sweater. All plain mid-century 1960s fishing-village clothes, no text on clothes.")
POV = "First-person POV from the narrator's eyes, her own pale hands and forearms in dark wool cuffs visible in the lower frame, wide 90-degree lens, slight handheld bob. "
SHOTS = {
 "s01": POV + "Dawn on a remote volcanic island: she runs down a grey stone path toward small wooden fishing boats on a dark pebble beach, islanders running ahead carrying bundles, a massive dark volcano filling the sky behind them with an orange glow and thick grey smoke at the summit, thin ash in the air, cool blue-grey light. " + CAST,
 "s02": "Wide establishing shot, no POV: about forty small figures of islanders gathered on a dark pebble beach at dawn beside wooden boats, some carrying bundles and a few sheep, a massive volcano behind them smoking with an orange glow, low grey clouds, a small village of low cottages on the green slope. " + CAST,
 "s03": POV + "Night, she sits in a crowded open wooden boat on a dark sea, her hands gripping the wooden side, islanders huddled in grey blankets around her, a faint orange glow of the volcano far behind on the horizon, heavy swell, cold blue moonlight.",
 "s04": POV + "Early morning on a grey sea: from a small crowded boat she sees a large dark-hulled passenger-cargo ship with a white superstructure approaching close, no name or text on the hull, a rope ladder hanging down the side, her hands on the boat's edge.",
 "s05": POV + "On the deck of the ship she holds the steel rail; ahead a harbour city under a tall flat-topped mountain in morning haze, cranes and ships in the harbour, seagulls.",
 "s06": POV + "She walks on wet tarmac toward long rows of low grey prefab huts of an old military camp in southern England, overcast sky, bare trees, a few islanders in the same wool clothes walking ahead looking around in confusion.",
 "s07": POV + "Inside a bare prefab hut: she sits on a metal-frame bed with a grey wool blanket, her hands in her lap, cold electric ceiling light, rain on a small window, a plain closed door ahead.",
 "s08": POV + "Close view of her hand scratching a short tally mark with a nail into a wooden window frame; the frame already has rows of tally marks; grey rainy window light.",
 "s09": POV + "Two years later, on a ship deck at dawn she holds the rail as a green volcanic island with a calm silent volcano, no smoke, rises out of thin mist ahead, small boats coming out to meet the ship, soft pale light.",
 "s10": POV + "She walks along a quiet grass lane between low stone cottages with corrugated metal roofs, doors closed, laundry-free wire lines, the volcano calm and clean behind with a little cloud on top, soft overcast light.",
 "s11": POV + "Final calm shot at the same dark pebble beach as the opening: she rests her hands on the side of a wooden boat pulled onto the stones, calm sea, the same massive volcano now silent with no smoke or glow, pale morning light, no people in sight.",
 "s12": "Low angle close shot following black rubber boots and wool trousers running on wet grey stones, other boots ahead, splashes, dawn light, slight motion blur, no faces. " + CAST,
}
def run(k):
    r = subprocess.run([sys.executable, "gen_frame.py", f"/home/claude/v74/{k}.jpg", SHOTS[k]], capture_output=True, text=True)
    ok = "url http" in r.stdout
    return k, ok, r.stdout[-200:] if not ok else ""
if __name__ == "__main__":
    only = sys.argv[1:] or list(SHOTS)
    with ThreadPoolExecutor(4) as ex:
        for k, ok, tail in ex.map(run, only): print(k, "OK" if ok else "FAIL " + tail)
