import numpy as np, soundfile as sf, subprocess, json
import edit31 as E
SR = 44100; rng = np.random.default_rng(21)
N = int(E.END * SR) + SR
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "vo/lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_raw.wav"], check=True)
v, _ = sf.read("voice_raw.wav")
voice = np.zeros(N)
for i, (st, d) in enumerate(zip(E.VS, E.D)):
    a = max(0, int((st - 0.06) * SR)); b = min(len(v), int((st + d + 0.12) * SR)); seg = v[a:b].copy()
    f = int(0.01 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    o = int((E.ST[i] - 0.06) * SR); voice[o:o + len(seg)] += seg
sf.write("voice31.wav", voice, SR)
sfx = np.zeros(N)
def tt(d): return np.arange(int(d * SR)) / SR
def add(s, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N: e = min(N, i + len(s)); sfx[i:e] += s[:e - i] * g
def ting():
    t = tt(0.8); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((2093, 6), (3136, 8), (4186, 11))) * 0.3
def splash():
    t = tt(0.7); x = rng.normal(0, 1, len(t)); x = np.convolve(x, np.ones(10) / 10, "same"); return x * np.exp(-t * 6) * 0.9 + np.sin(2 * np.pi * 110 * t) * np.exp(-t * 9) * 0.5
def coins(d):
    out = np.zeros(int(d * SR))
    for _ in range(int(d * 28)):
        p = int(rng.random() * max(1, len(out) - 12000)); t = tt(0.25); f = rng.choice([2400, 3100, 3700, 4400])
        out[p:p + len(t)] += np.sin(2 * np.pi * f * t) * np.exp(-t * 28) * rng.uniform(0.05, 0.18)
    return out
def thud():
    t = tt(0.7); return (np.sin(2 * np.pi * (70 - 35 * t) * t) * np.exp(-t * 6) + rng.normal(0, 1, len(t)) * np.exp(-t * 40) * 0.3) * 1.0
def whoosh(d, lo=300, hi=2600):
    t = tt(d); x = rng.normal(0, 1, len(t)); f = np.cumsum(np.interp(t, [0, d], [lo, hi])) / SR
    return np.convolve(np.sin(2 * np.pi * f) * x * np.sin(np.pi * t / d) ** 2, np.ones(6) / 6, "same") * 0.5
def drill(d):
    t = tt(d); return (np.sign(np.sin(2 * np.pi * 85 * t)) * 0.12 + np.sin(2 * np.pi * (330 + 40 * np.sin(t * 7)) * t) * 0.08 + rng.normal(0, 1, len(t)) * 0.05) * np.minimum(1, t / 0.2)
def boing():
    t = tt(0.5); return np.sin(2 * np.pi * np.cumsum(220 + 380 * np.exp(-t * 7) * np.sin(2 * np.pi * 14 * t)) / SR) * np.exp(-t * 6) * 0.4
def tinks(d):
    out = np.zeros(int(d * SR))
    for _ in range(int(d * 40)):
        p = int(rng.random() * max(1, len(out) - 6000)); t = tt(0.12); out[p:p + len(t)] += np.sin(2 * np.pi * rng.choice([2600, 3400, 4200, 5000]) * t) * np.exp(-t * 45) * rng.uniform(0.04, 0.14)
    return out
def flap():
    t = tt(0.6); x = np.convolve(rng.normal(0, 1, len(t)), np.ones(40) / 40, "same"); return x * 6 * (np.sin(2 * np.pi * 14 * t) ** 2) * np.exp(-t * 3) * 0.5
def bonk():
    t = tt(0.4); return np.sin(2 * np.pi * (300 - 160 * t) * t) * np.exp(-t * 9) * 0.7
def sparkle():
    t = tt(0.7); return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * 7) for f in (3520, 4698, 5920)) * 0.14
ST = E.ST
add(ting(), 0.9, 0.9); add(splash(), 4.0, 0.8)
add(coins(ST[2] - ST[1]), ST[1] - 0.1, 0.55); add(whoosh(1.2), ST[1] - 0.15, 0.5)
add(thud(), ST[2] - 0.1, 0.9); add(whoosh(1.4, 200, 1600), ST[3] - 0.3, 0.45)
add(drill(2.6), ST[4] + 0.3, 0.55); add(coins(1.4), ST[4] + 2.3, 0.4)
add(boing(), ST[4] + 4.4, 0.8)
add(tinks(ST[6] - ST[5]), ST[5], 0.5); add(whoosh(1.0), ST[5] - 0.1, 0.4)
add(sparkle(), ST[6] + 0.1, 0.9)
add(flap(), ST[7] + 0.4, 0.9); add(bonk(), ST[7] + 1.5, 0.9)
# music: minimal electronic bed, 96 bpm
t = np.arange(N) / SR; bpm = 96; beat = 60 / bpm; mus = np.zeros(N)
prog = [[220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7], [164.8, 207.7, 246.9]]
for k in range(int(E.END / (beat * 4)) + 1):
    i0 = int(k * beat * 4 * SR); x = tt(beat * 4); ch = prog[k % 4]
    s = sum(np.sin(2 * np.pi * f * x) for f in ch) * 0.05 * np.minimum(1, x / 0.4) * np.exp(-x / 2.5)
    s += np.sin(2 * np.pi * ch[0] / 2 * x) * 0.1 * np.exp(-x / 1.4)
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
for k in range(int(E.END / (beat / 2)) + 1):
    if k % 4 == 3: continue
    i0 = int(k * beat / 2 * SR); x = tt(0.22); ch = prog[(k // 8) % 4]; f = ch[(k % 3)] * 2
    s = np.sin(2 * np.pi * f * x) * np.exp(-x * 14) * 0.06
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
for k in range(int(E.END / beat) + 1):
    i0 = int(k * beat * SR); x = tt(0.2)
    s = np.sin(2 * np.pi * (52 + 60 * np.exp(-x * 28)) * x) * np.exp(-x * 14) * 0.3
    e2 = min(N, i0 + len(s)); mus[i0:e2] += s[:e2 - i0]
mus *= np.minimum(1, t / 0.5) * np.clip((E.END + 0.2 - t) / 1.2, 0, 1)
sf.write("music31.wav", mus / np.abs(mus).max() * 0.7, SR); sf.write("sfx31.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice31.wav", "-i", "music31.wav", "-i", "sfx31.wav", "-filter_complex",
    "[0:a]asplit=2[v][vsc];[1:a]volume=0.30[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=9:attack=8:release=320[md];"
    "[2:a]lowpass=f=6500,volume=0.55[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
    "-map", "[a]", "-t", str(E.END), "mix31.wav"], check=True)
print("mix", round(E.END, 2))
