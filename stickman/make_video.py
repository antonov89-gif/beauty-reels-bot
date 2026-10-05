"""Free animated stickman explainer video generator.

Draws one consistent hand-drawn style character procedurally (no AI image model,
so the character is identical in every scene), animates each scene frame by frame,
voices the script with offline TTS (espeak-ng + MBROLA), synthesizes soft background
music and assembles everything with ffmpeg.

Usage:  python3 make_video.py            # renders out/five_minute_rule.mp4
        python3 make_video.py --voice-dir my_wavs   # use your own voice files
                                                    # (scene01.wav ... scene10.wav)
"""
import argparse
import math
import os
import shutil
import subprocess
import wave
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 30
S = 2  # supersampling factor for anti-aliased lines

BG = (250, 226, 170)
INK = (28, 24, 22)
WHITE = (255, 255, 255)
SHIRT = (86, 150, 196)
SHIRT_DARK = (62, 118, 160)
PANTS = (70, 70, 84)
GREY = (150, 150, 150)
YELLOW = (255, 214, 72)
GREEN = (110, 190, 100)
RED = (224, 88, 72)
SWEAT = (120, 190, 240)

FONT_PATH = "/usr/share/fonts/opentype/comic-neue/ComicNeue-Bold.otf"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

# ---------------------------------------------------------------------------
# Script: (voice line, caption) per scene. Scene drawing functions below.
# ---------------------------------------------------------------------------
SCRIPT = [
    ("Ever feel too overwhelmed to even start?", "Overwhelmed?"),
    ("The work feels heavy, before you even open your laptop.", "So heavy..."),
    ("So instead, you scroll. Telling yourself you'll start later.", "I'll start later..."),
    ("The problem isn't laziness. It's that the task feels too big.", "Not laziness"),
    ("Here's a simple trick. The five minute rule.", "The 5-Minute Rule"),
    ("Set a timer for just five minutes, and promise yourself you'll stop after that.", "Just 5 minutes"),
    ("Once you start, the pressure disappears. You're just doing a little, not everything.", "Just a little"),
    ("And something surprising happens. Progress feels good. Momentum builds.", "Momentum!"),
    ("Five minutes often turns into much more. Now the task isn't scary anymore. It feels doable.", "Doable."),
    ("Remember, motivation doesn't come before action. Just start, for five minutes.", "Just Start."),
]


# ---------------------------------------------------------------------------
# Hand-drawn pen: every point gets a smooth, seed-dependent wobble so lines look
# drawn by hand, and the seed changes a few times per second ("line boil").
# ---------------------------------------------------------------------------
class Pen:
    def __init__(self, img, boil):
        self.d = ImageDraw.Draw(img)
        r = np.random.default_rng(boil)
        self.ph = r.uniform(0, 2 * math.pi, 4)
        self.amp = 1.6

    def j(self, x, y):
        p = self.ph
        dx = self.amp * math.sin(0.031 * x + 0.047 * y + p[0])
        dy = self.amp * math.cos(0.043 * x - 0.029 * y + p[1])
        return ((x + dx) * S, (y + dy) * S)

    @staticmethod
    def densify(pts, step=10):
        out = []
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
            for i in range(n):
                t = i / n
                out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
        out.append(pts[-1])
        return out

    def line(self, pts, w=5, col=INK, closed=False):
        if closed:
            pts = list(pts) + [pts[0]]
        q = [self.j(*p) for p in self.densify(pts)]
        self.d.line(q, fill=col, width=int(w * S), joint="curve")
        r = w * S / 2
        if not closed:
            for x, y in (q[0], q[-1]):
                self.d.ellipse((x - r, y - r, x + r, y + r), fill=col)

    def poly(self, pts, fill, w=5, outline=INK):
        q = [self.j(*p) for p in self.densify(list(pts) + [pts[0]])]
        self.d.polygon(q, fill=fill)
        if w:
            self.d.line(q, fill=outline, width=int(w * S), joint="curve")

    def ellipse_pts(self, cx, cy, rx, ry, a0=0, a1=360, n=None):
        n = n or max(16, int((rx + ry) * 0.6))
        return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                 cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

    def circle(self, cx, cy, r, fill=WHITE, w=5, ry=None):
        pts = self.ellipse_pts(cx, cy, r, ry or r)[:-1]
        if fill is None:
            self.line(pts, w, closed=True)
        else:
            self.poly(pts, fill, w)

    def dot(self, x, y, r, col=INK):
        X, Y = self.j(x, y)
        self.d.ellipse((X - r * S, Y - r * S, X + r * S, Y + r * S), fill=col)

    def rect(self, x0, y0, x1, y1, fill, w=5):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, w)

    def text(self, x, y, s, size, col=INK, anchor="mm"):
        f = font(size)
        self.d.text((x * S, y * S), s, font=f, fill=col, anchor=anchor)


