"""Map Shorts engine v64: remake of the OneCriticalMoment reference style (q6L_j157rGo), vertical 1080x1920 @30 fps.
Adds: orthographic globe, snow seasons, route arrow, unit icons, forts/fire, dated banner, stamps, thermometer, HUD card.
Based on engine63 (MapTrail style).
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

sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/lofoten_2026_10_22")
from scripts import SHORTS  # noqa: E402
from sat65 import SP, size  # noqa: E402

W, H, FPS = 1080, 1920, 30
MB, MX, BANG, OSW = "assets/Montserrat-Black.ttf", "assets/Montserrat-ExtraBold.ttf", "assets/Bangers.ttf", "assets/Oswald-Regular.ttf"
OSWB = "assets/Oswald-Bold.ttf"
WHT, BLK, YEL = (255, 255, 255), (0, 0, 0), (255, 214, 0)
CYAN, PURPLE, GOLD = (0, 229, 255), (123, 31, 162), (255, 215, 0)

SHORT = os.environ.get("SHORT", "lofoten")
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
RIVERS = _shp("assets/ne_rivers/ne_10m_rivers_lake_centerlines.shp", "name")


def bbox(key):
    lon0, lat0, d = SP[key]
    w, h = size(key)
    dl = d * (w / h) / math.cos(math.radians(lat0))
    return lon0 - dl, lon0 + dl, lat0 - d, lat0 + d


@lru_cache(maxsize=10)
def sat(key):
    """Graded once at load (the grade is a per-pixel colour map, so it commutes with cropping)."""
    p = f"sat65g/{key}.jpg"
    if not os.path.exists(p):
        os.makedirs("sat65g", exist_ok=True)
        g_ = grade(Image.open(f"sat65/{key}.jpg").convert("RGB")).convert("RGB")
        if key in ("MAL", "LOF", "NOR", "REI", "LO2", "MID", "RE2", "RE3"):                                    # the wide archipelago view is very dark: lift shadows so the atolls read on a phone
            g_ = Image.fromarray(np.clip(255 * (np.asarray(g_).astype(np.float32) / 255) ** 0.6 * 1.15, 0, 255).astype(np.uint8))
        if os.path.exists(f"dem/{key}.npy"):                # terrain relief (Google-Earth-like 3D look): hillshade from AWS Terrain Tiles
            g_ = Image.fromarray(np.clip(np.asarray(g_).astype(np.float32) * relief(key, g_.size)[..., None], 0, 255).astype(np.uint8))
        g_.save(p, quality=94)
    return Image.open(p).convert("RGB")


def relief(key, sz):
    """Multiplicative hillshade over land (sun from the north-west, 40 deg up), resized to the satellite image."""
    e = np.load(f"dem/{key}.npy")
    lon0, lat0, d = SP[key]
    w, h = size(key)
    dl = d * (w / h) / math.cos(math.radians(lat0))
    dy = 2 * d * 111320 / e.shape[0]
    dx = 2 * dl * 111320 * math.cos(math.radians(lat0)) / e.shape[1]
    gy, gx = np.gradient(e, dy, dx)
    slope = np.arctan(np.hypot(gx, gy) * 1.6)                 # mild vertical exaggeration
    aspect = np.arctan2(-gx, gy)
    az, alt = math.radians(315), math.radians(40)
    shade = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
    flat = math.sin(alt)
    f = 1.0 + 0.55 * (shade - flat)
    f = np.where(e > 3, f, 1.0)
    f = cv2.GaussianBlur(f.astype(np.float32), (0, 0), 2.0)
    return cv2.resize(np.clip(f, 0.45, 1.45), sz, interpolation=cv2.INTER_CUBIC)


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
    if box[0] >= 0 and box[1] >= 0 and box[2] <= w and box[3] <= h:
        return sat(key).resize((v.w, v.h), Image.BILINEAR, box=box, reducing_gap=2.0)
    # view reaches past the image (oblique canvases): resize the overlapping part and pad with the image's edge colour
    ib = (max(0, box[0]), max(0, box[1]), min(w, box[2]), min(h, box[3]))
    out = Image.new("RGB", (v.w, v.h), tuple(int(x) for x in np.asarray(sat(key).resize((8, 8))).reshape(-1, 3).mean(axis=0)))
    if ib[2] - ib[0] > 2 and ib[3] - ib[1] > 2:
        sx, sy = v.w / (box[2] - box[0]), v.h / (box[3] - box[1])
        part = sat(key).resize((max(1, int((ib[2] - ib[0]) * sx)), max(1, int((ib[3] - ib[1]) * sy))), Image.BILINEAR, box=ib, reducing_gap=2.0)
        out.paste(part, (int((ib[0] - box[0]) * sx), int((ib[1] - box[1]) * sy)))
    return out


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
    if len(ok) > 1 and fine != "MAL":                       # MAL is far sharper than WLD at the Maldives: no coarse blend (it smears the atolls)
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
        if isinstance(v, GlobeView) and not any(v.vis(lo, la) for lo, la in r[::max(1, len(r) // 10)]):
            continue
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
        if len(_cur) == 3 or _w[-1] in ",.?!:" or _j == len(_ws) - 1 or len(_w) >= 11:
            _chunks.append(_cur)
            _cur = []
    for _c in _chunks:
        for _j in _c:
            WORDS.append((_i, _j, _c))


def caption(img, t):
    if SHORT in ("maldives", "lofoten"):                       # silent Short: text comes from overlays only
        return
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
        f = fit(MB, 78, " ".join(txts), 980)
        sp = f.getlength(" ") * 2.0
        widths = [f.getlength(x) * 1.06 for x in txts]
        x = 540 - (sum(widths) + sp * (len(txts) - 1)) / 2
        for j, txt, wd in zip(chunk, txts, widths):
            on = j == cur
            k = 1.0
            lay = text_layer(txt, f, WHT, 7, True)
            put(img, lay, x + wd / 2, 1500, k)
            x += wd + sp
        return



# ================================================================== v64 additions
import cv2  # noqa: E402

SEASON = []     # (t, f): 0 = summer, 1 = deep winter


def SN(t, f):
    SEASON.append((t, f))


def season(t):
    ks = sorted(SEASON)
    if not ks:
        return 0.0
    if t <= ks[0][0]:
        return ks[0][1]
    for (a, fa), (b, fb) in zip(ks, ks[1:]):
        if a <= t < b:
            return fa + (fb - fa) * ease((t - a) / max(1e-3, b - a))
    return ks[-1][1]


FLASH = []      # white flashes (snow arrives, cuts with impact)


def winter_rgb(a, lat, f):
    """a: HxWx3 float32 graded imagery, lat: per-row latitude (H,), f: 0..1 -> bright snow on land (relief kept), ice on water."""
    w = np.clip((lat - 38.0) / 14.0, 0, 1)
    w = w * w * (3 - 2 * w)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    water = ((b > r + 6) & (lum < 125))[..., None]
    land = ~water
    snow = np.array([252, 254, 255], np.float32)
    k = (f * w)[:, None, None]
    detail = ((lum - 95.0) * 0.7)[..., None]                       # forest / relief texture shows through the snow
    sn = (snow + detail) * np.array([0.96, 0.985, 1.0], np.float32)
    out = a * (1 - 0.93 * k * land) + sn * 0.93 * k * land
    kw = k * water * 0.8
    out = out * (1 - kw) + np.array([84, 156, 226], np.float32) * kw
    return np.clip(out, 0, 255)


def winterize(im, v, f):
    if f <= 0.01:
        return im
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    lat = v.lat + (v.h / 2 - np.arange(v.h)) / v.ppd
    return Image.fromarray(np.clip(winter_rgb(a, lat, f), 0, 255).astype(np.uint8)).convert("RGBA")


def render_map64(v):
    """render_map + fill of the empty rows (no imagery north of ~72.5 N at this scale) from the world image."""
    im = render_map(v).convert("RGB")
    a = np.asarray(im)
    rows = a.sum(axis=2).mean(axis=1) < 22
    if rows.any() and covers("WLD", v):
        base = crop("WLD", v).convert("RGB")
        m = rows.astype(np.float32)
        m = np.convolve(m, np.ones(25) / 25, "same")[:, None, None]
        im = Image.fromarray((np.asarray(base) * m + a * (1 - m)).astype(np.uint8))
    return im.convert("RGBA")


# ------------------------------------------------------------------ globe
class GlobeView:
    def __init__(self, lon, lat, R, cx=540, cy=960):
        self.lon, self.lat, self.R, self.cx, self.cy = lon, lat, R, cx, cy
        self.w, self.h = W, H
        self.span = 0

    def _raw(self, lon, lat):
        la, lo, la0, lo0 = math.radians(lat), math.radians(lon), math.radians(self.lat), math.radians(self.lon)
        cosc = math.sin(la0) * math.sin(la) + math.cos(la0) * math.cos(la) * math.cos(lo - lo0)
        x = math.cos(la) * math.sin(lo - lo0)
        y = math.cos(la0) * math.sin(la) - math.sin(la0) * math.cos(la) * math.cos(lo - lo0)
        return x, y, cosc

    def xy(self, lon, lat):
        x, y, c = self._raw(lon, lat)
        if c < 0:
            n = math.hypot(x, y) or 1.0
            x, y = x / n, y / n
        return self.cx + x * self.R, self.cy - y * self.R

    def vis(self, lon, lat):
        return self._raw(lon, lat)[2] > 0.02

    def pts(self, ring):
        return [self.xy(lo, la) for lo, la in ring]

    def geo_bbox(self):
        return self.lon - 90, self.lon + 90, self.lat - 90, self.lat + 90


_GL = {}


def globe_assets():
    if not _GL:
        a = np.asarray(sat("WLD")).copy()
        a[:57] = a[57].astype(np.float32).mean(axis=0).astype(a.dtype)       # no imagery beyond 85 N / S: flat polar cap (no radial streaks)
        a[1990:] = a[1989].astype(np.float32).mean(axis=0).astype(a.dtype)
        tex_s = a
        lat = 90.0 - (np.arange(a.shape[0]) + 0.5) / a.shape[0] * 180.0
        tex_w = np.clip(winter_rgb(a.astype(np.float32), lat, 1.0), 0, 255).astype(np.uint8)
        YYg, XXg = np.mgrid[0:H, 0:W].astype(np.float32)
        rng = np.random.default_rng(64)
        stars = np.zeros((H, W, 3), np.float32)
        stars += np.array([0, 5, 17], np.float32)
        for _ in range(420):
            x, y = int(rng.integers(0, W)), int(rng.integers(0, H))
            b = float(rng.uniform(80, 255))
            stars[y:y + 2, x:x + 2] = (b, b, min(255.0, b * 1.1))
        nb = np.zeros((H, W, 3), np.float32)
        for cx_, cy_, rr_, col_ in [(180, 300, 520, (0, 90, 95)), (900, 700, 600, (8, 70, 110)), (300, 1500, 650, (0, 80, 70)), (980, 1750, 500, (6, 60, 100)), (560, 80, 420, (0, 70, 90))]:
            nb += np.exp(-((XXg - cx_) ** 2 + (YYg - cy_) ** 2) / (2 * (rr_ / 2.0) ** 2))[..., None] * np.array(col_, np.float32) * 0.95
        stars = np.clip(stars + nb, 0, 255)
        rng2 = np.random.default_rng(7)
        _GL.update(tex_s=tex_s, tex_w=tex_w, XX=XXg, YY=YYg, stars=stars, dust=rng2.uniform(0, 1, (140, 4)))
    return _GL


def globe_img(v, f, tt=0.0):
    g = globe_assets()
    X = (g["XX"] - v.cx) / v.R
    Y = (v.cy - g["YY"]) / v.R
    r2 = X * X + Y * Y
    inside = r2 <= 1.0
    Z = np.sqrt(np.maximum(0.0, 1.0 - r2))
    p0 = math.radians(v.lat)
    sinp = np.clip(Z * math.sin(p0) + Y * math.cos(p0), -1, 1)
    phi = np.arcsin(sinp)
    lam = math.radians(v.lon) + np.arctan2(X, Z * math.cos(p0) - Y * math.sin(p0))
    th, tw_ = g["tex_s"].shape[:2]
    mu = ((np.degrees(lam) + 180.0) % 360.0) / 360.0 * tw_
    mv = (90.0 - np.degrees(phi)) / 180.0 * th
    mu = mu.astype(np.float32)
    mv = mv.astype(np.float32)
    col = cv2.remap(g["tex_s"], mu, mv, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP).astype(np.float32)
    if f > 0.01:
        colw = cv2.remap(g["tex_w"], mu, mv, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP).astype(np.float32)
        col = col * (1 - f) + colw * f
    r = np.sqrt(r2)
    limb = np.clip((r - 0.86) / 0.14, 0, 1)
    col = col * (0.58 + 0.42 * Z[..., None] ** 0.35)
    col = col + limb[..., None] * np.array([40, 95, 150], np.float32) * 0.55
    glow = np.exp(-np.maximum(r - 1.0, 0) * 22.0)[..., None] * np.array([79, 163, 227], np.float32) * 0.85
    bg = g["stars"] + glow * (r >= 1.0)[..., None]
    bg = bg + dust_plate(tt)
    out = np.where(inside[..., None], col, bg)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")


GCAM = []       # (t, lon, lat, R)
SCN = []        # (t0, t1) globe scenes; everything else is the flat map


def GK(t, lon, lat, R):
    GCAM.append((t, lon, lat, R))


def GLOBE(t0, t1):
    SCN.append((t0, t1))


def globe_cam(t):
    ks = sorted(GCAM)
    if t <= ks[0][0]:
        return ks[0][1:]
    for a, b in zip(ks, ks[1:]):
        if a[0] <= t < b[0]:
            u = ease((t - a[0]) / max(1e-3, b[0] - a[0]))
            return tuple(a[i] + (b[i] - a[i]) * u for i in (1, 2, 3))
    return ks[-1][1:]


def in_globe(t):
    return any(a <= t < b for a, b in SCN)


# ------------------------------------------------------------------ new overlays
def smooth_path(pts, n=14):
    """Catmull-Rom through geo waypoints -> dense list."""
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            u = k / n
            out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * u + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * u * u
                                    + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * u ** 3) for c in (0, 1)))
    out.append(P[-2])
    return out


def path_screen(v, geo):
    """-> list of (x, y, visible) for a dense geo path."""
    if isinstance(v, GlobeView):
        return [(*v.xy(lo, la), v.vis(lo, la)) for lo, la in geo]
    return [(*v.xy(lo, la), True) for lo, la in geo]


def arrow(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    geo = o.setdefault("_geo", smooth_path(o["pts"]))
    sp = path_screen(v, geo)
    k = ease((t - o["t0"]) / o.get("dur", 1.4))
    n = max(2, int(len(sp) * k))
    seg, cur = [], []
    for x, y, vis in sp[:n]:
        if vis:
            cur.append((x, y))
        elif cur:
            seg.append(cur)
            cur = []
    if cur:
        seg.append(cur)
    a = clamp((o["t1"] - t) / 0.25)
    w = o.get("w", 14)
    col = o.get("col", (255, 30, 39))
    lay = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    for s_ in seg:
        if len(s_) > 1:
            dl.line([(x / 4, y / 4) for x, y in s_], fill=col + (200,), width=max(3, w // 2), joint="curve")
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    for s_ in seg:
        if len(s_) > 1:
            d.line(s_, fill=(0, 0, 0, int(150 * a)), width=w + 10, joint="curve")
            d.line(s_, fill=WHT + (int(255 * a),), width=w + 5, joint="curve")
            d.line(s_, fill=col + (int(255 * a),), width=w, joint="curve")
    if (k < 1 or o.get("keephead")) and seg and len(seg[-1]) > 2 and sp[min(n, len(sp)) - 1][2]:
        (x1, y1), (x0, y0) = seg[-1][-1], seg[-1][-3]
        ang = math.atan2(y1 - y0, x1 - x0)
        L = w * 3.4
        tip = (x1 + math.cos(ang) * L * 0.55, y1 + math.sin(ang) * L * 0.55)
        base = [(x1 + math.cos(ang + 2.5) * L * 0.8, y1 + math.sin(ang + 2.5) * L * 0.8),
                (x1 + math.cos(ang - 2.5) * L * 0.8, y1 + math.sin(ang - 2.5) * L * 0.8)]
        d.polygon([tip] + base, fill=col + (int(255 * a),), outline=WHT + (int(255 * a),))
        d.line([tip, base[0], base[1], tip], fill=WHT + (int(255 * a),), width=4, joint="curve")


def boat_sprite(sz):
    key = ("boat", int(sz))
    if key not in _GL:
        c = Image.new("RGBA", (120, 96), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        d.polygon([(8, 56), (112, 56), (96, 84), (24, 84)], fill=(255, 215, 0, 255), outline=(10, 10, 14, 255))
        d.line([(60, 56), (60, 10)], fill=(10, 10, 14, 255), width=6)
        d.polygon([(64, 14), (64, 50), (100, 50)], fill=(255, 255, 255, 255), outline=(10, 10, 14, 255))
        d.line([(8, 56), (112, 56), (96, 84), (24, 84), (8, 56)], fill=(10, 10, 14, 255), width=5, joint="curve")
        _GL[key] = c.resize((int(sz), int(sz * 0.8)), Image.LANCZOS)
    return _GL[key]


def units(img, v, o, t):
    """Boats (or riders) travelling along the route path."""
    if t < o["t0"] or t > o["t1"]:
        return
    geo = o.setdefault("_geo", smooth_path(o["pts"]))
    sp = path_screen(v, geo)
    u = ease((t - o["t0"]) / o.get("dur", 1.4))
    a = clamp((o["t1"] - t) / 0.25) * clamp((t - o["t0"]) / 0.15)
    sprite = boat_sprite(o.get("size", 70))
    for i in range(o.get("n", 4)):
        uu = u - i * o.get("gap", 0.018)
        if uu < 0:
            continue
        j = min(len(sp) - 1, int(uu * (len(sp) - 1)))
        x, y, vis = sp[j]
        if not vis:
            continue
        bob = math.sin(t * 5 + i * 1.7) * 4
        sp_ = sprite.copy()
        if a < 1:
            sp_.putalpha(sp_.getchannel("A").point(lambda q: int(q * a)))
        img.alpha_composite(sp_, (int(x - sp_.width / 2 + (i % 2) * 8), int(y - sp_.height + bob + (i % 2) * 6)))


def fort(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.35)
    a = clamp((o["t1"] - t) / 0.25)
    X, Y = v.xy(o["lon"], o["lat"])
    d = ImageDraw.Draw(img)
    pr = clamp((t - o["t0"]) / 0.7)
    if pr < 1:
        r = 20 + 90 * pr
        d.ellipse((X - r, Y - r, X + r, Y + r), outline=(255, 215, 0, int(230 * (1 - pr))), width=5)
    s_ = o.get("s", 1.0) * k
    if s_ > 0.05:
        poly = [(-26, 0), (-26, -30), (0, -52), (26, -30), (26, 0)]
        poly = [(X + px * s_, Y + py * s_) for px, py in poly]
        d.polygon(poly, fill=(150, 98, 52, int(255 * a)), outline=WHT + (int(255 * a),))
        d.line(poly + [poly[0]], fill=WHT + (int(255 * a),), width=4, joint="curve")
        for dx in (-13, 0, 13):
            d.line((X + dx * s_, Y, X + dx * s_, Y - 26 * s_), fill=(70, 44, 20, int(255 * a)), width=3)
        d.polygon([(X - 6 * s_, Y - 52 * s_), (X + 20 * s_, Y - 62 * s_), (X - 6 * s_, Y - 72 * s_)], fill=(255, 30, 39, int(255 * a)))
        d.line((X - 6 * s_, Y - 52 * s_, X - 6 * s_, Y - 78 * s_), fill=WHT + (int(255 * a),), width=3)
    lab = text_layer(o["txt"], font(OSWB, o.get("size", 54)), WHT, 3, True, a)
    side = o.get("side", 1)
    put(img, lab, X + side * (lab.width / 2 + 38), Y - 30, k)
    if o.get("year"):
        yl = text_layer(str(o["year"]), font(OSWB, o.get("size", 54) * 0.82), (255, 214, 0), 3, True, a)
        put(img, yl, X + side * (lab.width / 2 + 38), Y + 18, k)


def flame(d, X, Y, h, ph, a):
    w = h * 0.42
    for scale, col in ((1.0, (230, 40, 20)), (0.75, (255, 130, 20)), (0.45, (255, 220, 60))):
        hh, ww = h * scale, w * scale
        sway = math.sin(ph * 9 + scale * 3) * ww * 0.35
        pts = [(X - ww, Y), (X - ww * 1.05, Y - hh * 0.35), (X - ww * 0.5, Y - hh * 0.7), (X + sway, Y - hh),
               (X + ww * 0.6, Y - hh * 0.65), (X + ww * 1.05, Y - hh * 0.3), (X + ww, Y)]
        d.polygon(pts, fill=col + (int(235 * a),))


def fire(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.3) * clamp((t - o["t0"]) / 0.12)
    X, Y = v.xy(o["lon"], o["lat"])
    d = ImageDraw.Draw(img)
    h = o.get("h", 120) * back((t - o["t0"]) / 0.4)
    for dx in (-0.55, 0.0, 0.5):
        flame(d, X + dx * h * 0.55, Y, h * (1.0 if dx == 0 else 0.7), t + dx, a)


def banner(img, v, o, t):
    """Top plaque: red pill (year / word, odometer roll) + dark banner (name) + season icon, like the reference."""
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.3) * clamp((o["t1"] - t) / 0.2)
    if k <= 0.02:
        return
    y = 108 - (1 - clamp(k)) * 140
    pill = o["pill"]
    if isinstance(pill, tuple):
        val = pill[0] + (pill[1] - pill[0]) * ease((t - o["t0"]) / o.get("roll", 0.55))
        pill = f"{val:.0f}"
    fp, fn_ = font(OSWB, 64), font(OSWB, 56)
    pw = max(190, fp.getlength(pill) + 70)
    nw = fn_.getlength(o["name"]) + 120
    x0 = 540 - (pw + nw) / 2
    lay = Image.new("RGBA", (int(pw + nw + 20), 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((10, 10, 10 + pw, 100), 24, fill=(226, 24, 30, 255), outline=WHT + (255,), width=4)
    d.rounded_rectangle((10 + pw - 18, 10, 10 + pw + nw, 100), 24, fill=(14, 20, 28, 235), outline=WHT + (255,), width=4)
    d.rounded_rectangle((10 + pw - 18, 10, 10 + pw + 6, 100), 8, fill=(226, 24, 30, 255))
    d.text((10 + pw / 2, 57), pill, font=fp, fill=WHT + (255,), anchor="mm")
    d.text((10 + pw + 28 + (nw - 120) / 2 + 20, 57), o["name"], font=fn_, fill=WHT + (255,), anchor="mm")
    ic = o.get("icon")
    cx, cy = 10 + pw + nw - 44, 55
    if ic == "snow":
        for ang in (0, 60, 120):
            dx, dy = math.cos(math.radians(ang)) * 24, math.sin(math.radians(ang)) * 24
            d.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=(170, 220, 255, 255), width=5)
    elif ic == "sun":
        d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(255, 214, 0, 255))
        for ang in range(0, 360, 45):
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line((cx + dx * 16, cy + dy * 16, cx + dx * 25, cy + dy * 25), fill=(255, 214, 0, 255), width=4)
    put(img, lay, x0 + lay.width / 2 - 10, y + 50, 1.0)


def stamp(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    dt = t - o["t0"]
    k = 1.0 + 0.9 * clamp(1 - dt / 0.16)
    a = clamp((o["t1"] - t) / 0.2)
    f = fit(OSWB, o.get("size", 118), o["txt"], 900)
    tw = f.getlength(o["txt"])
    lay = Image.new("RGBA", (int(tw + 120), int(f.size * 1.45)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    col = o.get("col", (214, 20, 28))
    d.rounded_rectangle((6, 6, lay.width - 6, lay.height - 6), 16, outline=col + (int(255 * a),), width=10, fill=(0, 0, 0, int(120 * a)))
    d.text((lay.width / 2, lay.height / 2 + 4), o["txt"], font=f, fill=col + (int(255 * a),), anchor="mm", stroke_width=3, stroke_fill=WHT + (int(255 * a),))
    X, Y = (o["x"], o["y"]) if "x" in o else v.xy(o["lon"], o["lat"])
    put(img, lay, X, Y, k, o.get("angle", -6))


def thermo(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.35) * clamp((o["t1"] - t) / 0.25)
    val = o["v0"] + (o["v1"] - o["v0"]) * ease((t - o["t0"] - 0.2) / o.get("dur", 1.6))
    x, y0, hgt = o.get("x", 150), o.get("y", 520), 640
    lay = Image.new("RGBA", (320, hgt + 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((10, 10, 310, hgt + 210), 28, fill=(8, 14, 22, 205), outline=WHT + (255,), width=3)
    tx0, tx1, ty0, ty1 = 80, 140, 40, 40 + hgt - 70
    d.rounded_rectangle((tx0, ty0, tx1, ty1 + 60), 30, fill=(30, 40, 52, 255), outline=WHT + (255,), width=4)
    frac = clamp((val + 70) / 100.0)
    my = ty1 - frac * (ty1 - ty0 - 10)
    col = (255, 60, 50) if val > 0 else (90, 200, 255)
    d.rounded_rectangle((tx0 + 12, my, tx1 - 12, ty1 + 50), 18, fill=col + (255,))
    d.ellipse((tx0 - 14, ty1 + 10, tx1 + 14, ty1 + 100), fill=col + (255,), outline=WHT + (255,), width=4)
    for tv in range(-60, 21, 20):
        yy = ty1 - clamp((tv + 70) / 100.0) * (ty1 - ty0 - 10)
        d.line((tx1 + 8, yy, tx1 + 34, yy), fill=WHT + (255,), width=3)
        d.text((tx1 + 42, yy), f"{tv}", font=font(OSW, 34), fill=WHT + (255,), anchor="lm")
    d.text((160, hgt + 150), f"{val:.0f}°C".replace("-", "−"), font=font(OSWB, 84), fill=col + (255,), anchor="mm", stroke_width=3, stroke_fill=BLK + (255,))
    put(img, lay, x + 10, y0 + lay.height / 2, k)


def hudcard(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    k = clamp((t - o["t0"]) / 0.3) * clamp((o["t1"] - t) / 0.25)
    rows = o["rows"]
    rh = 96
    hh = 120 + rh * len(rows)
    lay = Image.new("RGBA", (900, hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((4, 4, 896, hh - 4), 30, fill=(8, 14, 22, int(215 * k)), outline=WHT + (int(255 * k),), width=3)
    d.text((450, 56), o["title"], font=font(OSWB, 58), fill=(255, 214, 0, int(255 * k)), anchor="mm")
    for i, (txt, val, frac, col) in enumerate(rows):
        dt = t - o["t0"] - 0.35 - i * 0.28
        if dt < 0:
            continue
        p = ease(dt / 0.55)
        y = 120 + i * rh + rh / 2 - 4
        d.text((36, y - 26), txt, font=font(OSWB, 42), fill=WHT + (255,), anchor="lm")
        d.text((864, y - 26), val, font=font(OSWB, 42), fill=col + (255,), anchor="rm")
        d.rounded_rectangle((36, y + 4, 864, y + 30), 13, fill=(40, 52, 66, 255))
        if frac * p > 0.01:
            d.rounded_rectangle((36, y + 4, 36 + 828 * frac * p, y + 30), 13, fill=col + (255,))
    put(img, lay, o.get("x", 540), o.get("y", 960), 1.0)


def rivers(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    a = fade(o, t, 0.5, 0.3)
    d = ImageDraw.Draw(img)
    for nm in o["names"]:
        for ln in RIVERS.get(nm, []):
            p = v.pts(ln[:: o.get("step", 2)])
            xs = [q[0] for q in p]
            ys = [q[1] for q in p]
            if max(xs) < -50 or min(xs) > W + 50 or max(ys) < -50 or min(ys) > H + 50:
                continue
            d.line(p, fill=(150, 225, 255, int(255 * a)), width=o.get("w", 6), joint="curve")


def snowfall(img, t, f):
    if f < 0.25:
        return
    n = int(160 * f)
    rng = np.random.default_rng(7)
    xs = rng.uniform(0, W, n)
    ys = rng.uniform(0, H, n)
    sp = rng.uniform(90, 220, n)
    sz = rng.uniform(2.5, 6.5, n)
    ph = rng.uniform(0, 6.28, n)
    d = ImageDraw.Draw(img)
    for i in range(n):
        x = (xs[i] + math.sin(t * 1.4 + ph[i]) * 30) % W
        y = (ys[i] + t * sp[i]) % H
        d.ellipse((x - sz[i], y - sz[i], x + sz[i], y + sz[i]), fill=(255, 255, 255, 200))


_label0 = label


def label(img, v, o, t):
    if "lon" in o and not isinstance(v, GlobeView) and t >= o["t0"]:
        X, Y = v.xy(o["lon"], o["lat"])
        w_ = font(o.get("font", OSW), o.get("size", 60) * (1.2 if o.get("font", OSW) == OSW else 1.0)).getlength(o["txt"]) / 2 + 24
        if X < w_ or X > W - w_:
            o2 = dict(o)
            o2.pop("lon"); o2.pop("lat")
            o2["x"], o2["y"] = min(max(X, w_), W - w_), Y
            return _label0(img, v, o2, t)
    return _label0(img, v, o, t)


DRAW.update({"label": label, "arrow": arrow, "units": units, "fort": fort, "fire": fire, "banner": banner, "stamp": stamp, "thermo": thermo,
             "hudcard": hudcard, "rivers": rivers})
ORDER = ["fill", "rivers", "arrow", "units", "fort", "fire", "pin", "curved", "label", "counter", "stamp", "thermo", "hudcard", "banner"]



# ================================================================== v65 additions (time zones Short)
def chips(img, v, o, t):
    """Rounded chips that pop in one by one (UTC offsets, clocks). items: [(text, colour)], grid of `cols` per row, centred at x, y."""
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.25)
    items, cols, f = o["items"], o.get("cols", len(o["items"])), font(OSWB, o.get("size", 44))
    rh, gap = o.get("rh", 84), o.get("gap", 14)
    rows = [items[i:i + cols] for i in range(0, len(items), cols)]
    n = 0
    for ri, row in enumerate(rows):
        ws = [f.getlength(s_) + 44 for s_, _ in row]
        x = o["x"] - (sum(ws) + gap * (len(row) - 1)) / 2
        for (s_, col), w_ in zip(row, ws):
            ti = o["t0"] + n * o.get("per", 0.25)
            n += 1
            if t >= ti:
                k = back((t - ti) / 0.3) * a
                lay = Image.new("RGBA", (int(w_ + 20), int(rh - 6)), (0, 0, 0, 0))
                d = ImageDraw.Draw(lay)
                d.rounded_rectangle((6, 6, lay.width - 6, lay.height - 6), 18, fill=(14, 20, 28, 240), outline=col + (255,), width=5)
                d.text((lay.width / 2, lay.height / 2 + 1), s_, font=f, fill=WHT + (255,), anchor="mm")
                put(img, lay, x + w_ / 2, o["y"] + ri * rh, max(0.01, k))
            x += w_ + gap


def ring(img, v, o, t):
    """Pulsing marker ring on a place."""
    if t < o["t0"] or t > o["t1"]:
        return
    if isinstance(v, GlobeView) and not v.vis(o["lon"], o["lat"]):
        return
    X, Y = v.xy(o["lon"], o["lat"])
    k = clamp((t - o["t0"]) / 0.3)
    a = clamp((o["t1"] - t) / 0.25)
    r0 = o.get("r", 24)
    ph = ((t - o["t0"]) * 1.1) % 1.0
    S = int(r0 * 4)
    lay = Image.new("RGBA", (S * 2, S * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    col = o.get("col", YEL)
    rr = r0 * k
    d.ellipse((S - rr, S - rr, S + rr, S + rr), outline=col + (int(255 * a),), width=6)
    pr = r0 * (1 + ph * 1.5)
    d.ellipse((S - pr, S - pr, S + pr, S + pr), outline=col + (int(200 * a * (1 - ph)),), width=4)
    d.ellipse((S - 6, S - 6, S + 6, S + 6), fill=WHT + (int(255 * a * k),))
    img.alpha_composite(lay, (int(X - S), int(Y - S)))


DRAW.update({"chips": chips, "ring": ring})
ORDER = ["fill", "rivers", "arrow", "units", "fort", "fire", "ring", "pin", "curved", "label", "counter", "chips", "stamp", "thermo", "hudcard", "banner"]


# ================================================================== v66 additions: reference look (space plate with dust, isometric map opening,
# neon tracked title, red triangle markers, magnifier, red X)
def dust_plate(tt):
    """Drifting soft dust specks on the space plate (outside the globe only: it is added to the background array)."""
    g = globe_assets()
    pl = np.zeros((H, W, 3), np.float32)
    for x0, y0, sz, ph in g["dust"]:
        x = (x0 * W + 18 * tt * (0.4 + ph)) % W
        y = (y0 * H - 11 * tt * (0.3 + sz)) % H
        r_ = 2 + int(sz * 4)
        a = 26 + 40 * sz * (0.6 + 0.4 * math.sin(tt * 1.3 + ph * 6))
        xi, yi = int(x), int(y)
        pl[max(0, yi - r_):yi + r_, max(0, xi - r_):xi + r_] += np.array([a * 0.6, a, a], np.float32)
    return pl


ISOS = []


def ISO(t0, t1):
    ISOS.append((t0, t1))


def in_iso(t):
    return any(a <= t < b for a, b in ISOS)


_ISOW = {}
IW, IH = 1700, 850


def _fwd(quad, rect):
    c = persp_coeffs(quad, rect)                       # maps rect points (output) to quad points (input): flat -> screen

    def f(x, y):
        den = c[6] * x + c[7] * y + 1.0
        return (c[0] * x + c[1] * y + c[2]) / den, (c[3] * x + c[4] * y + c[5]) / den
    return f


ISO_PINS = []        # (t, lon, lat, label, sub)


def iso_frame(t):
    """Opening: flat world map tilts into an isometric view in deep space; white pins rise from the candidate countries."""
    g = globe_assets()
    if "map" not in _ISOW:
        _ISOW["map"] = sat("WLD").resize((IW, IH), Image.BILINEAR).convert("RGBA")
    base = Image.fromarray(np.clip(g["stars"] + dust_plate(t), 0, 255).astype(np.uint8)).convert("RGBA")
    q = ease(t / 0.9)
    cx, cy = 540, 1000
    hb = 540 * (1.0 - 0.06 * q) * (1.0 + 0.03 * t)
    ht = hb * (1 - 0.38 * q)
    hh = hb * IH / IW * (1 - 0.30 * q)
    quad0 = [(-ht, -hh), (ht, -hh), (hb, hh), (-hb, hh)]
    a = math.radians(-12 * q)
    quad = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in quad0]
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + 12, y + 30) for x, y in quad], fill=(0, 0, 0, 150))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
    base.alpha_composite(_ISOW["map"].transform((W, H), Image.PERSPECTIVE, persp_coeffs([(0, 0), (IW, 0), (IW, IH), (0, IH)], quad), Image.BILINEAR))
    ImageDraw.Draw(base).line(quad + [quad[0]], fill=(120, 225, 255, 255), width=4, joint="curve")
    fw = _fwd(quad, [(0, 0), (IW, 0), (IW, IH), (0, IH)])
    d = ImageDraw.Draw(base)
    for (tp, lon, lat, lab, col) in ISO_PINS:
        if t < tp:
            continue
        X, Y = fw((lon + 180) / 360 * IW, (90 - lat) / 180 * IH)
        L = 230 * ease((t - tp) / 0.5)
        d.line((X, Y, X, Y - L), fill=(255, 255, 255, 255), width=5)
        d.ellipse((X - 9, Y - 9, X + 9, Y + 9), fill=(255, 255, 255, 255))
        if L > 120:
            put(base, text_layer(lab, font(OSWB, 64), col, 3, True, 1.0), X, Y - L - 36, back((t - tp - 0.3) / 0.3))
    return base


def neon(img, v, o, t):
    """Big tracked title, white with blue outline and a cyan glow (reference: 3D tracked typography)."""
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.25)
    f = fit(MB, o.get("size", 96), o["txt"], 900)
    tr = o.get("track", 10)
    ws = [f.getlength(c) for c in o["txt"]]
    tw = sum(ws) + tr * (len(ws) - 1)
    lay = Image.new("RGBA", (int(tw + 120), int(f.size * 1.6)), (0, 0, 0, 0))
    gl = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    x = 60
    for c, w_ in zip(o["txt"], ws):
        ImageDraw.Draw(gl).text((x, lay.height / 2), c, font=f, fill=(60, 190, 255, 255), anchor="lm", stroke_width=6, stroke_fill=(30, 120, 255, 255))
        ImageDraw.Draw(lay).text((x, lay.height / 2), c, font=f, fill=WHT + (255,), anchor="lm", stroke_width=3, stroke_fill=(20, 80, 220, 255))
        x += w_ + tr
    out = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    out.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10)))
    out.alpha_composite(lay)
    if a < 1:
        out.putalpha(out.getchannel("A").point(lambda q_: int(q_ * a)))
    X, Y = (o["x"], o["y"]) if "x" in o else v.xy(o["lon"], o["lat"])
    put(img, out, X, Y, back((t - o["t0"]) / 0.35), o.get("angle", 0))


def tri(img, v, o, t):
    """Red triangle marker with a dark name plate (reference: red summit triangle + label)."""
    if t < o["t0"] or t > o["t1"]:
        return
    if isinstance(v, GlobeView) and not v.vis(o["lon"], o["lat"]):
        return
    k = back((t - o["t0"]) / 0.35)
    a = clamp((o["t1"] - t) / 0.25)
    X, Y = v.xy(o["lon"], o["lat"])
    lay = Image.new("RGBA", (420, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.polygon([(210, 150), (172, 214), (248, 214)], fill=(226, 24, 30, int(255 * a)), outline=WHT + (int(255 * a),))
    f = font(OSWB, o.get("size", 52))
    tw = f.getlength(o["txt"]) + 44
    d.rounded_rectangle((210 - tw / 2, 60, 210 + tw / 2, 132), 16, fill=(14, 20, 28, int(235 * a)), outline=WHT + (int(255 * a),), width=3)
    d.text((210, 97), o["txt"], font=f, fill=WHT + (int(255 * a),), anchor="mm")
    put(img, lay, X, Y - 60, k)


def xmark(img, v, o, t):
    """Big red X (error badge)."""
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.3)
    a = clamp((o["t1"] - t) / 0.2)
    S = 280
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for w_, col in ((44, WHT), (30, (226, 24, 30))):
        d.line((50, 50, S - 50, S - 50), fill=col + (int(255 * a),), width=w_, joint="curve")
        d.line((S - 50, 50, 50, S - 50), fill=col + (int(255 * a),), width=w_, joint="curve")
    put(img, lay, o["x"], o["y"], k, o.get("angle", 0))


def lens(img, v, o, t):
    """Magnifying glass that sweeps in and locks onto a place (reference: lens sweeping to Everest)."""
    if t < o["t0"] or t > o["t1"]:
        return
    if isinstance(v, GlobeView) and not v.vis(o["lon"], o["lat"]):
        return
    X, Y = v.xy(o["lon"], o["lat"])
    k = ease((t - o["t0"]) / o.get("dur", 0.9))
    a = clamp((o["t1"] - t) / 0.25)
    cx, cy = X + o.get("dx", -380) * (1 - k), Y + o.get("dy", -240) * (1 - k)
    r_ = o.get("r", 120) * (1 + 0.06 * math.sin(t * 7) * k)
    S = int(r_ * 3)
    lay = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c0 = S / 2
    d.line((c0 + r_ * 0.72, c0 + r_ * 0.72, c0 + r_ * 1.35, c0 + r_ * 1.35), fill=(30, 36, 48, int(255 * a)), width=26)
    d.line((c0 + r_ * 0.72, c0 + r_ * 0.72, c0 + r_ * 1.35, c0 + r_ * 1.35), fill=(190, 200, 215, int(255 * a)), width=14)
    d.ellipse((c0 - r_, c0 - r_, c0 + r_, c0 + r_), fill=(255, 255, 255, int(38 * a)), outline=(235, 240, 250, int(255 * a)), width=14)
    d.ellipse((c0 - r_ + 12, c0 - r_ + 12, c0 + r_ - 12, c0 + r_ - 12), outline=(60, 60, 70, int(160 * a)), width=3)
    img.alpha_composite(lay, (int(cx - c0), int(cy - c0)))


DRAW.update({"neon": neon, "tri": tri, "xmark": xmark, "lens": lens})
ORDER = ["fill", "rivers", "arrow", "units", "fort", "fire", "ring", "pin", "tri", "lens", "curved", "label", "neon", "counter", "chips", "xmark", "stamp", "thermo", "hudcard", "banner"]

# ------------------------------------------------------------------ build
# ================================================================== v68 additions (Maldives Short, reference jTJ2UFF3B0I):
# pseudo-drone oblique camera over satellite imagery (tilt + orbit + push-in), single white text hook with thin shadow, no overlays/SFX
OBK = []        # (t, lon, lat, span, tilt, rot, cut, lin)
OBS = []        # (t0, t1) oblique scenes
HOOK = []       # (t0, t1, [lines], flag)


def OB(t, lon, lat, span, tilt=0.0, rot=0.0, cut=False, lin=False):
    OBK.append((t, lon, lat, span, tilt, rot, cut, lin))


def OBL(t0, t1):
    OBS.append((t0, t1))


def in_obl(t):
    return any(a <= t < b for a, b in OBS)


def obl_cam(t):
    ks = sorted(OBK, key=lambda k: k[0])
    if t <= ks[0][0]:
        return ks[0][1:6]
    for a, b in zip(ks, ks[1:]):
        if a[0] <= t < b[0]:
            if b[6]:
                return a[1:6]
            u = (t - a[0]) / max(1e-3, b[0] - a[0])
            u = u if b[7] else ease(u)
            span = math.exp(math.log(a[3]) + (math.log(b[3]) - math.log(a[3])) * u)
            return (a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, span, a[4] + (b[4] - a[4]) * u, a[5] + (b[5] - a[5]) * u)
    return ks[-1][1:6]


SRC_K = 2.3                       # source canvas = SRC_K x the screen, same pixels per degree as the screen


def obl_frame(t):
    """Oblique 'drone' look from a flat satellite image: render a big top-down canvas, then rotate and warp a trapezoid
    (far edge wider and taller = foreshortening) onto the screen."""
    lon, lat, span, tilt, rot = obl_cam(t)
    sw, sh = int(W * SRC_K) // 2 * 2, int(H * SRC_K) // 2 * 2
    v = View(lon, lat, span * SRC_K, sw, sh)
    vc = View(lon, lat, span * (1 + 1.3 * tilt) * 1.15)            # coverage test on the visible trapezoid only (not the whole canvas)
    ok = [k for k in MAP_KEYS if covers(k, vc)] or ["WLD"]
    src = crop(ok[0], v).convert("RGBA")
    if src.mode != "RGBA":
        src = src.convert("RGBA")
    c = (sw / 2, sh / 2)
    hwb, hwt = 540 * (1 - 0.30 * tilt), 540 * (1 + 1.1 * tilt)
    hb, ht = 960 * (1 - 0.25 * tilt), 960 * (1 + 1.3 * tilt)
    quad = [(-hwt, -ht), (hwt, -ht), (hwb, hb), (-hwb, hb)]
    a = math.radians(rot)
    pts = [(c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)) for x, y in quad]
    co = persp_coeffs(pts, [(0, 0), (W, 0), (W, H), (0, H)])
    return src.transform((W, H), Image.PERSPECTIVE, co, Image.BICUBIC)


def obl_overflow(t):
    """Largest distance (px) by which the warped quad leaves the source canvas (0 = fully inside)."""
    lon, lat, span, tilt, rot = obl_cam(t)
    sw, sh = W * SRC_K, H * SRC_K
    hwb, hwt = 540 * (1 - 0.30 * tilt), 540 * (1 + 1.1 * tilt)
    hb, ht = 960 * (1 - 0.25 * tilt), 960 * (1 + 1.3 * tilt)
    a = math.radians(rot)
    m = 0.0
    for x, y in [(-hwt, -ht), (hwt, -ht), (hwb, hb), (-hwb, hb)]:
        X, Y = sw / 2 + x * math.cos(a) - y * math.sin(a), sh / 2 + x * math.sin(a) + y * math.cos(a)
        m = max(m, -X, X - sw, -Y, Y - sh)
    return m


BLEND = []      # (t0, t1) crossfade window from the globe to the flat map


def hook_text(img, t):
    """The reference text: ONE white sans-serif block at the top, thin soft shadow, no outline, no glow, visible ~3 s, then gone."""
    for (t0, t1, lines, flag) in HOOK:
        if not (t0 <= t < t1):
            continue
        a = clamp((t - t0) / 0.18) * clamp((t1 - t) / 0.25)
        f = font(MX, 62)
        y = 250
        for ln in lines:
            lay = Image.new("RGBA", (1000, 110), (0, 0, 0, 0))
            sh = Image.new("RGBA", (1000, 110), (0, 0, 0, 0))
            ImageDraw.Draw(sh).text((503, 58), ln, font=f, fill=(0, 0, 0, int(235 * a)), anchor="mm")
            lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
            ImageDraw.Draw(lay).text((500, 55), ln, font=f, fill=(255, 255, 255, int(255 * a)), anchor="mm")
            img.alpha_composite(lay, (40, y - 55))
            y += 84
        if flag and str(flag).startswith("EMOJI:"):            # colour emoji right after the last line (reference: text + emoji)
            em = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
            ImageDraw.Draw(em).text((4, 4), flag[6:], font=ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 109), embedded_color=True)
            em = em.crop(em.getbbox()).resize((62, 62), Image.LANCZOS)
            if a < 1:
                em.putalpha(em.getchannel("A").point(lambda q_: int(q_ * a)))
            lw = f.getlength(lines[-1])
            img.alpha_composite(em, (int(540 + lw / 2 + 12), int(y - 84 - 31)))
        elif flag:
            fl = Image.new("RGBA", (96, 64), (0, 0, 0, 0))
            d = ImageDraw.Draw(fl)
            A = int(255 * a)
            if flag == "NO":
                d.rounded_rectangle((0, 0, 95, 63), 8, fill=(186, 12, 47, A))
                d.rectangle((0, 24, 95, 40), fill=(255, 255, 255, A))
                d.rectangle((26, 0, 42, 63), fill=(255, 255, 255, A))
                d.rectangle((0, 28, 95, 36), fill=(0, 32, 91, A))
                d.rectangle((30, 0, 38, 63), fill=(0, 32, 91, A))
            img.alpha_composite(fl, (540 - 48, y + 4))


_CLOUD = {}


def cloud_layer(t):
    """Google-Earth-like pass through a cloud deck during the dive: soft fractal clouds that grow (camera falls through them) and fade."""
    if not (0.75 <= t < 1.75):
        return None
    if "c" not in _CLOUD:
        rng = np.random.default_rng(11)
        acc = np.zeros((480, 270), np.float32)
        for k, amp in ((6, 1.0), (12, 0.5), (24, 0.25), (48, 0.12)):
            g = rng.random((k * 16 // 9 + 2, k + 2)).astype(np.float32)
            acc += amp * cv2.resize(g, (270, 480), interpolation=cv2.INTER_CUBIC)
        acc = (acc - acc.min()) / (acc.max() - acc.min())
        al = np.clip((acc - 0.45) / 0.3, 0, 1)
        rgba = np.dstack([np.full_like(al, 245), np.full_like(al, 248), np.full_like(al, 252), al * 255]).astype(np.uint8)
        _CLOUD["c"] = Image.fromarray(rgba, "RGBA").resize((W * 2, H * 2), Image.BICUBIC)
    u = (t - 0.75) / 1.0
    sc = 0.55 * math.exp(2.4 * u)                       # grows as we fall through
    a = math.sin(math.pi * u) * 0.9
    c = _CLOUD["c"]
    w, h = int(c.width * sc), int(c.height * sc)
    lay = c.resize((max(1, w), max(1, h)), Image.BILINEAR)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(lay, (int(W / 2 - w / 2), int(H / 2 - h / 2)) if w <= W else (0, 0), (0, 0) if w <= W else (int(w / 2 - W / 2), int(h / 2 - H / 2), int(w / 2 + W / 2), int(h / 2 + H / 2)))
    out.putalpha(out.getchannel("A").point(lambda q_: int(q_ * a)))
    return out


import shots69  # noqa: E402

shots69.build(SHORT, K, O, GK, GLOBE, OB, OBL, HOOK, ST, D, BLEND)
CUTS = sorted({k[0] for k in CAM if k[4]} | {a for a, b in SCN} | {b for a, b in SCN} | {b for a, b in ISOS} | {a for a, b in OBS} | {b for a, b in OBS})
SHAKES = sorted([o["t0"] for o in OV if o["kind"] == "stamp"] + [o["t0"] for o in OV if o.get("shake")])


def credit(img, extra=""):
    ImageDraw.Draw(img).text((W - 16, H - 12), "Imagery © Esri, Maxar, Earthstar Geographics · Natural Earth" + extra,
                             font=font(MX, 16), fill=(255, 255, 255, 150), anchor="rs")


def frame(fi):
    t = fi / FPS
    f = season(t)
    glob = in_globe(t) or in_iso(t)
    bw = next((b for b in BLEND if b[0] <= t < b[1]), None)
    if bw:                                                     # globe -> flat map handoff: short crossfade, matched scale
        u = ease((t - bw[0]) / (bw[1] - bw[0]))
        vg, vf = GlobeView(*globe_cam(t)), View(*camera(t))
        img = Image.blend(globe_img(vg, f, t), winterize(render_map64(vf), vf, f), u)
        v = vf
    elif in_obl(t):
        v = None
        img = obl_frame(t)
    elif in_iso(t):
        v = GlobeView(0, 0, 560)
        img = iso_frame(t)
    elif glob:
        v = GlobeView(*globe_cam(t))
        img = globe_img(v, f, t)
    else:
        v = View(*camera(t))
        img = winterize(render_map64(v), v, f)
    if in_obl(t):
        live = []
    else:
        live = [o for o in OV if o["t0"] - 0.01 <= t <= o["t1"] + 0.01 and (o.get("scene", "flat") in (("globe", "both") if glob else ("flat", "both")))]
    for kind in ORDER:
        for o in live:
            if o["kind"] == kind:
                DRAW[kind](img, v, o, t)
    if not glob:
        snowfall(img, t, f)
    credit(img)
    cl = cloud_layer(t) if SHORT == "lofoten" else None
    if cl is not None:
        img.alpha_composite(cl)
    caption(img, t)
    hook_text(img, t)
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    for fl in FLASH:
        if 0 <= t - fl < 0.16:
            arr = arr + (255 - arr) * (1 - (t - fl) / 0.16) * 0.8
    sk = 0.0
    for s_ in SHAKES:
        if 0 <= t - s_ < 0.28:
            sk = max(sk, 14 * (1 - (t - s_) / 0.28))
    dx, dy = int(sk * math.sin(t * 90)), int(sk * math.cos(t * 77))
    if dx or dy:
        arr = np.roll(arr, (dy, dx), axis=(0, 1))
    a = (np.clip(arr, 0, 255).astype(np.uint16) * (256 if SHORT == "lofoten" else VIG)) >> 8   # reference: no vignette
    return a.astype(np.uint8)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print(SHORT, "frames", NF, "total", round(TOTAL, 2), "keys", len(CAM), "overlays", len(OV), "cuts", [round(c, 2) for c in CUTS])
    elif cmd == "still":
        os.makedirs(f"{SHORT}/stills66", exist_ok=True)
        for a in sys.argv[2:]:
            Image.fromarray(frame(int(float(a) * FPS))).save(f"{SHORT}/stills66/{float(a):05.1f}.jpg", quality=86)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
        p.stdin.close()
        p.wait()
