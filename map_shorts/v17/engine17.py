"""v17 map Short engine, rebuilt after the GeoGlobeTales visual audit (map_shorts/analysis/visual_gap.md).

Calm continuous camera, small subtitles, neon lines/regions with bloom, vector icons drawn in code, unit dots,
teal sea grade + relief, two full-screen 2D inserts. No emoji, no shake/whip.
python3 engine17.py still <frame> | info | video <f0> <f1> out.mp4
"""
import json
import math
import subprocess
import sys

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from script17 import LINES

W, H, FPS = 1080, 1920, 30
LON0, LON1, LAT0, LAT1 = -25, 65, 8, 70
POP = "assets/Poppins-Bold.ttf"
POPX = "assets/Poppins-ExtraBold.ttf"

WHT = (255, 255, 255)
CREAM = (255, 246, 228)
CYAN = (60, 225, 255)
TEAL = (0, 200, 215)
RED = (255, 60, 60)
ORANGE = (243, 156, 18)
GREEN = (57, 255, 120)
YEL = (255, 214, 60)


def my(lat):
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


YTOP = my(LAT1)

# ---------------------------------------------------------------- timing
TM = json.load(open("timing.json"))
D, TW = TM["D"], TM["T"]
LEAD = 0.35
starts = [LEAD + s for s in TM["starts"]]
TOTAL = starts[-1] + D[-1] + 1.0
NF = int(TOTAL * FPS)


def clean(w):
    return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word=None):
    if word is None:
        return starts[i]
    ws = [clean(w) for w in LINES[i].split()]
    q = clean(word)
    for j, w in enumerate(ws):
        if w == q:
            return starts[i] + TW[i][j]
    for j, w in enumerate(ws):
        if q in w:
            return starts[i] + TW[i][j]
    raise KeyError(f"{word!r} not in line {i}")


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def back(x):
    """0 -> 1 with overshoot (elastic pop)."""
    x = min(1.0, max(0.0, x))
    c = 2.2
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def lerp(a, b, k):
    return a + (b - a) * k


# ---------------------------------------------------------------- geo
_SHP = shapefile.Reader("assets/ne50/ne_50m_admin_0_countries.shp")
_FIELDS = [f[0] for f in _SHP.fields[1:]]
COUNTRY = {}
for sr in _SHP.iterShapeRecords():
    rec = dict(zip(_FIELDS, sr.record))
    pts = sr.shape.points
    parts = list(sr.shape.parts) + [len(pts)]
    rings = []
    for a, b in zip(parts[:-1], parts[1:]):
        ring = np.array(pts[a:b])
        if ring[:, 0].max() < -10 or ring[:, 0].min() > 50 or ring[:, 1].max() < 0 or ring[:, 1].min() > 50:
            continue
        y = np.degrees(np.log(np.tan(np.pi / 4 + np.radians(np.clip(ring[:, 1], -85, 85)) / 2)))
        rings.append(np.stack([ring[:, 0], y], 1))
    if rings:
        COUNTRY[rec["ADMIN"]] = rings

# ---------------------------------------------------------------- camera / map
LEVELS = {"hi": (-15, 62, 240, "tex_hi.npy"), "mid": (-25, 70, 120, "tex_mid.npy"), "lo": (-25, 70, 30, "tex_lo.npy")}
_TEX = {}
SHADE_CFG = {"mid": ("shade_mid.npy", 4.0, 36.0, 120), "hi": ("shade_hi.npy", 4.0, 36.0, 240)}
_SH = {}
SH_PAD = 1600
K_RELIEF = 1.6
FLAT = math.sin(math.radians(42))


def tex(level):
    if level not in _TEX:
        _TEX[level] = np.load(LEVELS[level][3], mmap_mode="r")
    return _TEX[level]


def shade_map(level):
    if level not in _SH:
        _SH[level] = np.pad(np.load(SHADE_CFG[level][0]), SH_PAD, constant_values=int((FLAT + 1) * 127.5))
    return _SH[level]


def grade(arr):
    """teal sea, livelier land (the competitor's look)."""
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    w = np.clip((b - r - 20) / 45, 0, 1)[..., None]
    lum = arr.mean(2, keepdims=True)
    land = lum + (arr - lum) * 1.02
    land = land * np.array([1.0, 1.0, 0.97], np.float32)
    l2 = lum[..., 0]
    sea = np.stack([l2 * 0.30 + 10, l2 * 0.95 + 42, l2 * 1.05 + 52], -1)
    return np.clip(land * (1 - w) + sea * w, 0, 255)