_fonts = {}


def font(size):
    if size not in _fonts:
        _fonts[size] = ImageFont.truetype(FONT_PATH, int(size * S))
    return _fonts[size]


# ---------------------------------------------------------------------------
# Easing helpers
# ---------------------------------------------------------------------------
def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ease(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def back(t):
    t = clamp(t)
    c = 1.9
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2


def seg(x, y, ang, length):
    a = math.radians(ang)
    return x + length * math.cos(a), y + length * math.sin(a)


# ---------------------------------------------------------------------------
# The character. (x, y) = neck point. Angles: 0=right, 90=down (screen space).
# ---------------------------------------------------------------------------
def character(p, x, y, s=1.0, la=(115, 100), ra=(65, 80), ll=(97, 92), rl=(83, 88),
              face="smile", blink=False, look=(0, 0), sweat=None, head_dy=0,
              legs=True, right_hand_item=None):
    L = lambda v: v * s  # noqa: E731
    hips_y = y + L(165)
    # legs
    if legs:
        for hx, (a1, a2), side in ((-24, ll, -1), (24, rl, 1)):
            kx, ky = seg(x + L(hx), hips_y, a1, L(88))
            fx, fy = seg(kx, ky, a2, L(88))
            p.line([(x + L(hx), hips_y), (kx, ky), (fx, fy)], L(5.5))
            p.circle(fx + side * L(12), fy + L(4), L(22), fill=INK, w=L(3), ry=L(11))
    # arms (drawn before torso so sleeves cover the shoulder joint)
    hands = []
    for sx, (a1, a2) in ((-46, la), (46, ra)):
        sh = (x + L(sx), y + L(24))
        el = seg(*sh, a1, L(82))
        hd = seg(*el, a2, L(78))
        p.line([sh, el, hd], L(5.5))
        hands.append((sh, el, hd, a1))
    # torso / shirt
    torso = [(x - L(40), y + L(6)), (x + L(40), y + L(6)), (x + L(56), y + L(28)),
             (x + L(58), hips_y), (x - L(58), hips_y), (x - L(56), y + L(28))]
    p.poly(torso, SHIRT, L(5))
    p.line([(x - L(16), y + L(10)), (x, y + L(34)), (x + L(16), y + L(10))], L(4))
    p.line([(x, y + L(60)), (x, y + L(150))], L(3), col=SHIRT_DARK)
    # sleeves
    for sh, el, hd, a1 in hands:
        e = seg(*sh, a1, L(34))
        p.line([sh, e], L(36))
        p.line([sh, e], L(27), col=SHIRT)
    # hands
    for i, (sh, el, hd, a1) in enumerate(hands):
        if i == 1 and right_hand_item:
            right_hand_item(p, *hd)
        p.circle(hd[0], hd[1], L(17), WHITE, L(4.5))
    # head
    hx, hy = x, y - L(108) + head_dy
    p.circle(hx, hy, L(112), WHITE, L(5.5))
    ex, ey = look
    for sx in (-38, 38):
        cx, cy = hx + L(sx + ex), hy + L(-6 + ey)
        if blink:
            p.line([(cx - L(10), cy), (cx + L(10), cy)], L(4))
        elif face == "happy":
            p.line(p.ellipse_pts(cx, cy + L(4), L(11), L(9), 200, 340, 10), L(4.5))
        else:
            p.dot(cx, cy, L(9.5))
    mx, my = hx + L(ex * 0.6), hy + L(38 + ey * 0.4)
    if face == "smile":
        p.line(p.ellipse_pts(mx, my - L(10), L(22), L(14), 30, 150, 14), L(4.5))
    elif face == "worried":
        p.line([(mx - L(20), my + L(4)), (mx - L(7), my - L(3)), (mx + L(7), my + L(4)), (mx + L(20), my - L(2))], L(4.5))
        for sx, d in ((-38, 1), (38, -1)):
            bx = hx + L(sx)
            p.line([(bx - L(14), hy - L(32) - d * L(6)), (bx + L(14), hy - L(32) + d * L(6))], L(4.5))
    elif face == "happy":
        pts = p.ellipse_pts(mx, my - L(6), L(28), L(24), 0, 180, 16)
        p.poly(pts, INK, L(3))
        p.circle(mx, my + L(10), L(10), RED, 0, ry=L(5))
    elif face == "neutral":
        p.line([(mx - L(14), my), (mx + L(14), my)], L(4.5))
    if sweat is not None:
        sx, sy = hx + L(95), hy - L(40) + L(40) * sweat
        drop = [(sx, sy - L(22))] + p.ellipse_pts(sx, sy, L(11), L(12), -20, 200, 12)
        p.poly(drop, SWEAT, L(3.5))
    return hands


# ---------------------------------------------------------------------------
# Props
# ---------------------------------------------------------------------------
def paper_stack(p, x, base_y, n, sway):
    for i in range(n):
        y = base_y - i * 26
        off = math.sin(i * 1.7) * 10 + sway * i * 0.8
        p.rect(x - 85 + off, y - 24, x + 85 + off, y, WHITE, 4)
        p.line([(x - 60 + off, y - 12), (x + 40 + off, y - 12)], 2.5, GREY)


def laptop(p, x, y, sc=1.0, glow=0.0):
    L = lambda v: v * sc  # noqa: E731
    p.poly([(x - L(130), y - L(170)), (x + L(110), y - L(170)), (x + L(130), y), (x - L(110), y)], (90, 95, 110), L(5))
    col = tuple(int(c + (255 - c) * glow * 0.5) for c in (170, 210, 240))
    p.poly([(x - L(112), y - L(155)), (x + L(96), y - L(155)), (x + L(112), y - L(14)), (x - L(96), y - L(14))], col, L(3))
    p.rect(x - L(160), y, x + L(160), y + L(18), (120, 125, 140), L(5))


def phone(p, x, y, scroll):
    p.poly([(x - 34, y - 60), (x + 34, y - 60), (x + 34, y + 60), (x - 34, y + 60)], INK, 4)
    p.rect(x - 26, y - 50, x + 26, y + 50, (170, 215, 245), 0)
    for i in range(6):
        yy = y - 50 + ((i * 22 - scroll) % 110)
        if y - 46 < yy < y + 46:
            p.line([(x - 18, yy), (x + 14, yy)], 4, (240, 120, 150) if i % 2 else (90, 120, 200))


def clock(p, x, y, r, minutes, label=None):
    p.circle(x, y, r, WHITE, 5)
    for k in range(12):
        a = math.radians(k * 30)
        p.line([(x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82),
                (x + math.cos(a) * r * 0.92, y + math.sin(a) * r * 0.92)], 3)
    am = math.radians(minutes * 6 - 90)
    ah = math.radians(minutes * 0.5 - 90)
    p.line([(x, y), (x + math.cos(am) * r * 0.75, y + math.sin(am) * r * 0.75)], 5)
    p.line([(x, y), (x + math.cos(ah) * r * 0.5, y + math.sin(ah) * r * 0.5)], 7)
    p.dot(x, y, 7)


def mountain(p, x, base_y, h, label=True):
    wdt = h * 1.25
    p.poly([(x - wdt, base_y), (x - wdt * 0.15, base_y - h), (x + wdt * 0.05, base_y - h * 0.9),
            (x + wdt, base_y)], (160, 150, 140), 6)
    if h > 120:
        p.poly([(x - wdt * 0.15 - h * 0.12 * 1.0, base_y - h * 0.86), (x - wdt * 0.15, base_y - h),
                (x + wdt * 0.05, base_y - h * 0.9), (x + wdt * 0.08, base_y - h * 0.8),
                (x - wdt * 0.04, base_y - h * 0.84)], WHITE, 4)
    if label and h > 200:
        p.text(x, base_y - h * 0.4, "THE TASK", h * 0.13, WHITE)


def bulb(p, x, y, sc, glow):
    if sc <= 0.02:
        return
    for k in range(8):
        a = math.radians(k * 45 - 90)
        r0, r1 = 70 * sc, (95 + 12 * glow) * sc
        p.line([(x + math.cos(a) * r0, y + math.sin(a) * r0), (x + math.cos(a) * r1, y + math.sin(a) * r1)], 5 * sc, (230, 160, 40))
    p.circle(x, y, 50 * sc, YELLOW, 5 * sc)
    p.rect(x - 22 * sc, y + 44 * sc, x + 22 * sc, y + 72 * sc, GREY, 4 * sc)
    p.line([(x - 12 * sc, y + 10 * sc), (x - 4 * sc, y - 10 * sc), (x + 4 * sc, y + 10 * sc), (x + 12 * sc, y - 10 * sc)], 3 * sc, (200, 130, 20))


def handwrite(p, x, y, text, size, t, cps=14, col=INK, anchor="mm"):
    n = int(clamp(t * cps, 0, len(text)))
    if n <= 0:
        return
    full_w = font(size).getlength(text) / S
    left = x - full_w / 2 if anchor == "mm" else x
    p.text(left, y, text[:n], size, col, anchor="lm")
    if n < len(text):
        # pencil tip following the writing
        cx = left + font(size).getlength(text[:n]) / S
        p.line([(cx + 6, y + 10), (cx + 40, y - 40)], 9, (240, 190, 80))
        p.dot(cx + 6, y + 10, 4)


# ---------------------------------------------------------------------------
# Scenes: f(p, t, T) draws one frame at time t of a scene lasting T seconds.
# ---------------------------------------------------------------------------
def blink_at(t, period=3.1, off=0.7):
    return ((t + off) % period) < 0.12


def sc1(p, t, T):
    shake = math.sin(t * 38) * 2.5
    for i, (x, n) in enumerate(((1180, 13), (1390, 17), (1590, 11))):
        grow = back((t - 0.15 * i) / 0.7)
        paper_stack(p, x, 900, max(1, int(n * clamp(grow, 0, 1.1))), math.sin(t * 2 + i))
    character(p, 620 + shake, 520, 1.0, la=(125, 60), ra=(55, 120), face="worried",
              blink=blink_at(t), look=(14, -4), sweat=(t * 0.6) % 1)
    handwrite(p, 620, 140, SCRIPT[0][1], 92, t - 0.5)


def sc2(p, t, T):
    squash = math.sin(t * 3.2) * 8
    x = 760 + t * 18
    hands = character(p, x, 520 + squash, 1.0, la=(-115, -95), ra=(-65, -85), ll=(105, 80), rl=(75, 100),
                      face="worried", blink=blink_at(t), look=(0, 8), sweat=(t * 0.5) % 1, head_dy=10)
    top = min(h[2][1] for h in hands) - 10
    p.rect(x - 190, top - 190, x + 190, top, (205, 150, 90), 6)
    p.line([(x - 190, top - 120), (x + 190, top - 120)], 4, (170, 115, 60))
    p.text(x, top - 62, "WORK", 70, INK)
    for i in range(3):
        yy = top - 220 - ((t * 60 + i * 30) % 60)
        p.line([(x - 120 + i * 120, yy), (x - 120 + i * 120, yy - 25)], 5, (120, 90, 60))
    laptop(p, 1500, 900, 0.9)
    p.text(1500, 960, "(still closed)", 34, (110, 90, 70))
    handwrite(p, 420, 150, SCRIPT[1][1], 90, t - 0.4)


def sc3(p, t, T):
    # couch
    p.rect(520, 690, 1260, 820, (210, 110, 90), 6)
    p.rect(500, 600, 600, 860, (190, 95, 80), 6)
    p.rect(1180, 600, 1280, 860, (190, 95, 80), 6)
    p.rect(560, 820, 600, 880, INK, 0)
    p.rect(1180, 820, 1220, 880, INK, 0)
    thumb = math.sin(t * 9) * 6
    character(p, 880, 515, 1.0, la=(110, 20), ra=(70, 165 + thumb * 0.5), ll=(0, 92), rl=(-10, 95),
              face="neutral", blink=blink_at(t), look=(4, 18),
              right_hand_item=lambda pp, hx, hy: phone(pp, hx - 30, hy - 50, t * 140))
    clock(p, 1560, 330, 120, t * 240)
    handwrite(p, 1450, 560, SCRIPT[2][1], 70, t - 0.6, cps=12)
    if t > 1.2:
        z = (t * 1.5) % 3
        for k in range(int(z) + 1):
            p.text(1180 + k * 40, 380 - k * 40, "z", 40 + k * 10, (120, 110, 100))


def sc4(p, t, T):
    h = 560 + 60 * ease(t / T)
    mountain(p, 1180, 960, h)
    character(p, 330, 760, 0.45, la=(120, 100), ra=(60, 80), face="worried",
              blink=blink_at(t), look=(16, -12))
    p.line([(0, 960), (W, 960)], 6)
    handwrite(p, 380, 140, SCRIPT[3][1], 84, t - 0.3)
    if t > T * 0.55:
        k = ease((t - T * 0.55) / 0.5)
        p.text(330, 520 - 40 * k, "?!", 70 * k + 1, RED)


def sc5(p, t, T):
    pop = back((t - 0.6) / 0.5)
    bulb(p, 960, 160, pop, math.sin(t * 8))
    raise_k = ease((t - 0.4) / 0.4)
    character(p, 960, 470, 1.0, la=(115, 100), ra=(65 - 105 * raise_k, 80 - 155 * raise_k),
              face="happy" if t > 0.7 else "smile", blink=blink_at(t), look=(0, -4))
    k = back((t - 1.0) / 0.5)
    if k > 0:
        p.text(960, 980, SCRIPT[4][1], 110 * k, INK)


def sc6(p, t, T):
    remaining = max(0, 300 - int(t * 7))
    def timer(pp, hx, hy):
        cx, cy = hx + 120, hy - 60
        pp.rect(cx - 15, cy - 140, cx + 15, cy - 110, RED, 4)
        pp.circle(cx, cy, 115, RED, 6)
        pp.circle(cx, cy, 88, WHITE, 5)
        pp.text(cx, cy, f"{remaining // 60}:{remaining % 60:02d}", 58)
        a = math.radians(-90 + (300 - remaining) * 1.2)
        pp.line([(cx + math.cos(a) * 92, cy + math.sin(a) * 92), (cx + math.cos(a) * 108, cy + math.sin(a) * 108)], 7, YELLOW)
    character(p, 760, 470, 1.0, la=(115, 100), ra=(20, -30),
              face="smile", blink=blink_at(t), look=(14, 0), right_hand_item=timer)
    handwrite(p, 1470, 260, SCRIPT[5][1], 84, t - 0.4)
    k = ease((t - 2.0) / 0.4)
    if k > 0:
        p.text(1470, 400, "then you can stop", 46 * k + 1, (110, 90, 70))


def sc7(p, t, T):
    type_l = math.sin(t * 18) * 8
    type_r = math.sin(t * 18 + math.pi) * 8
    character(p, 760, 575, 1.0, la=(60, 25 + type_l), ra=(30, 25 + type_r),
              face="smile", blink=blink_at(t), look=(18, 10))
    p.rect(480, 720, 1440, 750, (180, 130, 80), 6)
    p.rect(520, 750, 1400, 1000, (200, 150, 100), 6)
    p.line([(960, 790), (960, 960)], 4, (160, 110, 70))
    laptop(p, 1060, 720, 1.0, glow=0.5 + 0.5 * math.sin(t * 4))
    for i in range(4):
        st = 0.6 + i * 0.7
        if t > st:
            k = clamp((t - st) / 1.2)
            x, y = 1060 + (i - 1.5) * 70, 500 - 160 * k
            if k < 1:
                p.line([(x - 14, y), (x - 2, y + 12), (x + 18, y - 14)], 7, GREEN)
    handwrite(p, 960, 150, SCRIPT[6][1], 90, t - 0.4)


def sc8(p, t, T):
    fill = ease(t / (T * 0.85))
    p.rect(460, 210, 1460, 280, WHITE, 6)
    if fill > 0.01:
        p.rect(470, 220, 470 + 980 * fill * 0.92, 270, GREEN, 0)
    p.text(960, 245, f"{int(fill * 92)}%", 46)
    jump = abs(math.sin(t * 5)) * 60
    character(p, 960, 560 - jump, 1.0, la=(-150, -115), ra=(-30, -65),
              ll=(100, 92) if jump < 30 else (110, 60), rl=(80, 88) if jump < 30 else (70, 120),
              face="happy", blink=blink_at(t))
    rng = np.random.default_rng(3)
    for i in range(40):
        x0 = rng.uniform(100, 1820)
        sp = rng.uniform(120, 260)
        y = -40 + ((t * sp + rng.uniform(0, 1100)) % 1150)
        col = [RED, YELLOW, GREEN, SHIRT, (200, 120, 220)][i % 5]
        a = t * 4 + i
        p.poly([(x0 + 10 * math.cos(a), y + 6 * math.sin(a)), (x0 - 10 * math.cos(a), y - 6 * math.sin(a)),
                (x0 - 10 * math.cos(a) + 6, y - 6 * math.sin(a) + 8), (x0 + 10 * math.cos(a) + 6, y + 6 * math.sin(a) + 8)], col, 0)
    handwrite(p, 960, 120, SCRIPT[7][1], 96, t - 0.4)


def sc9(p, t, T):
    k = ease(t / 2.0)
    h = 600 - 450 * k
    p.line([(0, 960), (W, 960)], 6)
    mountain(p, 960, 960, h, label=k < 0.3)
    top_y = 960 - h
    climb = ease((t - 2.0) / 1.2)
    cx = 600 + (945 - 600) * climb
    cy = 760 + (top_y - 252 - 760) * climb
    character(p, cx, cy, 0.75, la=(120, 100), ra=(-40 if climb >= 1 else 60, -60 if climb >= 1 else 80),
              face="happy" if climb >= 1 else "smile", blink=blink_at(t))
    if climb >= 1:
        fx = cx + 75
        fy = cy - 45
        wv = math.sin(t * 6) * 8
        p.line([(fx, fy + 40), (fx, fy - 140)], 6)
        p.poly([(fx, fy - 140), (fx + 110, fy - 115 + wv), (fx, fy - 85)], RED, 4)
    handwrite(p, 960, 150, SCRIPT[8][1], 110, t - 2.2)


def sc10(p, t, T):
    wave = math.sin(t * 7) * 22
    character(p, 620, 470, 1.0, la=(115, 100), ra=(-40, -75 + wave), face="smile",
              blink=blink_at(t), look=(10, 0))
    k = back((t - 0.5) / 0.6)
    if k > 0:
        p.text(1320, 450, SCRIPT[9][1], 140 * k)
    k2 = ease((t - 1.6) / 0.5)
    if k2 > 0:
        clock(p, 1320, 700, 90 * k2 + 1, t * 30)
        p.text(1320, 840, "for 5 minutes", 52 * k2 + 1, (110, 90, 70))


SCENES = [sc1, sc2, sc3, sc4, sc5, sc6, sc7, sc8, sc9, sc10]


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
# Vertical (Shorts) layout: the centre of the wide scene sits in a band in the
# middle of a 1080x1920 frame, with a title above and word-by-word subtitles below.
VW, VH = 1080, 1920
V_CROP = (160, 1760)  # part of the wide scene kept in vertical mode
V_BAND_Y = 560
TITLE = "THE 5-MINUTE RULE"


def subtitle_words(line, t, voice_dur):
    """Words of the current 3-word chunk and index of the spoken one.

    Timing is spread over the line by word length, so it works with any voice."""
    words = line.split()
    wts = [len(w) + 2 for w in words]
    tot = sum(wts)
    if t < 0 or t > voice_dur + 0.4:
        return [], -1
    acc, cur = 0.0, len(words) - 1
    for i, w in enumerate(wts):
        acc += w / tot * voice_dur
        if t < acc:
            cur = i
            break
    c0 = cur // 3 * 3
    return words[c0:c0 + 3], cur - c0


def render_vertical(img, idx, t, T, voice_dur, delay):
    x0, x1 = V_CROP
    z = 1.0 + 0.04 * ease(t / T)
    cw, ch = (x1 - x0) * S / z, H * S / z
    cx, cy = (x0 + x1) / 2 * S, H * S / 2
    bw = VW
    bh = int(round(VW * H / (x1 - x0)))
    band = img.resize((bw, bh), Image.LANCZOS, box=(cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2))
    out = Image.new("RGB", (VW, VH), BG)
    out.paste(band, (0, V_BAND_Y))
    d = ImageDraw.Draw(out)
    tf = ImageFont.truetype(FONT_PATH, 92)
    d.text((VW / 2, 330), TITLE, font=tf, fill=INK, anchor="mm")
    tw = tf.getlength(TITLE)
    d.line([(VW / 2 - tw / 2, 392), (VW / 2 + tw / 2, 386)], fill=RED, width=8)
    words, cur = subtitle_words(SCRIPT[idx][0], t - delay, voice_dur)
    if words:
        sf = ImageFont.truetype(FONT_PATH, 96)
        gap = sf.getlength(" ")
        widths = [sf.getlength(w.upper()) for w in words]
        total = sum(widths) + gap * (len(words) - 1)
        scale = min(1.0, (VW - 80) / total)
        if scale < 1.0:
            sf = ImageFont.truetype(FONT_PATH, int(96 * scale))
            gap = sf.getlength(" ")
            widths = [sf.getlength(w.upper()) for w in words]
            total = sum(widths) + gap * (len(words) - 1)
        x = (VW - total) / 2
        for i, (w, ww) in enumerate(zip(words, widths)):
            col = YELLOW if i == cur else WHITE
            d.text((x, 1470), w.upper(), font=sf, fill=col, anchor="lm", stroke_width=7, stroke_fill=INK)
            x += ww + gap
    return out


def render_frame(args):
    idx, t, T, frame_no, path = args[:5]
    vertical = len(args) > 5
    img = Image.new("RGB", (W * S, H * S), BG)
    p = Pen(img, boil=frame_no // 4)  # new wobble every 4 frames (~7.5/s)
    SCENES[idx](p, t, T)
    if vertical:
        img = render_vertical(img, idx, t, T, *args[5:])
    else:
        # gentle push-in camera
        z = 1.0 + 0.04 * ease(t / T)
        cw, ch = W * S / z, H * S / z
        x0, y0 = (W * S - cw) / 2, (H * S - ch) / 2
        img = img.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
    img.save(path, quality=92)


def tts(text, path):
    raw = path + ".raw.wav"
    subprocess.run(["espeak-ng", "-v", "mb-us2", "-s", "140", "-p", "45", "-w", raw, text], check=True)
    # warm it up a little: slight low boost, normalize
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    "aresample=44100,bass=g=3,loudnorm=I=-16:TP=-1.5", "-ac", "1", path], check=True)
    os.remove(raw)


