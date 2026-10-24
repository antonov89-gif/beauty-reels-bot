"""Map Shorts engine v70: GeoGlobeTales-style remake engine (DNA of xGmyqt_Ild0), vertical 1080x1920 @30 fps.
Three camera modes on one timeline: GLOBE (orthographic, NASA Blue Marble shaded relief), FLAT (local equirectangular from
regional Blue Marble keys) and MERC (Web Mercator world, for the map-distortion beats). Overlays use v.xy(lon, lat), so the
same overlay works in every mode. Every overlay start is logged as a sound event (events.json) for audio70.py.
Run in /home/claude/v70:  SHORT=au python3 engine70.py info | still t.. | video A B out.mp4 | events"""
import json
import math
import os
import subprocess
import sys
from functools import lru_cache

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy.ndimage import map_coordinates

W, H, FPS = 1080, 1920, 30
A = "/home/claude/v62/assets/"
MB, MX, POP = A + "Montserrat-Black.ttf", A + "Montserrat-ExtraBold.ttf", A + "Poppins-ExtraBold.ttf"
WHT, BLK, YEL, RED, CYAN, GRN = (255, 255, 255), (0, 0, 0), (255, 214, 0), (229, 57, 53), (0, 229, 255), (60, 220, 90)
BLUE, ORANGE, PINK, LIME = (30, 136, 229), (255, 152, 0), (255, 64, 129), (200, 240, 0)

SHORT = os.environ.get("SHORT", "au")
sys.path.insert(0, os.environ.get("SHOTS_DIR", "/home/user/beauty-reels-bot/map_shorts/australia_continent_2026_10_25"))
import script  # noqa: E402

LINES = script.LINES
TM = json.load(open(f"{SHORT}/timing.json"))
LEAD = 0.05
ST = [LEAD + s for s in TM["starts"]]
D, TW = TM["D"], TM["T"]
TOTAL = ST[-1] + D[-1] + 0.9
NF = int(TOTAL * FPS)
_FONTS = {}


def font(path, sz):
    k = (path, int(sz))
    if k not in _FONTS:
        _FONTS[k] = ImageFont.truetype(path, int(sz))
    return _FONTS[k]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def back(x):
    x = clamp(x)
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


def clean(w):
    return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word, nth=0):
    """Absolute time of the nth occurrence of word in line i."""
    hits = [j for j, w in enumerate(LINES[i].split()) if clean(w) == clean(word)]
    return ST[i] + TW[i][hits[nth]]


# ------------------------------------------------------------------ geodata
def _shp(path, field, field2=None):
    r = shapefile.Reader(path)
    fl = [f[0] for f in r.fields[1:]]
    out, extra = {}, {}
    for sr in r.iterShapeRecords():
        rec = dict(zip(fl, sr.record))
        n = rec[field]
        pts = sr.shape.points
        parts = list(sr.shape.parts) + [len(pts)]
        out.setdefault(n, []).extend(np.array(pts[a:b]) for a, b in zip(parts[:-1], parts[1:]))
        if field2:
            extra[n] = rec[field2]
    return out, extra


COUNTRY, CONTINENT = _shp(A + "ne50/ne_50m_admin_0_countries.shp", "ADMIN", "CONTINENT")
CONT_RINGS = {}
for _n, _rs in COUNTRY.items():
    CONT_RINGS.setdefault(CONTINENT.get(_n), []).extend(_rs)
PLATE = {}
for _f in json.load(open("data/plates.json"))["features"]:
    _g = _f["geometry"]
    _polys = _g["coordinates"] if _g["type"] == "MultiPolygon" else [_g["coordinates"]]
    PLATE[_f["properties"]["Code"]] = [np.array(p[0]) for p in _polys]


def rings_of(o):
    if "plate" in o:
        return PLATE[o["plate"]]
    if "rings" in o:
        return o["rings"]
    return COUNTRY[o["name"]]


def big(rings, n=1):
    return sorted(rings, key=len)[-n:]


# ------------------------------------------------------------------ imagery
SAT = {"world": (-180, -90, 180, 90), "aus": (105, -48, 162, -6), "grl": (-80, 56, -5, 86), "nam": (-170, 5, -5, 86)}
TEAL = np.array([16, 44, 70], np.float32)


def grade(im):
    """Reference look: saturated relief, deep blue water, a touch of contrast."""
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    water = np.clip((b - r - 6) / 22, 0, 1)
    a = a * (1 - 0.35 * water[..., None]) + TEAL * 0.35 * water[..., None] * (0.7 + lum[..., None] / 150)
    m = a.mean(axis=2, keepdims=True)
    a = m + (a - m) * 1.25
    a = (a - 118) * 1.1 + 122
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


@lru_cache(maxsize=8)
def sat(key):
    p = f"sat/{key}_g.jpg"
    if not os.path.exists(p):
        grade(Image.open(f"sat/{key}.jpg")).save(p, quality=94)
    return Image.open(p).convert("RGB")


@lru_cache(maxsize=1)
def world_arr():
    return np.asarray(sat("world")).astype(np.float32)


MERC_PPD, MERC_LAT = 22.755, 82.0


def mY(lat):
    lat = max(-89.0, min(89.0, lat))
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


