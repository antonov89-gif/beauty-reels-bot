"""Ep.1 sound bed v2 (30.10.2026), own synthesis, no samples, no music. v1 was ONE stationary hiss + sparse rustles (owner: "звук постоянно один и тот же").
v2 is built so that nothing stays the same:
 - air: 4 bands with independent random gains (+-9 dB, 0.8-2.5 s, no steady hum band) so the tone breathes; the colour differs per scene;
 - people: a crowd of synthetic voices (pulse train through vowel formants, syllables, phrases, pauses), unintelligible, in a palace reverb;
 - events: a library of different sounds (silk, wool, footsteps with heel click, door creak + latch, wood creak, ring clink, powder puff, wig set-down, cloth swish, fire crackle, far birds)
   placed (a) on the real motion peaks of each clip, (b) at hand-set story moments, (c) at random times by a per-clip event list, never on top of speech;
 - every clip has its own event mix and density; events are ducked 9 dB under speech; reverb on murmur and (partly) on events.
v3 (30.10, owner: "в референсе звуки от телефона, у нас этого нет"; reference audio measured, sound_reference_vlog1.md):
 - the phone is heard: a low handling rumble that rises with the real camera speed, grip rubs and knocks on the phone body on camera jerks and at pick-ups (dry, at the mic, not ducked);
 - the voice goes through a phone-mic chain: low cut, darker top, proximity (closer = more bass, louder, drier; farther = thinner, quieter, more room), distance from per-clip keyframes plus the measured zoom of the picture;
 - the air is low-frequency (the reference quiet floor has its centre at 170-620 Hz), the old hiss is gone.
Reference level: pause floor about -49 dB RMS (Vlog 1 measured), no silence >= 0.5 s at -50 dB. Usage: python3 build_bed.py"""
import subprocess, numpy as np, cv2
from scipy.signal import butter, sosfilt
SR = 48000
F = "frames/"
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
CLIPS = [("C01", "C01_final_v4", "A"), ("C02", "C02_final", "A"), ("C03", "C03_final", "A"), ("C04", "C04_final", "B"),
         ("C05", "C05_final_jumpcut", "B"), ("C06", "C06_final", "B"), ("C07", "C07_final", "C"), ("C08", "C08_final_lcut", "C")]
# scene: air level dB, band colour offsets dB (30-150, 150-600, 600-2500, 2500-7000), crowd voices, crowd level dB, reverb RT s
SCENE = {"A": dict(air=-50.5, col=(4, 1, -9, -22), voices=3, crowd=-57, rt=1.3, seed=11),
         "B": dict(air=-51, col=(3, 2, -9, -22), voices=0, crowd=-99, rt=0.8, seed=22),
         "C": dict(air=-50, col=(3, 3, -7, -18), voices=8, crowd=-50, rt=1.6, seed=33)}
# per clip: ambient event rate per second and weights of kinds; motion events use `motion` kinds
CLIP = {"C01": dict(rate=1.0, kinds={"bird": 3, "crackle": 4, "silk": 2, "creak": 1}, motion=["silk"], gain=0),
        "C02": dict(rate=1.6, kinds={"silk": 3, "shuffle": 3, "clink": 1, "creak": 1, "crackle": 2, "cough": 1}, motion=["silk", "clink"], gain=0),
        "C03": dict(rate=1.5, kinds={"shuffle": 3, "silk": 2, "creak": 2, "crackle": 2, "tools": 2}, motion=["silk", "silk", "creak"], gain=0),
        "C04": dict(rate=1.3, kinds={"crackle": 4, "wood": 2, "silk": 2, "creak": 1, "bird": 1}, motion=["wood", "wool", "silk"], gain=-1),
        "C05": dict(rate=1.0, kinds={"crackle": 3, "wool": 3, "silk": 2}, motion=["wool", "hair"], gain=-3),
        "C06": dict(rate=1.5, kinds={"crackle": 3, "hair": 3, "wool": 2, "clink": 1, "puff": 2}, motion=["hair", "puff", "wool", "clink"], gain=0),
        "C07": dict(rate=2.2, kinds={"step": 5, "silk": 3, "clink": 2, "creak": 2, "shuffle": 3, "door": 0}, motion=["silk", "step", "clink"], gain=0),
        "C08": dict(rate=2.0, kinds={"swish": 4, "creak": 3, "step": 2, "silk": 2, "clink": 1, "shuffle": 2}, motion=["swish", "silk", "creak"], gain=0)}
