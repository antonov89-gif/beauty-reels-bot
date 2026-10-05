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

from script10 import CONT, LINES

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
starts = []
t = LEAD
for i, d in enumerate(D):
    starts.append(t)
    t += d + (0.08 if (i + 1) in CONT else 0.22)
TOTAL = t + 0.9
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

SOVIET = ["Russia", "Ukraine", "Belarus", "Lithuania", "Latvia", "Estonia", "Moldova", "Georgia",
          "Armenia", "Azerbaijan", "Kazakhstan"]
GERMANY = ["Germany", "Austria"]

# ---------------------------------------------------------------- camera / map
_TEX = {}


def tex(level):
    if level not in _TEX:
        a = np.load("tex_hi.npy" if level == "hi" else "tex_lo.npy")
        _TEX[level] = Image.fromarray(a)
    return _TEX[level]


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
        level = "hi" if self.span < 30 else "lo"
        ppd = TPPD if level == "hi" else TPPD / 4
        hw, hh = self.span / 2, H / 2 / self.ppd
        box = ((self.lon - hw - LON0) * ppd, (YTOP - (self.Y + hh)) * ppd,
               (self.lon + hw - LON0) * ppd, (YTOP - (self.Y - hh)) * ppd)
        return tex(level).resize((W, H), Image.BILINEAR, box=box)


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
    d = ImageDraw.Draw(img)
    d.line(out, fill=BLK + (255,), width=width + 10, joint="curve")
    d.line(out, fill=color + (255,), width=width, joint="curve")
    if len(out) >= 2:
        (ax, ay), (bx, by) = out[-2], out[-1]
        ang = math.atan2(by - ay, bx - ax)
        hs = width * 2.1
        tip = (bx + math.cos(ang) * hs * 0.6, by + math.sin(ang) * hs * 0.6)
        l = (bx + math.cos(ang + 2.4) * hs, by + math.sin(ang + 2.4) * hs)
        r = (bx + math.cos(ang - 2.4) * hs, by + math.sin(ang - 2.4) * hs)
        d.polygon([tip, l, r], fill=color + (255,), outline=BLK + (255,), width=5)


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
def sc(lines, cam, fx):
    return {"lines": lines, "cam": cam, "fx": fx}