class Cam:
    def __init__(self, lon, lat, span):
        self.span = span
        self.ppd = W / span
        hw, hh = span / 2, H / 2 / self.ppd
        self.lon = min(LON1 - hw, max(LON0 + hw, lon))
        self.Y = min(YTOP - hh, max(my(LAT0) + hh, my(lat)))

    def xy(self, lon, lat):
        return ((lon - self.lon) * self.ppd + W / 2, (self.Y - my(lat)) * self.ppd + H / 2)

    def xyY(self, arr):
        return np.stack([(arr[:, 0] - self.lon) * self.ppd + W / 2, (self.Y - arr[:, 1]) * self.ppd + H / 2], 1)

    def render(self):
        hw, hh = self.span / 2, H / 2 / self.ppd
        level = "lo" if self.span > 34 else "mid"
        if self.span <= 14 and self.lon - hw > -15 and self.lon + hw < 50 \
                and self.Y + hh < my(62) and self.Y - hh > my(22):
            level = "hi"
        lon0, lat1, ppd, _ = LEVELS[level]
        T = tex(level)
        top = my(lat1)
        bx0, by0 = (self.lon - hw - lon0) * ppd, (top - (self.Y + hh)) * ppd
        bx1, by1 = (self.lon + hw - lon0) * ppd, (top - (self.Y - hh)) * ppd
        ix0, iy0 = max(0, int(bx0) - 1), max(0, int(by0) - 1)
        ix1, iy1 = min(T.shape[1], int(bx1) + 2), min(T.shape[0], int(by1) + 2)
        crop = Image.fromarray(np.ascontiguousarray(T[iy0:iy1, ix0:ix1]))
        out = crop.resize((W, H), Image.BICUBIC, box=(bx0 - ix0, by0 - iy0, bx1 - ix0, by1 - iy0))
        arr = np.asarray(out).astype(np.float32)
        if level in SHADE_CFG:
            SH = shade_map(level)
            _, slon0, stop, sppd = SHADE_CFG[level]
            t0 = my(stop)
            sx0, sx1 = (self.lon - hw - slon0) * sppd + SH_PAD, (self.lon + hw - slon0) * sppd + SH_PAD
            sy0, sy1 = (t0 - (self.Y + hh)) * sppd + SH_PAD, (t0 - (self.Y - hh)) * sppd + SH_PAD
            if sx0 >= 0 and sy0 >= 0 and sx1 <= SH.shape[1] and sy1 <= SH.shape[0]:
                piece = Image.fromarray(SH).resize((W, H), Image.BILINEAR, box=(sx0, sy0, sx1, sy1))
                arr = arr * (1 + K_RELIEF * ((np.asarray(piece).astype(np.float32) / 127.5 - 1) - FLAT))[..., None]
        return Image.fromarray(grade(arr).astype(np.uint8)).convert("RGBA")


# ---------------------------------------------------------------- drawing kit
_FONTS = {}


def font(path, size):
    key = (path, int(size))
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(path, max(1, int(size)))
    return _FONTS[key]


def bloom(img, painter, radius=18, strength=2):
    """painter(draw, scale) draws at the given scale; result is blurred and added twice for a neon glow."""
    g = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
    painter(ImageDraw.Draw(g), 0.5)
    g = g.filter(ImageFilter.GaussianBlur(radius / 2)).resize((W, H), Image.BILINEAR)
    for _ in range(strength):
        img.alpha_composite(g)


def partial(pts, prog):
    if prog >= 1:
        return list(pts)
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    L = sum(seg) * max(0.0, prog)
    out, acc = [pts[0]], 0.0
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if acc + s >= L:
            k = (L - acc) / max(s, 1e-6)
            out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
            return out
        out.append(b)
        acc += s
    return out


def neon_line(img, pts, color, prog, width=14, alpha=1.0, flow=None):
    p = partial(pts, prog)
    if len(p) < 2 or alpha <= 0:
        return
    a = int(255 * alpha)
    bloom(img, lambda d, s: d.line([(x * s, y * s) for x, y in p], fill=color + (int(200 * alpha),),
                                   width=max(2, int(width * 2.2 * s)), joint="curve"), 22, 2)
    d = ImageDraw.Draw(img)
    d.line(p, fill=color + (a,), width=width, joint="curve")
    d.line(p, fill=(255, 255, 255, int(a * 0.85)), width=max(2, width // 3), joint="curve")
    if flow is not None:  # bright pulses travelling along the line (water flow)
        seg = [math.hypot(b[0] - a_[0], b[1] - a_[1]) for a_, b in zip(p, p[1:])]
        L = sum(seg)
        for k in range(int(L / 70)):
            pos = (k * 70 + flow * 160) % L
            acc = 0.0
            for (u, v), s in zip(zip(p, p[1:]), seg):
                if acc + s >= pos:
                    q = (pos - acc) / max(s, 1e-6)
                    x, y = u[0] + (v[0] - u[0]) * q, u[1] + (v[1] - u[1]) * q
                    d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 255, int(230 * alpha)))
                    break
                acc += s