# phone-to-mouth distance 0 = close selfie, 1 = far (propped on the table / pointing away); the measured zoom of the picture moves it further
DIST = {"C01": [(0, .75), (1.6, .75), (2.4, .1)], "C02": [(0, .1)], "C03": [(0, .15)], "C04": [(0, .8)], "C05": [(0, .5)],
        "C06": [(0, .7), (1.4, .7), (3.0, .15)], "C07": [(0, .2)], "C08": [(0, .25)]}
# handling: (clip, time, kind, level dB) at the mic; plus automatic ones on camera jerks
HANDLE = [("C01", 0.15, "grip", -27), ("C01", 0.9, "bump", -26), ("C01", 1.7, "grip", -26), ("C01", 2.8, "bump", -24),
          ("C02", 2.2, "grip", -29), ("C02", 6.6, "grip", -31), ("C03", 0.85, "grip", -29), ("C03", 6.3, "bump", -31),
          ("C04", 0.05, "bump", -30), ("C06", 1.45, "grip", -24), ("C06", 1.55, "bump", -23), ("C06", 2.3, "grip", -27),
          ("C07", 0.1, "grip", -27), ("C07", 1.25, "bump", -24), ("C07", 5.6, "grip", -26), ("C08", 0.4, "grip", -27), ("C08", 2.7, "grip", -27)]
# hand-set story moments: (clip, time s, kind, level dB, pan)
STORY = [("C03", 0.9, "silk", -32, 0.1), ("C03", 1.5, "silk", -31, 0.3), ("C04", 4.6, "wood", -29, 0.0), ("C06", 5.4, "puff", -30, 0.0),
         ("C07", 0.2, "door", -31, 0.7), ("C07", 0.6, "step", -34, 0.6), ("C07", 0.9, "step", -33, -0.5), ("C07", 1.2, "step", -34, 0.4), ("C07", 1.5, "step", -33, -0.7),
         ("C07", 1.8, "step", -35, 0.2), ("C07", 2.1, "step", -34, -0.2), ("C07", 6.95, "wig", -30, 0.0),
         ("C08", 0.7, "swish", -33, -0.6), ("C08", 1.15, "swish", -32, 0.5), ("C08", 1.6, "creak", -33, 0.7), ("C08", 2.1, "swish", -34, -0.3)]
rng = np.random.default_rng(2026)


def pcm(p, ch=1):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vn", "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)


def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def db(x): return 10 ** (x / 20)


def motion(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", "fps=24,scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 96, 54).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)); return np.convolve(d, np.ones(3) / 3, "same")


def bandnoise(n, lo, hi, tilt, r):
    X = np.fft.rfft(r.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); f[0] = 1
    X *= f ** (-tilt / 2) * ((f > lo) & (f < hi)); y = np.fft.irfft(X, n); return y / (y.std() + 1e-9)


def slow(n, lo_s, hi_s, depth_db, r):                                   # random slow gain curve in dB -> linear
    pts = [0]
    while pts[-1] < n: pts.append(pts[-1] + int(SR * r.uniform(lo_s, hi_s)))
    v = r.uniform(-depth_db, depth_db, len(pts)); x = np.interp(np.arange(n), pts, v)
    return 10 ** (np.convolve(x, np.ones(2401) / 2401, "same") / 20)


def air(n, sc, ch):
    p = SCENE[sc]; r = np.random.default_rng(p["seed"] * 10 + ch); y = np.zeros(n)
    for (lo, hi, w), c in zip(((60, 200, 0.8), (200, 700, 1.0), (700, 2500, 0.9), (2500, 7000, 0.5)), p["col"]):
        y += bandnoise(n, lo, hi, 1.0, r) * w * db(c) * slow(n, 0.8, 2.5, 9, r)
    return (y / y.std() * db(p["air"])).astype(np.float32)