def S_list():
    S = []
    S.append(sc((0, 0), (22, 49, 30, 30, 52, 26), [
        ("ehl", SOVIET, RED, WT(0, "Soviets"), 0.55),
        ("badge", 40, 57, "THE SOVIETS", RED, WT(0, "Soviets"), "🇷🇺"),
        ("emoji", 40, 52, "❌", 170, WT(0, "Soviets") + 0.5),
        ("big", "HITLER'S HEADACHE", WT(0, "biggest"), 300, 92, WHT),
    ]))
    S.append(sc((1, 1), (-10, 46, 28, -14, 45, 30), [
        ("badge", -16, 47, "AMERICA", BLU, WT(1, "America"), "🇺🇸"),
        ("arrow", [(-8, 45), (-22, 44)], BLU, WT(1, "It"), 0.5, 18),
        ("emoji", -16, 42, "❌", 170, WT(1, "America") + 0.35),
    ]))
    S.append(sc((2, 2), (12, 46, 18, 12.5, 42.5, 13), [
        ("hl", GERMANY, (90, 90, 90), WT(2, "ally"), 0.45),
        ("hl", ["Italy"], GRN, WT(2, "Italy"), 0.6),
        ("big", "ITALY", WT(2, "Italy"), 430, 190),
        ("emoji", 15.5, 40.5, "🇮🇹", 150, WT(2, "Italy")),
    ]))
    S.append(sc((3, 3), (8, 47, 20, 6, 47.5, 17), [
        ("big", "1940", WT(3, "1940"), 330, 170),
        ("hl", GERMANY, (180, 40, 40), WT(3, "Germany"), 0.55),
        ("hl", ["France"], BLU, WT(3, "France"), 0.5),
        ("arrow", [(10.5, 51), (6.5, 50), (3.5, 48.8)], RED, WT(3, "attack"), 0.6, 26),
        ("emoji", 11.5, 43, "🤝", 120, WT(3, "Italy")),
        ("emoji", 13.5, 43, "❓", 90, WT(3, "join")),
    ]))
    S.append(sc((4, 4), (12, 43.5, 13, 12.5, 43, 11.5), [
        ("hl", ["Italy"], GRN, WT(4, "Italy"), 0.55),
        ("big", "NO.", WT(4, "no"), 460, 230, RED),
        ("emoji", 12.5, 42.4, "🙅", 150, WT(4, "no")),
        ("badge", 12.5, 39.5, "NOT READY", RED, WT(4, "ready"), "⚠️"),
    ]))
    S.append(sc((5, 5), (5, 46.5, 16, 6.5, 46, 14), [
        ("hl", ["France"], RED, WT(5, "France"), 0.6),
        ("emoji", 2.35, 48.85, "💥", 150, WT(5, "collapse")),
        ("hl", ["Italy"], GRN, WT(5, "Mussolini"), 0.5),
        ("emoji", 12.5, 42.5, "🤔", 140, WT(5, "Mussolini")),
        ("emoji", 12.5, 42.5, "💡", 140, WT(5, "changed")),
        ("big", "CHANGED HIS MIND", WT(5, "changed"), 360, 110),
    ]))
    S.append(sc((6, 7), (8.5, 45.3, 9, 7.2, 45.2, 5.5), [
        ("hl", ["Italy"], GRN, WT(6, "He"), 0.45),
        ("hl", ["France"], BLU, WT(6, "Alps"), 0.45),
        ("arrow", [(8.8, 45.6), (7.4, 45.6), (6.6, 45.5)], GRN, WT(6, "threw"), 0.7, 24),
        ("arrow", [(8.6, 44.9), (7.6, 44.8), (6.9, 44.6)], GRN, WT(6, "threw") + 0.15, 0.7, 24),
        ("arrow", [(8.3, 44.2), (7.7, 43.9), (7.1, 43.85)], GRN, WT(6, "threw") + 0.3, 0.7, 24),
        ("count", 0, 300000, "{:,}", WT(6, "three"), 0.9, 380, "ITALIAN TROOPS"),
        ("emoji", 7.0, 45.9, "🏔️", 120, WT(6, "Alps")),
        ("emoji", 6.85, 45.0, "🛑", 160, WT(7, "stopped")),
        ("shake", WT(7, "stopped")),
        ("badge", 6.0, 46.4, "FAR SMALLER FRENCH FORCE", BLU, WT(7, "French"), "🇫🇷", 38),
    ]))
    S.append(sc((8, 8), (7.3, 45.2, 6, 7.3, 45.2, 8), [
        ("hl", ["Italy"], GRN, 0, 0.45),
        ("big", "ALMOST NOTHING", WT(8, "almost"), 470, 120),
        ("emoji", 7.4, 44.7, "🤏", 170, WT(8, "gained")),
    ]))
    S.append(sc((9, 9), (19, 31, 20, 24, 31, 15), [
        ("big", "SEPT 1940", WT(9, "September"), 330, 130),
        ("hl", ["Libya"], GRN, WT(9, "Libya"), 0.5),
        ("hl", ["Egypt"], RED, WT(9, "Egypt"), 0.5),
        ("badge", 19.5, 28.5, "10TH ARMY", GRN, WT(9, "Tenth"), "🇮🇹"),
        ("badge", 29.5, 27.5, "BRITISH EGYPT", RED, WT(9, "British"), "🇬🇧", 40),
        ("arrow", [(23.0, 31.6), (24.6, 31.55), (25.6, 31.5)], GRN, WT(9, "marched"), 0.8, 24),
    ]))
    S.append(sc((10, 10), (25.6, 31.2, 6.5, 26.1, 31.3, 5.2), [
        ("hl", ["Egypt"], RED, 0, 0.4),
        ("arrow", [(24.9, 31.6), (25.4, 31.55), (25.95, 31.6)], GRN, WT(10, "advanced"), 1.2, 26),
        ("count", 0, 100, "{} KM", WT(10, "about"), 1.0, 380, None),
        ("emoji", 26.0, 31.15, "🛑", 140, WT(10, "stopped")),
        ("emoji", 26.0, 31.15, "⛺", 150, WT(10, "dug")),
        ("label", 25.93, 31.6, "SIDI BARRANI", WT(10, "stopped"), -1),
    ]))
    S.append(sc((11, 11), (26, 31.3, 9, 25.5, 31.3, 8), [
        ("hl", ["Egypt"], RED, 0, 0.4),
        ("emoji", 26.0, 31.15, "⛺", 120, 0),
        ("arrow", [(28.0, 31.1), (27.0, 31.3), (26.2, 31.45)], RED, WT(11, "struck"), 0.6, 30),
        ("badge", 27.6, 30.2, "36,000 BRITISH", RED, WT(11, "thirtysix"), "🇬🇧", 40),
        ("shake", WT(11, "struck")),
    ]))
    S.append(sc((12, 12), (24.5, 31.4, 10, 21.5, 31.4, 15), [
        ("hl", ["Libya"], GRN, 0, 0.35),
        ("arrow", [(25.9, 31.6), (25.1, 31.75), (24.0, 32.1), (22.6, 32.8), (21.5, 32.6), (20.3, 31.9),
                   (20.2, 31.0), (19.2, 30.3)], RED, WT(12, "chased"), 1.8, 28),
        ("count", 0, 800, "{} KM", WT(12, "eight"), 1.0, 360, None),
        ("big2", "100,000+", WT(12, "prisoners") - 0.4, 600, 150, "PRISONERS"),
        ("emoji", 21.2, 30.0, "🏳️", 160, WT(12, "prisoners")),
    ]))
    S.append(sc((13, 13), (17, 42, 14, 20.5, 40, 10), [
        ("hl", ["Italy"], GRN, 0, 0.45),
        ("hl", ["Albania"], (120, 220, 120), WT(13, "quick"), 0.5),
        ("emoji", 13.5, 42.5, "😤", 130, WT(13, "Mussolini")),
        ("hl", ["Greece"], BLU, WT(13, "Greece"), 0.55),
        ("big", "GREECE", WT(13, "Greece"), 380, 170, WHT),
        ("emoji", 22.2, 39.3, "🇬🇷", 140, WT(13, "Greece")),
        ("arrow", [(19.9, 40.6), (20.7, 40.1), (21.2, 39.6)], GRN, WT(13, "win"), 0.6, 24),
    ]))
    S.append(sc((14, 14), (20.6, 40.2, 8.5, 20.2, 40.6, 7.5), [
        ("hl", ["Greece"], BLU, 0, 0.5),
        ("hl", ["Albania"], (120, 220, 120), 0, 0.45),
        ("arrow", [(21.6, 39.5), (20.9, 40.0), (20.1, 40.8)], BLU, WT(14, "pushed"), 0.9, 30),
        ("arrow", [(22.0, 40.2), (21.2, 40.7), (20.4, 41.3)], BLU, WT(14, "pushed") + 0.2, 0.9, 30),
        ("emoji", 19.9, 41.2, "🏃", 150, WT(14, "Albania")),
        ("shake", WT(14, "pushed")),
    ]))
    S.append(sc((15, 15), (16, 46, 20, 19, 44, 18), [
        ("hl", GERMANY, (180, 40, 40), WT(15, "Hitler"), 0.55),
        ("hl", ["Greece"], BLU, 0, 0.45),
        ("arrow", [(13, 49), (16, 47), (20, 45), (23, 42.5), (22.5, 40.0)], RED, WT(15, "send"), 1.0, 30),
        ("badge", 15, 52.5, "TO THE RESCUE", (180, 40, 40), WT(15, "bail"), "🇩🇪"),
        ("emoji", 22.4, 39.3, "🤦", 140, WT(15, "ally")),
    ]))
    S.append(sc((16, 16), (24, 51, 30, 32, 52, 34), [
        ("ehl", SOVIET, RED, WT(16, "invasion"), 0.5),
        ("hl", GERMANY, (180, 40, 40), 0, 0.5),
        ("arrow", [(14, 52), (22, 53), (30, 54.5)], (180, 40, 40), WT(16, "invasion"), 0.8, 34),
        ("arrow", [(14, 49), (22, 49), (31, 49)], (180, 40, 40), WT(16, "invasion") + 0.15, 0.8, 34),
        ("badge", 18, 58.5, "SOME HISTORIANS SAY", (70, 70, 70), WT(16, "Some"), "📚", 38),
        ("big", "DELAYED", WT(16, "weeks"), 520, 150),
        ("emoji", 30, 43.0, "⏳", 160, WT(16, "weeks")),
    ]))
    S.append(sc((17, 17), (37.6, 55.75, 12, 37.6, 55.75, 6), [
        ("dark", 0.35, WT(17, "leaving")),
        ("snow", WT(17, "winter") - 0.6),
        ("label", 37.62, 55.75, "MOSCOW", WT(17, "Moscow") - 0.4, -1),
        ("emoji", 37.6, 54.9, "❄️", 200, WT(17, "winter")),
        ("big", "WINTER", WT(17, "winter"), 420, 190, WHT),
    ]))
    S.append(sc((18, 18), (15, 47, 22, 13, 44, 17), [
        ("hl", GERMANY, (180, 40, 40), 0, 0.45),
        ("hl", ["Italy"], GRN, WT(18, "ally"), 0.6),
        ("emoji", 13.0, 42.0, "😱", 170, WT(18, "nightmare")),
        ("big", "BIGGEST NIGHTMARE", WT(18, "nightmare"), 400, 110),
        ("shake", WT(18, "nightmare")),
    ]))
    return S


