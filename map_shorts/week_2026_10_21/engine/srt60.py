"""SRT (one cue per spoken line, 2 lines max). SHORT=<key> python3 srt60.py"""
import textwrap
import engine60 as V
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"
out = []
for i, line in enumerate(V.LINES):
    a = V.ST[i]; b = V.ST[i] + V.D[i] + 0.15
    out.append(f"{i + 1}\n{ts(a)} --> {ts(b)}\n" + "\n".join(textwrap.wrap(line, 44)) + "\n")
open(f"{V.SHORT}/{V.SHORT}.srt", "w").write("\n".join(out)); print(V.SHORT, "srt", len(out))
