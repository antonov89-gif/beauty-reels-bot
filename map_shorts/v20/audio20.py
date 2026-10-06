import subprocess
import numpy as np
import soundfile as sf
import engine20 as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(3)
sfx = np.zeros(N)


def add(sig, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N:
        e = min(N, i + len(sig)); sfx[i:e] += sig[:e - i] * g


def tt(d): return np.arange(int(d * SR)) / SR
def click(): t = tt(0.05); return rng.normal(0, 1, len(t)) * np.exp(-t * 160) * 0.4 + np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90) * 0.35
def tick(): t = tt(0.03); return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 140) * 0.22
def pop(): t = tt(0.1); return np.sin(2 * np.pi * (520 + 700 * np.exp(-t * 40)) * t) * np.exp(-t * 32) * 0.4
def boom(): t = tt(0.8); return np.sin(2 * np.pi * (48 + 40 * np.exp(-t * 9)) * t) * np.exp(-t * 4) * 0.9


def ching():
    t = tt(0.9)
    s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((2093, 5), (2637, 6), (3136, 7)))
    s[:int(0.06 * SR)] += rng.normal(0, 1, int(0.06 * SR)) * 0.6 * np.exp(-tt(0.06) * 60)
    return s * 0.26


def whoosh(d=0.45):
    t = tt(d); x = rng.normal(0, 1, len(t)) * np.sin(np.pi * t / d) ** 2
    return np.convolve(x, np.ones(12) / 12, "same") * 0.35


for ct in E.SCENE_T[1:-1]:
    add(click(), ct, 0.7)
for tb, c, lab, _ in E.BUYS:
    add(ching(), tb, 0.9)
    for q in range(8): add(tick(), tb + q * 0.07, 0.5)
for i, sc in enumerate(E.SCENES):
    t0 = E.SCENE_T[i]
    k = sc["t"]
    if k == "photo" and sc.get("grid") and sc.get("buy"):
        add(whoosh(0.5), E.WT(i, sc["buy"]), 0.8)
    if k == "photo" and sc.get("pt"):
        add(pop(), E.WT(i, sc["pt"]), 0.7)
    if k in ("count", "years", "tick"):
        for q in range(18): add(tick(), t0 + 0.15 + q * 0.065, 0.5)
    if k == "failed":
        ta = E.WT(i, sc["at"]); add(whoosh(0.4), ta, 0.8); add(boom(), ta + 0.25, 0.7)
    if k == "card":
        steps = sc.get("steps") or []
        add(pop(), t0 + 0.05, 0.6)
        for w in steps: add(pop(), E.WT(i, w), 0.6)
    if k in ("stack", "chart"):
        add(whoosh(0.8), t0 + 0.2, 0.6)
    if k == "people":
        for q in range(10): add(pop(), t0 + 0.15 + q * 0.12, 0.35)
    if k == "checkout" and sc.get("total"):
        add(ching(), t0 + 1.3, 1.0)
        for q in range(12): add(pop(), t0 + 1.3 + q * 0.05, 0.3)
sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
a, _ = sf.read("voice_44.wav")
voice = np.zeros(N); i0 = int(E.LEAD * SR); e = min(N, i0 + len(a)); voice[i0:e] = a[:e - i0]
sf.write("voice.wav", voice, SR)
t = np.arange(N) / SR
bar = 60 / 86 * 4
prog = [[261.6, 329.6, 392.0, 493.9], [220.0, 261.6, 329.6, 392.0], [174.6, 220.0, 261.6, 329.6], [196.0, 246.9, 293.7, 349.2],
        [233.1, 293.7, 349.2, 440.0], [196.0, 233.1, 293.7, 349.2], [174.6, 220.0, 261.6, 329.6], [196.0, 246.9, 293.7, 392.0]]
mus = np.zeros(N)
for b in range(int(E.TOTAL / bar) + 2):
    i0 = int(b * bar * SR); n = int(bar * SR)
    x = np.arange(n) / SR
    env = np.minimum(1, x / 0.03) * np.exp(-x / 1.8)
    sig = sum(np.sin(2 * np.pi * f * x) + 0.25 * np.sin(4 * np.pi * f * x) for f in prog[b % 8]) * env * 0.045
    sig += np.sin(2 * np.pi * prog[b % 8][0] / 2 * x) * np.minimum(1, x / 0.05) * np.exp(-x / 1.2) * 0.12
    e2 = min(N, i0 + n)
    if e2 > i0: mus[i0:e2] += sig[:e2 - i0]
beat = 60 / 86
for k in range(int(E.TOTAL / beat)):
    i0 = int(k * beat * SR); x = tt(0.22)
    kick = np.sin(2 * np.pi * (45 + 60 * np.exp(-x * 25)) * x) * np.exp(-x * 14) * (0.32 if k % 2 == 0 else 0.0)
    snare = rng.normal(0, 1, len(x)) * np.exp(-x * 30) * (0.08 if k % 2 == 1 else 0.0)
    hat = rng.normal(0, 1, len(x)) * np.exp(-x * 90) * 0.04
    s = kick + snare + hat
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
mus *= np.minimum(1, t / 1.0) * np.clip((E.TOTAL + 0.3 - t) / 3.0, 0, 1)
sf.write("music.wav", mus / np.abs(mus).max() * 0.7, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.26[m];[m][vsc]sidechaincompress=threshold=0.05:ratio=8:attack=8:release=300[md];"
                "[2:a]volume=0.75[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=48000[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "-ar", "48000", "mix.wav"], check=True)
print("mix done", E.TOTAL)