S = S_list()
SCENE_T = []
for i, s in enumerate(S):
    t0 = starts[s["lines"][0]] - (LEAD if i == 0 else 0.11)
    SCENE_T.append(max(0, t0))
SCENE_T.append(TOTAL)
CUTS = SCENE_T[1:-1]


def scene_at(t):
    for i in range(len(S)):
        if SCENE_T[i] <= t < SCENE_T[i + 1]:
            return i
    return len(S) - 1


# ---------------------------------------------------------------- per-frame
SNOW = np.random.default_rng(3).uniform(0, 1, (220, 4))


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
    d = ImageDraw.Draw(img)
    for e in edges:
        d.line(e, fill=color + (255,), width=6, joint="curve")
        d.line(e, fill=(255, 255, 255, 200), width=2, joint="curve")


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
            gap = f.getlength(" ")
            ws = [f.getlength(w.upper()) for w in chunk]
            tot = sum(ws) + gap * (len(chunk) - 1)
            if tot > W - 70:
                f = font(POPX, 78 * (W - 70) / tot)
                gap = f.getlength(" ")
                ws = [f.getlength(w.upper()) for w in chunk]
                tot = sum(ws) + gap * (len(chunk) - 1)
            x = (W - tot) / 2
            d = ImageDraw.Draw(img)
            for j, (w, ww) in enumerate(zip(chunk, ws)):
                col = YEL if c0 + j == cur else WHT
                d.text((x, 1430), w.upper(), font=f, fill=col, anchor="lm", stroke_width=9, stroke_fill=BLK)
                x += ww + gap
            return


