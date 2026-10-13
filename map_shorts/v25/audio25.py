import numpy as np, soundfile as sf, subprocess
import engine25 as E
SR = 44100; N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(9); sfx = np.zeros(N)
def tt(d): return np.arange(int(d * SR)) / SR
def add(s, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N: e = min(N, i + len(s)); sfx[i:e] += s[:e - i] * g
def whoosh(d=0.6):
    t = tt(d); x = np.convolve(rng.normal(0, 1, len(t)), np.ones(80) / 80, "same")
    return x * np.sin(np.pi * t / d) ** 2 * 2.0
def click():
    t = tt(0.08); return np.sin(2 * np.pi * 1300 * t) * np.exp(-t * 70) * 0.25
def impact():
    t = tt(0.9); return np.sin(2 * np.pi * (50 + 40 * np.exp(-t * 9)) * t) * np.exp(-t * 5) * 0.6
for i, (txt, clips, card) in enumerate(E.S):
    a = E.SPAN[i][0]
    if card and card[0] == "phase": add(whoosh(0.7), a - 0.3, 0.8); add(impact(), a + 0.15, 0.7)
    elif card and card[0] == "tip": add(click(), a + 0.05, 1.0); add(whoosh(0.4), a - 0.15, 0.35)
    elif card and card[0] == "recap":
        for q in range(8): add(click(), a + 0.4 + q * (E.SPAN[i][1] - a - 1.2) / 8, 0.6)
    elif card and card[0] in ("title", "end"): add(impact(), a + 0.2, 0.6)
sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
v, _ = sf.read("voice_44.wav"); voice = np.zeros(N); i0 = int(E.LEAD * SR); e = min(N, i0 + len(v)); voice[i0:e] = v[:e - i0]
sf.write("voice.wav", voice, SR)
# lo-fi acoustic bed: plucked guitar-like arpeggios (Karplus-Strong) + soft pad + light kick/shaker, 92 bpm
beat = 60 / 92
def pluck(f, d=1.2):
    n = int(d * SR); p = max(2, int(SR / f)); buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for k in range(n):
        out[k] = buf[k % p]; buf[k % p] = 0.996 * 0.5 * (buf[k % p] + buf[(k + 1) % p])
    return out * 0.3
prog = [[196.0, 246.9, 293.7, 392.0], [164.8, 196.0, 246.9, 329.6], [130.8, 164.8, 196.0, 261.6], [146.8, 185.0, 220.0, 293.7]]
cache = {}
mus = np.zeros(N)
nb = int(E.TOTAL / (beat / 2)) + 2
for k in range(nb):
    ch = prog[(k // 16) % 4]; f = ch[[0, 2, 1, 3, 2, 1, 3, 2][k % 8]]
    if f not in cache: cache[f] = pluck(f)
    s = cache[f]; i0 = int(k * beat / 2 * SR); e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0] * (1.0 if k % 2 == 0 else 0.7)
for k in range(int(E.TOTAL / (beat * 8)) + 1):
    ch = prog[k % 4]; i0 = int(k * beat * 8 * SR); x = tt(beat * 8)
    s = sum(np.sin(2 * np.pi * f / 2 * x) for f in ch[:3]) * 0.04 * np.minimum(1, x / 0.8) * np.minimum(1, (beat * 8 - x) / 0.8)
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
for k in range(int(E.TOTAL / beat) + 1):
    i0 = int(k * beat * SR); x = tt(0.2)
    s = np.sin(2 * np.pi * (50 + 60 * np.exp(-x * 25)) * x) * np.exp(-x * 14) * (0.25 if k % 2 == 0 else 0)
    s += np.convolve(rng.normal(0, 1, len(x)), np.ones(6) / 6, "same") * np.exp(-x * 50) * 0.05
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
t = np.arange(N) / SR
mus *= np.minimum(1, t / 1.0) * np.clip((E.TOTAL - t) / 2.5, 0, 1)
sf.write("music.wav", mus / np.abs(mus).max() * 0.7, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]lowpass=f=6000,volume=0.22[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=6:attack=10:release=400[md];"
                "[2:a]lowpass=f=6500,volume=0.6[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix", E.TOTAL)