def wav_len(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out)


def music(path, dur, sr=44100):
    """Soft synthesized pad + pluck progression (royalty free, generated here)."""
    t = np.arange(int(dur * sr)) / sr
    chords = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
    bar = 2.4
    out = np.zeros_like(t)
    for i in range(int(dur / bar) + 1):
        ch = chords[i % 4]
        s0 = int(i * bar * sr)
        n = int(bar * 1.3 * sr)
        tt = np.arange(n) / sr
        env = np.minimum(1, tt / 0.6) * np.exp(-tt / 2.2)
        sig = sum(np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt) for f in ch) * env * 0.08
        # pluck arpeggio
        for k, f in enumerate(ch + [ch[0] * 2]):
            st = int(k * bar / 4 * sr)
            m = int(0.8 * sr)
            pt = np.arange(m) / sr
            pl = np.sin(2 * np.pi * f * 2 * pt) * np.exp(-pt * 6) * 0.06
            seg_ = slice(st, min(n, st + m))
            sig[seg_] += pl[: seg_.stop - seg_.start]
        e = min(len(out), s0 + n)
        out[s0:e] += sig[: e - s0]
    fade = np.minimum(1, np.minimum(t / 1.5, (dur - t) / 2.0))
    out = out * fade
    out = (out / max(1e-9, np.abs(out).max()) * 0.5 * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(out.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice-dir", help="folder with scene01.wav..scene10.wav to use instead of offline TTS")
    ap.add_argument("--only", type=int, help="render a preview still of one scene (1-10)")
    ap.add_argument("--t", type=float, default=2.0, help="time (s) of the preview still")
    ap.add_argument("--vertical", action="store_true", help="9:16 Shorts/Reels version with subtitles")
    a = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    work = os.path.join(OUT, "work")
    if a.only:
        os.makedirs(work, exist_ok=True)
        job = (a.only - 1, a.t, 4.0, 0, os.path.join(OUT, f"preview_scene{a.only:02d}.jpg"))
        render_frame(job + ((3.0, 0.15) if a.vertical else ()))
        return

    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    PAD = 0.7
    durations, voices, voice_lens = [], [], []
    for i, (line, _) in enumerate(SCRIPT):
        vp = os.path.join(work, f"voice{i + 1:02d}.wav")
        if a.voice_dir:
            src = os.path.join(a.voice_dir, f"scene{i + 1:02d}.wav")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-ar", "44100", "-ac", "1", vp], check=True)
        else:
            tts(line, vp)
        voices.append(vp)
        voice_lens.append(wav_len(vp))
        durations.append(wav_len(vp) + PAD + (0.5 if i == 0 else 0) + (1.2 if i == len(SCRIPT) - 1 else 0))

    jobs, n = [], 0
    for i, T in enumerate(durations):
        for k in range(int(round(T * FPS))):
            job = (i, k / FPS, T, n, os.path.join(work, f"f{n:05d}.jpg"))
            if a.vertical:
                job += (voice_lens[i], 0.5 if i == 0 else 0.15)
            jobs.append(job)
            n += 1
    print(f"Rendering {n} frames ({sum(durations):.1f}s)...")
    with Pool() as pool:
        for c, _ in enumerate(pool.imap_unordered(render_frame, jobs, chunksize=8)):
            if c % 200 == 0:
                print(f"  {c}/{n}")

    # voice track: each line starts at its scene start (+0.5s delay on scene 1)
    starts = np.concatenate([[0], np.cumsum(durations)[:-1]])
    inputs, filters = [], []
    for i, (vp, st) in enumerate(zip(voices, starts)):
        inputs += ["-i", vp]
        d = int((st + (0.5 if i == 0 else 0.15)) * 1000)
        filters.append(f"[{i}:a]adelay={d}[v{i}]")
    mix = "".join(f"[v{i}]" for i in range(len(voices)))
    voice_path = os.path.join(work, "voice.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex",
                    ";".join(filters) + f";{mix}amix=inputs={len(voices)}:normalize=0[out]",
                    "-map", "[out]", voice_path], check=True)
    total = sum(durations)
    music_path = os.path.join(work, "music.wav")
    music(music_path, total)

    final = os.path.join(OUT, "five_minute_rule_shorts.mp4" if a.vertical else "five_minute_rule.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(work, "f%05d.jpg"),
        "-i", voice_path, "-i", music_path, "-filter_complex",
        "[2:a]volume=0.12[m];[1:a][m]amix=inputs=2:normalize=0:duration=longest,apad[a]",
        "-map", "0:v", "-map", "[a]", "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final], check=True)
    print("Done:", final)


if __name__ == "__main__":
    main()
