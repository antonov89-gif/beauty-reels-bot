"""v21: 'lost goat -> Dead Sea Scrolls' vertical Short. Flat vector illustration drawn in code (2x supersampled),
cuts every ~2 s, literal SFX, small captions, seamless loop (last frame = first frame).
python3 engine21.py still <frame> | info | video <f0> <f1> out.mp4"""
import json
import math
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from script21 import LINES

W, H, FPS = 1080, 1920, 30
S = 2
TM = json.load(open("timing.json"))
D, TW = TM["D"], TM["T"]
LEAD = 0.25
starts = [LEAD + s for s in TM["starts"]]
TOTAL = starts[-1] + D[-1] + 1.0
NF = int(TOTAL * FPS)

INK = (28, 24, 22)
CREAM = (250, 242, 226)
SAND = (233, 201, 145)
SAND_D = (205, 164, 104)
ROCK = (199, 154, 94)
ROCK_D = (150, 108, 62)
ROCK_DD = (105, 72, 42)
TEAL = (42, 167, 181)
SEA_D = (24, 120, 140)
RED = (239, 68, 68)
GOLD = (246, 196, 71)
GREEN = (60, 160, 90)
ROBE = (42, 120, 148)
SKIN = (222, 170, 130)
TERRA = (192, 106, 66)


def clean(w):
    return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word=None):
    if word is None:
        return starts[i]
    ws = [clean(w) for w in LINES[i].split()]
    q = clean(word)
    for j, w in enumerate(ws):
        if w == q or q in w:
            return starts[i] + TW[i][j]
    raise KeyError(word)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def back(x):
    x = min(1.0, max(0.0, x))
    return 1 + 3.0 * (x - 1) ** 3 + 2.0 * (x - 1) ** 2


def lerp(a, b, k):
    return a + (b - a) * k


def mix(c1, c2, k):
    return tuple(int(lerp(a, b, k)) for a, b in zip(c1, c2))


_F = {}


def font(kind, size, bold=False):
    key = (kind, int(size), bold)
    if key not in _F:
        f = ImageFont.truetype("fonts/Arimo.ttf" if kind == "sans" else "fonts/GochiHand.ttf", max(1, int(size)))
        if kind == "sans":
            try:
                f.set_variation_by_name("Bold" if bold else "Regular")
            except Exception:
                pass
        _F[key] = f
    return _F[key]


ZM = 1.0


# ---------------------------------------------------------------- canvas with camera
class Cv:
    def __init__(self, cx=540, cy=960, z=1.0, shake=(0, 0)):
        self.im = Image.new("RGB", (W * S, H * S), (0, 0, 0))
        self.d = ImageDraw.Draw(self.im, "RGBA")
        self.cx, self.cy, self.z = cx, cy, z * ZM
        self.sx, self.sy = shake

    def p(self, x, y):
        return (((x - self.cx) * self.z + W / 2 + self.sx) * S, ((y - self.cy) * self.z + H / 2 + self.sy) * S)

    def poly(self, pts, fill, outline=None, w=0):
        self.d.polygon([self.p(*q) for q in pts], fill=fill, outline=outline, width=int(w * S * self.z))

    def ell(self, cx, cy, rx, ry, fill, outline=None, w=0):
        a, b = self.p(cx - rx, cy - ry), self.p(cx + rx, cy + ry)
        self.d.ellipse((a[0], a[1], b[0], b[1]), fill=fill, outline=outline, width=int(w * S * self.z))

    def rect(self, x0, y0, x1, y1, fill, r=0):
        a, b = self.p(x0, y0), self.p(x1, y1)
        if r:
            self.d.rounded_rectangle((a[0], a[1], b[0], b[1]), radius=r * S * self.z, fill=fill)
        else:
            self.d.rectangle((a[0], a[1], b[0], b[1]), fill=fill)

    def line(self, pts, fill, w):
        self.d.line([self.p(*q) for q in pts], fill=fill, width=max(1, int(w * S * self.z)), joint="curve")

    def vgrad(self, y0, y1, c0, c1, x0=-2000, x1=4000):
        n = 28
        for k in range(n):
            ya, yb = lerp(y0, y1, k / n), lerp(y0, y1, (k + 1) / n)
            self.rect(x0, ya, x1, yb + 2, mix(c0, c1, k / (n - 1)))

    def text(self, x, y, s, f, fill, anchor="mm", shadow=0):
        ax, ay = self.p(x, y)
        fs = font(f[0], f[1] * S * self.z, f[2] if len(f) > 2 else False)
        if shadow:
            self.d.text((ax + 3 * S, ay + 4 * S), s, font=fs, fill=(0, 0, 0, shadow), anchor=anchor)
        self.d.text((ax, ay), s, font=fs, fill=fill, anchor=anchor)

    def out(self):
        return self.im.resize((W, H), Image.LANCZOS)


