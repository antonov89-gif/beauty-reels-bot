"""C04 from the Seedance 2.5 Lite pilot (seedance25lite_c04.mp4, 720p): our locked short line laid on the model's lips, the model's own SOUNDS kept (its speech removed by htdemucs).
Model says: "Now the wig." 0.0-1.84 | "My hair started falling out at 17." 2.54-4.48 | (silent 3.06 s) | "I took it personally." 7.54-8.9
Variant A: as generated. Variant B (trim): a vlog jump cut removes TRIM seconds of the silent pause, so the beat is about 1.3 s.
Usage: python3 build_c04_lite.py A|B -> frames/C04L_final_<v>.mp4 (1080x1920, our voice only) + scratchpad lite_c04_rest_<v>.f32 (model sounds, same cut)"""
import subprocess, sys, numpy as np
from faster_whisper import WhisperModel
V = sys.argv[1]; SR = 48000; MODEL = "frames/seedance25lite_c04.mp4"
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
UNITS = [(0, 1, 0.45, 1.10), (1, 3, 1.35, 1.95), (3, 10, 2.54, 4.48), (10, 14, 7.54, 8.90)]   # "Now," and "the wig." are two separate lip phrases in the model (0.58 and 1.39 s)   # our word range, model start, model end
TRIM = (5.2, 6.95) if V == "B" else None                                     # removed stretch of the silent pause
m = WhisperModel("medium", device="cpu", compute_type="int8")   # small put "My" inside the sigh before it
segs, _ = m.transcribe("../voice/tts_ep1/C04.mp3", word_timestamps=True, language="en", beam_size=5)
ov = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]; assert len(ov) == 14, [w for w, _, _ in ov]
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "../voice/tts_ep1/C04.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MODEL], capture_output=True, text=True).stdout)
cut = TRIM[1] - TRIM[0] if TRIM else 0.0; total = dur - cut; track = np.zeros(int(SR * (total + 0.3)), np.float32)


def cut_at(j):
    lo, hi = max(0.0, ov[j - 1][2] - 0.05), min(len(x) / SR, ov[j][1] + 0.15)
    return min((np.sqrt((x[int(t * SR):int((t + .02) * SR)] ** 2).mean()), t) for t in np.arange(lo, max(lo + .01, hi - .02), .005))[1] + 0.01


SIGH = (1.20, 1.60)                                              # the "small sigh" of our TTS before "My"; the model sighs/"ugh" with its mouth at 4.82-5.3 s
MV = np.frombuffer(open(SC + "sep/lite_c04_vocals.f32", "rb").read(), np.float32).reshape(-1, 2).mean(1)   # the model's speech alone (htdemucs), 44.1 kHz


def env(y, sr):
    w = int(sr * .01); return np.array([np.sqrt((y[i:i + w] ** 2).mean()) for i in range(0, len(y) - w, w)])


def onset(y, from_s=0.0):                                           # first 10-ms frame above -20 dB of the phrase's own peak, searched from from_s (skips a sigh before the word)
    e = env(y, SR); k = int(max(0, from_s) / 0.01); return (k + float(np.argmax(e[k:] > e.max() * 0.1))) * 0.01


def model_onset(m0, m1):
    a = int(max(0, m0 - 0.3) * 44100); e = env(MV[a:int(m1 * 44100)], 44100); return a / 44100 + float(np.argmax(e > e.max() * 0.1)) * 0.01


for a, b, m0, m1 in UNITS:
    s0 = cut_at(a) if a else max(0, ov[0][1] - 0.04); s1 = cut_at(b) if b < len(ov) else ov[-1][2] + 0.25
    if (a, b) == (1, 3): s1 = min((np.sqrt((x[int(t * SR):int((t + .02) * SR)] ** 2).mean()), t) for t in np.arange(0.92, 1.2, .005))[1] + 0.01   # stop before the sigh
    if (a, b) == (3, 10): s0 = max(s0, SIGH[1])                                                                                                       # start after the sigh
    seg = x[int(s0 * SR):int(s1 * SR)].copy(); f = int(SR * .006); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    tp = float(np.clip((ov[b - 1][2] - ov[a][1]) / (m1 - m0), 1.0, 1.12))
    if abs(tp - 1) > .01: seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tp:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, np.float32)
    lead = onset(seg, (ov[a][1] - s0) / tp - 0.1); t0 = model_onset(m0, m1) - (cut if TRIM and m0 > TRIM[1] else 0)   # align the first speech energy of our phrase to the first speech energy of the model's phrase
    i0 = int(max(0, t0 - lead) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]
    print(" ".join(w for w, _, _ in ov[a:b]), "| speech starts", round(t0, 2), "tempo", round(tp, 3), "| our length", round(len(seg) / SR, 2), "model length", round(m1 - m0, 2))
if True:                                                            # our sigh on the model's sigh
    sg = x[int(SIGH[0] * SR):int(SIGH[1] * SR)].copy(); f = int(SR * .02); sg[:f] *= np.linspace(0, 1, f); sg[-f:] *= np.linspace(1, 0, f)
    t_m = 4.82 - (cut if TRIM and 4.82 > TRIM[1] else 0); i0 = int(t_m * SR) - int(onset(sg) * SR); k = min(len(sg), len(track) - i0)
    if i0 >= 0 and not (TRIM and TRIM[0] <= 4.82 < TRIM[1] + .5): track[i0:i0 + k] += sg[:k] * 2.0; print("sigh placed at", round(t_m, 2), "s, our length", round(len(sg) / SR, 2))
open(SC + "c04L_voice.f32", "wb").write(track.tobytes())
vf = "scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p"
if TRIM: vf = f"select='not(between(t,{TRIM[0]},{TRIM[1]}))',setpts=N/24/TB," + vf
fc = f"[0:v]{vf}[vv];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.2dB,alimiter=limit=0.80:attack=2:release=60:level=disabled[v]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c04L_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]",
                "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", f"frames/C04L_final_{V}.mp4"], check=True)
r = np.frombuffer(open(SC + "sep/lite_c04_rest.f32", "rb").read(), np.float32).reshape(-1, 2)
r = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", "-", "-ar", str(SR), "-f", "f32le", "-"], input=r.tobytes(), capture_output=True).stdout, np.float32).reshape(-1, 2)
if TRIM: r = np.concatenate([r[:int(TRIM[0] * SR)], r[int(TRIM[1] * SR):]])
open(SC + f"lite_c04_rest_{V}.f32", "wb").write(r.astype(np.float32).tobytes())
