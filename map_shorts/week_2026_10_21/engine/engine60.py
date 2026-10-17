"""Geography map Shorts engine (week of 21.10.2026), vertical 1080x1920.
Run in /home/claude/v60:  SHORT=<key> python3 engine60.py info | still t.. | video A B out.mp4
Scenes live in shots60.py; voice timing in <key>/timing.json (Lumean alignment)."""
import json
import math
import os
import subprocess
import sys
from functools import lru_cache

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/week_2026_10_21")
from scripts import SHORTS  # noqa: E402
from sat60 import SP, W_IMG, H_IMG  # noqa: E402

W, H, FPS = 1080, 1920, 30
POPX, POPB, TITAN = "assets/Poppins-ExtraBold.ttf", "assets/Poppins-Bold.ttf", "assets/titan-one.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (70, 205, 100), (80, 170, 255), (255, 255, 255), (0, 0, 0)
ORG, CYAN, PINK = (255, 150, 40), (90, 220, 255), (255, 80, 160)

SHORT = os.environ.get("SHORT", "pheasant")
LINES = SHORTS[SHORT]["lines"]
TM = json.load(open(f"{SHORT}/timing.json"))
LEAD = 0.3
ST = [LEAD + s for s in TM["starts"]]
D, TW = TM["D"], TM["T"]
TOTAL = ST[-1] + D[-1] + 0.8
NF = int(TOTAL * FPS)

_FONTS = {}


def font(path, size):
    k = (path, int(size))
    if k not in _FONTS:
        _FONTS[k] = ImageFont.truetype(path, max(8, int(size)))
    return _FONTS[k]


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def clean(w):
    return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word, nth=0):
    ws = [clean(w) for w in LINES[i].split()]
    q = clean(word)
    hits = [j for j, w in enumerate(ws) if w == q] or [j for j, w in enumerate(ws) if q in w]
    if not hits:
        raise KeyError((i, word))
    return ST[i] + TW[i][hits[min(nth, len(hits) - 1)]]


# ------------------------------------------------------------------ geo + imagery
def geo(key, lon, lat):
    lon0, lat0, d = SP[key]
    dl = d * (W_IMG / H_IMG) / math.cos(math.radians(lat0))
    return (lon - (lon0 - dl)) / (2 * dl), (lat0 + d - lat) / (2 * d)


@lru_cache(maxsize=8)
def sat(key):
    return Image.open(f"sat/{key}.jpg").convert("RGB")


def view(im, z, cx, cy, w=W, h=H):
    iw, ih = im.size
    s = max(w / iw, h / ih) * z
    bw, bh = w / s, h / s
    x0 = min(max(0.0, cx * iw - bw / 2), iw - bw)
    y0 = min(max(0.0, cy * ih - bh / 2), ih - bh)
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + bw, y0 + bh)), (x0, y0, s)


def to_screen(m, key, lon, lat):
    x0, y0, s = m
    fx, fy = geo(key, lon, lat)
    return (fx * W_IMG - x0) * s, (fy * H_IMG - y0) * s


_SHP = shapefile.Reader("assets/ne50/ne_50m_admin_0_countries.shp")
_FIELDS = [f[0] for f in _SHP.fields[1:]]
COUNTRY = {}
for _sr in _SHP.iterShapeRecords():
    _rec = dict(zip(_FIELDS, _sr.record))
    _pts = _sr.shape.points
    _parts = list(_sr.shape.parts) + [len(_pts)]
    COUNTRY[_rec["ADMIN"]] = [np.array(_pts[a:b]) for a, b in zip(_parts[:-1], _parts[1:])]


# ------------------------------------------------------------------ drawing helpers
def fit(fname, size, txt, maxw):
    f = font(fname, size)
    while f.getlength(txt) > maxw and f.size > 14:
        f = font(fname, f.size - 2)
    return f


