"""Baby story clips (veo3-1-fast, 720p, 8 s, $0.18 each) from the approved storyboard frames. Runs 2 at a time (APIpod rate limit).
Usage: python3 clips_b81.py c02 c07b ... -> /home/claude/v88/clips/<id>.mp4"""
import subprocess
import sys

TAIL = " No new people or objects appear, faces stay the same, no text, no subtitles, no logos, no gore."
MOTION = {
    "c02": "The camera follows the nurse from behind at shoulder height as she walks briskly down the crowded corridor carrying the baby; people on the benches turn their heads, a doctor steps aside; smooth continuous forward tracking.",
    "c07b": "The mother hums softly with her eyes closed and gently strokes the baby's cheek; the baby's crying face slowly relaxes and calms; very slow push-in toward the two of them, warm window light flickering gently.",
    "c11": "The mother presses her cheek to the baby and rocks him slowly while the father's arms close around both; the nurse steps back smiling; very slow push-in, then hold still.",
}
FRAME = {"c02": "s02", "c07b": "s07b", "c11": "s11"}
if __name__ == "__main__":
    ids = sys.argv[1:]
    for k in range(0, len(ids), 2):
        procs = [subprocess.Popen(["python3", "/home/user/beauty-reels-bot/map_shorts/baby81_2026_10_27/gen_clip.py",
                                   f"/home/claude/v88/frames/{FRAME[c]}.jpg", f"/home/claude/v88/clips/{c}.mp4", MOTION[c] + TAIL],
                                  stdout=open(f"/home/claude/v88/clips/{c}.log", "w"), stderr=subprocess.STDOUT) for c in ids[k:k + 2]]
        for p in procs:
            p.wait()
        for c in ids[k:k + 2]:
            print(c, "ok" if subprocess.run(["test", "-s", f"/home/claude/v88/clips/{c}.mp4"]).returncode == 0 else "FAIL", flush=True)
