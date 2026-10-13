"""Looping pizzicato bed for the 24 s zoom loop (105 bpm, 7 phrases x 6 beats). Renders 3 cycles, keeps the middle one."""
import numpy as np, soundfile as sf, subprocess
import engine29 as E
SR = 44100; rng = np.random.default_rng(7)
C = E.CYCLE; N = int(round(C * SR)); TOT = 3 * N
mix = np.zeros(TOT)
def add(sig, t, g=1.0):
    i = int(t * SR)
    if i < 0 or i >= TOT: return
    e = min(TOT, i + len(sig)); mix[i:e] += sig[:e - i] * g
def pluck(f, dur=0.55, bright=0.5):
    n = int(SR / f); buf = rng.uniform(-1, 1, n); out = np.zeros(int(dur * SR)); dec = 0.996 - 0.004 * (1 - bright)
    for i in range(len(out)):
        out[i] = buf[i % n]; buf[i % n] = dec * 0.5 * (buf[i % n] + buf[(i + 1) % n])
    env = np.exp(-np.arange(len(out)) / SR * 6.5); return out * env
_P = {}
def pl(f, dur=0.5, bright=0.5):
    k = (round(f, 2), dur, bright)
    if k not in _P: _P[k] = pluck(f, dur, bright)
    return _P[k]
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
B = E.BEAT; e8 = B / 2
CH = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62], [60, 64, 67], [53, 57, 60], [55, 59, 62]]
PAT = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 4, 3]
def tone(ch, j):
    seq = [ch[0], ch[1], ch[2], ch[0] + 12, ch[1] + 12]; return seq[j]
def whoosh(d):
    t = np.arange(int(d * SR)) / SR; x = rng.normal(0, 1, len(t))
    x = np.convolve(x, np.ones(24) / 24, "same"); return x * np.sin(np.pi * t / d) ** 3 * 0.5
def bling():
    t = np.arange(int(0.9 * SR)) / SR
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((1568, 5), (2093, 6), (3136, 8))) * 0.18
for cyc in range(3):
    t0 = cyc * C
    for p, ch in enumerate(CH):
        tp = t0 + p * 6 * B
        for j in range(12):
            m = tone(ch, PAT[j]) + 12
            add(pl(hz(m), 0.45, 0.7), tp + j * e8, 0.55 if j % 3 == 0 else 0.38)
        for b in (0, 3):
            add(pl(hz(ch[0] - 24), 0.9, 0.3), tp + b * B, 0.9)
        add(pl(hz(ch[2]), 0.7, 0.6), tp + 4 * B, 0.6); add(pl(hz(ch[0] + 24), 0.6, 0.9), tp + 4 * B, 0.45)   # arrival accent
        add(whoosh(E.MOVE * 0.9), tp + 0.05, 0.22)
        if p in (0, 4, 5, 6): add(bling(), tp + 4 * B, 1.0)   # level switches: coin->map, hatch, porthole, stamp
out = mix[N:2 * N]
i0 = int(E.T0 * SR); out = np.concatenate([out[i0:], out[:i0]])
out = out / np.abs(out).max() * 0.85
sf.write("music_raw.wav", out, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "music_raw.wav", "-af", "highpass=f=60,acompressor=threshold=0.25:ratio=3,volume=1.0", "music.wav"], check=True)
print("ok", len(out) / SR)