def glow_text(img, xy, txt, f, col, a=1.0, anchor="mm", glow=None, stroke=None):
    x, y = xy
    bb = ImageDraw.Draw(img).textbbox((x, y), txt, font=f, anchor=anchor, stroke_width=(stroke or 3))
    pad = 40
    box = (int(bb[0] - pad), int(bb[1] - pad), int(bb[2] + pad), int(bb[3] + pad))
    pw, ph = box[2] - box[0], box[3] - box[1]
    if pw <= 0 or ph <= 0:
        return
    loc = (x - box[0], y - box[1])
    if glow:
        g = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        ImageDraw.Draw(g).text(loc, txt, font=f, fill=glow + (int(220 * a),), anchor=anchor,
                               stroke_width=max(6, int(f.size * 0.18)), stroke_fill=glow + (int(220 * a),))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(12)), (box[0], box[1]))
    sh = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((loc[0] + 3, loc[1] + 5), txt, font=f, fill=(0, 0, 0, int(160 * a)), anchor=anchor)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), (box[0], box[1]))
    ImageDraw.Draw(img).text((x, y), txt, font=f, fill=col + (int(255 * a),), anchor=anchor,
                             stroke_width=stroke or max(2, int(f.size * 0.06)), stroke_fill=(0, 0, 0, int(220 * a)))


def label(img, txt, x, y, t, t0, size=64, col=WHT, glow=None, anchor="mm", maxw=W - 120, fname=POPX):
    if t < t0:
        return
    k = ease((t - t0) / 0.18)
    s = 1.25 - 0.25 * k
    glow_text(img, (x, y), txt, fit(fname, size * s, txt, maxw), col, min(1.0, k * 1.5), anchor, glow)


def pill(img, txt, cx, cy, sz, bg, fg=WHT, a=1.0):
    f = font(POPX, sz)
    pw, ph = f.getlength(txt) + sz * 1.3, sz * 1.75
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((cx - pw / 2, cy - ph / 2, cx + pw / 2, cy + ph / 2), int(ph * 0.3), fill=bg + (int(230 * a),),
                        outline=WHT + (int(255 * a),), width=2)
    d.text((cx, cy), txt, font=f, fill=fg + (int(255 * a),), anchor="mm")


def counter(img, v0, v1, fmt, x, y, t, t0, dur, size, col=YEL, glow=None):
    if t < t0:
        return
    v = v0 + (v1 - v0) * ease((t - t0) / dur)
    label(img, fmt.format(v), x, y, t, t0, size, col, glow)


def grad_title(img, txt, cx, cy, size, t, t0, maxw=W - 100):
    if t < t0:
        return
    k = ease((t - t0) / 0.25)
    f = font(TITAN, size * (1.4 - 0.4 * k))
    while f.getlength(txt) > maxw and f.size > 20:
        f = font(TITAN, f.size - 2)
    bb = ImageDraw.Draw(img).textbbox((cx, cy), txt, font=f, anchor="mm", stroke_width=20)
    pad = 40
    box = (int(bb[0] - pad), int(bb[1] - pad), int(bb[2] + pad), int(bb[3] + pad))
    pw, ph = box[2] - box[0], box[3] - box[1]
    loc = (cx - box[0], cy - box[1])
    lay = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    gl = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    ImageDraw.Draw(gl).text(loc, txt, font=f, fill=PINK + (220,), anchor="mm", stroke_width=24, stroke_fill=PINK + (220,))
    lay.alpha_composite(gl.filter(ImageFilter.GaussianBlur(16)))
    d = ImageDraw.Draw(lay)
    d.text(loc, txt, font=f, fill=BLK + (255,), anchor="mm", stroke_width=16, stroke_fill=BLK + (255,))
    d.text(loc, txt, font=f, fill=WHT + (255,), anchor="mm", stroke_width=5, stroke_fill=WHT + (255,))
    m = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(m).text(loc, txt, font=f, fill=255, anchor="mm")
    b2 = m.getbbox()
    if b2:
        g = np.zeros((ph, pw, 3), np.uint8)
        stops = ((255, 214, 64), (255, 132, 52), (255, 52, 140), (150, 50, 210))
        for y in range(b2[1], b2[3] + 1):
            tt = (y - b2[1]) / max(1, b2[3] - b2[1])
            kk = tt * 3
            i = min(int(kk), 2)
            u = kk - i
            g[y] = [int(stops[i][c] * (1 - u) + stops[i + 1][c] * u) for c in range(3)]
        gi = Image.fromarray(g).convert("RGBA")
        gi.putalpha(m.filter(ImageFilter.MinFilter(7)))
        lay.alpha_composite(gi)
    if k < 1:
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * min(1.0, k * 1.6))))
    img.alpha_composite(lay, (box[0], box[1]))


