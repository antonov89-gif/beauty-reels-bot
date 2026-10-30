"""C09 from the Seedance 2.5 Lite remake (seedance25lite_c09.mp4, 720p): our locked line laid on the king's MOUTH, Marcel's own voice for "Pardon, Sire!", the model's own SOUNDS kept (its speech removed by htdemucs).
v2 (30.10, owner: "sound does not match"): v1 placed our phrases on the onsets of the model's speech stem; measured against the real mouth (lip_measure.py, face mesh) the model's audio is itself up to 0.4 s late on "Eyes" (the mouth opens at 6.1 s, the voice starts at 6.52 s) and our voice was 0.2 s late on "Lower!", 0.3-0.4 s early-ending on "and there goes the hat". Now every short unit of our line (a word or a few words) is placed by a search over start (+-0.25 s of a seed) and tempo that maximises the correlation of the mouth opening with our speech energy; units where the face is turned away (2.3-3.3 s) keep the seed from the model's audio.
The model made no real "Pardon, Sire!" (only a faint blip at 2.5 s), so Marcel's cry is ours (voice/tts_ep1/marcel_C09_pardon.mp3), placed when the hat tumbles and he turns after it.
Usage: python3 lip_measure.py frames/seedance25lite_c09.mp4 <scratchpad>/c09qc/mouth_model.json ; python3 build_c09_lite.py -> frames/C09L_final_A.mp4 (1080x1920, our voices only) + scratchpad lite_c09_rest_A.f32 (model sounds)"""
import json, subprocess, numpy as np
V = "A"; SR = 48000; MODEL = "frames/seedance25lite_c09.mp4"
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
MARCEL_AT = 1.85; MARCEL_GAIN = 0.6                    # speech onset of "Pardon, Sire!" (s) and its level against the king (he stands further away)
# name, speech in our TTS (voice/tts_ep1/C09.mp3; borders from the energy dips and word times), mouth window in the clip, seed start, search radius, tempo range, optimise?
UNITS = [("Lower!",          0.16, 0.67, 0.05, 0.85, 0.27, 0.25, (1.0, 1.5), True, 1.0),
         ("Lower!",          1.10, 1.52, 1.00, 1.60, 1.12, 0.20, (1.2, 1.6), True, 1.0),   # only "Lo-wer" is kept, the sustained tail is cut (the mouth shuts at 1.42; cut earlier the word sounded like "Low")
         ("And there goes",  2.27, 2.95, 0, 0, 2.95, 0, (1.1, 1.1), False, 1.0),          # head turned away (no face 2.3-3.4): seed from the model's audio (2.95); "goes" ends at 2.95 in our TTS (voiced to 2.86, then the s)
         ("the",             2.95, 3.14, 3.75, 4.00, 3.83, 0.04, (0.9, 1.2), True, 1.0),   # voiced 2.96-3.12, dip at 3.12-3.15 (v1-v4 cut at 2.81/3.10 and carried the end of "goes" into "the")
         ("hat.",            3.15, 3.42, 4.00, 4.80, 4.02, 0.06, (0.4, 0.8), True, 2.2),   # mouth shuts at 3.96, then wide 4.0-4.7: a long breathy "haaat"; our "hat." trails off 17 dB down: flattened and lifted
         ("Eyes on",         3.87, 4.145, 5.95, 6.78, 6.15, 0.15, (0.55, 1.1), True, 1.0), # mouth wide 6.1-6.65, the model's voice only starts at 6.52
         ("me,",             4.145, 4.47, 6.78, 7.30, 6.88, 0.12, (0.8, 1.3), True, 1.0),  # lips shut at 6.85-6.95 (m), vowel 7.0-7.2
         ("not on the",      4.66, 5.14, 7.10, 7.54, 7.16, 0.06, (1.3, 1.6), True, 1.0),   # small mouth 7.25-7.5, closed at 7.50
         ("hat.",            5.16, 5.33, 7.54, 8.05, 7.58, 0.08, (0.6, 1.0), True, 1.5)]   # wide 7.58-7.83
mouth = json.load(open(SC + "c09qc/mouth_model.json")); mt = np.array([r[0] for r in mouth]); ml = np.array([np.nan if r[1] is None else r[1] for r in mouth])


