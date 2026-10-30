"""Room tone + foley bed for ep.1 (free, synthesised; no samples, no music). Level and spectrum follow the reference measurement
(Vlog 1: pause floor -57...-45 dB RMS, median -50, low-heavy spectrum, an ambience per shot, no silence > 1 s at -50 dB).
Per scene one continuous bed (same room = same tone); foley hangs on real motion peaks of each clip (frame difference).
Voice is lowered 2.6 dB because dual-mono stereo reads 3 dB louder than the mono finals (keeps -14.5 LUFS).
Usage: python3 build_bed.py   (reads frames/*_final*.mp4, writes frames/<clip>_bed.mp4 and frames/EP1_C01-C08_bed.mp4)"""
import subprocess, numpy as np
SR = 48000
F = "frames/"
CLIPS = [("C01", "C01_final_v4", "A"), ("C02", "C02_final", "A"), ("C03", "C03_final", "A"), ("C04", "C04_final", "B"),
         ("C05", "C05_final_jumpcut", "B"), ("C06", "C06_final", "B"), ("C07", "C07_final", "C"), ("C08", "C08_final_lcut", "C")]
# scene: tone colour, murmur of people in the room (dB), seed
SCENE = {"A": dict(murmur=-60, tone=-48.5, seed=1), "B": dict(murmur=-70, tone=-48.5, seed=2), "C": dict(murmur=-52, tone=-48.5, seed=3)}
rng = np.random.default_rng(7)


def pcm(p, ch=1):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vn", "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)


def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def motion(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", "fps=24,scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 96, 54).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2)); return np.convolve(d, np.ones(3) / 3, "same")


def shaped(n, tilt, lo, hi, seed):
    r = np.random.default_rng(seed); X = np.fft.rfft(r.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); f[0] = 1
    X *= f ** (-tilt / 2) * ((f > lo) & (f < hi)); y = np.fft.irfft(X, n); return (y / y.std()).astype(np.float32)


def db(x): return 10 ** (x / 20)


def envelope_noise(n, rate, seed):                                     # slow random syllable-like envelope 0..1
    r = np.random.default_rng(seed); k = int(n / SR * rate) + 3; e = np.clip(r.standard_normal(k) * 0.9 + 0.2, 0, None)
    return np.interp(np.linspace(0, k - 1, n), np.arange(k), np.convolve(e, [.25, .5, .25], "same")).astype(np.float32)


def scene_bed(n, sc, name):
    p = SCENE[sc]; out = np.zeros((2, n), np.float32)
    for ch in range(2):
        room = shaped(n, 1.0, 30, 7000, p["seed"] * 10 + ch)             # pink, low-heavy room tone
        room *= 1 + 0.12 * np.sin(2 * np.pi * (0.07 + 0.02 * ch) * np.arange(n) / SR + ch)
        out[ch] = room * db(p["tone"])
        mur = shaped(n, 0.5, 180, 1600, p["seed"] * 100 + ch) * envelope_noise(n, 3.5, p["seed"] * 7 + ch) ** 1.5
        out[ch] += mur * db(p["murmur"]) / max(mur.std(), 1e-6) * 0.5
    return out


def rustle(n_ms, level, seed):                                          # fabric / wig: band-passed noise burst
    n = int(SR * n_ms / 1000); y = shaped(n, 0.3, 700, 6500, seed); t = np.arange(n) / n
    env = np.minimum(t / 0.12, 1) * np.exp(-3.2 * t) * (0.6 + 0.4 * np.abs(np.sin(9 * np.pi * t)))
    return (y * env * db(level)).astype(np.float32)


def thud(level, seed):                                                  # soft footstep on parquet
    n = int(SR * 0.22); t = np.arange(n) / SR; y = np.sin(2 * np.pi * 95 * t) * np.exp(-t * 28) + 0.35 * shaped(n, 0.2, 800, 3000, seed) * np.exp(-t * 60)
    return (y * db(level)).astype(np.float32)


def clink(level, seed):                                             # ring on a finger / brooch: very short, inharmonic, not a tune
    r = np.random.default_rng(seed); n = int(SR * 0.16); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * r.uniform(.97, 1.03) * t) * np.exp(-t * d) for f, d in ((3100, 38), (4730, 55), (6890, 80)))
    return (y / 3 * db(level)).astype(np.float32)