def make_ir(rt, seed):
    r = np.random.default_rng(seed); n = int(SR * min(rt * 1.1, 2.0)); t = np.arange(n) / SR
    ir = bandnoise(n, 120, 9000, 0.6, r) * np.exp(-6.9 * t / rt) * (1 + 3 * np.exp(-t * 40)); ir[:int(SR * 0.012)] *= np.linspace(0, 1, int(SR * 0.012))
    return (ir / np.sqrt((ir ** 2).sum())).astype(np.float32)


def reverb(x, ir): 
    n = len(x) + len(ir); X = np.fft.rfft(x, n) * np.fft.rfft(ir, n); return np.fft.irfft(X, n)[:len(x)].astype(np.float32)


VOWELS = [(700, 1100, 2500), (500, 1700, 2500), (300, 2200, 3000), (400, 800, 2400), (350, 1100, 2500)]


def voice_syll(n, f0, vow, r):                                          # one syllable: pulse train through 3 formants, unintelligible by design
    ph = np.cumsum(np.linspace(f0, f0 * r.uniform(.88, 1.12), n) / SR); pulses = (np.diff(np.floor(ph), prepend=0) > 0).astype(np.float64)
    X = np.fft.rfft(pulses); f = np.fft.rfftfreq(n, 1 / SR); g = sum(np.exp(-0.5 * ((np.log(f + 1) - np.log(c)) / 0.18) ** 2) * a for c, a in zip(vow, (1, .6, .3)))
    y = np.fft.irfft(X * g, n); w = np.hanning(n) ** 1.5; return (y * w / (np.abs(y).max() + 1e-9)).astype(np.float32)


def crowd(n, sc, ch):
    p = SCENE[sc]; out = np.zeros(n, np.float32)
    for v in range(p["voices"]):
        r = np.random.default_rng(p["seed"] * 1000 + v * 7 + ch * 131); f0 = r.uniform(95, 230); t = r.uniform(0, 3)
        while t < n / SR - 0.4:
            for _ in range(r.integers(3, 8)):                            # a phrase of syllables
                L = int(SR * r.uniform(.12, .26)); i = int(t * SR)
                if i + L >= n: break
                out[i:i + L] += voice_syll(L, f0 * r.uniform(.9, 1.1), VOWELS[r.integers(len(VOWELS))], r) * r.uniform(.4, 1); t += L / SR + r.uniform(.02, .08)
            t += r.uniform(.8, 3.5) * (1 + 6 / (p["voices"] + 1))        # pause: more voices -> denser talk
    return out


def env_exp(n, a, k): t = np.arange(n) / n; return np.minimum(t / a, 1) * np.exp(-k * t)


def ev_silk(r):  n = int(SR * r.uniform(.18, .42)); return bandnoise(n, 1500, 9000, 0.2, r) * env_exp(n, .08, 4) * (0.5 + 0.5 * np.abs(np.sin(r.uniform(5, 11) * np.pi * np.arange(n) / n)))
def ev_wool(r):  n = int(SR * r.uniform(.3, .6)); return bandnoise(n, 200, 2500, 0.5, r) * env_exp(n, .15, 3.5) * (0.6 + 0.4 * np.abs(np.sin(r.uniform(3, 7) * np.pi * np.arange(n) / n)))
def ev_swish(r): n = int(SR * r.uniform(.45, .8)); return bandnoise(n, 300, 4500, 0.4, r) * env_exp(n, .3, 3.0)
def ev_hair(r):  n = int(SR * r.uniform(.25, .5)); return bandnoise(n, 3000, 12000, 0.0, r) * env_exp(n, .05, 5) * (0.5 + 0.5 * np.abs(np.sin(r.uniform(12, 24) * np.pi * np.arange(n) / n)))
def ev_puff(r):  n = int(SR * .22); return bandnoise(n, 150, 3500, 0.8, r) * env_exp(n, .3, 5)