@lru_cache(maxsize=1)
def merc_world():
    """Web Mercator world (lon -180..180, lat +-82) resampled from the equirectangular world key."""
    p = "sat/world_merc.jpg"
    if os.path.exists(p):
        return Image.open(p).convert("RGB")
    src = world_arr()
    ym = mY(MERC_LAT)
    hh = int(2 * ym * MERC_PPD)
    ww = src.shape[1]
    Y = ym - (np.arange(hh) + 0.5) / MERC_PPD
    lat = np.degrees(2 * np.arctan(np.exp(np.radians(Y))) - math.pi / 2)
    rows = (90 - lat) / 180 * src.shape[0]
    out = src[np.clip(rows.astype(int), 0, src.shape[0] - 1)][:, :ww]
    im = Image.fromarray(out.astype(np.uint8))
    im.save(p, quality=93)
    return im


# ------------------------------------------------------------------ views
class Flat:
    mode = "flat"

    def __init__(self, lon, lat, span):
        self.lon, self.lat, self.span = lon, lat, span
        self.ppd = H / (2 * span)
        self.kx = self.ppd * math.cos(math.radians(lat))
        self.hw = (W / 2) / self.kx

    def xy(self, lon, lat):
        return W / 2 + (lon - self.lon) * self.kx, H / 2 - (lat - self.lat) * self.ppd

    def vis(self, lon, lat):
        return True

    def render(self):
        a0, a1, c0, c1 = self.lon - self.hw, self.lon + self.hw, self.lat - self.span, self.lat + self.span
        best = None
        for k, (l0, b0, l1, b1) in SAT.items():
            if k == "world":
                continue
            if a0 >= l0 and a1 <= l1 and c0 >= b0 and c1 <= b1:
                best = k
        k = best or "world"
        l0, b0, l1, b1 = SAT[k]
        im = sat(k)
        w, h = im.size
        box = ((a0 - l0) / (l1 - l0) * w, (b1 - c1) / (b1 - b0) * h, (a1 - l0) / (l1 - l0) * w, (b1 - c0) / (b1 - b0) * h)
        return im.resize((W, H), Image.BILINEAR, box=box, reducing_gap=2.0).convert("RGBA")


class Merc:
    mode = "merc"

    def __init__(self, lon, lat, ppd):
        self.lon, self.Y, self.ppd = lon, mY(lat), ppd

    def xy(self, lon, lat):
        return W / 2 + (lon - self.lon) * self.ppd, H / 2 - (mY(lat) - self.Y) * self.ppd

    def vis(self, lon, lat):
        return True

    def render(self):
        im = merc_world()
        w, h = im.size
        ym = mY(MERC_LAT)
        x0 = (self.lon - W / 2 / self.ppd + 180) * MERC_PPD
        x1 = (self.lon + W / 2 / self.ppd + 180) * MERC_PPD
        y0 = (ym - (self.Y + H / 2 / self.ppd)) * MERC_PPD
        y1 = (ym - (self.Y - H / 2 / self.ppd)) * MERC_PPD
        out = Image.new("RGB", (W, H), (8, 14, 30))
        cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(w, x1), min(h, y1)
        if cx1 > cx0 and cy1 > cy0:
            sx, sy = W / (x1 - x0), H / (y1 - y0)
            part = im.resize((max(1, int((cx1 - cx0) * sx)), max(1, int((cy1 - cy0) * sy))), Image.BILINEAR,
                             box=(cx0, cy0, cx1, cy1), reducing_gap=2.0)
            out.paste(part, (int((cx0 - x0) * sx), int((cy0 - y0) * sy)))
        return out.convert("RGBA")


_YY, _XX = np.mgrid[0:H, 0:W].astype(np.float32)
_rng = np.random.default_rng(7)
_STARS = [(int(_rng.uniform(0, W)), int(_rng.uniform(0, H)), _rng.uniform(0.6, 2.2), int(_rng.uniform(90, 230))) for _ in range(260)]


@lru_cache(maxsize=1)
def space_bg():
    g = (np.clip(1 - np.hypot(_XX - W / 2, _YY - H * 0.45) / 1500, 0, 1) ** 1.5)[..., None]
    a = np.array([4, 8, 22], np.float32) + g * np.array([18, 30, 70], np.float32)
    im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    for x, y, r, al in _STARS:
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, al))
    return im


