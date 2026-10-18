"""Map Shorts engine v63: strict remake of the MapTrail reference style (5wEVWjvaX2k), vertical 1080x1920 @30 fps.
One virtual camera (lon, lat, span) flies over a stack of Esri images and picks the sharpest one that covers the view,
so zooms from the region down to a strait are continuous. Overlays live on a global timeline, not inside shots.
Run in /home/claude/v62:  SHORT=turkey python3 engine63.py info | still t.. | video A B out.mp4"""
import json
import math
import os
import subprocess
import sys
from functools import lru_cache

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/turkey_2026_10_24")
from scripts import SHORTS  # noqa: E402
from sat63 import SP, size  # noqa: E402

W, H, FPS = 1080, 1920, 30
MB, MX, BANG, OSW = "assets/Montserrat-Black.ttf", "assets/Montserrat-ExtraBold.ttf", "assets/Bangers.ttf", "assets/Oswald-Regular.ttf"
WHT, BLK, YEL = (255, 255, 255), (0, 0, 0), (255, 214, 0)
CYAN, PURPLE, GOLD = (0, 229, 255), (123, 31, 162), (255, 215, 0)

SHORT = os.environ.get("SHORT", "turkey")
LINES = SHORTS[SHORT]["lines"]
TM = json.load(open(f"{SHORT}/timing.json"))
LEAD = 0.05                         # reference: voice starts on frame 0
ST = [LEAD + s for s in TM["starts"]]
D, TW = TM["D"], TM["T"]
TOTAL = ST[-1] + D[-1] + 0.9
NF = int(TOTAL * FPS)

_FONTS = {}


def font(path, sz):
    k = (path, int(sz))
    if k not in _FONTS:
        _FONTS[k] = ImageFont.truetype(path, max(8, int(sz)))
    return _FONTS[k]


def clamp(x, a=0.0, b=1.0):
    return min(b, max(a, x))


def ease(x):                       # strong ease-in-out (cubic), as in the reference camera
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def back(x):                       # elastic pop with overshoot
    x = clamp(x)
    c = 1.9
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def clean(w):
    return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word, nth=0):
    ws = [clean(w) for w in LINES[i].split()]
    q = clean(word)
    hits = [j for j, w in enumerate(ws) if w == q] or [j for j, w in enumerate(ws) if q in w]
    if not hits:
        raise KeyError((i, word))
    return ST[i] + TW[i][hits[min(nth, len(hits) - 1)]]


# ------------------------------------------------------------------ geodata
def _shp(path, field):
    r = shapefile.Reader(path)
    fl = [f[0] for f in r.fields[1:]]
    out = {}
    for sr in r.iterShapeRecords():
        n = dict(zip(fl, sr.record))[field]
        pts = sr.shape.points
        parts = list(sr.shape.parts) + [len(pts)]
        out.setdefault(n, []).extend(np.array(pts[a:b]) for a, b in zip(parts[:-1], parts[1:]))
    return out


COUNTRY = _shp("assets/ne50/ne_50m_admin_0_countries.shp", "ADMIN")
SEA = _shp("assets/ne_marine/ne_10m_geography_marine_polys.shp", "name")
_TR10 = sorted(_shp("assets/ne10/ne_10m_admin_0_countries.shp", "ADMIN")["Turkey"], key=len)
COUNTRY["Anatolia10"] = [_TR10[-1]]                                                 # 10m parts for close-ups of Istanbul
COUNTRY["Thrace10"] = [_TR10[-2]]
DEM = np.load("assets/dem/tr_dem.npy").astype(np.float32)          # lon 25..46.5, lat 43.5..35, step 0.02
_gy, _gx = np.gradient(DEM)
SHADE = np.clip(0.75 + (-_gx - _gy) / 120.0, 0.35, 1.25).astype(np.float32)


def bbox(key):
    lon0, lat0, d = SP[key]
    w, h = size(key)
    dl = d * (w / h) / math.cos(math.radians(lat0))
    return lon0 - dl, lon0 + dl, lat0 - d, lat0 + d


@lru_cache(maxsize=10)
def sat(key):
    """Graded once at load (the grade is a per-pixel colour map, so it commutes with cropping)."""
    p = f"sat63g/{key}.jpg"
    if not os.path.exists(p):
        os.makedirs("sat63g", exist_ok=True)
        grade(Image.open(f"sat63/{key}.jpg").convert("RGB")).convert("RGB").save(p, quality=94)
    return Image.open(p).convert("RGB")


MAP_KEYS = sorted(SP, key=lambda k: -size(k)[1] / (2 * SP[k][2]))                # sharpest (px per degree) first


# ------------------------------------------------------------------ camera
CAM = []        # (t, lon, lat, span, cut)


def K(t, lon, lat, span, cut=False, lin=False):
    CAM.append((t, lon, lat, span, cut, lin))


def camera(t):
    ks = sorted(CAM, key=lambda k: k[0])
    if t <= ks[0][0]:
        return ks[0][1:4]
    for a, b in zip(ks, ks[1:]):
        if a[0] <= t < b[0]:
            if b[4]:
                return a[1:4]
            u = (t - a[0]) / max(1e-3, b[0] - a[0])
            u = u if b[5] else ease(u)
            span = math.exp(math.log(a[3]) + (math.log(b[3]) - math.log(a[3])) * u)
            return a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, span
    return ks[-1][1:4]