def ev_step(r):
    n = int(SR * .26); t = np.arange(n) / SR; f = r.uniform(70, 120)
    y = np.sin(2 * np.pi * f * t) * np.exp(-t * 26) + 0.5 * bandnoise(n, 600, 3500, 0.2, r) * np.exp(-t * 55)
    c = int(SR * r.uniform(.03, .05)); y[c:c + 90] += bandnoise(90, 2500, 7000, 0, r) * 0.5 * np.hanning(90)        # heel click
    return y


def ev_shuffle(r): n = int(SR * r.uniform(.2, .4)); return bandnoise(n, 250, 3000, 0.3, r) * env_exp(n, .2, 4) * 0.7
def ev_wood(r):    n = int(SR * .3); t = np.arange(n) / SR; return np.sin(2 * np.pi * r.uniform(180, 260) * t) * np.exp(-t * 30) + 0.6 * bandnoise(n, 800, 4000, 0.2, r) * np.exp(-t * 70)
def ev_wig(r):                                                          # a tap on the wig: hair rustle plus a soft knock
    h = ev_hair(r) * 0.8; k = ev_wood(r) * 0.5; y = np.zeros(max(len(h), len(k))); y[:len(h)] += h; y[:len(k)] += k; return y


def ev_creak(r):                                                        # swept resonance: wood or leather
    n = int(SR * r.uniform(.35, .7)); t = np.arange(n) / SR; f = np.linspace(r.uniform(250, 500), r.uniform(500, 1000), n) * (1 + 0.04 * np.sin(2 * np.pi * r.uniform(25, 45) * t))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.4 + bandnoise(n, 300, 2500, 0.3, r) * 0.6; return y * np.sin(np.pi * np.arange(n) / n) ** 1.5 * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * r.uniform(30, 60) * t)))


def ev_door(r):
    c = ev_creak(r); n = int(SR * 1.0); y = np.zeros(n); y[:len(c)] = c[:n] * 0.9; k = int(SR * .78); t = np.arange(int(SR * .15)) / SR
    y[k:k + len(t)] += (np.sin(2 * np.pi * 160 * t) * np.exp(-t * 35) + 0.7 * bandnoise(len(t), 1000, 6000, 0, r) * np.exp(-t * 90))[:n - k]; return y


def ev_clink(r):
    n = int(SR * .2); t = np.arange(n) / SR; fs = r.uniform(.9, 1.15)
    return sum(np.sin(2 * np.pi * f * fs * t) * np.exp(-t * d) for f, d in ((3100, 36), (4730, 52), (6890, 75))) / 3


def ev_tools(r):                                                        # a little metal case set down: two clinks and a knock
    a = ev_clink(r); k = ev_wood(r)[:int(SR * .1)]; y = np.zeros(int(SR * .5)); y[:len(a)] += a; y[int(SR * .22):int(SR * .22) + len(k)] += k * .8; return y


def ev_crackle(r):                                                      # fire: a few tiny pops
    n = int(SR * r.uniform(.12, .5)); y = np.zeros(n)
    for _ in range(r.integers(1, 5)):
        i = r.integers(0, max(1, n - 200)); y[i:i + 120] += bandnoise(120, 1200, 8000, 0, r) * np.exp(-np.arange(120) / 25) * r.uniform(.2, 1)
    return y


def ev_cough(r):                                                        # a distant courtier clearing his throat: short burst, low voice
    n = int(SR * .22); return voice_syll(n, 110, (600, 1000, 2400), r) * 0.7 + bandnoise(n, 800, 3000, 0.3, r) * env_exp(n, .1, 8) * 0.5


def ev_bird(r):                                                         # far, outside the window: short FM whistles
    out = np.zeros(int(SR * r.uniform(.5, 1.0))); t0 = 0
    for _ in range(r.integers(2, 5)):
        n = int(SR * r.uniform(.05, .11)); t = np.arange(n) / SR; f = r.uniform(2800, 4600) * (1 + r.uniform(-.2, .3) * np.linspace(0, 1, n))
        if t0 + n >= len(out): break
        out[t0:t0 + n] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.hanning(n); t0 += n + int(SR * r.uniform(.04, .12))
    return out


