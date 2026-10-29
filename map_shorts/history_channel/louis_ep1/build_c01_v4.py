"""C01 v4 (owner 29.10: "Oops, the ceiling" WHILE the camera still looks at the ceiling, and no visible splice).
Hand-held opening cut at 4.0 s (camera lands at 3.7 s) + Seedance 2.5 part 2 v4, whose first frame IS the last frame of that cut (plain concat, no dissolve).
Voice (ours, locked): "Oops, the ceiling." over the ceiling at OOPS_AT; "There ... faint" aligned by phrase to the model's speech.
Usage: python3 build_c01_v4.py <part2.mp4> <out.mp4>"""
import subprocess, sys, numpy as np
from faster_whisper import WhisperModel
OPEN_LEN = 4.0; P2_SKIP = 1 / 24; SR = 48000; OOPS_AT = 0.45  # P2_SKIP: part 2 frame 0 repeats the opening's last frame, drop it
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
OURS = "../voice/tts_ep1/C01.mp3"; OPEN = "frames/C01_open_handheld.mp4"; P2, OUT = sys.argv[1], sys.argv[2]
m = WhisperModel("small", device="cpu", compute_type="int8")


def words(path):
    segs, _ = m.transcribe(path, word_timestamps=True, language="en")
    return [(w.word.strip().strip(".,!").lower(), w.start, w.end) for s in segs for w in s.words]


def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P2, "-vn", "-ac", "1", "-ar", "16000", SC + "p2v4.wav"], check=True)
mv = words(SC + "p2v4.wav"); ov = words(OURS)
if mv and mv[0][1] < 0.05:                                          # Whisper pins the first word to 0.0: use the energy onset of the model's speech
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", SC + "p2v4.wav", "-f", "f32le", "-"], capture_output=True, check=True).stdout, dtype=np.float32); e = np.array([np.sqrt((a[i:i + 160] ** 2).mean()) for i in range(0, len(a) - 160, 160)])
    on = float(np.argmax(e > e.max() * 0.1)) * 0.01; mv[0] = (mv[0][0], on, max(on + 0.2, mv[0][2])); print("first-word onset by energy", on)
print("model:", [(w, round(a, 2)) for w, a, _ in mv]); print("ours:", [w for w, _, _ in ov])
assert len(mv) == len(ov) - 3, "model words do not match the line: check by ear before aligning"
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", OURS, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32); total = OPEN_LEN + dur(P2) - P2_SKIP
track = np.zeros(int(SR * (total + 0.3)), dtype=np.float32)


def put(seg, t):
    i0 = int(max(0, t) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]


def cut(a, b): return x[int(max(0, ov[a][1] - 0.06) * SR):int((ov[b - 1][2] + 0.10) * SR)]


put(cut(0, 3), OOPS_AT)
rep = []
for a, b in [(3, 4), (4, 7), (7, 8), (8, 11), (11, 15)]:           # There | Welcome to Versailles | Yes | I'm that handsome | Try not to faint
    seg = cut(a, b); our_d = ov[b - 1][2] - ov[a][1]; mod_d = mv[b - 4][2] - mv[a - 3][1]; tempo = 1.0
    if b - a > 1 and our_d > mod_d * 1.12:
        tempo = min(1.15, our_d / mod_d)
        seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, dtype=np.float32)
    put(seg, OPEN_LEN - P2_SKIP + mv[a - 3][1] - 0.06)
    for j in range(a, b): rep.append((ov[j][0], round(OPEN_LEN - P2_SKIP + mv[j - 3][1], 2), round((ov[j][1] - ov[a][1]) / tempo - (mv[j - 3][1] - mv[a - 3][1]), 2), round(tempo, 2)))
print("word | abs time | residual vs lips | tempo"); [print(*r) for r in rep]; print("max |residual|", max(abs(r[2]) for r in rep))
open(SC + "c01v4_voice.f32", "wb").write(track.tobytes())
fc = (f"[0:v]trim=0:{OPEN_LEN},setpts=PTS-STARTPTS,setsar=1,fps=24[a];[1:v]trim=start_frame=1,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p[b];"
      f"[a][b]concat=n=2:v=1:a=0[vv];[2:a]loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.2dB,alimiter=limit=0.80:attack=2:release=60:level=disabled[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", OPEN, "-i", P2, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c01v4_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]", "-c:v", "libx264", "-crf", "16",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", OUT], check=True)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", OUT, "-vf", "scale=216:384,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
v = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 384, 216).astype(np.float32); d = np.abs(np.diff(v, axis=0)).mean(axis=(1, 2)); s = int(OPEN_LEN * 24) - 1
print("duration %.2f s" % (len(v) / 24), "| join frame diffs", [round(float(q), 1) for q in d[s - 3:s + 4]], "(join =", round(float(d[s]), 1), ") | median after landing", round(float(np.median(d[90:])), 1))
