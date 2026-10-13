import numpy as np, soundfile as sf, subprocess
import engine28 as E
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
def waves(d):
    t = tt(d); x = np.convolve(rng.normal(0, 1, len(t)), np.ones(400) / 400, "same")
    return x * (0.6 + 0.4 * np.sin(2 * np.pi * t / 4.5)) * 6
SC, S = E.SC, E.S
for i in range(1, E.N): add(whoosh(0.5), SC[i] - 0.2, 0.35)
add(riser(2.0), SC[0] + 0.2, 0.5)
for i, (_, sc) in enumerate(S):
    if sc["t"] == "map":
        for q, key in enumerate(sc["mark"]):
            if key in E.P: add(pop(), SC[i] + 0.5 + q * 0.35, 0.8)
        if sc.get("route"): add(riser(1.6), SC[i] + 0.2, 0.35)
    else:
        add(stamp(), SC[i] + 0.4, 0.7)
        for q in range(len(sc.get("lines", []))): add(pop(), SC[i] + 0.4 + q * 0.7, 0.8)
    if "clip" in sc: add(whoosh(0.4), SC[i] + (SC[i + 1] - SC[i]) * sc["clip"][1] - 0.1, 0.4)

EV_POP = [(0, "oil"), (2, "country"), (2, "desert"), (2, "mountains"), (3, "Saudi"), (3, "Iraq"), (3, "Kuwait"), (3, "Qatar"), (3, "Emirates"), (3, "bottle"),
          (7, "China"), (7, "India"), (7, "Japan"), (7, "Korea"), (9, "agree"), (12, "Fujairah"), (13, "bottleneck"), (17, "built"), (20, "food"), (20, "medicine"),
          (20, "cars"), (20, "machines"), (21, "behind"), (23, "Oman"), (23, "Sohar"), (23, "Duqm"), (26, "Industrial"), (28, "not"), (28, "map"), (29, "tunnels"),
          (29, "bridges"), (29, "cuttings"), (30, "Saudi"), (30, "Iran"), (30, "helped"), (32, "weakness"), (32, "missile"), (35, "door")]
EV_SLAM = [(0, "fifth"), (1, "shut"), (5, "few"), (8, "closed"), (9, "ceasefire"), (9, "fighting"), (12, "past"), (15, "2012"), (17, "expected"),
           (21, "biggest"), (26, "two"), (34, "insurance"), (35, "fifth")]
for w in EV_POP:
    try: add(pop(), E.WT(*w), 0.7)
    except KeyError: print("miss", w)
for w in EV_SLAM:
    try: add(stamp(), E.WT(*w), 0.75)
    except KeyError: print("miss", w)
add(whoosh(0.8), E.WT(4, "thirtythree"), 0.5); add(whoosh(1.0), E.WT(14, "crow"), 0.5)
sf.write("sfx.wav", sfx, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "lumean/result.mp3", "-ar", str(SR), "-ac", "1", "voice_44.wav"], check=True)
a, _ = sf.read("voice_44.wav"); v = np.zeros(N); i0 = int(E.LEAD * SR); e = min(N, i0 + len(a)); v[i0:e] = a[:e - i0]
sf.write("voice.wav", v, SR)
# upbeat documentary synth bed, 92 bpm
t = np.arange(N) / SR; beat = 60 / 92; mus = np.zeros(N)
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
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.30[m];[m][vsc]sidechaincompress=threshold=0.05:ratio=9:attack=8:release=320[md];"
                "[2:a]lowpass=f=5500,volume=0.7[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "mix.wav"], check=True)
print("mix", E.TOTAL)
