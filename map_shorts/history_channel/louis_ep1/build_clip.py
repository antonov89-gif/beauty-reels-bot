"""Generic clip build for ep.1 clips after C01 (same method as build_c01_v4.py).
Our locked voice (voice/tts_ep1/<CID>.mp3) is cut into sentences; each sentence starts where the model's matching phrase starts (energy, gaps >= GAP s) and is fitted to its length, tempo capped at 1.15x.
The model clip's frame 0 repeats the previous clip's last frame (it was the input image), so it is dropped.
Usage: python3 build_clip.py <CID> <model.mp4> <out.mp4> [<previous_clip.mp4> for a preview with the join]"""
import subprocess, sys, numpy as np
from faster_whisper import WhisperModel
CID, MODEL, OUT = sys.argv[1:4]; PREV = sys.argv[4] if len(sys.argv) > 4 else None
SR = 48000; SKIP = 1 / 24; MAXT = 1.15; GAP = 0.4; GAP2 = 0.25; GAPW = 0.15
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
x = pcm(OURS, SR); total = dur(MODEL) - SKIP; track = np.zeros(int(SR * (total + 0.3)), dtype=np.float32)
cuts = [0] + [i + 1 for i, (w, _, _) in enumerate(ov) if w[-1:] in ".!?" and i + 1 < len(ov)] + [len(ov)]   # our sentences
a16 = pcm(SC + CID + "_m.wav", 16000); e = np.array([np.sqrt((a16[i:i + 160] ** 2).mean()) for i in range(0, len(a16) - 160, 160)])
act = e > e.max() * 0.08; regs = []; st = None                     # the model's phrases by energy (Whisper word times drift on these clips)
for i, v in enumerate(list(act) + [False]):
    if v and st is None: st = i
    if not v and st is not None:
        if regs and st / 100 - regs[-1][1] < GAP: regs[-1][1] = i / 100
        else: regs.append([st / 100, i / 100])
        st = None
regs = [r for r in regs if r[1] - r[0] > 0.35]                      # drops a short "hm" or breath
print("model phrases by energy:", regs, "| our sentences:", len(cuts) - 1)
assert len(mv) == len(ov) or len(regs) == len(cuts) - 1, "word and phrase counts differ: check by ear, align by hand"
def subregions(i0, i1, gap):
    sub = []; st = None
    for i in range(i0, i1 + 1):
        v = i < i1 and act[i]
        if v and st is None: st = i
        if not v and st is not None:
            if sub and st / 100 - sub[-1][1] < gap: sub[-1][1] = i / 100
            else: sub.append([st / 100, i / 100])
            st = None
    return sub


units = []
if len(mv) == len(ov):                                              # same words: each energy phrase takes the model words whose middle falls in it, ours by the same index
    sub = [r for r in subregions(0, len(act), GAPW) if r[1] - r[0] > 0.12]   # whole clip: short phrases like "Now, the wig" count too
    owner = [min(range(len(sub)), key=lambda k: 0 if sub[k][0] <= (w[1] + w[2]) / 2 <= sub[k][1] else min(abs(sub[k][0] - (w[1] + w[2]) / 2), abs(sub[k][1] - (w[1] + w[2]) / 2))) for w in mv]
    for k in range(len(sub)):
        idx = [j for j, o in enumerate(owner) if o == k]
        if idx: units.append(((idx[0], idx[-1] + 1), sub[k][0], sub[k][1]))
    assert all(u[0][1] == v[0][0] for u, v in zip(units, units[1:])), "word order broken: align by hand"
else:
    units = []                                                          # (our word range, model start, model end): a sentence is split further at the model's internal pauses
    for (a, b), (m0, m1) in zip(zip(cuts, cuts[1:]), regs):
        sub = []; st = None; i0, i1 = int(m0 * 100), int(m1 * 100)
        for i in range(i0, i1 + 1):
            v = i < i1 and act[i]
            if v and st is None: st = i
            if not v and st is not None:
                if sub and st / 100 - sub[-1][1] < GAP2: sub[-1][1] = i / 100
                else: sub.append([st / 100, i / 100])
                st = None
        pauses = sorted(range(a + 1, b), key=lambda j: ov[j][1] - ov[j - 1][2], reverse=True)[:len(sub) - 1]
        if len(sub) > 1 and len(pauses) == len(sub) - 1 and all(ov[j][1] - ov[j - 1][2] >= 0.08 for j in pauses):
            edges = [a] + sorted(pauses) + [b]; units += [((p, q), r0, r1) for (p, q), (r0, r1) in zip(zip(edges, edges[1:]), sub)]
        else: units.append(((a, b), m0, m1))

rep = []
for (a, b), m0, m1 in units:
    seg = x[int(max(0, ov[a][1] - 0.06) * SR):int((ov[b - 1][2] + 0.10) * SR)]
    our_d = ov[b - 1][2] - ov[a][1]; mod_d = m1 - m0; tempo = 1.0
    if our_d > mod_d * 1.05:
        tempo = min(MAXT, our_d / mod_d)
        seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tempo:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, dtype=np.float32)
    over = max(0.0, our_d / tempo - mod_d); t0 = m0 - over / 2          # still longer than the lips: centre it, the offset is split between start and end
    i0 = int(max(0, t0 - 0.06 - SKIP) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]
    rep.append((" ".join(w for w, _, _ in ov[a:b]), round(t0 - SKIP, 2), round(over / 2, 2), round(tempo, 2)))
print("phrase | start | offset at start and end vs lips (s) | tempo"); [print(*r) for r in rep]; print("max offset", max(abs(r[2]) for r in rep))
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