class Globe:
    mode = "globe"

    def __init__(self, lon, lat, R, cy=H * 0.47):
        self.lon, self.lat, self.R, self.cx, self.cy = lon, lat, R, W / 2, cy
        self.f0, self.l0 = math.radians(lat), math.radians(lon)

    def _proj(self, lon, lat):
        f, l = math.radians(lat), math.radians(lon) - self.l0
        cosc = math.sin(self.f0) * math.sin(f) + math.cos(self.f0) * math.cos(f) * math.cos(l)
        x = self.R * math.cos(f) * math.sin(l)
        y = self.R * (math.cos(self.f0) * math.sin(f) - math.sin(self.f0) * math.cos(f) * math.cos(l))
        return x, y, cosc

    def xy(self, lon, lat):
        x, y, cosc = self._proj(lon, lat)
        if cosc < 0:                                              # hidden side: clamp to the limb
            n = math.hypot(x, y) or 1.0
            x, y = x / n * self.R, y / n * self.R
        return self.cx + x, self.cy - y

    def vis(self, lon, lat):
        return self._proj(lon, lat)[2] > 0.02

    def render(self):
        img = space_bg().copy()
        R = self.R
        x0, x1 = int(max(0, self.cx - R - 2)), int(min(W, self.cx + R + 2))
        y0, y1 = int(max(0, self.cy - R - 2)), int(min(H, self.cy + R + 2))
        if x1 > x0 and y1 > y0:
            X = (_XX[y0:y1, x0:x1] - self.cx) / R
            Y = (self.cy - _YY[y0:y1, x0:x1]) / R
            rho = np.hypot(X, Y)
            inside = rho < 1.0
            c = np.arcsin(np.clip(rho, 0, 1))
            sc, cc = np.sin(c), np.cos(c)
            rr = np.where(rho == 0, 1e-9, rho)
            phi = np.arcsin(np.clip(cc * math.sin(self.f0) + Y * sc * math.cos(self.f0) / rr, -1, 1))
            lam = self.l0 + np.arctan2(X * sc, rr * cc * math.cos(self.f0) - Y * sc * math.sin(self.f0))
            src = world_arr()
            hs, ws = src.shape[:2]
            row = (math.pi / 2 - phi) / math.pi * hs - 0.5
            col = (((np.degrees(lam) + 180) % 360) / 360 * ws - 0.5) % ws
            self.rc = (x0, y0, x1, y1, (row + 0.5) / hs, (col + 0.5) / ws, inside)        # normalised lat/lon per pixel, for mask fills
            rgb = np.stack([map_coordinates(src[..., k], [row, col], order=1, mode="nearest") for k in range(3)], -1)
            shade = (0.55 + 0.45 * np.clip(cc, 0, 1) ** 0.5)[..., None]                          # limb darkening
            rgb = rgb * shade
            a = (np.clip((1.0 - rho) * R / 1.5, 0, 1) * 255).astype(np.uint8)
            tile = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8)).convert("RGBA")
            tile.putalpha(Image.fromarray(np.where(inside, a, 0).astype(np.uint8)))
            # atmosphere halo
            halo = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0))
            hd = ImageDraw.Draw(halo)
            hr = R / 4
            hd.ellipse((self.cx / 4 - hr - 3, self.cy / 4 - hr - 3, self.cx / 4 + hr + 3, self.cy / 4 + hr + 3), outline=(90, 170, 255, 200), width=5)
            img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BILINEAR))
            img.alpha_composite(tile, (x0, y0))
        return img


# ------------------------------------------------------------------ camera: segments + keys per mode
SEG = []                         # (t0, t1, mode)
KEYS = {"globe": [], "flat": [], "merc": []}


def SEGMENT(t0, t1, mode):
    SEG.append((t0, t1, mode))


def K(mode, t, *p, lin=False):
    KEYS[mode].append((t, p, lin))


def cam(mode, t):
    ks = sorted(KEYS[mode], key=lambda k: k[0])
    if t <= ks[0][0]:
        p = ks[0][1]
    elif t >= ks[-1][0]:
        p = ks[-1][1]
    else:
        for a, b in zip(ks, ks[1:]):
            if a[0] <= t < b[0]:
                u = (t - a[0]) / max(1e-3, b[0] - a[0])
                u = u if b[2] else ease(u)
                p = [a[1][0] + (b[1][0] - a[1][0]) * u, a[1][1] + (b[1][1] - a[1][1]) * u,
                     math.exp(math.log(a[1][2]) + (math.log(b[1][2]) - math.log(a[1][2])) * u)]
                break
    return {"globe": Globe, "flat": Flat, "merc": Merc}[mode](*p)


def view_at(t):
    for s in SEG:
        if s[0] <= t < s[1]:
            return cam(s[2], t)
    return cam(SEG[-1][2], t)


# ------------------------------------------------------------------ text helpers
def text_layer(txt, f, col, stroke, shadow=True, a=1.0, stroke_col=BLK):
    bb = f.getbbox(txt, stroke_width=stroke)
    pad = 30
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    o = (pad - bb[0], pad - bb[1])
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((o[0] + 4, o[1] + 7), txt, font=f, fill=(0, 0, 0, int(170 * a)), stroke_width=stroke, stroke_fill=(0, 0, 0, int(170 * a)))
        lay.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(lay).text(o, txt, font=f, fill=col + (int(255 * a),), stroke_width=stroke, stroke_fill=stroke_col + (int(255 * a),))
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
OV = []


def O(kind, t0, t1=1e9, **kw):
    kw.update(kind=kind, t0=t0, t1=t1)
    OV.append(kw)
    return kw


def fade(o, t, fin=0.25, fout=0.25):
    return clamp((t - o["t0"]) / fin) * clamp((o["t1"] - t) / fout)


def pos(v, o, key="", default=(540, 500)):
    if (key + "lon") in o:
        return v.xy(o[key + "lon"], o[key + "lat"])
    return o.get(key + "xy", default)


def ring_pts(v, ring, sub=1):
    r = ring[::sub] if len(ring) > 400 else ring
    if v.mode == "flat":
        return [v.xy(lo, la) for lo, la in r]
    return [v.xy(lo, la) for lo, la in r]


