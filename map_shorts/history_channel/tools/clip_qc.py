"""Post-generation QC of ONE clip for the history channel (owner 05.11: the clip-inspector agent runs this, then looks at the frames).
Needs /tmp/fv (opencv, numpy) and /tmp/fvm/yunet.onnx + sface.onnx (see face_gate.py header). Free, read-only except the frames dir.
Usage: /tmp/fv/bin/python clip_qc.py CLIP.mp4 [--first STILL] [--last STILL] [--prev PREVIOUS_CLIP.mp4] [--skip SECONDS] [--frames OUT_DIR]
       [--face-ref CARD.jpg | --no-face] [--mistake A-B]  (--mistake: the planned phone-mistake seconds, e.g. 1-3; excluded from the sharp gate, listed)
Prints a JSON report + PASS/FAIL per gate:
 face   : SFace similarity to the card A3 (or --face-ref, e.g. Marcel's card) at 2 fps (after --skip): median >= 0.70, p10 >= 0.55
          (calibrated 05.11: accepted clips 0.73-0.83 / p10 0.62-0.79; T3b 'a different man' 0.66 / 0.51); frames below 0.55 listed.
          --no-face skips the gate for a shot without a principal face (state why in reference_check).
 sharp  : head-area sharpness per second against the clip's OWN first second (the model's render of the start still; a 4K still is always
          3-6x 'sharper' than any 720p video frame, so the still itself is not a usable baseline): FAIL if the last third lost > 30 % (decay)
          or 2+ consecutive seconds are below 60 % (lasting loss); a single low second is a WARN (motion blur? check that frame by eye). Also reported: first second vs the start still at video size (information) and vs --prev clip mean.
 seams  : frame-difference spikes > median + 8 MAD that last <= 2 frames (a cut/jump inside the clip)
 motion : seconds with a frozen background (sum of the two edge strips < 1.0, same measure as the reference gate) <= 10 %; seconds with a still lower body (< 2.5) <= 15 % (reference gate)
 pins   : RMSE of the first/last frame vs the given stills (<= 0.06 = held)
 join   : RMSE of this clip's first frame vs the previous clip's last frame (information; a cut between setups is allowed)
It also writes a contact sheet (2 fps) and 1 frame per second into --frames for the eye check."""
import cv2, numpy as np, json, os, subprocess, sys
A3 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_card/A3_white_wig.jpg"
det = cv2.FaceDetectorYN.create("/tmp/fvm/yunet.onnx", "", (320, 320), 0.6, 0.3, 5000)
rec = cv2.FaceRecognizerSF.create("/tmp/fvm/sface.onnx", "")
def emb(img):
    h, w = img.shape[:2]; det.setInputSize((w, h)); _, f = det.detect(img)
    if f is None: return None
    f = f[np.argmax(f[:, 2] * f[:, 3])]; return rec.feature(rec.alignCrop(img, f))
def sharp(img):
    g = cv2.cvtColor(cv2.resize(img, (720, 1280)), cv2.COLOR_BGR2GRAY); h, w = g.shape
    return float(cv2.Laplacian(g[int(h*.15):int(h*.62), int(w*.1):int(w*.9)], cv2.CV_64F).var())
def rmse(a, b):
    a = cv2.resize(a, (360, 640)).astype(np.float32); b = cv2.resize(b, (360, 640)).astype(np.float32)
    return float(np.sqrt(((a - b) ** 2).mean()) / 255)
def arg(k, d=None): return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
clip = sys.argv[1]; out = arg("--frames", "/tmp/clipqc_" + os.path.basename(clip).replace(".mp4", "")); os.makedirs(out, exist_ok=True)
skip = float(arg("--skip", "0"))
cap = cv2.VideoCapture(clip); fps = cap.get(cv2.CAP_PROP_FPS) or 24
frames = []
while True:
    ok, fr = cap.read()
    if not ok: break
    frames.append(fr)
n = len(frames); dur = n / fps; R = {"clip": clip, "frames": n, "fps": round(fps, 2), "duration": round(dur, 2), "size": f"{frames[0].shape[1]}x{frames[0].shape[0]}"}
# face
NOFACE = "--no-face" in sys.argv
a3 = emb(cv2.imread(arg("--face-ref", A3))); sims = []
for i in range(0, n, int(round(fps / 2))):
    if i / fps < skip: continue
    e = emb(frames[i]); sims.append((round(i / fps, 2), None if e is None else round(float(rec.match(e, a3, cv2.FaceRecognizerSF_FR_COSINE)), 3)))
vals = [s for _, s in sims if s is not None]
R["face"] = {"median": round(float(np.median(vals)), 3) if vals else None, "p10": round(float(np.percentile(vals, 10)), 3) if vals else None,
             "ref": arg("--face-ref", A3).split("/")[-1], "low_frames": [t for t, s in sims if s is not None and s < 0.55], "no_face_frames": [t for t, s in sims if s is None]}
