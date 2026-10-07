import textwrap, engine24 as E
def ts(x):
    h, m = int(x // 3600), int(x % 3600 // 60); s = x % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
out, n = [], 1
for i, l in enumerate(E.LINES):
    words = l.split(); tw = E.TW[i]
    # split long lines into halves at word timing
    chunks = [words] if len(l) <= 84 else [words[:len(words) // 2], words[len(words) // 2:]]
    idx = 0
    for c in chunks:
        a = E.ST[i] + tw[idx]; idx += len(c)
        b = E.ST[i] + (tw[idx] if idx < len(words) else E.D[i]) - 0.02
        out.append(f"{n}\n{ts(a)} --> {ts(b)}\n" + "\n".join(textwrap.wrap(" ".join(c), 42)) + "\n"); n += 1
open("new_year_first_last.srt", "w").write("\n".join(out)); print(n - 1, "cues")
