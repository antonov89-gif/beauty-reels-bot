import numpy as np, soundfile as sf, subprocess
import engine26 as E
SR = 44100; N = int(E.TOTAL * SR) + SR; rng = np.random.default_rng(6); sfx = np.zeros(N)
def tt(d): return np.arange(int(d * SR)) / SR
def add(s, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N: e = min(N, i + len(s)); sfx[i:e] += s[:e - i] * g
def whoosh(d=0.35):
    t = tt(d); return np.convolve(rng.normal(0, 1, len(t)), np.ones(70) / 70, "same") * np.sin(np.pi * t / d) ** 2 * 2.0
def click():
    t = tt(0.08); return np.sin(2 * np.pi * 1300 * t) * np.exp(-t * 70) * 0.3
def ching():
    t = tt(0.7); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((1568, 6), (2093, 7), (3136, 9))) * 0.12
def impact():
    t = tt(0.8); return np.sin(2 * np.pi * (50 + 40 * np.exp(-t * 9)) * t) * np.exp(-t * 5) * 0.6
for c, k in E.CUTS[1:]: add(whoosh(), c - 0.15, 0.35)
for i in E.ITEMS: add(click(), E.ST[i] - 0.05, 1.0)
for ta, a in E.ADDS: add(ching(), ta, 0.9)
add(impact(), E.ST[6] - 0.05, 0.9)
sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
v, _ = sf.read("voice_44.wav"); voice = np.zeros(N); i0 = int(E.LEAD * SR); e = min(N, i0 + len(v)); voice[i0:e] = v[:e - i0]; sf.write("voice.wav", voice, SR)
m, _ = sf.read("/home/claude/v25/music.wav"); m = m[int(100 * SR):int(100 * SR) + N]
t = np.arange(len(m)) / SR; m = m * np.minimum(1, t / 0.3) * np.clip((E.TOTAL - t) / 1.2, 0, 1); sf.write("music.wav", m, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.3[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=6:attack=10:release=350[md];"
                "[2:a]lowpass=f=7000,volume=0.7[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("ok", E.TOTAL)
