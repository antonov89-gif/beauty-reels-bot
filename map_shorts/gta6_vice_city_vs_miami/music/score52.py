"""Long-form version with sections and breaks. Original 80s-Miami style synthwave bed (own composition, no samples). python3 score.py out.wav seconds"""
import sys, numpy as np, soundfile as sf
SR = 44100; BPM = 104; DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 40
rng = np.random.default_rng(7); N = int(DUR * SR); out = np.zeros((N, 2)); beat = 60 / BPM; step = beat / 4
def place(sig, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or i < 0: return
    e = min(N, i + len(sig)); s = sig[:e - i] * g
    out[i:e, 0] += s * (1 - pan) / 2 * 1.4; out[i:e, 1] += s * (1 + pan) / 2 * 1.4
def tt(d): return np.arange(int(d * SR)) / SR
from scipy.signal import lfilter
def lp(x, a):                      # one-pole low-pass
    return lfilter([a], [1, a - 1], x)
def saw(f, d, det=0.0):
    t = tt(d); return ((2 * ((f * (1 + det)) * t % 1) - 1) + (2 * ((f * (1 - det)) * t % 1) - 1)) / 2
def env(d, a=0.01, r=0.1):
    t = tt(d); return np.minimum(1, t / a) * np.clip((d - t) / r, 0, 1)
def kick():
    t = tt(0.35); return np.sin(2 * np.pi * np.cumsum(48 + 110 * np.exp(-t * 28)) / SR) * np.exp(-t * 9) * 0.9
def snare():
    t = tt(0.4); n = rng.normal(0, 1, len(t)); return (n * np.exp(-t * 14) * 0.5 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 20) * 0.5) * (t < 0.28)
def hat(o=False):
    t = tt(0.25 if o else 0.06); n = rng.normal(0, 1, len(t)); n = n - np.concatenate([[0], n[:-1]]); return n * np.exp(-t * (18 if o else 70)) * 0.22
def tom(f):
    t = tt(0.3); return np.sin(2 * np.pi * np.cumsum(f * (1 + 0.5 * np.exp(-t * 15))) / SR) * np.exp(-t * 9) * 0.5
hz = lambda m: 440 * 2 ** ((m - 69) / 12)
prog = [(57, [60, 64, 69]), (53, [57, 60, 65]), (48, [55, 60, 64]), (55, [59, 62, 67])]   # Am F C G
prog2 = [(53, [57, 60, 65]), (55, [59, 62, 67]), (52, [55, 59, 64]), (57, [60, 64, 69])]  # F G Em Am
import json
BREAKS = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []      # chapter-card times: drums drop, riser in
bars = int(DUR / (beat * 4)) + 1
for b in range(bars):
    t0 = b * beat * 4; root, ch = (prog2 if (b // 16) % 2 else prog)[b % 4]
    brk = any(-beat * 4 < bt - t0 <= beat * 4 for bt in BREAKS)
    # pad
    pad = sum(saw(hz(n), beat * 4, 0.004) for n in ch) * env(beat * 4, 0.6, 0.8) * 0.045
    place(lp(pad, 0.06), t0, 1.0, 0.0)
    # bass (16th pulse)
    for s in range(16):
        n = root - 12 + (0 if s % 4 else 0); d = step * 0.9
        b_ = lp(saw(hz(n), d), 0.12) * env(d, 0.004, 0.05) * 0.55
        if s % 2 == 0 or s in (7, 15): place(b_, t0 + s * step, 1.0)
    # arp
    arp = [ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1], ch[0] + 12, ch[1]]
    for s in range(16):
        n = arp[s % 8] + (12 if (b // 2) % 2 else 0); d = step * 0.8
        a = np.sign(np.sin(2 * np.pi * hz(n) * tt(d))) * env(d, 0.003, 0.08) * 0.05 * np.exp(-tt(d) * 6)
        place(lp(a, 0.5), t0 + s * step, 1.0, -0.5 if s % 2 else 0.5)
    # drums (from bar 2)
    if b >= 1 and not brk:
        for q in range(4):
            place(kick(), t0 + q * beat, 0.8)
            if q in (1, 3): place(snare(), t0 + q * beat, 0.7)
        for s in range(16): place(hat(s % 4 == 2), t0 + s * step, 0.7, 0.3)
        if b % 4 == 3: [place(tom(f), t0 + beat * 3 + k * step, 0.7) for k, f in enumerate((150, 130, 110, 90))]
for bt in BREAKS:
    rt = tt(1.6); place(rng.normal(0, 1, len(rt)) * (rt / 1.6) ** 2 * 0.10, bt - 1.6, 1.0); place(kick() * 1.4, bt, 1.0)
# riser into the end
rt = tt(3.0); rs = rng.normal(0, 1, len(rt)) * (rt / 3.0) ** 2 * 0.12
place(rs, max(0, DUR - 3.2), 1.0)
out *= np.minimum(1, np.arange(N)[:, None] / (0.5 * SR)) * np.clip((N - np.arange(N)[:, None]) / (1.5 * SR), 0, 1)
out /= np.abs(out).max() / 0.8
sf.write(sys.argv[1], out, SR)
