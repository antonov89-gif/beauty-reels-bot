"""ROUGH CUT v1 of ep.2 (06.11, owner: "начинай монтаж, проверяй"): picture only, no voice yet (no TTS key), no music, model audio dropped, hard cuts only (reference grammar). Everything is decoded from the original files and written by ONE encoder (CRF 16, one final encode); the only exception is Take 1, which is the already edited TAKE1_rough_v2_muted.mp4 (its builder was not saved), so Take 1 has one extra generation of encoding.
Virtual hand-held (same walk/nudge model as louis_ep1/make_sway.py: smoothed random walk drift + roll + a few nudges, zoom 1.06 hides the borders) only on clips that failed the motion gate raw (T2a, T2c, T3a, T3c, T4a, T4b); T2b (Marcel POV) and T3d already pass; the food burst is built from the five 4K stills with a moving crop (one downscale per frame from the 4K original).
Missing pieces (not generated yet, balance empty): 3b-B king reaction, 4b-2 Marcel, 4b-1 retake (the first take is a placeholder), Takes 5, 6, 7. Usage: /tmp/fv/bin/python edit_rough_v1.py [out.mp4]"""
import sys, subprocess, numpy as np, cv2, json
P = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/pilot_frames/"
OUT = sys.argv[1] if len(sys.argv) > 1 else P + "EP2_rough_v1_muted.mp4"
W, H, FPS = 720, 1280, 24
ENC = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
timeline = []; t_total = [0.0]

def walk(r, n, sd, smooth_s):
    k = max(3, int(smooth_s * FPS)); w = np.cumsum(r.normal(0, 1, n + 2 * k)); w = np.convolve(w, np.hanning(k) / np.hanning(k).sum(), "same")[k:k + n]
    w -= np.linspace(w[0], w[-1], n) * 0.6; return w / (np.abs(w).max() + 1e-9) * sd

def sway_params(n, seed, nudges, zoom):
    r = np.random.default_rng(seed); t = np.arange(n) / FPS
    dx = walk(r, n, 0.012 * W, 1.2) + walk(r, n, 0.003 * W, 0.25); dy = walk(r, n, 0.010 * H, 1.4) + walk(r, n, 0.0025 * H, 0.25); rot = walk(r, n, 0.9, 1.6)
    for n0 in nudges:
        a = r.uniform(-1, 1, 3) * np.array([0.03 * W, 0.022 * H, 2.0]); x = t - n0
        e = np.where(x < 0, 0, np.where(x < .12, x / .12, np.exp(-(x - .12) / .35) * np.cos((x - .12) * 9)))
        dx += a[0] * e; dy += a[1] * e; rot += a[2] * e
    return dx, dy, rot, np.full(n, zoom)

def put(frame): ENC.stdin.write(frame.tobytes())

def clip(name, t0=None, t1=None, sway=False, seed=1, nudges=(), zoom=1.06, label=""):
    cap = cv2.VideoCapture(P + name); fps = cap.get(cv2.CAP_PROP_FPS) or FPS
    n_all = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); a = int((t0 or 0) * fps); b = min(n_all, int(t1 * fps)) if t1 else n_all
    cap.set(cv2.CAP_PROP_POS_FRAMES, a); n = b - a
    if sway: dx, dy, rot, zm = sway_params(n, seed, [x for x in nudges], zoom)
    start = t_total[0]
    for i in range(n):
        ok, f = cap.read()
        if not ok: n = i; break
        if sway:
            M = cv2.getRotationMatrix2D((W / 2, H / 2), rot[i], zm[i]); M[0, 2] += dx[i]; M[1, 2] += dy[i]
            f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
        put(f)
    t_total[0] += n / FPS; timeline.append({"src": name, "in": t0 or 0, "out": round((a + n) / fps, 2), "sway": sway, "start": round(start, 2), "len": round(n / FPS, 2), "label": label})