def visible_rings(v, rings):
    out = []
    for r in rings:
        sub = max(1, len(r) // 500)
        if v.mode == "globe":
            vis = sum(1 for lo, la in r[::sub] if v.vis(lo, la))
            if vis < 0.2 * len(r[::sub]):
                continue
        if v.mode == "flat" and (np.ptp(r[:, 0]) > 300):
            continue
        p = ring_pts(v, r, sub)
        xs = [q[0] for q in p]
        ys = [q[1] for q in p]
        if len(p) < 3 or max(xs) < -400 or min(xs) > W + 400 or max(ys) < -400 or min(ys) > H + 400:
            continue
        out.append(p)
    return out


MW, MH = 4096, 2048
_MASKS = {}


def eq_mask(rings):
    """Polygon mask in equirectangular lon/lat space (cached), sampled by the globe per pixel: no limb artefacts."""
    k = (id(rings), len(rings))
    if k not in _MASKS:
        m = Image.new("L", (MW, MH), 0)
        d = ImageDraw.Draw(m)
        for r in rings:
            d.polygon([((lo + 180) / 360 * MW, (90 - la) / 180 * MH) for lo, la in r], fill=255)
        _MASKS[k] = np.asarray(m).astype(np.float32) / 255
    return _MASKS[k]


def globe_segments(v, rings):
    """Border polylines on the globe: only segments whose both ends are on the visible side."""
    out = []
    for r in rings:
        sub = max(1, len(r) // 700)
        cur = []
        prev = None
        prev_la = None
        for lo, la in r[::sub]:
            seam = prev is not None and ((abs(lo) > 179.9 and abs(prev) > 179.9) or (la > 89.5 and prev_la > 89.5) or (la < -89.5 and prev_la < -89.5))
            ok = v.vis(lo, la) and (prev is None or abs(lo - prev) < 90) and not seam
            prev, prev_la = lo, la
            if ok:
                cur.append(v.xy(lo, la))
            elif len(cur) > 1:
                out.append(cur)
                cur = []
            else:
                cur = []
        if len(cur) > 1:
            out.append(cur)
    return out


def fill_globe(img, v, o, t, a):
    rings = rings_of(o)
    x0, y0, x1, y1, rn, cn, inside = v.rc
    m = eq_mask(rings)
    vals = map_coordinates(m, [rn * MH - 0.5, cn * MW - 0.5], order=1, mode="nearest") * inside
    col, glow, border = o.get("col", YEL), o.get("glow"), o.get("border", WHT)
    pulse = 1.0 + (0.25 * math.sin((t - o["t0"]) * 6) if o.get("pulse") else 0.0)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    segs = globe_segments(v, rings)
    if glow:
        g = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0))
        dg = ImageDraw.Draw(g)
        for s in segs:
            dg.line([(x / 4, y / 4) for x, y in s], fill=glow + (int(230 * min(1, pulse)),), width=max(2, int(o.get("glow_w", 18) * pulse) // 4), joint="curve")
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR))
    al = o.get("alpha", 0.55)
    if al > 0:
        tile = Image.new("RGBA", (x1 - x0, y1 - y0), col + (0,))
        tile.putalpha(Image.fromarray((vals * 255 * al).astype(np.uint8)))
        lay.alpha_composite(tile, (x0, y0))
    if border:
        d = ImageDraw.Draw(lay)
        for s in segs:
            d.line(s, fill=border + (255,), width=o.get("bw", 3), joint="curve")
    if a < 1:
        lay.putalpha(lay.getchannel("A").point(lambda q: int(q * a)))
    img.alpha_composite(lay)


def fill(img, v, o, t):
    a = fade(o, t, o.get("fin", 0.35), 0.3)
    if a <= 0:
        return
    if v.mode == "globe":
        return fill_globe(img, v, o, t, a)
    rings = visible_rings(v, rings_of(o))
    if not rings:
        return
    col, glow, border = o.get("col", YEL), o.get("glow"), o.get("border", WHT)
    pulse = 1.0 + (0.25 * math.sin((t - o["t0"]) * 6) if o.get("pulse") else 0.0)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if glow:
        g = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0))
        dg = ImageDraw.Draw(g)
        for r in rings:
            q = [(x / 4, y / 4) for x, y in r]
            dg.line(q + [q[0]], fill=glow + (int(230 * min(1, pulse)),), width=max(2, int(o.get("glow_w", 18) * pulse) // 4), joint="curve")
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR))
    if o.get("alpha", 0.55) > 0:
        f = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
        df = ImageDraw.Draw(f)
        for r in rings:
            df.polygon([(x / 2, y / 2) for x, y in r], fill=col + (int(255 * o.get("alpha", 0.55)),))
        lay.alpha_composite(f.resize((W, H), Image.BILINEAR))
    if border:
        d = ImageDraw.Draw(lay)
        for r in rings:
            d.line(r + [r[0]], fill=border + (255,), width=o.get("bw", 3), joint="curve")
    if a < 1:
        lay.putalpha(lay.getchannel("A").point(lambda q: int(q * a)))
    img.alpha_composite(lay)


def plates(img, v, o, t):
    """All plate boundaries, drawn on progressively (reference: neon line reveal)."""
    a = fade(o, t, 0.3, 0.3)
    if a <= 0:
        return
    u = clamp((t - o["t0"]) / o.get("draw", 1.2))
    lay = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for code, rings in PLATE.items():
        if v.mode == "globe":
            segs = globe_segments(v, [r[: max(3, int(len(r) * u))] for r in rings])
        else:
            segs = [r[: max(3, int(len(r) * u))] for r in visible_rings(v, rings)]
        for s in segs:
            d.line([(x / 2, y / 2) for x, y in s], fill=o.get("col", ORANGE) + (int(240 * a),), width=3, joint="curve")
    glow = lay.filter(ImageFilter.GaussianBlur(4))
    img.alpha_composite(glow.resize((W, H), Image.BILINEAR))
    img.alpha_composite(lay.resize((W, H), Image.BILINEAR))


