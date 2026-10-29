"""Generic clip build for ep.1 clips after C01 (same method as build_c01_v4.py).
Our locked voice (voice/tts_ep1/<CID>.mp3) is cut into phrases at punctuation and each phrase is placed on the model's speech (lips), tempo capped at 1.15x.
The model clip's frame 0 repeats the previous clip's last frame (it was the input image), so it is dropped.
Usage: python3 build_clip.py <CID> <model.mp4> <out.mp4> [<previous_clip.mp4> for a preview with the join]"""
import subprocess, sys, numpy as np
from faster_whisper import WhisperModel
CID, MODEL, OUT = sys.argv[1:4]; PREV = sys.argv[4] if len(sys.argv) > 4 else None
SR = 48000; SKIP = 1 / 24; MAXT = 1.15
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
OURS = f"../voice/tts_ep1/{CID}.mp3"
m = WhisperModel("small", device="cpu", compute_type="int8")


def words(path):
    segs, _ = m.transcribe(path, word_timestamps=True, language="en")
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]


def pcm(path, sr):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True).stdout, dtype=np.float32)


def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-vn", "-ac", "1", "-ar", "16000", SC + CID + "_m.wav"], check=True)
mv = words(SC + CID + "_m.wav"); ov = words(OURS)
print("model:", " ".join(f"{w}@{a:.2f}" for w, a, _ in mv)); print("ours: ", " ".join(w for w, _, _ in ov))
if mv and mv[0][1] < 0.05:                                          # Whisper pins the first word to 0.0: use the energy onset
    a = pcm(SC + CID + "_m.wav", 16000); e = np.array([np.sqrt((a[i:i + 160] ** 2).mean()) for i in range(0, len(a) - 160, 160)])
    on = float(np.argmax(e > e.max() * 0.1)) * 0.01; mv[0] = (mv[0][0], on, max(on + 0.2, mv[0][2])); print("first-word onset by energy", on)
assert len(mv) == len(ov), "model and our word counts differ: check by ear, align by hand"
x = pcm(OURS, SR); total = dur(MODEL) - SKIP; track = np.zeros(int(SR * (total + 0.3)), dtype=np.float32)
cuts = [0] + [i + 1 for i, (w, _, _) in enumerate(ov) if w[-1:] in ".,!?" and i + 1 < len(ov)] + [len(ov)]
rep = []
for a, b in zip(cuts, cuts[1:]):
    seg = x[int(max(0, ov[a][1] - 0.06) * SR):int((ov[b - 1][2] + 0.10) * SR)]
    our_d = ov[b - 1][2] - ov[a][1]; mod_d = mv[b - 1][2] - mv[a][1]; tempo = 1.0
    if b - a > 1 and our_d > mod_d * 1.12:
        tempo = min(MAXT, our_d / mod_d)
        seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, dtype=np.float32)
    i0 = int(max(0, mv[a][1] - 0.06 - SKIP) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]
    for j in range(a, b): rep.append((ov[j][0], round(mv[j][1] - SKIP, 2), round((ov[j][1] - ov[a][1]) / tempo - (mv[j][1] - mv[a][1]), 2), round(tempo, 2)))
print("word | time | residual vs lips | tempo"); [print(*r) for r in rep]; print("max |residual|", max(abs(r[2]) for r in rep))
open(SC + CID + "_voice.f32", "wb").write(track.tobytes())
fc = ("[0:v]trim=start_frame=1,setpts=PTS-STARTPTS,scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p[vv];"
      "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.2dB,alimiter=limit=0.80:attack=2:release=60:level=disabled[v]")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + CID + "_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]",
                "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", OUT], check=True)
if PREV:                                                            # preview: previous clip + this clip, to judge the join
    pv = OUT.replace(".mp4", "_with_prev.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", PREV, "-i", OUT, "-filter_complex", "[0:v]setsar=1[a];[1:v]setsar=1[b];[a][0:a][b][1:a]concat=n=2:v=1:a=1[v][au]", "-map", "[v]", "-map", "[au]",
                    "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k", pv], check=True)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", pv, "-vf", "scale=216:384,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    v = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 384, 216).astype(np.float32); d = np.abs(np.diff(v, axis=0)).mean(axis=(1, 2)); s = round(dur(PREV) * 24) - 1
    print("preview", pv, "| join frame diffs", [round(float(q), 1) for q in d[s - 3:s + 4]], "(join =", round(float(d[s]), 1), ") | clip median", round(float(np.median(d[s:])), 1))