# ---------------------------------------------------------------- characters and props
def goat(c, x, y, s=1.0, body=(240, 232, 214), patch=(190, 160, 120), face=1, ph=0.0, rise=0.0):
    f = face
    lg = math.sin(ph * 6.2832) * 7 * s
    for dx, sw in ((-34, 1), (-20, -1), (22, -1), (36, 1)):
        c.line([(x + f * dx * s, y), (x + f * dx * s + lg * sw, y + 44 * s)], mix(body, INK, 0.55), 7 * s)
    c.rect(x - 52 * s, y - 30 * s, x + 52 * s, y + 6 * s, body, r=18 * s)
    c.ell(x + f * 8 * s, y - 18 * s, 22 * s, 12 * s, patch)
    c.line([(x - f * 50 * s, y - 20 * s), (x - f * 64 * s, y - 34 * s)], body, 8 * s)
    c.poly([(x + f * 40 * s, y - 28 * s), (x + f * 70 * s, y - 52 * s), (x + f * 82 * s, y - 40 * s), (x + f * 62 * s, y - 14 * s),
            (x + f * 44 * s, y - 8 * s)], body)
    c.ell(x + f * 78 * s, y - 36 * s, 9 * s, 7 * s, body)
    c.line([(x + f * 56 * s, y - 50 * s), (x + f * 52 * s, y - 74 * s)], INK, 5 * s)
    c.line([(x + f * 62 * s, y - 50 * s), (x + f * 62 * s, y - 70 * s)], INK, 5 * s)
    c.ell(x + f * 66 * s, y - 40 * s, 3 * s, 3 * s, INK)
    c.line([(x + f * 76 * s, y - 24 * s), (x + f * 78 * s, y - 12 * s)], mix(body, INK, 0.4), 4 * s)


def shepherd(c, x, y, s=1.0, face=1, ph=0.0, pose="walk", t=0.0):
    f = face
    sw = math.sin(ph * 6.2832)
    # legs
    legs = (-8, 8)
    for k, dx in enumerate(legs):
        a = sw * (1 if k else -1) * (12 if pose == "walk" else 4)
        c.line([(x + f * dx * s, y - 52 * s), (x + f * (dx + a) * s, y)], (60, 48, 40), 11 * s)
    # robe
    c.poly([(x - 28 * s, y - 62 * s), (x + 28 * s, y - 62 * s), (x + 36 * s, y - 14 * s), (x - 36 * s, y - 14 * s)], ROBE)
    c.poly([(x - 16 * s, y - 14 * s), (x + 16 * s, y - 14 * s), (x + 24 * s, y), (x - 24 * s, y)], mix(ROBE, INK, 0.25))
    c.rect(x - 28 * s, y - 62 * s, x + 28 * s, y - 52 * s, mix(ROBE, CREAM, 0.35), r=4 * s)
    # head + keffiyeh
    hy = y - 92 * s
    c.ell(x, hy, 22 * s, 24 * s, SKIN)
    c.poly([(x - 28 * s, hy - 6 * s), (x - 20 * s, hy - 30 * s), (x + 20 * s, hy - 30 * s), (x + 28 * s, hy - 6 * s), (x + 34 * s, hy + 34 * s),
            (x + 20 * s, hy + 24 * s), (x - 20 * s, hy + 24 * s), (x - 34 * s, hy + 34 * s)], CREAM)
    c.ell(x + f * 8 * s, hy + 2 * s, 17 * s, 20 * s, SKIN)
    c.line([(x - 22 * s, hy - 22 * s), (x + 22 * s, hy - 22 * s)], INK, 7 * s)
    c.ell(x + f * 12 * s, hy - 2 * s, 3.4 * s, 3.4 * s, INK)
    # arms + props
    if pose == "walk":
        c.line([(x + f * 6 * s, y - 56 * s), (x + f * (22 + sw * 8) * s, y - 28 * s)], ROBE, 10 * s)
        c.line([(x + f * 30 * s, y - 130 * s), (x + f * 26 * s, y + 4 * s)], (110, 76, 44), 7 * s)
    elif pose == "climb":
        up = math.sin(ph * 6.2832)
        c.line([(x, y - 56 * s), (x + f * 26 * s, y - (92 + 14 * up) * s)], ROBE, 10 * s)
        c.line([(x, y - 56 * s), (x - f * 20 * s, y - (86 - 14 * up) * s)], ROBE, 10 * s)
    elif pose == "search":
        c.line([(x, y - 56 * s), (x + f * 30 * s, y - 96 * s), (x + f * 22 * s, y - 112 * s)], ROBE, 10 * s)
        c.line([(x, y - 56 * s), (x - f * 24 * s, y - 24 * s)], ROBE, 10 * s)
        c.line([(x - f * 40 * s, y - 126 * s), (x - f * 40 * s, y + 4 * s)], (110, 76, 44), 7 * s)
    elif pose == "throw":
        k = ease(t)
        ang = lerp(-2.2, -0.2, k)
        ex, ey = x + f * 40 * s * math.cos(ang) * -1, y - 66 * s + 44 * s * math.sin(ang)
        c.line([(x, y - 56 * s), (ex, ey)], ROBE, 10 * s)
        c.line([(x, y - 56 * s), (x - f * 22 * s, y - 26 * s)], ROBE, 10 * s)
    elif pose == "up":
        c.line([(x, y - 56 * s), (x + f * 22 * s, y - 130 * s)], ROBE, 10 * s)
        c.line([(x, y - 56 * s), (x - f * 22 * s, y - 130 * s)], ROBE, 10 * s)