def region(img, cam, names, color, alpha, edge=WHT, glow=True):
    if alpha <= 0.01:
        return
    m = Image.new("L", (W // 4, H // 4), 0)
    dm = ImageDraw.Draw(m)
    edges = []
    for n in names:
        for r in COUNTRY.get(n, []):
            p = cam.xyY(r)
            if p[:, 0].max() < -50 or p[:, 0].min() > W + 50 or p[:, 1].max() < -50 or p[:, 1].min() > H + 50:
                continue
            dm.polygon([tuple(q / 4) for q in p], fill=255)
            edges.append([tuple(q) for q in p])
    m = m.resize((W, H), Image.BILINEAR).point(lambda v: int(v * min(1, alpha)))
    layer = Image.new("RGBA", (W, H), color + (0,))
    layer.putalpha(m)
    img.alpha_composite(layer)
    if glow:
        bloom(img, lambda d, s: [d.line([(x * s, y * s) for x, y in e], fill=color + (int(230 * min(1, alpha * 2)),),
                                         width=max(2, int(16 * s))) for e in edges], 20, 1)
    d = ImageDraw.Draw(img)
    for e in edges:
        d.line(e, fill=edge + (int(255 * min(1, alpha * 3)),), width=4, joint="curve")


def ring(img, x, y, color, lt, mark="!"):
    """pulsing shockwave rings with a warning marker."""
    if lt < 0:
        return
    k = back(lt / 0.35)
    for j in range(3):
        ph = ((lt * 0.9 + j / 3) % 1.0)
        r = 60 + ph * 260
        a = int(200 * (1 - ph) * min(1, lt / 0.3))
        bloom(img, lambda d, s, r=r, a=a: d.ellipse(((x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s),
                                                    outline=color + (a,), width=max(2, int(18 * s))), 16, 1)
    rr = (62 if mark else 16) * k
    d = ImageDraw.Draw(img)
    d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=color + (235,), outline=WHT + (255,), width=5)
    if mark and rr > 20:
        d.text((x, y + 2), mark, font=font(POPX, rr * 1.3), fill=WHT, anchor="mm")


def shadow_text(img, xy, txt, f, fill, anchor="mm", sh=150):
    lay = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
    fs = font(f.path, f.size / 2)
    ImageDraw.Draw(lay).text((xy[0] / 2, xy[1] / 2 + 3), txt, font=fs, fill=(0, 0, 0, sh), anchor=anchor)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(5)).resize((W, H), Image.BILINEAR))
    ImageDraw.Draw(img).text(xy, txt, font=f, fill=fill, anchor=anchor)


def big_text(img, txt, t, t0, y=330, size=150, color=CREAM, sub=None, t1=None):
    if t < t0 or (t1 is not None and t > t1):
        return
    k = back((t - t0) / 0.35)
    f = font(POPX, max(8, size * (0.6 + 0.4 * k)))
    while f.getlength(txt) > W - 90 and f.size > 20:
        f = font(POPX, f.size * 0.92)
    shadow_text(img, (W / 2, y), txt, f, color + (int(255 * min(1, k)),))
    if sub:
        shadow_text(img, (W / 2, y + size * 0.62), sub, font(POP, size * 0.30), WHT + (int(255 * min(1, k)),))


def label(img, x, y, txt, t, t0, side=-1, size=44):
    if t < t0:
        return
    k = back((t - t0) / 0.3)
    d = ImageDraw.Draw(img)
    r = 9 * k
    d.ellipse((x - r, y - r, x + r, y + r), fill=WHT, outline=(0, 0, 0, 120), width=2)
    f = font(POPX, size * (0.7 + 0.3 * k))
    hw = f.getlength(txt) / 2
    shadow_text(img, (min(W - 40 - hw, max(40 + hw, x)), y + side * 48), txt, f, WHT + (int(255 * min(1, k)),))


# vector icons (white flat style with soft shadow), drawn around (x, y) with height h
def icon_person(d, x, y, h, col=WHT):
    hr = h * 0.13
    d.ellipse((x - hr, y - h / 2, x + hr, y - h / 2 + 2 * hr), fill=col)
    d.rounded_rectangle((x - h * 0.17, y - h / 2 + 2.25 * hr, x + h * 0.17, y + h * 0.12), radius=h * 0.08, fill=col)
    d.rectangle((x - h * 0.15, y + h * 0.08, x - h * 0.03, y + h / 2), fill=col)
    d.rectangle((x + h * 0.03, y + h * 0.08, x + h * 0.15, y + h / 2), fill=col)


def icon_drop(d, x, y, h, col=CYAN):
    r = h * 0.32
    d.polygon([(x, y - h / 2), (x - r * 0.95, y + h / 2 - r * 1.25), (x + r * 0.95, y + h / 2 - r * 1.25)], fill=col)
    d.ellipse((x - r, y + h / 2 - 2 * r, x + r, y + h / 2), fill=col)
    d.ellipse((x - r * 0.45, y + h / 2 - r * 1.5, x - r * 0.1, y + h / 2 - r * 1.0), fill=(255, 255, 255, 200))


