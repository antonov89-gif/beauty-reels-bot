"""Audio for engine63 Shorts: synthesised 118 BPM upbeat bed (reference style) + SFX from the overlay timeline + voice.
SHORT=<key> python3 audio63.py  -> <key>/mix.wav   (voice is skipped if <key>/lumean/result.mp3 is missing: preview mode)"""
import os
import subprocess

import numpy as np
import soundfile as sf

import engine63 as V

SR = 44100
N = int(V.TOTAL * SR) + SR
rng = np.random.default_rng(63)
BPM = 118
BEAT = 60 / BPM


def tt(d):
    return np.arange(int(d * SR)) / SR


def place(buf, s, t, g=1.0):
    i = int(t * SR)
    if i < 0:
        s = s[-i:]
        i = 0
    if i < N:
        e = min(N, i + len(s))
        buf[i:e] += s[:e - i] * g


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, "same")


# ------------------------------------------------------------------ instruments
def kick():
    t = tt(0.35)
    return np.sin(2 * np.pi * (45 + 110 * np.exp(-t * 28)) * t) * np.exp(-t * 9) * 0.9


def clap():
    t = tt(0.22)
    return lp(rng.normal(0, 1, len(t)), 3) * (np.exp(-t * 30) + 0.5 * np.exp(-np.maximum(0, t - 0.012) * 30)) * 0.35


def hat(open_=False):
    t = tt(0.18 if open_ else 0.05)
    x = rng.normal(0, 1, len(t))
    x = x - lp(x, 6)
    return x * np.exp(-t * (18 if open_ else 80)) * 0.18


def bass(f, d):
    t = tt(d)
    x = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t)
    return lp(x, 40) * np.minimum(1, t / 0.01) * np.exp(-t * 2.5) * 0.32


def pluck(f, d=0.25):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * f * h * t) / h for h in (1, 2, 3, 4))
    return x * np.exp(-t * 11) * 0.12


def pad(fs, d):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * f * t + np.sin(2 * np.pi * 0.3 * t)) for f in fs)
    env = np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.4)
    return x * env * 0.035


def music():
    m = np.zeros(N)
    # A minor - F - C - G, one chord per bar
    roots = [55.0, 43.65, 65.41, 49.0]
    chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]]
    arp = [[440, 523.3, 659.3, 523.3], [349.2, 440, 523.3, 440], [523.3, 659.3, 784, 659.3], [392, 493.9, 587.3, 493.9]]
    nb = int(V.TOTAL / BEAT) + 4
    for b in range(nb):
        t0 = b * BEAT
        bar = (b // 4) % 4
        place(m, kick(), t0, 1.0)
        if b % 2 == 1:
            place(m, clap(), t0, 1.0)
        place(m, hat(), t0 + BEAT / 2, 1.0)
        place(m, hat(b % 4 == 3), t0 + BEAT * 0.75, 0.7)
        place(m, bass(roots[bar], BEAT * 0.48), t0, 1.0)
        place(m, bass(roots[bar], BEAT * 0.4), t0 + BEAT / 2, 0.8)
        for q in range(2):
            place(m, pluck(arp[bar][(b * 2 + q) % 4]), t0 + q * BEAT / 2, 1.0)
        if b % 4 == 0:
            place(m, pad(chords[bar], BEAT * 4), t0, 1.0)
    return m


# ------------------------------------------------------------------ sfx
def whoosh(d=0.45, f0=250, f1=2400):
    t = tt(d)
    x = rng.normal(0, 1, len(t))
    f = np.cumsum(np.interp(t, [0, d], [f0, f1])) / SR
    return lp(np.sin(2 * np.pi * f) * x * np.sin(np.pi * t / d) ** 2, 6) * 0.3


def pop(pitch=1.0):
    t = tt(0.12)
    return np.sin(2 * np.pi * (480 + 900 * np.exp(-t * 40)) * pitch * t) * np.exp(-t * 35) * 0.45


def tick():
    t = tt(0.035)
    return np.sin(2 * np.pi * 2100 * t) * np.exp(-t * 110) * 0.22


def ding():
    t = tt(0.8)
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((1568, 4), (2093, 5), (3136, 7))) * 0.18