def place(buf, ev, t, pan):
    i = int(t * SR); k = min(len(ev), buf.shape[1] - i)
    if k > 0: buf[0, i:i + k] += ev[:k] * (1 - pan) ** 0.5; buf[1, i:i + k] += ev[:k] * (1 + pan) ** 0.5


def foley_for(cid, path, d, voice):
    m = motion(path); thr = m.mean() + 0.9 * m.std(); ev = []; last = -9
    for i in range(1, len(m) - 1):
        if m[i] > thr and m[i] >= m[i - 1] and m[i] >= m[i + 1] and i / 24 - last > 0.45: ev.append(i / 24); last = i / 24
    buf = np.zeros((2, int(SR * (d + 0.3))), np.float32); n = 0
    for k, t in enumerate(ev):
        amp = min(1.0, m[int(t * 24)] / (thr * 2.0)); lv = -41 + 7 * amp + rng.uniform(-1.5, 1.5)   # louder with bigger motion
        place(buf, rustle(rng.uniform(160, 380), lv, 500 + k), t, rng.uniform(-.5, .5)); n += 1
        if cid in ("C02", "C04", "C05", "C06") and rng.random() < 0.3: place(buf, clink(lv - 4, 900 + k), t + 0.05, rng.uniform(-.3, .3))
    if cid == "C07":                                                    # the court walks in (first 4 s), then settles; wig tap at "wig" (about 6.9 s)
        for k, t in enumerate(np.cumsum(rng.uniform(.28, .55, 9)) + 0.2):
            if t < 4.2: place(buf, thud(-40 - 1.5 * t, 70 + k), t, rng.uniform(-.8, .8))
        place(buf, rustle(220, -33, 77), 6.95, 0.0); place(buf, thud(-36, 78), 6.97, 0.0); n += 2
    if cid == "C08":                                                    # the court bows behind him: cloth swishes at 0.7 and 1.6 s
        for t in (0.7, 1.6): place(buf, rustle(420, -38, int(t * 100)), t, rng.uniform(-.6, .6)); n += 1
    return buf, n


def main():
    info = []; order = []
    for cid, src, sc in CLIPS:
        p = F + src + ".mp4"; order.append((cid, p, sc, dur(p)))
    scenes = {}
    for cid, p, sc, d in order: scenes.setdefault(sc, []).append((cid, p, d))
    for sc, items in scenes.items():
        total = sum(d for _, _, d in items) + 1.0; bed = scene_bed(int(SR * total), sc, sc); t0 = 0.0
        for cid, p, d in items:
            voice = pcm(p); fol, n = foley_for(cid, p, d, voice); s = int(SR * t0); L = int(SR * d)
            seg = bed[:, s:s + L].copy(); seg[:, :fol.shape[1]] += fol[:, :L] if fol.shape[1] >= L else np.pad(fol, ((0, 0), (0, L - fol.shape[1])))[:, :L]
            f = int(SR * 0.02); seg[:, :f] *= np.linspace(0, 1, f); seg[:, -f:] *= np.linspace(1, 0, f)   # clean hard cut between shots
            v = np.zeros(L, np.float32); v[:min(L, len(voice))] = voice[:L]
            mix = seg + v[None, :] * db(-2.6); mix = np.clip(mix, -0.89, 0.89)
            raw = SC + cid + "_bed.f32"; open(raw, "wb").write(mix.T.astype(np.float32).tobytes())
            out = F + cid + "_bed.mp4"
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", p, "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", out], check=True)
            print(cid, "scene", sc, "dur", round(d, 2), "foley events", n, flush=True); t0 += d
    ins = sum([["-i", F + c + "_bed.mp4"] for c, _, _ in CLIPS], [])
    fc = "".join(f"[{i}:v]setsar=1[v{i}];" for i in range(len(CLIPS))) + "".join(f"[v{i}][{i}:a]" for i in range(len(CLIPS))) + f"concat=n={len(CLIPS)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "320k", F + "EP1_C01-C08_bed.mp4"], check=True)


SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
main()
