"""Fit a translated voice line-by-line into the English timing. python3 fit_ml.py es"""
import csv, json, subprocess, sys, os
import numpy as np, soundfile as sf
import engine52 as E
LANG = sys.argv[1]; SR = 44100; D0 = f"ml/lumean_{LANG}"
LINES = [l.strip() for l in open(f"ml/{LANG}.txt", encoding="utf-8") if l.strip()]
assert len(LINES) == E.N, (len(LINES), E.N)
rows = list(csv.DictReader(open(f"{D0}/alignment.csv", encoding="utf-8")))
chars = [(r["char"], float(r["start"]), float(r["end"])) for r in rows]
def norm(s): return "".join(c for c in s.lower() if c.isalnum())
alnum = [(i, c.lower()) for i, (c, _, _) in enumerate(chars) if c.isalnum()]
k = 0; starts, D, T = [], [], []
for line in LINES:
    wt = []; first = last = None
    for w in line.split():
        n = norm(w)
        if not n: continue
        j = k
        while "".join(c for _, c in alnum[j:j + len(n)]) != n:
            j += 1
            if j > len(alnum): raise SystemExit(f"cannot find {w}")
        wt.append(chars[alnum[j][0]][1]); last = chars[alnum[j + len(n) - 1][0]][2]
        if first is None: first = chars[alnum[j][0]][1]
        k = j + len(n)
    starts.append(first); D.append(last - first); T.append([x - first for x in wt])
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D0}/result.mp3", "-ar", str(SR), "-ac", "1", f"ml/raw_{LANG}.wav"], check=True)
a, _ = sf.read(f"ml/raw_{LANG}.wav")
N = int(E.TOTAL * SR) + SR; voice = np.zeros(N); cur_free = 0.0; place_st, tempos = [], []
for i in range(E.N):
    s0 = max(0.0, starts[i] - 0.04); s1 = starts[i] + D[i] + 0.15; seg = a[int(s0 * SR):int(s1 * SR)]; L = len(seg) / SR
    slot_end = (E.ST[i + 1] - 0.10) if i < E.N - 1 else E.TOTAL - 1.6
    st = max(E.ST[i] - 0.04, cur_free)
    if st + L > slot_end: st = max(cur_free, E.ST[i] - 0.7)
    tempo = min(1.3, max(1.0, L / max(0.5, slot_end - st)))
    if tempo > 1.001:
        sf.write("ml/_seg.wav", seg, SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "ml/_seg.wav", "-af", f"atempo={tempo:.4f}", "ml/_seg2.wav"], check=True)
        seg, _ = sf.read("ml/_seg2.wav")
    i0 = int(st * SR); e = min(N, i0 + len(seg)); voice[i0:e] += seg[:e - i0]
    cur_free = st + len(seg) / SR + 0.12; place_st.append(st + 0.04); tempos.append(tempo)
    print(i, f"slot {slot_end - E.ST[i]:5.1f}s  need {L:5.1f}s  tempo {tempo:.2f}  end {cur_free - 0.12:6.1f}" + ("  OVER" if cur_free - 0.12 > slot_end + 0.05 else ""))
sf.write(f"ml/voice_{LANG}.wav", voice, SR)
json.dump({"starts": place_st, "D": [d / t for d, t in zip(D, tempos)], "T": [[x / t for x in tw] for tw, t in zip(T, tempos)], "lines": LINES}, open(f"ml/timing_{LANG}.json", "w", encoding="utf-8"), ensure_ascii=False)
# subtitles
def ts(x):
    h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)) % 1000:03d}"
out = []; n = 1
for i, l in enumerate(LINES):
    w = l.split(); tw = [x / tempos[i] for x in T[i]]
    if len(tw) != len([x for x in w if norm(x)]): tw = None
    ws = [x for x in w if norm(x)]
    for c in range(0, len(ws), 7):
        if tw: a0 = place_st[i] + tw[c]; b0 = place_st[i] + (tw[c + 7] - 0.05 if c + 7 < len(ws) else D[i] / tempos[i] + 0.1)
        out.append(f"{n}\n{ts(a0)} --> {ts(b0)}\n{' '.join(ws[c:c + 7])}\n"); n += 1
open(f"ml/gta6_vice_city_vs_miami_{LANG}.srt", "w", encoding="utf-8").write("\n".join(out))
# mix with the same music + sfx as the English master
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"ml/voice_{LANG}.wav", "-i", "music.wav", "-i", "sfx.wav", "-filter_complex",
                "[0:a]asplit=2[v][vsc];[1:a]volume=0.5[m];[m][vsc]sidechaincompress=threshold=0.04:ratio=7:attack=8:release=350[md];"
                "[2:a]lowpass=f=9000,volume=0.6[s];[v][md][s]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.9,aresample=44100[a]",
                "-map", "[a]", "-t", str(E.TOTAL), "-c:a", "aac", "-b:a", "192k", f"ml/audio_{LANG}.m4a"], check=True)
print("done", LANG, "max tempo", round(max(tempos), 2), "mean", round(sum(tempos) / len(tempos), 3))
