"""Map-animation Shorts engine (GeoGlobeTales style), v10 rebuild.

python3 engine.py still <frame>          -> still_<frame>.png
python3 engine.py video <f0> <f1> out.mp4 -> render frames [f0, f1) to mp4 (no audio)
"""
import json
import math
import subprocess
import sys

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from script16 import CONT, LINES

W, H, FPS = 1080, 1920, 30
LON0, LON1, LAT0, LAT1 = -25, 65, 8, 70
TPPD = 120  # texture pixels per degree (hi)
POP = "assets/Poppins-Bold.ttf"
POPX = "assets/Poppins-ExtraBold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

YEL = (255, 214, 10)
RED = (232, 52, 52)
GRN = (60, 200, 90)
BLU = (60, 140, 255)
WHT = (255, 255, 255)
BLK = (0, 0, 0)


def my(lat):
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


YTOP = my(LAT1)

# ---------------------------------------------------------------- timing
TM = json.load(open("timing.json"))
D, TW = TM["D"], TM["T"]
LEAD = 0.35
starts = [LEAD + s for s in TM["starts"]]
TOTAL = starts[-1] + D[-1] + 1.2
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


def pop(x):
    """0 -> 1.15 -> 1 overshoot."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    if x < 0.6:
        return 1.15 * ease(x / 0.6)
    return 1.15 - 0.15 * ease((x - 0.6) / 0.4)


# ---------------------------------------------------------------- geo
_SHP = shapefile.Reader("assets/ne50/ne_50m_admin_0_countries.shp")
_FIELDS = [f[0] for f in _SHP.fields[1:]]
COUNTRY = {}
for sr in _SHP.iterShapeRecords():
    rec = dict(zip(_FIELDS, sr.record))
    name = rec["ADMIN"]
    pts = sr.shape.points
    parts = list(sr.shape.parts) + [len(pts)]
    rings = []
    for a, b in zip(parts[:-1], parts[1:]):
        ring = np.array(pts[a:b])
        if ring[:, 0].max() < LON0 - 10 or ring[:, 0].min() > LON1 + 10:
            continue
        if ring[:, 1].max() < LAT0 - 5 or ring[:, 1].min() > LAT1 + 5:
            continue
        lat = np.clip(ring[:, 1], -85, 85)
        y = np.degrees(np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)))
        rings.append(np.stack([ring[:, 0], y], 1))
    if rings:
        COUNTRY[name] = rings

LABELPT = {"Spain": ("SPAIN", -3.5, 40.0), "France": ("FRANCE", 2.4, 46.9), "Italy": ("ITALY", 11.8, 43.6),
           "Tunisia": ("TUNISIA", 9.4, 34.4)}

SOVIET = ["Russia", "Ukraine", "Belarus", "Lithuania", "Latvia", "Estonia", "Moldova", "Georgia",
          "Armenia", "Azerbaijan", "Kazakhstan"]
GERMANY = ["Germany", "Austria"]

# ---------------------------------------------------------------- camera / map
LEVELS = {  # name: (lon0, lat1(top), ppd, file)
    "hi": (-15, 62, 240, "tex_hi.npy"),
    "mid": (-25, 70, 120, "tex_mid.npy"),
    "lo": (-25, 70, 30, "tex_lo.npy"),
}
_TEX = {}


def tex(level):
    if level not in _TEX:
        _TEX[level] = np.load(LEVELS[level][3], mmap_mode="r")
    return _TEX[level]


_SH = {}
SHADE_CFG = {"mid": ("shade_mid.npy", -14.0, 52.0, 120), "hi": ("shade_hi.npy", -14.0, 52.0, 240)}
SH_PAD = 1600
K_RELIEF = 1.9
FLAT = math.sin(math.radians(42))


def shade_map(level):
    if level not in _SH:
        a = np.load(SHADE_CFG[level][0])
        _SH[level] = np.pad(a, SH_PAD, constant_values=int((FLAT + 1) * 127.5))
    return _SH[level]


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
        """arr: Nx2 of (lon, mercY) -> pixel coords."""
        x = (arr[:, 0] - self.lon) * self.ppd + W / 2
        y = (self.Y - arr[:, 1]) * self.ppd + H / 2
        return np.stack([x, y], 1)

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
        out = crop.resize((W, H), Image.BICUBIC if self.span < 10 else Image.BILINEAR,
                          box=(bx0 - ix0, by0 - iy0, bx1 - ix0, by1 - iy0))
        if level in SHADE_CFG:
            SH = shade_map(level)
            _, slon0, stop, sppd = SHADE_CFG[level]
            top = my(stop)
            sx0, sx1 = (self.lon - hw - slon0) * sppd + SH_PAD, (self.lon + hw - slon0) * sppd + SH_PAD
            sy0, sy1 = (top - (self.Y + hh)) * sppd + SH_PAD, (top - (self.Y - hh)) * sppd + SH_PAD
            if sx0 >= 0 and sy0 >= 0 and sx1 <= SH.shape[1] and sy1 <= SH.shape[0]:
                piece = Image.fromarray(SH).resize((W, H), Image.BILINEAR, box=(sx0, sy0, sx1, sy1))
                f = 1 + K_RELIEF * ((np.asarray(piece).astype(np.float32) / 127.5 - 1) - FLAT)
                out = Image.fromarray(np.clip(np.asarray(out).astype(np.float32) * f[..., None], 0, 255).astype(np.uint8))
        return out


def lerp(a, b, k):
    return a + (b - a) * k


VIGN = None


def vignette():
    global VIGN
    if VIGN is None:
        yy, xx = np.mgrid[0:H // 4, 0:W // 4]
        d = np.sqrt(((xx - W / 8) / (W / 8)) ** 2 + ((yy - H / 8) / (H / 8)) ** 2)
        v = np.clip(1.0 - 0.35 * np.clip(d - 0.55, 0, None) ** 1.4, 0.55, 1)
        VIGN = np.asarray(Image.fromarray((v * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR))[..., None] / 255.0
    return VIGN


# ---------------------------------------------------------------- drawing helpers
_FONTS = {}


def font(path, size):
    key = (path, int(size))
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(path, max(1, int(size)))
    return _FONTS[key]


_EMO = {}


def emoji_sprite(ch):
    """Noto emoji at 109 px with a white sticker outline (cached)."""
    if ch not in _EMO:
        f = ImageFont.truetype(EMOJI, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((80, 80), ch, font=f, embedded_color=True, anchor="mm")
        a = im.split()[3]
        outline = a.filter(ImageFilter.MaxFilter(11))
        base = Image.new("RGBA", im.size, WHT + (0,))
        base.putalpha(outline)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sh.putalpha(outline.point(lambda v: v * 0.35))
        out = Image.new("RGBA", (170, 170), (0, 0, 0, 0))
        out.alpha_composite(sh, (6, 8))
        out.alpha_composite(base, (2, 2))
        out.alpha_composite(im, (2, 2))
        _EMO[ch] = out
    return _EMO[ch]


def paste_emoji(img, ch, x, y, size):
    if size < 4:
        return
    sp = emoji_sprite(ch)
    s = int(size * 170 / 120)
    sp = sp.resize((s, s), Image.LANCZOS)
    img.alpha_composite(sp, (int(x - s / 2), int(y - s / 2)))


def text_stroke(d, xy, txt, f, fill, stroke=8, anchor="mm", sfill=BLK):
    d.text(xy, txt, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)


def badge(img, x, y, txt, color, k, emoji=None, size=56):
    """Rounded tag with optional emoji, popping in with scale k."""
    if k <= 0.01:
        return
    f = font(POP, size * k)
    d = ImageDraw.Draw(img)
    tw = f.getlength(txt)
    ew = size * 1.15 * k if emoji else 0
    pw, ph = tw + ew + 44 * k, size * 1.55 * k
    x0, y0 = min(W - 30 - pw, max(30, x - pw / 2)), y - ph / 2
    d.rounded_rectangle((x0 + 5, y0 + 7, x0 + pw + 5, y0 + ph + 7), radius=ph / 2.4, fill=(0, 0, 0, 110))
    d.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), radius=ph / 2.4, fill=color + (255,), outline=WHT,
                        width=max(1, int(5 * k)))
    tx = x0 + 22 * k + ew
    d.text((tx, y + 2 * k), txt, font=f, fill=WHT, anchor="lm", stroke_width=max(1, int(3 * k)), stroke_fill=BLK)
    if emoji:
        paste_emoji(img, emoji, x0 + 22 * k + ew / 2 - 4 * k, y, size * 1.05 * k)


def arrow(img, pts, color, prog, width=22):
    """Progressively drawn thick arrow along pixel polyline pts."""
    if prog <= 0 or len(pts) < 2:
        return
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total = sum(seg)
    L = total * min(1, prog)
    out, acc = [pts[0]], 0
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if acc + s >= L:
            k = (L - acc) / max(s, 1e-6)
            out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
            break
        out.append(b)
        acc += s
    sh = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    ds.line([(x / 2 + 6, y / 2 + 8) for x, y in out], fill=(0, 0, 0, 120), width=int(width * 0.75), joint="curve")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    (ax, ay), (bx, by) = out[-2], out[-1]
    ang = math.atan2(by - ay, bx - ax)
    hs = width * 2.0
    tip = (bx + math.cos(ang) * hs * 0.7, by + math.sin(ang) * hs * 0.7)
    l = (bx + math.cos(ang + 2.35) * hs, by + math.sin(ang + 2.35) * hs)
    r = (bx + math.cos(ang - 2.35) * hs, by + math.sin(ang - 2.35) * hs)
    d.line(out, fill=WHT + (255,), width=width + 12, joint="curve")
    d.polygon([tip, l, r], fill=WHT + (255,), outline=WHT + (255,), width=12)
    d.line(out, fill=color + (255,), width=width, joint="curve")
    d.polygon([tip, l, r], fill=color + (255,))
    lite = tuple(min(255, c + 70) for c in color)
    d.line(out, fill=lite + (255,), width=max(2, width // 4), joint="curve")


def big(img, txt, t, t0, y=520, size=150, color=YEL, sub=None):
    """Slam text: scale 1.6 -> 1 in 0.15 s."""
    if t < t0:
        return 0
    k = (t - t0) / 0.15
    s = 1.6 - 0.6 * ease(k) if k < 1 else 1.0
    f = font(POPX, size * s)
    d = ImageDraw.Draw(img)
    while f.getlength(txt) > W - 80 and f.size > 20:
        f = font(POPX, f.size * 0.9)
    text_stroke(d, (W / 2, y), txt, f, color, stroke=max(4, int(size * 0.09)))
    if sub:
        text_stroke(d, (W / 2, y + size * 0.8), sub, font(POP, size * 0.36), WHT, stroke=5)
    return 1


# ---------------------------------------------------------------- scenes
def sc(lines, cam, fx, **kw):
    return dict(lines=lines, cam=cam, fx=fx, **kw)


NEWC = (-0.98, 37.60)
ROUTE1 = [NEWC, (0.85, 40.7), (2.9, 42.45), (4.75, 43.95)]
ROUTE2 = [(4.75, 43.95), (5.7, 45.2), (6.95, 45.1)]
ROUTE3 = [(6.95, 45.1), (7.68, 45.07)]
ROME = (12.5, 41.9)
CARTH = (10.32, 36.85)
DR0 = DR1 = 0.0


def S_list():
    S = []
    S.append(sc((0, 0), (5.0, 44.4, 12, 6.9, 45.4, 6.5), [
        ("emoji", 6.9, 45.2, "🐘", 190, WT(0, "elephants")),
        ("emoji", 6.2, 45.8, "❄️", 150, WT(0, "snow")),
        ("big", "IMPOSSIBLE?", WT(0, "Alps"), 330, 130, WHT),
        ("shake", WT(0, "Alps")),
    ]))
    S.append(sc((1, 1), (9.8, 38.8, 16, 9.8, 38.2, 11), [
        ("label", CARTH[0], CARTH[1], "CARTHAGE", WT(1, "Carthage"), 1),
        ("big", "218 BC", WT(1, "218"), 330, 150, WHT),
        ("hl", ["Italy"], RED, WT(1, "Rome"), 0.4),
        ("emoji", ROME[0], ROME[1], "🏛️", 150, WT(1, "Rome")),
        ("emoji", 9.0, 38.8, "❌", 190, WT(1, "sea")),
        ("arrow", [(CARTH[0], CARTH[1] + 0.3), (9.0, 38.6), (11.0, 40.2)], (200, 200, 200), WT(1, "sea") - 0.3, 0.6, 20),
    ]))
    S.append(sc((2, 2), (0.0, 39.5, 9, 0.5, 40.6, 7), [
        ("label", NEWC[0], NEWC[1], "NEW CARTHAGE", WT(2, "Spain"), 1),
        ("hl", ["Spain"], (120, 120, 120), WT(2, "Spain"), 0.25),
        ("count", 0, 90000, "{:,}", WT(2, "ninety"), 1.0, 420, "SOLDIERS"),
        ("emoji", 0.0, 40.0, "🐘", 170, WT(2, "elephants")),
        ("badge", 0.9, 41.9, "37 ELEPHANTS", RED, WT(2, "thirtyseven"), "🐘", 44),
    ]))
    S.append(sc((3, 3), (2.3, 41.5, 9, 4.2, 43.6, 6), [
        ("arrow", ROUTE1, RED, WT(3, "crossed"), 1.8, 26),
        ("label", 2.9, 42.45, "PYRENEES", WT(3, "Pyrenees"), 1),
        ("label", 4.75, 43.95, "RHONE", WT(3, "Rhone"), -1),
        ("emoji", 4.6, 44.4, "🛶", 170, WT(3, "rafts")),
        ("emoji", 4.95, 44.1, "🐘", 150, WT(3, "elephants")),
    ]))
    S.append(sc((4, 4), (5.6, 44.9, 7, 6.9, 45.1, 3.8), [
        ("arrow", ROUTE2, RED, WT(4, "Alps") - 0.4, 1.4, 26),
        ("big", "THE ALPS", WT(4, "Alps"), 330, 150, WHT),
        ("emoji", 6.3, 45.55, "🧊", 150, WT(4, "ice")),
        ("emoji", 7.2, 45.4, "🪨", 150, WT(4, "landslides")),
        ("emoji", 6.75, 45.7, "🏹", 150, WT(4, "tribes")),
        ("shake", WT(4, "landslides")),
    ]))
    S.append(sc((5, 5), (7.0, 45.1, 4.2, 7.6, 45.0, 7), [
        ("arrow", ROUTE3, RED, WT(5, "reached") - 0.5, 0.8, 28),
        ("count", 0, 15, "{} DAYS", WT(5, "fifteen"), 0.8, 330, None),
        ("label", 7.68, 45.07, "ITALY", WT(5, "Italy"), -1),
        ("hl", ["Italy"], GRN, WT(5, "Italy"), 0.25),
        ("emoji", 7.7, 45.5, "🏁", 150, WT(5, "Italy")),
    ]))
    S.append(sc((6, 6), (7.4, 45.2, 8, 7.6, 44.8, 6), [
        ("count", 90000, 26000, "{:,}", WT(6, "twentysix"), 1.0, 360, "MEN ARRIVED"),
        ("emoji", 7.5, 45.0, "😮‍💨", 160, WT(6, "cost")),
        ("shake", WT(6, "twentysix")),
    ]))
    S.append(sc((7, 7), (10.0, 44.4, 9, 11.8, 43.4, 8), [
        ("hl", ["Italy"], RED, WT(7, "shocked"), 0.3),
        ("arrow", [(7.68, 45.07), (9.6, 45.0)], RED, WT(7, "kept"), 0.6, 24),
        ("arrow", [(9.6, 45.0), (11.0, 44.2), (12.1, 43.13)], RED, WT(7, "kept") + 0.6, 0.8, 24),
        ("label", 9.6, 45.0, "TREBIA", WT(7, "victory"), -1),
        ("label", 12.1, 43.13, "TRASIMENE", WT(7, "victory") + 0.4, 1),
        ("emoji", 10.8, 44.6, "⚔️", 140, WT(7, "victory")),
        ("big", "VICTORY", WT(7, "victory"), 330, 140, YEL),
    ]))
    S.append(sc((8, 8), (15.5, 41.6, 8, 16.1, 41.3, 4.2), [
        ("arrow", [(12.1, 43.13), (14.2, 42.1), (16.13, 41.3)], RED, WT(8, "Kannee") - 0.3, 1.0, 26),
        ("label", 16.13, 41.3, "CANNAE", WT(8, "Kannee"), 1),
        ("big", "216 BC", WT(8, "216"), 330, 150, WHT),
        ("emoji", 16.0, 41.5, "💥", 170, WT(8, "destroyed")),
        ("badge", 16.0, 42.0, "MUCH LARGER ROMAN ARMY", BLU, WT(8, "larger"), "🏛️", 36),
        ("shake", WT(8, "destroyed")),
    ]))
    S.append(sc((9, 9), (12.3, 42.0, 7, 12.5, 41.9, 4.6), [
        ("hl", ["Italy"], GRN, 0, 0.2),
        ("emoji", ROME[0], ROME[1], "🏛️", 170, WT(9, "Rome")),
        ("emoji", ROME[0], ROME[1], "❌", 190, WT(9, "never")),
        ("big", "NEVER TOOK ROME", WT(9, "never"), 330, 130, WHT),
        ("count", 0, 15, "{} YEARS IN ITALY", WT(9, "fifteen"), 1.0, 450, None),
    ]))
    S.append(sc((10, 10), (11.5, 39.5, 11, 10.6, 37.2, 6), [
        ("hl", ["Tunisia"], BLU, WT(10, "Africa"), 0.3),
        ("arrow", [(12.5, 38.0), (11.2, 37.4), (10.1, 37.1)], BLU, WT(10, "struck"), 0.8, 26),
        ("label", CARTH[0], CARTH[1], "CARTHAGE", WT(10, "Carthage"), 1),
        ("big", "ZAMA", WT(10, "Zama"), 330, 150, YEL),
        ("emoji", 9.6, 36.2, "😞", 150, WT(10, "lost")),
        ("shake", WT(10, "Zama")),
    ]))
    S.append(sc((11, 11), (6.0, 43.5, 6, 5.0, 43.5, 12), [
        ("emoji", 6.9, 45.2, "🐘", 190, WT(11, "impossible")),
        ("emoji", 6.2, 45.8, "❄️", 150, WT(11, "impossible")),
        ("big", "NOT ENOUGH", WT(11, "wasn't"), 330, 130, YEL),
        ("shake", WT(11, "wasn't")),
    ]))
    return S


S = S_list()


def with_splits(S):
    ts = [s.get("t0", starts[s["lines"][0]] - (LEAD if i == 0 else 0.11)) for i, s in enumerate(S)] + [TOTAL]
    out, flip = [], 1
    for i, s in enumerate(S):
        d = ts[i + 1] - ts[i]
        if d > 3.4:
            c = s["cam"]
            mid = ts[i] + d * 0.5
            s1, s2 = dict(s), dict(s)
            s1["cam"] = (c[0], c[1], c[2], lerp(c[0], c[3], .5), lerp(c[1], c[4], .5), lerp(c[2], c[5], .5))
            dx = flip * 0.10 * c[5]
            flip = -flip
            s2["cam"] = (c[3] + dx, c[4], c[5] * 0.78, c[3] - dx * 0.3, c[4], c[5] * 0.62)
            s2["t0"] = mid
            out += [s1, s2]
        else:
            out.append(s)
    return out


S = with_splits(S)
SCENE_T = []
for i, s in enumerate(S):
    t0 = s.get("t0", starts[s["lines"][0]] - (LEAD if i == 0 else 0.11))
    SCENE_T.append(max(0, t0))
SCENE_T.append(TOTAL)
CUTS = SCENE_T[1:-1]


def scene_at(t):
    for i in range(len(S)):
        if SCENE_T[i] <= t < SCENE_T[i + 1]:
            return i
    return len(S) - 1


# ---------------------------------------------------------------- per-frame
SNOW = np.random.default_rng(3).uniform(0, 1, (320, 4))
GRAIN = np.random.default_rng(9).normal(0, 4.0, (H + 256, W + 256, 1)).astype(np.float32)


def draw_borders(ov, cam):
    d = ImageDraw.Draw(ov)
    for name, rings in COUNTRY.items():
        for r in rings:
            p = cam.xyY(r)
            if p[:, 0].max() < -50 or p[:, 0].min() > W + 50 or p[:, 1].max() < -50 or p[:, 1].min() > H + 50:
                continue
            d.line([tuple(q) for q in p], fill=(255, 255, 255, 120), width=2)


def draw_hl(img, cam, names, color, alpha, pulse=0.0):
    """Region fill (mask at 1/4 res) + crisp edge."""
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
    a = alpha * (1 + 0.15 * pulse)
    m = m.resize((W, H), Image.BILINEAR).point(lambda v: int(v * min(1, a)))
    layer = Image.new("RGBA", (W, H), color + (0,))
    layer.putalpha(m)
    img.alpha_composite(layer)
    g = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0))
    dg = ImageDraw.Draw(g)
    for e in edges:
        dg.line([(x / 4, y / 4) for x, y in e], fill=color + (int(200 * min(1, a / 0.5)),), width=4)
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    for e in edges:
        d.line(e, fill=color + (255,), width=5, joint="curve")
        d.line(e, fill=(255, 255, 255, 220), width=2, joint="curve")



def _poly_px(cam, ll):
    return cam.xyY(np.array([(lo, my(la)) for lo, la in ll]))


def dashed(d, p, color, width, on=30, off=18, phase=0.0):
    pts = list(map(tuple, p)) + [tuple(p[0])]
    acc, draw = phase % (on + off), True
    if acc >= on:
        acc, draw = acc - on, False
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        pos = 0.0
        while pos < L:
            seg = (on if draw else off) - acc
            n = min(seg, L - pos)
            if draw:
                d.line([(ax + (bx - ax) * pos / L, ay + (by - ay) * pos / L),
                        (ax + (bx - ax) * (pos + n) / L, ay + (by - ay) * (pos + n) / L)], fill=color, width=width)
            pos += n
            acc += n
            if acc >= (on if draw else off) - 1e-6:
                draw, acc = not draw, 0.0


def draw_sea(img, cam, t, t_in):
    p = _poly_px(cam, SEA60)
    ain = ease((t - t_in) / 0.5)
    drain = min(1.0, max(0.0, (t - DR0) / (DR1 - DR0)))
    m = Image.new("L", (W // 4, H // 4), 0)
    ImageDraw.Draw(m).polygon([tuple(q / 4) for q in p], fill=255)
    m = np.asarray(m.resize((W, H), Image.BILINEAR)).astype(np.float32) / 255
    y0, y1 = p[:, 1].min(), p[:, 1].max()
    yb = y0 + (y1 - y0) * ease(drain) * 1.08
    yy = np.arange(H, dtype=np.float32)[:, None]
    m = m * np.clip((yy - yb) / 60.0 + 0.5, 0, 1)
    a = (m * 150 * ain).astype(np.uint8)
    layer = np.zeros((H, W, 4), np.uint8)
    layer[..., 0], layer[..., 1], layer[..., 2], layer[..., 3] = 30, 120, 235, a
    img.alpha_composite(Image.fromarray(layer, "RGBA"))
    g = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0))
    q = p / 4
    dashed(ImageDraw.Draw(g), q, (120, 190, 255, int(230 * ain)), 5, 8, 5, t * 12)
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    dashed(d, p, (255, 255, 255, int(255 * ain)), 5, 30, 18, t * 48)


def draw_sean(img, cam, t, t_in):
    p = _poly_px(cam, SEAN)
    k = ease((t - t_in) / 0.7)
    m = Image.new("L", (W // 4, H // 4), 0)
    ImageDraw.Draw(m).polygon([tuple(q / 4) for q in p], fill=255)
    m = m.resize((W, H), Image.BILINEAR).point(lambda v: int(v * 0.55 * k))
    layer = Image.new("RGBA", (W, H), (60, 220, 130, 0))
    layer.putalpha(m)
    img.alpha_composite(layer)
    d = ImageDraw.Draw(img)
    pulse = 5 + 2 * math.sin(t * 6)
    d.line([tuple(x) for x in p] + [tuple(p[0])], fill=(255, 255, 255, int(255 * k)), width=int(pulse), joint="curve")


DUSTP = np.random.default_rng(5).uniform(0, 1, (260, 4))


def draw_dust(img, t, t_in):
    k = ease((t - t_in) / 0.8)
    img.alpha_composite(Image.new("RGBA", (W, H), (190, 140, 80, int(85 * k))))
    d = ImageDraw.Draw(img)
    for sx, sy, sp, sz in DUSTP:
        x = (sx * W + (t - t_in) * (260 + sp * 420)) % W
        y = (sy * H - (t - t_in) * 40 * sp) % H
        L = 30 + sz * 70
        d.line([(x - L, y + L * 0.12), (x, y)], fill=(235, 205, 160, int(170 * k)), width=2 + int(sz * 3))


def persp_coeffs(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, np.float64), np.array(B, np.float64))


def tilt_warp(img, a):
    """fake 3D pitch: far (top) edge shows the whole width, near (bottom) edge is magnified"""
    if a < 0.01:
        return img
    dst = [(0, 0), (W, 0), (W, H), (0, H)]
    src = [(0, 0), (W, 0), (W - a * W, H), (a * W, H)]
    out = img.transform((W, H), Image.PERSPECTIVE, persp_coeffs(dst, src), Image.BICUBIC)
    hz = np.linspace(0.30, 0.0, H, dtype=np.float32)[:, None, None]
    arr = np.asarray(out).astype(np.float32)
    arr[..., :3] = arr[..., :3] * (1 - hz) + np.array([40, 52, 70], np.float32) * hz
    return Image.fromarray(arr.astype(np.uint8), out.mode)


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
            since = t - (starts[i] + TW[i][cur])
            for j, (w, ww) in enumerate(zip(chunk, ws)):
                if c0 + j == cur:
                    sc_ = 1.0 + 0.06 * max(0.0, 1 - since / 0.14)
                    fz = font(POPX, f.size * sc_)
                    wz = fz.getlength(w.upper())
                    d.text((x + ww / 2 - wz / 2 + 4, 1436), w.upper(), font=fz, fill=(0, 0, 0, 160), anchor="lm")
                    d.text((x + ww / 2 - wz / 2, 1430), w.upper(), font=fz, fill=YEL, anchor="lm", stroke_width=9,
                           stroke_fill=BLK)
                else:
                    d.text((x + 4, 1436), w.upper(), font=f, fill=(0, 0, 0, 160), anchor="lm")
                    d.text((x, 1430), w.upper(), font=f, fill=WHT, anchor="lm", stroke_width=9, stroke_fill=BLK)
                x += ww + gap
            return


def frame(fi):
    t = fi / FPS
    si = scene_at(t)
    s = S[si]
    t0, t1 = SCENE_T[si], SCENE_T[si + 1]
    k = ease((t - t0) / max(0.1, t1 - t0))
    c = s["cam"]
    pz = 0.0
    for f in s["fx"]:
        te = f[2] if f[0] in ("big", "big2") else f[4] if f[0] == "count" else f[1] if f[0] == "shake" else None
        if te is not None and 0 <= t - te < 0.32:
            pz = max(pz, math.sin(math.pi * (t - te) / 0.32))
    span = lerp(c[2], c[5], k) * (1 - 0.07 * pz)
    cam = Cam(lerp(c[0], c[3], k) + 0.012 * span * math.sin(t * 1.9), lerp(c[1], c[4], k) + 0.01 * span * math.cos(t * 1.4), span)
    shake = 0.0
    for f in s["fx"]:
        if f[0] == "shake" and 0 <= t - f[1] < 0.35:
            shake = 1 - (t - f[1]) / 0.35
    img = cam.render().convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_borders(ov, cam)
    img.alpha_composite(ov)
    # pass 1: map layers
    names = []
    for f in s["fx"]:
        kind = f[0]
        if kind in ("hl", "ehl") and t >= f[3]:
            a = f[4] * ease((t - f[3]) / 0.25)
            draw_hl(img, cam, f[1], f[2], a, math.sin(t * 6) if kind == "ehl" else 0)
            lab = LABELPT.get(f[1][0])
            if lab and (len(f) < 6 or f[5]):
                names.append((lab, ease((t - f[3] - 0.1) / 0.3)))
        elif kind == "sea60" and t >= f[1]:
            draw_sea(img, cam, t, f[1])
        elif kind == "sean" and t >= f[1]:
            draw_sean(img, cam, t, f[1])
        elif kind == "dust" and t >= f[1]:
            draw_dust(img, t, f[1])
        elif kind == "frost" and t >= f[2]:
            a = f[1] * ease((t - f[2]) / 0.8)
            img.alpha_composite(Image.new("RGBA", (W, H), (225, 238, 255, int(255 * a))))
        elif kind == "dark" and t >= f[2]:
            a = f[1] * ease((t - f[2]) / 0.5)
            img.alpha_composite(Image.new("RGBA", (W, H), (5, 10, 30, int(255 * a))))
    for (txt, lo, la), k2 in names:
        x, y = cam.xy(lo, la)
        if -200 < x < W + 200 and 150 < y < 1350 and k2 > 0:
            sz = max(34, min(70, 2.2 * cam.ppd))
            f2 = font(POPX, sz)
            sp = " ".join(txt)
            lw = f2.getlength(sp) / 2
            x = min(W - 40 - lw, max(40 + lw, x))
            dl = ImageDraw.Draw(img)
            dl.text((x + 3, y + 4), sp, font=f2, fill=(0, 0, 0, int(140 * k2)), anchor="mm")
            dl.text((x, y), sp, font=f2, fill=(255, 255, 255, int(235 * k2)), anchor="mm",
                    stroke_width=2, stroke_fill=(0, 0, 0, int(120 * k2)))
    for f in s["fx"]:
        kind = f[0]
        if kind == "arrow" and t >= f[3]:
            pts = [cam.xy(lo, la) for lo, la in f[1]]
            arrow(img, pts, f[2], ease((t - f[3]) / f[4]), f[5])
    # pass 2: sprites / labels
    for f in s["fx"]:
        kind = f[0]
        if kind == "emoji" and t >= f[5]:
            x, y = cam.xy(f[1], f[2])
            bob = math.sin((t - f[5]) * 4) * 6
            paste_emoji(img, f[3], x, y + bob, f[4] * pop((t - f[5]) / 0.3))
        elif kind == "badge" and t >= f[5]:
            x, y = cam.xy(f[1], f[2])
            x = min(W - 60, max(60, x))
            badge(img, x, y, f[3], f[4], pop((t - f[5]) / 0.3), f[6] if len(f) > 6 else None,
                  f[7] + 10 if len(f) > 7 else 56)
        elif kind == "label" and t >= f[4]:
            x, y = cam.xy(f[1], f[2])
            kk = pop((t - f[4]) / 0.3)
            d = ImageDraw.Draw(img)
            d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=WHT, outline=BLK, width=4)
            ly = y + f[5] * 70
            d.line([(x, y), (x, ly)], fill=WHT, width=4)
            badge(img, x, ly + f[5] * 20, f[3], (30, 30, 30), kk, None, 50)
        elif kind == "snow" and t >= f[1]:
            d = ImageDraw.Draw(img)
            a = ease((t - f[1]) / 0.6)
            for sx, sy, sp, sz in SNOW:
                x = (sx * W + math.sin(t * 2 + sy * 9) * 30) % W
                y = (sy * H + t * (150 + sp * 250)) % H
                r = 3 + sz * 7
                d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255, int(220 * a)))
    for f in s["fx"]:
        kind = f[0]
        if kind == "big" and f[3] > 0:
            big(img, f[1], t, f[2], f[3], f[4], f[5] if len(f) > 5 else YEL)
        elif kind == "big2":
            big(img, f[1], t, f[2], f[3], f[4], YEL, f[5])
        elif kind == "count" and t >= f[4]:
            v = f[1] + (f[2] - f[1]) * ease((t - f[4]) / f[5])
            txt = f[3].format(int(round(v)))
            big(img, txt, t, f[4], f[6], 150, YEL, f[7])
    # whip smear + chromatic aberration + flash at cuts
    for ct in CUTS:
        if 0 <= t - ct < 0.2:
            a = 1 - (t - ct) / 0.2
            n = int(70 * a * a)
            if n > 2:
                arr = np.asarray(img).astype(np.float32)
                acc = sum(np.roll(arr, int(sh), axis=1) for sh in np.linspace(-n, n, 9)) / 9
                img = Image.fromarray(acc.astype(np.uint8), "RGBA")
        if 0 <= t - ct < 0.12:
            a = 1 - (t - ct) / 0.12
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(70 * a))))
            r, g, b, al = img.split()
            sh = int(10 * a) + 1
            img = Image.merge("RGBA", (r.transform(img.size, Image.AFFINE, (1, 0, -sh, 0, 1, 0)), g,
                                       b.transform(img.size, Image.AFFINE, (1, 0, sh, 0, 1, 0)), al))
    img = tilt_warp(img, 0.17 * min(1.0, max(0.0, (span - 5) / 8)))
    caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32) * vignette()
    if s.get("winter"):
        wk = ease((t - s["winter"]) / 0.8)
        gray = rgb.mean(2, keepdims=True)
        rgb = rgb * (1 - 0.7 * wk) + (gray * np.array([0.95, 1.05, 1.25]) + 25) * 0.7 * wk
    gy, gx = (fi * 37) % 256, (fi * 91) % 256
    rgb += GRAIN[gy:gy + H, gx:gx + W]
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    if shake > 0:
        dx = int(math.sin(t * 90) * 18 * shake)
        dy = int(math.cos(t * 77) * 14 * shake)
        out = out.transform(out.size, Image.AFFINE, (1, 0, dx, 0, 1, dy))
    return out


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
