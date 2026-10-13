"""Looping pizzicato bed: 80 bpm, 8 phrases x 4 beats (move 3 beats + hold 1), 16th-note plucks like a string pizzicato run."""
import numpy as np, soundfile as sf
import engine30 as E
SR = 44100; rng = np.random.default_rng(11)
C = E.CYCLE; N = int(round(C * SR)); TOT = 3 * N
mix = np.zeros(TOT)
def add(sig, t, g=1.0):
    i = int(t * SR)
    if 0 <= i < TOT:
        e = min(TOT, i + len(sig)); mix[i:e] += sig[:e - i] * g
_P = {}
def pluck(f, dur=0.4, bright=0.6):
    k = (round(f, 1), dur, bright)
    if k in _P: return _P[k]
    n = max(2, int(SR / f)); buf = rng.uniform(-1, 1, n); buf = np.convolve(buf, np.ones(2) / 2, "same") if bright < 0.5 else buf
    out = np.zeros(int(dur * SR)); dec = 0.994 + 0.004 * bright
    for i in range(len(out)):
        j = i % n; out[i] = buf[j]; buf[j] = dec * 0.5 * (buf[j] + buf[(j + 1) % n])
    env = np.exp(-np.arange(len(out)) / SR * 9) * np.minimum(1, np.arange(len(out)) / 40)
    _P[k] = out * env; return _P[k]
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)
B = E.BEAT; s16 = B / 4
CH = [[60, 64, 67], [55, 59, 62], [57, 60, 64], [53, 57, 60], [60, 64, 67], [55, 59, 62], [53, 57, 60], [55, 59, 62]]
UP = [0, 1, 2, 3, 4, 3, 2, 1]
def tone(ch, j): return [ch[0], ch[1], ch[2], ch[0] + 12, ch[1] + 12][j]
def swoosh(d):
    t = np.arange(int(d * SR)) / SR; x = np.convolve(rng.normal(0, 1, len(t)), np.ones(30) / 30, "same")
    return x * np.sin(np.pi * t / d) ** 3 * 0.6
def bell():
    t = np.arange(int(1.0 * SR)) / SR
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((1046.5, 4), (1568, 5), (2093, 7))) * 0.14
for cyc in range(3):
    t0 = cyc * C
    for p, ch in enumerate(CH):
        tp = t0 + p * 4 * B
        for j in range(16):
            if j >= 12 and j % 2: continue             # breathe during the hold
            m = tone(ch, UP[j % 8]) + 12
            add(pluck(hz(m), 0.35, 0.7), tp + j * s16, 0.5 if j % 4 == 0 else 0.33)
        add(pluck(hz(ch[0] - 24), 0.9, 0.3), tp, 1.0)
        add(pluck(hz(ch[0] - 12), 0.7, 0.4), tp + 2 * B, 0.6)
        add(pluck(hz(ch[2] + 12), 0.8, 0.9), tp + 3 * B, 0.7); add(pluck(hz(ch[0] + 24), 0.8, 0.9), tp + 3 * B, 0.5)
        add(swoosh(E.MOVE * 0.8), tp + 0.15, 0.18)
        if p in (0, 3, 4, 5, 7): add(bell(), tp + 3 * B, 1.0)       # level changes land on the hold beat
out = mix[N:2 * N]; i0 = int(E.T0 * SR); out = np.concatenate([out[i0:], out[:i0]])
out = np.tanh(out / np.abs(out).max() * 5.0); out = out / np.abs(out).max() * 0.84
sf.write("music.wav", out, SR, subtype="FLOAT"); print("ok")
