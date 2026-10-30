"""Ep.1 sound v4 (30.10.2026): REAL recordings instead of synthesis (owner on v3: "эхо и будто музыка какая-то, сравни ещё раз с референсом").
v3 removed: the synthetic crowd (pulse-train voices read as a hum/music), synthetic birds/clinks, the room reverb on the voice (the echo).
Sources: BigSoundBank (Joseph Sardin), CC0-like licence, commercial use without attribution, not in Content ID (licence page checked 30.10); files in ../sfx/bsb/<id>.mp3, list in ../sfx/SOURCES.md.
Bed per scene: A bedchamber = Chambord castle interior #1 (3431, quiet visitors' murmur, no words), B dressing room = fireplace #3 (2855) + a little of 3431,
C court = Chambord castle #3 (3433, busy murmur under vaults). Foley: door 3211, footsteps on parquet 0376/0165, squeaking parquet 3051/3053/3060, cloth 0013,
coat rubbed 1104 (grips), microphone taps 2016-2019 (knocks on the phone), key on a wooden table 0087. Phone voice: low cut, a darker top, proximity (closer = more bass and louder), NO reverb.
Usage: python3 build_sound_v4.py -> frames/<clip>_snd.mp4, frames/EP1_C01-C08_snd.mp4"""
import os, subprocess, numpy as np, cv2
from scipy.signal import butter, sosfilt
SR = 48000; F = "frames/"; B = "../sfx/bsb/"
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
CLIPS = [("C01", "C01_final_v4", "A"), ("C02", "C02_final", "A"), ("C03", "C03_final", "A"), ("C04", "C04_final_sway", "B"),
         ("C05", "C05_final_sway", "B"), ("C06", "C06_final", "B"), ("C07", "C07_final", "C"), ("C08", "C08_final_lcut", "C")]
BED = {"A": [("3431", 20.0, -47)], "B": [("2855", 30.0, -49), ("3431", 90.0, -58)], "C": [("3433", 40.0, -41)]}   # (file, start s in the file, RMS dB)
DIST = {"C01": [(0, .75), (1.6, .75), (2.4, .1)], "C02": [(0, .1)], "C03": [(0, .15)], "C04": [(0, .65)], "C05": [(0, .5)],
        "C06": [(0, .7), (1.4, .7), (3.0, .15)], "C07": [(0, .2)], "C08": [(0, .25)]}
# (clip, time s, source id, start in file s or None = loudest part, length s, peak dB, pan)
FOLEY = [("C01", 0.15, "1104", None, 0.6, -30, 0), ("C01", 0.9, "2016", 0, 0.4, -27, 0), ("C01", 1.8, "1104", 3.0, 0.5, -31, 0), ("C01", 2.8, "2018", 0, 0.5, -28, 0),
         ("C02", 2.2, "0013", None, 0.6, -33, .2), ("C02", 6.6, "1104", 5.0, 0.5, -34, 0),
         ("C03", 0.85, "0013", 3.0, 0.7, -32, .3), ("C03", 6.3, "2017", 0, 0.4, -31, 0),
         ("C04", 0.05, "0087", None, 0.8, -31, 0), ("C04", 1.7, "2017", 0, 0.4, -29, 0), ("C04", 4.6, "0087", 9.0, 0.8, -32, 0), ("C04", 5.4, "2019", 0, 0.8, -29, 0),
         ("C05", 1.85, "2018", 0, 0.5, -30, 0),
         ("C06", 1.4, "1104", 1.0, 0.7, -28, 0), ("C06", 1.55, "2019", 0, 0.8, -27, 0), ("C06", 3.5, "1104", 6.0, 0.6, -27, 0),
         ("C07", 0.15, "3211", None, 2.4, -29, .7), ("C07", 0.6, "0376", 4.0, 2.6, -33, .5), ("C07", 1.25, "2016", 0, 0.4, -28, 0), ("C07", 5.6, "1104", 2.0, 0.5, -30, 0),
         ("C08", 0.4, "0013", 6.0, 0.6, -32, -.3), ("C08", 0.7, "3053", 0, 1.3, -33, -.6), ("C08", 1.15, "0013", 1.0, 0.7, -32, .5), ("C08", 1.6, "3060", 0, 1.9, -33, .6), ("C08", 2.7, "1104", 4.0, 0.5, -31, 0)]