class View:
    def __init__(self, lon, lat, span, w=W, h=H):
        self.lon, self.lat, self.span, self.w, self.h = lon, lat, span, w, h
        self.ppd = h / (2 * span)
        self.kx = self.ppd * math.cos(math.radians(lat))
        self.hw = (w / 2) / self.kx

    def xy(self, lon, lat):
        return self.w / 2 + (lon - self.lon) * self.kx, self.h / 2 - (lat - self.lat) * self.ppd

    def pts(self, ring):
        return [(self.w / 2 + (lo - self.lon) * self.kx, self.h / 2 - (la - self.lat) * self.ppd) for lo, la in ring]

    def geo_bbox(self):
        return self.lon - self.hw, self.lon + self.hw, self.lat - self.span, self.lat + self.span


def crop(key, v):
    l0, l1, b0, b1 = bbox(key)
    w, h = size(key)
    a0, a1, c0, c1 = v.geo_bbox()
    box = ((a0 - l0) / (l1 - l0) * w, (b1 - c1) / (b1 - b0) * h, (a1 - l0) / (l1 - l0) * w, (b1 - c0) / (b1 - b0) * h)
    return sat(key).resize((v.w, v.h), Image.BILINEAR, box=box, reducing_gap=2.0)


def covers(key, v, margin=0.0):
    l0, l1, b0, b1 = bbox(key)
    a0, a1, c0, c1 = v.geo_bbox()
    return a0 >= l0 - margin and a1 <= l1 + margin and c0 >= b0 - margin and c1 <= b1 + margin


def render_map(v):
    """Sharpest covering image; crossfade from the coarser one while the fine image is just big enough."""
    ok = [k for k in MAP_KEYS if covers(k, v)]
    if not ok:                                             # nothing covers: take the image with the largest overlap
        def overlap(k):
            l0, l1, b0, b1 = bbox(k)
            a0, a1, c0, c1 = v.geo_bbox()
            return max(0, min(l1, a1) - max(l0, a0)) * max(0, min(b1, c1) - max(b0, c0))
        ok = [max(MAP_KEYS, key=overlap)]
    fine = ok[0]
    im = crop(fine, v)
    if len(ok) > 1:
        l0, l1, b0, b1 = bbox(fine)
        frac = (2 * v.span) / (b1 - b0)                    # share of the fine image used by the view
        wgt = clamp((frac - 0.7) / 0.3)
        if wgt > 0:
            im = Image.blend(im, crop(ok[1], v), wgt)
    return im.convert("RGBA")


YY, XX = np.mgrid[0:H, 0:W]
VIG = (256 * (1 - 0.28 * np.clip((((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2 - 0.55) / 1.45, 0, 1))).astype(np.uint16)[..., None]
del YY, XX
TEAL = np.array([19, 43, 51], np.float32)


def grade(im):
    """Reference look: deep teal-charcoal water, high-contrast land, soft edge vignette."""
    a = np.asarray(im).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    water = np.clip((b - r - 4) / 18, 0, 1) * np.clip((120 - lum) / 50, 0, 1)
    a = a * (1 - 0.55 * water[..., None]) + TEAL * 0.55 * water[..., None] * (0.6 + lum[..., None] / 160)
    a = (a - 118) * 1.12 + 118
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


# ------------------------------------------------------------------ text helpers
def text_layer(txt, f, col, stroke, shadow=True, a=1.0):
    bb = f.getbbox(txt, stroke_width=stroke)
    pad = 30
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    o = (pad - bb[0], pad - bb[1])
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((o[0] + 4, o[1] + 7), txt, font=f, fill=(0, 0, 0, int(170 * a)), stroke_width=stroke, stroke_fill=(0, 0, 0, int(170 * a)))
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(lay).text(o, txt, font=f, fill=col + (int(255 * a),), stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * a)))
    return lay


def put(img, lay, x, y, scale=1.0, angle=0.0):
    if scale <= 0.01:
        return
    if scale != 1.0:
        lay = lay.resize((max(1, int(lay.width * scale)), max(1, int(lay.height * scale))), Image.BICUBIC)
    if angle:
        lay = lay.rotate(angle, Image.BICUBIC, expand=True)
    img.alpha_composite(lay, (int(x - lay.width / 2), int(y - lay.height / 2)))


def fit(path, sz, txt, maxw):
    f = font(path, sz)
    while f.getlength(txt) > maxw and f.size > 16:
        f = font(path, f.size - 2)
    return f


# ------------------------------------------------------------------ overlays
OV = []         # dicts: kind, t0, t1, ...


def O(kind, t0, t1=1e9, **kw):
    kw.update(kind=kind, t0=t0, t1=t1)
    OV.append(kw)
    return kw


def fade(o, t, fin=0.3, fout=0.3):
    return clamp((t - o["t0"]) / fin) * clamp((o["t1"] - t) / fout)


def rings_xy(v, rings, scale=1.0):
    out = []
    for r in rings:
        p = v.pts(r)
        xs = [q[0] for q in p]
        ys = [q[1] for q in p]
        if len(p) < 3 or max(xs) < -300 or min(xs) > v.w + 300 or max(ys) < -300 or min(ys) > v.h + 300:
            continue
        out.append([(x * scale, y * scale) for x, y in p])
    return out


