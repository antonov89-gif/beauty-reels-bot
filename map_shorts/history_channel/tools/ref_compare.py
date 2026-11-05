"""Reference comparator (owner 05.11): measures a clip / edit / whole video of the history channel against the reference Vlog 1 gate and prints a table
reference / ours / verdict. Free, read-only. Needs /tmp/fv (opencv, numpy) and /tmp/fvm/yunet.onnx.
Usage: /tmp/fv/bin/python ref_compare.py VIDEO.mp4 [--ref REF.mov --ref-from 6 --ref-to 23] [--words N] [--setups N] [--mistakes N] [--json OUT.json]
 cuts/shots : hard cuts (isolated frame-difference spikes) -> shot lengths, mean, median, longest, count of micro-shots < 2 s
 motion     : % of seconds with a frozen background (sum of two edge strips < 1.0) and % of seconds with still hands/body (lower part < 2.5)
 head       : head-centre path in face widths per second (YuNet, every 0.5 s)
 pace       : words per minute if --words is given (spoken words of the piece, from the script)
 setups/mistakes : given by hand (--setups = different camera setups seen, --mistakes = phone mistakes seen)
Reference gate (map_shorts/history_channel/louis_series_bible.md "Reference gate 05.11"): frozen bg <= 10 %, still body <= 15 %, head >= 0.18 fw/s,
60-90 wpm, >= 1 phone mistake per take, 7 setups per 128 s, per episode 2-3 long takes 15-30 s, 3-4 medium 8-17 s, one burst of 6-9 cuts (0.2-1.5 s)."""
import cv2, numpy as np, json, sys
det = cv2.FaceDetectorYN.create("/tmp/fvm/yunet.onnx", "", (320, 320), 0.6, 0.3, 5000)
def arg(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
def measure(path, t0=0.0, t1=None):
    cap = cv2.VideoCapture(path); fps = cap.get(cv2.CAP_PROP_FPS) or 24
    if t0: cap.set(cv2.CAP_PROP_POS_MSEC, t0 * 1000)
    small, heads, i = [], [], 0
    while True:
        pos = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        if t1 and pos >= t1: break
        ok, fr = cap.read()
        if not ok: break
        small.append(cv2.cvtColor(cv2.resize(fr, (108, 192)), cv2.COLOR_BGR2GRAY).astype(np.float32))
        if i % max(1, int(round(fps / 2))) == 0:
            h, w = fr.shape[:2]; im = cv2.resize(fr, (540, 960)); det.setInputSize((540, 960)); _, f = det.detect(im)
            heads.append(None if f is None else (len(small) - 1, *[float(x) for x in f[np.argmax(f[:, 2] * f[:, 3])][:4]]))
        i += 1
    n = len(small); dur = n / fps
    d = np.array([np.abs(small[k] - small[k - 1]).mean() for k in range(1, n)])
    med = float(np.median(d)); mad = float(np.median(np.abs(d - med))) or 0.5
    cut_idx = [k for k in range(len(d)) if d[k] > max(20.0, med + 10 * mad) and (k + 1 >= len(d) or d[k + 1] < 0.6 * d[k])]
    cuts = [round((k + 1) / fps, 2) for k in cut_idx]
    edges = [0.0] + cuts + [round(dur, 2)]
    shots = [round(b - a, 2) for a, b in zip(edges, edges[1:])]
    cutset = set(cut_idx); bg, low = [], []
    for s in range(int(dur)):
        a, b = int(s * fps) + 1, min(int((s + 1) * fps), n - 1)
        ks = [k for k in range(a, b) if (k - 1) not in cutset]
        if not ks: continue
        bg.append(np.mean([np.abs(small[k] - small[k - 1])[:100, :15].mean() + np.abs(small[k] - small[k - 1])[:100, 93:].mean() for k in ks]))
        low.append(np.mean([np.abs(small[k] - small[k - 1])[120:].mean() for k in ks]))
    pts = [h for h in heads if h]; path = 0.0; t = 0.0
    for p, q in zip(pts, pts[1:]):
        dt = (q[0] - p[0]) / fps
        if dt <= 0 or dt > 1.5: continue
        fw = max(p[3], q[3]); path += float(np.hypot((q[1] + q[3] / 2) - (p[1] + p[3] / 2), (q[2] + q[4] / 2) - (p[2] + p[4] / 2))) / fw; t += dt
    return {"duration_s": round(dur, 1), "shots": len(shots), "cut_times": cuts, "shot_lengths": shots, "mean_shot_s": round(float(np.mean(shots)), 1),
            "median_shot_s": round(float(np.median(shots)), 1), "longest_shot_s": max(shots), "micro_shots_lt_2s": sum(1 for x in shots if x < 2.0),
            "frozen_background_pct": round(100 * float(np.mean(np.array(bg) < 1.0))), "still_body_pct": round(100 * float(np.mean(np.array(low) < 2.5))),
            "head_fw_per_s": round(path / t, 2) if t else None}
R = measure(sys.argv[1])
words, setups, mist = arg("--words"), arg("--setups"), arg("--mistakes")
if words: R["words_per_min"] = round(int(words) / (R["duration_s"] / 60))
if setups: R["setups"] = int(setups)
if mist: R["phone_mistakes"] = int(mist)
ref = measure(arg("--ref"), float(arg("--ref-from", "0")), float(arg("--ref-to")) if arg("--ref-to") else None) if arg("--ref") else None
G = {"frozen_background_pct": ("<= 10", lambda v: v <= 10), "still_body_pct": ("<= 15", lambda v: v <= 15), "head_fw_per_s": (">= 0.18", lambda v: v is not None and v >= 0.18),
     "words_per_min": ("60-90", lambda v: 60 <= v <= 90), "phone_mistakes": (">= 1", lambda v: v >= 1)}
print(f"{'metric':26} {'reference':>12} {'ours':>10}  gate       verdict")
for k in ["duration_s", "shots", "mean_shot_s", "median_shot_s", "longest_shot_s", "micro_shots_lt_2s", "frozen_background_pct", "still_body_pct", "head_fw_per_s", "words_per_min", "setups", "phone_mistakes"]:
    if k not in R: continue
    g = G.get(k); v = "" if not g else ("OK" if g[1](R[k]) else "FAIL")
    print(f"{k:26} {str(ref.get(k, '-')) if ref else '-':>12} {str(R[k]):>10}  {g[0] if g else '':10} {v}")
print("cut times:", R["cut_times"]); print("shot lengths:", R["shot_lengths"])
if ref: print("reference cut times:", ref["cut_times"])
if arg("--json"): json.dump({"ours": R, "reference": ref}, open(arg("--json"), "w"), indent=1)
