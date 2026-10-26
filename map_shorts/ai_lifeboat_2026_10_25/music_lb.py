"""Own synthwave-style bed for the lifeboat Short (reference DNA: steady electronic bed ~115-120 BPM, persistent bassline, rising pads,
a recurring short sting on every question). Everything is synthesised here; no samples, no third-party melody.
music(total, starts, T) -> mono float array at 44.1 kHz."""
import math
import numpy as np

SR = 44100
BPM = 118
BEAT = 60 / BPM
# A minor: Am - F - C - G (one chord per bar), darker Dm - Am in the 'own child' section
PROG = [(57, 60, 64), (53, 57, 60), (48, 52, 55), (55, 59, 62)]
DARK = [(50, 53, 57), (57, 60, 64)]

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def lowpass(x, cut):
    a = math.exp(-2 * math.pi * cut / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x):
        s = (1 - a) * v + a * s; y[i] = s
    return y

def saw(f, n, ph=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * t + ph) % 1.0) - 1

def env(n, a=0.01, r=0.2):
    e = np.ones(n); ia = max(1, int(a * SR)); ir = max(1, int(r * SR))
    e[:ia] = np.linspace(0, 1, ia); e[-ir:] *= np.linspace(1, 0, ir); return e

def music(total, starts, T, dark=None, stings=None):
    n = int(total * SR) + SR; out = np.zeros(n)
    bar = 4 * BEAT
    child0, child1 = dark or (starts[6], starts[8])  # lifeboat: 'Then I changed one thing' .. 'Two of three changed'
    def chord_at(t):
        if child0 <= t < child1: return DARK[int((t - child0) // bar) % 2]
        return PROG[int(t // bar) % 4]
    # pads: detuned saws, slow attack, low-passed, swell grows over the video
    pad = np.zeros(n); nb = int(total // bar) + 1
    for b in range(nb):
        t0 = b * bar; i0 = int(t0 * SR); m = int(bar * SR)
        if i0 >= n: break
        m = min(m, n - i0); ch = chord_at(t0 + 0.01)
        s = sum(saw(hz(x), m) + saw(hz(x) * 1.004, m, 0.3) for x in ch) / 6
        pad[i0:i0 + m] += s * env(m, 0.35, 0.3)
    pad = lowpass(pad, 900) * 0.20
    # bass: eighth notes on the chord root, plucky filter
    bass = np.zeros(n); step = BEAT / 2; k = 0
    while k * step < total:
        t0 = k * step; i0 = int(t0 * SR); m = int(step * SR * 0.9)
        if i0 + m >= n: break
        r = chord_at(t0)[0] - 24
        s = saw(hz(r), m) * np.exp(-np.arange(m) / SR * 7)
        bass[i0:i0 + m] += s * (1.0 if k % 2 == 0 else 0.75); k += 1
    bass = lowpass(bass, 380) * 0.55
    # arp: 16ths from 4 s, soft square
    arp = np.zeros(n); st = BEAT / 4; k = int(4.0 / st)
    while k * st < total:
        t0 = k * st; i0 = int(t0 * SR); m = int(st * SR * 0.8)
        if i0 + m >= n: break
        ch = chord_at(t0); note = ch[k % 3] + 12 + (12 if (k // 3) % 2 else 0)
        tt = np.arange(m) / SR; s = np.sign(np.sin(2 * math.pi * hz(note) * tt)) * np.exp(-tt * 18)
        arp[i0:i0 + m] += s; k += 1
    arp = lowpass(arp, 2500) * 0.07
    # drums: kick on beats 1 and 3, hats on eighths; drop out for 2 beats before the 'own child' line
    dr = np.zeros(n); rng = np.random.default_rng(3); k = 0
    while k * (BEAT / 2) < total:
        t0 = k * BEAT / 2; i0 = int(t0 * SR)
        drop = child0 - 2 * BEAT <= t0 < child0
        if i0 + 9000 < n and not drop:
            if k % 4 == 0:
                tt = np.arange(9000) / SR; f = 110 * np.exp(-tt * 22) + 42
                dr[i0:i0 + 9000] += np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-tt * 9) * 0.9
            hh = rng.standard_normal(1600) * np.exp(-np.arange(1600) / SR * 90)
            hh = hh - lowpass(hh, 6000)
            dr[i0:i0 + 1600] += hh * (0.16 if k % 2 else 0.10)
        k += 1
    # question sting: own 3-note bell motif (E5, C5, A4) on every question
    sting = np.zeros(n)
    def bell(at):
        for j, m in enumerate((76, 72, 69)):
            i0 = int((at + j * 0.13) * SR); L = int(0.9 * SR)
            if i0 + L >= n: continue
            tt = np.arange(L) / SR
            sting[i0:i0 + L] += (np.sin(2 * math.pi * hz(m) * tt) + 0.4 * np.sin(2 * math.pi * hz(m) * 2.76 * tt)) * np.exp(-tt * 5) * 0.22
    for li, w in (stings or [(1, 9), (3, 13), (6, 9), (8, 9)]):
        bell(starts[li] + T[li][min(w, len(T[li]) - 1)])
    # riser into the own-child line
    rise = np.zeros(n); i0 = int((child0 - 2 * BEAT) * SR); L = int(2 * BEAT * SR)
    tt = np.arange(L) / SR; rise[i0:i0 + L] = lowpass(rng.standard_normal(L), 3000) * (tt / tt[-1]) ** 2 * 0.35
    # intensity curve: quieter intro, full from line 2, peak in the child section, fade at the end
    t = np.arange(n) / SR
    inten = np.clip(0.55 + 0.45 * np.clip((t - starts[1]) / 2, 0, 1), 0, 1) * np.where((t >= child0) & (t < child1), 1.15, 1.0)
    fade = np.clip((total + 0.5 - t) / 2.0, 0, 1)
    return ((pad + bass + arp + dr) * inten + sting + rise) * fade