def jar(c, x, y, s=1.0, glow=0.0, lid=True):
    if glow > 0:
        for r, a in ((120, 30), (80, 50), (50, 70)):
            c.ell(x, y - 30 * s, r * s, r * s, GOLD + (int(a * glow),))
    c.ell(x, y - 36 * s, 34 * s, 42 * s, TERRA)
    c.rect(x - 14 * s, y - 88 * s, x + 14 * s, y - 62 * s, TERRA)
    c.ell(x, y - 88 * s, 18 * s, 6 * s, mix(TERRA, INK, 0.3))
    c.line([(x - 30 * s, y - 40 * s), (x + 30 * s, y - 40 * s)], mix(TERRA, INK, 0.3), 3 * s)
    c.line([(x - 28 * s, y - 28 * s), (x + 28 * s, y - 28 * s)], mix(TERRA, INK, 0.3), 3 * s)
    if lid:
        c.ell(x, y - 92 * s, 16 * s, 8 * s, mix(TERRA, CREAM, 0.3))


def scroll(c, x, y, s=1.0, rot=0.0, open_=1.0, lines=True):
    w = 80 * s * (0.35 + 0.65 * open_)
    h = 140 * s
    c.rect(x - w, y - h / 2, x + w, y + h / 2, CREAM, r=4 * s)
    for dx in (-w, w):
        c.ell(x + dx, y, 10 * s, h / 2 + 4 * s, mix(CREAM, ROCK_D, 0.35))
        c.ell(x + dx, y, 4 * s, h / 2 - 4 * s, mix(CREAM, ROCK_D, 0.15))
    if lines and open_ > 0.5:
        for k in range(7):
            yy = y - h / 2 + 20 * s + k * 17 * s
            c.line([(x - w + 22 * s, yy), (x + w - 22 * s - (k % 3) * 18 * s, yy)], mix(INK, CREAM, 0.35), 3 * s)


def rock_prop(c, x, y, s=1.0):
    c.poly([(x - 14 * s, y), (x - 10 * s, y - 14 * s), (x + 6 * s, y - 16 * s), (x + 16 * s, y - 4 * s), (x + 8 * s, y + 8 * s)], (120, 108, 96))


def qmark(c, x, y, k, s=1.0):
    if k <= 0:
        return
    r = 44 * s * back(k)
    c.ell(x, y, r, r, RED)
    c.text(x, y + 3, "?", ("sans", 64 * s * back(k), True), (255, 255, 255))


def sparkle(c, x, y, r, col=(255, 255, 255, 235)):
    c.poly([(x, y - r), (x + r * 0.22, y - r * 0.22), (x + r, y), (x + r * 0.22, y + r * 0.22), (x, y + r), (x - r * 0.22, y + r * 0.22),
            (x - r, y), (x - r * 0.22, y - r * 0.22)], col)


# ---------------------------------------------------------------- backgrounds
def landscape(c, t=0.0, bleed=0.0):
    c.vgrad(-900, 760, (150, 205, 235), (252, 232, 190))
    c.ell(840, 300, 70, 70, (255, 244, 205, 255))
    c.ell(840, 300, 130, 130, (255, 244, 205, 70))
    # distant Moab mountains
    c.poly([(-300, 760), (-120, 640), (60, 700), (260, 600), (460, 690), (700, 610), (960, 700), (1200, 620), (1500, 760)], (214, 168, 150))
    # Dead Sea
    c.rect(-300, 740, 1500, 920, TEAL)
    c.rect(-300, 740, 1500, 752, (110, 215, 220))
    for k in range(7):
        c.line([(60 + k * 170 + (t * 14) % 30, 780 + (k % 3) * 8), (110 + k * 170 + (t * 14) % 30, 780 + (k % 3) * 8)], (255, 255, 255, 110), 3)
    # hills
    c.poly([(-300, 900), (-100, 820), (200, 860), (520, 800), (860, 860), (1200, 810), (1500, 900), (1500, 2200), (-300, 2200)], mix(SAND, ROCK, 0.3))
    c.poly([(-300, 1010), (150, 930), (500, 990), (900, 920), (1500, 1000), (1500, 2300), (-300, 2300)], SAND)
    c.poly([(-300, 1250), (300, 1170), (700, 1230), (1500, 1160), (1500, 2400), (-300, 2400)], mix(SAND, SAND_D, 0.5))
    for k in range(14):
        x = -100 + k * 120
        c.line([(x, 1400 + (k % 4) * 70), (x - 8, 1380 + (k % 4) * 70)], (150, 140, 80), 5)
        c.line([(x, 1400 + (k % 4) * 70), (x + 8, 1380 + (k % 4) * 70)], (150, 140, 80), 5)


