"""Panama Canal long-form 16:9. python3 engine32.py info | still t.. | prefetch | frames | video A B out.mp4"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import tiles
from script32 import S, LINES

W, H, FPS = 1920, 1080, 30
POP, POPX = "Poppins-Bold.ttf", "Poppins-ExtraBold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (60, 200, 90), (60, 140, 255), (255, 255, 255), (0, 0, 0)
GOLD, ORG, NAVY, CYAN = (255, 190, 60), (255, 140, 30), (10, 24, 48), (90, 220, 255)
TM = json.load(open("timing.json")); D, TW = TM["D"], TM["T"]
N = len(S)
LEAD, GAP = 0.6, 1.6
CH = [c for c, _ in S]
OFF = []; o = 0.0
for i in range(N):
    if i > 0 and CH[i] != CH[i - 1]: o += GAP
    OFF.append(o)
ST = [LEAD + s + OFF[i] for i, s in enumerate(TM["starts"])]
SC = [0.0] + [ST[i] - (GAP if CH[i] != CH[i - 1] else 0.12) for i in range(1, N)]
TOTAL = ST[-1] + D[-1] + 2.5
SC.append(TOTAL + 1)
NF = int(TOTAL * FPS)


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


exec(open("helpers_raw.py").read())


def clean(w): return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word, nth=0):
    ws = [clean(w) for w in LINES[i].split()]; q = clean(word); hits = [j for j, w in enumerate(ws) if w == q] or [j for j, w in enumerate(ws) if q in w]
    if not hits: raise KeyError((i, word))
    return ST[i] + TW[i][hits[min(nth, len(hits) - 1)]]


# ------------------------------------------------------------------ shot list: per line, (kind, arg, weight[, opts])
# kind: A = Veo clip (arg = (name, start_sec)), K = Ken Burns on keyframe, M = map, C = card
SHOTS = {
 0: [("A", ("A01", 0), 7), ("A", ("A23", 0), 5.3), ("A", ("A02", 0), 6)],
 1: [("M", "panama", 1)],
 2: [("A", ("A02", 3.5), 6), ("K", "A15", 6), ("K", "A22", 6)],
 3: [("K", "A03", 6), ("A", ("A05", 0), 6.4)],
 4: [("A", ("A04", 0), 1)],
 5: [("A", ("A06", 0), 1)],
 6: [("K", "A14", 5), ("C", "pools", 6.4)],
 7: [("M", "horn", 1)],
 8: [("A", ("A07", 0), 8), ("A", ("A08", 0), 7.7)],
 9: [("A", ("A09", 0), 6), ("A", ("A11", 0), 5.3), ("A", ("A10", 0), 6)],
 10: [("K", "A25", 6), ("K", "A24", 5.5)],
 11: [("K", "A01", 1)],
 12: [("M", "colon", 6), ("A", ("A23", 2.5), 7.5)],
 13: [("A", ("A12", 0), 7.7), ("K", "A02", 6)],
 14: [("A", ("A13", 0), 6), ("A", ("A14", 0), 6.3)],
 15: [("A", ("A15", 0), 1)],
 16: [("C", "revenue", 1)],
 17: [("A", ("A16", 0), 7), ("A", ("A23", 4), 5.3), ("A", ("A01", 3.5), 6)],
 18: [("A", ("A17", 0), 1)],
 19: [("A", ("A03", 0), 7.5), ("A", ("A06", 2.5), 5, {"flip": 1}), ("K", "A04", 5)],
 20: [("A", ("A18", 0), 1)],
 21: [("A", ("A19", 0), 8), ("K", "A19", 4.4)],
 22: [("A", ("A20", 0), 1)],
 23: [("A", ("A21", 0), 1)],
 24: [("M", "east", 1)],
 25: [("A", ("A22", 0), 9), ("K", "A22", 7.9)],
 26: [("A", ("A23", 0), 7), ("M", "detour", 8.8)],
 27: [("M", "rioindio", 1)],
 28: [("A", ("A24", 0), 8), ("K", "A24", 4.2)],
 29: [("A", ("A25", 0), 7), ("A", ("A26", 0), 7.8)],
 30: [("A", ("A27", 0), 7), ("A", ("A20", 3), 5.1)],
 31: [("A", ("A27", 3.5), 1)],
}
ARCHIVAL = {"A07", "A08", "A09", "A10", "A11", "A17"}
TL = []  # (t0, t1, line, kind, arg, opts)
for i in range(N):
    a, b = SC[i], SC[i + 1] if i + 1 < N else TOTAL
    sh = SHOTS[i]; tw = sum(s[2] for s in sh); t = a
    for s in sh:
        d = (b - a) * s[2] / tw
        TL.append((t, t + d, i, s[0], s[1], s[3] if len(s) > 3 else {})); t += d
CUTS = [x[0] for x in TL[1:]]


def shot_at(t):
    for k, x in enumerate(TL):
        if x[0] <= t < x[1]: return k
    return len(TL) - 1


# ------------------------------------------------------------------ sources
def cover(im, z=1.0, cx=0.5, cy=0.5, flip=False):
    """Scale an image to cover WxH with zoom z and focus point (cx, cy)."""
    iw, ih = im.size; s = max(W / iw, H / ih) * z
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    x0 = min(max(0, int(cx * nw - W / 2)), nw - W); y0 = min(max(0, int(cy * nh - H / 2)), nh - H)
    im = im.resize((nw, nh), Image.BILINEAR).crop((x0, y0, x0 + W, y0 + H))
    return im.transpose(Image.FLIP_LEFT_RIGHT) if flip else im


_FR = {}
def clip_frame(name, sec):
    d = f"frames/{name}"; n = len(os.listdir(d))
    idx = min(n, max(1, int(sec * 24) + 1))
    return Image.open(f"{d}/{idx:04d}.jpg").convert("RGB")


_KF = {}
def keyframe(name):
    if name not in _KF: _KF[name] = Image.open(f"keyframes/{name}.jpg").convert("RGB")
    return _KF[name]


def render_clip(arg, t0, t1, t, opts):
    name, s0 = arg; dur = t1 - t0; avail = 8.0 - s0
    if not os.path.isdir(f"frames/{name}"): return render_kb(name, t0, t1, t)
    rate = min(1.0, max(0.62, avail / max(dur, 0.1)))
    sec = s0 + (t - t0) * rate
    im = clip_frame(name, min(sec, 7.95))
    k = (t - t0) / max(dur, 0.1)
    return cover(im, 1.0 + 0.05 * k, flip=bool(opts.get("flip")))


KB_DIR = {"A03": (1.18, 1.0, 0.55, 0.5), "A15": (1.0, 1.12, 0.45, 0.6), "A22": (1.12, 1.0, 0.4, 0.6), "A14": (1.0, 1.12, 0.35, 0.55),
          "A25": (1.0, 1.1, 0.5, 0.45), "A24": (1.12, 1.0, 0.55, 0.5), "A01": (1.0, 1.15, 0.45, 0.6), "A02": (1.12, 1.0, 0.55, 0.45),
          "A04": (1.0, 1.15, 0.5, 0.55), "A19": (1.12, 1.0, 0.45, 0.6), "A27": (1.0, 1.1, 0.5, 0.6)}


def render_kb(name, t0, t1, t):
    z0, z1, cx, cy = KB_DIR.get(name, (1.0, 1.1, 0.5, 0.5)); k = ease((t - t0) / max(0.1, t1 - t0)) * 0.7 + (t - t0) / max(0.1, t1 - t0) * 0.3
    return cover(keyframe(name), z0 + (z1 - z0) * k, 0.5 + (cx - 0.5) * k, 0.5 + (cy - 0.5) * k)


def grade(im, esri=False):
    a = np.asarray(im).astype(np.float32) / 255
    a = a ** (0.85 if esri else 0.82)
    g = a.mean(2, keepdims=True); a = g + (a - g) * 1.15
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


# ------------------------------------------------------------------ maps
CANAL = [(-79.917, 9.39), (-79.92, 9.30), (-79.91, 9.265), (-79.86, 9.21), (-79.79, 9.16), (-79.73, 9.12), (-79.69, 9.10), (-79.66, 9.06),
         (-79.63, 9.03), (-79.60, 9.00), (-79.585, 8.97), (-79.57, 8.93), (-79.55, 8.89), (-79.53, 8.85)]
NY, SF = (-74.0, 40.7), (-122.4, 37.8)
HORN = [NY, (-68, 33), (-58, 18), (-45, 3), (-36, -8), (-39, -22), (-48, -33), (-58, -44), (-65, -54), (-67.3, -56.6), (-72, -55), (-76, -48),
        (-75, -36), (-73, -22), (-79, -8), (-86, 2), (-97, 12), (-108, 20), (-115, 27), SF]
VIAPAN = [NY, (-73, 30), (-75, 20), (-77.5, 13), (-79.9, 9.4), (-79.53, 8.85), (-82, 7), (-92, 10), (-104, 17), (-113, 25), SF]
SHA = (121.5, 31.2)
SUEZ = [SHA, (122, 25), (113, 15), (104, 2), (95, 6), (80, 6), (65, 12), (52, 13), (43, 12.5), (38, 20), (32.5, 30), (28, 33.5), (12, 37.5), (-5.6, 36), (-20, 37),
        (-45, 39), (-74.0, 40.7)]
AFRICA = [SHA, (122, 25), (113, 15), (104, 2), (95, -6), (75, -20), (50, -30), (30, -37), (18.5, -35.5), (5, -25), (-10, -10), (-25, 5), (-45, 25), (-65, 37), (-74.0, 40.7)]
MAPS = {
 "panama": dict(a=(-79.7, 9.0, 40.0), b=(-79.75, 9.1, 3.2)),
 "horn": dict(a=(-88.0, -14.0, 285.0), b=(-88.0, -14.0, 265.0)),
 "colon": dict(a=(-79.92, 9.37, 0.9), b=(-79.9, 9.38, 0.45)),
 "east": dict(a=(-79.74, 9.12, 1.15), b=(-79.74, 9.12, 0.95)),
 "detour": dict(a=(30.0, 12.0, 250.0), b=(28.0, 12.0, 235.0)),
 "rioindio": dict(a=(-79.95, 9.1, 1.9), b=(-80.0, 9.05, 1.3)),
}


def map_cam(key, t0, t1, t):
    m = MAPS[key]; k = ease((t - t0) / max(0.1, t1 - t0)); (la, lb), (pa, pb), (za, zb) = zip(m["a"], m["b"])
    if key == "panama": k = ease((t - t0) / 3.2)
    return tiles.Cam(la + (lb - la) * k, pa + (pb - pa) * k, math.exp(math.log(za) + (math.log(zb) - math.log(za)) * k))


def ipath(cam, pts): return [cam.xy(lo, la) for lo, la in pts]


def partial(pts, k):
    if k <= 0 or len(pts) < 2: return pts[:1]
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; L = sum(seg) * min(1, k); out = [pts[0]]; acc = 0
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if acc + s >= L:
            q = (L - acc) / max(s, 1e-6); out.append((a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)); return out
        out.append(b); acc += s
    return out


def smooth(pts, n=10):
    if len(pts) < 3: return pts
    P = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for s in range(n):
            u = s / n; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in range(2)))
    return out + [pts[-1]]


def glow_line(img, pts, color, width, dash=None, phase=0.0):
    if len(pts) < 2: return
    gl = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
    ImageDraw.Draw(gl).line([(x / 2, y / 2) for x, y in pts], fill=color + (150,), width=int(width * 1.4), joint="curve")
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(7)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    d.line(pts, fill=BLK + (200,), width=width + 6, joint="curve")
    if dash:
        on, off = dash; seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; pos = -phase % (on + off)
        for (a, b), s in zip(zip(pts, pts[1:]), seg):
            u = 0.0
            while u < s:
                c = (pos + u) % (on + off); run = min(s - u, (on - c) if c < on else (on + off - c))
                if c < on: d.line([(a[0] + (b[0] - a[0]) * u / s, a[1] + (b[1] - a[1]) * u / s), (a[0] + (b[0] - a[0]) * (u + run) / s, a[1] + (b[1] - a[1]) * (u + run) / s)], fill=color + (255,), width=width)
                u += max(run, 0.5)
            pos += s
    else:
        d.line(pts, fill=color + (255,), width=width, joint="curve")


def pin(img, x, y, txt, color, k, up=True, size=40):
    if k <= 0: return
    d = ImageDraw.Draw(img); r = 13 * min(k, 1.15)
    d.ellipse((x - r - 4, y - r - 4, x + r + 4, y + r + 4), fill=WHT); d.ellipse((x - r, y - r, x + r, y + r), fill=color)
    if txt:
        f = font(POPX, size * min(1, k)); tw = f.getlength(txt); yy = y - 58 if up else y + 58
        d.rounded_rectangle((x - tw / 2 - 20, yy - size * 0.75, x + tw / 2 + 20, yy + size * 0.75), 14, fill=(12, 20, 38, 230), outline=color, width=4)
        d.text((x, yy + 2), txt, font=f, fill=WHT, anchor="mm")


def ship_on(img, pts, k, size=70):
    if k <= 0 or len(pts) < 2: return
    p = partial(pts, k); x, y = p[-1]; a, b = p[-2] if len(p) > 1 else p[-1], p[-1]
    paste_emoji(img, "🚢", x, y - 10, size)


def maplabel(d, xy, txt, size=44, col=WHT):
    text_stroke(d, xy, txt, font(POPX, size), col, stroke=6)


def render_map(key, t0, t1, t, i):
    cam = map_cam(key, t0, t1, t); lt = t - t0; dur = t1 - t0
    img = grade(cam.render(), cam.src == "esri").convert("RGBA"); d = ImageDraw.Draw(img)
    if key == "panama":
        k = ease((lt - 1.2) / 2.6)
        glow_line(img, partial(smooth(ipath(cam, CANAL)), k), YEL, 9)
        if lt > 3.2:
            al = ease((lt - 3.2) / 0.6)
            maplabel(d, cam.xy(-79.25, 9.78), "ATLANTIC (CARIBBEAN SEA)", 44, (255, 255, 255, int(255 * al)))
            maplabel(d, cam.xy(-79.25, 8.45), "PACIFIC OCEAN", 44, (255, 255, 255, int(255 * al)))
        pin(img, *cam.xy(-79.9, 9.36), "COLÓN", BLU, ease((lt - 3.6) / 0.4) * 1.0)
        pin(img, *cam.xy(-79.55, 8.95), "PANAMA CITY", RED, ease((lt - 4.0) / 0.4), up=False)
        if lt > 4.6: badge(img, W - 300, 170, "82 KM", ORG, ease((lt - 4.6) / 0.35), size=60)
    elif key == "horn":
        kh = ease((lt - 0.6) / 4.5); kp = ease((t - WT(i, "saves") + 0.6) / 2.0); th = WT(i, "thirteen") - 0.1
        ph = smooth(ipath(cam, HORN), 8); pp = smooth(ipath(cam, VIAPAN), 8)
        glow_line(img, partial(ph, kh), RED, 9, dash=(26, 14), phase=t * 60)
        glow_line(img, partial(pp, kp), GRN, 10)
        ship_on(img, ph, kh, 64)
        pin(img, *cam.xy(*NY), "NEW YORK", BLU, ease(lt / 0.4))
        pin(img, *cam.xy(*SF), "SAN FRANCISCO", BLU, ease((lt - 0.3) / 0.4))
        if kh > 0.55: pin(img, *cam.xy(-67.3, -56.6), "CAPE HORN", RED, ease((kh - 0.55) / 0.1), up=True)
        if kh > 0.98: badge(img, W / 2 + 330, H - 300, "≈ 22,500 KM", RED, ease((lt - 5.2) / 0.3), size=54)
        if kp > 0.6: badge(img, W / 2 - 280, 300, "≈ 9,500 KM", GRN, ease((kp - 0.6) / 0.15), size=54)
        if t >= th: big(img, "−13,000 KM", t, th, y=H / 2 - 20, size=120)
    elif key == "colon":
        pin(img, *cam.xy(-79.90, 9.355), "COLÓN", BLU, ease((lt - 0.4) / 0.4), up=False)
        for q, (lo, la) in enumerate([(-80.02, 9.43), (-79.98, 9.47), (-80.06, 9.40), (-79.95, 9.45), (-80.1, 9.45), (-80.04, 9.5), (-79.93, 9.49), (-80.12, 9.38)]):
            x, y = cam.xy(lo, la); paste_emoji(img, "🚢", x, y + math.sin(t * 1.3 + q) * 3, 54 * ease((lt - 0.8 - q * 0.12) / 0.3))
        if lt > 1.2: badge(img, W / 2, 150, "≈ 35 SHIPS A DAY", ORG, ease((lt - 1.2) / 0.35), size=58)
    elif key == "east":
        xa, _ = cam.xy(-79.92, 9.39); xp, _ = cam.xy(-79.55, 8.89)
        glow_line(img, smooth(ipath(cam, CANAL)), YEL, 8)
        ka = ease((lt - 0.5) / 0.8); kp = ease((lt - 2.0) / 0.8)
        if ka > 0: d.line([(xa, 0), (xa, H * ka)], fill=CYAN + (230,), width=5)
        if kp > 0: d.line([(xp, 0), (xp, H * kp)], fill=GRN + (230,), width=5)
        pin(img, *cam.xy(-79.92, 9.39), "ATLANTIC ENTRANCE · 79.9° W", CYAN, ka, size=34)
        pin(img, *cam.xy(-79.55, 8.89), "PACIFIC ENTRANCE · 79.5° W", GRN, kp, up=False, size=34)
        try: tt = WT(i, "southeast")
        except KeyError: tt = t0 + 8
        if t >= tt - 0.8:
            arrow(img, partial(smooth(ipath(cam, CANAL)), 1.0)[::6] + [cam.xy(-79.53, 8.85)], ORG, ease((t - tt + 0.8) / 1.6), 18)
            if t > tt: big(img, "→ SOUTHEAST", t, tt, y=H / 2 + 60, size=96, color=ORG)
        if t >= WT(i, "east") - 0.1 and t < tt - 0.8:
            text_stroke(d, (W / 2, 150), "PACIFIC END IS FURTHER EAST", font(POPX, 66), YEL, stroke=8)
    elif key == "detour":
        x, y = cam.xy(-79.7, 9.1); k = ease((lt - 0.3) / 0.4)
        if k > 0:
            f = font(POPX, int(110 * k)); text_stroke(d, (x, y), "✕", f, RED, stroke=8)
            pin(img, x, y, "PANAMA: SLOTS CUT", RED, k, up=False, size=34)
        ks = ease((lt - 1.0) / 3.0); ka = ease((lt - 2.5) / 3.5)
        glow_line(img, partial(smooth(ipath(cam, SUEZ), 6), ks), ORG, 8, dash=(24, 14), phase=t * 60)
        glow_line(img, partial(smooth(ipath(cam, AFRICA), 6), ka), GOLD, 8, dash=(24, 14), phase=t * 60)
        pin(img, *cam.xy(*SHA), "ASIA", BLU, ease((lt - 0.6) / 0.4))
        pin(img, *cam.xy(-74.0, 40.7), "US EAST COAST", BLU, ease((lt - 0.8) / 0.4))
        if ks > 0.7: pin(img, *cam.xy(32.5, 30.0), "SUEZ", ORG, ease((ks - 0.7) / 0.2), size=34)
        if ka > 0.6: pin(img, *cam.xy(18.5, -35.5), "CAPE OF GOOD HOPE", GOLD, ease((ka - 0.6) / 0.2), up=False, size=34)
        d.text((W - 40, H - 150), "Routes simplified", font=font(POP, 26), fill=(255, 255, 255, 210), anchor="rm", stroke_width=3, stroke_fill=BLK)
    elif key == "rioindio":
        maplabel(d, cam.xy(-79.86, 9.17), "GATUN LAKE", 46, CYAN)
        pin(img, *cam.xy(-80.17, 8.95), "RÍO INDIO RESERVOIR (PLANNED)", GRN, ease((lt - 0.8) / 0.4), up=False, size=36)
        if lt > 1.6:
            p0, p1 = cam.xy(-80.15, 8.98), cam.xy(-79.98, 9.13)
            arrow(img, [p0, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - 40), p1], CYAN, ease((lt - 1.6) / 1.2), 14)
    if key in ("panama", "colon", "east", "rioindio") and cam.src == "esri":
        d.text((W - 40, H - 150), "Imagery: Esri World Imagery", font=font(POP, 24), fill=(255, 255, 255, 200), anchor="rm", stroke_width=3, stroke_fill=BLK)
    return img


# ------------------------------------------------------------------ cards
def bg_dark(t):
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]; xx = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
    base = np.array([10, 24, 48], np.float32) * (1 - 0.45 * yy) + np.array([20, 50, 90], np.float32) * 0.35 * (1 - ((xx - 0.5) ** 2 + (yy - 0.45) ** 2) * 2)
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA")


def dim_bg(name, t0, t1, t, a=0.55):
    im = render_kb(name, t0, t1, t).convert("RGBA").filter(ImageFilter.GaussianBlur(6))
    im.alpha_composite(Image.new("RGBA", (W, H), (6, 14, 30, int(255 * a)))); return im


def counter(d, xy, v, fmt, f, col, k):
    txt = fmt.format(v * ease(k)); text_stroke(d, xy, txt, f, col, stroke=9)


def render_card(key, t0, t1, t, i):
    lt = t - t0
    if key == "pools":
        img = dim_bg("A06", t0, t1, t, 0.7); d = ImageDraw.Draw(img)
        k = ease(lt / 1.2); text_stroke(d, (W / 2, 170), f"≈ {int(200 * k):,},000,000 L".replace("≈ 0,000,000", "≈ 0"), font(POPX, 104), CYAN, stroke=9)
        text_stroke(d, (W / 2, 270), "OF FRESH WATER PER CROSSING (OLD LOCKS)", font(POP, 38), WHT, stroke=5)
        try: tp = WT(i, "eighty") - 0.2
        except KeyError: tp = t0 + 1.5
        n = int(80 * ease((t - tp) / 2.4)) if t > tp else 0
        cw, chh, gx, gy = 140, 44, 20, 14; x0 = W / 2 - (10 * cw + 9 * gx) / 2; y0 = 330
        for q in range(80):
            x, y = x0 + (q % 10) * (cw + gx), y0 + (q // 10) * (chh + gy)
            if q < n:
                d.rounded_rectangle((x, y, x + cw, y + chh), 8, fill=(30, 150, 230, 255), outline=WHT, width=3)
                for ln in range(1, 4): d.line([(x + 8, y + chh * ln / 4), (x + cw - 8, y + chh * ln / 4)], fill=(255, 255, 255, 110), width=2)
            else: d.rounded_rectangle((x, y, x + cw, y + chh), 8, outline=(255, 255, 255, 60), width=2)
        if n > 0: text_stroke(d, (W / 2, 875), f"{n} OLYMPIC POOLS", font(POPX, 70), YEL, stroke=8)
        return img
    if key == "revenue":
        img = dim_bg("A23", t0, t1, t, 0.62); d = ImageDraw.Draw(img)
        ta, tb, tc = WT(i, "thirteen") - 0.2, WT(i, "five", 0) - 0.2, WT(i, "fifteen") - 0.2
        text_stroke(d, (W / 2, 140), "FISCAL YEAR 2025", font(POPX, 56), WHT, stroke=6)
        if t > ta:
            counter(d, (W / 2, 330), 13404, "{:,.0f}", font(POPX, 130), YEL, (t - ta) / 1.4)
            text_stroke(d, (W / 2, 430), "SHIPS CROSSED", font(POP, 42), WHT, stroke=5)
        if t > tb:
            counter(d, (W / 2, 610), 5.7, "${:.1f} BILLION", font(POPX, 130), GRN, (t - tb) / 1.4)
            text_stroke(d, (W / 2, 710), "REVENUE", font(POP, 42), WHT, stroke=5)
        if t > tc:
            badge(img, W / 2, 860, "> $15 MILLION EVERY DAY", RED, min(1.0, (t - tc) / 0.3) * (1.0 + 0.1 * max(0, 1 - (t - tc) / 0.3)), size=62)
        return img
    return bg_dark(t)


# ------------------------------------------------------------------ overlays tied to words
def callout(img, txt, t, t0, t1=None, y=170, size=74, col=YEL, sub=None):
    if t < t0 or (t1 is not None and t > t1 + 0.3): return
    k = min(1.0, (t - t0) / 0.22); s = 1.25 - 0.25 * ease(k)
    a = 1.0 if t1 is None or t < t1 else max(0, 1 - (t - t1) / 0.3)
    f = font(POPX, size * s); d = ImageDraw.Draw(img); tw = f.getlength(txt)
    sw = font(POP, size * 0.42).getlength(sub) if sub else 0
    bw = max(tw, sw) + 70; bh = size * s * 1.25 + (size * 0.55 if sub else 0)
    x0, y0 = W / 2 - bw / 2, y - size * s * 0.62
    pan = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(pan)
    pd.rounded_rectangle((x0 + 6, y0 + 8, x0 + bw + 6, y0 + bh + 8), 22, fill=(0, 0, 0, int(110 * a)))
    pd.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), 22, fill=(10, 18, 34, int(225 * a)), outline=col + (int(255 * a),), width=5)
    img.alpha_composite(pan)
    d.text((W / 2, y0 + size * s * 0.64), txt, font=f, fill=col + (int(255 * a),), anchor="mm")
    if sub: d.text((W / 2, y0 + size * s * 1.25 + size * 0.12), sub, font=font(POP, size * 0.42), fill=(255, 255, 255, int(255 * a)), anchor="mm")


def ev(i, w, nth=0, dt=-0.1):
    try: return WT(i, w, nth) + dt
    except KeyError: print("miss", i, w, file=sys.stderr); return 1e9


OVL = [  # (line, word, nth, text, sub, hold_until_word|seconds, color)
 (0, "eightytwo", 0, "82 KM", "THE WHOLE SHORTCUT", 3.0, YEL),
 (0, "million", 0, "≈ $1,000,000", "FOR ONE CROSSING", 3.2, GRN),
 (0, "four", 0, "≈ $4,000,000", "JUST TO SKIP THE LINE", 4.0, RED),
 (3, "twentyseven", 0, "427 M LONG", "NEOPANAMAX LOCK CHAMBER", 3.5, YEL),
 (3, "eiffel", 0, "427 M  vs  330 M", "LOCK CHAMBER vs EIFFEL TOWER", 3.5, YEL),
 (4, "fiftyfive", 0, "55 M × 18 M", "WIDTH × DEPTH", 3.5, YEL),
 (4, "ten", 0, "10,000+ CONTAINERS", None, 2.8, CYAN),
 (5, "twentysix", 0, "+26 M", "≈ AN 8-STORY BUILDING", 4.0, YEL),
 (8, "france", 0, "FRANCE · 1881–1889", None, 3.5, WHT),
 (8, "twenty", 0, "> 20,000 DEATHS", "HISTORIANS' ESTIMATE", 3.5, RED),
 (9, "nineteen", 0, "USA · 1904", None, 2.6, WHT),
 (9, "fifteenth", 0, "15 AUGUST 1914", "FIRST OFFICIAL CROSSING", 3.5, YEL),
 (9, "five", 0, "≈ $500 MILLION", None, 2.6, GRN),
 (9, "thousand", 0, "> 5,000 DEATHS", None, 3.0, RED),
 (10, "nineteen", 0, "1999", "CANAL HANDED TO PANAMA", 3.5, YEL),
 (10, "twenty", 0, "2016", "NEW, BIGGER LOCKS", 3.5, YEL),
 (13, "pilot", 0, "PILOT: COMPULSORY", None, 3.5, ORG),
 (14, "mules", 0, "\"MULES\"", "ELECTRIC TOWING LOCOMOTIVES", 3.2, YEL),
 (15, "million", 0, "UP TO ≈ $1,000,000", "LARGEST CONTAINER SHIPS", 4.0, GRN),
 (17, "auctions", 0, "SLOT AUCTIONS", None, 2.5, ORG),
 (17, "november", 0, "$3,975,000", "NOVEMBER 2023 · ONE CROSSING", 4.2, GRN),
 (17, "august", 0, "≈ $4,000,000", "AUGUST 2026", 3.2, GRN),
 (18, "twentyeight", 0, "1928", "RICHARD HALLIBURTON SWIMS THE CANAL", 4.0, WHT),
 (18, "thirtysix", 0, "$0.36", "THE CHEAPEST TOLL EVER", 3.5, YEL),
 (19, "thirtythree", 0, "GATES UP TO 33 M", None, 3.0, YEL),
 (19, "pumps", 0, "NO PUMPS — GRAVITY", None, 3.0, CYAN),
 (19, "three", 0, "3 STEPS · +26 M", None, 3.5, YEL),
 (20, "sixty", 0, "≈ 60% OF WATER REUSED", None, 3.5, CYAN),
 (21, "largest", 0, "LARGEST ARTIFICIAL LAKE", "WHEN IT WAS BUILT", 3.5, CYAN),
 (22, "no", 0, "NO RAIN = NO CANAL", None, 3.0, RED),
 (23, "continental", 0, "CONTINENTAL DIVIDE", "CULEBRA CUT", 3.5, YEL),
 (25, "forty", 0, "≈ 40% LESS RAIN", "2023", 4.0, RED),
 (26, "twenty", 0, "≈ 20 SLOTS A DAY", "AT THE WORST POINT", 3.5, RED),
 (28, "eleven", 0, "≈ 11 HOURS", None, 3.0, YEL),
 (28, "three", 0, "3 STEPS DOWN", "COCOLÍ LOCKS", 3.0, YEL),
 (29, "pacific", 0, "PACIFIC OCEAN", None, 3.0, CYAN),
 (30, "rain", 0, "THE REAL CURRENCY: RAIN", None, 4.0, CYAN),
 (31, "four", 0, "$4,000,000 TO SKIP A LINE?", "TELL US IN THE COMMENTS", 5.5, YEL),
]
OV = [(ev(i, w, n), txt, sub, max(0.8, min(hold, SC[i + 1] - 0.45 - ev(i, w, n))), col) for i, w, n, txt, sub, hold, col in OVL]


def overlays(img, t, k, map_or_card):
    if map_or_card: return
    for t0, txt, sub, hold, col in OV:
        if t0 <= t <= t0 + hold + 0.3: callout(img, txt, t, t0, t0 + hold, y=150, col=col, sub=sub)


CHAPTER = {"scale": "THE SCALE", "history": "HOW IT WAS BUILT", "anchor": "ARRIVAL", "money": "THE MONEY", "locks_up": "UP THE LOCKS",
           "lake": "GATUN LAKE", "cut": "THE CULEBRA CUT", "drought": "THE DROUGHT", "locks_down": "DOWN TO THE PACIFIC"}


def chapter_banner(img, t):
    for i in range(1, N):
        if CH[i] != CH[i - 1] and CH[i] in CHAPTER and SC[i] <= t < SC[i] + 3.6:
            lt = t - SC[i]; k = ease(lt / 0.5) * (1 - ease((lt - 3.1) / 0.5)); txt = CHAPTER[CH[i]]
            f = font(POPX, 44); tw = f.getlength(txt); x0 = 60 - (1 - k) * 700; y0 = 56
            d = ImageDraw.Draw(img)
            d.rounded_rectangle((x0, y0, x0 + tw + 76, y0 + 84), 18, fill=(12, 20, 38, 235), outline=WHT, width=4)
            d.rectangle((x0 + 14, y0 + 14, x0 + 26, y0 + 70), fill=YEL)
            d.text((x0 + 48, y0 + 44), txt, font=f, fill=WHT, anchor="lm")


def subscribe(img, t):
    i = 11; a = SC[i]
    if not (a + 0.8 <= t < SC[i + 1] - 0.2): return
    lt = t - a - 0.8; k = min(1.0, lt / 0.3)
    f = font(POPX, 60); d = ImageDraw.Draw(img); txt = "SUBSCRIBE" if lt < 3.0 else "SUBSCRIBED ✓"
    col = (220, 30, 30) if lt < 3.0 else (90, 90, 90)
    tw = f.getlength(txt); x0, y0 = W / 2 - tw / 2 - 50, H / 2 + 120
    d.rounded_rectangle((x0, y0, x0 + tw + 100, y0 + 110 * k), 26, fill=col + (255,))
    if k >= 1: d.text((W / 2, y0 + 56), txt, font=f, fill=WHT, anchor="mm")
    if 1.8 < lt < 3.3: paste_emoji(img, "👆", W / 2 + tw / 2 + 10 - (lt - 1.8) * 30, y0 + 110, 90)


def ai_label(img, kind, arg):
    name = arg[0] if kind == "A" else arg
    txt = "AI RECONSTRUCTION — NOT ARCHIVAL FOOTAGE" if name in ARCHIVAL else "AI-GENERATED ILLUSTRATION"
    ImageDraw.Draw(img).text((W - 36, 40), txt, font=font(POP, 24), fill=(255, 255, 255, 190), anchor="rt", stroke_width=2, stroke_fill=BLK)


# ------------------------------------------------------------------ frame
def base(k, t):
    t0, t1, i, kind, arg, opts = TL[k]
    if kind == "A": im = render_clip(arg, t0, t1, t, opts).convert("RGBA")
    elif kind == "K": im = render_kb(arg, t0, t1, t).convert("RGBA")
    elif kind == "M": return render_map(arg, t0, t1, t, i)
    else: return render_card(arg, t0, t1, t, i)
    ai_label(im, kind, arg)
    return im


def caption(img, t):
    for i in range(N):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.15:
            words = LINES[i].split(); cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05: cur = j
            c0 = cur // 5 * 5; chunk = words[c0:c0 + 5]
            f = font(POPX, 44); gap = f.getlength(" ") * 1.4
            ws = [f.getlength(w) for w in chunk]; tot = sum(ws) + gap * (len(chunk) - 1)
            x = (W - tot) / 2; d = ImageDraw.Draw(img)
            for j, (w, ww) in enumerate(zip(chunk, ws)):
                col = YEL if c0 + j == cur else WHT
                d.text((x + 3, H - 82 + 3), w, font=f, fill=(0, 0, 0, 160), anchor="lm")
                d.text((x, H - 82), w, font=f, fill=col, anchor="lm", stroke_width=6, stroke_fill=BLK)
                x += ww + gap
            return


GRAIN = np.random.default_rng(3).normal(0, 3.0, (H + 256, W + 256, 1)).astype(np.float32)


def frame(fi):
    t = fi / FPS; k = shot_at(t); t0 = TL[k][0]
    img = base(k, t)
    if k > 0 and t - t0 < 0.3:
        a = ease((t - t0) / 0.3); prev = base(k - 1, t)
        img = Image.blend(prev, img, a)
    overlays(img, t, k, TL[k][3] in ("M", "C"))
    chapter_banner(img, t); subscribe(img, t)
    caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32) * vignette()
    if t < 0.6: rgb *= t / 0.6
    if t > TOTAL - 1.5: rgb *= max(0, (TOTAL - t) / 1.5)
    gy, gx = (fi * 37) % 256, (fi * 91) % 256
    rgb += GRAIN[gy:gy + H, gx:gx + W]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2), "shots", len(TL))
        for x in TL: print(round(x[0], 2), round(x[1] - x[0], 2), x[2], x[3], x[4])
    elif cmd == "still":
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills/s_{float(a):06.1f}.jpg", quality=88)
    elif cmd == "prefetch":
        keys = []
        for k, (t0, t1, i, kind, arg, o) in enumerate(TL):
            if kind != "M": continue
            for q in range(13): keys += map_cam(arg, t0, t1, t0 + (t1 - t0) * q / 12).keys()
        print(tiles.prefetch(sorted(set(keys))))
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 300 == 0: print(fi, flush=True)
        p.stdin.close(); p.wait()