def icon_derrick(d, x, y, h, col=WHT):
    w = h * 0.36
    top, base = y - h / 2, y + h / 2
    d.line([(x - w, base), (x, top), (x + w, base)], fill=col, width=max(3, int(h * 0.06)))
    for k in (0.35, 0.6, 0.82):
        yy = top + (base - top) * k
        ww = w * k
        d.line([(x - ww, yy), (x + ww, yy)], fill=col, width=max(2, int(h * 0.04)))
    d.rectangle((x - w * 1.2, base - h * 0.04, x + w * 1.2, base + h * 0.04), fill=col)


def icon_nosign(d, x, y, r, col=RED):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=int(r * 0.2))
    a = r * 0.7
    d.line([(x - a, y - a), (x + a, y + a)], fill=col, width=int(r * 0.2))


def icon_car(d, x, y, h, col=WHT):
    w = h * 2.2
    d.rounded_rectangle((x - w / 2, y - h * 0.15, x + w / 2, y + h * 0.3), radius=h * 0.12, fill=col)
    d.rounded_rectangle((x - w * 0.28, y - h * 0.5, x + w * 0.22, y - h * 0.05), radius=h * 0.12, fill=col)
    for cx in (x - w * 0.3, x + w * 0.3):
        d.ellipse((cx - h * 0.2, y + h * 0.15, cx + h * 0.2, y + h * 0.55), fill=(40, 40, 40))


def icon_palm(d, x, y, h, col=(60, 180, 90)):
    d.line([(x, y + h / 2), (x + h * 0.06, y - h * 0.3)], fill=(140, 100, 60), width=max(3, int(h * 0.08)))
    for ang in (-150, -110, -70, -30, 10):
        a = math.radians(ang)
        d.line([(x + h * 0.06, y - h * 0.3), (x + h * 0.06 + math.cos(a) * h * 0.42, y - h * 0.3 + math.sin(a) * h * 0.25 + h * 0.12)],
               fill=col, width=max(3, int(h * 0.09)))


def icon(img, kind, x, y, h, t, t0, col=None):
    if t < t0:
        return
    k = back((t - t0) / 0.32)
    hh = h * k
    if hh < 3:
        return
    fn = {"person": icon_person, "drop": icon_drop, "derrick": icon_derrick, "car": icon_car, "palm": icon_palm}[kind]
    sh = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
    fn(ImageDraw.Draw(sh), x / 2 + 3, y / 2 + 5, hh / 2, (0, 0, 0, 140))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    fn(d, x, y, hh, col) if col else fn(d, x, y, hh)


def dots(img, cam, pts, t, t0, dur, color, r=8, alpha=1.0):
    n = len(pts)
    shown = []
    for i, (lo, la) in enumerate(pts):
        ti = t0 + dur * i / n
        if t >= ti:
            x, y = cam.xy(lo, la)
            if -20 < x < W + 20 and -20 < y < H + 20:
                shown.append((x, y, back((t - ti) / 0.25)))
    if not shown:
        return
    bloom(img, lambda d, s: [d.ellipse(((x - r * 2 * k) * s, (y - r * 2 * k) * s, (x + r * 2 * k) * s, (y + r * 2 * k) * s),
                                       fill=color + (int(200 * alpha),)) for x, y, k in shown], 10, 1)
    d = ImageDraw.Draw(img)
    for x, y, k in shown:
        rr = r * k
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=(255, 255, 255, int(255 * alpha)))


# ---------------------------------------------------------------- inserts (non-map 2D scenes)
GRAIN = np.random.default_rng(9).normal(0, 3.5, (H + 256, W + 256, 1)).astype(np.float32)
POROS = np.random.default_rng(4).uniform(0, 1, (420, 3))
RAIN = np.random.default_rng(6).uniform(0, 1, (160, 3))


