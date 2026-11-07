"""ROUGH CUT v4 of ep.2 (07.11, owner: all takes in, then reworks): picture only, no voice yet, no music, model audio dropped, hard cuts only. Pieces after Take 4 are the owner-accepted Seedance clips with the trims decided on 07.11. Usage: /tmp/fv/bin/python edit_rough_v4.py [out.mp4]"""
import sys, subprocess, numpy as np, cv2, json
P = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/pilot_frames/"
OUT = sys.argv[1] if len(sys.argv) > 1 else P + "EP2_rough_v4_muted.mp4"
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

def clip(name, t0=None, t1=None, sway=False, seed=1, nudges=(), zoom=1.06, label="", box=None):
    cap = cv2.VideoCapture(P + name); fps = cap.get(cv2.CAP_PROP_FPS) or FPS
    n_all = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); a = int((t0 or 0) * fps); b = min(n_all, int(t1 * fps)) if t1 else n_all
    cap.set(cv2.CAP_PROP_POS_FRAMES, a); n = b - a
    sway = False
    if sway: dx, dy, rot, zm = sway_params(n, seed, [x for x in nudges], zoom)
    start = t_total[0]
    for i in range(n):
        ok, f = cap.read()
        if not ok: n = i; break
        if sway:
            M = cv2.getRotationMatrix2D((W / 2, H / 2), rot[i], zm[i]); M[0, 2] += dx[i]; M[1, 2] += dy[i]
            f = cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
        if box:
            bx, by, bw, bh = box; f = cv2.resize(f[by:by + bh, bx:bx + bw], (W, H), interpolation=cv2.INTER_LANCZOS4)
        elif f.shape[1] != W or f.shape[0] != H:
            f = cv2.resize(f, (W, H), interpolation=cv2.INTER_LANCZOS4)
        put(f)
    t_total[0] += n / FPS; timeline.append({"src": name, "in": t0 or 0, "out": round((a + n) / fps, 2), "sway": sway, "start": round(start, 2), "len": round(n / FPS, 2), "label": label})

def still(name, secs, crop_from, crop_to, seed, label=""):
    """moving crop on a 4K still: crop_from/to = (cx, cy, scale) in fractions of the image; scale = visible height fraction."""
    img = cv2.imread(P + "anchors/" + name); ih, iw = img.shape[:2]; n = int(round(secs * FPS)); r = np.random.default_rng(seed)
    jx = np.zeros(n); jy = np.zeros(n); start = t_total[0]
    for i in range(n):
        k = i / max(1, n - 1); cx = (crop_from[0] + (crop_to[0] - crop_from[0]) * k) * iw + jx[i]; cy = (crop_from[1] + (crop_to[1] - crop_from[1]) * k) * ih + jy[i]
        sc = crop_from[2] + (crop_to[2] - crop_from[2]) * k; ch = sc * ih; cw = ch * W / H
        x0 = int(np.clip(cx - cw / 2, 0, iw - cw)); y0 = int(np.clip(cy - ch / 2, 0, ih - ch))
        put(cv2.resize(img[y0:y0 + int(ch), x0:x0 + int(cw)], (W, H), interpolation=cv2.INTER_AREA))
    t_total[0] += n / FPS; timeline.append({"src": name, "sway": "crop", "start": round(start, 2), "len": round(n / FPS, 2), "label": label})

# TAKE 1 (already an edit, 36.8 s)
clip("PILOT_take1_15s.mp4", t0=3.5, t1=10.0, label="Take 1 pilot (raw; the violent zoom-out and shake of the first 3.5 s cut)")
clip("PILOT_take1_15s.mp4", t0=12.0, label="Take 1 pilot after the ghost cut and its jolts (10.0-12.0 s cut)")
clip("TAKE1_piece2b.mp4", label="Take 1 piece 2b (raw)")
clip("TAKE1_piece3_alive.mp4", label="Take 1 piece 3 alive (raw)")
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
clip("TAKE_t4bA_seedance.mp4", t0=2.0, label="4b-A wine spills (Seedance Lite, from 2.0 s: eyes closed 0.5-2.2 s cut)")
clip("TAKE_t4bB_seedance_std.mp4", label="4b-B Marcel confesses (Seedance Standard, whole, owner 07.11)")
# TAKE 5 (owner decisions 07.11)
clip("TAKE_t5a_seedance_v2.mp4", t1=11.0, label="5a peas v2 (0-11 s, limp tail cut)")
clip("TAKE_t5b_seedance.mp4", t1=3.7, label="5b laden table (0-3.7 s, closed-eyes tail cut)")
clip("TAKE_t5c_seedance_v2.mp4", label="5c born for happiness v2 (whole)")
# TAKE 6
clip("TAKE_t6_seedance.mp4", label="6 the verdict (whole)")
# TAKE 7 (walking version)
clip("TAKE_t7aw_seedance.mp4", t1=3.7, label="7a walk (0-3.7 s)")
clip("TAKE_t7aw_seedance.mp4", t0=8.0, label="7a walk (8.0-10 s)")
clip("TAKE_t7bw_seedance.mp4", t0=0.6, t1=11.8, box=(0, 0, 648, 1150), label="7b walk (0.6-11.8 s, top-left crop removes the extra hand)")
ENC.stdin.close(); ENC.wait()
json.dump({"out": OUT, "total_s": round(t_total[0], 2), "segments": timeline}, open(OUT.replace(".mp4", "_timeline.json"), "w"), indent=1)
print("done", round(t_total[0], 1), "s")