def continents(img, v, o, t):
    a = fade(o, t, 0.4, 0.3)
    if a <= 0:
        return
    cols = {"Africa": ORANGE, "Asia": PINK, "Europe": BLUE, "North America": GRN, "South America": LIME, "Oceania": YEL, "Antarctica": WHT}
    f = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
    df = ImageDraw.Draw(f)
    order = list(cols)
    if v.mode == "globe":
        for k, c in enumerate(order):
            if t < o["t0"] + 0.12 * k:
                continue
            fill_globe(img, v, dict(rings=CONT_RINGS[c], col=cols[c], alpha=0.6, border=None, t0=o["t0"], t1=o["t1"]), t, a)
        return
    for name, rings in COUNTRY.items():
        c = CONTINENT.get(name)
        if c not in cols:
            continue
        k = order.index(c)
        if t < o["t0"] + 0.12 * k:
            continue
        for r in visible_rings(v, rings):
            df.polygon([(x / 2, y / 2) for x, y in r], fill=cols[c] + (int(150 * a),))
    img.alpha_composite(f.resize((W, H), Image.BILINEAR))


def pill(img, v, o, t):
    """Rounded label box with text: dark pill + white text (reference top tags)."""
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.2)
    X, Y = pos(v, o)
    f = fit(MX, o.get("size", 52), o["txt"], 900)
    tw = f.getlength(o["txt"])
    lay = Image.new("RGBA", (int(tw + 80), int(f.size * 1.9)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((0, 0, lay.width - 1, lay.height - 1), radius=lay.height // 2, fill=o.get("bg", (12, 20, 40)) + (int(215 * a),),
                        outline=o.get("edge", WHT) + (int(255 * a),), width=3)
    d.text((lay.width / 2, lay.height / 2), o["txt"], font=f, fill=o.get("col", WHT) + (int(255 * a),), anchor="mm")
    put(img, lay, X, Y, back((t - o["t0"]) / 0.3))


def label(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.2)
    X, Y = pos(v, o)
    lay = text_layer(o["txt"], fit(o.get("font", MB), o.get("size", 84), o["txt"], o.get("maxw", 980)), o.get("col", WHT), o.get("stroke", 8), True, a)
    put(img, lay, X, Y, back((t - o["t0"]) / 0.3) * o.get("scale", 1.0), o.get("angle", 0))


def strike(img, v, o, t):
    """Word, red strike line drawn across at ts, replaced by a yellow word at tr (reference 0:01-0:04)."""
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.2)
    X, Y = pos(v, o)
    f = fit(MB, o.get("size", 120), o["old"], 980)
    if t < o["tr"]:
        old = text_layer(o["old"], f, WHT, 9, True, a)
        put(img, old, X, Y, back((t - o["t0"]) / 0.3))
        if t >= o["ts"]:
            u = ease((t - o["ts"]) / 0.22)
            half = f.getlength(o["old"]) / 2 + 20
            d = ImageDraw.Draw(img)
            x0, x1 = X - half, X - half + 2 * half * u
            d.line((x0, Y + 6, x1, Y - 2), fill=(0, 0, 0, 160), width=22)
            d.line((x0, Y + 2, x1, Y - 6), fill=RED + (255,), width=16)
    else:
        nf = fit(MB, o.get("size", 120), o["new"], 980)
        new = text_layer(o["new"], nf, YEL, 9, True, a)
        put(img, new, X, Y, back((t - o["tr"]) / 0.32) * (1.0 + 0.04 * math.sin((t - o["tr"]) * 5)))


def arrow(img, v, o, t):
    """Curved white pointer arrow drawn from a text anchor to a target (reference: thin curved arrows)."""
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.2)
    P0 = pos(v, o, "a")
    P1 = pos(v, o, "b")
    bend = o.get("bend", 0.25)
    mx, my = (P0[0] + P1[0]) / 2, (P0[1] + P1[1]) / 2
    nx, ny = -(P1[1] - P0[1]) * bend, (P1[0] - P0[0]) * bend
    u = ease((t - o["t0"]) / 0.35)
    pts = []
    for i in range(41):
        s = i / 40 * u
        x = (1 - s) ** 2 * P0[0] + 2 * (1 - s) * s * (mx + nx) + s ** 2 * P1[0]
        y = (1 - s) ** 2 * P0[1] + 2 * (1 - s) * s * (my + ny) + s ** 2 * P1[1]
        pts.append((x, y))
    d = ImageDraw.Draw(img)
    d.line([(x + 3, y + 4) for x, y in pts], fill=(0, 0, 0, int(140 * a)), width=9, joint="curve")
    d.line(pts, fill=WHT + (int(255 * a),), width=7, joint="curve")
    if u > 0.95:
        (xa, ya), (xb, yb) = pts[-4], pts[-1]
        ang = math.atan2(yb - ya, xb - xa)
        for s in (-1, 1):
            d.line((xb, yb, xb - 34 * math.cos(ang + s * 0.5), yb - 34 * math.sin(ang + s * 0.5)), fill=WHT + (int(255 * a),), width=7)


