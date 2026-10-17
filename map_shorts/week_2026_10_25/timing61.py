"""timing.json from Lumean alignment.csv for one Short: python3 timing60.py <key> (run in /home/claude/v60/<key>)."""
import csv, json, re, sys, unicodedata
sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/week_2026_10_25")
from scripts import SHORTS
LINES = SHORTS[sys.argv[1]]["lines"]
norm0 = lambda c: unicodedata.normalize("NFKD", c).encode("ascii", "ignore").decode().lower() or c.lower()
rows = list(csv.DictReader(open("lumean/alignment.csv")))
chars = [(r["char"], float(r["start"]), float(r["end"])) for r in rows]
alnum = [(i, norm0(c)) for i, (c, _, _) in enumerate(chars) if c.isalnum()]
norm = lambda s: re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())
k = 0; starts, D, T = [], [], []
for line in LINES:
    wt = []; first = last = None
    for w in line.split():
        n = norm(w)
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
print(sys.argv[1], [round(s, 1) for s in starts], "end", round(starts[-1] + D[-1], 1))