def tags(img, items, t, x=60, y0=520, dy=88, size=44):
    for q, (txt, t0) in enumerate(items):
        if t < t0:
            continue
        k = ease((t - t0) / 0.2)
        f = font(POPX, size)
        w = f.getlength(txt) + 60
        y = y0 + q * dy
        xx = x - (1 - k) * 120
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((xx, y - 32, xx + w, y + 32), 14, fill=(10, 8, 24, int(205 * k)), outline=CYAN + (int(255 * k),), width=3)
        d.text((xx + 30, y), txt, font=f, fill=WHT + (int(255 * k),), anchor="lm")


def pin(img, X, Y, txt, t, t0, col=PINK, side=1):
    if t < t0:
        return
    k = ease((t - t0) / 0.3)
    d = ImageDraw.Draw(img)
    pul = 0.5 + 0.5 * math.sin((t - t0) * 6)
    for r in (46 + 30 * pul, 30):
        d.ellipse((X - r, Y - r, X + r, Y + r), outline=col + (int((90 if r > 31 else 255) * k),), width=4)
    d.ellipse((X - 11, Y - 11, X + 11, Y + 11), fill=col + (int(255 * k),), outline=WHT + (255,), width=3)
    if txt:
        f = fit(POPX, 38, txt, 560)
        w = f.getlength(txt) + 40
        lx = X + 60 if side > 0 else X - 60 - w
        lx = min(max(20, lx), W - 20 - w)
        ly = Y - 90
        d.line((X, Y - 12, lx + (0 if side > 0 else w), ly + 24), fill=WHT + (int(255 * k),), width=3)
        d.rounded_rectangle((lx, ly - 4, lx + w, ly + 52), 12, fill=(10, 8, 24, int(215 * k)), outline=col + (int(255 * k),), width=3)
        d.text((lx + 20, ly + 24), txt, font=f, fill=WHT + (int(255 * k),), anchor="lm")


