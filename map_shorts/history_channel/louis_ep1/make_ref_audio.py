"""Reference audio for a clip on Seedance 2.5 Lite r2v (voice trial v4, owner 30.10): the clip's whole line in the v3 locked voice (voice/tts_ep1/<CLIP>.mp3) at natural speed, placed at START seconds on a TOTAL-second timeline (silence around it).
Usage: python3 make_ref_audio.py C10 0.5 8 -> voice/tts_ep1/C10_ref8s.wav (48 kHz mono, gitignored, rebuild with this script). Free (local)."""
import subprocess, sys, numpy as np
clip, start, total = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); SR = 48000
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"../voice/tts_ep1/{clip}.mp3", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
w = int(SR * .01); e = np.array([np.sqrt((x[i:i + w] ** 2).mean()) for i in range(0, len(x) - w, w)]); on = np.flatnonzero(e > e.max() * 0.03)
a, b = max(0, on[0] * 0.01 - 0.05), min(len(x) / SR, (on[-1] + 1) * 0.01 + 0.15)            # the spoken part with a little air
seg = x[int(a * SR):int(b * SR)].copy(); f = int(SR * .01); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
assert start + len(seg) / SR <= total, f"line {len(seg) / SR:.2f} s does not fit"
out = np.zeros(int(SR * total), np.float32); i0 = int(start * SR); out[i0:i0 + len(seg)] = seg
name = f"../voice/tts_ep1/{clip}_ref{int(total)}s.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", name], input=out.tobytes(), check=True)
print(f"{name}: line {len(seg) / SR:.2f} s at {start:.2f}-{start + len(seg) / SR:.2f} of {total:.0f} s")
