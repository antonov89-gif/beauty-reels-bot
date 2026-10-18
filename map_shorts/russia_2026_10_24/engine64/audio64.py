"""Audio for engine64 Shorts: synthesised 118 BPM upbeat bed (reference style) + SFX from the overlay timeline + voice.
SHORT=<key> python3 audio63.py  -> <key>/mix.wav   (voice is skipped if <key>/lumean/result.mp3 is missing: preview mode)"""
import os
import subprocess

import numpy as np
import soundfile as sf

import engine64 as V

SR = 44100
N = int(V.TOTAL * SR) + SR
rng = np.random.default_rng(63)
BPM = 132
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
    roots = [55.0, 55.0, 43.65, 49.0]
    chords = [[220, 261.6, 329.6], [220, 261.6, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7]]
    arp = [[440, 523.3, 659.3, 523.3], [440, 523.3, 659.3, 784], [349.2, 440, 523.3, 440], [392, 493.9, 587.3, 493.9]]
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


def noise(d, k=40):
    return lp(rng.normal(0, 1, int(d * SR)), k)


def boom():
    t = tt(1.0)
    return (np.sin(2 * np.pi * (38 + 60 * np.exp(-t * 3)) * t) * np.exp(-t * 3.2) * 0.9 + noise(1.0, 60) * np.exp(-t * 6) * 1.0) * 0.8


def thud():
    t = tt(0.5)
    return (np.sin(2 * np.pi * (70 + 80 * np.exp(-t * 18)) * t) * np.exp(-t * 7) * 0.8 + noise(0.5, 30) * np.exp(-t * 30) * 0.6) * 0.8


def crack():
    t = tt(0.5)
    x = rng.normal(0, 1, len(t))
    x = x - lp(x, 4)
    return x * np.exp(-t * 14) * 0.5 + np.sin(2 * np.pi * (2400 - 1500 * t) * t) * np.exp(-t * 20) * 0.25


def fire_whoosh(d=0.9):
    t = tt(d)
    x = lp(rng.normal(0, 1, len(t)), 12) * (np.sin(np.pi * t / d) ** 1.5)
    return x * 0.9 + (rng.normal(0, 1, len(t)) - lp(rng.normal(0, 1, len(t)), 5)) * np.exp(-t * 4) * 0.12


def knock():
    t = tt(0.18)
    return np.sin(2 * np.pi * 180 * t) * np.exp(-t * 26) * 0.55


def wind(d=1.6):
    t = tt(d)
    x = lp(rng.normal(0, 1, len(t)), 60) * np.sin(np.pi * t / d) ** 2
    return x * 1.6


def build():
    sfx = np.zeros(N)
    for c in V.CUTS:
        if 0 < c < V.TOTAL - 1:
            place(sfx, whoosh(0.5), c - 0.22, 0.5)
            place(sfx, boom(), c, 0.55)                     # bass hit exactly on the cut
    ks = sorted(V.CAM, key=lambda k: k[0])
    for a_, b_ in zip(ks, ks[1:]):
        if b_[4]:
            continue
        ratio = max(a_[3], b_[3]) / min(a_[3], b_[3])
        dist = abs(a_[1] - b_[1]) + abs(a_[2] - b_[2])
        if ratio > 3 or dist > 10:
            place(sfx, whoosh(min(0.9, max(0.35, (b_[0] - a_[0]) * 0.6))), a_[0] + 0.05, 0.45)
    last_banner = -9
    for o in V.OV:
        k, t0 = o["kind"], o["t0"]
        if t0 < 0 and k != "banner":
            continue
        if k == "banner":
            if t0 - last_banner > 4.0 or t0 < 0:
                place(sfx, pop(), max(t0, 0.02), 0.4)
                place(sfx, tick(), max(t0, 0.02) + 0.1, 0.5)
                last_banner = t0
        elif k == "arrow":
            place(sfx, whoosh(0.9, 400, 3200), t0, 0.55)
        elif k == "fort":
            place(sfx, knock(), t0 + 0.05, 0.9)
            place(sfx, pop(), t0, 0.5)
        elif k == "fire":
            place(sfx, fire_whoosh(), t0, 0.7)
        elif k == "stamp":
            place(sfx, thud(), t0, 0.95)
            place(sfx, crack(), t0, 0.5)
        elif k in ("pin", "label"):
            place(sfx, pop(), t0, 0.35)
            if o.get("shake"):
                place(sfx, thud(), t0, 0.7)
        elif k == "counter":
            dur = o.get("dur", 1.2)
            for q in range(int(dur / 0.06)):
                place(sfx, tick(), t0 + q * 0.06, 0.5)
            place(sfx, ding(), t0 + dur, 0.45)
            if o.get("shake"):
                place(sfx, thud(), t0, 0.5)
        elif k == "thermo":
            place(sfx, wind(1.8), t0, 0.6)
        elif k == "hudcard":
            for q in range(len(o["rows"])):
                place(sfx, tick(), t0 + 0.35 + q * 0.28, 0.8)
    for fl in V.FLASH:
        place(sfx, crack(), fl, 0.8)
        place(sfx, whoosh(0.6, 300, 4000), fl - 0.1, 0.4)
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
                    "[0:a]highpass=f=85,deesser=i=0.3,equalizer=f=250:t=q:w=1:g=-1.5,equalizer=f=3500:t=q:w=1.1:g=1.8,acompressor=threshold=-21dB:ratio=2:attack=15:release=140:makeup=2,aecho=0.9:0.9:34|68:0.09|0.05,asplit=2[v][vsc];[1:a]volume=0.42[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=7:attack=8:release=300[md];"
                    "[2:a]lowpass=f=10000,volume=0.65[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.8:level=0,aresample=44100[a]",
                    "-map", "[a]", "-t", str(V.TOTAL), f"{tag}/mix.wav"], check=True)
    print("mix", tag, round(V.TOTAL, 2))