def fill_layer(v, rings, col, alpha, glow=None, border=WHT, bw=3, glow_w=16):
    """Semi-transparent fill + outer glow in glow colour + crisp white border (reference highlight style)."""
    lay = Image.new("RGBA", (v.w, v.h), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", (v.w // 4, v.h // 4), (0, 0, 0, 0))
        dg = ImageDraw.Draw(g)
        for r in rings_xy(v, rings, 0.25):
            dg.line(r + [r[0]], fill=glow + (230,), width=max(2, glow_w // 4), joint="curve")
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)).resize((v.w, v.h), Image.BILINEAR))
    f = Image.new("RGBA", (v.w // 2, v.h // 2), (0, 0, 0, 0))
    df = ImageDraw.Draw(f)
    for r in rings_xy(v, rings, 0.5):
        df.polygon(r, fill=col + (int(255 * alpha),))
    lay.alpha_composite(f.resize((v.w, v.h), Image.BILINEAR))
    d = ImageDraw.Draw(lay)
    for r in rings_xy(v, rings):
        d.line(r + [r[0]], fill=border + (255,), width=bw, joint="curve")
    return lay


def mask_full(v, rings):
    m = Image.new("L", (v.w, v.h), 0)
    d = ImageDraw.Draw(m)
    for r in rings_xy(v, rings):
        d.polygon(r, fill=255)
    return m


@lru_cache(maxsize=4)
def flag_tex(code, w, h):
    f = Image.new("RGBA", (w, h), (227, 10, 23, 255))
    if code == "TR":
        d = ImageDraw.Draw(f)
        R = h * 0.25
        cx, cy = w * 0.38, h / 2
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=WHT)
        r2 = R * 0.8
        d.ellipse((cx + R * 0.25 - r2, cy - r2, cx + R * 0.25 + r2, cy + r2), fill=(227, 10, 23))
        sx, sy, s = w * 0.56, h / 2, h * 0.125
        d.polygon([(sx + (s if i % 2 == 0 else s * 0.4) * math.cos(i * math.pi / 5), sy + (s if i % 2 == 0 else s * 0.4) * math.sin(i * math.pi / 5)) for i in range(10)], fill=WHT)
    return f


def flagfill(img, v, o, t):
    """Country filled with its flag, gold 3D bevelled edge (reference 00:00)."""
    a = fade(o, t, 0.25, 0.35)
    if a <= 0:
        return
    rings = COUNTRY[o["name"]]
    rx = rings_xy(v, rings)
    xs = [p[0] for r in rx for p in r]
    ys = [p[1] for r in rx for p in r]
    x0, x1, y0, y1 = int(min(xs)), int(max(xs)), int(min(ys)), int(max(ys))
    bw, bh = max(2, x1 - x0), max(2, y1 - y0)
    side = max(bw, int(bh * 1.5))
    tex = flag_tex(o["code"], side, int(side / 1.5))
    m = mask_full(v, rings)
    d = ImageDraw.Draw(img)
    for r in rx:                                           # extruded dark-gold side
        d.polygon([(x, y + 10) for x, y in r], fill=(120, 90, 0, int(255 * a)))
    lay = Image.new("RGBA", (v.w, v.h), (0, 0, 0, 0))
    lay.paste(tex, (int((x0 + x1) / 2 - tex.width / 2), int((y0 + y1) / 2 - tex.height / 2)))
    sh = np.asarray(img.convert("RGB")).astype(np.float32).mean(axis=2) / 255.0       # keep relief under the flag
    la = np.asarray(lay).astype(np.float32)
    la[..., :3] *= (0.72 + 0.4 * sh[..., None])
    al = np.asarray(m).astype(np.float32) * a
    la[..., 3] = al
    img.alpha_composite(Image.fromarray(np.clip(la, 0, 255).astype(np.uint8)))
    for r in rx:
        d.line(r + [r[0]], fill=GOLD + (int(255 * a),), width=9, joint="curve")
        d.line(r + [r[0]], fill=(255, 245, 170, int(255 * a)), width=2, joint="curve")


def cfill(img, v, o, t):
    """Country highlight in the reference look: saturated colour that keeps the relief (colourise by luminance),
    thin white border, optional glow. Seas stay translucent (o['flat'])."""
    a = fade(o, t, 0.3, 0.3)
    if a <= 0:
        return
    rings = COUNTRY[o["name"]] if "name" in o else SEA[o["sea"]]
    if o.get("flat"):
        lay = fill_layer(v, rings, o["col"], o.get("alpha", 0.4), o.get("glow"), o.get("border", WHT), o.get("bw", 2))
        if a < 1:
            lay.putalpha(lay.getchannel("A").point(lambda q: int(q * a)))
        img.alpha_composite(lay)
        return
    m = Image.new("L", (v.w // 2, v.h // 2), 0)
    dm = ImageDraw.Draw(m)
    for r in rings_xy(v, rings, 0.5):
        dm.polygon(r, fill=255)
    bb = m.getbbox()
    if bb:
        x0, y0, x1, y1 = bb[0] * 2, bb[1] * 2, min(v.w, bb[2] * 2), min(v.h, bb[3] * 2)
        sub = np.asarray(img.crop((x0, y0, x1, y1)).convert("RGB")).astype(np.float32)
        lum = (0.3 * sub[..., 0] + 0.59 * sub[..., 1] + 0.11 * sub[..., 2]) / 255.0
        lum = np.clip((lum - lum.mean()) * 1.3 + 0.5, 0, 1)            # relief only, independent of desert/forest brightness
        col = np.array(o["col"], np.float32)
        out = np.clip(col * (0.55 + 0.6 * lum[..., None]), 0, 255)
        mk = np.asarray(m.resize((v.w, v.h), Image.BILINEAR).crop((x0, y0, x1, y1))).astype(np.float32) / 255.0
        lay = np.dstack([out, mk * 255 * o.get("alpha", 0.88) * a]).astype(np.uint8)
        img.alpha_composite(Image.fromarray(lay, "RGBA"), (x0, y0))
    glow = o.get("glow")
    d = ImageDraw.Draw(img)
    if glow:
        g = Image.new("RGBA", (v.w // 4, v.h // 4), (0, 0, 0, 0))
        dg = ImageDraw.Draw(g)
        for r in rings_xy(v, rings, 0.25):
            dg.line(r + [r[0]], fill=glow + (int(220 * a),), width=3, joint="curve")
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(2.5)).resize((v.w, v.h), Image.BILINEAR))
    for r in rings_xy(v, rings):
        d.line(r + [r[0]], fill=o.get("border", WHT) + (int(255 * a),), width=o.get("bw", 3), joint="curve")


def elev(img, v, o, t):
    """High ground (> min m) inside the country: fiery orange texture with pulsing yellow-orange glow."""
    a = fade(o, t, 0.5, 0.3)
    if a <= 0:
        return
    w4, h4 = v.w // 4, v.h // 4
    xs = (np.arange(w4) * 4 + 2 - v.w / 2) / v.kx + v.lon
    ys = v.lat - (np.arange(h4) * 4 + 2 - v.h / 2) / v.ppd
    LO, LA = np.meshgrid(xs, ys)
    ix = np.clip(((LO - 25.0) / 0.02).astype(int), 0, DEM.shape[1] - 1)
    iy = np.clip(((43.5 - LA) / 0.02).astype(int), 0, DEM.shape[0] - 1)
    inside = (LO >= 25) & (LO <= 46.5) & (LA >= 35) & (LA <= 43.5)
    e = DEM[iy, ix] * inside
    cm = np.asarray(mask_full(View(v.lon, v.lat, v.span, w4, h4), COUNTRY[o["name"]])) > 0
    m = np.clip((e - o["min"]) / 400, 0, 1) * cm
    shade = SHADE[iy, ix]
    col = np.zeros((h4, w4, 4), np.float32)
    col[..., 0] = 255 * shade
    col[..., 1] = 109 * shade + 40 * np.clip((e - 2500) / 1500, 0, 1)
    col[..., 2] = 0
    col[..., 3] = m * 200 * a
    lay = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)).resize((v.w, v.h), Image.BILINEAR)
    pul = 0.6 + 0.4 * math.sin((t - o["t0"]) * 5)
    edge = Image.fromarray((m > 0.5).astype(np.uint8) * 255).filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
    g = Image.new("RGBA", (w4, h4), (255, 171, 0, 0))
    g.putalpha(edge.point(lambda q: int(q * 0.9 * pul * a)))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(1.5)).resize((v.w, v.h), Image.BILINEAR))
    img.alpha_composite(lay)


