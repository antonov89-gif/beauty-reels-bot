import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro("/home/claude/v10/assets/kokoro.onnx", "/home/claude/v10/assets/voices.bin")
L = [
 "What if we melted every bit of gold ever mined into one giant cube?",
 "Rings, coins, bars from every vault. About two hundred twenty thousand tonnes.",
 "The cube? Just twenty-two and a half meters wide. It fits between the legs of the Eiffel Tower.",
 "Now add all the gold still buried underground. Thirty percent more gold, but the cube grows by only two meters.",
 "Split it between eight point three billion people, and your share is about thirty-five grams.",
 "A cube smaller than a dice.",
 "Don't spend it all at once.",
]
tot = 0; words = 0
for sp in (1.0, 1.1):
    tot = 0
    for l in L:
        a, sr = k.create(l, voice="am_michael", speed=sp, lang="en-us")
        idx = np.where(np.abs(a) > 0.01)[0]; d = (idx[-1] - idx[0]) / sr
        tot += d
    words = sum(len(l.split()) for l in L)
    print("speed", sp, "speech s", round(tot, 1), "+gaps", round(tot + 0.3 * (len(L) - 1), 1), "words", words, "wpm", round(words / (tot + 0.3 * (len(L) - 1)) * 60))