def insert_aquifer(t, t0, green_t):
    lt = t - t0
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    gk = ease((t - green_t) / 0.8)
    for y in range(0, 640, 8):  # sky
        q = y / 640
        base = np.array([250, 226, 180]) * (1 - q) + np.array([255, 205, 140]) * q
        grn = np.array([190, 225, 235]) * (1 - q) + np.array([200, 235, 210]) * q
        c = tuple(int(v) for v in base * (1 - gk) + grn * gk)
        d.rectangle((0, y, W, y + 8), fill=c)
    off = int(500 * (1 - ease(lt / 0.7)))
    layers = [(640, 820, (232, 190, 128), "SAND"), (820, 960, (172, 118, 78), "CLAY"),
              (960, 1380, (205, 160, 108), "SANDSTONE"), (1380, 1920, (112, 82, 62), "BEDROCK")]
    for y0, y1, col, name in layers:
        d.rectangle((0, y0 + off, W, y1 + off), fill=col)
        d.line([(0, y0 + off), (W, y0 + off)], fill=tuple(max(0, c - 30) for c in col), width=4)
        d.text((40, y0 + off + 22), name, font=font(POP, 34), fill=(255, 255, 255, 200))
    # water in the sandstone: glowing pores, then a blue fill
    wk = ease((lt - 0.9) / 1.6)
    if wk > 0:
        ov = Image.new("RGBA", (W, H), (40, 150, 255, 0))
        dv = ImageDraw.Draw(ov)
        dv.rectangle((0, 960 + off, W, 1380 + off), fill=(40, 150, 255, int(120 * wk)))
        img.alpha_composite(ov)
        bloom(img, lambda dd, s: [dd.ellipse(((px * W - 9) * s, (980 + py * 380 + off - 9) * s, (px * W + 9) * s,
                                              (980 + py * 380 + off + 9) * s), fill=(90, 210, 255, 220))
                                  for px, py, pz in POROS[: int(len(POROS) * wk)]], 8, 1)
        for px, py, pz in POROS[: int(len(POROS) * wk)]:
            r = 3 + pz * 4
            d.ellipse((px * W - r, 980 + py * 380 + off - r, px * W + r, 980 + py * 380 + off + r), fill=(200, 240, 255))
        shadow_text(img, (W / 2, 1170 + off), "WATER-BEARING SANDSTONE", font(POPX, 50), WHT + (int(255 * wk),))
    # green Sahara: grass, palms, rain seeping down
    if gk > 0:
        d.rectangle((0, 628 + off, W, 652 + off), fill=(70, 160, 70, int(255 * gk)))
        for k, px in enumerate((150, 420, 760, 960)):
            icon(img, "palm", px, 560 + off, 150, t, green_t + 0.1 * k)
        dr = ImageDraw.Draw(img)
        for rx, ry, rs in RAIN:
            y = (ry * 1300 + (t - green_t) * (500 + rs * 300)) % 1300 + 40
            if y < 640 or y > 960:
                a = 120 if y > 640 else 200
                dr.line([(rx * W, y), (rx * W - 6, y + 26)], fill=(120, 190, 255, int(a * gk)), width=4)
    tk = ease((lt - 0.2) / 0.5)
    if tk > 0:
        shadow_text(img, (W / 2, 300), "NUBIAN SANDSTONE", font(POPX, 84), (90, 70, 50, int(255 * tk)), sh=60)
        shadow_text(img, (W / 2, 395), "AQUIFER", font(POPX, 84), (40, 130, 220, int(255 * tk)), sh=60)
    # depth marker
    dk = ease((lt - 0.5) / 0.6)
    if dk > 0:
        x = W - 120
        dd = ImageDraw.Draw(img)
        y1 = 640 + off + (1000 - 640) * dk
        dd.line([(x, 640 + off), (x, y1)], fill=WHT, width=5)
        dd.line([(x - 22, 640 + off), (x + 22, 640 + off)], fill=WHT, width=5)
        dd.line([(x - 22, y1), (x + 22, y1)], fill=WHT, width=5)
        shadow_text(img, (x - 20, (640 + y1) / 2 + off * 0), "500 m+", font(POPX, 46), YEL + (int(255 * dk),), anchor="rm")
    return img


def insert_pipe(t, t0, cars_t):
    lt = t - t0
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    for y in range(0, H, 8):
        q = y / H
        d.rectangle((0, y, W, y + 8), fill=(int(242 - 30 * q), int(214 - 40 * q), int(170 - 50 * q)))
    ground = 1180
    d.rectangle((0, ground, W, H), fill=(205, 160, 105))
    m = 150  # px per metre
    k = back(lt / 0.5)
    cx, cy, R = 560, ground - 2 * m, 2 * m * k
    if R > 4:
        sh = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse(((cx - R + 10) / 2, (cy - R + 18) / 2, (cx + R + 10) / 2, (cy + R + 18) / 2), fill=(0, 0, 0, 120))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)).resize((W, H), Image.BILINEAR))
        d = ImageDraw.Draw(img)
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(150, 150, 150))
        r2 = R * 0.86
        d.ellipse((cx - r2, cy - r2, cx + r2, cy + r2), fill=(40, 70, 95))
        wk = ease((lt - 0.4) / 0.8)
        if wk > 0:
            r3 = r2 * 0.98
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(ov).ellipse((cx - r3, cy - r3, cx + r3, cy + r3), fill=(40, 160, 255, int(210 * wk)))
            img.alpha_composite(ov)
    pk = ease((lt - 0.35) / 0.4)
    if pk > 0:
        icon(img, "person", cx + 2 * m + 100, ground - 0.9 * m, 1.8 * m, t, t0 + 0.35)
        dd = ImageDraw.Draw(img)
        x = cx - 2 * m - 70
        dd.line([(x, ground - 4 * m), (x, ground)], fill=WHT, width=5)
        for yy in (ground - 4 * m, ground):
            dd.line([(x - 20, yy), (x + 20, yy)], fill=WHT, width=5)
        shadow_text(img, (x - 18, ground - 2 * m), "4 m", font(POPX, 64), YEL + (int(255 * pk),), anchor="rm")
        shadow_text(img, (cx + 2 * m + 100, ground - 1.8 * m - 50), "1.8 m", font(POP, 40), WHT + (int(255 * pk),))
    if t >= cars_t:  # 50 cars as units
        for i in range(50):
            ti = cars_t + 1.1 * i / 50
            if t >= ti:
                col, row = i % 10, i // 10
                icon(img, "car", 90 + col * 100, ground + 120 + row * 90, 38, t, ti)
        big_text(img, "≈ 50 CARS", t, cars_t + 0.2, 300, 120, CREAM, "PER PIPE SECTION")
    return img