def pin(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.35)
    a = clamp((o["t1"] - t) / 0.25)
    X, Y = v.xy(o["lon"], o["lat"])
    L = o.get("len", 170) * clamp((t - o["t0"]) / 0.25)
    d = ImageDraw.Draw(img)
    d.line((X + 2, Y + 2, X + 2, Y - L + 2), fill=(0, 0, 0, int(150 * a)), width=4)
    d.line((X, Y, X, Y - L), fill=WHT + (int(255 * a),), width=4)
    if not o.get("sub"):
        d.ellipse((X - 8, Y - 8, X + 8, Y + 8), fill=WHT + (int(255 * a),), outline=BLK + (int(200 * a),), width=2)
    lay = text_layer(o["txt"], font(OSW, o.get("size", 78)), WHT, 2, True, a)
    put(img, lay, X, Y - L - lay.height / 2 + 24, k)
    if o.get("sub") and t >= o.get("sub_t", o["t0"]):
        v0, v1, fmt, dur = o["sub"]
        val = v0 + (v1 - v0) * clamp((t - o.get("sub_t", o["t0"])) / dur) ** 0.6
        sl = text_layer(fmt.format(val), font(OSW, o.get("size", 78) * 0.85), WHT, 2, True, a)
        put(img, sl, X, Y + sl.height / 2 - 14, back((t - o.get("sub_t", o["t0"])) / 0.3), -4)


def curved(img, v, o, t):
    """Sea name warped along an arc, white with a teal ghost copy underneath (reference 00:20)."""
    a = fade(o, t, 0.4, 0.3)
    if a <= 0:
        return
    X, Y = v.xy(o["lon"], o["lat"])
    f = font(MX, o.get("size", 58))
    txt = o["txt"]
    R = o.get("radius", 900)
    rot = math.radians(o.get("angle", -12))
    widths = [f.getlength(c) for c in txt]
    tot = sum(widths)
    s = -tot / 2
    k = back((t - o["t0"]) / 0.5)
    for ghost, col, off in ((True, (0, 150, 140), (5, 8)), (False, WHT, (0, 0))):
        acc = s
        for c, cw in zip(txt, widths):
            phi = (acc + cw / 2) / R
            px = X + R * math.sin(phi) * math.cos(rot) - (R - R * math.cos(phi)) * math.sin(rot) * -1
            py = Y - (R - R * math.cos(phi)) * math.cos(rot) - R * math.sin(phi) * math.sin(rot) * -1
            acc += cw
            if c == " ":
                continue
            lay = text_layer(c, f, col, 0 if ghost else 3, False, a * (0.8 if ghost else 1.0))
            put(img, lay, px + off[0], py + off[1], k, -math.degrees(phi + rot))


