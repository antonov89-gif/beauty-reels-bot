"""Audio for the week-of-21.10 Shorts. SHORT=<key> python3 audio60.py  -> <key>/mix.wav
voice = Lumean (ElevenLabs) delayed by LEAD; music = original beds synthesised for earlier Shorts; SFX synthesised here."""
import os, subprocess
import numpy as np, soundfile as sf
import engine61 as V
SR = 44100
N = int(V.TOTAL * SR) + SR
rng = np.random.default_rng(60)
BED = {"pointroberts": "v15", "guiana": "v16", "velez": "v17", "birtawil": "v16", "sa3": "v15", "llivia": "v17", "angle": "v16"}


def tt(d): return np.arange(int(d * SR)) / SR


def place(buf, s, t, g=1.0):
    i = int(t * SR)
    if i < 0: s = s[-i:]; i = 0
    if i < N: e = min(N, i + len(s)); buf[i:e] += s[:e - i] * g


def noise(d, lp=40): return np.convolve(rng.normal(0, 1, int(d * SR)), np.ones(lp) / lp, "same")


def whoosh(d=0.4):
    t = tt(d); x = rng.normal(0, 1, len(t)); f = np.cumsum(np.interp(t, [0, d], [300, 2600])) / SR
    return np.convolve(np.sin(2 * np.pi * f) * x * np.sin(np.pi * t / d) ** 2, np.ones(8) / 8, "same") * 0.3


def boom():
    t = tt(1.4); return (np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 3)) * t) * np.exp(-t * 2.4) * 0.9 + noise(1.4, 60) * np.exp(-t * 5) * 1.4) * 0.8


def ding():
    t = tt(0.9); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((1568, 4), (2093, 5), (3136, 7))) * 0.2


def tick():
    t = tt(0.04); return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * 0.25


def pop():
    t = tt(0.12); return np.sin(2 * np.pi * (500 + 900 * np.exp(-t * 40)) * t) * np.exp(-t * 35) * 0.45


raw, sr = sf.read(f"{V.SHORT}/lumean/result.mp3")
raw = raw.mean(axis=1) if raw.ndim > 1 else raw
if sr != SR:
    import scipy.signal as ss
    raw = ss.resample_poly(raw, SR, sr)
voice = np.zeros(N); i0 = int(V.LEAD * SR); seg = raw[:N - i0]; voice[i0:i0 + len(seg)] = seg
voice *= np.clip((V.TOTAL - 0.3 - np.arange(N) / SR) / 0.3, 0, 1)
m, msr = sf.read(f"/home/claude/{BED[V.SHORT]}/music.wav")
m = m.mean(axis=1) if m.ndim > 1 else m
if msr != SR:
    import scipy.signal as ss
    m = ss.resample_poly(m, SR, msr)
music = np.zeros(N); seg = m[:N]; music[:len(seg)] = seg
music *= np.minimum(1, np.arange(N) / (0.3 * SR)) * np.clip((V.TOTAL - np.arange(N) / SR) / 1.2, 0, 1)
sfx = np.zeros(N)
place(sfx, boom(), 0.0, 0.7)
for c in V.CUTS: place(sfx, whoosh(), c - 0.12, 0.4)
for s in V.SH:
    for fn, a in s[3]:
        if fn == "counter":
            ts, dur = a[5], a[6]
            for q in range(int(dur / 0.07)): place(sfx, tick(), ts + q * 0.07, 0.5)
            place(sfx, ding(), ts + dur, 0.5)
        elif fn == "flag": place(sfx, pop(), a[4], 0.55)
        elif fn == "pin": place(sfx, pop(), a[3], 0.55)
        elif fn == "big":
            place(sfx, pop(), a[3], 0.35)
place(sfx, ding(), V.TOTAL - 1.6, 0.4)
tag = V.SHORT
sf.write(f"{tag}/voice.wav", voice, SR); sf.write(f"{tag}/music.wav", music, SR); sf.write(f"{tag}/sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tag}/voice.wav", "-i", f"{tag}/music.wav", "-i", f"{tag}/sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.5[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=7:attack=8:release=300[md];"
                "[2:a]lowpass=f=9000,volume=0.6[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-2:LRA=9,alimiter=limit=0.7:level=0,aresample=44100[a]",
                "-map", "[a]", "-t", str(V.TOTAL), f"{tag}/mix.wav"], check=True)
print("mix", tag, round(V.TOTAL, 2))