def cliff_bg(c):
    c.vgrad(-2400, 2200, (150, 205, 235), (252, 232, 190))
    c.poly([(-200, 2200), (-200, -2400), (300, -2400), (260, -1400), (330, -600), (250, 400), (330, 1300), (260, 1800), (300, 2200)],
           mix(SAND, SAND_D, 0.4))
    # main cliff
    pts = [(260, 2200), (300, 1500), (240, 900), (330, 300), (280, -300), (360, -900), (330, -1500), (420, -2400), (1500, -2400), (1500, 2200)]
    c.poly(pts, ROCK)
    # strata
    for k in range(22):
        y = 1800 - k * 190
        c.line([(300 + (k % 3) * 20, y), (1500, y + (k % 2) * 30)], ROCK_D + (200,), 5)
        c.line([(300, y + 40), (1500, y + 56)], mix(ROCK, ROCK_D, 0.4), 3)
    # ledge path
    c.poly([(1500, 1900), (260, 1900), (260, 2300), (1500, 2300)], mix(SAND, SAND_D, 0.5))
    c.rect(-300, 1940, 1500, 2300, mix(SAND, SAND_D, 0.5))
    c.line([(0, 1940), (1500, 1940)], mix(SAND_D, INK, 0.2), 6)


LEDGE = [(380, 1900), (520, 1700), (430, 1480), (640, 1300), (520, 1060), (760, 880), (600, 620), (820, 380), (660, 120), (880, -160),
         (700, -420), (900, -700), (720, -780)]
CAVE = (860, -820)


def path_pos(u):
    n = len(LEDGE) - 1
    u = min(max(u, 0), 1) * n
    i = min(int(u), n - 1)
    k = u - i
    return lerp(LEDGE[i][0], LEDGE[i + 1][0], k), lerp(LEDGE[i][1], LEDGE[i + 1][1], k)


def cave_mouth(c, glow=0.0):
    x, y = CAVE
    c.ell(x, y, 150, 190, ROCK_DD)
    c.ell(x, y + 6, 126, 168, (14, 10, 10))
    if glow:
        c.ell(x, y + 40, 90 * glow, 120 * glow, GOLD + (int(70 * glow),))


def cave_interior(c, t, glow):
    c.vgrad(-400, 2300, (24, 18, 16), (62, 44, 30))
    for k in range(9):
        c.poly([(-100 + k * 140, 0), (-30 + k * 140, 60 + (k % 3) * 40), (40 + k * 140, 0)], (40, 30, 24))
    c.ell(540, 1100, 520, 300, GOLD + (int(26 * glow),))
    c.rect(-200, 1180, 1300, 1300, ROCK_D)
    c.rect(-200, 1180, 1300, 1196, ROCK)


def studio_bg(c, tint=0.0):
    c.vgrad(-200, 2200, mix((252, 246, 232), (240, 220, 190), tint), mix((236, 226, 206), (222, 196, 156), tint))


# ---------------------------------------------------------------- shots
SHOTS = [
    ("wide", 0.0, WT(0, "one")),
    ("goatzoom", WT(0, "one"), starts[1] - 0.06),
    ("climb1", starts[1] - 0.06, WT(1, "cliffs")),
    ("climb2", WT(1, "cliffs"), starts[2] - 0.06),
    ("search", starts[2] - 0.06, WT(2, "threw") - 0.1),
    ("throw", WT(2, "threw") - 0.1, starts[3] - 0.06),
    ("dark", starts[3] - 0.06, starts[4] - 0.06),
    ("jars", starts[4] - 0.06, WT(4, "scrolls") - 0.15),
    ("scroll", WT(4, "scrolls") - 0.15, starts[5] - 0.06),
    ("years", starts[5] - 0.06, starts[6] - 0.06),
    ("oldest", starts[6] - 0.06, starts[7] - 0.06),
    ("scale", starts[7] - 0.06, WT(7, "few") - 0.1),
    ("price", WT(7, "few") - 0.1, starts[8] - 0.06),
    ("priceless", starts[8] - 0.06, starts[9] - 0.06),
    ("caves_a", starts[9] - 0.06, WT(9, "eleven") - 0.1),
    ("caves_b", WT(9, "eleven") - 0.1, starts[10] - 0.06),
    ("chain", starts[10] - 0.06, starts[11] - 0.06),
    ("end", starts[11] - 0.06, TOTAL + 1),
]
SUB = {"wide": 2, "climb2": 2, "throw": 2, "jars": 3, "end": 2}
CUTS = [s[1] for s in SHOTS[1:]]
for n_, a_, b_ in SHOTS:
    for q_ in range(1, SUB.get(n_, 1)):
        CUTS.append(a_ + (min(b_, TOTAL) - a_) * q_ / SUB[n_])
