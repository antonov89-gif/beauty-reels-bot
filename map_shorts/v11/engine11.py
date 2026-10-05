"""Map Short v11: 'What if 8 billion people lived in one building?'

Tile camera (NASA GIBS Blue Marble z<=8, USGS imagery z9-16) with fly-to zooms,
plus drawn diagram scenes (density grid, cube, height comparison).

python3 engine11.py prefetch                 -> download every tile the camera needs
python3 engine11.py info | still N | video A B out.mp4
"""
import json
import math
import os
import subprocess
import sys
import urllib.request
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter

from helpers import (BLK, BLU, FPS, GRN, H, POP, POPX, RED, W, WHT, YEL, arrow, badge, big, ease, font,
                     paste_emoji, pop, text_stroke)
from script11 import LINES

ORANGE = (255, 140, 30)
TILE_DIR = "tiles"
SPACE = (6, 10, 22)

# ---------------------------------------------------------------- timing
TM = json.load(open("timing.json"))
D, TW = TM["D"], TM["T"]
LEAD = 0.35
starts = [LEAD + s for s in TM["starts"]]
TOTAL = starts[-1] + D[-1] + 1.3
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


# ---------------------------------------------------------------- web mercator
def wx(lon):
    return (lon + 180) / 360 * 256


def wy(lat):
    lat = max(-85.0, min(85.0, lat))
    return (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * 256


def m_per_deg_lon(lat):
    return 111320 * math.cos(math.radians(lat))


class Cam:
    """lon/lat centre, span = degrees of longitude across the frame width."""

    def __init__(self, lon, lat, span):
        self.lon, self.lat, self.span = lon, lat, span
        self.X, self.Y = wx(lon), wy(lat)
        self.k = W / (span / 360 * 256)  # screen px per z0 world px

    def xy(self, lon, lat):
        return ((wx(lon) - self.X) * self.k + W / 2, (wy(lat) - self.Y) * self.k + H / 2)

    def m2px(self, meters):
        return meters / m_per_deg_lon(self.lat) / self.span * W

    def zoom(self):
        z = math.ceil(math.log2(self.k * 1.05))
        return max(1, min(16, z))

    def tiles(self):
        z = self.zoom()
        if z >= 9 and not us_area(self.lon, self.lat):
            z = 8
        s = 2 ** z
        x0 = (self.X - W / 2 / self.k) * s / 256
        x1 = (self.X + W / 2 / self.k) * s / 256
        y0 = max(0, (self.Y - H / 2 / self.k) * s / 256)
        y1 = min(s, (self.Y + H / 2 / self.k) * s / 256)
        out = []
        for ty in range(int(math.floor(y0)), int(math.ceil(y1))):
            for tx in range(int(math.floor(x0)), int(math.ceil(x1))):
                out.append((z, tx % s, ty, tx))
        return z, out

    def render(self):
        z, tl = self.tiles()
        s = 2 ** z
        scale = self.k / s  # screen px per tile px
        img = Image.new("RGB", (W, H), SPACE)
        ox = W / 2 - self.X * s * self.k / s
        oy = H / 2 - self.Y * s * self.k / s
        # compose at tile resolution then scale once
        txs = [t[3] for t in tl]
        tys = [t[2] for t in tl]
        if not tl:
            return img
        bx0, by0 = min(txs), min(tys)
        cw, ch = (max(txs) - bx0 + 1) * 256, (max(tys) - by0 + 1) * 256
        canvas = Image.new("RGB", (cw, ch), SPACE)
        for (zz, tx, ty, txr) in tl:
            t = get_tile(zz, tx, ty)
            if t is not None:
                canvas.paste(t, ((txr - bx0) * 256, (ty - by0) * 256))
        # screen box in canvas coords
        left = (self.X * s / 256 - bx0) * 256 - W / 2 / scale
        top = (self.Y * s / 256 - by0) * 256 - H / 2 / scale
        box = [left, top, left + W / scale, top + H / scale]
        pl, pt = max(0, -math.floor(box[0])), max(0, -math.floor(box[1]))
        pr, pb = max(0, math.ceil(box[2]) - cw), max(0, math.ceil(box[3]) - ch)
        if pl or pt or pr or pb:
            big_ = Image.new("RGB", (cw + pl + pr, ch + pt + pb), SPACE)
            big_.paste(canvas, (pl, pt))
            canvas = big_
            box = [box[0] + pl, box[1] + pt, box[2] + pl, box[3] + pt]
        out = canvas.resize((W, H), Image.BILINEAR if scale < 1.6 else Image.BICUBIC, box=box)
        # outside the world (polar band) stays space-coloured
        ytop = (0 - self.Y) * self.k + H / 2
        ybot = (256 - self.Y) * self.k + H / 2
        if ytop > 0 or ybot < H:
            d = ImageDraw.Draw(out)
            if ytop > 0:
                d.rectangle((0, 0, W, ytop), fill=SPACE)
            if ybot < H:
                d.rectangle((0, ybot, W, H), fill=SPACE)
        return out


def us_area(lon, lat):
    return (-170 < lon < -60 and 18 < lat < 72)


def tile_url(z, x, y):
    if z <= 8:
        return (f"https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_ShadedRelief_Bathymetry/default/"
                f"GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpeg")
    return f"https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"


def tile_path(z, x, y):
    return os.path.join(TILE_DIR, str(z), f"{x}_{y}.jpg")


_TC = OrderedDict()


def get_tile(z, x, y):
    key = (z, x, y)
    if key in _TC:
        _TC.move_to_end(key)
        return _TC[key]
    p = tile_path(z, x, y)
    im = None
    if os.path.exists(p) and os.path.getsize(p) > 100:
        try:
            im = style_tile(Image.open(p).convert("RGB"), z)
        except Exception:
            im = None
    nodata = None
    if im is not None and z >= 9:
        a = np.asarray(im).astype(np.int16)
        nodata = (a.max(2) < 8) | (a.min(2) > 250)
        if nodata.mean() < 0.001:
            nodata = None
    if (im is None or nodata is not None) and z > 1:
        if not os.path.exists(tile_path(z - 1, x // 2, y // 2)):
            fetch((z - 1, x // 2, y // 2))
        par = get_tile(z - 1, x // 2, y // 2)
        if par is not None:
            qx, qy = (x % 2) * 128, (y % 2) * 128
            up = par.crop((qx, qy, qx + 128, qy + 128)).resize((256, 256), Image.BILINEAR)
            if im is None:
                im = up
            else:
                m = Image.fromarray((nodata * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
                im = Image.composite(up, im, m)
    _TC[key] = im
    if len(_TC) > 600:
        _TC.popitem(last=False)
    return im


def style_tile(im, z):
    a = np.asarray(im).astype(np.float32)
    g = a.mean(2, keepdims=True)
    sat = 1.25 if z <= 8 else 1.18
    a = np.clip(g + (a - g) * sat, 0, 255)
    a = np.clip((a - 128) * 1.08 + 128 + (4 if z > 8 else 0), 0, 255)
    return Image.fromarray(a.astype(np.uint8))


# ---------------------------------------------------------------- borders (Natural Earth)
_SHP = shapefile.Reader("assets/ne50/ne_50m_admin_0_countries.shp")
_F = [f[0] for f in _SHP.fields[1:]]
COUNTRY = {}
for sr in _SHP.iterShapeRecords():
    rec = dict(zip(_F, sr.record))
    pts = sr.shape.points
    parts = list(sr.shape.parts) + [len(pts)]
    rings = []
    for a, b in zip(parts[:-1], parts[1:]):
        r = np.array(pts[a:b])
        lat = np.clip(r[:, 1], -85, 85)
        y = (1 - np.log(np.tan(np.radians(lat)) + 1 / np.cos(np.radians(lat))) / np.pi) / 2 * 256
        rings.append(np.stack([(r[:, 0] + 180) / 360 * 256, y], 1))
    COUNTRY[rec["ADMIN"]] = rings


def ring_px(cam, r):
    return np.stack([(r[:, 0] - cam.X) * cam.k + W / 2, (r[:, 1] - cam.Y) * cam.k + H / 2], 1)


def draw_borders(img, cam, alpha):
    if alpha <= 0:
        return
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for rings in COUNTRY.values():
        for r in rings:
            p = ring_px(cam, r)
            if p[:, 0].max() < -50 or p[:, 0].min() > W + 50 or p[:, 1].max() < -50 or p[:, 1].min() > H + 50:
                continue
            if len(p) > 2 and np.abs(np.diff(p[:, 0])).max() > W * 3:
                continue
            d.line([tuple(q) for q in p], fill=(255, 255, 255, int(110 * alpha)), width=2)
    img.alpha_composite(ov)


def draw_hl(img, cam, names, color, a):
    m = Image.new("L", (W // 4, H // 4), 0)
    dm = ImageDraw.Draw(m)
    edges = []
    for n in names:
        for r in COUNTRY.get(n, []):
            p = ring_px(cam, r)
            if p[:, 0].max() < -50 or p[:, 0].min() > W + 50 or p[:, 1].max() < -50 or p[:, 1].min() > H + 50:
                continue
            dm.polygon([tuple(q / 4) for q in p], fill=255)
            edges.append([tuple(q) for q in p])
    m = m.resize((W, H), Image.BILINEAR).point(lambda v: int(v * min(1, a)))
    layer = Image.new("RGBA", (W, H), color + (0,))
    layer.putalpha(m)
    img.alpha_composite(layer)
    d = ImageDraw.Draw(img)
    for e in edges:
        d.line(e, fill=color + (255,), width=5, joint="curve")
        d.line(e, fill=(255, 255, 255, 220), width=2, joint="curve")


# ---------------------------------------------------------------- geo constants
WHITTIER = (-148.6836, 60.7742)
INDY = (-86.2347, 39.7950)
MECCA = (39.8262, 21.4225)
GIGATX = (-97.6173, 30.2216)
EVERETT = (-122.2720, 47.9240)
CPARK = (-73.9654, 40.7829)
CP_CORNERS = [(-73.9730, 40.7644), (-73.9496, 40.7968), (-73.9580, 40.8006), (-73.9819, 40.7681)]
MANH_ANGLE = 29.0  # Manhattan grid rotation (degrees east of north)


def geo_square(center, side_m, angle_deg, k=1.0):
    """Corners (lon, lat) of a square centred at center, rotated like the Manhattan grid."""
    lon0, lat0 = center
    h = side_m / 2 * k
    a = math.radians(angle_deg)
    out = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        dx, dy = sx * h, sy * h
        ex = dx * math.cos(a) + dy * math.sin(a)
        ny = -dx * math.sin(a) + dy * math.cos(a)
        out.append((lon0 + ex / m_per_deg_lon(lat0), lat0 + ny / 111320))
    return out


# ---------------------------------------------------------------- scenes
def sc(lines, cam=None, fx=(), diagram=None, **kw):
    return dict(lines=lines, cam=cam, fx=list(fx), diagram=diagram, **kw)


S = [
    sc((0, 0), (-40, 15, 200, -60, 25, 150), [
        ("count", 0, 8_000_000_000, "{:,}", WT(0, "eight"), 1.4, 380, "PEOPLE ON EARTH"),
        ("emoji", -100, 40, "🧍", 120, WT(0, "people")), ("emoji", 15, 50, "👩", 120, WT(0, "people") + 0.1),
        ("emoji", 80, 25, "🧍", 120, WT(0, "people") + 0.2), ("emoji", 115, 35, "👨", 120, WT(0, "people") + 0.3),
        ("emoji", 20, 5, "🧒", 120, WT(0, "people") + 0.4), ("emoji", -60, -15, "👵", 120, WT(0, "people") + 0.5),
        ("emoji_screen", 540, 1050, "🏢", 300, WT(0, "building")),
    ], borders=0.6),
    sc((1, 1), (-60, 25, 150, -95, 40, 70), [
        ("big", "HOW BIG?", WT(1, "big"), 420, 190),
        ("emoji_screen", 540, 900, "🤔", 230, WT(1, "How")),
    ], borders=0.6),
    sc((2, 2), (-115, 52, 45, WHITTIER[0], WHITTIER[1], 0.07), [
        ("badge_screen", 540, 300, "WHITTIER, ALASKA", (40, 90, 160), WT(2, "Whittier"), "🇺🇸"),
        ("pin", WHITTIER[0], WHITTIER[1], "BEGICH TOWERS", WT(2, "tower") - 0.4),
        ("big", "14 FLOORS", WT(2, "fourteen"), 520, 120),
    ], fly=True),
    sc((3, 3), (WHITTIER[0], WHITTIER[1], 0.07, WHITTIER[0], WHITTIER[1], 0.04), [
        ("pin", WHITTIER[0], WHITTIER[1], "BEGICH TOWERS", 0),
        ("ring_emoji", WHITTIER[0], WHITTIER[1], ["📮", "👮", "🏥", "⛪"],
         [WT(3, "Post"), WT(3, "police"), WT(3, "clinic"), WT(3, "church")]),
        ("big", "ONE ROOF", WT(3, "roof"), 420, 150),
    ]),
    sc((4, 4), (WHITTIER[0], WHITTIER[1], 0.04, -80, 30, 190), [
        ("count", 0, 8_000_000_000, "{:,}", WT(4, "eight") - 0.2, 0.9, 420, "WAY BIGGER"),
    ], fly=True, zoomout=True, borders=0.5),
    sc((5, 5), (-90, 40, 18, INDY[0], INDY[1], 0.045), [
        ("badge_screen", 540, 300, "INDIANAPOLIS SPEEDWAY", (40, 90, 160), WT(5, "Indianapolis"), "🏁"),
        ("race", INDY, WT(5, "Speedway")),
        ("count", 0, 250_000, "{:,}", WT(5, "quarter") - 0.3, 0.8, 520, "SEATS"),
    ], fly=True),
    sc((6, 6), (25, 28, 60, MECCA[0], MECCA[1], 9), [
        ("hl", ["Saudi Arabia"], (40, 150, 80), WT(6, "Mecca"), 0.45),
        ("emoji", MECCA[0], MECCA[1], "🕋", 170, WT(6, "Grand")),
        ("badge", MECCA[0], MECCA[1] + 2.4, "MECCA", (40, 120, 70), WT(6, "Mecca"), "📍"),
        ("count", 0, 2_000_000, "{:,}", WT(6, "two") - 0.2, 0.8, 380, "WORSHIPPERS"),
    ], borders=0.7),
    sc((7, 7), (MECCA[0], MECCA[1], 9, 20, 20, 190), [
        ("dark", 0.55, WT(7, "Still")),
        ("progress", WT(7, "Still")),
        ("big", "NOT EVEN CLOSE", WT(7, "close"), 520, 120, RED),
        ("big", "MEASURE SPACE", WT(7, "measure"), 1180, 100, YEL),
    ], borders=0.4),
    sc((8, 8), None, [], diagram="density"),
    sc((9, 9), (-97.7, 30.3, 2.4, GIGATX[0], GIGATX[1], 0.35), [
        ("pin", GIGATX[0], GIGATX[1], "GIGA TEXAS", WT(9, "Giga")),
        ("emoji", GIGATX[0] + 0.03, GIGATX[1] + 0.04, "🚗", 130, WT(9, "Tesla")),
        ("big", "~1 KM²", WT(9, "square"), 420, 170),
    ]),
    sc((10, 10), (GIGATX[0], GIGATX[1], 0.35, GIGATX[0], GIGATX[1], 0.25), [
        ("pin", GIGATX[0], GIGATX[1], "GIGA TEXAS", 0),
        ("count", 0, 3_700_000, "{:,}", WT(10, "three") - 0.2, 0.9, 380, "PEOPLE"),
        ("badge_screen", 540, 1180, "A WHOLE COUNTRY", (40, 90, 160), WT(10, "country"), "🇺🇾"),
    ]),
    sc((11, 11), (-115, 45, 22, EVERETT[0], EVERETT[1], 0.05), [
        ("badge_screen", 540, 300, "BOEING EVERETT FACTORY", (40, 90, 160), WT(11, "Boeing"), "✈️"),
        ("pin", EVERETT[0], EVERETT[1], "13.4 MILLION m³", WT(11, "volume") - 0.3),
        ("big", "#1 BY VOLUME", WT(11, "biggest"), 1200, 110),
    ], fly=True),
    sc((12, 12), (EVERETT[0], EVERETT[1], 0.05, EVERETT[0], EVERETT[1], 0.035), [
        ("pin", EVERETT[0], EVERETT[1], "13.4 MILLION m³", 0),
        ("stack", WT(12, "Stack")),
        ("count", 0, 32_000_000, "{:,}", WT(12, "thirty") - 0.3, 0.9, 380, "PEOPLE"),
    ]),
    sc((13, 14), None, [], diagram="cube"),
    sc((15, 15), (-73.96, 40.80, 0.22, CPARK[0], CPARK[1], 0.075), [
        ("park", WT(15, "Central")),
        ("cube_fp", WT(15, "Drop")),
        ("badge_screen", 540, 300, "MANHATTAN", (40, 90, 160), WT(15, "Manhattan"), "🗽"),
        ("big", "WIDER THAN THE PARK", WT(15, "wider"), 1220, 84),
    ], fly=True),
    sc((16, 16), None, [], diagram="heights"),
    sc((17, 17), (CPARK[0], CPARK[1], 0.08, CPARK[0], CPARK[1], 0.06), [
        ("park", 0), ("cube_fp", -1), ("walker", WT(17, "walk")),
        ("big", "ALL OF HUMANITY", WT(17, "All"), 360, 108),
    ]),
]

SCENE_T = []
for i, s in enumerate(S):
    SCENE_T.append(0 if i == 0 else max(0, starts[s["lines"][0]] - 0.11))
SCENE_T.append(TOTAL)
CUTS = SCENE_T[1:-1]


def scene_at(t):
    for i in range(len(S)):
        if SCENE_T[i] <= t < SCENE_T[i + 1]:
            return i
    return len(S) - 1


def cam_at(s, t, t0, t1):
    c = s["cam"]
    k = (t - t0) / max(0.1, t1 - t0)
    if s.get("fly"):
        k = ease(min(1, k / 0.8))  # finish the flight a little early, then hold
    else:
        k = ease(k)
    sp = c[2] * (c[5] / c[2]) ** k
    if (s.get("fly") or s.get("zoomout")) and c[2] != c[5]:
        # centre moves linearly with span, so the target never leaves the frame
        kc = min(1, max(0, (sp - c[2]) / (c[5] - c[2])))
    else:
        kc = k
    lon = c[0] + (c[3] - c[0]) * kc
    lat = c[1] + (c[4] - c[1]) * kc
    return Cam(lon, lat, sp)


# ---------------------------------------------------------------- diagrams
def diagram_bg():
    img = Image.new("RGBA", (W, H))
    yy = np.linspace(0, 1, H)[:, None]
    top, bot = np.array([18, 30, 56.0]), np.array([5, 9, 20.0])
    a = (top * (1 - yy[..., None]) + bot * yy[..., None]) * np.ones((1, W, 1))
    img = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 14))
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 14))
    img.alpha_composite(ov)
    return img


_BG = None


def person_top(d, x, y, r, col):
    d.ellipse((x - r * 1.5, y - r * 0.8, x + r * 1.5, y + r * 0.8), fill=col, outline=BLK, width=3)
    d.ellipse((x - r * 0.62, y - r * 0.62, x + r * 0.62, y + r * 0.62), fill=(240, 200, 160), outline=BLK, width=3)


def diag_density(img, t, s):
    i = s["lines"][0]
    d = ImageDraw.Draw(img)
    cx, cy, side = 540, 820, 560
    k = ease((t - starts[i] + 0.1) / 0.4)
    hs = side / 2 * k
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle((cx - hs, cy - hs, cx + hs, cy + hs), fill=(255, 255, 255, 28))
    img.alpha_composite(ov)
    d.rectangle((cx - hs, cy - hs, cx + hs, cy + hs), outline=YEL, width=6)
    if k > 0.9:
        f = font(POPX, 54)
        text_stroke(d, (cx, cy + side / 2 + 60), "1 m", f, WHT, 6)
        text_stroke(d, (cx - side / 2 - 70, cy), "1 m", f, WHT, 6)
    cols = [(220, 60, 60), (60, 140, 255), (60, 200, 90), (255, 160, 40)]
    for j, (dx, dy) in enumerate(((-1, -1), (1, -1), (-1, 1), (1, 1))):
        tt = WT(i, "shoulder") + j * 0.22
        kk = pop((t - tt) / 0.3)
        if kk > 0:
            person_top(d, cx + dx * side / 4, cy + dy * side / 4, 62 * kk, cols[j])
    big(img, "4 PEOPLE / m²", t, WT(i, "four"), 300, 120)


def iso(x, y, z, s, ox, oy):
    a = math.radians(30)
    return (ox + (x - y) * math.cos(a) * s, oy + (x + y) * math.sin(a) * s - z * s)


def diag_cube(img, t, s):
    i0, i1 = s["lines"]
    d = ImageDraw.Draw(img)
    k = ease((t - starts[i0]) / 1.6)
    side = 1.0
    hgt = k
    sc_ = 330
    ox, oy = 540, 1060
    P = lambda x, y, z: iso(x - 0.5, y - 0.5, z, sc_, ox, oy)  # noqa: E731
    # ground shadow
    d.polygon([P(0, 0, 0), P(side, 0, 0), P(side, side, 0), P(0, side, 0)], fill=(0, 0, 0, 120))
    if hgt > 0.01:
        left = [P(0, side, 0), P(side, side, 0), P(side, side, hgt), P(0, side, hgt)]
        right = [P(side, 0, 0), P(side, side, 0), P(side, side, hgt), P(side, 0, hgt)]
        top = [P(0, 0, hgt), P(side, 0, hgt), P(side, side, hgt), P(0, side, hgt)]
        d.polygon(left, fill=(200, 150, 30, 255))
        d.polygon(right, fill=(150, 105, 15, 255))
        d.polygon(top, fill=(255, 214, 10, 255))
        # floor lines on the faces (stacked floors)
        nfl = int(14 * hgt)
        for f_ in range(1, nfl + 1):
            z = f_ / 14
            d.line([P(0, side, z), P(side, side, z), P(side, 0, z)], fill=(90, 60, 0, 120), width=2)
        for poly in (left, right, top):
            d.line(poly + [poly[0]], fill=BLK + (255,), width=5)
    if t >= WT(i0, "cubic"):
        big(img, "3.3 KM³", t, WT(i0, "cubic") - 0.2, 330, 170)
    if t >= starts[i1]:
        f = font(POPX, 60)
        for j, (a, b, tt) in enumerate(((P(0, side, 0), P(side, side, 0), WT(i1, "kilometer")),
                                         (P(side, side, 0), P(side, 0, 0), WT(i1, "kilometer") + 0.25),
                                         (P(side, 0, 0), P(side, 0, hgt), WT(i1, "side")))):
            kk = pop((t - tt) / 0.3)
            if kk > 0:
                mx, my_ = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                off = (0, 70) if j < 2 else (110, 0)
                text_stroke(d, (mx + off[0], my_ + off[1]), "1.5 km", font(POPX, 60 * kk), WHT, 7)
        big(img, "ONE GIANT CUBE", t, WT(i1, "giant"), 1350, 96, WHT)
    # people dots raining into the cube while it grows
    if 0.05 < k < 0.999:
        rng = np.random.default_rng(int(t * 30))
        for _ in range(40):
            x = rng.uniform(250, 830)
            y = rng.uniform(200, 700)
            d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 255, 160))


def diag_heights(img, t, s):
    i = s["lines"][0]
    d = ImageDraw.Draw(img)
    ground = 1240
    items = [("EIFFEL", 330, (170, 170, 190)), ("EMPIRE STATE", 443, (150, 170, 200)),
             ("BURJ KHALIFA", 828, (120, 190, 230)), ("THE CUBE", 1500, YEL)]
    scale = 0.47  # px per meter (to scale, including the cube's width)
    d.rectangle((0, ground, W, H), fill=(20, 30, 40, 255))
    d.line([(0, ground), (W, ground)], fill=WHT + (255,), width=4)
    xs = [80, 175, 280, 700]
    for j, ((name, hm, col), x) in enumerate(zip(items, xs)):
        tt = starts[i] + 0.2 + j * 0.35 if j < 3 else WT(i, "fifteen")
        if j == 2:
            tt = min(tt, WT(i, "Burj") - 0.3)
        k = ease((t - tt) / (0.5 if j < 3 else 0.9))
        if k <= 0:
            continue
        hpx = hm * scale * k
        if name == "THE CUBE":
            w_ = 1500 * scale / 2
            d.rectangle((x - w_, ground - hpx, x + w_, ground), fill=col + (255,), outline=BLK, width=5)
            for f_ in range(1, int(20 * k)):
                yy = ground - f_ * hpx / (20 * k)
                d.line([(x - w_, yy), (x + w_, yy)], fill=(120, 90, 0, 160), width=2)
        elif name == "BURJ KHALIFA":
            for lvl, wfrac in ((0.0, 1.0), (0.35, 0.7), (0.62, 0.45), (0.82, 0.25)):
                y0 = ground - hpx * lvl
                y1 = ground - hpx * (min(1, lvl + 0.38))
                ww = 30 * wfrac
                d.rectangle((x - ww, y1, x + ww, y0), fill=col + (255,), outline=BLK, width=3)
            d.line([(x, ground - hpx), (x, ground - hpx * 0.8)], fill=col, width=6)
        elif name == "EIFFEL":
            d.polygon([(x - 40, ground), (x - 6, ground - hpx), (x + 6, ground - hpx), (x + 40, ground)],
                      fill=col + (255,), outline=BLK, width=3)
        else:
            d.rectangle((x - 26, ground - hpx * 0.85, x + 26, ground), fill=col + (255,), outline=BLK, width=3)
            d.rectangle((x - 10, ground - hpx, x + 10, ground - hpx * 0.85), fill=col + (255,), outline=BLK, width=3)
        if k > 0.95:
            text_stroke(d, (x, ground - hpx - 40), f"{hm} m", font(POPX, 38 if j < 3 else 56), WHT, 6)
            nm = name.replace(" ", "\n") if j < 3 else name
            d.multiline_text((x, ground + 60), nm, font=font(POP, 26 if j < 3 else 44), fill=WHT, anchor="mm",
                             align="center", stroke_width=4, stroke_fill=BLK)
    big(img, "1,500 M TALL", t, WT(i, "fifteen") + 0.6, 190, 120)


DIAG = {"density": diag_density, "cube": diag_cube, "heights": diag_heights}


# ---------------------------------------------------------------- frame
SNOW = None
GRAIN = np.random.default_rng(9).normal(0, 3.5, (H + 256, W + 256, 1)).astype(np.float32)
VIGN = None


def vignette():
    global VIGN
    if VIGN is None:
        yy, xx = np.mgrid[0:H // 4, 0:W // 4]
        dd = np.sqrt(((xx - W / 8) / (W / 8)) ** 2 + ((yy - H / 8) / (H / 8)) ** 2)
        v = np.clip(1.0 - 0.35 * np.clip(dd - 0.55, 0, None) ** 1.4, 0.55, 1)
        VIGN = np.asarray(Image.fromarray((v * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR))[..., None] / 255.0
    return VIGN


def pin(img, x, y, txt, k):
    if k <= 0:
        return
    d = ImageDraw.Draw(img)
    r = 16 * k
    for rr, a in ((r * 3.2, 50), (r * 2.2, 90)):
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(255, 214, 10, a), width=4)
    d.ellipse((x - r, y - r, x + r, y + r), fill=YEL, outline=BLK, width=4)
    ly = y - 120 * k
    d.line([(x, y - r), (x, ly + 30)], fill=WHT, width=4)
    badge(img, x, ly, txt, (25, 25, 30), k, None, 50)


def caption(img, t):
    for i in range(len(LINES)):
        if starts[i] - 0.05 <= t < starts[i] + D[i] + 0.15:
            words = LINES[i].split()
            cur = 0
            for j, o in enumerate(TW[i]):
                if t >= starts[i] + o - 0.05:
                    cur = j
            c0 = cur // 3 * 3
            chunk = words[c0:c0 + 3]
            f = font(POPX, 78)
            gap = f.getlength(" ") * 1.7
            ws = [f.getlength(w.upper()) for w in chunk]
            tot = sum(ws) + gap * (len(chunk) - 1)
            if tot > W - 70:
                f = font(POPX, 78 * (W - 70) / tot)
                gap = f.getlength(" ") * 1.7
                ws = [f.getlength(w.upper()) for w in chunk]
                tot = sum(ws) + gap * (len(chunk) - 1)
            x = (W - tot) / 2
            d = ImageDraw.Draw(img)
            for j, (w, ww) in enumerate(zip(chunk, ws)):
                col = YEL if c0 + j == cur else WHT
                d.text((x + 4, 1436), w.upper(), font=f, fill=(0, 0, 0, 160), anchor="lm")
                d.text((x, 1430), w.upper(), font=f, fill=col, anchor="lm", stroke_width=9, stroke_fill=BLK)
                x += ww + gap
            return


def frame(fi):
    global _BG
    t = fi / FPS
    si = scene_at(t)
    s = S[si]
    t0, t1 = SCENE_T[si], SCENE_T[si + 1]
    if s["diagram"]:
        if _BG is None:
            _BG = diagram_bg()
        img = _BG.copy()
        DIAG[s["diagram"]](img, t, s)
        cam = None
    else:
        cam = cam_at(s, t, t0, t1)
        img = cam.render().convert("RGBA")
        draw_borders(img, cam, s.get("borders", 0) * min(1, max(0, (cam.span - 3) / 10)))
    shake = 0.0
    for f in s["fx"]:
        kind = f[0]
        if kind == "hl" and t >= f[3]:
            draw_hl(img, cam, f[1], f[2], f[4] * ease((t - f[3]) / 0.3))
        elif kind == "dark" and t >= f[2]:
            img.alpha_composite(Image.new("RGBA", (W, H), (4, 8, 20, int(255 * f[1] * ease((t - f[2]) / 0.4)))))
        elif kind == "park" and t >= f[1]:
            k = ease((t - f[1]) / 0.4) if f[1] > 0 else 1
            pts = [cam.xy(lo, la) for lo, la in CP_CORNERS]
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(ov).polygon(pts, fill=(60, 220, 90, int(70 * k)), outline=(60, 220, 90, int(255 * k)),
                                       width=6)
            img.alpha_composite(ov)
            cx = sum(p[0] for p in pts) / 4
            cy = sum(p[1] for p in pts) / 4
            if k > 0.5 and f[1] > 0:
                badge(img, cx + 230, cy + 260, "CENTRAL PARK", (40, 130, 60), pop((t - f[1]) / 0.3), "🌳", 44)
        elif kind == "cube_fp" and (f[1] < 0 or t >= f[1]):
            k = 1.0 if f[1] < 0 else ease((t - f[1]) / 0.8)
            corners = [cam.xy(lo, la) for lo, la in geo_square(CPARK, 1500, MANH_ANGLE, max(0.02, k))]
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            od.polygon([(x + 14, y + 18) for x, y in corners], fill=(0, 0, 0, 90))
            od.polygon(corners, fill=(255, 214, 10, 110), outline=(255, 214, 10, 255), width=8)
            img.alpha_composite(ov)
            if k > 0.95:
                a, b = corners[0], corners[1]
                text_stroke(ImageDraw.Draw(img), ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 50), "1.5 km",
                            font(POPX, 56), WHT, 7)
    for f in s["fx"]:
        kind = f[0]
        if kind == "emoji" and t >= f[5]:
            x, y = cam.xy(f[1], f[2])
            paste_emoji(img, f[3], x, y + math.sin((t - f[5]) * 4) * 6, f[4] * pop((t - f[5]) / 0.3))
        elif kind == "emoji_screen" and t >= f[5]:
            paste_emoji(img, f[3], f[1], f[2] + math.sin((t - f[5]) * 4) * 8, f[4] * pop((t - f[5]) / 0.3))
        elif kind == "badge" and t >= f[5]:
            x, y = cam.xy(f[1], f[2])
            badge(img, x, y, f[3], f[4], pop((t - f[5]) / 0.3), f[6] if len(f) > 6 else None, 56)
        elif kind == "badge_screen" and t >= f[5]:
            badge(img, f[1], f[2], f[3], f[4], pop((t - f[5]) / 0.3), f[6] if len(f) > 6 else None, 54)
        elif kind == "pin" and t >= f[4]:
            x, y = cam.xy(f[1], f[2])
            pin(img, x, y, f[3], pop((t - f[4]) / 0.3) if f[4] > 0 else 1)
        elif kind == "ring_emoji":
            x, y = cam.xy(f[1], f[2])
            for j, (ch, tt) in enumerate(zip(f[3], f[4])):
                if t >= tt:
                    a = math.radians(-150 + j * 100)
                    paste_emoji(img, ch, x + math.cos(a) * 300, y + math.sin(a) * 300 + 220,
                                140 * pop((t - tt) / 0.3))
        elif kind == "race" and t >= f[2]:
            lo, la = f[1]
            for j in range(3):
                a = (t - f[2]) * 1.6 + j * 2.1
                ex = lo + 0.0045 * math.sin(a)
                ey = la + 0.0060 * math.cos(a)
                x, y = cam.xy(ex, ey)
                paste_emoji(img, "🏎️", x, y, 90 * ease((t - f[2]) / 0.3))
        elif kind == "stack" and t >= f[1]:
            d = ImageDraw.Draw(img)
            n = int(min(12, (t - f[1]) * 10))
            for r_ in range(n):
                y = 1250 - r_ * 34
                for c_ in range(14):
                    x = 300 + c_ * 34 + (r_ % 2) * 17
                    d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(255, 214, 10, 230), outline=BLK, width=2)
        elif kind == "walker" and t >= f[1]:
            corners = [cam.xy(lo, la) for lo, la in geo_square(CPARK, 1500, MANH_ANGLE)]
            k = ease((t - f[1]) / 2.2)
            a, b = corners[0], corners[2]
            x, y = a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
            d = ImageDraw.Draw(img)
            d.line([a, (x, y)], fill=WHT + (255,), width=6)
            paste_emoji(img, "🚶", x, y - 40, 120)
            text_stroke(d, (540, 500), f"{int(20 * k)} MIN WALK", font(POPX, 100), YEL, 10)
        elif kind == "progress" and t >= f[1]:
            d = ImageDraw.Draw(img)
            k = ease((t - f[1]) / 0.6)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(ov).rounded_rectangle((90, 760, 990, 840), radius=40, fill=(255, 255, 255, 45))
            img.alpha_composite(ov)
            d.rounded_rectangle((90, 760, 990, 840), radius=40, outline=WHT, width=5)
            d.rounded_rectangle((96, 766, 96 + max(24, 2 * k), 834), radius=34, fill=YEL)
            text_stroke(d, (540, 900), "2 MILLION OF 8,000 MILLION", font(POPX, 46 * k + 1), WHT, 5)
    for f in s["fx"]:
        kind = f[0]
        if kind == "big":
            big(img, f[1], t, f[2], f[3], f[4], f[5] if len(f) > 5 else YEL)
            if t - f[2] < 0.3 and t >= f[2]:
                shake = max(shake, 1 - (t - f[2]) / 0.3)
        elif kind == "count" and t >= f[4]:
            v = f[1] + (f[2] - f[1]) * ease((t - f[4]) / f[5])
            big(img, f[3].format(int(round(v))), t, f[4], f[6], 120 if f[2] > 10 ** 8 else 150, YEL, f[7])
    for ct in CUTS:
        if 0 <= t - ct < 0.12:
            a = 1 - (t - ct) / 0.12
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(70 * a))))
    caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32) * vignette()
    gy, gx = (fi * 37) % 256, (fi * 91) % 256
    rgb += GRAIN[gy:gy + H, gx:gx + W]
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    if shake > 0:
        dx = int(math.sin(t * 90) * 10 * shake)
        dy = int(math.cos(t * 77) * 8 * shake)
        out = out.transform(out.size, Image.AFFINE, (1, 0, dx, 0, 1, dy))
    return out