def still(name, secs, crop_from, crop_to, seed, label=""):
    """moving crop on a 4K still: crop_from/to = (cx, cy, scale) in fractions of the image; scale = visible height fraction."""
    img = cv2.imread(P + "anchors/" + name); ih, iw = img.shape[:2]; n = int(round(secs * FPS)); r = np.random.default_rng(seed)
    jx = walk(r, n, 0.006 * iw, 0.6); jy = walk(r, n, 0.005 * ih, 0.6); start = t_total[0]
    for i in range(n):
        k = i / max(1, n - 1); cx = (crop_from[0] + (crop_to[0] - crop_from[0]) * k) * iw + jx[i]; cy = (crop_from[1] + (crop_to[1] - crop_from[1]) * k) * ih + jy[i]
        sc = crop_from[2] + (crop_to[2] - crop_from[2]) * k; ch = sc * ih; cw = ch * W / H
        x0 = int(np.clip(cx - cw / 2, 0, iw - cw)); y0 = int(np.clip(cy - ch / 2, 0, ih - ch))
        put(cv2.resize(img[y0:y0 + int(ch), x0:x0 + int(cw)], (W, H), interpolation=cv2.INTER_AREA))
    t_total[0] += n / FPS; timeline.append({"src": name, "sway": "crop", "start": round(start, 2), "len": round(n / FPS, 2), "label": label})

# TAKE 1 (already an edit, 36.8 s)
clip("TAKE1_rough_v2_muted.mp4", label="Take 1 opener (existing rough edit)")
# TAKE 2
clip("TAKE2_T2a_v2.mp4", sway=True, seed=21, nudges=(3.0, 8.5), label="2a rule and bow")
clip("TAKE2_T2b.mp4", label="2b Marcel POV")
clip("TAKE2_T2c.mp4", sway=True, seed=23, nudges=(4.0, 9.5), label="2c grape")
# TAKE 3
clip("TAKE3_T3a.mp4", sway=True, seed=31, nudges=(2.0, 5.5, 8.0), label="3a soup")
for i, (nm, sec, f, t_) in enumerate([("T3b_F1_4k.jpg", 0.9, (0.5, 0.55, 0.62), (0.45, 0.5, 0.5)), ("T3b_F2_4k.jpg", 0.7, (0.5, 0.5, 0.7), (0.55, 0.55, 0.55)),
        ("T3b_F3_4k.jpg", 0.6, (0.45, 0.4, 0.6), (0.5, 0.45, 0.5)), ("T3b_F4_4k.jpg", 1.0, (0.5, 0.5, 0.75), (0.45, 0.5, 0.6)),
        ("T3b_F2_4k.jpg", 0.5, (0.3, 0.7, 0.4), (0.35, 0.65, 0.35)), ("T3b_F3_4k.jpg", 0.5, (0.65, 0.65, 0.4), (0.6, 0.6, 0.35)), ("T3b_F5_4k.jpg", 1.0, (0.5, 0.55, 0.7), (0.5, 0.5, 0.55))]):
    still(nm, sec, f, t_, 40 + i, label="food burst")
clip("TAKE3_T3c.mp4", sway=True, seed=33, nudges=(5.5,), label="3b-C fork")
clip("TAKE3_T3d.mp4", label="3c fork or fingers")
# TAKE 4
clip("TAKE4_T4a.mp4", sway=True, seed=41, nudges=(3.0, 9.0), label="4a drink")
clip("TAKE4_T4b.mp4", t0=1.0, sway=True, seed=42, nudges=(5.0,), label="4b-1 wine and laugh (first take, PLACEHOLDER, from 1.0 s)")
ENC.stdin.close(); ENC.wait()
json.dump({"out": OUT, "total_s": round(t_total[0], 2), "segments": timeline}, open(OUT.replace(".mp4", "_timeline.json"), "w"), indent=1)
print("done", round(t_total[0], 1), "s")
