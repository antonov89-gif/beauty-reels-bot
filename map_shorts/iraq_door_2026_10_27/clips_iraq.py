"""Iraq clips (veo3-1-fast, 720p, 8 s, $0.18 each) from the approved 3D keyframes in /home/claude/v86/ai. Two at a time (rate limit).
Usage: python3 clips_iraq.py c02 c03 ... -> /home/claude/v86/clips/<id>.mp4 ; prints 'cNN ok' or 'cNN FAIL'."""
import os
import subprocess
import sys

TAIL = (" The map, coastlines, borders, red and purple country layers and glowing lines stay perfectly fixed in place; "
        "no new objects appear; no text, no letters, no numbers.")
MOTION = {
    "c02": "Slow cinematic drone drift over the country at dusk; the network of warm city lights gently pulses and glows brighter along the roads; soft haze moving; camera pushes slowly toward the glowing coastline.",
    "c03": "Slow dramatic drone push-in along the coast between the two neighbouring countries; water shimmer and drifting haze; the yellow glowing coastline pulses softly.",
    "c04": "Slow aerial glide forward along the glowing cyan channel toward the open sea; gentle water ripples, crane lights flicker at the terminal; the camera descends slightly.",
    "c05": "Slow orbiting drone move over the channel; the white dashed border line floats and gently shimmers; the cyan deep-water lane pulses brighter along its length; light moving across the water.",
    "c07": "Slow push-in between the two ports; port cranes move slowly, small boats leave white wakes in the channel, golden light shimmering on the water.",
    "c09": "Slow cinematic pull-back at sunset; the oil supertanker moves slowly out to sea with a white wake; warm clouds drift across the sky; golden light sweeps over the country.",
}
FRAME = {c: "s" + c[1:] for c in MOTION}
if __name__ == "__main__":
    ids = sys.argv[1:]
    for k in range(0, len(ids), 2):
        ps = []
        for c in ids[k:k + 2]:
            ps.append((c, subprocess.Popen(
                ["python3", "/home/user/beauty-reels-bot/map_shorts/iraq_door_2026_10_27/gen_clip.py", f"/home/claude/v86/ai/{FRAME[c]}.jpg",
                 f"/home/claude/v86/clips/{c}.mp4", MOTION[c] + TAIL],
                stdout=open(f"/home/claude/v86/clips/{c}.log", "w"), stderr=subprocess.STDOUT)))
        for c, p in ps:
            p.wait()
            ok = os.path.exists(f"/home/claude/v86/clips/{c}.mp4") and os.path.getsize(f"/home/claude/v86/clips/{c}.mp4") > 100000
            print(c, "ok" if ok else "FAIL", flush=True)