def ruler(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    A = v.xy(*o["a"])
    B = v.xy(*o["b"])
    u = ease((t - o["t0"]) / 0.5)
    P = (A[0] + (B[0] - A[0]) * u, A[1] + (B[1] - A[1]) * u)
    d = ImageDraw.Draw(img)
    ang = math.atan2(B[1] - A[1], B[0] - A[0])
    nx, ny = -math.sin(ang) * 26, math.cos(ang) * 26
    d.line((A, P), fill=(0, 0, 0, 160), width=12)
    d.line((A, P), fill=WHT + (255,), width=7)
    for q in (A, P):
        d.line((q[0] - nx, q[1] - ny, q[0] + nx, q[1] + ny), fill=WHT + (255,), width=7)
    if t >= o["t0"] + 0.2:
        val = o["v0"] + (o["v1"] - o["v0"]) * ease((t - o["t0"] - 0.2) / o.get("dur", 1.0))
        lay = text_layer(o["fmt"].format(val), font(MB, o.get("size", 70)), WHT, 6)
        mx, my = (A[0] + B[0]) / 2 - nx * 3.2, (A[1] + B[1]) / 2 - ny * 3.2
        put(img, lay, mx, my, 1.0, -math.degrees(ang))


def counter(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    val = o["v0"] + (o["v1"] - o["v0"]) * clamp((t - o["t0"]) / o.get("dur", 1.2)) ** 0.6
    X, Y = v.xy(o["lon"], o["lat"]) if "lon" in o else (o["x"], o["y"])
    a = clamp((o["t1"] - t) / 0.25)
    lay = text_layer(o["fmt"].format(val), fit(MB, o.get("size", 76), o["fmt"].format(o["v1"]), 980), o.get("col", WHT), 7, True, a)
    put(img, lay, X, Y, back((t - o["t0"]) / 0.3))


def label(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.25)
    X, Y = v.xy(o["lon"], o["lat"]) if "lon" in o else (o["x"], o["y"])
    fnt = o.get("font", OSW)
    lay = text_layer(o["txt"], fit(fnt, o.get("size", 60) * (1.2 if fnt == OSW else 1.0), o["txt"], 1000), o.get("col", WHT), 2 if fnt == OSW else 5, True, a)
    put(img, lay, X, Y, back((t - o["t0"]) / 0.3))


def capsule(d, a, b, w, col):
    d.line((a, b), fill=col, width=int(w))
    for p in (a, b):
        d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=col)


def arm(d, S, s, side, flex, pulse):
    """Cartoon flexing arm (emoji-like) from shoulder S; side +1 = right, -1 = left. Black outline pass, then fill."""
    E = (S[0] + side * 1.55 * s, S[1] + 0.05 * s)
    phi = math.radians(16 - 36 * flex)
    ux, uy = side * math.sin(phi), -math.cos(phi)                              # forearm direction
    F = (E[0] + ux * 1.95 * s, E[1] + uy * 1.95 * s)
    B = (S[0] + side * 0.95 * s, S[1] - 0.36 * s)
    rb = 0.44 * s * (1 + 0.28 * pulse)
    lerp = lambda u: (E[0] + (F[0] - E[0]) * u, E[1] + (F[1] - E[1]) * u)        # noqa: E731
    body, light, ink = (150, 62, 192, 255), (196, 120, 230, 255), (12, 6, 18, 255)
    o = 0.17 * s
    for out in (True, False):
        c = ink if out else body
        add = o if out else 0
        capsule(d, S, E, 0.6 * s + add, c)
        capsule(d, E, lerp(0.85), 0.5 * s + add, c)
        r = 0.44 * s + add / 2
        d.ellipse((F[0] - r, F[1] - r, F[0] + r, F[1] + r), fill=c)
        d.ellipse((B[0] - rb - add / 2, B[1] - rb - add / 2, B[0] + rb + add / 2, B[1] + rb + add / 2), fill=c)
    d.ellipse((B[0] - rb * 0.55, B[1] - rb * 0.7, B[0] + rb * 0.1, B[1] - rb * 0.15), fill=light)
    for q in (-0.15, 0.12):                                 # knuckle creases on the fist
        kx, ky = F[0] - side * 0.2 * s, F[1] + q * s
        d.arc((kx - 0.2 * s, ky - 0.1 * s, kx + 0.2 * s, ky + 0.1 * s), 180, 360, fill=ink, width=max(3, int(0.07 * s)))
    cx, cy = lerp(0.66)
    px, py = -uy, ux                                         # perpendicular
    hw, hl = 0.36 * s, 0.17 * s
    band = [(cx + px * hw + ux * hl, cy + py * hw + uy * hl), (cx - px * hw + ux * hl, cy - py * hw + uy * hl),
            (cx - px * hw - ux * hl, cy - py * hw - uy * hl), (cx + px * hw - ux * hl, cy + py * hw - uy * hl)]
    d.polygon(band, fill=(198, 255, 0, 255), outline=ink, width=max(4, int(0.08 * s)))


def face(d, X, Y, s, mood, t, t0):
    if mood == "angry":
        for sx in (-1, 1):
            cx = X + sx * 1.05 * s
            d.ellipse((cx - 0.8 * s - 5, Y - 0.72 * s - 5, cx + 0.8 * s + 5, Y + 0.72 * s + 5), fill=(10, 6, 16, 255))
            d.ellipse((cx - 0.8 * s, Y - 0.72 * s, cx + 0.8 * s, Y + 0.72 * s), fill=WHT + (255,))
            pr = 0.3 * s
            px = cx - sx * 0.2 * s
            d.ellipse((px - pr, Y - pr + 0.1 * s, px + pr, Y + pr + 0.1 * s), fill=(10, 6, 16, 255))
            # angry lid: slanted dark wedge covering the top inner part
            d.polygon([(cx - 0.95 * s, Y - 0.95 * s), (cx + 0.95 * s, Y - 0.95 * s),
                       (cx + sx * -0.95 * s, Y - (0.05 if sx > 0 else -0.05) * s - 0.1 * s), (cx - sx * -0.95 * s, Y - 0.62 * s)],
                      fill=(123, 31, 162, 255))
            d.line((cx - sx * 0.95 * s, Y - 0.1 * s, cx + sx * 0.95 * s, Y - 0.7 * s), fill=(10, 6, 16, 255), width=max(6, int(0.2 * s)))
        d.arc((X - 0.6 * s, Y + 0.95 * s, X + 0.6 * s, Y + 1.6 * s), 200, 340, fill=(10, 6, 16, 255), width=max(6, int(0.18 * s)))
    else:
        look = math.sin((t - t0) * 1.6)
        for sx in (-1, 1):
            cx = X + sx * 1.15 * s
            blink = 0.12 if (t - t0) % 2.8 > 2.66 else 1.0
            rw, rh = 0.95 * s, 1.1 * s * blink
            d.ellipse((cx - rw - 6, Y - rh - 6, cx + rw + 6, Y + rh + 6), fill=(10, 6, 16, 255))
            d.ellipse((cx - rw, Y - rh, cx + rw, Y + rh), fill=WHT + (255,))
            if blink > 0.5:
                pr = 0.5 * s
                px, py = cx + look * 0.3 * s, Y - 0.35 * s
                d.ellipse((px - pr, py - pr, px + pr, py + pr), fill=(10, 6, 16, 255))
                d.ellipse((px - pr * 0.1, py - pr * 0.75, px + pr * 0.45, py - pr * 0.2), fill=WHT + (255,))
            d.arc((cx - 0.8 * s, Y - 1.9 * s, cx + 0.8 * s, Y - 1.2 * s), 200, 340, fill=(10, 6, 16, 255), width=max(5, int(0.16 * s)))
        d.arc((X - 0.55 * s, Y + 0.9 * s, X + 0.55 * s, Y + 1.7 * s), 20, 160, fill=(10, 6, 16, 255), width=max(6, int(0.18 * s)))


def character(img, v, o, t):
    """Country as a cartoon character: face + optional flexing arms on the borders; pops in, pops out."""
    if t < o["t0"] or t > o["t1"]:
        return
    kin = back((t - o["t0"]) / 0.35)
    kout = clamp((o["t1"] - t) / 0.2)
    k = kin * kout
    s = o.get("s", 46) * k
    dt = t - o["t0"]
    lay = Image.new("RGBA", (v.w, v.h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    shake = (math.sin(dt * 47) * 4, math.cos(dt * 39) * 3) if o["mood"] == "angry" else (0, math.sin(dt * 2 * math.pi * 0.9) * 7)
    if o.get("arms"):
        flex = 0.5 + 0.5 * math.sin(dt * 2 * math.pi / 0.62)
        for side, key in ((-1, "left"), (1, "right")):
            S = v.xy(*o[key])
            arm(d, (S[0] + shake[0], S[1] + shake[1]), o.get("arm_s", 78) * k, side, flex, flex)
    X, Y = v.xy(o["lon"], o["lat"])
    face(d, X + shake[0], Y + shake[1], s, o["mood"], t, o["t0"])
    img.alpha_composite(lay)


def bubble(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.32) * clamp((o["t1"] - t) / 0.2)
    if k <= 0.01:
        return
    X, Y = v.xy(o["lon"], o["lat"]) if "lon" in o else (o["x"], o["y"])
    f = font(BANG, o.get("size", 84))
    X = min(max(X, f.getlength(o["txt"]) / 2 + 90), W - f.getlength(o["txt"]) / 2 - 90)        # keep the bubble on screen
    tw = f.getlength(o["txt"])
    bw, bh = tw + 80, f.size * 1.25 + 40
    lay = Image.new("RGBA", (int(bw + 40), int(bh + 90)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = 20, 20, 20 + bw, 20 + bh
    tail = [(x0 + bw * 0.38, y1 - 4), (x0 + bw * 0.30, y1 + 60), (x0 + bw * 0.55, y1 - 4)]
    d.rounded_rectangle((x0 + 5, y0 + 8, x1 + 5, y1 + 8), int(bh * 0.45), fill=(0, 0, 0, 110))
    d.polygon(tail, fill=(213, 0, 0, 255))
    d.rounded_rectangle((x0, y0, x1, y1), int(bh * 0.45), fill=(213, 0, 0, 255))
    d.rounded_rectangle((x0 + 7, y0 + 7, x1 - 7, y1 - 7), int(bh * 0.4), fill=(255, 214, 0, 255))
    d.polygon([(p[0] + (7 if i != 1 else 3), p[1] - (7 if i != 1 else 12)) for i, p in enumerate(tail)], fill=(255, 214, 0, 255))
    d.text(((x0 + x1) / 2, (y0 + y1) / 2 + 4), o["txt"], font=f, fill=(15, 10, 10, 255), anchor="mm")
    put(img, lay, X, Y - lay.height / 2 + 40, k, o.get("angle", 0))


def route(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    pts = v.pts(o["pts"])
    k = ease((t - o["t0"]) / o.get("dur", 1.0))
    L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = sum(L) * k
    out = [pts[0]]
    for i, l in enumerate(L):
        if tot <= 0:
            break
        u = min(1.0, tot / max(l, 1e-6))
        out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u))
        tot -= l
    d = ImageDraw.Draw(img)
    a = clamp((o["t1"] - t) / 0.25)
    if len(out) > 1:
        d.line(out, fill=(0, 0, 0, int(140 * a)), width=o.get("w", 8) + 6, joint="curve")
        d.line(out, fill=o.get("col", WHT) + (int(255 * a),), width=o.get("w", 8), joint="curve")


DRAW = {"flagfill": flagfill, "fill": cfill, "elev": elev, "pin": pin, "curved": curved, "ruler": ruler, "counter": counter,
        "label": label, "char": character, "bubble": bubble, "route": route}
ORDER = ["fill", "flagfill", "elev", "route", "ruler", "char", "pin", "curved", "counter", "label", "bubble"]


# ------------------------------------------------------------------ tilted world card
SCENES = []     # (t0, t1, params) for tilt-card segments


def TILT(t0, t1, **kw):
    SCENES.append((t0, t1, kw))


FW, FH = 1500, 1000
_BG = Image.new("RGB", (W, H), (8, 20, 52))
_bd = ImageDraw.Draw(_BG)
for _y in range(H):
    _bd.line((0, _y, W, _y), fill=(6 + _y // 160, 16 + _y // 90, 44 + _y // 50))
for _x in range(0, W + 1, 86):
    _bd.line((_x, 0, _x, H), fill=(25, 118, 210), width=2)
for _y in range(0, H + 1, 86):
    _bd.line((0, _y, W, _y), fill=(25, 118, 210), width=2)
del _bd
_BG = _BG.convert("RGBA")


def persp_coeffs(src, dst):
    A, B = [], []
    for (x, y), (X, Y) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -X * x, -X * y]); B.append(X)
        A.append([0, 0, 0, x, y, 1, -Y * x, -Y * y]); B.append(Y)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def card_quad(scale, tilt, roll):
    cx, cy = 540, 900
    hb = 500 * scale
    ht = hb * (1 - 0.18 * tilt)
    hh = hb * FH / FW * (1 - 0.12 * tilt)
    q = [(-ht, -hh), (ht, -hh), (hb, hh), (-hb, hh)]
    c, s = math.cos(math.radians(roll)), math.sin(math.radians(roll))
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in q]


def arc_pts(a, b, lift=0.28, n=48):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    L = math.dist(a, b)
    nx, ny = -(b[1] - a[1]) / max(L, 1), (b[0] - a[0]) / max(L, 1)
    if ny > 0:
        nx, ny = -nx, -ny
    c = (mx + nx * L * lift, my + ny * L * lift)
    return [((1 - u) ** 2 * a[0] + 2 * (1 - u) * u * c[0] + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * c[1] + u * u * b[1])
            for u in np.linspace(0, 1, n)]


def tilt_frame(t, sc):
    t0, t1, p = sc
    q = ease((t - t0) / 0.9)
    lon, lat, span = p["cam"]
    v = View(lon, lat, span, FW, FH)
    l0, l1, b0, b1 = bbox("OTT")
    w, h = size("OTT")
    a0, a1, c0, c1 = v.geo_bbox()
    flat = (sat("OTT").resize((FW, FH), Image.BILINEAR, box=((a0 - l0) / (l1 - l0) * w, (b1 - c1) / (b1 - b0) * h,
                                                                  (a1 - l0) / (l1 - l0) * w, (b1 - c0) / (b1 - b0) * h))).convert("RGBA")
    for name in p.get("red", []):
        if t >= p.get("red_t", t0):
            k = clamp((t - p["red_t"] - p["red"].index(name) * 0.06) / 0.3)
            if k > 0:
                lay = fill_layer(v, COUNTRY[name], (213, 0, 0), 0.8 * k, None, WHT, 2)
                flat.alpha_composite(lay)
    d = ImageDraw.Draw(flat)
    src = v.xy(*p["origin"])
    for i, (dst, ta) in enumerate(p.get("arcs", [])):
        if t < ta:
            continue
        pts = arc_pts(src, v.xy(*dst))
        e = clamp((t - ta) / 0.45)
        n = max(2, int(len(pts) * e))
        g = Image.new("RGBA", (FW // 2, FH // 2), (0, 0, 0, 0))
        ImageDraw.Draw(g).line([(x / 2, y / 2) for x, y in pts[:n]], fill=CYAN + (230,), width=9, joint="curve")
        flat.alpha_composite(g.filter(ImageFilter.GaussianBlur(4)).resize((FW, FH), Image.BILINEAR))
        d.line(pts[:n], fill=CYAN + (255,), width=6, joint="curve")
        m = ((t - ta) * 2.2) % 1.0                         # yellow pulse travelling along the arc
        j = int(m * (n - 1))
        x, y = pts[j]
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 214, 0, 255))
        if e >= 1:
            x, y = pts[-1]
            d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=(255, 214, 0, 255), outline=WHT + (255,), width=3)
    d.ellipse((src[0] - 14, src[1] - 14, src[0] + 14, src[1] + 14), fill=(227, 10, 23, 255), outline=WHT + (255,), width=4)
    for txt, lon_, lat_, ta, col in p.get("labels", []):
        if t >= ta:
            X, Y = v.xy(lon_, lat_)
            put(flat, text_layer(txt, font(MX, 64), col, 5), X, Y, back((t - ta) / 0.3))
    if p.get("note"):
        put(flat, text_layer(p["note"], font(MX, 30), WHT, 3), FW - 170, FH - 40)
    scale = p.get("s0", 2.2) + (p.get("s1", 1.0) - p.get("s0", 2.2)) * q
    quad = card_quad(scale, q, p.get("roll", 5) * q)
    img = _BG.copy()
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + 14, y + 26) for x, y in quad], fill=(0, 0, 0, 170))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    img.alpha_composite(flat.transform((W, H), Image.PERSPECTIVE, persp_coeffs([(0, 0), (FW, 0), (FW, FH), (0, FH)], quad), Image.BILINEAR))
    ImageDraw.Draw(img).line(quad + [quad[0]], fill=WHT + (255,), width=6, joint="curve")
    return img


