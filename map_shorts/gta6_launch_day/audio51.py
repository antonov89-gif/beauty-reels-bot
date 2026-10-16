import os, subprocess
import numpy as np, soundfile as sf
import engine51 as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(51)
def tt(d): return np.arange(int(d * SR)) / SR
def place(buf, s, t, g=1.0):
    i = int(t * SR)
    if i < 0: s = s[-i:]; i = 0
    if i < N: e = min(N, i + len(s)); buf[i:e] += s[:e - i] * g
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
a, _ = sf.read("voice_44.wav"); voice = np.zeros(N); place(voice, a, E.LEAD); sf.write("voice.wav", voice, SR)
def noise(d, lp=40): return np.convolve(rng.normal(0, 1, int(d * SR)), np.ones(lp) / lp, "same")
def rumble(d=1.6):
    t = tt(d); return (noise(d, 300) * 6 + np.sin(2 * np.pi * 38 * t) * 0.4) * np.sin(np.pi * t / d) ** 2 * 0.5
def bubbles(d=2.0):
    s = np.zeros(int(d * SR))
    for k in range(14):
        p = int(rng.random() * (d - 0.15) * SR); x = tt(0.09); f = 300 + rng.random() * 500
        b = np.sin(2 * np.pi * (f + 900 * x) * x) * np.exp(-x * 40) * 0.3; s[p:p + len(b)] += b[:len(s) - p]
    return s
def tick():
    t = tt(0.05); return np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 110) * 0.35
def whoosh(d=0.45):
    t = tt(d); x = rng.normal(0, 1, len(t)); f = np.cumsum(np.interp(t, [0, d], [300, 2600])) / SR
    return np.convolve(np.sin(2 * np.pi * f) * x * np.sin(np.pi * t / d) ** 2, np.ones(8) / 8, "same") * 0.3
def waves(d=1.6):
    t = tt(d); return noise(d, 120) * 4 * (0.6 + 0.4 * np.sin(2 * np.pi * t / 1.2)) * np.sin(np.pi * t / d)
def zipf(d=0.5):
    t = tt(d); return np.sign(np.sin(2 * np.pi * (40 + 60 * t / d) * t)) * rng.normal(0, 0.3, len(t)) * np.exp(-t * 3) * 0.3
def hiss(d=0.7):
    t = tt(d); return rng.normal(0, 1, len(t)) * np.exp(-t * 5) * 0.25
def crack():
    t = tt(0.8); return (rng.normal(0, 1, len(t)) * np.exp(-t * 18) * 0.8 + np.sin(2 * np.pi * (60 + 40 * np.exp(-t * 6)) * t) * np.exp(-t * 4)) * 0.6
def water(d=2.0):
    t = tt(d); return noise(d, 25) * 3 * np.minimum(1, t / 0.4) * np.clip((d - t) / 0.6, 0, 1) * 0.6
def boing():
    t = tt(0.5); return np.sin(2 * np.pi * np.cumsum(220 + 180 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)) / SR) * np.exp(-t * 5) * 0.35
def ding():
    t = tt(1.0); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((1568, 4), (2093, 5), (3136, 7))) * 0.22
def pop():
    t = tt(0.12); return np.sin(2 * np.pi * (520 + 900 * np.exp(-t * 40)) * t) * np.exp(-t * 35) * 0.4

sfx = np.zeros(N); WT = E.WT
def thump():
    t = tt(0.55); return np.sin(2 * np.pi * (50 + 100 * np.exp(-t * 14)) * t) * np.exp(-t * 6) * 0.9
def boom():
    t = tt(2.2); return (np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 3)) * t) * np.exp(-t * 2.2) * 0.9 + noise(2.2, 60) * np.exp(-t * 5) * 1.5) * 0.9
def tickc():
    t = tt(0.06); return np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 90) * 0.5
def riser(d=6.0):
    t = tt(d); f = np.cumsum(120 + 1700 * (t / d) ** 2) / SR; return (np.sin(2 * np.pi * f) * 0.5 + noise(d, 8) * 0.8) * (t / d) ** 1.8 * 0.35
def cheer(d=3.0):
    t = tt(d); return noise(d, 12) * 3 * (0.6 + 0.4 * np.sin(2 * np.pi * 3.1 * t)) * np.sin(np.pi * t / d) ** 1.4 * 0.5
def drone(d=4.0, f=55):
    t = tt(d); return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.01 * t)) * (0.6 + 0.4 * np.sin(2 * np.pi * 6 * t)) * np.minimum(1, t / 0.5) * np.clip((d - t) / 0.5, 0, 1) * 0.25
def ping():
    t = tt(0.4); return np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 9) * 0.25
def kaching():
    return np.concatenate([ping(), np.zeros(int(0.06 * SR)), ding()])
def chime():
    t = tt(1.8); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((523, 2.0), (659, 2.4), (784, 2.8), (1046, 3.2))) * 0.25
def click():
    t = tt(0.05); return rng.normal(0, 1, len(t)) * np.exp(-t * 120) * 0.6
for c in E.CUTS: place(sfx, whoosh(0.35), c - 0.12, 0.6)
place(sfx, boom(), 0.35, 1.0); place(sfx, thump(), 0.9, 0.8)
tz = WT(0, "zero")
for q in range(1, 7): place(sfx, tickc(), tz - q, 0.8)
place(sfx, boom(), tz, 0.9)
a, b = E.SH[2][0], E.SH[2][1]; place(sfx, riser(b - a), a, 0.9)
place(sfx, cheer(4.0), E.SH[3][0] + 0.3, 0.9); place(sfx, thump(), WT(2, "ninety") - 0.1, 0.8)
place(sfx, kaching(), WT(3, "eight") - 0.1, 0.9); place(sfx, kaching(), WT(3, "billion") - 0.1, 0.9); place(sfx, boing(), WT(3, "nobody") - 0.1, 0.6)
place(sfx, rumble(3.0), E.SH[6][0], 0.5); place(sfx, crack(), WT(4, "moved") - 0.1, 0.7); place(sfx, boom(), WT(4, "blast") - 0.1, 0.8)
place(sfx, drone(max(3.0, E.CUT5 - E.SH[7][0]), 55), E.SH[7][0], 0.9); place(sfx, thump(), WT(5, "servers") - 0.1, 0.8); place(sfx, cheer(3.0), E.CUT5, 0.6)
for c in E.C6: place(sfx, whoosh(0.5), c, 0.7)
place(sfx, ding(), WT(6, "wakes") - 0.5, 0.7); place(sfx, waves(5.0), E.BL[6], 0.3)
place(sfx, thump(), WT(7, "two") - 0.1, 0.9); place(sfx, ding(), WT(7, "thirteen") - 0.2, 0.8)
place(sfx, click(), E.ST[8] + 0.45, 1.0); place(sfx, chime(), E.ST[8] + 0.55, 0.9); place(sfx, riser(1.2), E.ST[8] - 0.4, 0.5); place(sfx, boom(), E.ST[8] + 1.2, 0.8)
mus, _ = sf.read("music/bed.wav"); mus = mus.mean(axis=1) if mus.ndim > 1 else mus
m = np.zeros(N); m[:min(N, len(mus))] = mus[:N]; m *= np.minimum(1, np.arange(N) / (0.3 * SR)) * np.clip((E.TOTAL + 0.3 - np.arange(N) / SR) / 1.5, 0, 1)
sf.write("music.wav", m, SR); sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.55[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=7:attack=8:release=350[md];"
                "[2:a]lowpass=f=9000,volume=0.7[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix", E.TOTAL)
