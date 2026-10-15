import os, subprocess
import numpy as np, soundfile as sf
import engine37 as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(37)
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
sfx = np.zeros(N); WT = E.WT; TL = E.TL; B = E.B
def hit():
    t = tt(1.2); return (np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 8)) * t) * np.exp(-t * 3.5) * 0.9 + rng.normal(0, 1, len(t)) * np.exp(-t * 25) * 0.25)
def thump():
    t = tt(0.5); return (np.sin(2 * np.pi * (70 + 30 * np.exp(-t * 15)) * t) * np.exp(-t * 9) * 0.8 + noise(0.5, 80)[:len(t)] * np.exp(-t * 20) * 1.5)
def roar(d=4.2):
    t = tt(d); return (noise(d, 60) * 9 + noise(d, 8) * 2.5) * np.minimum(1, t / 0.4) * np.clip((d - t) / 1.2, 0, 1) * 0.35
def riser(d=1.0):
    t = tt(d); f = np.cumsum(np.interp(t, [0, d], [200, 1500])) / SR
    return (np.sin(2 * np.pi * f) * 0.25 + rng.normal(0, 1, len(t)) * 0.12) * (t / d) ** 2 * 0.5
def clink():
    t = tt(0.6); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((2800, 8), (3900, 11))) * 0.28
def stamp():
    t = tt(0.3); return (rng.normal(0, 1, len(t)) * np.exp(-t * 30) * 0.5 + np.sin(2 * np.pi * 90 * t) * np.exp(-t * 12)) * 0.8
def ping():
    t = tt(0.4); return np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 9) * 0.25
def plop():
    t = tt(0.25); return np.sin(2 * np.pi * (300 + 500 * np.exp(-t * 25)) * t) * np.exp(-t * 14) * 0.4
place(sfx, riser(0.9), WT(0, "ninetysix") - 0.75, 0.6); place(sfx, hit(), WT(0, "ninetysix"), 0.9)
place(sfx, stamp(), WT(0, "purpose"), 0.8)
place(sfx, thump(), TL[1][0] + 1.7, 0.8); place(sfx, hiss(0.7), TL[1][0] + 1.75, 0.5)
place(sfx, roar(), B[1] + 0.1, 0.9); place(sfx, pop(), WT(1, "fuel") - 0.05, 0.7)
for w in ("boots", "backpacks", "bags"): place(sfx, pop(), WT(2, w) - 0.05, 0.8)
place(sfx, thump(), TL[4][0] + 1.0, 0.6)
place(sfx, clink(), WT(3, "three"), 0.8); place(sfx, ding(), TL[8][0] + 0.2, 0.7)
place(sfx, whoosh(0.5), TL[10][0] - 0.2, 0.6)
place(sfx, plop(), WT(4, "poop"), 0.8); place(sfx, ding(), WT(4, "rocks"), 0.7)
place(sfx, pop(), WT(5, "fifty") - 0.05, 0.7); place(sfx, riser(1.2), WT(5, "survived") - 1.0, 0.5); place(sfx, ding(), TL[12][0] + 0.3, 0.8); place(sfx, ping(), WT(5, "survived"), 0.8)
place(sfx, thump(), TL[13][0] + 0.9, 0.7); place(sfx, boing(), WT(6, "pickup"), 0.9); place(sfx, whoosh(0.6), WT(6, "pickup") + 0.1, 0.5)
for c in E.CUTS: place(sfx, whoosh(0.3), c - 0.1, 0.25)
t = np.arange(N) / SR; beat = 60 / 96; mus = np.zeros(N)
prog = [[220.0, 261.6, 329.6], [196.0, 246.9, 293.7], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
for k in range(int(E.TOTAL / (beat / 2)) + 2):
    i0 = int(k * beat / 2 * SR); x = tt(beat / 2); ch = prog[(k // 8) % 4]; f = ch[k % 3] * 2
    s = np.sin(2 * np.pi * f * x) * np.exp(-x * 9) * 0.07; e = min(N, i0 + len(s)); mus[i0:e] += s[:e - i0]
for k in range(int(E.TOTAL / (beat * 4)) + 1):
    i0 = int(k * beat * 4 * SR); x = tt(beat * 4); ch = prog[k % 4]
    s = sum(np.sin(2 * np.pi * f * x) for f in ch) * 0.035 * np.minimum(1, x / 0.3) * np.exp(-x / 2.5) + np.sin(2 * np.pi * ch[0] / 2 * x) * 0.08 * np.exp(-x / 1.5)
    e = min(N, i0 + len(s)); mus[i0:e] += s[:e - i0]
for k in range(int(E.TOTAL / beat) + 1):
    i0 = int(k * beat * SR); x = tt(0.2); s = np.sin(2 * np.pi * (50 + 60 * np.exp(-x * 25)) * x) * np.exp(-x * 14) * 0.3
    e = min(N, i0 + len(s)); mus[i0:e] += s[:e - i0]
mus *= np.minimum(1, t / 0.3) * np.clip((E.TOTAL + 0.1 - t) / 1.0, 0, 1)
sf.write("music.wav", mus / np.abs(mus).max() * 0.7, SR); sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.22[m];[m][vsc]sidechaincompress=threshold=0.05:ratio=8:attack=8:release=300[md];"
                "[2:a]lowpass=f=7000,volume=0.55[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix", E.TOTAL)
