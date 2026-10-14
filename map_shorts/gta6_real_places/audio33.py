import os, subprocess
import numpy as np, soundfile as sf
import engine33 as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(11)
def tt(d): return np.arange(int(d * SR)) / SR
def place(buf, s, t, g=1.0):
    i = int(t * SR)
    if i < 0: s = s[-i:]; i = 0
    if i < N: e = min(N, i + len(s)); buf[i:e] += s[:e - i] * g
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
a, _ = sf.read("voice_44.wav"); voice = np.zeros(N); place(voice, a, E.LEAD)
sf.write("voice.wav", voice, SR)
# native sound of the AI clips
amb = np.zeros(N)
for t0, t1, i, kind, arg in E.TL:
    if kind != "C": continue
    w = f"amb_{arg}.wav"
    if not os.path.exists(w): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"clips/{arg}.mp4", "-vn", "-ar", str(SR), "-ac", "1", w], check=True)
    x, _ = sf.read(w); d = int((t1 - t0 + 0.25) * SR); x = x[:d].copy()
    f = min(len(x), int(0.15 * SR)); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f); place(amb, x, t0)
amb = amb / max(1e-6, np.abs(amb).max()) * 0.7
# sfx
sfx = np.zeros(N)
def whoosh(d=0.35):
    t = tt(d); x = rng.normal(0, 1, len(t)); f = np.cumsum(np.interp(t, [0, d], [400, 3200])) / SR
    return np.convolve(np.sin(2 * np.pi * f) * x * np.sin(np.pi * t / d) ** 2, np.ones(6) / 6, "same") * 0.35
def hit():
    t = tt(0.9); return np.sin(2 * np.pi * (50 + 55 * np.exp(-t * 9)) * t) * np.exp(-t * 4.5) * 0.9 + rng.normal(0, 1, len(t)) * np.exp(-t * 30) * 0.25
def pop():
    t = tt(0.12); return np.sin(2 * np.pi * (520 + 900 * np.exp(-t * 40)) * t) * np.exp(-t * 35) * 0.45
for c in E.CUTS: place(sfx, whoosh(), c - 0.12, 0.5)
for t0, t1, i, kind, arg in E.TL:
    if kind == "M" and arg != "florida": place(sfx, pop(), t0 + 0.15, 0.7); place(sfx, hit(), t0 + 0.25, 0.4)
for tt_ in (0.6, 1.6, 2.6): place(sfx, pop(), E.SC[1] + tt_ + 0.0, 0.8)
place(sfx, hit(), E.WT(7, "hundred") - 0.1, 0.9)
place(sfx, hit(), 0.05, 0.8)
# music: 112 bpm dark synthwave bed
t = np.arange(N) / SR; beat = 60 / 112; mus = np.zeros(N)
prog = [[110.0, 130.8, 164.8], [87.3, 110.0, 130.8], [98.0, 123.5, 146.8], [82.4, 103.8, 123.5]]
for k in range(int(E.TOTAL / (beat / 2)) + 2):
    i0 = int(k * beat / 2 * SR); x = tt(beat / 2); ch = prog[(k // 16) % 4]; f = ch[k % 3] * 2
    s = (np.sign(np.sin(2 * np.pi * f * x)) * 0.3 + np.sin(2 * np.pi * f * x)) * np.exp(-x * 7) * 0.09
    e = min(N, i0 + len(s)); mus[i0:e] += s[:e - i0]
for k in range(int(E.TOTAL / (beat * 4)) + 1):
    i0 = int(k * beat * 4 * SR); x = tt(beat * 4); ch = prog[k % 4]
    s = sum(np.sin(2 * np.pi * f * x) for f in ch) * 0.05 * np.minimum(1, x / 0.25) * np.exp(-x / 2.5) + np.sin(2 * np.pi * ch[0] / 2 * x) * 0.12 * np.exp(-x / 1.6)
    e = min(N, i0 + len(s)); mus[i0:e] += s[:e - i0]
for k in range(int(E.TOTAL / beat) + 1):
    i0 = int(k * beat * SR); x = tt(0.25)
    s = np.sin(2 * np.pi * (46 + 70 * np.exp(-x * 25)) * x) * np.exp(-x * 13) * 0.5 + rng.normal(0, 1, len(x)) * np.exp(-x * 60) * (0.14 if k % 2 else 0.03)
    e = min(N, i0 + len(s)); mus[i0:e] += s[:e - i0]
mus *= np.minimum(1, t / 0.3) * np.clip((E.TOTAL + 0.2 - t) / 1.5, 0, 1)
sf.write("music.wav", mus / np.abs(mus).max() * 0.7, SR); sf.write("amb.wav", amb, SR); sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-i", "amb.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.28[m];[3:a]volume=0.35[am];[m][am]amix=inputs=2:normalize=0[bed];"
                "[bed][vsc]sidechaincompress=threshold=0.05:ratio=8:attack=8:release=300[bd];"
                "[2:a]lowpass=f=6500,volume=0.6[s];[v][bd][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix", E.TOTAL)
