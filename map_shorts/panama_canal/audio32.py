import os, subprocess
import numpy as np, soundfile as sf
import engine32 as E
SR = 44100
N = int(E.TOTAL * SR) + SR
rng = np.random.default_rng(7)
def tt(d): return np.arange(int(d * SR)) / SR
def place(buf, s, t, g=1.0):
    i = int(t * SR)
    if i < 0: s = s[-i:]; i = 0
    if i < N: e = min(N, i + len(s)); buf[i:e] += s[:e - i] * g

# ---- voice: split the Lumean take per line and shift each line by its chapter offset
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
a, _ = sf.read("voice_44.wav"); voice = np.zeros(N)
st = E.TM["starts"]
for i in range(E.N):
    s0 = 0 if i == 0 else int((st[i] - 0.12) * SR)
    s1 = len(a) if i == E.N - 1 else int((st[i + 1] - 0.12) * SR)
    seg = a[s0:s1].copy(); f = min(len(seg), 400); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    place(voice, seg, E.LEAD + s0 / SR + E.OFF[i])
sf.write("voice.wav", voice, SR)

# ---- ambience from the Veo clips (their native sound), low under the voice
amb = np.zeros(N)
for t0, t1, i, kind, arg, o in E.TL:
    if kind != "A": continue
    name, s0 = arg; src = f"clips/{name}.mp4"
    if not os.path.exists(src): continue
    w = f"amb_{name}.wav"
    if not os.path.exists(w): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vn", "-ar", str(SR), "-ac", "1", w], check=True)
    x, _ = sf.read(w); x = x[int(s0 * SR):]
    d = int((t1 - t0 + 0.3) * SR); x = x[:d]
    if len(x) < d: x = np.concatenate([x, x[::-1]])[:d]
    f = int(0.25 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    place(amb, x, t0)

# ---- sfx
sfx = np.zeros(N)
def whoosh(d=0.45):
    t = tt(d); x = rng.normal(0, 1, len(t)); f = np.cumsum(np.interp(t, [0, d], [300, 2600])) / SR
    return np.convolve(np.sin(2 * np.pi * f) * x * np.sin(np.pi * t / d) ** 2, np.ones(8) / 8, "same") * 0.3
def hit():
    t = tt(1.2); return (np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 8)) * t) * np.exp(-t * 3.5) * 0.9 + rng.normal(0, 1, len(t)) * np.exp(-t * 25) * 0.25)
def tick():
    t = tt(0.05); return np.sin(2 * np.pi * 2100 * t) * np.exp(-t * 110) * 0.3
def gavel():
    t = tt(0.35); return (np.sin(2 * np.pi * 180 * t) * 0.6 + rng.normal(0, 1, len(t)) * 0.4) * np.exp(-t * 22)
for c in E.CUTS: place(sfx, whoosh(), c - 0.2, 0.3)
for t0, txt, sub, hold, col in E.OV:
    if t0 < 1e8: place(sfx, hit() if "$" in txt else tick(), t0, 0.45 if "$" in txt else 0.8)
for i in range(1, E.N):
    if E.CH[i] != E.CH[i - 1]: place(sfx, hit(), E.SC[i], 0.35)
place(sfx, gavel(), E.WT(17, "auctions") + 0.25, 0.9)
sf.write("sfx.wav", sfx, SR)

# ---- music: slow cinematic documentary bed (pads + pulse), 84 bpm, builds per chapter
t = np.arange(N) / SR; beat = 60 / 84; mus = np.zeros(N)
prog = [[146.8, 174.6, 220.0], [116.5, 146.8, 174.6], [130.8, 164.8, 196.0], [110.0, 138.6, 164.8]]
bar = beat * 4
for k in range(int(E.TOTAL / bar) + 1):
    i0 = int(k * bar * SR); x = tt(bar * 1.3); ch = prog[k % 4]
    s = sum(np.sin(2 * np.pi * f * x + 0.3 * np.sin(2 * np.pi * 0.2 * x)) + 0.4 * np.sin(2 * np.pi * f * 2.003 * x) for f in ch) * 0.05
    s *= np.minimum(1, x / 0.8) * np.exp(-np.maximum(0, x - bar) * 3)
    s += np.sin(2 * np.pi * ch[0] / 2 * x) * 0.10 * np.exp(-x / 2.5)
    e = min(N, i0 + len(s)); mus[i0:e] += s[:e - i0]
inten = np.ones(N) * 0.55
for i in range(E.N):
    if E.CH[i] in ("hook", "money", "drought", "locks_up"): inten[int(E.SC[i] * SR):int(E.SC[i + 1] * SR)] = 1.0
for k in range(int(E.TOTAL / (beat / 2)) + 1):
    i0 = int(k * beat / 2 * SR); x = tt(0.2); ch = prog[(k // 8) % 4]
    s = np.sin(2 * np.pi * ch[k % 3] * 2 * x) * np.exp(-x * 18) * 0.05
    if k % 2 == 0: s += np.sin(2 * np.pi * (45 + 60 * np.exp(-x * 30)) * x) * np.exp(-x * 14) * 0.28
    e = min(N, i0 + len(s)); mus[i0:e] += s[:e - i0] * inten[min(i0, N - 1)]
sm = np.convolve(inten, np.ones(SR) / SR, "same")
mus *= (0.6 + 0.4 * sm) * np.minimum(1, t / 0.5) * np.clip((E.TOTAL + 0.2 - t) / 2.5, 0, 1)
sf.write("music.wav", mus / np.abs(mus).max() * 0.7, SR)
sf.write("amb.wav", amb / max(1e-6, np.abs(amb).max()) * 0.7, SR)

subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice.wav", "-i", "music.wav", "-i", "sfx.wav", "-i", "amb.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.26[m];[3:a]volume=0.22[am];[m][am]amix=inputs=2:normalize=0[bed];"
                "[bed][vsc]sidechaincompress=threshold=0.05:ratio=8:attack=8:release=350[bd];"
                "[2:a]lowpass=f=6000,volume=0.6[s];[v][bd][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix", E.TOTAL)
