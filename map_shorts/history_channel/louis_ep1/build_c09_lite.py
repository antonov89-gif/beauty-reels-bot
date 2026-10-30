"""C09 from the Seedance 2.5 Lite remake (seedance25lite_c09.mp4, 720p): the locked voice laid on the king's lips by COMPING whole words/phrases from three takes, Marcel's own voice for "Pardon, Sire!".
v8 (30.10): v2-v7 cut one take into words and stretched them (tempo down to 0.40) to fit the lips: the owner: "Нет это ужасно". Now: no slowing down, speed-up at most 1.3, cuts only in the pauses between words, every piece taken from the take whose length already fits the lips:
take A = tts_ep1/C09.mp3 (the take used before), takes B and C = tts_ep1/C09b-C09c.mp3 (one Lumean order 30.10, 0.23 RUB, owner "Да"; B 0-11 s with drawls, C 11-22 s plain slow).
Lip targets (lip_measure.py on the clip): Lower 0.25-0.62 | Lower 1.12-1.42 | (Marcel) | And there goes ...-3.55 (head turned 2.3-3.4) | the 3.83-3.93 | lips shut 3.96 | haaat 4.0-4.7 | Eyes on 6.1-6.65, me 6.9-7.2 | not on the hat 7.25-7.9.
Usage: python3 build_c09_lite.py -> frames/C09L_final_A.mp4 (1080x1920, voices only) + scratchpad lite_c09_rest_A.f32 (model sounds)"""
import subprocess, numpy as np
V = "A"; SR = 48000; MODEL = "frames/seedance25lite_c09.mp4"
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
A, BC = "../voice/tts_ep1/C09.mp3", "../voice/tts_ep1/C09b-C09c.mp3"
MARCEL_AT = 1.85; MARCEL_GAIN = 0.6                    # speech onset of "Pardon, Sire!" (s) and its level against the king (he stands further away)
# name, take, speech start/end in the take (borders sit in pauses >= 80 ms), speech start in the clip, tempo, level (None = same active level as the first piece; a number = the previous piece's factor times it)
PIECES = [("Lower!",          A,  0.16,  0.67, 0.19, 1.20, None),
          ("Lower!",          BC, 1.11,  1.67, 1.06, 1.30, None),
          ("And there goes",  BC, 15.39, 16.38, 2.76, 1.25, None),   # take C; ends 3.55 with the open mouth on "goes"
          ("the",             BC, 16.48, 16.71, 3.81, 1.15, None),   # take C; ends at the shut lips (3.96-4.0)
          ("haaa-",           BC, 5.14,  5.51, 4.10, 1.00, None),    # take B, a real drawl at natural speed, on the opening mouth 4.1-4.47
          ("-t",              BC, 5.67,  5.75, 4.50, 1.00, 0.6),     # take B's closing "t" without its 0.16 s closure, on the widest mouth at 4.5 s; only the burst (0.08 s), not the 0.1 s breath after it
          ("Eyes on me,",     BC, 18.95, 20.11, 6.08, 1.00, None),   # take C, natural speed: "me" on the opening lips 6.9-7.2
          ("not on the hat.", A,  4.66,  5.36, 7.25, 1.00, None)]    # take A: the only take short enough for 7.25-7.9


def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)


takes = {A: load(A), BC: load(BC)}; mx = load("../voice/tts_ep1/marcel_C09_pardon.mp3")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MODEL], capture_output=True, text=True).stdout)
track = np.zeros(int(SR * (dur + 0.3)), np.float32)
ref = None
for name, take, a, b, at, tp, lv in PIECES:
    PAD = 0.03                                                                  # into the pause on both sides
    seg = takes[take][int((a - PAD) * SR):int((b + PAD) * SR)].astype(np.float64).copy(); f = int(SR * .01); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    w = int(SR * .05); r = np.sqrt(np.convolve(seg ** 2, np.ones(w) / w, "same")); act = np.sqrt((seg[r > r.max() * 0.2] ** 2).mean())
    ref = ref or act; fac = ref / act if lv is None else fac * lv; seg *= fac   # pieces from different takes at one level (active-speech RMS)
    seg = seg.astype(np.float32)
    if abs(tp - 1) > .01: seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tp:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, np.float32)
    f = int(SR * .005); seg = seg.copy(); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)   # fades again after atempo (its last samples clicked at 0.69 s)
    i0 = int((at - PAD / tp) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]
    print(f"{name:16s} {('A' if take == A else ('B' if a < 11 else 'C'))} {a:5.2f}-{b:5.2f}  at {at:.2f}-{at + (b - a) / tp:.2f} s  tempo {tp:.2f}")
f = int(SR * .01); mx = mx.copy(); mx[:f] *= np.linspace(0, 1, f); mx[-f:] *= np.linspace(1, 0, f)
w = int(SR * .01); em = np.array([np.sqrt((mx[i:i + w] ** 2).mean()) for i in range(0, len(mx) - w, w)])
i0 = int((MARCEL_AT - float(np.argmax(em > em.max() * 0.1)) * 0.01) * SR); k = min(len(mx), len(track) - i0); track[i0:i0 + k] += mx[:k] * MARCEL_GAIN
print("Marcel 'Pardon, Sire!' speech starts at", MARCEL_AT, "s")
open(SC + "c09L_voice.f32", "wb").write(track.tobytes())
meas = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c09L_voice.f32", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])           # one constant gain to -14 LUFS (a single-pass loudnorm + 2 ms limiter put clicks into the voice)
vf = "scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p"
fc = f"[0:v]{vf}[vv];[1:a]volume={-14 - I:.2f}dB,alimiter=limit=0.84:attack=5:release=80:level=disabled[v]"
print("voice", I, "LUFS -> gain", round(-14 - I, 2), "dB")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c09L_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]",
                "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", f"frames/C09L_final_{V}.mp4"], check=True)
r = np.frombuffer(open(SC + "sep/lite_c09_rest.f32", "rb").read(), np.float32).reshape(-1, 2)
r = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", "-", "-ar", str(SR), "-f", "f32le", "-"], input=r.tobytes(), capture_output=True).stdout, np.float32)
open(SC + f"lite_c09_rest_{V}.f32", "wb").write(r.astype(np.float32).tobytes())