def route(img, pts, t, t0, dur=1.6, col=CYAN, width=10, dashed=False):
    if t < t0 or len(pts) < 2:
        return
    k = ease((t - t0) / dur)
    Ls = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(Ls) * k
    out = [pts[0]]
    for i, l in enumerate(Ls):
        if tot <= 0:
            break
        u = min(1.0, tot / max(l, 1e-6))
        out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u))
        tot -= l
    g = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0))
    ImageDraw.Draw(g).line([(x / 4, y / 4) for x, y in out], fill=col + (200,), width=max(2, width * 3 // 4), joint="curve")
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    if not dashed:
        d.line(out, fill=WHT + (255,), width=width, joint="curve")
        d.line(out, fill=col + (255,), width=max(3, width - 4), joint="curve")
        return
    seg, gap = 34, 22
    for a, b in zip(out[:-1], out[1:]):
        L = math.dist(a, b)
        p = 0.0
        while p < L:
            q = min(L, p + seg)
            pa = (a[0] + (b[0] - a[0]) * p / L, a[1] + (b[1] - a[1]) * p / L)
            pb = (a[0] + (b[0] - a[0]) * q / L, a[1] + (b[1] - a[1]) * q / L)
            d.line((pa, pb), fill=col + (255,), width=width)
            p += seg + gap


def screen_rings(key, m, rings, dlon=0.0, dlat=0.0):
    out = []
    for r in rings:
        pts = [to_screen(m, key, lo + dlon, la + dlat) for lo, la in r]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        if max(xs) < -200 or min(xs) > W + 200 or max(ys) < -200 or min(ys) > H + 200 or len(pts) < 3:
            continue
        out.append(pts)
    return out


def country(img, key, m, name, t, t0, col, fill=0.3, dlon=0.0, dlat=0.0, width=6):
    if t < t0:
        return
    k = ease((t - t0) / 0.4)
    rings = screen_rings(key, m, COUNTRY[name], dlon, dlat)
    if not rings:
        return
    lay = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for r in rings:
        rr = [(x / 2, y / 2) for x, y in r]
        if fill > 0:
            d.polygon(rr, fill=col + (int(255 * fill * k),))
        d.line(rr + [rr[0]], fill=col + (int(170 * k),), width=width * 2)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR))
    d2 = ImageDraw.Draw(img)
    for r in rings:
        d2.line(r + [r[0]], fill=WHT + (int(255 * k),), width=max(2, width // 2), joint="curve")


def circle_km(img, key, m, lon, lat, km, t, t0, col=YEL):
    if t < t0:
        return
    k = ease((t - t0) / 0.6)
    dlat = km / 111.0
    dlon = km / (111.0 * math.cos(math.radians(lat)))
    pts = [to_screen(m, key, lon + dlon * math.cos(a), lat + dlat * math.sin(a)) for a in np.linspace(0, 2 * math.pi * k, 90)]
    if len(pts) > 1:
        d = ImageDraw.Draw(img)
        d.line(pts, fill=WHT + (255,), width=9)
        d.line(pts, fill=col + (255,), width=5)


def flag(img, code, x, y, w, a=1.0):
    """Simplified national flag (no emblems), centred at x, y, width w."""
    h = int(w * 2 / 3)
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(f)

    def hz(cols, ratios=None):
        ratios = ratios or [1] * len(cols)
        tot = sum(ratios)
        y0 = 0
        for c, r in zip(cols, ratios):
            y1 = y0 + h * r / tot
            d.rectangle((0, y0, w, y1), fill=c)
            y0 = y1

    def vt(cols):
        for i, c in enumerate(cols):
            d.rectangle((w * i / len(cols), 0, w * (i + 1) / len(cols), h), fill=c)

    if code == "ES":
        hz([(170, 21, 27), (241, 191, 0), (170, 21, 27)], [1, 2, 1])
    elif code == "FR":
        vt([(0, 35, 149), (255, 255, 255), (237, 41, 57)])
    elif code == "BE":
        vt([(0, 0, 0), (253, 218, 36), (239, 51, 64)])
    elif code == "NL":
        hz([(174, 28, 40), (255, 255, 255), (33, 70, 139)])
    elif code == "BO":
        hz([(213, 43, 30), (249, 228, 0), (0, 122, 51)])
    elif code == "EG":
        hz([(206, 17, 38), (255, 255, 255), (0, 0, 0)])
        d.ellipse((w / 2 - h * 0.11, h / 2 - h * 0.11, w / 2 + h * 0.11, h / 2 + h * 0.11), fill=(192, 147, 0))
    elif code == "RU":
        hz([(255, 255, 255), (0, 57, 166), (213, 43, 30)])
    elif code == "US":
        for i in range(13):
            d.rectangle((0, h * i / 13, w, h * (i + 1) / 13), fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
        d.rectangle((0, 0, w * 0.4, h * 7 / 13), fill=(60, 59, 110))
        for r in range(4):
            for c in range(5):
                cx, cy = w * 0.4 * (c + 0.5) / 5, h * 7 / 13 * (r + 0.5) / 4
                d.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=(255, 255, 255))
    elif code == "CL":
        d.rectangle((0, 0, w, h / 2), fill=(255, 255, 255))
        d.rectangle((0, h / 2, w, h), fill=(213, 43, 30))
        d.rectangle((0, 0, h / 2, h / 2), fill=(0, 57, 166))
        cx, cy, R = h / 4, h / 4, h * 0.13
        star = [(cx + (R if i % 2 == 0 else R * 0.4) * math.sin(i * math.pi / 5), cy - (R if i % 2 == 0 else R * 0.4) * math.cos(i * math.pi / 5)) for i in range(10)]
        d.polygon(star, fill=(255, 255, 255))
    elif code == "AU":
        d.rectangle((0, 0, w, h), fill=(1, 33, 105))
        for cx, cy, R in ((w * 0.75, h * 0.25, h * 0.06), (w * 0.62, h * 0.5, h * 0.06), (w * 0.75, h * 0.8, h * 0.06), (w * 0.88, h * 0.45, h * 0.06), (w * 0.25, h * 0.75, h * 0.1)):
            star = [(cx + (R if i % 2 == 0 else R * 0.45) * math.sin(i * math.pi / 7), cy - (R if i % 2 == 0 else R * 0.45) * math.cos(i * math.pi / 7)) for i in range(14)]
            d.polygon(star, fill=(255, 255, 255))
        d.rectangle((0, 0, w / 2, h / 2), fill=(1, 33, 105))
        d.line((0, 0, w / 2, h / 2), fill=(255, 255, 255), width=max(3, h // 10))
        d.line((0, h / 2, w / 2, 0), fill=(255, 255, 255), width=max(3, h // 10))
        d.line((0, 0, w / 2, h / 2), fill=(200, 16, 46), width=max(1, h // 30))
        d.line((0, h / 2, w / 2, 0), fill=(200, 16, 46), width=max(1, h // 30))
        d.rectangle((w / 4 - h / 18, 0, w / 4 + h / 18, h / 2), fill=(255, 255, 255))
        d.rectangle((0, h / 4 - h / 18, w / 2, h / 4 + h / 18), fill=(255, 255, 255))
        d.rectangle((w / 4 - h / 36, 0, w / 4 + h / 36, h / 2), fill=(200, 16, 46))
        d.rectangle((0, h / 4 - h / 36, w / 2, h / 4 + h / 36), fill=(200, 16, 46))
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), max(4, w // 14), fill=int(255 * a))
    f.putalpha(m)
    sh = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((20, 26, w + 20, h + 26), max(4, w // 14), fill=(0, 0, 0, int(140 * a)))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)), (int(x - w / 2 - 20), int(y - h / 2 - 20)))
    img.alpha_composite(f, (int(x - w / 2), int(y - h / 2)))
    ImageDraw.Draw(img).rounded_rectangle((x - w / 2, y - h / 2, x + w / 2, y + h / 2), max(4, w // 14), outline=WHT + (int(255 * a),), width=4)


def credit(img, txt):
    ImageDraw.Draw(img).text((W - 18, H - 12), txt, font=font(POPB, 17), fill=(255, 255, 255, 170), anchor="rs")


# ------------------------------------------------------------------ custom diagrams
def flipflags(img, x, y, t, t0, t1, a="ES", b="FR", w=300):
    if not (t0 <= t < t1):
        return
    ph = (t - t0) / 0.6
    side = int(ph) % 2
    u = ph - int(ph)
    sx = abs(math.cos(math.pi * min(1.0, u / 0.25))) if u < 0.25 else 1.0
    code = (a, b)[side]
    lay = Image.new("RGBA", (w + 60, w), (0, 0, 0, 0))
    flag(lay, code, (w + 60) // 2, w // 2, w)
    ww = max(2, int((w + 60) * (sx if u < 0.25 else 1.0)))
    lay = lay.resize((ww, w))
    img.alpha_composite(lay, (int(x - ww / 2), int(y - w / 2)))


def enclaves(img, t, t_be, t_nl):
    """Schematic of Baarle: Dutch land with Belgian pieces, some with Dutch pieces inside."""
    x0, y0, x1, y1 = 90, 420, 990, 1320
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((x0, y0, x1, y1), 30, fill=(240, 140, 40, 235), outline=WHT + (255,), width=5)
    d.text((x0 + 30, y0 + 40), "NETHERLANDS", font=font(POPX, 40), fill=WHT, anchor="lm", stroke_width=3, stroke_fill=BLK)
    rng = np.random.default_rng(22)
    pieces = []
    for _ in range(22):
        for _try in range(60):
            w, h = rng.integers(60, 190), rng.integers(50, 150)
            px, py = rng.integers(x0 + 30, x1 - 30 - w), rng.integers(y0 + 90, y1 - 30 - h)
            if all(px + w + 12 < a or a + c + 12 < px or py + h + 12 < b or b + e + 12 < py for a, b, c, e in pieces):
                pieces.append((px, py, w, h))
                break
    shown = int(min(22, max(0, (t - t_be) / 0.08))) if t >= t_be else 0
    for q, (px, py, w, h) in enumerate(pieces[:shown]):
        d.rounded_rectangle((px, py, px + w, py + h), 12, fill=(250, 214, 30, 255), outline=BLK + (255,), width=4)
    if t >= t_nl:
        k = ease((t - t_nl) / 0.4)
        big = sorted(pieces, key=lambda p: -p[2] * p[3])[:3]
        for px, py, w, h in big:
            iw, ih = max(20, w * 0.38 * k), max(20, h * 0.38 * k)
            cx, cy = px + w / 2, py + h / 2
            d.rounded_rectangle((cx - iw / 2, cy - ih / 2, cx + iw / 2, cy + ih / 2), 8, fill=(240, 140, 40, 255), outline=WHT + (255,), width=3)
    pill(img, "SCHEMATIC · NOT TO SCALE", 540, y1 + 50, 22, (40, 40, 50))
    if shown:
        label(img, f"{shown} PIECES OF BELGIUM", 540, 340, t, t_be, 66, YEL, BLK)


def house(img, t, t0, t_move):
    """Front-door rule: a house cut by the border; the door decides the country."""
    if t < t0:
        return
    k = ease((t - t0) / 0.3)
    d = ImageDraw.Draw(img)
    bx0, by0, bx1, by1 = 190, 760, 890, 1300
    d.polygon([(bx0 - 40, by0), (540, 520), (bx1 + 40, by0)], fill=(150, 50, 40, int(255 * k)), outline=WHT + (int(255 * k),))
    d.rectangle((bx0, by0, bx1, by1), fill=(235, 225, 205, int(255 * k)), outline=WHT + (int(255 * k),), width=5)
    for wx in (250, 690):
        d.rectangle((wx, 840, wx + 140, 960), fill=(120, 180, 230, int(255 * k)), outline=BLK + (int(255 * k),), width=4)
    moved = ease((t - t_move) / 0.6) if t >= t_move else 0.0
    dx = 300 + (680 - 300) * moved
    d.rectangle((dx - 70, 1070, dx + 70, by1), fill=(110, 60, 30, int(255 * k)), outline=BLK + (int(255 * k),), width=4)
    d.ellipse((dx + 35, 1180, dx + 51, 1196), fill=YEL + (int(255 * k),))
    route(img, [(540, 470), (540, 1380)], t, t0 + 0.2, 0.5, WHT, 8, dashed=True)
    flag(img, "BE", 330, 1440, 170, k)
    flag(img, "NL", 750, 1440, 170, k)
    lab = "THIS HOUSE IS BELGIAN" if moved < 0.5 else "NOW IT'S DUTCH"
    label(img, lab, 540, 430, t, t0 + 0.3 if moved < 0.5 else t_move + 0.3, 62, YEL, BLK)


def clocks(img, t, t0):
    if t < t0:
        return
    k = ease((t - t0) / 0.35)
    for cx, title, day, hh, mm, col in ((540, "BIG DIOMEDE · RUSSIA", "TUESDAY", 9, 0, YEL), (540, "LITTLE DIOMEDE · USA", "MONDAY", 12, 0, CYAN)):
        cy = 720 if "BIG" in title else 1230
        R = 170 * (0.8 + 0.2 * k)
        d = ImageDraw.Draw(img)
        d.ellipse((cx - 330 - R, cy - R, cx - 330 + R, cy + R), fill=(15, 12, 30, int(235 * k)), outline=col + (int(255 * k),), width=8)
        ox = cx - 330
        for q in range(12):
            a = q * math.pi / 6
            d.line((ox + (R - 24) * math.sin(a), cy - (R - 24) * math.cos(a), ox + (R - 8) * math.sin(a), cy - (R - 8) * math.cos(a)), fill=WHT + (int(255 * k),), width=5)
        ah = (hh % 12 + mm / 60) * math.pi / 6
        am = mm * math.pi / 30
        d.line((ox, cy, ox + R * 0.5 * math.sin(ah), cy - R * 0.5 * math.cos(ah)), fill=WHT + (int(255 * k),), width=12)
        d.line((ox, cy, ox + R * 0.78 * math.sin(am), cy - R * 0.78 * math.cos(am)), fill=WHT + (int(255 * k),), width=7)
        glow_text(img, (cx + 150, cy - 70), title, fit(POPX, 40, title, 560), WHT, k)
        glow_text(img, (cx + 150, cy + 10), day, font(POPX, 76), col, k)
        glow_text(img, (cx + 150, cy + 90), f"{hh}:{mm:02d}", font(POPX, 64), WHT, k)


# ------------------------------------------------------------------ shot list
SH = []


def S(t0, kind, *args):
    SH.append([max(0.0, t0), kind, args, []])


def O(fn, *args):
    SH[-1][3].append((fn, args))


import shots60  # noqa: E402

HOOK = shots60.build(SHORT, S, O, WT, ST, D)
CUTS = [s[0] for s in SH[1:]]
SHAKES = []
for _s in SH:
    for _fn, _a in _s[3]:
        if _fn in ("counter", "slam"):
            SHAKES.append((_a[5] if _fn == "counter" else _a[3]) + 0.02)


def scene_t(i):
    return SH[i][0], (SH[i + 1][0] if i + 1 < len(SH) else TOTAL)


def shot_at(t):
    for k in range(len(SH) - 1, -1, -1):
        if t >= SH[k][0]:
            return k
    return 0


_BG = {}


def card_bg(key):
    if key not in _BG:
        im, _ = view(sat(key), 1.1, 0.5, 0.5)
        _BG[key] = Image.eval(im.filter(ImageFilter.GaussianBlur(12)), lambda v: int(v * 0.6)).convert("RGBA")
    return _BG[key].copy()


def cam(k, t):
    t0, t1 = scene_t(k)
    key, z0, z1, cx, cy = SH[k][2]
    u = ease((t - t0) / max(0.1, t1 - t0))
    if isinstance(cx, tuple):                         # cx = (lon, lat): centre on a place
        cx, cy = geo(key, *cx)
    return key, z0 + (z1 - z0) * u, cx, cy


def base(k, t):
    kind = SH[k][1]
    if kind == "sat":
        key, z, cx, cy = cam(k, t)
        im, m = view(sat(key), z, cx, cy)
        return im.convert("RGBA"), (key, m)
    key = SH[k][2][0]
    return card_bg(key), (key, view(sat(key), 1.1, 0.5, 0.5)[1])


def overlays(img, t, k, km):
    key, m = km
    for fn, a in SH[k][3]:
        if fn == "big":
            txt, x, y, ts, size, col, glow = a
            label(img, txt, x, y, t, ts, size, col, glow)
        elif fn == "slam":
            txt, x, y, ts, size, col, glow = a
            label(img, txt, x, y, t, ts, size, col, glow)
        elif fn == "counter":
            v0, v1, fmt, x, y, ts, dur, size, col, glow = a
            counter(img, v0, v1, fmt, x, y, t, ts, dur, size, col, glow)
        elif fn == "pin":
            lon, lat, txt, ts = a[:4]
            col = a[4] if len(a) > 4 else PINK
            X, Y = to_screen(m, key, lon, lat)
            pin(img, X, Y, txt, t, ts, col, side=-1 if X > 600 else 1)
        elif fn == "geolabel":
            lon, lat, txt, ts, size, col = a
            X, Y = to_screen(m, key, lon, lat)
            label(img, txt, X, Y, t, ts, size, col, BLK)
        elif fn == "country":
            name, ts, col, fill = a[:4]
            dlon, dlat = (a[4], a[5]) if len(a) > 5 else (0.0, 0.0)
            country(img, key, m, name, t, ts, col, fill, dlon, dlat)
        elif fn == "route":
            pts, ts, dur, col, width, dashed = a
            route(img, [to_screen(m, key, lo, la) for lo, la in pts], t, ts, dur, col, width, dashed)
        elif fn == "sroute":                               # screen-space route
            pts, ts, dur, col, width, dashed = a
            route(img, pts, t, ts, dur, col, width, dashed)
        elif fn == "circle":
            lon, lat, km_, ts, col = a
            circle_km(img, key, m, lon, lat, km_, t, ts, col)
        elif fn == "flag":
            code, x, y, w, ts = a
            if t >= ts:
                flag(img, code, x, y, w, ease((t - ts) / 0.25))
        elif fn == "pill":
            txt, x, y, sz, ts = a
            if t >= ts:
                pill(img, txt, x, y, sz, (30, 30, 46), a=ease((t - ts) / 0.25))
        elif fn == "tags":
            tags(img, a[0], t, y0=a[1] if len(a) > 1 else 520)
        elif fn == "flipflags":
            flipflags(img, *a[:2], t, *a[2:])
        elif fn == "enclaves":
            enclaves(img, t, *a)
        elif fn == "house":
            house(img, t, *a)
        elif fn == "clocks":
            clocks(img, t, *a)
        elif fn == "tint":
            col, alpha, ts = a
            if t >= ts:
                img.alpha_composite(Image.new("RGBA", (W, H), col + (int(alpha * ease((t - ts) / 0.5)),)))


def hook(img, t):
    a, b = HOOK
    if t <= 3.0:
        grad_title(img, a, 540, 250, 96, t, -0.3)
        grad_title(img, b, 540, 370, 96, t, -0.3)
    elif t < TOTAL - 0.5:
        txt = f"{a} {b}"
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((60, 66, 1020, 140), 22, fill=(8, 8, 20, 190), outline=PINK + (255,), width=3)
        d.text((540, 103), txt, font=fit(POPX, 34, txt, 900), fill=WHT, anchor="mm")


def caption(img, t):
    for i in range(len(LINES)):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.2:
            words = LINES[i].split()
            cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05:
                    cur = j
            c0 = cur // 3 * 3
            chunk = words[c0:c0 + 3]
            f = fit(POPX, 74, " ".join(chunk), 980)
            widths = [f.getlength(w + " ") for w in chunk]
            x = 540 - (sum(widths) - f.getlength(" ")) / 2
            for j, w in enumerate(chunk):
                col = YEL if c0 + j == cur else WHT
                glow_text(img, (x, 1630), w, f, col, 1.0, "lm", None, 5)
                x += widths[j]
            return


YY, XX = np.mgrid[0:H, 0:W]
VIG = (1 - 0.30 * (((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) / 2).astype(np.float32)[..., None]
del YY, XX


def post(img, t):
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    sk = 0.0
    for s in SHAKES:
        if 0 <= t - s < 0.25:
            sk = max(sk, 12 * (1 - (t - s) / 0.25))
    dx, dy = int(sk * math.sin(t * 90)), int(sk * math.cos(t * 77))
    if dx or dy:
        a = np.roll(a, (dy, dx), axis=(0, 1))
    a = (a * VIG - 128) * 1.06 + 128
    rng = np.random.default_rng(int(t * 30) % 997)
    g = rng.normal(0, 4.0, (H // 2, W // 2)).astype(np.float32)
    a += np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None]
    cut = min([abs(t - c) for c in CUTS] + [9])
    if cut < 0.1:
        a += 50 * (1 - cut / 0.1)
    return np.clip(a, 0, 255).astype(np.uint8)


def whip(prev, nxt, u):
    p = np.asarray(prev.convert("RGB")).astype(np.float32)
    n = np.asarray(nxt.convert("RGB")).astype(np.float32)
    k = int(80 * math.sin(math.pi * u))
    src = p if u < 0.5 else n
    out = np.zeros_like(p)
    for s in range(-3, 4):
        out += np.roll(src, int(s * k / 3), axis=1)
    return Image.fromarray(np.clip(out / 7, 0, 255).astype(np.uint8)).convert("RGBA")


def frame(fi):
    t = fi / FPS
    k = shot_at(t)
    img, km = base(k, t)
    if k > 0 and t - SH[k][0] < 0.12:
        img = whip(base(k - 1, t)[0], img, (t - SH[k][0]) / 0.12)
    overlays(img, t, k, km)
    uses_ne = any(fn in ("country",) for fn, _ in SH[k][3])
    credit(img, "Imagery © Esri, Maxar, Earthstar Geographics" + (" · Borders: Natural Earth" if uses_ne else ""))
    hook(img, t)
    caption(img, t)
    return Image.fromarray(post(img, t))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print(SHORT, "frames", NF, "total", round(TOTAL, 2))
        for i, s in enumerate(SH):
            print(i, round(s[0], 2), round(scene_t(i)[1] - s[0], 2), s[1], s[2][:1])
    elif cmd == "still":
        os.makedirs(f"{SHORT}/stills", exist_ok=True)
        for a in sys.argv[2:]:
            frame(int(float(a) * FPS)).save(f"{SHORT}/stills/{float(a):05.1f}.jpg", quality=86)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
        p.stdin.close()
        p.wait()