def flex():
    """Cartoon flex stinger: rubbery boing + punch."""
    t = tt(0.5)
    boing = np.sin(2 * np.pi * (180 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)) * t) * np.exp(-t * 6) * 0.4
    k = np.zeros(len(t))
    kk = kick()
    k[:len(kk)] = kk
    return boing + k * 0.6


def laser(d=0.5):
    t = tt(d)
    f = np.cumsum(np.interp(t, [0, d], [1800, 400])) / SR
    return (np.sin(2 * np.pi * f) * 0.5 + whoosh(d, 900, 3000)[:len(t)]) * np.exp(-t * 3) * 0.35


def build():
    sfx = np.zeros(N)
    for c in V.CUTS:
        place(sfx, whoosh(0.5), c - 0.2, 0.55)
    ks = sorted(V.CAM, key=lambda k: k[0])
    for a, b in zip(ks, ks[1:]):                      # whoosh on big camera moves
        if b[4]:
            continue
        ratio = max(a[3], b[3]) / min(a[3], b[3])
        dist = abs(a[1] - b[1]) + abs(a[2] - b[2])
        if ratio > 1.6 or dist > 3:
            place(sfx, whoosh(min(0.9, max(0.35, (b[0] - a[0]) * 0.6))), a[0] + 0.05, 0.45 if ratio < 20 else 0.7)
    nb = 0
    for o in V.OV:
        k, t0 = o["kind"], o["t0"]
        if t0 < 0:
            continue
        if k in ("pin", "label", "fill", "curved"):
            place(sfx, pop(), t0, 0.35 if k == "fill" else 0.45)
        elif k == "char":
            place(sfx, pop(1.3), t0, 0.5)
            if o.get("arms"):
                for q in range(int((o["t1"] - t0) / 0.62)):
                    place(sfx, flex(), t0 + 0.2 + q * 0.62, 0.45)
        elif k in ("counter", "ruler"):
            dur = o.get("dur", 1.2)
            for q in range(int(dur / 0.06)):
                place(sfx, tick(), t0 + q * 0.06, 0.5)
            place(sfx, ding(), t0 + dur, 0.45)
        elif k == "bubble":
            place(sfx, pop(1.0 + 0.12 * nb), t0, 0.6)
            nb += 1
        elif k == "elev":
            place(sfx, whoosh(0.8, 120, 900), t0, 0.4)
    for t0, t1, p in V.SCENES:
        for _, ta in p.get("arcs", []):
            place(sfx, laser(), ta, 0.4)
    return sfx


if __name__ == "__main__":
    tag = V.SHORT
    voice = np.zeros(N)
    vp = f"{tag}/lumean/result.mp3"
    if os.path.exists(vp):
        raw, sr = sf.read(vp)
        raw = raw.mean(axis=1) if raw.ndim > 1 else raw
        if sr != SR:
            import scipy.signal as ss
            raw = ss.resample_poly(raw, SR, sr)
        i0 = int(V.LEAD * SR)
        seg = raw[:N - i0]
        voice[i0:i0 + len(seg)] = seg
    else:
        print("no voice: preview mix")
    m = music()
    m *= np.minimum(1, np.arange(N) / (0.2 * SR)) * np.clip((V.TOTAL - np.arange(N) / SR) / 1.0, 0, 1)
    sfx = build()
    sf.write(f"{tag}/voice.wav", voice, SR)
    sf.write(f"{tag}/music.wav", m / (np.abs(m).max() + 1e-9) * 0.8, SR)
    sf.write(f"{tag}/sfx.wav", np.clip(sfx, -1, 1), SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tag}/voice.wav", "-i", f"{tag}/music.wav", "-i", f"{tag}/sfx.wav",
                    "-filter_complex",
                    "[0:a]asplit=2[v][vsc];[1:a]volume=0.42[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=7:attack=8:release=300[md];"
                    "[2:a]lowpass=f=10000,volume=0.65[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.84:level=0,aresample=44100[a]",
                    "-map", "[a]", "-t", str(V.TOTAL), f"{tag}/mix.wav"], check=True)
    print("mix", tag, round(V.TOTAL, 2))