def needed_tiles():
    need = set()
    for fi in range(0, NF):
        t = fi / FPS
        si = scene_at(t)
        s = S[si]
        if s["diagram"]:
            continue
        cam = cam_at(s, t, SCENE_T[si], SCENE_T[si + 1])
        for z, x, y, _ in cam.tiles()[1]:
            need.add((z, x, y))
    return need


def fetch(key):
    z, x, y = key
    p = tile_path(z, x, y)
    if os.path.exists(p):
        return 0
    os.makedirs(os.path.dirname(p), exist_ok=True)
    for _ in range(3):
        try:
            b = urllib.request.urlopen(urllib.request.Request(tile_url(z, x, y),
                                                              headers={"User-Agent": "map-shorts/1.0"}),
                                       timeout=30).read()
            open(p, "wb").write(b)
            return 1
        except urllib.error.HTTPError as e:
            if e.code == 404:
                open(p, "wb").write(b"")
                return 0
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prefetch":
        need = needed_tiles()
        print("tiles needed", len(need), flush=True)
        with ThreadPoolExecutor(12) as ex:
            got = sum(ex.map(fetch, sorted(need)))
        print("downloaded", got)
    elif cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for i, s in enumerate(S):
            print(i, s["lines"], round(SCENE_T[i], 2), int(SCENE_T[i] * FPS), s["diagram"] or "")
    elif cmd == "still":
        fi = int(sys.argv[2])
        frame(fi).save(f"still_{fi:05d}.png")
    elif cmd == "video":
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
