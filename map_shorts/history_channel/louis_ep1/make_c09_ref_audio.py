"""Reference audio for C09 on Seedance 2.5 Lite r2v (audio-driven lips): the king's locked line from take A (tts_ep1/C09.mp3, the take the owner already heard), cut ONLY in its pauses and laid at natural speed on an 8-s timeline with room for the action:
Lower! 0.25 | Lower! 1.15 | (1.8-2.9 the hat slips and rolls, Marcel's "Pardon, Sire!" goes in later in the edit, not into the reference) | And there goes the hat. 2.95 | (he turns back, yanks the phone) | Eyes on me, not on the hat. 5.70 | end 8.0 s.
Output: voice/tts_ep1/C09_ref8s.wav (48 kHz mono). The same file is the king's voice of the final mix, so nothing is stretched afterwards. Free (local)."""
import subprocess, numpy as np
SR = 48000; A = "../voice/tts_ep1/C09.mp3"
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", A, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32)
PH = [(0.16, 0.67, 0.25), (1.10, 1.75, 1.15), (2.27, 3.40, 2.95), (3.87, 5.40, 5.70)]   # speech start/end in take A (pauses on both sides), start in the clip
out = np.zeros(SR * 8, np.float32)
for a, b, at in PH:
    pad = 0.05; seg = x[int((a - pad) * SR):int((b + pad) * SR)].copy(); f = int(SR * .01); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    i0 = int((at - pad) * SR); out[i0:i0 + len(seg)] += seg[:len(out) - i0]
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", "../voice/tts_ep1/C09_ref8s.wav"], input=out.tobytes(), check=True)
print("written voice/tts_ep1/C09_ref8s.wav, 8.0 s")
