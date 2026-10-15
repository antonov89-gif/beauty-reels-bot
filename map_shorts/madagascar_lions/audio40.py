import os, subprocess
import numpy as np, soundfile as sf
import engine40 as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(40)
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
sfx = np.zeros(N); WT = E.WT; TL = E.TL
def rip():
    t = tt(0.45); return rng.normal(0, 1, len(t)) * (0.4 + 0.6 * (np.sin(2 * np.pi * 40 * t) > 0)) * np.exp(-t * 6) * 0.35
def clockt(d=2.0):
    s = np.zeros(int(d * SR))
    for q in range(int(d / 0.5)):
        x = tt(0.04); b = np.sin(2 * np.pi * 3000 * x) * np.exp(-x * 150) * 0.3; p = int(q * 0.5 * SR); s[p:p + len(b)] += b[:len(s) - p]
    return s
def crickets(d=1.5):
    t = tt(d); return np.sin(2 * np.pi * 4200 * t) * (np.sin(2 * np.pi * 30 * t) > 0.6) * (np.sin(2 * np.pi * 1.5 * t) > 0) * 0.06
def rooster():
    t = tt(0.9); f = 600 + 500 * np.sin(np.pi * t / 0.9) ** 2; return np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.sin(np.pi * t / 0.9) * 0.08
def ping():
    t = tt(0.4); return np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 9) * 0.25
def sad():
    t = tt(1.2); f = np.where(t < 0.4, 392, np.where(t < 0.8, 370, 349)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-((t % 0.4) * 4)) * 0.25
place(sfx, waves(3.0), 0.2, 0.45); place(sfx, pop(), WT(0, "hundred") - 0.15, 0.8); place(sfx, ding(), WT(0, "lion") - 0.1, 0.5); place(sfx, pop(), WT(0, "lion") - 0.1, 0.7)
place(sfx, rumble(2.5), TL[1][0] + 0.3, 0.7); place(sfx, pop(), WT(1, "hundred") - 0.15, 0.8); place(sfx, tick(), WT(1, "appeared") - 0.4, 0.9); place(sfx, hiss(0.7), WT(1, "appeared") - 0.3, 0.6)
place(sfx, crickets(3.0), TL[2][0] + 0.1, 1.0); place(sfx, pop(), WT(2, "ninety") - 0.15, 0.8)
place(sfx, waves(3.0), TL[3][0] + 0.1, 0.55); place(sfx, pop(), WT(3, "sixty") - 0.2, 0.7); place(sfx, pop(), WT(3, "rafts") - 0.1, 0.7)
place(sfx, pop(), WT(4, "fossa") - 0.1, 0.7); place(sfx, boing(), WT(4, "isnt") - 0.15, 0.8)
place(sfx, ding(), WT(5, "zero") - 0.1, 0.8); place(sfx, pop(), WT(5, "zero") - 0.1, 0.7); place(sfx, sad(), WT(5, "board") - 0.1, 0.6)
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
