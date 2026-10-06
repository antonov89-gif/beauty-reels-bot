"""Free offline narration with Kokoro (am_michael); writes lumean-compatible timing.json + voice track."""
import json, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
from script13 import LINES
k = Kokoro("/home/claude/v10/assets/kokoro.onnx", "/home/claude/v10/assets/voices.bin")
MAPW = {"1703,": "seventeen oh three,", "2007": "two thousand seven", "Moët": "Mo-ett", "Nestlé.": "Nestlay.",
        "Société": "Sosiety", "Bains": "Ban", "Mer": "Mair", "M-Pesa": "M Pesa", "ICTSI.": "I C T S I.",
        "ASML": "A S M L", "TSMC": "T S M C", "LVMH,": "L V M H,", "OCP": "O C P", "MHP": "M H P",
        "AB": "A B", "InBev": "In Bev", "Itaipu": "Ee-tie-poo", "Inditex,": "Inditex,"}
SR = 24000
voice, starts, D, T = [], [], [], []
t = 0.4
for i, line in enumerate(LINES):
    spoken = " ".join(MAPW.get(w, w) for w in line.split())
    a, sr = k.create(spoken, voice="am_michael", speed=1.0, lang="en-us")
    idx = np.where(np.abs(a) > 0.01)[0]
    a = a[max(0, idx[0] - 600): idx[-1] + 2000]
    dur = len(a) / sr
    words = line.split()
    wts = [len(re.sub(r"\W", "", w)) + 1.5 + (2.5 if w[-1] in ",.?!" else 0) for w in words]
    tot = sum(wts); acc = 0.0; offs = []
    for w in wts:
        offs.append(0.05 + acc / tot * (dur - 0.2)); acc += w
    starts.append(t); D.append(dur); T.append(offs)
    voice.append(np.zeros(int((t - (sum(len(v) for v in voice) / sr)) * sr)))
    voice.append(a)
    t += dur + 0.7
    print(i, round(dur, 1), flush=True)
v = np.concatenate(voice)
sf.write("voice_kokoro.wav", v, SR)
json.dump({"starts": [s - 0.4 + 0.0 for s in starts], "D": D, "T": T, "voice": "voice_kokoro.wav", "voice_offset": 0.4},
          open("timing.json", "w"))
print("total", round(len(v) / SR, 1))
