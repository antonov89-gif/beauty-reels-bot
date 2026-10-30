"""C09 from the Seedance 2.5 Lite r2v take (seedance25lite_c09r2v.mp4, owner 30.10: "Видео намного лучше"): our locked voice laid as WHOLE phrases from takes A/B/C (no slowing down, speed-up at most 1.3, cuts only in pauses) on the model's own speech timing, Marcel's "Pardon, Sire!" while the hat falls. Free (local).
Model speech / lips (lip_measure.py): Lower 1.88-2.21 (lips 1.83-2.04) | Lower 3.21-3.83 (lips 3.25-3.67) | hat slips 3.6, lands 4.3 | head turned 4.67-5.62 | And there goes the hat 5.06-5.88 (lips "the hat" 5.62-5.88) | Eyes on me, not on the hat 6.75-7.75 (lips 6.67-6.92, 7.54-7.83).
Usage: python3 build_c09r2v.py -> frames/C09R_final_A.mp4 (1080x1920, voices only) + scratchpad lite_c09r2v_rest_A.f32 (model sounds)"""
import subprocess, numpy as np
V = "A"; SR = 48000; MODEL = "frames/seedance25lite_c09r2v.mp4"
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
A, BC = "../voice/tts_ep1/C09.mp3", "../voice/tts_ep1/C09b-C09c.mp3"
MARCEL_AT = 4.00; MARCEL_GAIN = 0.6                    # speech onset of "Pardon, Sire!" while the hat tumbles, before the king's next line (4.87)
# name, take, speech start/end in the take (pauses on both sides), speech start in the clip, tempo
PIECES = [("Lower!",                      A, 0.16, 0.67, 1.85, 1.30),
          ("Lower!",                      A, 1.10, 1.75, 3.21, 1.20),   # x1.2: ends 3.75 with the lips (3.67) instead of 3.86
          ("And there goes the hat.",     A, 2.27, 3.40, 4.87, 1.00),   # "And there goes" while his head is turned away (4.67-5.62), "the hat" on the lips 5.55-6.0
          ("Eyes on me, not on the hat.", A, 3.87, 5.40, 6.66, 1.30)]


def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)


takes = {A: load(A), BC: load(BC)}; mx = load("../voice/tts_ep1/marcel_C09_pardon.mp3")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MODEL], capture_output=True, text=True).stdout)
track = np.zeros(int(SR * (dur + 0.3)), np.float32)
for name, take, a, b, at, tp in PIECES:
    PAD = 0.03
    seg = takes[take][int((a - PAD) * SR):int((b + PAD) * SR)].copy(); f = int(SR * .01); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    if abs(tp - 1) > .01: seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tp:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, np.float32).copy()
    f = int(SR * .005); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    i0 = int((at - PAD / tp) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]
    print(f"{name:28s} at {at:.2f}-{at + (b - a) / tp:.2f} s  tempo {tp:.2f}")
f = int(SR * .01); mx = mx.copy(); mx[:f] *= np.linspace(0, 1, f); mx[-f:] *= np.linspace(1, 0, f)
w = int(SR * .01); em = np.array([np.sqrt((mx[i:i + w] ** 2).mean()) for i in range(0, len(mx) - w, w)])
i0 = int((MARCEL_AT - float(np.argmax(em > em.max() * 0.1)) * 0.01) * SR); k = min(len(mx), len(track) - i0); track[i0:i0 + k] += mx[:k] * MARCEL_GAIN
print("Marcel 'Pardon, Sire!' speech starts at", MARCEL_AT, "s")
open(SC + "c09R_voice.f32", "wb").write(track.tobytes())
meas = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c09R_voice.f32", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])   # one constant gain to -14 LUFS + soft limiter (no single-pass loudnorm: it clicked)
vf = "scale=1080:1920:flags=lanczos,setsar=1,fps=24,format=yuv420p"
fc = f"[0:v]{vf}[vv];[1:a]volume={-14 - I:.2f}dB,alimiter=limit=0.84:attack=5:release=80:level=disabled[v]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c09R_voice.f32", "-filter_complex", fc, "-map", "[vv]", "-map", "[v]",
                "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", f"frames/C09R_final_{V}.mp4"], check=True)
r = np.frombuffer(open(SC + "sep/lite_c09r2v_rest.f32", "rb").read(), np.float32).reshape(-1, 2)
r = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", "-", "-ar", str(SR), "-f", "f32le", "-"], input=r.tobytes(), capture_output=True).stdout, np.float32)
open(SC + f"lite_c09r2v_rest_{V}.f32", "wb").write(r.astype(np.float32).tobytes())
