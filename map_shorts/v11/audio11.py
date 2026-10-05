import numpy as np, soundfile as sf, subprocess, json
import engine11 as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(1)

def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / r)

def whoosh(d=0.45):
    n = int(d * SR); x = rng.normal(0, 1, n)
    t = np.arange(n) / SR
    f = np.cumsum(np.interp(t, [0, d], [300, 3000])) / SR
    bp = np.sin(2 * np.pi * f) * x
    e = np.sin(np.pi * t / d) ** 2
    return np.convolve(bp * e, np.ones(8) / 8, "same") * 0.35

def boom():
    n = int(0.9 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (55 * t + 40 * (1 - np.exp(-t * 8)))) * np.exp(-t * 4)
    s += rng.normal(0, 1, n) * np.exp(-t * 25) * 0.4
    return s * 0.9

def pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (500 + 900 * np.exp(-t * 40)) * t) * np.exp(-t * 35) * 0.5

def tick():
    n = int(0.04 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 2200 * t) * np.exp(-t * 120) * 0.3

def stamp():
    n = int(0.3 * SR); t = np.arange(n) / SR
    return (rng.normal(0, 1, n) * np.exp(-t * 30) * 0.5 + np.sin(2 * np.pi * 90 * t) * np.exp(-t * 12)) * 0.8

def wind(d=3.0):
    n = int(d * SR); x = np.cumsum(rng.normal(0, 1, n)); x -= np.convolve(x, np.ones(2000) / 2000, "same")
    t = np.arange(n) / SR
    return x / np.abs(x).max() * np.minimum(1, t / 1.0) * np.minimum(1, (d - t) / 0.8) * 0.25

sfx = np.zeros(N)
def add(sig, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < N:
        e = min(N, i + len(sig)); sfx[i:e] += sig[: e - i] * g

def riser(d=1.6):
    n = int(d * SR); t = np.arange(n) / SR
    f = 120 + 900 * (t / d) ** 2
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / d) ** 1.5 * 0.35 + rng.normal(0, 1, n) * (t / d) ** 2 * 0.08

for ct in E.CUTS:
    add(whoosh(0.35), ct - 0.15, 0.6)
for i, s in enumerate(E.S):
    if s.get("fly") or s.get("zoomout"):
        add(whoosh(1.2), E.SCENE_T[i], 0.9)
    for f in s["fx"]:
        k = f[0]
        if k in ("big",) and f[2] > 0.2: add(stamp(), f[2], 0.8); add(boom(), f[2], 0.35)
        elif k in ("emoji", "emoji_screen", "badge", "badge_screen") and f[5] > 0.2: add(pop(), f[5], 0.8)
        elif k == "pin" and f[4] > 0.2: add(pop(), f[4], 0.8)
        elif k == "hl" and f[3] > 0.2: add(pop() * 0.5, f[3], 0.5)
        elif k == "ring_emoji":
            for tt in f[4]: add(pop(), tt, 0.8)
        elif k == "count":
            for j in range(12): add(tick(), f[4] + j * f[5] / 12, 0.8)
            add(stamp(), f[4] + f[5], 0.6)
        elif k == "walker":
            for j in range(10): add(tick(), f[1] + j * 0.22, 0.6)
        elif k == "progress": add(whoosh(0.5), f[1], 0.6)
        elif k in ("park", "cube_fp") and f[1] > 0.2: add(stamp(), f[1], 0.6)
# diagram scenes
for j in range(4): add(pop(), E.WT(8, "shoulder") + j * 0.22, 0.9)
add(stamp(), E.WT(8, "four"), 0.8)
add(riser(1.6), E.starts[13] - 0.1, 0.8); add(boom(), E.WT(13, "cubic") - 0.2, 0.6); add(stamp(), E.WT(13, "cubic") - 0.2, 0.7)
for w in ("kilometer", "side"): add(pop(), E.WT(14, w), 0.8)
add(stamp(), E.WT(14, "giant"), 0.7)
for j in range(3): add(pop(), E.starts[16] + 0.2 + j * 0.35, 0.7)
add(riser(1.0), E.WT(16, "fifteen") - 0.1, 0.8); add(boom(), E.WT(16, "fifteen") + 0.6, 0.8)
sf.write("sfx.wav", sfx, SR)

# voice track: one Lumean take placed at LEAD
import subprocess as sp
sp.run(["ffmpeg","-y","-loglevel","error","-i","lumean/result.mp3","-ar",str(SR),"-ac","1","voice_raw.wav"],check=True)
a, sr = sf.read("voice_raw.wav")
voice = np.zeros(N); i0 = int(E.LEAD * SR); e = min(N, i0 + len(a)); voice[i0:e] = a[: e - i0]
sf.write("voice.wav", voice, SR)

# music bed: minor drone + pulse, A minor -> F -> C -> G progression, 100 bpm
t = np.arange(N) / SR
bar = 2.4
roots = [110.0, 87.31, 130.81, 98.0]
mus = np.zeros(N)
for b in range(int(E.TOTAL / bar) + 2):
    r = roots[b % 4]; i0 = int(b * bar * SR); n = int(bar * 1.2 * SR)
    tt = np.arange(n) / SR
    e = np.minimum(1, tt / 0.3) * np.exp(-tt / 3)
    chord = r * np.array([1, 1.189 if b % 4 == 0 else 1.26, 1.498, 2])
    sig = sum(np.sin(2 * np.pi * f * tt) for f in chord) * e * 0.15
    sig += np.sin(2 * np.pi * r / 2 * tt) * e * 0.35
    for p in range(8):  # pulse 8ths
        st = int(p * bar / 8 * SR); m = int(0.18 * SR)
        pt = np.arange(m) / SR
        sig[st:st + m] += (np.sin(2 * np.pi * r * 2 * pt) * np.exp(-pt * 25) * 0.18)[: len(sig[st:st + m])]
    e2 = min(N, i0 + n)
    if e2 > i0: mus[i0:e2] += sig[: e2 - i0]
# kick on beats
beat = 60 / 100
for b in range(int(E.TOTAL / beat)):
    add_t = b * beat; i0 = int(add_t * SR); n = int(0.25 * SR); tt = np.arange(n) / SR
    k = np.sin(2 * np.pi * (50 + 80 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 12) * 0.5
    e2 = min(N, i0 + n)
    if e2 > i0: mus[i0:e2] += k[: e2 - i0]
mus *= np.minimum(1, t / 1.0) * np.minimum(1, (E.TOTAL + 0.5 - t) / 1.5).clip(0)
sf.write("music.wav", mus / np.abs(mus).max() * 0.8, SR)

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav",
  "-filter_complex",
  "[0:a]asplit=2[v][vsc];[1:a]volume=0.34[m];[m][vsc]sidechaincompress=threshold=0.05:ratio=9:attack=8:release=320[md];"
  "[2:a]volume=0.9[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
  "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix done", E.TOTAL)
