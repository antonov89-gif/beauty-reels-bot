"""C01 v3 (owner 29.10: he must say "Oops, the ceiling" WHILE the camera still looks at the ceiling).
Free assembly from existing material: hand-held ceiling opening + Kling tilt (cut at KLING_END), then the Seedance 2.5 final part 2 from P2_START (skips the model's own "Oops, the ceiling", which would be silent mouthing after the landing).
Voice (ours, locked): "Oops, the ceiling." placed over the ceiling (he is off-camera there, only his forehead is at the bottom edge); the rest aligned by phrase to the model's speech.
Prints the jump at the join (frame diff) so the owner's 'no visible splice' rule is measured."""
import subprocess, numpy as np
from faster_whisper import WhisperModel
KLING_END = 2.3; A_LEN = 1.7; OPEN_LEN = A_LEN + KLING_END; P2_START = 2.6; XF = 0.15; SR = 48000; OOPS_AT = 0.45
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
OURS = "../voice/tts_ep1/C01.mp3"; P2 = "frames/seedance25_p2_final.mp4"; OPEN = "frames/C01_open_handheld.mp4"
m = WhisperModel("small", device="cpu", compute_type="int8")


def words(path):
    segs, _ = m.transcribe(path, word_timestamps=True)
    return [(w.word.strip().strip(".,!").lower(), w.start, w.end) for s in segs for w in s.words]


subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P2, "-vn", "-ac", "1", "-ar", "16000", SC + "p2v3.wav"], check=True)
mv = words(SC + "p2v3.wav"); ov = words(OURS); mv[0] = (mv[0][0], 0.94, 1.2)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", OURS, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32); total = OPEN_LEN + (9.04 - P2_START) - XF
track = np.zeros(int(SR * (total + 0.3)), dtype=np.float32)


def put(seg, t):
    i0 = int(max(0, t) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]


def cut(a, b): return x[int(max(0, ov[a][1] - 0.06) * SR):int((ov[b - 1][2] + 0.10) * SR)]


put(cut(0, 3), OOPS_AT)                                            # "Oops, the ceiling." over the ceiling, natural pace
rep = []
for a, b in [(3, 4), (4, 7), (7, 8), (8, 11), (11, 15)]:           # There | Welcome to Versailles | Yes | I'm that handsome | Try not to faint
    seg = cut(a, b); our_d = ov[b - 1][2] - ov[a][1]; mod_d = mv[b - 1][2] - mv[a][1]; tempo = 1.0
    if b - a > 1 and our_d > mod_d * 1.12:
        tempo = min(1.15, our_d / mod_d)
        seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, dtype=np.float32)
    t = OPEN_LEN - XF + (mv[a][1] - 0.06 - P2_START); put(seg, t)
    for j in range(a, b): rep.append((ov[j][0], round(OPEN_LEN - XF + mv[j][1] - P2_START, 2), round((ov[j][1] - ov[a][1]) / tempo - (mv[j][1] - mv[a][1]), 2)))
print("word | abs time | residual vs lips"); [print(*r) for r in rep]; print("max |residual|", max(abs(r[2]) for r in rep))
open(SC + "c01v3_voice.f32", "wb").write(track.tobytes())
fc = (f"[0:v]trim=0:{OPEN_LEN},setpts=PTS-STARTPTS,setsar=1,fps=24[a];[1:v]trim=start={P2_START},setpts=PTS-STARTPTS,scale=1080:1920,setsar=1,fps=24,format=yuv420p[b];"
      f"[a][b]xfade=transition=fade:duration={XF}:offset={OPEN_LEN-XF:.3f}[vv];[2:a]loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.2dB,alimiter=limit=0.80:attack=2:release=60:level=disabled[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", OPEN, "-i", P2, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c01v3_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]", "-c:v", "libx264", "-crf", "16",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "frames/C01_final_v3.mp4"], check=True)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "frames/C01_final_v3.mp4", "-vf", "scale=216:384,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
v = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 384, 216).astype(np.float32); d = np.abs(np.diff(v, axis=0)).mean(axis=(1, 2)); s = int((OPEN_LEN - XF) * 24)
print("duration %.2f s" % (len(v) / 24), "| join frame diffs", [round(float(q), 1) for q in d[s - 3:s + 6]], "| clip median", round(float(np.median(d)), 1))
