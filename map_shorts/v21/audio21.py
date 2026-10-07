import subprocess
import numpy as np
import soundfile as sf
import engine21 as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(7)
sfx = np.zeros(N)


def add(sig, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N:
        e = min(N, i + len(sig)); sfx[i:e] += sig[:e - i] * g


def tt(d): return np.arange(int(d * SR)) / SR


def whoosh(d=0.35):
    t = tt(d); x = rng.normal(0, 1, len(t)) * np.sin(np.pi * t / d) ** 2
    return np.convolve(x, np.ones(10) / 10, "same") * 0.4


def bleat():
    t = tt(0.5); f = 330 + 60 * np.sin(2 * np.pi * 28 * t) - 90 * t
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.5) * 0.25


def step():
    t = tt(0.07); return rng.normal(0, 1, len(t)) * np.exp(-t * 70) * 0.25


def crash():
    t = tt(1.1); x = rng.normal(0, 1, len(t)) * np.exp(-t * 5)
    for k in range(8):
        p = int((0.05 + k * 0.045 + rng.random() * 0.03) * SR)
        c = np.sin(2 * np.pi * (1500 + rng.random() * 2500) * tt(0.15)) * np.exp(-tt(0.15) * 35) * 0.6
        x[p:p + len(c)] += c[:len(x) - p]
    return x * 0.6


def thud():
    t = tt(0.5); return np.sin(2 * np.pi * (60 + 60 * np.exp(-t * 14)) * t) * np.exp(-t * 7) * 0.9


def shimmer():
    t = tt(1.4); s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 2.2) for f in (1568, 2093, 2637, 3136))
    return s * 0.1 * np.minimum(1, t / 0.05)


def paper():
    t = tt(0.5); return np.convolve(rng.normal(0, 1, len(t)), np.ones(3) / 3, "same") * np.sin(np.pi * t / 0.5) ** 2 * 0.18


def tick():
    t = tt(0.03); return np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 140) * 0.2


def clink():
    t = tt(0.5); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((2800, 9), (3700, 12))) * 0.2


def bell():
    t = tt(2.2); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((880, 1.6), (1320, 2.2), (1760, 3))) * 0.2


def pop():
    t = tt(0.1); return np.sin(2 * np.pi * (500 + 900 * t / 0.1) * t) * np.exp(-t * 40) * 0.3


for ct in E.CUTS:
    add(whoosh(0.28), ct - 0.12, 0.5)
for k in range(8): add(step(), E.starts[1] + 0.2 + k * 0.4, 0.8)
add(bleat(), E.WT(0, "lost") + 0.1, 0.9)
add(bleat(), E.starts[11] + 0.6, 0.9)
for k in range(10): add(step(), E.starts[1] + 0.4 + k * 0.3, 0.6)
add(whoosh(0.5), E.WT(2, "threw") - 0.05, 1.0)
add(thud(), E.WT(3, "pottery") - 0.1, 0.9)
add(crash(), E.WT(3, "pottery"), 1.0)
add(shimmer(), E.WT(4, "jars"), 0.8)
add(paper(), E.WT(4, "scrolls") - 0.1, 1.0)
add(shimmer(), E.WT(4, "scrolls") + 0.05, 1.0)
for k in range(24): add(tick(), E.starts[5] + k * 0.05, 0.6)
for k in range(3): add(clink(), E.WT(7, "few") + k * 0.12, 1.0)
add(bell(), E.starts[8] + 0.55, 1.0)
for k in range(11): add(pop(), E.WT(9, "eleven") - 0.8 + k * 0.1, 0.7)
for k in range(4): add(pop(), E.starts[10] - 0.06 + k * 0.5, 0.9)
sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
a, _ = sf.read("voice_44.wav")
voice = np.zeros(N); i0 = int(E.LEAD * SR); e = min(N, i0 + len(a)); voice[i0:e] = a[:e - i0]
sf.write("voice.wav", voice, SR)
# playful pizzicato/marimba bed, 104 bpm, pentatonic
t = np.arange(N) / SR
beat = 60 / 104
mus = np.zeros(N)
notes = [261.6, 329.6, 392.0, 329.6, 440.0, 392.0, 329.6, 293.7]
for k in range(int(E.TOTAL / (beat / 2)) + 2):
    i0 = int(k * beat / 2 * SR); x = tt(0.35); f = notes[k % 8] * (1 if (k // 8) % 2 == 0 else 0.75)
    s = (np.sin(2 * np.pi * f * x) + 0.4 * np.sin(4 * np.pi * f * x)) * np.exp(-x * 11) * 0.12
    e2 = min(N, i0 + len(s))
    if e2 > i0: mus[i0:e2] += s[:e2 - i0]
for k in range(int(E.TOTAL / beat) + 1):
    i0 = int(k * beat * SR); x = tt(0.2)
    s = np.sin(2 * np.pi * (50 + 60 * np.exp(-x * 25)) * x) * np.exp(-x * 14) * 0.3 * (1 if k % 2 == 0 else 0.0)
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
mus *= np.clip((E.TOTAL + 0.3 - t) / 1.2, 0, 1) * np.minimum(1, t / 0.2)
sf.write("music.wav", mus / np.abs(mus).max() * 0.7, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.28[m];[m][vsc]sidechaincompress=threshold=0.05:ratio=8:attack=8:release=300[md];"
                "[2:a]volume=0.8[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix done", E.TOTAL)