CUTS.sort()


def shot_at(t):
    for n, a, b in SHOTS:
        if a <= t < b:
            return n, a, b
    return SHOTS[-1]


def goat_lost_pos(t, a):
    k = ease((t - a) / 1.6)
    return 700 + 120 * k, 1520 + 40 * k


def render(t):
    global ZM
    name, a, b = shot_at(t)
    lt, dur = t - a, max(0.1, b - a)
    n_sub = SUB.get(name, 1)
    ZM = 1.3 if n_sub > 1 and int(lt / (min(b, TOTAL) - a) * n_sub) % 2 == 1 else 1.0
    p = lt / dur
    shake = (0, 0)
    if name in ("dark",) and lt < 0.45:
        shake = (math.sin(lt * 90) * 14 * (1 - lt / 0.45), math.cos(lt * 80) * 10 * (1 - lt / 0.45))
    if name == "wide" or name == "end":
        # herd walks left to right; the lost goat wanders off and (end) peeks back
        zoom = 1.0 + 0.04 * (p if name == "wide" else 0)
        c = Cv(540, 960, zoom)
        landscape(c, t)
        for k, (gx, gy) in enumerate(((120, 1500), (280, 1560), (430, 1480), (600, 1580))):
            goat(c, gx + 40 * math.sin(t * 1.5 + k) + (t * 24 if name == "wide" else 0) % 60, gy, 0.8, face=1, ph=t * 1.3 + k * 0.3)
        shepherd(c, 40 + (t * 30 if name == "wide" else 0) % 60, 1560, 1.15, ph=t * 1.2)
        if name == "wide":
            gx, gy = goat_lost_pos(t, a)
            goat(c, gx, gy, 0.8, body=(176, 128, 86), patch=(120, 80, 50), face=1, ph=t * 1.5)
            if lt > 0.9:
                kk = ease((lt - 0.9) / 0.3)
                c.ell(gx + 4, gy - 22, 130 * kk, 130 * kk, None, outline=RED + (230,), w=8)
            c.text(540, 430, "1947", ("hand", 190), (40, 30, 24), shadow=70)
        else:
            if lt > 0.3:
                kk = ease((lt - 0.3) / 0.5)
                c.text(540, 430, "1947", ("hand", 190), (40, 30, 24), shadow=70)
            # goat peeks out from behind a rock, then runs off
            rx = 760
            c.poly([(rx - 70, 1650), (rx - 50, 1560), (rx + 30, 1540), (rx + 80, 1620), (rx + 60, 1660)], (140, 118, 96))
            if 0.9 < lt:
                kk = ease((lt - 0.9) / 0.5)
                run = ease((lt - 2.0) / 0.9)
                goat(c, rx + 40 + 420 * run, 1620 - 8 * kk, 0.75, body=(176, 128, 86), patch=(120, 80, 50), face=1, ph=t * 3)
                if lt < 1.9:
                    c.text(rx + 40, 1470, "(hi)", ("hand", 60), INK)
            c.ell(rx, 1620, 78, 40, (140, 118, 96))
    elif name == "goatzoom":
        zoom = lerp(1.6, 2.5, ease(p))
        gx = 700 + 120 + 200 * ease(p)
        c = Cv(gx - 40, 1480, zoom)
        landscape(c, t)
        goat(c, gx, 1560, 0.95, body=(176, 128, 86), patch=(120, 80, 50), face=1, ph=t * 1.6)
        qmark(c, gx - 40, 1330, ease((lt - 0.4) / 0.3), 0.8)
        for k, (hx, hy) in enumerate(((gx - 330, 1590), (gx - 190, 1520))):
            goat(c, hx, hy, 0.8, face=1, ph=t * 1.2 + k)
    elif name in ("climb1", "climb2"):
        u0, u1 = (0.0, 0.42) if name == "climb1" else (0.42, 0.78)
        u = lerp(u0, u1, ease(p) * 0.4 + p * 0.6)
        sx, sy = path_pos(u)
        c = Cv(lerp(560, 640, u), sy - 120, 1.15 if name == "climb1" else 1.0)
        cliff_bg(c)
        # sea far below visible in lower area
        c.rect(-300, 2080, 1500, 2300, TEAL)
        shepherd(c, sx, sy, 1.2, ph=t * 1.4, pose="climb")
        if name == "climb1" and lt < 1.0:
            c.text(560, sy - 330, "find the goat!", ("hand", 74), (40, 30, 24), shadow=60)
    elif name == "search":
        sx, sy = path_pos(0.86)
        c = Cv(lerp(700, 720, p), lerp(-480, -520, p), 1.55)
        cliff_bg(c)
        cave_mouth(c)
        shepherd(c, sx, sy, 1.25, ph=t * 0.3, pose="search")
        c.text(sx + 10, sy - 270, "no goat...", ("hand", 74), (40, 30, 24), shadow=60) if lt > 0.4 else None
        qmark(c, sx - 60, sy - 340, ease((lt - 0.7) / 0.3), 0.9)
    elif name == "throw":
        sx, sy = path_pos(0.86)
        tx, ty = CAVE[0] - 10, CAVE[1] + 20
        k = ease(p)
        c = Cv(lerp(740, 800, k), lerp(-560, -760, k), lerp(1.55, 1.9, k))
        cliff_bg(c)
        cave_mouth(c)
        shepherd(c, sx, sy, 1.25, pose="throw", t=min(1.0, lt / 0.25))
        if lt > 0.2:
            r = min(1.0, (lt - 0.2) / 0.55)
            rx = lerp(sx + 30, tx, r)
            ry = lerp(sy - 170, ty, r) - math.sin(r * math.pi) * 150
            rock_prop(c, rx, ry, 1.6)
            for q in range(4):
                rr = max(0.0, r - 0.05 * (q + 1))
                c.ell(lerp(sx + 30, tx, rr), lerp(sy - 170, ty, rr) - math.sin(rr * math.pi) * 150, 5, 5, (255, 255, 255, 120 - q * 25))
    elif name == "dark":
        c = Cv(540, 960, 1.0, shake)
        c.vgrad(-200, 2200, (8, 6, 6), (22, 16, 14))
        c.ell(540, 900, 380, 460, (14, 10, 10))
        k = ease(lt / 0.12)
        for r_, a_ in ((120, 220), (220, 150), (340, 90)):
            c.ell(540, 980, r_ * (0.4 + 1.2 * ease(lt / 0.5)), r_ * (0.4 + 1.2 * ease(lt / 0.5)), None, outline=(255, 210, 120, int(a_ * (1 - ease(lt / 0.8)))), w=10)
        for q in range(9):
            ang = q * 0.7 + 0.3
            d_ = 60 + 330 * ease(lt / 0.5)
            c.poly([(540 + math.cos(ang) * d_, 980 + math.sin(ang) * d_), (540 + math.cos(ang + 0.2) * (d_ + 40), 980 + math.sin(ang + 0.2) * (d_ + 40)),
                    (540 + math.cos(ang - 0.15) * (d_ + 26), 980 + math.sin(ang - 0.15) * (d_ + 26))], TERRA + (int(255 * (1 - ease(lt / 1.2))),))
        c.text(540, 560, "CRASH!", ("hand", 150), (255, 220, 150), shadow=140) if lt > 0.05 else None
    elif name in ("jars", "scroll"):
        glow = ease(lt / 0.5)
        zoom = lerp(1.0, 1.25, ease(p)) if name == "jars" else lerp(1.25, 1.6, ease(p))
        c = Cv(540, 1000 if name == "jars" else 920, zoom)
        cave_interior(c, t, glow)
        pos = [(160, 1196), (300, 1196), (440, 1196), (640, 1196), (780, 1196), (920, 1196)]
        for k, (jx, jy) in enumerate(pos):
            ap = back((lt - 0.08 * k) / 0.3) if name == "jars" else 1.0
            jar(c, jx, jy, 1.25 * max(0.01, ap), glow=glow * (1.0 if k == 3 else 0.35), lid=(k != 3 or name == "jars" and lt < 1.0))
        if name == "scroll":
            u = ease(lt / 0.7)
            scroll(c, 640, 1196 - 130 - 230 * u, 1.7, open_=ease((lt - 0.35) / 0.6))
            sparkle(c, 640 + 120 * math.sin(t * 6), 760 + 40 * math.cos(t * 5), 36 * (0.6 + 0.4 * math.sin(t * 9)))
            sparkle(c, 540, 700, 24 * (0.6 + 0.4 * math.cos(t * 8)))
    elif name == "years":
        c = Cv(540, 960, 1.0)
        studio_bg(c, 0.4)
        k = ease(lt / 1.2)
        scroll(c, 540, 820, 3.0, open_=1.0)
        yrs = int(2000 * k)
        c.text(540, 340, "{:,} years".format(yrs), ("sans", 120, True), INK, shadow=50)
        c.text(540, 1500, "BC to AD", ("hand", 80), (110, 80, 50)) if lt > 1.0 else None
    elif name == "oldest":
        zoom = lerp(1.0, 1.18, ease(p))
        c = Cv(540, 960, zoom)
        studio_bg(c, 0.3)
        scroll(c, 540, 900, 3.4, open_=1.0)
        k = back((lt - 0.2) / 0.35)
        c.rect(120, 380 - 4, 960, 520, (255, 255, 255, 235), r=26)
        c.text(540, 450, "oldest known copies", ("sans", 56, True), INK) if k > 0.1 else None
        c.text(540, 1480, "of books of the Bible", ("hand", 84), (130, 70, 40))
    elif name in ("scale", "price"):
        c = Cv(540, 960, 1.0 + (0.12 * ease(p) if name == "price" else 0))
        studio_bg(c, 0.2)
        cx_, cy_ = 540, 1150
        tilt = lerp(0.0, 0.26, ease(lt / 0.8)) if name == "price" else lerp(0.0, 0.0, 1)
        if name == "scale":
            tilt = -0.0 + 0.04 * math.sin(lt * 6)
        c.poly([(cx_ - 26, cy_ + 360), (cx_ + 26, cy_ + 360), (cx_ + 10, cy_ - 20), (cx_ - 10, cy_ - 20)], (120, 96, 70))
        c.rect(cx_ - 150, cy_ + 350, cx_ + 150, cy_ + 390, (92, 70, 48), r=14)
        L = 330
        ax, ay = cx_ - L * math.cos(tilt), cy_ - 20 - L * math.sin(tilt)
        bx, by = cx_ + L * math.cos(tilt), cy_ - 20 + L * math.sin(tilt)
        c.line([(ax, ay), (bx, by)], (150, 120, 80), 18)
        for (px, py) in ((ax, ay), (bx, by)):
            c.line([(px, py), (px, py + 190)], (150, 120, 80), 6)
            c.poly([(px - 130, py + 190), (px + 130, py + 190), (px + 90, py + 230), (px - 90, py + 230)], (120, 96, 70))
        # left pan: scroll (heavier = value), right pan: a few coins
        scroll(c, ax, ay + 100, 1.0, open_=1.0, lines=False)
        for q in range(3):
            c.ell(bx - 40 + q * 40, by + 168 - (q % 2) * 6, 30, 30, GOLD, outline=(176, 130, 40), w=4)
        if name == "price":
            k = back((lt - 0.2) / 0.35)
            c.rect(250, 420, 830, 560, (255, 255, 255, 240), r=28)
            c.text(540, 490, "a few pounds", ("sans", 72, True), (200, 60, 50))
            sparkle(c, ax, ay + 30, 26)
        else:
            c.text(540, 460, "the first sale...", ("hand", 100), (110, 80, 50))
    elif name == "priceless":
        c = Cv(540, 960, lerp(1.0, 1.12, ease(p)))
        c.vgrad(-200, 2200, (18, 20, 36), (44, 40, 66))
        c.ell(540, 1000, 480, 520, (255, 205, 110, 120))
        c.rect(180, 640, 900, 1300, (200, 225, 250, 25), r=40)
        c.rect(200, 660, 880, 1280, (255, 255, 255, 10), r=34)
        scroll(c, 540, 960, 3.0, open_=1.0)
        c.rect(150, 1300, 930, 1370, (90, 70, 50), r=14)
        for q in range(8):
            sparkle(c, 540 + 330 * math.cos(t * 1.4 + q * 0.8), 980 + 300 * math.sin(t * 1.4 + q * 0.8), 18 + 10 * math.sin(t * 7 + q))
        k = back((lt - 0.15) / 0.3)
        c.text(540, 420, "priceless", ("hand", 170 * max(0.4, k)), GOLD, shadow=120)
        c.text(540, 1500, "Jerusalem", ("sans", 52, True), (210, 210, 230)) if lt > 0.9 else None
    elif name in ("caves_a", "caves_b"):
        z = 0.55 if name == "caves_a" else lerp(0.55, 0.62, ease(p))
        c = Cv(760, 400, z)
        cliff_bg(c)
        pts = [(520, 1500), (840, 1450), (620, 1180), (980, 1100), (560, 820), (900, 760), (640, 480), (960, 400), (580, 140), (860, 60), (700, -220)]
        n_on = 0
        if name == "caves_a":
            n_on = int(11 * ease(lt / max(0.3, dur)))
        else:
            n_on = 11
        for k, (cx_, cy_) in enumerate(pts):
            on = k < n_on
            c.ell(cx_, cy_, 70, 82, ROCK_DD)
            c.ell(cx_, cy_ + 4, 58, 70, (14, 10, 10))
            if on:
                c.ell(cx_, cy_ + 10, 56, 66, GOLD + (190,))
                c.text(cx_, cy_ + 8, str(k + 1), ("sans", 74, True), INK)
        if name == "caves_a":
            c.text(760, -350, "hundreds more...", ("hand", 130), (40, 30, 24), shadow=70)
        else:
            c.text(760, -350, "11 caves", ("hand", 190), (40, 30, 24), shadow=70)
            k = ease((lt - 0.5) / 0.9)
            c.text(760, -110, "≈ {:,} manuscripts".format(int(900 * k)), ("sans", 70, True), (130, 40, 30), shadow=70)
    elif name == "chain":
        c = Cv(540, 960, 1.0)
        studio_bg(c, 0.25)
        pos = [(540, 470), (540, 790), (540, 1110), (540, 1430)]
        icons = ["goat", "rock", "cave", "scroll"]
        for k, ((px, py), ic) in enumerate(zip(pos, icons)):
            ta = k * 0.5
            if lt < ta:
                continue
            kk = back((lt - ta) / 0.3)
            if k > 0:
                aa = ease((lt - ta + 0.2) / 0.25)
                c.line([(px, pos[k - 1][1] + 120), (px, pos[k - 1][1] + 120 + (py - pos[k - 1][1] - 240) * aa)], RED, 12)
                if aa > 0.95:
                    c.poly([(px - 24, py - 124), (px + 24, py - 124), (px, py - 90)], RED)
            c.ell(px, py, 118 * kk, 118 * kk, (255, 255, 255, 235), outline=(210, 190, 150), w=6)
            if ic == "goat":
                goat(c, px - 6, py + 30, 1.0 * kk, body=(176, 128, 86), patch=(120, 80, 50))
            elif ic == "rock":
                rock_prop(c, px, py + 10, 5.0 * kk)
            elif ic == "cave":
                c.ell(px, py + 10, 66 * kk, 80 * kk, ROCK_DD)
                c.ell(px, py + 16, 52 * kk, 66 * kk, (14, 10, 10))
            else:
                scroll(c, px, py, 0.9 * kk, open_=1.0, lines=False)
        c.text(540, 200, "all because of", ("hand", 96), (110, 80, 50))
        c.text(540, 1580, "one lost goat", ("hand", 130), (200, 60, 50), shadow=40) if lt > 1.6 else None
    else:
        c = Cv()
        c.vgrad(0, 1920, (0, 0, 0), (0, 0, 0))
    return c.out()