# ------------------------------------------------------------------ captions
WORDS = []
for _i, _line in enumerate(LINES):
    _ws = _line.split()
    _chunks, _cur = [], []
    for _j, _w in enumerate(_ws):
        _cur.append(_j)
        if len(_cur) == 2 or _w[-1] in ",.?!:" or _j == len(_ws) - 1 or len(_w) >= 9:
            _chunks.append(_cur)
            _cur = []
    for _c in _chunks:
        for _j in _c:
            WORDS.append((_i, _j, _c))


def caption(img, t):
    for i in range(len(LINES)):
        if not (ST[i] - 0.05 <= t < ST[i] + D[i] + 0.25):
            continue
        ws = LINES[i].split()
        cur = 0
        for j, off in enumerate(TW[i]):
            if t >= ST[i] + off - 0.03:
                cur = j
        chunk = next(c for (ii, jj, c) in WORDS if ii == i and jj == cur)
        txts = [ws[j].upper().strip() for j in chunk]
        f = fit(MB, 72, " ".join(txts), 960)
        sp = f.getlength(" ") * 1.7
        widths = [f.getlength(x) * 1.04 for x in txts]
        x = 540 - (sum(widths) + sp * (len(txts) - 1)) / 2
        for j, txt, wd in zip(chunk, txts, widths):
            on = j == cur
            k = 1.0
            if on:
                k = 1.0 + 0.15 * clamp(1 - (t - ST[i] - TW[i][j]) / 0.12) + 0.0
                k = max(1.0, min(1.15, 1.15 - 0.15 * clamp((t - ST[i] - TW[i][j] - 0.12) / 0.2)))
            lay = text_layer(txt, f, YEL if on else WHT, 7, True)
            put(img, lay, x + wd / 2, 1382, k)
            x += wd + sp
        return


