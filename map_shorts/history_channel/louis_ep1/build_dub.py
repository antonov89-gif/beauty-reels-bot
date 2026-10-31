"""Dub voice tracks for episode 1 (owner 31.10 "Делай": French, Spanish, Russian in the locked voice, Lumean orders 0.96 / 0.95 / 0.92 RUB).
Each language file (voice/tts_ep1/dub_<lang>.mp3, clips joined by 2-s pauses) is cut into the 14 clips; in every clip the dub phrases (voiced runs between pauses >= 0.18 s)
are laid on the English phrases of the final cut (which sit on the lips): same order, phrase start on phrase start, no slowing down, speed-up at most 1.3, no overlap.
If the counts differ, the closest neighbouring runs are merged until they match. Output: <scratchpad>/dub_<lang>_<clip>.f32 (mono 48 kHz, -15.8 LUFS) for build_ep1.py (DUB=<lang>).
Usage: python3 build_dub.py fr|es|ru. Free (local)."""
import subprocess, sys, numpy as np
SR = 48000; SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"; F = "frames/"; TARGET = -15.8
lang = sys.argv[1]
CLIPS = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C12", "C13", "C14", "C15"]
EN = {"C01": SC + "C01K_final_A_voice48.f32", "C02": F + "C02L_final_A.mp4", "C03": F + "C03L_final_A.mp4", "C04": F + "C04L_final_A.mp4", "C05": F + "C05L_final_A.mp4",
      "C06": F + "C06_final.mp4", "C07": F + "C07_final.mp4", "C08": F + "C08_final_lcut.mp4"}
EN.update({c: SC + f"{c}R_final_voice48.f32" for c in ("C09", "C10", "C12", "C13", "C14", "C15")})


def load(p):
    if p.endswith(".f32"): return np.frombuffer(open(p, "rb").read(), np.float32).copy()
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32).copy()


def env(x): w = SR // 100; return np.array([np.sqrt((x[i:i + w] ** 2).mean()) for i in range(0, len(x) - w, w)])


def runs(x, gap=0.18, thr=0.03):
    e = env(x); q = e > e.max() * thr; out = []; i = 0
    while i < len(q):
        j = i
        while j < len(q) and q[j] == q[i]: j += 1
        if q[i]:
            if out and i / 100 - out[-1][1] < gap: out[-1][1] = j / 100
            else: out.append([i / 100, j / 100])
        i = j
    return [r for r in out if r[1] - r[0] >= 0.08]


def merge_to(rs, n):                                                    # merge the two neighbours with the smallest gap until len == n
    rs = [list(r) for r in rs]
    while len(rs) > n:
        k = min(range(len(rs) - 1), key=lambda i: rs[i + 1][0] - rs[i][1]); rs[k][1] = rs[k + 1][1]; del rs[k + 1]
    return rs


def lufs(x):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "ebur128", "-f", "null", "-"], input=x.astype(np.float32).tobytes(), capture_output=True).stderr.decode()
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])


dub = load(f"../voice/tts_ep1/dub_{lang}.mp3"); e = env(dub); q = e > e.max() * 0.02; seps = []; i = 0
while i < len(q):
    j = i
    while j < len(q) and q[j] == q[i]: j += 1
    if not q[i] and (j - i) / 100 >= 1.2: seps.append((i + j) / 200)
    i = j
assert len(seps) == len(CLIPS) - 1, f"{lang}: {len(seps)} separators"
bounds = [0.0] + seps + [len(dub) / SR]
for n, c in enumerate(CLIPS):
    seg = dub[int(bounds[n] * SR):int(bounds[n + 1] * SR)]; ref = load(EN[c])
    rd, re_ = runs(seg, gap=0.25, thr=0.04), runs(ref, gap=0.25, thr=0.06); k = min(len(rd), len(re_)); rd, re_ = merge_to(rd, k), merge_to(re_, k)   # the phrases made by the {{pause}} marks (same marks in both lines)
    track = np.zeros(len(ref) + SR, np.float32); placed = []
    for m in range(k):
        a, b = rd[m]; ea, eb = re_[m]
        tp = float(np.clip((b - a) / max(0.15, eb - ea), 1.0, 1.3))
        cut0 = 0.0 if m == 0 else (rd[m - 1][1] + a) / 2; cut1 = len(seg) / SR if m == k - 1 else (b + rd[m + 1][0]) / 2
        placed.append([cut0, cut1, a, b, tp, ea, eb])
    st = lambda p: p[5]; en = lambda p: p[5] + (p[3] - p[2]) / p[4]
    for m in range(k - 2, -1, -1):                                      # no overlap: pull the earlier phrase back (max 0.45 s), then push the later one
        over = en(placed[m]) + 0.06 - st(placed[m + 1]); room = st(placed[m]) - (en(placed[m - 1]) + 0.06 if m > 0 else 0.0)
        if over > 0: d = min(over, max(0.0, room), 0.45); placed[m][5] -= d; placed[m][6] -= d
    for m in range(1, k):
        over = en(placed[m - 1]) + 0.06 - st(placed[m])
        if over > 0: placed[m][5] += over; placed[m][6] += over
    late = 0.0; cutoff = 0.0
    for cut0, cut1, a, b, tp, ea, eb in placed:
        cutoff = max(cutoff, ea + (b - a) / tp - len(ref) / SR)
        piece = seg[int(cut0 * SR):int(cut1 * SR)].copy(); f = int(SR * .01); piece[:f] *= np.linspace(0, 1, f); piece[-f:] *= np.linspace(1, 0, f)
        if abs(tp - 1) > .01: piece = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tp:.3f}", "-f", "f32le", "-"], input=piece.tobytes(), capture_output=True, check=True).stdout, np.float32).copy()
        f = int(SR * .005); piece[:f] *= np.linspace(0, 1, f); piece[-f:] *= np.linspace(1, 0, f)
        at = ea - (a - cut0) / tp; i0 = int(max(0, at) * SR); kk = min(len(piece), len(track) - i0); track[i0:i0 + kk] += piece[:kk]
        late = max(late, (ea + (b - a) / tp) - eb)
    track = track[:len(ref)]; track *= 10 ** ((TARGET - lufs(track)) / 20)
    open(SC + f"dub_{lang}_{c}.f32", "wb").write(track.astype(np.float32).tobytes())
    print(f"{lang} {c}: phrases {k}; tempos {[round(p[4], 2) for p in placed]}; longest overrun past the English phrase {late:+.2f} s" + (f"; SPEECH CUT AT THE CLIP END by {cutoff:.2f} s" if cutoff > 0 else ""))
