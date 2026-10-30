"""Episode 1 assembly, step 1 (owner 30.10 "Делай"): voice-only clip files for the clips made after the C01-C08 cut, in the same form as the older finals
(1080x1920, 24 fps, mono 48 kHz voice at about -15.8 LUFS, like C02L_final_A ... C08_final_lcut) plus the video model's own sounds as 48 kHz stereo f32 for build_ep1.py.
- C01 = Kling 4.0 picture + our v3 voice (build_c01_kling_ourvoice.py, owner "Нормально"): voice = scratchpad c01K_voice.f32, sounds = Kling's htdemucs non-speech stem.
- C09, C10, C12-C15 = Seedance 2.5 Lite r2v takes with the model's own voice (trial v4): voice = htdemucs vocals stem, sounds = non-speech stem.
- C11 = the dressing burst: stills B1-B8 (heel, rings, powder puff, hand mirror, sun brooch, lace cravat, comb, cuff), 1 s each, slow push-in with a small hand-held drift, hard cuts, silent track.
Usage: python3 prep_ep1_clips.py -> frames/C01K_final_A.mp4, frames/C09R_final.mp4 ... frames/C15R_final.mp4, frames/C11_burst.mp4 + scratchpad <name>_rest48.f32. Free (local)."""
import subprocess, numpy as np
SR = 48000; F = "frames/"; SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
TARGET = -15.8                                                         # mono voice-only level of the older finals (measured C02L-C08: -15.0...-16.5)
FIT = "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,fps=24,format=yuv420p"   # 720x1278 / 1076x1924 -> 1080x1920 without stretching


def lufs_mono(x):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "ebur128", "-f", "null", "-"], input=x.astype(np.float32).tobytes(), capture_output=True).stderr.decode()
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def stem48(path, ch):                                                  # htdemucs stem (44.1 kHz stereo f32) -> 48 kHz, ch channels
    x = np.frombuffer(open(path, "rb").read(), np.float32)
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "2", "-i", "-", "-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"], input=x.tobytes(), capture_output=True, check=True).stdout, np.float32).copy()


def make(name, video, voice, rest):
    g = TARGET - lufs_mono(voice); v = voice * 10 ** (g / 20); pk = np.abs(v).max()
    open(SC + name + "_voice48.f32", "wb").write(v.astype(np.float32).tobytes())        # linear, unclipped: build_ep1.py reads THIS (the limiter is applied once, on the final mix)
    open(SC + name + "_rest48.f32", "wb").write(rest.astype(np.float32).tobytes())
    raw = SC + name + "_voice48_prev.f32"; open(raw, "wb").write((v if pk < 0.89 else np.tanh(v / 0.89) * 0.89).astype(np.float32).tobytes())   # the mp4's own track is a preview only
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", video, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", raw, "-map", "0:v", "-map", "1:a", "-vf", FIT,
                    "-c:v", "libx264", "-crf", "16", "-c:a", "aac", "-b:a", "320k", "-shortest", F + name + ".mp4"], check=True)
    print(f"{name}: voice gain {g:+.1f} dB, peak {pk:.2f}")


make("C01K_final_A", F + "kling40_c01i2v.mp4", np.frombuffer(open(SC + "c01K_voice.f32", "rb").read(), np.float32).copy(), stem48(SC + "sep/k40_c01i2v_rest.f32", 2))
for c in ("c09", "c10", "c12", "c13", "c14", "c15"):
    make(f"{c.upper()}R_final", F + f"seedance25lite_{c}r2v.mp4", stem48(SC + f"sep/lite_{c}r2v_vocals.f32", 1), stem48(SC + f"sep/lite_{c}r2v_rest.f32", 2))

# C11 burst
parts = []
for i in range(1, 9):
    out = SC + f"burst_{i}.mp4"; d = 24                                                    # 1 s = 24 frames, push-in 1.00 -> 1.07, small drift
    z = f"zoompan=z='1+0.07*on/{d}':x='iw/2-(iw/zoom/2)+{(-1) ** i * 6}*on/{d}+3*sin(on/2.7)':y='ih/2-(ih/zoom/2)+2*cos(on/3.1)':d={d}:s=1080x1920:fps=24"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", "1", "-i", F + f"B{i}.jpg", "-vf", f"scale=1404:2516:flags=lanczos,{z},setsar=1,format=yuv420p", "-frames:v", str(d),
                    "-c:v", "libx264", "-crf", "16", out], check=True)
    parts.append(out)
lst = SC + "burst_list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", F + "C11_burst.mp4"], check=True)
print("C11_burst: 8 x 1 s")
