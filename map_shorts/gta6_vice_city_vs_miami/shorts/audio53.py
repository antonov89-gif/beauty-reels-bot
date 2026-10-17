"""Audio for the vertical Shorts: slice of the long video's voice + music, plus SFX. SHORT=s1 python3 audio53.py"""
import os, subprocess
import numpy as np, soundfile as sf
import engine53 as V
SR = 44100; N = int(V.TOTAL * SR) + SR; rng = np.random.default_rng(53)
def tt(d): return np.arange(int(d * SR)) / SR
def place(buf, s, t, g=1.0):
    i = int(t * SR)
    if i < 0: s = s[-i:]; i = 0
    if i < N: e = min(N, i + len(s)); buf[i:e] += s[:e - i] * g
def noise(d, lp=40): return np.convolve(rng.normal(0, 1, int(d * SR)), np.ones(lp) / lp, "same")
def whoosh(d=0.4):
    t = tt(d); x = rng.normal(0, 1, len(t)); f = np.cumsum(np.interp(t, [0, d], [300, 2600])) / SR
    return np.convolve(np.sin(2 * np.pi * f) * x * np.sin(np.pi * t / d) ** 2, np.ones(8) / 8, "same") * 0.3
def thump():
    t = tt(0.55); return np.sin(2 * np.pi * (50 + 100 * np.exp(-t * 14)) * t) * np.exp(-t * 6) * 0.9
def boom():
    t = tt(1.8); return (np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 3)) * t) * np.exp(-t * 2.2) * 0.9 + noise(1.8, 60) * np.exp(-t * 5) * 1.5) * 0.9
def ding():
    t = tt(1.0); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((1568, 4), (2093, 5), (3136, 7))) * 0.22
def cut(path, g0):
    a, sr = sf.read(path); a = a.mean(axis=1) if a.ndim > 1 else a
    i0 = int(g0 * SR); seg = a[i0:i0 + N]; out = np.zeros(N); out[:len(seg)] = seg; return out
voice = cut("voice.wav", V.OFF)
fade = np.clip((V.TOTAL - 0.9 - np.arange(N) / SR) / 0.3, 0, 1); voice *= fade      # cut the next line's first syllable
music = cut("music/bed.wav", V.OFF) * np.minimum(1, np.arange(N) / (0.2 * SR)) * np.clip((V.TOTAL - np.arange(N) / SR) / 1.2, 0, 1)
sfx = np.zeros(N)
place(sfx, boom(), 0.0, 0.8)
for c in V.CUTS: place(sfx, whoosh(), c - 0.12, 0.4)
for s in V.SPLITS: place(sfx, thump(), s + 0.3, 0.8); place(sfx, ding(), s + 0.35, 0.4)
place(sfx, ding(), V.TOTAL - 2.6, 0.5)
tag = V.SHORT
sf.write(f"voice_{tag}.wav", voice, SR); sf.write(f"music_{tag}.wav", music, SR); sf.write(f"sfx_{tag}.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"voice_{tag}.wav", "-i", f"music_{tag}.wav", "-i", f"sfx_{tag}.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.55[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=7:attack=8:release=300[md];"
                "[2:a]lowpass=f=9000,volume=0.65[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-2:LRA=9,alimiter=limit=0.7:level=0,aresample=44100[a]",
                "-map", "[a]", "-t", str(V.TOTAL), f"mix_{tag}.wav"], check=True)
print("mix", tag, round(V.TOTAL, 2))