def measure(img, v, o, t):
    """Double-headed measurement arrow between two points + counter (reference 0:08-0:10)."""
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.2)
    A_, B_ = v.xy(*o["a"]), v.xy(*o["b"])
    u = ease((t - o["t0"]) / 0.5)
    mx, my = (A_[0] + B_[0]) / 2, (A_[1] + B_[1]) / 2
    P = (mx + (A_[0] - mx) * u, my + (A_[1] - my) * u)
    Q = (mx + (B_[0] - mx) * u, my + (B_[1] - my) * u)
    d = ImageDraw.Draw(img)
    d.line((P, Q), fill=(0, 0, 0, int(150 * a)), width=13)
    d.line((P, Q), fill=WHT + (int(255 * a),), width=7)
    ang = math.atan2(Q[1] - P[1], Q[0] - P[0])
    for (x, y), s0 in ((P, math.pi), (Q, 0.0)):
        for s in (-1, 1):
            d.line((x, y, x - 30 * math.cos(ang + s0 + s * 0.55), y - 30 * math.sin(ang + s0 + s * 0.55)), fill=WHT + (int(255 * a),), width=7)
    if t >= o["t0"] + 0.25:
        val = o["v0"] + (o["v1"] - o["v0"]) * ease((t - o["t0"] - 0.25) / o.get("dur", 1.0))
        lay = text_layer(o["fmt"].format(val), font(MB, o.get("size", 78)), WHT, 7, True, a)
        put(img, lay, mx, my - 70, back((t - o["t0"] - 0.25) / 0.3))
        if o.get("sub") and t >= o["t0"] + 0.6:
            sl = text_layer(o["sub"], font(MX, o.get("size", 78) * 0.6), YEL, 5, True, a)
            put(img, sl, mx, my + 60, back((t - o["t0"] - 0.6) / 0.3))