TAPS = ["2016", "2017", "2018", "2019"]
# optional overrides (env): C04SRC=C04L_final_A  C04SND=<f32 of the model's own sounds, 48 kHz stereo>  TAG=_lite  (outputs <clip>_snd<TAG>.mp4)
TAG = os.environ.get("TAG", "")
if os.environ.get("C04SRC"): CLIPS = [(c, os.environ["C04SRC"] if c == "C04" else s, sc) for c, s, sc in CLIPS]
MODEL_SND = {"C04": os.environ["C04SND"]} if os.environ.get("C04SND") else {}
if os.environ.get("C04DIST"): DIST["C04"] = [(0, float(os.environ["C04DIST"]))]   # the Lite C04 leans close to the lens


def db(x): return 10 ** (x / 20)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def load(p, ch=1): return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vn", "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32).reshape(-1, ch).T.copy()
_cache = {}
def src(i): 
    if i not in _cache: _cache[i] = load(B + i + ".mp3", 2)
    return _cache[i]


def piece(i, start, length):                                            # a slice of a recording, 15 ms fades; start None = the loudest window
    x = src(i); L = int(length * SR)
    if start is None:
        e = np.convolve((x.mean(0) ** 2), np.ones(L) / L, "valid") if x.shape[1] > L else np.array([0.0]); s = int(np.argmax(e[::480]) * 480)
    else: s = int(start * SR)
    y = x[:, s:s + L].copy(); f = min(int(.015 * SR), y.shape[1] // 3)
    if f > 0: y[:, :f] *= np.linspace(0, 1, f); y[:, -f:] *= np.linspace(1, 0, f)
    return y


def camera(p):                                                          # per frame: camera speed (frame widths per frame) and cumulative log zoom (ORB)
    cap = cv2.VideoCapture(p); orb = cv2.ORB_create(800); bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True); prev = None; sp = [0.0]; ls = [0.0]
    while True:
        ok, fr = cap.read()
        if not ok: break
        g = cv2.cvtColor(cv2.resize(fr, (180, 320)), cv2.COLOR_BGR2GRAY)
        if prev is not None:
            v, sc = 0.05, 1.0
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


def phone_voice(v, dist):                                               # phone-mic colour + proximity, no reverb
    hp = sosfilt(butter(2, 110, "hp", fs=SR, output="sos"), v); lo = sosfilt(butter(2, 300, "lp", fs=SR, output="sos"), hp); hi = sosfilt(butter(2, 3500, "hp", fs=SR, output="sos"), hp)
    y = hp + lo * (0.6 * (1 - dist) - 0.3 * dist) - hi * 0.4
    return (sosfilt(butter(2, 8000, "lp", fs=SR, output="sos"), y) * db(-6 * dist)).astype(np.float32)


def duck_curve(v, L, depth_db):
    fr = int(SR * .05); e = np.array([np.sqrt((v[i:i + fr] ** 2).mean()) for i in range(0, len(v) - fr, fr)]); a = np.convolve((e > 0.02).astype(float), np.ones(7) / 7, "same")
    return np.interp(np.arange(L) / fr, np.arange(len(a)), 1 - (1 - db(-depth_db)) * a).astype(np.float32)


def put(buf, y, t, peak, pan):
    y = y / (np.abs(y).max() + 1e-9) * db(peak); i = int(t * SR); k = min(y.shape[1], buf.shape[1] - i)
    if k > 0: buf[0, i:i + k] += y[0, :k] * (1 - pan) ** .5; buf[1, i:i + k] += y[1, :k] * (1 + pan) ** .5


