import subprocess
import numpy as np
import soundfile as sf
import engine19s as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(3)
sfx = np.zeros(N)


def add(sig, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N:
        e = min(N, i + len(sig)); sfx[i:e] += sig[:e - i] * g


def tt(d): return np.arange(int(d * SR)) / SR


def click():
    t = tt(0.05); return (rng.normal(0, 1, len(t)) * np.exp(-t * 160) * 0.5 + np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * 0.4)


def ching():
    t = tt(0.9)
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((2093, 5), (2637, 6), (3136, 7)))
    s[:int(0.06 * SR)] += rng.normal(0, 1, int(0.06 * SR)) * 0.6 * np.exp(-tt(0.06) * 60)
    return s * 0.28


def tick():
    t = tt(0.03); return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 140) * 0.25


def whoosh(d=0.4):
    t = tt(d); x = rng.normal(0, 1, len(t)) * np.sin(np.pi * t / d) ** 2
    return np.convolve(x, np.ones(12) / 12, "same") * 0.35


def boom():
    t = tt(0.8); return np.sin(2 * np.pi * (48 + 40 * np.exp(-t * 9)) * t) * np.exp(-t * 4) * 0.9


for ct in E.SCENE_T[1:-1]:
    add(click(), ct, 0.8)
for i, p in E.PHOTO.items():
    tb = E.WT(i, p["buy"]) + 0.15
    add(ching(), tb, 1.0)
    for q in range(10): add(tick(), tb + q * 0.06, 0.6)
    if p.get("grid"): add(whoosh(0.5), E.WT(i, p["grid"]), 0.8)
add(boom(), E.SCENE_T[8], 0.9)
for q in range(20): add(tick(), E.WT(9, "nine") + q * 0.04, 0.5)
sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice_raw.wav", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
a, _ = sf.read("voice_44.wav")
voice = np.zeros(N); i0 = int(E.LEAD * SR); e = min(N, i0 + len(a)); voice[i0:e] = a[:e - i0]
sf.write("voice.wav", voice, SR)
# light lo-fi bed: soft electric-piano chords + muted kick/hat, 88 bpm
t = np.arange(N) / SR
bar = 60 / 88 * 4
chords = [[261.6, 329.6, 392.0, 493.9], [220.0, 261.6, 329.6, 392.0], [174.6, 220.0, 261.6, 329.6], [196.0, 246.9, 293.7, 349.2]]
mus = np.zeros(N)
for b in range(int(E.TOTAL / bar) + 2):
    i0 = int(b * bar * SR); n = int(bar * SR)
    x = np.arange(n) / SR
    env = np.minimum(1, x / 0.02) * np.exp(-x / 1.6)
    sig = sum(np.sin(2 * np.pi * f * x) + 0.3 * np.sin(4 * np.pi * f * x) for f in chords[b % 4]) * env * 0.05
    e2 = min(N, i0 + n)
    if e2 > i0: mus[i0:e2] += sig[:e2 - i0]
beat = 60 / 88
for k in range(int(E.TOTAL / beat)):
    i0 = int(k * beat * SR); x = tt(0.2)
    kick = np.sin(2 * np.pi * (45 + 60 * np.exp(-x * 25)) * x) * np.exp(-x * 14) * (0.35 if k % 2 == 0 else 0.0)
    hat = rng.normal(0, 1, len(x)) * np.exp(-x * 90) * 0.05
    s = kick + hat
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
mus *= np.minimum(1, t / 0.5) * np.clip((E.TOTAL + 0.3 - t) / 1.2, 0, 1)
sf.write("music.wav", mus / np.abs(mus).max() * 0.7, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.30[m];[m][vsc]sidechaincompress=threshold=0.05:ratio=8:attack=8:release=300[md];"
                "[2:a]volume=0.8[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix done", E.TOTAL)
