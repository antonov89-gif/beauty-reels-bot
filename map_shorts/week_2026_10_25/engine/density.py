import os, sys, importlib
k = sys.argv[1]; os.environ["SHORT"] = k
V = importlib.import_module("engine61")
idx = {"big": 3, "slam": 3, "counter": 5, "pin": 3, "geolabel": 3, "country": 1, "route": 1, "sroute": 1, "circle": 3, "flag": 4, "pill": 4, "tint": 2}
ev = [s[0] for s in V.SH[1:]]
seen = set()
for s in V.SH:
    for fn, a in s[3]:
        if id(a) in seen: continue
        seen.add(id(a))
        if fn in idx:
            t = a[idx[fn]]
            if fn == "counter" and a[0] == a[1]: continue
            ev.append(max(t, 0.0) if t >= 0 else None)
ev = sorted(e for e in ev if e is not None and e > 0.05)
T = V.TOTAL
w = [sum(1 for e in ev if a <= e < a + 10) for a in range(0, int(T - 9), 1)]
print(f"{k:13s} T={T:5.1f} events={len(ev):3d} avg/10s={len(ev)/T*10:4.1f} min window={min(w)} max gap={max(b-a for a,b in zip([0]+ev, ev+[T])):.1f}s")
