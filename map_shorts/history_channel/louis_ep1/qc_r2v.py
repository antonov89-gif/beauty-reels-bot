"""QC of one r2v clip (voice trial v4): ASR words with probabilities, speaker similarity to C09/C10/C12 model voices and to the v3 locked voice, lips vs the model's own speech, music check on the non-speech stem.
Usage: python3 qc_r2v.py C12   (needs scratchpad sep/lite_<clip>r2v_{vocals,rest}.f32, <scratchpad>/<clip>r2v/model.wav, mouth.json)"""
import json, subprocess, sys, numpy as np
from faster_whisper import WhisperModel
from resemblyzer import VoiceEncoder, preprocess_wav
c = sys.argv[1]; low = c.lower()
SP = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
m = WhisperModel("medium", device="cpu", compute_type="int8")
for beam in (5, 1):
    s, _ = m.transcribe(SP + f"{low}r2v/model.wav", word_timestamps=True, language="en", beam_size=beam)
    print("ASR", beam, " ".join(f"{w.word.strip()}[{w.start:.2f}]({w.probability:.2f})" for x in s for w in x.words))
def stem(name):
    v = np.frombuffer(open(SP + f"sep/{name}_vocals.f32", "rb").read(), np.float32).reshape(-1, 2).mean(1)
    y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "1", "-i", "-", "-ar", "16000", "-f", "f32le", "-"], input=v.tobytes(), capture_output=True).stdout, np.float32)
    return preprocess_wav(y, source_sr=16000)
def load(p):
    return preprocess_wav(np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32), source_sr=16000)
enc = VoiceEncoder("cpu"); me = enc.embed_utterance(stem(f"lite_{low}r2v"))
others = {"C09 model": stem("lite_c09r2v"), "C10 model": stem("lite_c10r2v")}
import os
if c != "C12" and os.path.exists(SP + "sep/lite_c12r2v_vocals.f32"): others["C12 model"] = stem("lite_c12r2v")
print("speaker similarity of the", c, "model voice to:", {k: round(float(me @ enc.embed_utterance(v)), 2) for k, v in others.items() if k.split()[0] != c},
      "| v3 locked take of this clip:", round(float(me @ enc.embed_utterance(load(f"../voice/tts_ep1/{c}.mp3"))), 2), "| v3 C09 take A:", round(float(me @ enc.embed_utterance(load("../voice/tts_ep1/C09.mp3"))), 2))
mo = json.load(open(SP + f"{low}r2v/mouth.json")); t = np.array([r[0] for r in mo]); lip = np.array([np.nan if r[1] is None else r[1] for r in mo])
v = np.frombuffer(open(SP + f"sep/lite_{low}r2v_vocals.f32", "rb").read(), np.float32).reshape(-1, 2).mean(1); sr = 44100
def env_at(ts, win=0.04): return np.array([np.sqrt((v[int(max(0, a - win) * sr):int((a + win) * sr)] ** 2).mean() + 1e-12) for a in ts])
r = []
for lag in np.arange(-0.4, 0.401, 0.04):
    ts = t + lag; ok = ~np.isnan(lip) & (ts > 0) & (ts < len(v) / sr - 0.05)
    r.append((np.corrcoef(lip[ok], np.sqrt(env_at(ts[ok])))[0, 1], lag))
cc, l = max(r); print(f"lips vs the model's speech: best lag {l:+.2f} s corr {cc:.2f} | lag 0 {[q for q in r if abs(q[1]) < 1e-6][0][0]:.2f}; frames with a face {int((~np.isnan(lip)).sum())} of {len(lip)}")
rs = np.frombuffer(open(SP + f"sep/lite_{low}r2v_rest.f32", "rb").read(), np.float32).reshape(-1, 2).mean(1); h = int(44100 * .5)
print("non-speech stem per 0.5 s dBFS:", " ".join(f"{20 * np.log10(np.sqrt((rs[i:i + h] ** 2).mean()) + 1e-9):.0f}" for i in range(0, len(rs) - h, h)))
