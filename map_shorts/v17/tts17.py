"""Free voice (Kokoro). Builds voice_raw.wav + timing.json for script17."""
import json, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from script17 import LINES, MAPW
k = Kokoro("assets/kokoro.onnx", "assets/voices.bin")
SR = 24000
GAP = 0.12
parts, D, T, starts = [], [], [], []
t = 0.0
for i, line in enumerate(LINES):
    spoken = " ".join(MAPW.get(w, w) for w in line.split())
    a, sr = k.create(spoken, voice="am_michael", speed=1.1, lang="en-us")
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 400): idx[-1] + 1200]
    dur = len(a) / sr
    words = line.split()
    wts = [len(re.sub(r"\W", "", w)) + 1.5 + (2.5 if w[-1] in ",.?!" else 0) for w in words]
    tot = sum(wts); acc = 0.0; offs = []
    for w in wts:
        offs.append(0.05 + acc / tot * (dur - 0.2)); acc += w
    starts.append(t); D.append(dur); T.append(offs)
    parts.append(a); parts.append(np.zeros(int(GAP * sr)))
    t += dur + GAP
sf.write("voice_raw.wav", np.concatenate(parts), SR)
json.dump({"starts": starts, "D": D, "T": T}, open("timing.json", "w"))
print("total", round(t, 1), [round(d, 1) for d in D])
