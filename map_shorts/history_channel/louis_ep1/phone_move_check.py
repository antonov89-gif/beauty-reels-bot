"""Phone-realism check for a hand-held clip (owner 29.10: "everything realistic, the camera must not fly").
A real phone tilt is a ROTATION about the camera: the scene shifts, but objects do not grow or shrink. A "flying" camera shows up as ZOOM (scale change) between frames.
Method: ORB features between consecutive frames -> partial affine (scale, rotation, translation). Prints per-0.25-s: vertical shift (px/frame, normalised by frame height), scale change (% per second), roll (deg).
Verdict: cumulative scale change over the clip (excluding blur-only frames) > 12 % = FLY (reject). Usage: python3 phone_move_check.py clip.mp4"""
import sys
import cv2
import numpy as np

cap = cv2.VideoCapture(sys.argv[1]); fps = cap.get(cv2.CAP_PROP_FPS) or 24
orb = cv2.ORB_create(1500); bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
prev = None; rows = []; i = 0; cum_log_scale = 0.0
while True:
    ok, fr = cap.read()
    if not ok: break
    g = cv2.cvtColor(cv2.resize(fr, (270, int(270 * fr.shape[0] / fr.shape[1]))), cv2.COLOR_BGR2GRAY)
    if prev is not None:
        k1, d1 = orb.detectAndCompute(prev, None); k2, d2 = orb.detectAndCompute(g, None)
        s = 1.0; ang = 0.0; dy = np.nan
        if d1 is not None and d2 is not None and len(k1) > 20 and len(k2) > 20:
            m = bf.match(d1, d2)
            if len(m) >= 12:
                p1 = np.float32([k1[x.queryIdx].pt for x in m]); p2 = np.float32([k2[x.trainIdx].pt for x in m])
                M, inl = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=3)
                if M is not None and inl is not None and inl.sum() >= 10:
                    s = float(np.hypot(M[0, 0], M[1, 0])); ang = float(np.degrees(np.arctan2(M[1, 0], M[0, 0]))); dy = float(M[1, 2]) / g.shape[0]
                    cum_log_scale += np.log(s)
        rows.append((i / fps, s, ang, dy))
    prev = g; i += 1
print(f"{sys.argv[1]}: {i} frames, {fps:.0f} fps")
print("t(s)   scale/frame   roll(deg)  vertical shift (frame heights/frame)")
for k in range(0, len(rows), 6):
    seg = rows[k:k + 6]
    print(f"{seg[0][0]:.2f}   {np.mean([r[1] for r in seg]):.4f}        {np.mean([r[2] for r in seg]):+.2f}      {np.nanmean([r[3] for r in seg]) if not all(np.isnan(r[3]) for r in seg) else float('nan'):+.3f}")
tot = (np.exp(cum_log_scale) - 1) * 100
print(f"cumulative scale change over the clip: {tot:+.1f} %  ->", "FLY (reject)" if abs(tot) > 12 else "rotation-like (ok)")
