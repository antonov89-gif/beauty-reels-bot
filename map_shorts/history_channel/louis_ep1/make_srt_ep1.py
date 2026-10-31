"""English closed captions for episode 1 (upload to the platform, off by default; no burned-in captions by the channel rule).
Text = the script lines (voice/lines_ep1_emotion.json, normal spelling, tags and pauses removed); timing = faster-whisper word timestamps on the final file, mapped sentence by sentence in order.
Usage: python3 make_srt_ep1.py frames/EP1_full_D.mp4 EP1_en.srt. Free (local)."""
import json, re, subprocess, sys
from faster_whisper import WhisperModel
P, OUT = sys.argv[1], sys.argv[2]; SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"
starts = [(l.split()[0], float(l.split()[1])) for l in open(SC + "ep1_starts.txt")]
lines = json.load(open("../voice/lines_ep1_emotion.json"))["lines"]
wav = SC + "srt16.wav"; subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", P, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
m = WhisperModel("medium", device="cpu", compute_type="int8"); s, _ = m.transcribe(wav, word_timestamps=True, language="en", beam_size=5)
W = [(w.start, w.end) for seg in s for w in seg.words]


def ts(t):
    h, r = divmod(max(0, t), 3600); mi, se = divmod(r, 60); return f"{int(h):02d}:{int(mi):02d}:{int(se):02d},{int(round((se - int(se)) * 1000)):03d}"


cues = []
for i, (c, a) in enumerate(starts):
    if c not in lines or c == "C11": continue
    b = starts[i + 1][1]; ws = [w for w in W if a <= w[0] < b]
    text = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]|\{\{[^}]*\}\}", " ", lines[c])).strip()
    sents = [x.strip() for x in re.split(r"(?<=[.!?])\s+", text) if x.strip()]
    n = [len(x.split()) for x in sents]; tot = sum(n); k = 0
    for sent, cnt in zip(sents, n):
        j0 = min(len(ws) - 1, round(k * len(ws) / tot)); j1 = min(len(ws) - 1, max(j0, round((k + cnt) * len(ws) / tot) - 1)); k += cnt
        if not ws: continue
        cues.append((ws[j0][0], max(ws[j1][1], ws[j0][0] + 0.6), sent, c))
merged = []                                                             # short pieces of one clip ("Bow." "Lower." "Good.") read better as one cue
for q in cues:
    if merged and merged[-1][3] == q[3] and (merged[-1][1] - merged[-1][0] < 0.9 or q[1] - q[0] < 0.9) and len(merged[-1][2]) + len(q[2]) + 1 <= 42:
        merged[-1] = (merged[-1][0], q[1], merged[-1][2] + " " + q[2], q[3])
    else: merged.append(q)
cues = merged
out = []
for i, (t0, t1, txt, _) in enumerate(cues):
    t1 = min(t1 + 0.15, cues[i + 1][0] - 0.02) if i + 1 < len(cues) else t1 + 0.3
    if len(txt) > 42:                                                   # two lines, split near the middle on a space
        mid = len(txt) // 2; cut = min((abs(p - mid), p) for p in [q.start() for q in re.finditer(" ", txt)])[1]; txt = txt[:cut] + "\n" + txt[cut + 1:]
    out.append(f"{i + 1}\n{ts(t0)} --> {ts(t1)}\n{txt}\n")
open(OUT, "w").write("\n".join(out)); print(OUT, len(out), "cues")