# ---------------------------------------------------------------- story geometry
CITIES = [(13.19, 32.89), (12.73, 32.76), (14.26, 32.65), (15.09, 32.38), (16.59, 31.2), (20.07, 32.12),
          (21.75, 32.76), (23.96, 32.08)]
FIELDS = [((21.1, 25.7), 0.9, 60), ((22.0, 27.4), 0.7, 40), ((23.3, 24.25), 0.6, 30), ((13.9, 27.5), 1.1, 80)]
_rng = np.random.default_rng(12)
WELLS = []
for (lo, la), r, n in FIELDS:
    for _ in range(n):
        a, rr = _rng.uniform(0, 2 * math.pi), r * math.sqrt(_rng.uniform(0, 1))
        WELLS.append((lo + math.cos(a) * rr, la + math.sin(a) * rr * 0.8))
_rng.shuffle(WELLS)
PIPES = [
    [(21.1, 25.7), (21.3, 27.0), (20.9, 28.6), (20.4, 29.9), (20.22, 30.76)],
    [(22.0, 27.4), (21.2, 28.2)],
    [(20.22, 30.76), (20.1, 31.5), (20.07, 32.12)],
    [(20.22, 30.76), (19.2, 30.45), (18.0, 30.6), (16.59, 31.2)],
    [(13.9, 27.5), (13.7, 29.0), (13.4, 30.6), (13.25, 31.9), (13.19, 32.89)],
    [(16.59, 31.2), (15.5, 31.9), (15.09, 32.38), (14.26, 32.65), (13.19, 32.89)],
]
FIND = (21.3, 26.2)


def sc(lines, cam, fx, **kw):
    return dict(lines=lines, cam=cam, fx=fx, **kw)


