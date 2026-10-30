"""C01 v3 from the Kling 4.0 i2v take (frames/kling40_c01i2v.mp4) with OUR locked voice laid over it (owner 30.10: "Поверх этого голоса сделай попробуй, убавить до минимума и наложить"): Kling's own voice is taken out with the htdemucs vocals stem (the non-speech stem with the phone knock and rustle stays),
our v3 line (voice/tts_ep1/C01.mp3) is laid as WHOLE phrases cut in the pauses, no slowing down, speed-up at most 1.3 (the C09 rule after the owner rejected a word-sliced voice: "Нет это ужасно"), each phrase placed on the start of the same phrase in Kling's speech (its lips follow its own speech: lag 0.00 s, corr 0.71).
Kling speech runs (vocals stem, pauses >= 0.3 s): 0.30-1.65 "Oops, the ceiling." (off screen, the face is in frame from 2.2 s) | 2.40-2.80 "There." | 3.90-4.50 "Bonjour." | 5.25-7.15 "I am Louis, King of France." | 8.00-9.50 "They call me the Sun King." | 10.75-11.20 "Yes," | 11.55-12.45 "I'm that handsome."
Our line (silences >= 0.2 s): 0-1.50 | 1.98-2.39 | 2.90-3.52 | 3.84-5.56 (one piece, inner gap 0.24 s) | 5.98-7.67 | Yes, 8.20-8.9 | I'm that handsome 9.25-10.45.
Usage: python3 build_c01_kling_ourvoice.py [tag] -> frames/C01K_ourvoice_<tag>.mp4 (video stream copied, 1076x1924) + scratchpad c01K_voice.f32. Free (local)."""
import subprocess, sys, numpy as np
TAG = sys.argv[1] if len(sys.argv) > 1 else "A"; SR = 48000; MODEL = "frames/kling40_c01i2v.mp4"
SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
LINE = "../voice/tts_ep1/C01.mp3"
# name, speech start/end in our take (inside the pauses), start of the same phrase in Kling's speech (clip seconds), tempo (>= 1.0)
PIECES = [("Oops, the ceiling.",          0.00, 1.50, 0.30, 1.10),
          ("There.",                     1.98, 2.39, 2.40, 1.00),
          ("Bonjour.",                   2.90, 3.52, 3.90, 1.00),
          ("I am Louis, King of France.", 3.84, 5.56, 5.25, 1.00),
          ("They call me the Sun King.", 5.98, 7.67, 8.00, 1.13),
          ("Yes,",                       8.20, 8.90, 10.75, 1.30),
          ("I'm that handsome.",         9.25, 10.45, 11.55, 1.30)]


def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)


take = load(LINE)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", MODEL], capture_output=True, text=True).stdout)
track = np.zeros(int(SR * (dur + 0.3)), np.float32)
for name, a, b, at, tp in PIECES:
    PAD = 0.03
    i_a = int((a - PAD) * SR); lead = 0
    if i_a < 0: lead = -i_a; i_a = 0
    seg = np.concatenate([np.zeros(lead, np.float32), take[i_a:int((b + PAD) * SR)]]).copy(); f = int(SR * .01); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    if abs(tp - 1) > .01: seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tp:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, np.float32).copy()
    f = int(SR * .005); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    i0 = int((at - PAD / tp) * SR); k = min(len(seg), len(track) - i0); track[i0:i0 + k] += seg[:k]
    print(f"{name:28s} at {at:.2f}-{at + (b - a) / tp:.2f} s  tempo {tp:.2f}")
open(SC + "c01K_voice.f32", "wb").write(track.tobytes())
meas = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", SC + "c01K_voice.f32", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float([l for l in meas.splitlines() if l.strip().startswith("I:")][-1].split()[1])
# Kling's own non-speech stem (phone knock, rustle) as it is, our voice at the loudness of Kling's speech stem, one constant gain + soft limiter at the end (no single-pass loudnorm: it clicked)
rest = np.frombuffer(open(SC + "sep/k40_c01i2v_rest.f32", "rb").read(), np.float32).reshape(-1, 2)
rest = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", "-", "-ar", str(SR), "-f", "f32le", "-"], input=rest.tobytes(), capture_output=True, check=True).stdout, np.float32).reshape(-1, 2)
voc = np.frombuffer(open(SC + "sep/k40_c01i2v_vocals.f32", "rb").read(), np.float32).reshape(-1, 2).mean(1)
vm = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", "44100", "-ac", "1", "-i", "-", "-af", "ebur128", "-f", "null", "-"], input=voc.tobytes(), capture_output=True).stderr.decode()
KLING_VOICE_LUFS = float([l for l in vm.splitlines() if l.strip().startswith("I:")][-1].split()[1])
n = min(len(track), len(rest)); st = rest[:n].copy(); st += (track[:n] * 10 ** ((KLING_VOICE_LUFS - I) / 20))[:, None]
open(SC + "c01K_mix.f32", "wb").write(st.astype(np.float32).tobytes())
m2 = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", SC + "c01K_mix.f32", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
I2 = float([l for l in m2.splitlines() if l.strip().startswith("I:")][-1].split()[1])
print(f"our voice {I:.1f} LUFS -> {KLING_VOICE_LUFS:.1f} (Kling's speech stem); mix {I2:.1f} LUFS -> -14 LUFS gain {-14 - I2:.2f} dB")
fc = f"[1:a]volume={-14 - I2:.2f}dB,alimiter=limit=0.84:attack=5:release=80:level=disabled[a]"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", MODEL, "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", SC + "c01K_mix.f32", "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-shortest", f"frames/C01K_ourvoice_{TAG}.mp4"], check=True)
print(f"frames/C01K_ourvoice_{TAG}.mp4")