def counter(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    val = o["v0"] + (o["v1"] - o["v0"]) * clamp((t - o["t0"]) / o.get("dur", 1.0)) ** 0.6
    X, Y = pos(v, o)
    a = clamp((o["t1"] - t) / 0.2)
    txt = o["fmt"].format(val)
    lay = text_layer(txt, fit(MB, o.get("size", 110), o["fmt"].format(o["v1"]), 980), o.get("col", YEL), 9, True, a)
    put(img, lay, X, Y, back((t - o["t0"]) / 0.3))


def _icon(d, kind, cx, cy, r, a):
    w = (255, 255, 255, int(255 * a))
    if kind == "x":
        for s in (-1, 1):
            d.line((cx - r * 0.45, cy - s * r * 0.45, cx + r * 0.45, cy + s * r * 0.45), fill=w, width=int(r * 0.2))
    elif kind == "check":
        d.line((cx - r * 0.45, cy, cx - r * 0.1, cy + r * 0.38, cx + r * 0.5, cy - r * 0.4), fill=w, width=int(r * 0.2), joint="curve")
    elif kind == "ruler":
        d.rectangle((cx - r * 0.6, cy - r * 0.18, cx + r * 0.6, cy + r * 0.18), outline=w, width=int(r * 0.09))
        for i in range(5):
            x = cx - r * 0.45 + i * r * 0.225
            d.line((x, cy - r * 0.18, x, cy - r * (0.0 if i % 2 else -0.05)), fill=w, width=int(r * 0.07))
    elif kind == "plate":
        d.ellipse((cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55), outline=w, width=int(r * 0.1))
        d.line((cx - r * 0.55, cy - r * 0.05, cx - r * 0.15, cy + r * 0.12, cx + r * 0.1, cy - r * 0.2, cx + r * 0.55, cy + r * 0.05), fill=w, width=int(r * 0.09), joint="curve")
    elif kind == "book":
        d.rectangle((cx - r * 0.5, cy - r * 0.4, cx - r * 0.03, cy + r * 0.4), outline=w, width=int(r * 0.09))
        d.rectangle((cx + r * 0.03, cy - r * 0.4, cx + r * 0.5, cy + r * 0.4), outline=w, width=int(r * 0.09))
    elif kind == "compass":
        d.ellipse((cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55), outline=w, width=int(r * 0.09))
        d.polygon([(cx, cy - r * 0.45), (cx + r * 0.13, cy), (cx, cy + r * 0.45), (cx - r * 0.13, cy)], fill=w)
    elif kind == "trophy":
        d.pieslice((cx - r * 0.42, cy - r * 0.55, cx + r * 0.42, cy + r * 0.25), 0, 180, fill=w)
        d.rectangle((cx - r * 0.08, cy + r * 0.0, cx + r * 0.08, cy + r * 0.35), fill=w)
        d.rectangle((cx - r * 0.3, cy + r * 0.35, cx + r * 0.3, cy + r * 0.45), fill=w)
    elif kind == "ice":
        for k in range(3):
            ang = k * math.pi / 3
            d.line((cx - r * 0.5 * math.cos(ang), cy - r * 0.5 * math.sin(ang), cx + r * 0.5 * math.cos(ang), cy + r * 0.5 * math.sin(ang)), fill=w, width=int(r * 0.09))
    elif kind == "q":
        d.text((cx, cy), "?", font=font(MB, int(r * 1.1)), fill=w, anchor="mm")


def badge(img, v, o, t):
    """Flat circular UI badge with a pictogram and a small label (reference: wave/depth/salt badges)."""
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.2)
    X, Y = pos(v, o)
    r = o.get("r", 70)
    k = back((t - o["t0"]) / 0.32)
    if k <= 0.02:
        return
    lay = Image.new("RGBA", (int(r * 2.6), int(r * 2.6)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = lay.width / 2
    d.ellipse((c - r - 6, c - r - 6 + 6, c + r + 6, c + r + 6 + 6), fill=(0, 0, 0, int(110 * a)))
    d.ellipse((c - r, c - r, c + r, c + r), fill=o.get("col", BLUE) + (int(255 * a),), outline=WHT + (int(255 * a),), width=5)
    _icon(d, o["icon"], c, c, r, a)
    put(img, lay, X, Y, k)
    if o.get("txt"):
        tl = text_layer(o["txt"], fit(MX, o.get("tsize", 40), o["txt"], 520), WHT, 5, True, a)
        put(img, tl, X, Y + r * 1.0 + 34, k)


def pin(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.35)
    a = clamp((o["t1"] - t) / 0.2)
    X, Y = v.xy(o["lon"], o["lat"])
    L = o.get("len", 150) * clamp((t - o["t0"]) / 0.25)
    d = ImageDraw.Draw(img)
    d.line((X + 2, Y + 2, X + 2, Y - L + 2), fill=(0, 0, 0, int(150 * a)), width=4)
    d.line((X, Y, X, Y - L), fill=WHT + (int(255 * a),), width=4)
    d.ellipse((X - 9, Y - 9, X + 9, Y + 9), fill=o.get("dot", RED) + (int(255 * a),), outline=WHT + (int(255 * a),), width=3)
    lay = text_layer(o["txt"], font(MB, o.get("size", 58)), o.get("col", WHT), 6, True, a)
    put(img, lay, X, Y - L - lay.height / 2 + 26, k)


def _rot(lon, lat, axis, ang):
    """Rotate points (deg arrays) about a unit axis by ang (rad) on the sphere (Rodrigues)."""
    f, l = np.radians(lat), np.radians(lon)
    p = np.stack([np.cos(f) * np.cos(l), np.cos(f) * np.sin(l), np.sin(f)], -1)
    k = np.asarray(axis)
    c, s = math.cos(ang), math.sin(ang)
    q = p * c + np.cross(k, p) * s + np.outer(p @ k, k) * (1 - c)
    return np.degrees(np.arctan2(q[:, 1], q[:, 0])), np.degrees(np.arcsin(np.clip(q[:, 2], -1, 1)))


def _vec(lon, lat):
    f, l = math.radians(lat), math.radians(lon)
    return np.array([math.cos(f) * math.cos(l), math.cos(f) * math.sin(l), math.sin(f)])


def truesize(img, v, o, t):
    """A country outline slid across the sphere along a great circle and re-projected every frame (true-size effect)."""
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.25) * clamp((t - o["t0"]) / 0.2)
    u = ease((t - o["ta"]) / (o["tb"] - o["ta"]))
    p0, p1 = _vec(*o["src"]), _vec(*o["dst"])
    axis = np.cross(p0, p1)
    axis /= np.linalg.norm(axis)
    ang = math.acos(clamp(float(p0 @ p1), -1, 1)) * u
    rings = []
    for r in rings_of(o):
        lo, la = _rot(r[:, 0], r[:, 1], axis, ang)
        rings.append(np.stack([lo, la], -1))
    oo = dict(o, rings=rings, t0=o["t0"], t1=o["t1"])
    oo.pop("name", None)
    if o.get("ghost"):
        fill(img, v, dict(rings=rings_of(o), t0=o["t0"], t1=o["t1"], col=o.get("col", CYAN), alpha=0.0, border=(150, 230, 255), bw=2, kind="fill"), t)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fill(lay, v, dict(oo, alpha=o.get("alpha", 0.55), glow=o.get("glow", WHT)), t)
    if a < 1:
        lay.putalpha(lay.getchannel("A").point(lambda q: int(q * a)))
    img.alpha_composite(lay)


def graticule(img, v, o, t):
    """Parallels every 15 deg (Mercator stretch made visible)."""
    a = fade(o, t, 0.4, 0.3)
    if a <= 0:
        return
    d = ImageDraw.Draw(img)
    u = clamp((t - o["t0"]) / 1.0)
    for lat in range(-75, 90, 15):
        if abs(lat) > 15 + 75 * u:
            continue
        y = v.xy(0, lat)[1]
        col = YEL if abs(lat) >= 60 else WHT
        d.line((0, y, W, y), fill=col + (int((170 if abs(lat) >= 60 else 90) * a),), width=3 if abs(lat) >= 60 else 2)
    for lon in range(-180, 181, 30):
        x = v.xy(lon, 0)[0]
        d.line((x, 0, x, H), fill=WHT + (int(60 * a),), width=2)


def stretch(img, v, o, t):
    """Vertical double arrows that grow (land stretched near the poles)."""
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.2)
    u = ease((t - o["t0"]) / 0.6)
    X, Y = pos(v, o)
    L = o.get("len", 200) * (0.3 + 0.7 * u)
    d = ImageDraw.Draw(img)
    for s in (-1, 1):
        y1 = Y + s * L / 2
        d.line((X, Y, X, y1), fill=YEL + (int(255 * a),), width=9)
        d.line((X, y1, X - 24, y1 - s * 30), fill=YEL + (int(255 * a),), width=9)
        d.line((X, y1, X + 24, y1 - s * 30), fill=YEL + (int(255 * a),), width=9)


