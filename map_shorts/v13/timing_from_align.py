import csv, json, re
from script13 import LINES
rows = list(csv.DictReader(open("lumean/alignment.csv")))
chars = [(r["char"], float(r["start"]), float(r["end"])) for r in rows]
stream = "".join(c for c, _, _ in chars)
pos = 0
starts, D, T = [], [], []
def norm(s): return "".join(c for c in s.lower() if c.isalnum())
# index of alnum chars
alnum = [(i, c.lower()) for i, (c, _, _) in enumerate(chars) if c.isalnum()]
k = 0
for line in LINES:
    wt = []; first = last = None
    for w in line.split():
        n = norm(w)
        if not n: continue
        # find n in alnum sequence starting at k
        j = k
        while "".join(c for _, c in alnum[j:j + len(n)]) != n:
            j += 1
            if j > len(alnum): raise SystemExit(f"cannot find {w}")
        ci0, ci1 = alnum[j][0], alnum[j + len(n) - 1][0]
        wt.append(chars[ci0][1]); last = chars[ci1][2]
        if first is None: first = chars[ci0][1]
        k = j + len(n)
    starts.append(first); D.append(last - first); T.append([x - first for x in wt])
json.dump({"starts": starts, "D": D, "T": T, "audio": "lumean/result.mp3"}, open("timing.json", "w"))
for i, (s, d) in enumerate(zip(starts, D)): print(i, round(s, 2), round(d, 2))
