"""Audio for map loops: original 120 BPM synth bed, exactly 4 bars = 8.0 s, plus one SFX per visual event. Everything is placed
circularly (a tail that runs past the end wraps to the start), so the audio loops with no seam, like the picture.
No voice and no third-party audio. Instruments are taken over from audio83 (Walk It). LOOP=l01_circle python3 audio_loop.py -> <loop>/mix.wav"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine_loop as V  # noqa: E402

SR = 44100
N = int(round(V.TOTAL * SR))
rng = np.random.default_rng(84)
BPM = 120
BEAT = 60 / BPM


def tt(d):
    return np.arange(int(d * SR)) / SR


def place(buf, s, t, g=1.0):
    """Add s at time t, wrapping around the loop end."""
    i = int(round(t * SR)) % N
    idx = (i + np.arange(len(s))) % N
    np.add.at(buf, idx, s * g)


def lp(x, k):
    return np.convolve(x, np.ones(k) / k, "same")


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
    roots = [73.42, 58.27, 87.31, 65.41]                       # Dm - Bb - F - C, one chord per bar: 4 bars = one loop
    chords = [[293.7, 349.2, 440], [233.1, 293.7, 349.2], [349.2, 440, 523.3], [261.6, 329.6, 392]]
    arp = [[587.3, 698.5, 880, 698.5], [466.2, 587.3, 698.5, 587.3], [698.5, 880, 1046.5, 880], [523.3, 659.3, 784, 659.3]]
    for b in range(int(round(V.TOTAL / BEAT))):
        t0, bar = b * BEAT, (b // 4) % 4
        place(m, kick(), t0)
        if b % 2 == 1:
            place(m, clap(), t0)
        place(m, hat(), t0 + BEAT / 2)
        place(m, hat(b % 4 == 3), t0 + BEAT * 0.75, 0.7)
        place(m, bass(roots[bar], BEAT * 0.48), t0)
        place(m, bass(roots[bar], BEAT * 0.4), t0 + BEAT / 2, 0.8)
        for q in range(4):
            place(m, pluck(arp[bar][(b * 4 + q) % 4]), t0 + q * BEAT / 4, 0.75 if q % 2 else 1.0)
        if b % 4 == 0:
            place(m, pad(chords[bar], BEAT * 4 + 0.4), t0 - 0.2)
    return m


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


def glow():
    t = tt(0.5)
    return sum(np.sin(2 * np.pi * f * t) for f in (880, 1320)) * np.sin(np.pi * t / 0.5) ** 2 * 0.06


def slide(d=2.0):
    t = tt(d)
    f = np.cumsum(np.interp(t, [0, d], [900, 180])) / SR
    return (np.sin(2 * np.pi * f) * 0.25 + whoosh(d, 1800, 300)[:len(t)] * 0.6) * np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.3)


def sfx():
    s = np.zeros(N)
    for t0, kind in V.events():
        if kind == "whoosh":
            place(s, whoosh(0.55), t0 - 0.1, 0.55)
        elif kind == "pop":
            place(s, pop(1.0 + 0.1 * rng.uniform(-1, 1)), t0, 0.5)
        elif kind == "swish":
            place(s, whoosh(0.3, 900, 3500), t0, 0.35)
        elif kind == "glow":
            place(s, glow(), t0, 0.7)
    for o in V.OV:
        if o["kind"] == "bars":                                # ticks while a bar grows, ding when it lands
            for it in o["items"]:
                for (ta, va), (tb, vb) in zip(it["k"], it["k"][1:]):
                    if vb > va and 0 <= ta < V.TOTAL:
                        for q in range(int((tb - ta) / 0.07)):
                            place(s, tick(), ta + q * 0.07, 0.45)
                        place(s, ding(), tb, 0.45)
        elif o["kind"] == "truesize":
            for ta, tb, _ in o.get("legs", []):
                if 0 <= ta < V.TOTAL:
                    place(s, slide(tb - ta), ta, 0.55)
    return s


def loudnorm(src, dst, target=-14.0):
    """Two-pass linear loudnorm (a gain, no pumping), so the loop seam stays clean."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", f"loudnorm=I={target}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    js = json.loads(p.stderr[p.stderr.rindex("{"):p.stderr.rindex("}") + 1])
    af = (f"loudnorm=I={target}:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,aresample=44100")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af, "-c:a", "pcm_s16le", dst], check=True)


if __name__ == "__main__":
    tag = V.LOOP
    m, s = music(), sfx()
    mix = m / (np.abs(m).max() + 1e-9) * 0.55 + np.clip(s, -1, 1) * 0.6
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)                    # soft clip, keeps peaks round
    sf.write(f"{tag}/premix.wav", mix, SR)
    loudnorm(f"{tag}/premix.wav", f"{tag}/mix.wav")
    print("mix ok", tag, len(mix) / SR, "s")
