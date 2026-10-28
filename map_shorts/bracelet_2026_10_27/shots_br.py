"""Bracelet rescue Short (another channel, AI-generated, realistic): 13 storyboard frames. LOCK keeps the same woman, wrist, bangle and cuff in every shot.
Usage: python3 shots_br.py b01 b02 ...  (two at a time) -> /home/claude/v90/frames/<id>.jpg"""
import os
import subprocess
import sys

LOCK = ("Keep identical in every shot: WOMAN: late 20s, warm light-brown skin, dark hair tied back, sage-green knit top, natural short unpainted nails. "
        "HER LEFT WRIST: a thick hammered yellow-gold bangle with a row of tiny engraved dots, stuck tight on the wrist; the skin of the hand just below it shows a "
        "mild purple-blue bruise-like gradient from swelling (no blood, no wound). "
        "JEWELLER: a man about 45 in a dark grey leather apron, only his hands and forearms are visible. WORKSHOP: warm wooden bench, firebrick, brass tools, steel rolling mill. "
        "FINISHED PIECE: a wide polished yellow-gold cuff bracelet with a hand-engraved leaf pattern. ")
SHOTS = {
    "b01": "High angle: her left forearm rests palm-down on a cream linen cloth, the jeweller's hands in a dark grey apron hold a small rotary ring cutter against the thick gold bangle that is visibly too tight and pressing into the swollen skin; the back of her hand and wrist show a clear, vivid purple-blue bruise-like gradient (swelling only, no blood, no wound); her other hand is tense at the edge of the frame; the bench around is plain with only a few steel tools, no gold cuff, no other jewellery anywhere.",
    "b02": "Extreme close-up: the spinning cutter wheel biting into the thick gold bangle, a fine spray of gold dust and a few tiny sparks, the bruised skin soft in the background.",
    "b03": "Close-up: the thick gold bangle is cut through, a clear open gap of a few millimetres at the top of the bangle where the cutter passed, the cutter lifted away, the swollen skin beneath is pressed and discoloured purple-blue.",
    "b03n": "Wide-medium shot from the side: ONLY ONE of her arms is in the frame: her left forearm lies on the workbench, coming from a sage-green sleeve at the right edge to her hand at the left, back of the hand up; her other arm and hand are completely out of frame, nothing else of her is visible. The thick gold bangle on her wrist has just been cut through, a clean open gap at the top; the jeweller's two hands in a dark grey apron hold small cutters near it; the swollen wrist shows a purple-blue bruise-like gradient (no blood); no strap, no band, no cord on her wrist; warm wooden bench and the rolling mill blurred behind.",
    "b04": "Medium close-up: steel pliers spread the cut bangle open and the jeweller slides it off her swollen wrist, her hand relaxes, the purple-blue mark softer in the light; no other gold jewellery and no finished cuff anywhere on the bench or in the background.",
    "b05": "Top-down on a firebrick: the opened gold bangle lies in a ceramic crucible, a pinch of white flux powder falls onto it from a spoon, brass tools around.",
    "b06": "Close-up: a gas torch flame melts the gold in the crucible into one glowing orange-yellow liquid bead, heat shimmer, dark background.",
    "b07": "Close-up: molten gold pours in a bright thin stream from the crucible into a rectangular steel ingot mould, glowing and smoking slightly.",
    "b08": "Close-up: tongs lift the small cooled gold bar out of a steel bowl of water, steam rising, droplets on the bar, matte golden surface.",
    "b09": "Medium close-up: a small gold bar enters the steel rollers of an electric rolling mill, the jeweller's hand at the crank side, motor and rollers sharp.",
    "b10": "Close-up: a long thin flat strip of bright gold emerges from the rolling mill rollers and curls onto the bench, reflective surface; only the jeweller's hands and apron are visible, no woman, no bracelet on anyone.",
    "b11": "Close-up: the gold strip is bent around a round wooden mandrel held in a bench vise, a small steel hammer mid-swing, motion blur on the hammer; only the jeweller's hands and apron are visible, no woman, no bracelet on anyone.",
    "b12": "Macro: the finished wide engraved gold cuff is held in the jeweller's hands and polished with a soft grey cloth, the leaf pattern catches the light, brass tools blurred behind; only the jeweller's hands and apron are visible, no woman, no one wearing any bracelet.",
    "b13": "Medium close-up: the woman slides the wide polished gold cuff onto her left wrist, the skin now clean and healed with no bruise, she looks down and smiles softly, warm window light.",
}
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_frame_real.py")
if __name__ == "__main__":
    os.makedirs("/home/claude/v90/frames", exist_ok=True)
    ids = sys.argv[1:]
    for k in range(0, len(ids), 2):
        ps = [(s, subprocess.Popen(["python3", G, f"/home/claude/v90/frames/{s}.jpg", LOCK + SHOTS[s]],
                                   stdout=open(f"/home/claude/v90/frames/{s}.log", "w"), stderr=subprocess.STDOUT)) for s in ids[k:k + 2]]
        for s, p in ps:
            p.wait()
            ok = os.path.exists(f"/home/claude/v90/frames/{s}.jpg") and os.path.getsize(f"/home/claude/v90/frames/{s}.jpg") > 30000
            print(s, "ok" if ok else "FAIL", flush=True)