# ------------------------------------------------------------------ build
import shots63  # noqa: E402

shots63.build(SHORT, K, O, TILT, WT, ST, D)
CUTS = sorted({k[0] for k in CAM if k[4]} | {s[0] for s in SCENES} | {s[1] for s in SCENES})


def credit(img, extra=""):
    ImageDraw.Draw(img).text((W - 16, H - 12), "Imagery © Esri, Maxar, Earthstar Geographics · Natural Earth" + extra,
                             font=font(MX, 16), fill=(255, 255, 255, 150), anchor="rs")


def frame(fi):
    t = fi / FPS
    sc = next((s for s in SCENES if s[0] <= t < s[1]), None)
    if sc:
        img = tilt_frame(t, sc)
        v = View(*camera(t))
        for o in OV:
            if o["kind"] in ("counter", "label") and "lon" not in o and o["t0"] - 0.01 <= t <= o["t1"]:
                DRAW[o["kind"]](img, v, o, t)
    else:
        v = View(*camera(t))
        img = render_map(v)
        live = [o for o in OV if o["t0"] - 0.01 <= t <= o["t1"] + 0.01 and not o.get("card")]
        for kind in ORDER:
            for o in live:
                if o["kind"] == kind:
                    DRAW[kind](img, v, o, t)
    credit(img, " · Elevation: AWS Terrain Tiles" if any(o["kind"] == "elev" and o["t0"] <= t <= o["t1"] for o in OV) else "")
    caption(img, t)
    a = (np.asarray(img.convert("RGB")).astype(np.uint16) * VIG) >> 8
    return a.astype(np.uint8)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print(SHORT, "frames", NF, "total", round(TOTAL, 2), "keys", len(CAM), "overlays", len(OV), "cuts", [round(c, 2) for c in CUTS])
    elif cmd == "still":
        os.makedirs(f"{SHORT}/stills63", exist_ok=True)
        for a in sys.argv[2:]:
            Image.fromarray(frame(int(float(a) * FPS))).save(f"{SHORT}/stills63/{float(a):05.1f}.jpg", quality=86)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
        p.stdin.close()
        p.wait()