def S_list():
    S = []
    S.append(sc((0, 0), (17.0, 27.5, 26, 17.0, 28.3, 19), [
        ("region", ["Libya"], TEAL, 0.0, 0.28),
        ("pipes", WT(0, "giant"), 1.4, 1.0),
        ("big", "UNDER THE DESERT?", WT(0, "under"), 330, 110),
    ]))
    S.append(sc((1, 1), (17.0, 28.3, 19, 17.0, 27.6, 16), [
        ("region", ["Libya"], ORANGE, WT(1, "desert") - 0.3, 0.42),
        ("count", 0, 90, "≈{}%", WT(1, "ninety"), 0.9, 330, "DESERT"),
        ("nodrop", 17.0, 26.0, WT(1, "rivers")),
    ]))
    S.append(sc((2, 2), (17.0, 27.6, 16, 17.2, 31.0, 9.5), [
        ("region", ["Libya"], ORANGE, 0, 0.25),
        ("people", WT(2, "Almost"), 1.6),
        ("ring", 17.6, 31.6, RED, WT(2, "running")),
    ]))
    S.append(sc((3, 3), (17.2, 31.0, 9.5, 21.3, 26.6, 8), [
        ("big", "1950s", WT(3, "1950s"), 330, 150),
        ("derrick", FIND[0], FIND[1], WT(3, "oil")),
        ("label", FIND[0], FIND[1] + 0.9, "SEARCHING FOR OIL", WT(3, "searching") + 0.4, -1),
        ("ring", FIND[0], FIND[1], CYAN, WT(3, "Water") - 0.1),
        ("big", "WATER", WT(3, "Water"), 560, 150, CYAN),
    ]))
    S.append(sc((4, 4), None, [], insert="aquifer", green=WT(4, "green")))
    S.append(sc((5, 5), (19.0, 28.0, 16, 18.0, 28.6, 14), [
        ("region", ["Libya"], TEAL, 0, 0.22),
        ("big", "1984", WT(5, "1984"), 300, 170),
        ("big2", "GREAT MAN-MADE RIVER", WT(5, "Great"), 450, 64),
    ]))
    S.append(sc((6, 6), (18.0, 28.6, 14, 20.2, 26.8, 9.5), [
        ("wells", WT(6, "More"), 2.6),
        ("count", 0, 1300, "≈{:,}", WT(6, "thirteen"), 1.6, 330, "WELLS"),
        ("label", 21.1, 25.0, "500 m+ DEEP", WT(6, "five"), 1),
    ]))
    S.append(sc((7, 7), (20.2, 26.8, 9.5, 17.0, 29.6, 15), [
        ("wells", 0, 0.01),
        ("pipes", WT(7, "pipes"), 3.2, 1.0),
        ("count", 0, 2800, "{:,}+ KM", WT(7, "two"), 1.4, 330, "OF PIPES"),
    ]))
    S.append(sc((8, 8), None, [], insert="pipe", cars=WT(8, "fifty") - 0.2))
    S.append(sc((9, 9), (17.0, 29.6, 15, 17.0, 31.0, 11), [
        ("wells", 0, 0.01),
        ("pipes", 0, 0.01, 1.0),
        ("drops", WT(9, "supplies")),
        ("count", 0, 70, "≈{}%", WT(9, "seventy"), 1.0, 330, "OF LIBYA'S FRESH WATER"),
    ]))
    S.append(sc((10, 10), (17.0, 31.0, 11, 19.5, 27.2, 13), [
        ("pipes", 0, 0.01, 1.0),
        ("wells_red", WT(10, "fossil")),
        ("ring", FIND[0], FIND[1], RED, WT(10, "fossil")),
        ("ring", 13.9, 27.5, RED, WT(10, "fossil") + 0.25),
        ("big", "FOSSIL WATER", WT(10, "fossil"), 330, 120, CREAM, "IT BARELY REFILLS"),
    ]))
    S.append(sc((11, 11), (19.5, 27.2, 13, 17.0, 27.5, 26), [
        ("region", ["Libya"], TEAL, WT(11, "fill"), 0.28),
        ("pipes_fade", WT(11, "one"), WT(11, "dry") + 0.4),
        ("big", "COULD RUN DRY", WT(11, "dry") - 0.2, 330, 120),
    ]))
    return S


S = S_list()
SCENE_T = [max(0, s.get("t0", starts[s["lines"][0]] - (LEAD if i == 0 else 0.11))) for i, s in enumerate(S)] + [TOTAL]


def scene_at(t):
    for i in range(len(S)):
        if SCENE_T[i] <= t < SCENE_T[i + 1]:
            return i
    return len(S) - 1


def persp_coeffs(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, np.float64), np.array(B, np.float64))


def tilt(img, a):
    if a < 0.01:
        return img
    src = [(0, 0), (W, 0), (W - a * W, H), (a * W, H)]
    return img.transform((W, H), Image.PERSPECTIVE, persp_coeffs([(0, 0), (W, 0), (W, H), (0, H)], src), Image.BICUBIC)


def rotate_zoom(img, deg, z):
    a = math.radians(deg)
    c, s_ = math.cos(a) / z, math.sin(a) / z
    cx, cy = W / 2, H / 2
    return img.transform((W, H), Image.AFFINE, (c, s_, cx - c * cx - s_ * cy, -s_, c, cy + s_ * cx - c * cy), Image.BICUBIC)


VIGN = None