def ev_grip(r):                                                         # fingers sliding / re-gripping the phone body, heard through the mic
    n = int(SR * r.uniform(.25, .7)); y = bandnoise(n, 60, 1400, 1.2, r); grain = np.abs(bandnoise(n, 15, 80, 0, r)); return y * grain * env_exp(n, .2, 2.5)


def ev_bump(r):                                                         # a knock on the phone body: low thump + short mid knock
    n = int(SR * .2); t = np.arange(n) / SR; return np.sin(2 * np.pi * r.uniform(55, 110) * t) * np.exp(-t * 32) + 0.5 * bandnoise(n, 300, 2000, 0.5, r) * np.exp(-t * 90)


EV = {k[3:]: v for k, v in globals().items() if k.startswith("ev_")}
LEVEL = dict(grip=-28, bump=-26, silk=-39, wool=-37, swish=-36, hair=-41, puff=-33, step=-34, shuffle=-39, wood=-33, wig=-31, creak=-39, door=-33, clink=-43, tools=-38, crackle=-40, cough=-44, bird=-47)
WET = dict(grip=0, bump=0, bird=.9, door=.5, step=.45, creak=.4, cough=.8, shuffle=.4, tools=.4)


def place(buf, ev, t, pan, wet, ir):
    if len(ev) == 0 or t < 0: return
    i = int(t * SR); w = reverb(np.pad(ev, (0, len(ir))), ir) if wet > 0 else None
    for ch, g in ((0, (1 - pan) ** .5), (1, (1 + pan) ** .5)):
        d = ev * (1 - wet * .6) * g
        if w is not None: d = np.pad(d, (0, len(w) - len(d))) + w * wet * g * .8
        k = min(len(d), buf.shape[1] - i)
        if k > 0: buf[ch, i:i + k] += d[:k]


def add_event(buf, kind, t, lvl, pan, ir, r):
    ev = EV[kind](r); ev = ev / (np.abs(ev).max() + 1e-9) * db(lvl + 4); place(buf, ev.astype(np.float32), t, pan, WET.get(kind, .15), ir)


def speech_duck(voice, n):                                              # 1 = no speech, 0.35 = under speech (-9 dB)
    fr = int(SR * .05); e = np.array([np.sqrt((voice[i:i + fr] ** 2).mean()) for i in range(0, len(voice) - fr, fr)]); a = (e > 0.02).astype(np.float32)
    a = np.convolve(a, np.ones(7) / 7, "same"); g = np.interp(np.arange(n) / fr, np.arange(len(a)), 1 - 0.65 * a); return g.astype(np.float32)


def clip_events(cid, path, d, voice, ir, buf, duck):
    r = np.random.default_rng(sum(map(ord, cid)) * 17)
    cfg = CLIP[cid]; m = motion(path); thr = m.mean() + 0.8 * m.std(); last = -9; nm = nr = ns = 0
    for i in range(1, len(m) - 1):                                      # (a) on real motion peaks
        if m[i] > thr and m[i] >= m[i - 1] and m[i] >= m[i + 1] and i / 24 - last > 0.4:
            last = i / 24; k = cfg["motion"][r.integers(len(cfg["motion"]))]; amp = min(1, m[i] / (thr * 2)); add_event(buf, k, i / 24, LEVEL[k] + 7 * (amp - 1) + 5 + cfg["gain"], r.uniform(-.6, .6), ir, r); nm += 1
    for c, t, k, lv, pan in STORY:                                      # (b) story moments
        if c == cid: add_event(buf, k, t, lv + cfg["gain"], pan, ir, r); ns += 1
    kinds = list(cfg["kinds"]); w = np.array([cfg["kinds"][k] for k in kinds], float); w /= w.sum(); t = r.uniform(.2, .7)
    while t < d - .3:                                                   # (c) random ambient list, Poisson-ish, never the same twice in a row
        k = kinds[r.choice(len(kinds), p=w)]; gi = min(len(duck) - 1, int(t * SR))
        if duck[gi] > 0.9: add_event(buf, k, t, LEVEL[k] + r.uniform(-3, 3) + cfg["gain"], r.uniform(-.8, .8), ir, r); nr += 1
        t += r.exponential(1 / cfg["rate"]) + .15
    return nm, ns, nr


