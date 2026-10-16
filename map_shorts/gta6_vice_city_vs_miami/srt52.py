import engine52 as E
def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)) % 1000:03d}"
out = []; n = 1
for i, l in enumerate(E.LINES):
    w = l.split(); T = E.TW[i]
    for c in range(0, len(w), 7):
        a = E.ST[i] + T[c]; b = E.ST[i] + (T[c + 7] - 0.05 if c + 7 < len(w) else E.D[i] + 0.1)
        out.append(f"{n}\n{ts(a)} --> {ts(b)}\n{' '.join(w[c:c + 7])}\n"); n += 1
open("gta6_vice_city_vs_miami.srt", "w").write("\n".join(out)); print(n - 1)
for k, s in enumerate(E.SH):
    if s[1] == "card": print(s[2][0], s[2][1], int(s[0] // 60), int(s[0] % 60))
print("leonida", E.BL[2], "count", E.BL[27], "finale", E.BL[28])