def vignette():
    global VIGN
    if VIGN is None:
        yy, xx = np.mgrid[0:H // 4, 0:W // 4]
        dd = np.sqrt(((xx - W / 8) / (W / 8)) ** 2 + ((yy - H / 8) / (H / 8)) ** 2)
        v = np.clip(1.0 - 0.32 * np.clip(dd - 0.5, 0, None) ** 1.4, 0.6, 1)
        VIGN = np.asarray(Image.fromarray((v * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR))[..., None] / 255.0
    return VIGN


def caption(img, t):
    """small white sentence-case subtitles with a soft shadow (competitor style)."""
    for i in range(len(LINES)):
        if starts[i] - 0.05 <= t < starts[i] + D[i] + 0.12:
            words = LINES[i].split()
            cur = 0
            for j, o in enumerate(TW[i]):
                if t >= starts[i] + o - 0.05:
                    cur = j
            c0 = cur // 4 * 4
            txt = " ".join(words[c0:c0 + 4])
            f = font(POP, 52)
            while f.getlength(txt) > W - 120:
                f = font(POP, f.size - 2)
            shadow_text(img, (W / 2, 1500), txt, f, WHT + (255,), sh=200)
            return


def draw_fx(img, cam, s, t):
    for f in s["fx"]:
        k = f[0]
        if k == "region" and t >= f[3]:
            region(img, cam, f[1], f[2], f[4] * ease((t - f[3]) / 0.4))
    for f in s["fx"]:
        k = f[0]
        if k in ("pipes", "pipes_fade"):
            if k == "pipes":
                t0, dur, al = f[1], f[2], f[3]
            else:
                t0, dur = 0, 0.01
                al = 1 - 0.8 * ease((t - f[1]) / (f[2] - f[1]))
            if t >= t0:
                for j, p in enumerate(PIPES):
                    pj = (t - t0 - dur * j / len(PIPES) * 0.7) / (dur * 0.45)
                    neon_line(img, [cam.xy(*q) for q in p], CYAN, ease(pj), 12, al, flow=t)
        elif k in ("wells", "wells_red"):
            if k == "wells":
                dots(img, cam, WELLS, t, f[1], f[2], CYAN, 5)
            else:
                rk = ease((t - f[1]) / 0.5)
                col = tuple(int(lerp(a, b, rk)) for a, b in zip(CYAN, RED))
                dots(img, cam, WELLS, t, 0, 0.01, col, 5, 1 - 0.4 * rk * (0.5 + 0.5 * math.sin(t * 8)))
        elif k == "people" and t >= f[1]:
            n = 0
            for ci, (lo, la) in enumerate(CITIES):
                x, y = cam.xy(lo, la)
                for j in range(3):
                    ti = f[1] + f[2] * n / (len(CITIES) * 3)
                    icon(img, "person", x + (j - 1) * 40, y + 36 + (j % 2) * 20, 64, t, ti)
                    n += 1
        elif k == "drops" and t >= f[1]:
            for ci, (lo, la) in enumerate(CITIES):
                x, y = cam.xy(lo, la)
                icon(img, "drop", x, y - 40, 60, t, f[1] + 0.12 * ci)
        elif k == "nodrop" and t >= f[3]:
            x, y = cam.xy(f[1], f[2])
            kk = back((t - f[3]) / 0.35)
            icon(img, "drop", x, y, 120, t, f[3])
            if kk > 0.1:
                icon_nosign(ImageDraw.Draw(img), x, y, 95 * kk)
        elif k == "derrick" and t >= f[3]:
            x, y = cam.xy(f[1], f[2])
            icon(img, "derrick", x, y - 60, 130, t, f[3])
        elif k == "ring":
            x, y = cam.xy(f[1], f[2])
            ring(img, x, y, f[3], t - f[4], "!" if f[3] == RED else "")
        elif k == "label":
            x, y = cam.xy(f[1], f[2])
            label(img, x, y, f[3], t, f[4], f[5])


def draw_text(img, s, t):
    for f in s["fx"]:
        k = f[0]
        if k == "big":
            big_text(img, f[1], t, f[2], f[3], f[4], f[5] if len(f) > 5 else CREAM, f[6] if len(f) > 6 else None)
        elif k == "big2" and t >= f[2]:
            kk = back((t - f[2]) / 0.35)
            shadow_text(img, (W / 2, f[3]), f[1], font(POPX, f[4] * (0.7 + 0.3 * kk)), YEL + (int(255 * min(1, kk)),))
        elif k == "count" and t >= f[4]:
            v = f[1] + (f[2] - f[1]) * ease((t - f[4]) / f[5])
            big_text(img, f[3].format(int(round(v))), t, f[4], f[6], 150, CREAM, f[7])


def frame(fi):
    t = fi / FPS
    si = scene_at(t)
    s = S[si]
    t0, t1 = SCENE_T[si], SCENE_T[si + 1]
    if s.get("insert") == "aquifer":
        img = insert_aquifer(t, t0, s["green"])
    elif s.get("insert") == "pipe":
        img = insert_pipe(t, t0, s["cars"])
    else:
        k = ease((t - t0) / max(0.1, t1 - t0))
        c = s["cam"]
        span = lerp(c[2], c[5], k)
        cam = Cam(lerp(c[0], c[3], k), lerp(c[1], c[4], k), span)
        img = cam.render()
        draw_fx(img, cam, s, t)
        img = tilt(img, 0.12 * min(1.0, max(0.0, (span - 8) / 10)))
        img = rotate_zoom(img, 1.6 * math.sin(t * 0.33), 1.06)
        draw_text(img, s, t)
    caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32) * vignette()
    gy, gx = (fi * 37) % 256, (fi * 91) % 256
    rgb += GRAIN[gy:gy + H, gx:gx + W]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


CUTS = SCENE_T[1:-1]

if __name__ == "__main__":
    if sys.argv[1] == "still":
        fi = int(sys.argv[2])
        frame(fi).save(f"still_{fi:05d}.png")
    elif sys.argv[1] == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for i, s in enumerate(S):
            print(i, s["lines"], round(SCENE_T[i], 2), int(SCENE_T[i] * FPS))
    elif sys.argv[1] == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast",
                              "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 30 == 0:
                print(fi, flush=True)
        p.stdin.close()
        p.wait()
