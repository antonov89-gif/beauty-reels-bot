"""Stonehenge clips (veo3-1-fast, 720p, 8 s, $0.18 each) from the approved frames. Runs 2 at a time (APIpod rate limit).
Usage: python3 clips_st.py c01 c03 ... -> /home/claude/v85/clips/<id>.mp4"""
import subprocess
import sys

TAIL = " Keep every stone one solid piece, no new objects or people appearing, no wheels, no metal, no text."
MOTION = {
    "c01": "Slow low-angle push-in toward the giant stone circle at sunrise; the small group of people stand still, one adjusts a coiled rope, wind moves the grass and their hair.",
    "c03": "The huge stone on its wooden sledge slides forward along the parallel timber rails toward the camera while the pullers' legs strain and step forward; slow camera moving backward at ground level.",
    "c04": "The giant stone slowly tips and slides down into the pit, the team easing the ropes and levers, dust and loose earth falling into the pit; static camera.",
    "c06": "The people on the timber platform push with long levers and the horizontal lintel stone slides slowly into place on top of the two uprights; slow upward tilt of the camera.",
    "c07": "Slow aerial drift forward over the green valley as the long line of people drags the stone on its sledge along the winding path.",
    "c08": "Slow push-in toward the flat reddish stone slab lying in the centre of the circle, mist drifting through the uprights, light slowly warming; no people.",
}
FRAME = {"c01": "s01", "c03": "s03", "c04": "s04", "c06": "s06", "c07": "s07", "c08": "s08"}
if __name__ == "__main__":
    ids = sys.argv[1:]
    for k in range(0, len(ids), 2):
        procs = [subprocess.Popen(["python3", "/home/user/beauty-reels-bot/map_shorts/stonehenge_2026_10_27/gen_clip.py",
                                   f"/home/claude/v85/frames/{FRAME[c]}.jpg", f"/home/claude/v85/clips/{c}.mp4", MOTION[c] + TAIL],
                                  stdout=open(f"/home/claude/v85/clips/{c}.log", "w"), stderr=subprocess.STDOUT) for c in ids[k:k + 2]]
        for p in procs:
            p.wait()
        for c in ids[k:k + 2]:
            print(c, "ok" if subprocess.run(["test", "-s", f"/home/claude/v85/clips/{c}.mp4"]).returncode == 0 else "FAIL", flush=True)