def flash(img, v, o, t):
    if not (o["t0"] <= t <= o["t1"]):
        return
    a = 1 - clamp((t - o["t0"]) / (o["t1"] - o["t0"]))
    img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(200 * a))))


def clip(img, v, o, t):
    """Placeholder for an AI clip insert (frames dir), with the mandatory on-screen AI label."""
    if not (o["t0"] <= t <= o["t1"]):
        return
    fi = int((t - o["t0"]) * FPS)
    files = sorted(os.listdir(o["dir"]))
    if not files:
        return
    im = Image.open(os.path.join(o["dir"], files[min(fi, len(files) - 1)])).convert("RGBA").resize((W, H))
    img.alpha_composite(im)
    ImageDraw.Draw(img).text((W / 2, 250), "AI-GENERATED ILLUSTRATION", font=font(MX, 34), fill=(255, 255, 255, 230), anchor="mm",
                             stroke_width=3, stroke_fill=(0, 0, 0, 200))


DRAW = dict(fill=fill, plates=plates, continents=continents, truesize=truesize, graticule=graticule, pin=pin, measure=measure,
            arrow=arrow, stretch=stretch, badge=badge, counter=counter, pill=pill, label=label, strike=strike, clip=clip, flash=flash)
ORDER = ["clip", "continents", "graticule", "fill", "plates", "truesize", "pin", "measure", "arrow", "stretch", "badge", "counter", "pill", "label", "strike", "flash"]

# ------------------------------------------------------------------ captions (2-word chunks, active word yellow)
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
        txts = [ws[j].strip() for j in chunk]
        f = fit(POP, 74, " ".join(txts), 960)
        sp = f.getlength(" ") * 1.4
        widths = [f.getlength(x) * 1.03 for x in txts]
        x = 540 - (sum(widths) + sp * (len(txts) - 1)) / 2
        for j, txt, wd in zip(chunk, txts, widths):
            on = j == cur
            k = max(1.0, min(1.12, 1.12 - 0.12 * clamp((t - ST[i] - TW[i][j] - 0.1) / 0.18))) if on else 1.0
            lay = text_layer(txt, f, YEL if on else WHT, 7, True)
            put(img, lay, x + wd / 2, 1440, k)
            x += wd + sp
        return


# ------------------------------------------------------------------ build
import shots70  # noqa: E402

shots70.build(SEGMENT, K, O, WT, ST, D, dict(COUNTRY=COUNTRY, big=big))
CREDIT = "NASA Blue Marble (GIBS) · Natural Earth · Plate boundaries: Bird 2003 (PB2002, ODC-By)"


def frame(fi):
    t = fi / FPS
    v = view_at(t)
    img = v.render()
    live = [o for o in OV if o["t0"] - 0.01 <= t <= o["t1"] + 0.01]
    for kind in ORDER:
        for o in live:
            if o["kind"] == kind:
                DRAW[kind](img, v, o, t)
    ImageDraw.Draw(img).text((W - 16, H - 12), CREDIT, font=font(MX, 16), fill=(255, 255, 255, 150), anchor="rs")
    caption(img, t)
    return np.asarray(img.convert("RGB"))


SFX_OF = dict(strike="strike", label="pop", pill="pop", badge="pop", pin="pop", counter="tick", measure="tick", arrow="swish",
              fill="glow", truesize="slide", plates="glow", continents="glow", graticule="glow", stretch="swish", flash="hit", clip="whoosh")


def events():
    ev = []
    for o in OV:
        s = SFX_OF.get(o["kind"])
        if s:
            ev.append((round(o["t0"], 3), s))
        if o["kind"] == "strike":
            ev.append((round(o["ts"], 3), "marker"))
            ev.append((round(o["tr"], 3), "ding"))
    for mode, ks in KEYS.items():
        ks = sorted(ks, key=lambda k: k[0])
        for a, b in zip(ks, ks[1:]):
            dz = abs(math.log(b[1][2] / a[1][2])) + (abs(b[1][0] - a[1][0]) + abs(b[1][1] - a[1][1])) / 40
            if dz > 0.35 and b[0] - a[0] < 3.5:
                ev.append((round(a[0], 3), "whoosh"))
    for s in SEG[1:]:
        ev.append((round(s[0], 3), "whoosh"))
    ev = sorted(set(e for e in ev if 0 <= e[0] < TOTAL))
    json.dump(ev, open(f"{SHORT}/events.json", "w"))
    return ev


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print(SHORT, "frames", NF, "total", round(TOTAL, 2), "segments", len(SEG), "overlays", len(OV))
    elif cmd == "events":
        ev = events()
        for s in range(0, int(TOTAL) + 1, 10):
            print(f"{s:2d}-{s + 10:2d}s", sum(1 for e in ev if s <= e[0] < s + 10), "sound events,",
                  sum(1 for o in OV if s <= o["t0"] < s + 10), "visual events")
    elif cmd == "still":
        os.makedirs(f"{SHORT}/stills", exist_ok=True)
        for a in sys.argv[2:]:
            Image.fromarray(frame(int(float(a) * FPS))).save(f"{SHORT}/stills/{float(a):05.1f}.jpg", quality=86)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
        p.stdin.close()
        p.wait()