# ---------------------------------------------------------------- captions + frame
def captions(img, t):
    for i in range(len(LINES)):
        if starts[i] - 0.05 <= t < starts[i] + D[i] + 0.15:
            words = LINES[i].split()
            cur = 0
            for j, o in enumerate(TW[i]):
                if t >= starts[i] + o - 0.05:
                    cur = j
            c0 = cur // 3 * 3
            txt = " ".join(words[c0:c0 + 3])
            f = font("sans", 96, True)
            while f.getlength(txt) > W - 100:
                f = font("sans", f.size - 2, True)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            dl.text((W / 2 + 2, H * 0.88 + 4), txt, font=f, fill=(0, 0, 0, 215), anchor="mm")
            lay = lay.filter(ImageFilter.GaussianBlur(6))
            ImageDraw.Draw(lay).text((W / 2, H * 0.88), txt, font=f, fill=(255, 255, 255, 255), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0, 150))
            img.alpha_composite(lay)
            return


VIGN = None
GRAIN = np.random.default_rng(5).normal(0, 3.0, (H + 64, W + 64, 1)).astype(np.float32)


def frame(fi):
    global VIGN
    t = fi / FPS
    img = render(t).convert("RGBA")
    # bottom shade so captions stay readable on bright scenes
    sh = np.zeros((H, W, 4), np.uint8)
    ramp = np.clip((np.arange(H) - H * 0.74) / (H * 0.26), 0, 1) ** 1.3 * 120
    sh[..., 3] = ramp[:, None].astype(np.uint8)
    img.alpha_composite(Image.fromarray(sh, "RGBA"))
    # flash on key beats
    for ft in (WT(3, "pottery"), WT(4, "scrolls")):
        if 0 <= t - ft < 0.18:
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(110 * (1 - (t - ft) / 0.18)))))
    captions(img, t)
    if VIGN is None:
        yy, xx = np.mgrid[0:H // 4, 0:W // 4]
        dd = np.sqrt(((xx - W / 8) / (W / 8)) ** 2 + ((yy - H / 8) / (H / 8)) ** 2)
        v = np.clip(1.0 - 0.30 * np.clip(dd - 0.55, 0, None) ** 1.4, 0.6, 1)
        VIGN = np.asarray(Image.fromarray((v * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR))[..., None] / 255.0
    rgb = np.asarray(img.convert("RGB")).astype(np.float32) * VIGN
    gy, gx = (fi * 37) % 64, (fi * 91) % 64
    rgb += GRAIN[gy:gy + H, gx:gx + W]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "still":
        for a in sys.argv[2:]:
            frame(int(a)).save(f"still_{int(a):05d}.png")
    elif cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for n, a, b in SHOTS:
            print(n, round(a, 2), round(min(b, TOTAL), 2))
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
        p.stdin.close()
        p.wait()