def flatten(seg, power=0.6, cap=2.2):                                # evens out a word that trails off (our deadpan "hat.") so it carries as much as the wide mouth asks for
    w = int(SR * .03); e = np.sqrt(np.convolve(seg ** 2, np.ones(w) / w, "same")); e = np.maximum(e, e.max() * 0.02)
    return (seg * np.minimum((e.max() / e) ** power, cap)).astype(np.float32)


def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)


def env(y, sr=SR):
    w = int(sr * .01); return np.array([np.sqrt((y[i:i + w] ** 2).mean()) for i in range(0, len(y) - w, w)])


x = load("../voice/tts_ep1/C09.mp3"); mx = load("../voice/tts_ep1/marcel_C09_pardon.mp3")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MODEL], capture_output=True, text=True).stdout)
track = np.zeros(int(SR * (dur + 0.3)), np.float32); ex = env(x)


def fit(o0, o1, w0, w1, seed, rad, tr, lo):
    """start s and tempo tp for one unit: max correlation of the mouth opening with our speech energy over the frames of the window that have a face"""
    ok = ~np.isnan(ml) & (mt >= w0) & (mt < w1); best = (-9, seed, 1.0, None)
    if ok.sum() < 6: return None
    a = ml[ok]
    for tp in np.arange(tr[0], tr[1] + 1e-9, 0.05):
        for s in np.arange(max(seed - rad, lo), seed + rad + 1e-4, 0.02):
            src = o0 + (mt[ok] - s) * tp                                                      # time in our TTS that sounds at each video frame
            e = np.where((src >= o0) & (src <= o1), np.interp(src, np.arange(len(ex)) * .01, ex), 0.0)
            if e.max() == 0 or a.std() == 0: continue
            c = np.corrcoef(a, np.sqrt(e))[0, 1] - 0.15 * abs(s - seed) / rad
            if c > best[0]: best = (c, s, tp, None)
    return best


prev_end = 0.0
for n, (name, o0, o1, w0, w1, seed, rad, tr, opt, gain) in enumerate(UNITS):
    r = fit(o0, o1, w0, w1, seed, rad, tr, prev_end - 0.06) if opt else None
    c, s, tp = (r[0], r[1], r[2]) if r else (float("nan"), seed, tr[0])
    seg = x[int((o0 - 0.04) * SR):int((o1 + 0.04) * SR)].copy(); f = int(SR * .006); seg[:f] *= np.linspace(0, 1, f); fo = int(SR * (.04 if name == "Lower!" and o0 > 1 else .006)); seg[-fo:] *= np.linspace(1, 0, fo)
    if gain > 1: seg = flatten(seg); fo2 = int(SR * .03); seg[-fo2:] *= np.linspace(1, 0, fo2)   # the breath after the "t" is not lifted
    if abs(tp - 1) > .01: seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", (f"atempo={tp:.3f}" if tp >= 0.5 else f"atempo=0.5,atempo={tp / 0.5:.3f}"), "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, np.float32)
    i0 = int(max(0, s - 0.04 / tp) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k] * gain
    prev_end = s + (o1 - o0) / tp
    print(f"{name:16s} start {s:.2f} s  tempo {tp:.2f}  speech {(o1 - o0) / tp:.2f} s  mouth corr {c:.2f}" + ("" if opt else "  (seed, no face)"))
f = int(SR * .01); mx = mx.copy(); mx[:f] *= np.linspace(0, 1, f); mx[-f:] *= np.linspace(1, 0, f)
em = env(mx); i0 = int((MARCEL_AT - float(np.argmax(em > em.max() * 0.1)) * 0.01) * SR); k = min(len(mx), len(track) - i0); track[i0:i0 + k] += mx[:k] * MARCEL_GAIN
print("Marcel 'Pardon, Sire!' speech starts at", MARCEL_AT, "s")
open(SC + "c09L_voice.f32", "wb").write(track.tobytes())
vf = "scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p"
fc = f"[0:v]{vf}[vv];[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,volume=2.2dB,alimiter=limit=0.80:attack=2:release=60:level=disabled[v]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c09L_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]",
                "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", f"frames/C09L_final_{V}.mp4"], check=True)
r = np.frombuffer(open(SC + "sep/lite_c09_rest.f32", "rb").read(), np.float32).reshape(-1, 2)
r = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", "-", "-ar", str(SR), "-f", "f32le", "-"], input=r.tobytes(), capture_output=True).stdout, np.float32)
open(SC + f"lite_c09_rest_{V}.f32", "wb").write(r.astype(np.float32).tobytes())