def main():
    rng = np.random.default_rng(4); outs = []; t_scene = {}
    for cid, srcname, sc in CLIPS:
        p = F + srcname + ".mp4"; d = dur(p); L = int(SR * d); voice = load(p)[0][:L]; voice = np.pad(voice, (0, L - len(voice)))
        bed = np.zeros((2, L), np.float32); t0 = t_scene.get(sc, 0.0)
        for i, st, lvl in BED[sc]:                                      # continuous bed per scene (next clip of the same scene continues the recording)
            y = src(i)[:, int((st + t0) * SR):int((st + t0) * SR) + L]; y = np.pad(y, ((0, 0), (0, L - y.shape[1])))
            bed += y / (np.sqrt((y ** 2).mean()) + 1e-9) * db(lvl)
        t_scene[sc] = t0 + d
        bed *= duck_curve(voice, L, 4)[None, :]
        fol = np.zeros((2, L + SR * 3), np.float32); n = 0
        for c, t, i, st, ln, pk, pan in FOLEY:
            if c == cid: put(fol, piece(i, st, ln), t, pk, pan); n += 1
        speed, zoom = camera(p); last = -9
        for k in range(2, len(speed) - 2):                              # knocks on the phone at the real camera jerks
            if speed[k] > 0.012 and speed[k] == speed[max(0, k - 12):k + 12].max() and k / 24 - last > 0.6 and not any(c == cid and abs(t - k / 24) < .5 for c, t, *_ in FOLEY):
                last = k / 24; put(fol, piece(TAPS[rng.integers(4)], 0, 0.5), k / 24, -30 + rng.uniform(-2, 2), 0); n += 1
        key = DIST[cid]; dk = np.interp(np.arange(L) / SR, [q[0] for q in key] + [d + 1], [q[1] for q in key] + [key[-1][1]])
        zs = np.interp(np.arange(L) / SR, np.arange(len(zoom)) / 24, zoom); dist = np.clip(dk - 0.8 * zs, 0, 1)
        if cid in MODEL_SND:                                            # the video model's own sounds (its speech removed by htdemucs): room, knocks, cloth
            ms = np.frombuffer(open(MODEL_SND[cid], "rb").read(), np.float32).reshape(-1, 2).T[:, :L]; bed = bed * db(-6) + np.pad(ms, ((0, 0), (0, L - ms.shape[1]))) * db(3)
        room = bed + fol[:, :L]                                         # the room and the foley reach the same phone mic: same colour (reference quiet floor centre 170-624 Hz)
        for ch in range(2):
            r_ = room[ch]; hi = sosfilt(butter(2, 3000, "hp", fs=SR, output="sos"), r_)
            room[ch] = sosfilt(butter(2, 7000, "lp", fs=SR, output="sos"), sosfilt(butter(2, 60, "hp", fs=SR, output="sos"), r_ - 0.6 * hi))
        mix = room + phone_voice(voice, dist)[None, :] * db(-2.6)
        f = int(SR * .015); mix[:, :f] *= np.linspace(0, 1, f); mix[:, -f:] *= np.linspace(1, 0, f)
        outs.append((cid, p, mix, n))
    allmix = np.concatenate([m for _, _, m, _ in outs], axis=1); open(SC + "v4_all.f32", "wb").write(allmix.T.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", SC + "v4_all.f32", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = float(r.split("I:")[-1].split("LUFS")[0]); g = db(-15.0 - I)                # whole episode to -15 LUFS (reference -15.4), one gain for all clips
    for cid, p, mix, n in outs:
        mix = np.clip(mix * g, -.89, .89); raw = SC + cid + "_snd.f32"; open(raw, "wb").write(mix.T.astype(np.float32).tobytes())
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", p, "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", F + cid + "_snd" + TAG + ".mp4"], check=True)
        print(cid, "foley", n, flush=True)
    ins = sum([["-i", F + c + "_snd" + TAG + ".mp4"] for c, _, _ in CLIPS], [])
    fc = "".join(f"[{i}:v]setsar=1[v{i}];" for i in range(len(CLIPS))) + "".join(f"[v{i}][{i}:a]" for i in range(len(CLIPS))) + f"concat=n={len(CLIPS)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "320k", F + "EP1_C01-C08_snd" + TAG + ".mp4"], check=True)


if __name__ == "__main__":
    main()
