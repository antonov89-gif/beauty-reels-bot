import numpy as np, soundfile as sf, subprocess
import engine24 as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(4)
sfx = np.zeros(N)
def tt(d): return np.arange(int(d * SR)) / SR
def add(s, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N: e = min(N, i + len(s)); sfx[i:e] += s[:e - i] * g
def whoosh(d=0.4):
    t = tt(d); x = rng.normal(0, 1, len(t)); f = np.cumsum(np.interp(t, [0, d], [300, 2800])) / SR
    return np.convolve(np.sin(2 * np.pi * f) * x * np.sin(np.pi * t / d) ** 2, np.ones(8) / 8, "same") * 0.35
def pop():
    t = tt(0.12); return np.sin(2 * np.pi * (500 + 900 * np.exp(-t * 40)) * t) * np.exp(-t * 35) * 0.45
def stamp():
    t = tt(0.3); return (rng.normal(0, 1, len(t)) * np.exp(-t * 30) * 0.5 + np.sin(2 * np.pi * 90 * t) * np.exp(-t * 12)) * 0.8
def tick():
    t = tt(0.04); return np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 120) * 0.25
def firework():
    t = tt(1.4); s = np.sin(2 * np.pi * (60 + 50 * np.exp(-t * 10)) * t) * np.exp(-t * 6) * 0.6
    for k in range(40):
        p = int((0.15 + rng.random() * 1.0) * SR); c = rng.normal(0, 1, 300) * np.exp(-np.arange(300) / 60) * 0.5
        s[p:p + 300] += c[:len(s) - p]
    return s * 0.7
def riser(d=1.2):
    t = tt(d); f = np.cumsum(np.interp(t, [0, d], [200, 1400])) / SR
    return (np.sin(2 * np.pi * f) * 0.3 + rng.normal(0, 1, len(t)) * 0.15) * (t / d) ** 2 * 0.5
def plane(d=1.8):
    t = tt(d); x = np.convolve(rng.normal(0, 1, len(t)), np.ones(30) / 30, "same")
    return (x * 3 + np.sin(2 * np.pi * (180 - 60 * t / d) * t) * 0.2) * np.sin(np.pi * t / d) ** 2 * 0.4
def squawk():
    t = tt(0.35); f = 1400 + 500 * np.sin(2 * np.pi * 9 * t) - 900 * t
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.35) * 0.25 * (1 + 0.5 * np.sign(np.sin(2 * np.pi * 40 * t)))
def clink():
    t = tt(0.6); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((2800, 8), (3900, 11))) * 0.25
WT, ST, SC = E.WT, E.ST, E.SC
for c in E.CUTS: add(whoosh(), c - 0.15, 0.8)
for w, g in ((WT(0, "first"), 1), (WT(0, "last"), 1), (WT(1, "twentyfour"), 1), (WT(3, "first"), 1), (WT(4, "before"), 1), (WT(5, "nineteen"), 1),
             (WT(6, "moved"), 1), (WT(8, "last"), 1), (WT(9, "full"), 1), (WT(10, "twice"), 1), (WT(11, "very"), 1)): add(stamp(), w, 0.8)
for q in range(24): add(tick(), ST[1] + 2.2 * q / 24, 0.7)
add(riser(1.0), WT(2, "International") - 1.0, 0.8)
for w in ((3, "Kiribati"), (3, "hundred"), (3, "thirtythree"), (4, "Kiritimati"), (4, "London"), (4, "Banana"), (4, "Poland"), (5, "capital"),
          (5, "eastern"), (5, "whole"), (6, "thousands"), (8, "American"), (9, "Samoa"), (9, "seventy"), (11, "Baker"), (11, "Howland"), (11, "nobody"), (12, "final")):
    add(pop(), WT(*w), 0.9)
for dt in (0.2, 0.6, 1.0, 1.4, 1.8, 2.2, 2.6, 3.0): add(firework(), SC[0] + dt, 0.5)
for q in range(6): add(firework(), WT(4, "celebrate") + q * 0.22, 0.45)
for w in ("Zealand", "Australia", "Asia", "Europe", "Africa", "Americas"): add(firework(), WT(7, w), 0.6); add(firework(), WT(7, w) + 0.5, 0.4)
add(firework(), SC[10] + 0.1, 0.5); add(plane(1.8), WT(10, "fly"), 1.0); add(firework(), WT(10, "fly") + 1.6, 0.5)
for q in range(7): add(firework(), SC[12] + 0.3 + q * 0.45, 0.45)
for q in range(3): add(squawk(), WT(12, "seabirds") + q * 0.18, 1.0)
add(clink(), WT(12, "seabirds") + 0.5, 1.0)
sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
a, _ = sf.read("voice_44.wav"); v = np.zeros(N); i0 = int(E.LEAD * SR); e = min(N, i0 + len(a)); v[i0:e] = a[:e - i0]
sf.write("voice.wav", v, SR)
# upbeat documentary synth bed, 112 bpm
t = np.arange(N) / SR; beat = 60 / 112; mus = np.zeros(N)
prog = [[220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7], [164.8, 207.7, 246.9]]
for k in range(int(E.TOTAL / (beat / 2)) + 2):
    i0 = int(k * beat / 2 * SR); x = tt(beat / 2); ch = prog[(k // 16) % 4]; f = ch[k % 3] * 2
    s = (np.sign(np.sin(2 * np.pi * f * x)) * 0.25 + np.sin(2 * np.pi * f * x)) * np.exp(-x * 9) * 0.08
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
for k in range(int(E.TOTAL / (beat * 4)) + 1):
    i0 = int(k * beat * 4 * SR); x = tt(beat * 4); ch = prog[(k // 2) % 4]
    s = sum(np.sin(2 * np.pi * f * x) for f in ch) * 0.05 * np.minimum(1, x / 0.3) * np.exp(-x / 3)
    s += np.sin(2 * np.pi * ch[0] / 2 * x) * 0.12 * np.exp(-x / 1.5)
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
for k in range(int(E.TOTAL / beat) + 1):
    i0 = int(k * beat * SR); x = tt(0.25)
    s = np.sin(2 * np.pi * (48 + 70 * np.exp(-x * 25)) * x) * np.exp(-x * 13) * 0.45 + rng.normal(0, 1, len(x)) * np.exp(-x * 60) * (0.12 if k % 2 else 0.03)
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
mus *= np.minimum(1, t / 0.3) * np.clip((E.TOTAL + 0.2 - t) / 1.5, 0, 1)
sf.write("music.wav", mus / np.abs(mus).max() * 0.7, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.34[m];[m][vsc]sidechaincompress=threshold=0.05:ratio=9:attack=8:release=320[md];"
                "[2:a]volume=0.9[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix", E.TOTAL)
