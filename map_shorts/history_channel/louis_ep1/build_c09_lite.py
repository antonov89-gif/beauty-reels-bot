"""C09 from the Seedance 2.5 Lite remake (seedance25lite_c09.mp4, 720p): our locked line laid on the king's lips, Marcel's own voice for "Pardon, Sire!", the model's own SOUNDS kept (its speech removed by htdemucs).
Model speech (energy of the htdemucs vocals stem, 10% / 30% of peak): "Lower," 0.30-0.65 | "lower," 1.05-1.45 | "and there goes the hat" 2.95-4.65 | (silent pause 1.0 s) | "Eyes on me, not on the hat" 6.5-7.9 (faint breath at 6.0-6.15). The model made no real "Pardon, Sire!" (only a faint blip at 2.5 s), so Marcel's cry is ours (voice/tts_ep1/marcel_C09_pardon.mp3), placed when the hat rolls and he turns after it.
Our line is shorter than the model's slow deadpan delivery, so the tempo may go down to 0.80 and up to 1.25 (phrase borders and lengths are measured on the energy of our own track, not taken from ASR).
Usage: python3 build_c09_lite.py -> frames/C09L_final_A.mp4 (1080x1920, our voices only) + scratchpad lite_c09_rest_A.f32 (model sounds)"""
import subprocess, numpy as np
from faster_whisper import WhisperModel
V = "A"; SR = 48000; MODEL = "frames/seedance25lite_c09.mp4"
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
UNITS = [(0.30, 0.65), (1.05, 1.45), (2.95, 4.65), (6.50, 7.90)]
MARCEL_AT = 1.85; MARCEL_GAIN = 0.6                    # speech onset of "Pardon, Sire!" (s) and its level against the king (he stands further away)
def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)


x = load("../voice/tts_ep1/C09.mp3"); mx = load("../voice/tts_ep1/marcel_C09_pardon.mp3")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MODEL], capture_output=True, text=True).stdout)
track = np.zeros(int(SR * (dur + 0.3)), np.float32)
MV = np.frombuffer(open(SC + "sep/lite_c09_vocals.f32", "rb").read(), np.float32).reshape(-1, 2).mean(1)   # the model's speech alone (htdemucs), 44.1 kHz


def env(y, sr):
    w = int(sr * .01); return np.array([np.sqrt((y[i:i + w] ** 2).mean()) for i in range(0, len(y) - w, w)])


def onset(y, from_s=0.0):                                           # first 10-ms frame above -20 dB of the phrase's own peak
    e = env(y, SR); k = int(max(0, from_s) / 0.01); return (k + float(np.argmax(e[k:] > e.max() * 0.1))) * 0.01


def model_onset(m0, m1):
    a = int(max(0, m0 - 0.3) * 44100); e = env(MV[a:int(m1 * 44100)], 44100); return a / 44100 + float(np.argmax(e > e.max() * 0.3)) * 0.01


def gaps(y):                                                        # centres of the silent stretches (> 0.2 s, below -26 dB of the peak) between our phrases
    e = env(y, SR); q = e < e.max() * 0.05; out = []; i = 0
    while i < len(q):
        if q[i]:
            j = i
            while j < len(q) and q[j]: j += 1
            if j - i >= 20 and i > 5 and j < len(q) - 5: out.append((i + j) / 2 * 0.01)
            i = j
        else: i += 1
    return out


G = gaps(x); assert len(G) == 3, G
edges = [0.0] + G + [len(x) / SR]
for n, (m0, m1) in enumerate(UNITS):
    seg = x[int(edges[n] * SR):int(edges[n + 1] * SR)].copy(); f = int(SR * .006); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    e = env(seg, SR); idx = np.flatnonzero(e > e.max() * 0.1); ours = (idx[-1] + 1 - idx[0]) * 0.01   # speech length of this phrase in our line
    tp = float(np.clip(ours / (m1 - m0), 0.80, 1.25))
    if abs(tp - 1) > .01: seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tp:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, np.float32)
    lead = onset(seg); t0 = model_onset(m0, m1)                    # first speech energy of our phrase on the first speech energy of the model's phrase
    i0 = int(max(0, t0 - lead) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]
    print("unit", n + 1, "| speech starts", round(t0, 2), "tempo", round(tp, 3), "| our speech", round(ours / tp, 2), "s, model lips", round(m1 - m0, 2), "s")
f = int(SR * .01); mx = mx.copy(); mx[:f] *= np.linspace(0, 1, f); mx[-f:] *= np.linspace(1, 0, f)
i0 = int((MARCEL_AT - onset(mx)) * SR); k = min(len(mx), len(track) - i0); track[i0:i0 + k] += mx[:k] * MARCEL_GAIN
print("Marcel 'Pardon, Sire!' speech starts at", MARCEL_AT, "s")
open(SC + "c09L_voice.f32", "wb").write(track.tobytes())
vf = "scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p"
fc = f"[0:v]{vf}[vv];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.2dB,alimiter=limit=0.80:attack=2:release=60:level=disabled[v]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c09L_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]",
                "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", f"frames/C09L_final_{V}.mp4"], check=True)
r = np.frombuffer(open(SC + "sep/lite_c09_rest.f32", "rb").read(), np.float32).reshape(-1, 2)
r = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", "-", "-ar", str(SR), "-f", "f32le", "-"], input=r.tobytes(), capture_output=True).stdout, np.float32)
open(SC + f"lite_c09_rest_{V}.f32", "wb").write(r.astype(np.float32).tobytes())
