import json, math, sys
sys.path.insert(0, '.')
from script20 import LINES
import engine20 as E

def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"

MAXCH, MAXL = 42, 2
SPOKEN_FIX = {'And your money has barely noticed.': 'And your money is barely noticed.'}  # what the voice really says
cues = []
for i, line in enumerate(LINES):
    line = SPOKEN_FIX.get(line, line)
    words = line.split()
    t0 = E.starts[i]
    tw = [t0 + o for o in E.TW[i]]
    end = t0 + E.D[i]
    # split into sentences, then into balanced pieces of <= 58 chars (no orphan words)
    sents, cur = [], []
    for w in words:
        cur.append(w)
        if w[-1] in ".?!":
            sents.append(cur); cur = []
    if cur:
        sents.append(cur)
    chunks = []
    for sw in sents:
        txt = " ".join(sw)
        n = max(1, math.ceil(len(txt) / 58))
        if n == 1:
            chunks.append(sw); continue
        # choose n-1 split points near equal char shares, preferring words that end with , ; :
        tot = len(txt); idx = []; acc = 0; lens = []
        for w in sw:
            acc += len(w) + 1; lens.append(acc)
        cuts = []
        for k in range(1, n):
            target = tot * k / n
            cand = [j for j in range(1, len(sw)) if abs(lens[j - 1] - target) < tot / n * 0.45]
            cand = sorted(cand, key=lambda j: (0 if sw[j - 1][-1] in ",;:" else 1, abs(lens[j - 1] - target)))
            cuts.append(cand[0] if cand else min(range(1, len(sw)), key=lambda j: abs(lens[j - 1] - target)))
        cuts = sorted(set(cuts)); prev = 0
        for c in cuts + [len(sw)]:
            if c > prev:
                chunks.append(sw[prev:c]); prev = c
    pos = 0
    for c in chunks:
        a = tw[pos]
        b = tw[pos + len(c)] - 0.04 if pos + len(c) < len(words) else end + 0.2
        pos += len(c)
        txt = " ".join(c)
        if len(txt) > MAXCH:  # balance into two lines
            mid = len(txt) // 2
            k = min((m for m in range(len(txt)) if txt[m] == " "), key=lambda m: abs(m - mid))
            txt = txt[:k] + "\n" + txt[k + 1:]
        cues.append([a, max(b, a + 0.6), txt])
for k in range(len(cues) - 1):  # no overlaps
    if cues[k][1] > cues[k + 1][0] - 0.02:
        cues[k][1] = cues[k + 1][0] - 0.02
with open("spend_100b_long.srt", "w", encoding="utf-8") as f:
    for n, (a, b, txt) in enumerate(cues, 1):
        f.write(f"{n}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
print(len(cues), "cues; last", ts(cues[-1][1]))
dur = [b - a for a, b, _ in cues]
print("min/avg/max dur", round(min(dur), 2), round(sum(dur) / len(dur), 2), round(max(dur), 2))
cps = [len(t.replace("\n", "")) / max(0.1, b - a) for a, b, t in cues]
print("max chars/sec", round(max(cps), 1), "avg", round(sum(cps) / len(cps), 1), "over 20 cps:", sum(1 for c in cps if c > 20))