def camera(p):                                                          # per frame: camera speed (frame widths per frame) and cumulative log zoom
    cap = cv2.VideoCapture(p); orb = cv2.ORB_create(800); bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True); prev = None; sp = [0.0]; ls = [0.0]
    while True:
        ok, fr = cap.read()
        if not ok: break
        g = cv2.cvtColor(cv2.resize(fr, (180, 320)), cv2.COLOR_BGR2GRAY)
        if prev is not None:
            v, sc = 0.05, 1.0                                           # no features = lens covered or a fast blur
            k1, d1 = orb.detectAndCompute(prev, None); k2, d2 = orb.detectAndCompute(g, None)
            if d1 is not None and d2 is not None and len(k1) > 15 and len(k2) > 15:
                m = bf.match(d1, d2)
                if len(m) >= 10:
                    p1 = np.float32([k1[x.queryIdx].pt for x in m]); p2 = np.float32([k2[x.trainIdx].pt for x in m])
                    M, inl = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=3)
                    if M is not None and inl is not None and inl.sum() >= 8: v = float(np.hypot(M[0, 2], M[1, 2])) / 180; sc = float(np.hypot(M[0, 0], M[1, 0]))
            sp.append(v); ls.append(ls[-1] + np.log(max(.9, min(1.1, sc))))
        prev = g
    return np.convolve(np.array(sp), np.ones(5) / 5, "same"), np.array(ls)


def per_sample(curve, L): return np.interp(np.arange(L) / SR, np.arange(len(curve)) / 24, curve).astype(np.float32)


def phone_voice(v, dist, ir):                                           # phone-mic chain with proximity; dist 0..1 per sample
    hp = sosfilt(butter(2, 110, "hp", fs=SR, output="sos"), v); lo = sosfilt(butter(2, 300, "lp", fs=SR, output="sos"), hp); hi = sosfilt(butter(2, 3500, "hp", fs=SR, output="sos"), hp)
    y = hp + lo * (0.9 * (1 - dist) - 0.4 * dist) - hi * 0.5            # close: proximity bass; far: thinner; always a darker top than a studio mic (reference tilt -8.4 dB/oct)
    y = sosfilt(butter(2, 8000, "lp", fs=SR, output="sos"), y)
    return (y * 10 ** (-9 * dist / 20) + reverb(y.astype(np.float32), ir) * (0.12 + 0.3 * dist)).astype(np.float32)   # far = quieter and roomier (reference word level range 13.8 dB)


def handling(cid, d, speed, ir, r):                                     # rumble that follows the camera speed + grips/knocks on jerks and hand-set moments
    L = int(SR * d); buf = np.zeros((2, L + SR * 2), np.float32); n = 0
    sp = per_sample(speed, L); g = 10 ** ((-58 + 18 * np.clip(sp / 0.03, 0, 1)) / 20); g = np.convolve(g, np.ones(2400) / 2400, "same")
    for ch in range(2): buf[ch, :L] += bandnoise(L, 30, 600, 1.5, np.random.default_rng(sum(map(ord, cid)) + ch)) * g
    for c, t, k, lv in HANDLE:
        if c == cid: add_event(buf, k, t, lv - 4, r.uniform(-.2, .2), ir, r); n += 1
    last = -9
    for i in range(2, len(speed) - 2):                                  # automatic: speed peaks (jerks) above 0.012 frame widths per frame
        if speed[i] > 0.012 and speed[i] == speed[max(0, i - 12):i + 12].max() and i / 24 - last > 0.6 and not any(c == cid and abs(t - i / 24) < .4 for c, t, _, _ in HANDLE):
            last = i / 24; k = "bump" if speed[i] > 0.025 else "grip"; add_event(buf, k, i / 24, LEVEL[k] - 4 + r.uniform(-2, 2), r.uniform(-.2, .2), ir, r); n += 1
    return buf[:, :L], n


