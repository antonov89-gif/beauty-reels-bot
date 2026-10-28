"""Bracelet Short clips: Seedance 2.0 i2v 720p, 4 s each ($0.504), from the approved storyboard frames. Two at a time.
Usage: python3 clips_br.py b02 b03 ... -> /home/claude/v90/clips/<id>.mp4"""
import os
import subprocess
import sys

TAIL = " Realistic hands with five fingers, natural skin, true workshop sound. No text, no logos, no new objects or people appear."
MOTION = {
    "b02": "Extreme close-up: the spinning cutter wheel cuts into the thick gold bangle, a fine spray of gold dust and tiny sparks, the bruised skin soft in the background; slight push-in.",
    "b03": "The cutter breaks through the bangle with a small snap, leaving a clear thin gap; the jeweller lifts the cutter away; the swollen bruised wrist stays still; slight push-in.",
    "b04": "Steel pliers spread the cut bangle open and the jeweller slides it off her swollen wrist; her hand relaxes and opens; slight camera drift; sound of metal and a relieved breath.",
    "b05": "Top-down: a spoon sprinkles white flux powder onto the opened gold bangle in the ceramic crucible; the powder settles on the gold; static camera with a slight push-in.",
    "b06": "The torch flame heats the gold in the crucible; it softens and collapses into one glowing orange liquid bead; heat shimmer; torch hiss; slight push-in.",
    "b07": "Molten gold pours in a bright thin stream into the steel ingot mould, glowing and smoking slightly; steady camera; sound of pouring.",
    "b08": "Tongs lift the small cooled gold bar out of the water; steam rises and droplets fall back into the bowl; hissing sizzle; slight push-in.",
    "b09": "The jeweller feeds the small gold bar between the steel rollers and turns the crank; the bar flattens as it passes through; rollers turning; motor hum.",
    "b10": "The long thin flat gold strip emerges from the rollers and curls onto the bench, reflective surface; slight push-in.",
    "b11": "The jeweller hammers the gold strip around the wooden mandrel held in the vise; clear metallic hammer strikes; the strip bends into a curve.",
    "b12": "The jeweller polishes the engraved gold cuff with a soft cloth, slowly turning it so the leaf pattern catches the light; slight push-in.",
    "b13": "The woman slides the wide polished gold cuff onto her left wrist, looks down and smiles softly; warm window light; slight push-in; the sound of the cuff sliding on.",
}
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen_clip_multi.py")
if __name__ == "__main__":
    os.makedirs("/home/claude/v90/clips", exist_ok=True)
    ids = sys.argv[1:]
    for k in range(0, len(ids), 2):
        ps = [(c, subprocess.Popen(["python3", G, "seedance-2.0-i2v", f"/home/claude/v90/frames/{c}.jpg", f"/home/claude/v90/clips/{c}.mp4", MOTION[c] + TAIL, "4"],
                                   stdout=open(f"/home/claude/v90/clips/{c}.log", "w"), stderr=subprocess.STDOUT)) for c in ids[k:k + 2]]
        for c, p in ps:
            p.wait()
            ok = os.path.exists(f"/home/claude/v90/clips/{c}.mp4") and os.path.getsize(f"/home/claude/v90/clips/{c}.mp4") > 50000
            print(c, "ok" if ok else "FAIL", flush=True)