def frame(fi):
    t = fi / FPS
    si = scene_at(t)
    s = S[si]
    t0, t1 = SCENE_T[si], SCENE_T[si + 1]
    k = ease((t - t0) / max(0.1, t1 - t0))
    c = s["cam"]
    cam = Cam(lerp(c[0], c[3], k), lerp(c[1], c[4], k), lerp(c[2], c[5], k))
    shake = 0.0
    for f in s["fx"]:
        if f[0] == "shake" and 0 <= t - f[1] < 0.35:
            shake = 1 - (t - f[1]) / 0.35
    img = cam.render().convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_borders(ov, cam)
    img.alpha_composite(ov)
    # pass 1: map layers
    for f in s["fx"]:
        kind = f[0]
        if kind in ("hl", "ehl") and t >= f[3]:
            a = f[4] * ease((t - f[3]) / 0.25)
            draw_hl(img, cam, f[1], f[2], a, math.sin(t * 6) if kind == "ehl" else 0)
        elif kind == "dark" and t >= f[2]:
            a = f[1] * ease((t - f[2]) / 0.5)
            img.alpha_composite(Image.new("RGBA", (W, H), (5, 10, 30, int(255 * a))))
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
    # chromatic aberration + flash at cuts
    for ct in CUTS:
        if 0 <= t - ct < 0.12:
            a = 1 - (t - ct) / 0.12
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(110 * a))))
            r, g, b, al = img.split()
            sh = int(10 * a) + 1
            img = Image.merge("RGBA", (r.transform(img.size, Image.AFFINE, (1, 0, -sh, 0, 1, 0)), g,
                                       b.transform(img.size, Image.AFFINE, (1, 0, sh, 0, 1, 0)), al))
    caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32) * vignette()
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
