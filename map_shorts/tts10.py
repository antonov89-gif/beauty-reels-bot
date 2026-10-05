import json, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from script10 import LINES, MAPW
k = Kokoro("assets/kokoro.onnx", "assets/voices.bin")
D, T = [], []
for i, line in enumerate(LINES):
    spoken = " ".join(MAPW.get(w, w) for w in line.split())
    a, sr = k.create(spoken, voice="am_michael", speed=1.0, lang="en-us")
    # trim leading/trailing silence
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 800): idx[-1] + 2400]
    sf.write(f"voice/l{i:02d}.wav", a, sr)
    dur = len(a) / sr
    words = line.split()
    wts = [len(re.sub(r"\W", "", w)) + 1.5 + (2.5 if w[-1] in ",.?!" else 0) for w in words]
    tot = sum(wts); acc = 0.0; offs = []
    for w in wts:
        offs.append(0.08 + acc / tot * (dur - 0.25)); acc += w
    D.append(dur); T.append(offs)
    print(i, round(dur, 2), line)
json.dump({"D": D, "T": T, "sr": sr}, open("timing.json", "w"))
print("total", round(sum(D), 1))