R["face"]["PASS"] = True if NOFACE else (bool(vals) and R["face"]["median"] >= 0.70 and R["face"]["p10"] >= 0.55)
if NOFACE: R["face"]["skipped"] = "--no-face"
# sharpness per second
per = [sharp(frames[min(int(s * fps), n - 1)]) for s in range(int(dur))]
base = float(np.mean(per[:1])) if per else sharp(frames[0])
third = max(1, len(per) // 3)
R["sharp"] = {"per_second": [round(x) for x in per], "baseline_first_second": round(base), "min_ratio_vs_first": round(min(per) / base, 2),
              "worst_second": int(np.argmin(per)), "decay_first_to_last_third": round(1 - np.mean(per[-third:]) / np.mean(per[:third]), 2)}
if arg("--first"):
    st = cv2.imread(arg("--first")); h0, w0 = frames[0].shape[:2]
    R["sharp"]["info_first_vs_still_at_video_size"] = round(base / sharp(cv2.resize(st, (w0, h0), interpolation=cv2.INTER_AREA)), 2)
if arg("--prev"):
    pc = cv2.VideoCapture(arg("--prev")); pf = []
    while True:
        ok, fr = pc.read()
        if not ok: break
        pf.append(fr)
    pfps = pc.get(cv2.CAP_PROP_FPS) or 24
    R["sharp"]["info_vs_prev_clip_mean"] = round(float(np.mean(per)) / float(np.mean([sharp(pf[int(i * pfps)]) for i in range(int(len(pf) / pfps))])), 2)
mis = [int(x) for x in arg("--mistake", "-1--1").replace("--", " -").split("-") if x.strip()] if arg("--mistake") else []
excl = set(range(mis[0], mis[1])) if len(mis) == 2 else set()
if excl: R["sharp"]["excluded_planned_mistake_seconds"] = sorted(excl)
low = [i for i, x in enumerate(per) if x < 0.60 * base and i not in excl]
runs = [i for i in low if i + 1 in low]
R["sharp"]["seconds_below_60pct"] = low
R["sharp"]["WARN_single_dips"] = [i for i in low if i + 1 not in low and i - 1 not in low]
R["sharp"]["PASS"] = bool(not runs and R["sharp"]["decay_first_to_last_third"] <= 0.30)
# seams and motion
small = [cv2.cvtColor(cv2.resize(f, (108, 192)), cv2.COLOR_BGR2GRAY).astype(np.float32) for f in frames]
d = np.array([np.abs(small[i] - small[i - 1]).mean() for i in range(1, n)])
med = float(np.median(d)); mad = float(np.median(np.abs(d - med))) or 0.5
spk = np.where(d > med + 8 * mad)[0]
seams = []
for k in spk:
    run = [j for j in spk if abs(j - k) <= 2]
    if len(run) <= 2 and (k / fps) > 0.2: seams.append(round((k + 1) / fps, 2))
R["seams"] = {"median_diff": round(med, 2), "suspect_cuts": [float(x) for x in sorted(set(seams))], "PASS": len(seams) == 0}
bg, lowb = [], []
for s in range(int(dur)):
    a, b = int(s * fps) + 1, min(int((s + 1) * fps), n - 1)
    dd = [np.abs(small[i] - small[i - 1]) for i in range(a, b)]
    bg.append(np.mean([x[:100, :15].mean() + x[:100, 93:].mean() for x in dd])); lowb.append(np.mean([x[120:].mean() for x in dd]))
R["motion"] = {"frozen_background_pct": round(100 * float(np.mean(np.array(bg) < 1.0))), "still_body_pct": round(100 * float(np.mean(np.array(lowb) < 2.5)))}
R["motion"]["PASS"] = bool(R["motion"]["frozen_background_pct"] <= 10 and R["motion"]["still_body_pct"] <= 15)
# pins and join
R["pins"] = {}
if arg("--first"): R["pins"]["first_vs_still"] = round(rmse(frames[0], cv2.imread(arg("--first"))), 3)
if arg("--last"): R["pins"]["last_vs_still"] = round(rmse(frames[-1], cv2.imread(arg("--last"))), 3)
R["pins"]["PASS"] = bool(all(v <= 0.06 for k, v in R["pins"].items() if k != "PASS"))
if arg("--prev"):
    R["join_vs_prev_last"] = round(rmse(frames[0], pf[-1]), 3)
# frames for the eye check
for s in range(int(dur) + 1):
    cv2.imwrite(f"{out}/s_{s:02d}.jpg", frames[min(int(s * fps), n - 1)])
sheet = [cv2.resize(frames[min(int(i * fps / 2), n - 1)], (180, 320)) for i in range(int(dur * 2) + 1)]
rows = [np.hstack(sheet[i:i + 8] + [np.zeros((320, 180, 3), np.uint8)] * (8 - len(sheet[i:i + 8]))) for i in range(0, len(sheet), 8)]
cv2.imwrite(f"{out}/sheet.jpg", np.vstack(rows)); R["frames_dir"] = out
R["ALL_PASS"] = bool(all(R[k]["PASS"] for k in ("face", "sharp", "seams", "motion", "pins")))
print(json.dumps(R, indent=1))