def main():
    order = []
    for cid, src, sc in CLIPS: p = F + src + ".mp4"; order.append((cid, p, sc, dur(p)))
    scenes = {}
    for cid, p, sc, d in order: scenes.setdefault(sc, []).append((cid, p, d))
    for sc, items in scenes.items():
        total = sum(d for _, _, d in items) + 1.0; n = int(SR * total); P = SCENE[sc]; ir = make_ir(P["rt"], P["seed"])
        bed = np.zeros((2, n), np.float32)
        for ch in range(2):
            bed[ch] = air(n, sc, ch)
            if P["voices"]: cr = reverb(crowd(n, sc, ch), ir); bed[ch] += cr * db(P["crowd"]) / (np.sqrt((cr ** 2).mean()) + 1e-9)   # crowd RMS = P["crowd"] dB
        evb = np.zeros((2, n + SR * 3), np.float32); t0 = 0.0; offs = []
        for cid, p, d in items:
            voice = pcm(p); tmp = np.zeros((2, int(SR * (d + 2.5))), np.float32); L = int(SR * d); vv = np.zeros(L, np.float32); vv[:min(L, len(voice))] = voice[:L]; duck = speech_duck(vv, L); nm, ns, nr = clip_events(cid, p, d, voice, ir, tmp, duck)
            L = int(SR * d); g = np.ones(L, np.float32); vv = np.zeros(L, np.float32); vv[:min(L, len(voice))] = voice[:L]; g = speech_duck(vv, L)
            tmp[:, :L] *= g[None, :]; s = int(SR * t0); evb[:, s:s + tmp.shape[1]] += tmp; offs.append((cid, p, d, t0, vv, nm, ns, nr)); t0 += d
        mix_all = bed + evb[:, :n]
        for cid, p, d, t0, vv, nm, ns, nr in offs:
            s = int(SR * t0); L = int(SR * d); seg = mix_all[:, s:s + L].copy(); f = int(SR * .02); seg[:, :f] *= np.linspace(0, 1, f); seg[:, -f:] *= np.linspace(1, 0, f)
            speed, zoom = camera(p); r = np.random.default_rng(sum(map(ord, cid)) * 31)
            key = DIST[cid]; dk = np.interp(np.arange(L) / SR, [k[0] for k in key] + [d + 1], [k[1] for k in key] + [key[-1][1]])
            dist = np.clip(dk - 0.8 * per_sample(zoom, L), 0, 1)
            hb, nh = handling(cid, d, speed, ir, r); seg = seg + hb
            voice_ph = phone_voice(vv, dist, ir)
            mix = np.clip(seg + voice_ph[None, :] * db(-2.6), -.89, .89)
            raw = SC + cid + "_bed.f32"; open(raw, "wb").write(mix.T.astype(np.float32).tobytes()); open(SC + cid + "_bedonly.f32", "wb").write(seg.T.astype(np.float32).tobytes())
            out = F + cid + "_bed.mp4"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", p, "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", out], check=True)
            print(cid, "scene", sc, "dur", round(d, 2), "events: motion", nm, "story", ns, "ambient", nr, "handling", nh, "| distance min/max", round(float(dist.min()), 2), round(float(dist.max()), 2), flush=True)
    ins = sum([["-i", F + c + "_bed.mp4"] for c, _, _ in CLIPS], [])
    fc = "".join(f"[{i}:v]setsar=1[v{i}];" for i in range(len(CLIPS))) + "".join(f"[v{i}][{i}:a]" for i in range(len(CLIPS))) + f"concat=n={len(CLIPS)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "320k", F + "EP1_C01-C08_bed.mp4"], check=True)


main()
