"""Audio for engine70 Shorts: original synthesised 122 BPM driving synth bed (reference mood: upbeat electronic) + one SFX per
visual event (reference: 5-8 SFX per 10 s, every graphic has its sound) + voice. SHORT=wk python3 audio83.py -> wk/mix.wav (copied from audio70)"""
import os
import subprocess

import numpy as np
import soundfile as sf

import engine83 as V

SR = 44100
N = int(V.TOTAL * SR) + SR
rng = np.random.default_rng(70)
BPM = 122
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
    # D minor - Bb - F - C, one chord per bar
    roots = [73.42, 58.27, 87.31, 65.41]
    chords = [[293.7, 349.2, 440], [233.1, 293.7, 349.2], [349.2, 440, 523.3], [261.6, 329.6, 392]]
    arp = [[587.3, 698.5, 880, 698.5], [466.2, 587.3, 698.5, 587.3], [698.5, 880, 1046.5, 880], [523.3, 659.3, 784, 659.3]]
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
        for q in range(4):
            place(m, pluck(arp[bar][(b * 4 + q) % 4]), t0 + q * BEAT / 4, 0.75 if q % 2 else 1.0)
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


def marker():
    """Felt-pen strike: band-passed noise scratch."""
    t = tt(0.24)
    x = rng.normal(0, 1, len(t))
    x = lp(x, 3) - lp(x, 18)
    return x * np.sin(np.pi * t / 0.24) * (1 + 0.5 * np.sin(2 * np.pi * 38 * t)) * 0.5


def hit():
    t = tt(0.6)
    return (np.sin(2 * np.pi * (40 + 80 * np.exp(-t * 18)) * t) * np.exp(-t * 6) * 0.8 + lp(rng.normal(0, 1, len(t)), 4) * np.exp(-t * 20) * 0.2)


def glow():
    t = tt(0.5)
    return sum(np.sin(2 * np.pi * f * t) for f in (880, 1320)) * np.sin(np.pi * t / 0.5) ** 2 * 0.06


def slide(d=2.2):
    """Shrink: descending synth sweep + air."""
    t = tt(d)
    f = np.cumsum(np.interp(t, [0, d], [900, 180])) / SR
    return (np.sin(2 * np.pi * f) * 0.25 + whoosh(d, 1800, 300)[:len(t)] * 0.6) * np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.3)


def build():
    sfx = np.zeros(N)
    ev = V.events()
    for t0, kind in ev:
        if kind == "whoosh":
            place(sfx, whoosh(0.55), t0 - 0.1, 0.55)
        elif kind == "pop":
            place(sfx, pop(1.0 + 0.1 * rng.uniform(-1, 1)), t0, 0.5)
        elif kind == "swish":
            place(sfx, whoosh(0.3, 900, 3500), t0, 0.35)
        elif kind == "marker":
            place(sfx, marker(), t0, 0.6)
        elif kind == "ding":
            place(sfx, ding(), t0, 0.55)
        elif kind == "hit":
            place(sfx, hit(), t0, 0.6)
        elif kind == "glow":
            place(sfx, glow(), t0, 0.7)
    for o in V.OV:
        if o["kind"] in ("counter", "measure"):
            dur = o.get("dur", 1.0)
            st = o["t0"] + (0.25 if o["kind"] == "measure" else 0)
            for q in range(int(dur / 0.07)):
                place(sfx, tick(), st + q * 0.07, 0.45)
            place(sfx, ding(), st + dur, 0.45)
        elif o["kind"] == "truesize":
            place(sfx, slide(o["tb"] - o["ta"]), o["ta"], 0.55)
    return sfx


if __name__ == "__main__":
    tag = V.SHORT
    voice = np.zeros(N)
    raw, sr = sf.read(f"{tag}/lumean/result.mp3")
    raw = raw.mean(axis=1) if raw.ndim > 1 else raw
    if sr != SR:
        import scipy.signal as ss
        raw = ss.resample_poly(raw, SR, sr)
    i0 = int(V.LEAD * SR)
    seg = raw[:N - i0]
    voice[i0:i0 + len(seg)] = seg
    m = music()
    m *= np.minimum(1, np.arange(N) / (0.2 * SR)) * np.clip((V.TOTAL - np.arange(N) / SR) / 0.3, 0, 1)
    sfx = build()
    sf.write(f"{tag}/voice.wav", voice, SR)
    sf.write(f"{tag}/music.wav", m / (np.abs(m).max() + 1e-9) * 0.8, SR)
    sf.write(f"{tag}/sfx.wav", np.clip(sfx, -1, 1), SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tag}/voice.wav", "-i", f"{tag}/music.wav", "-i", f"{tag}/sfx.wav",
                    "-filter_complex",
                    "[0:a]asplit=2[v][vsc];[1:a]volume=0.40[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=7:attack=8:release=300[md];"
                    "[2:a]lowpass=f=10000,volume=0.6[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.84:level=0,aresample=44100[a]",
                    "-map", "[a]", "-c:a", "pcm_s16le", f"{tag}/mix.wav"], check=True)
    print("mix ok")
