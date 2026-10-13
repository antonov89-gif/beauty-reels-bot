"""Infinite-zoom loop Short, reference style: clean outlined vector art on light backgrounds, ~2-3 s per level, no captions.
Chain: hand with EUR 1 coin -> the map on the coin -> Europe -> Switzerland -> Zurich pin -> bank oculus -> vault door porthole
-> gold bars -> engraved stamp (the same hand with the coin) -> loop.   python3 engine30.py still N.. | info | video A B out.mp4"""
import math, subprocess, sys
import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, SS = 1080, 1920, 30, 2
W2, H2 = W * SS, H * SS
CX, CY = W2 / 2, H2 / 2
POPX = "Poppins-ExtraBold.ttf"
BPM = 80.0; BEAT = 60 / BPM
STEP = 4 * BEAT                        # 3 s per stop: move 3 beats, hold 1 beat
MOVE, HOLD = 3 * BEAT, 1 * BEAT
WR = 0.58
INK = (34, 30, 40)
ZUR = (8.541, 47.372)
SPAN0, SPAN_ZH = 40.0, 0.55
R = {"A": 6.0, "M": 1300.0, "B": 6.0, "D": 6.0, "G": 8.0}
ORDER = ["A", "M", "B", "D", "G"]
U_LEVEL = {}; u = 0.0
for k in ORDER: U_LEVEL[k] = u; u += math.log(R[k])
U_TOTAL = u
STOPS = [0.0, U_LEVEL["M"], U_LEVEL["M"] + math.log(SPAN0 / 6.5), U_LEVEL["M"] + math.log(SPAN0 / SPAN_ZH), U_LEVEL["B"],
         U_LEVEL["D"], U_LEVEL["G"], U_LEVEL["G"] + math.log(2.6), U_TOTAL]
NSTEP = len(STOPS) - 1
CYCLE = NSTEP * STEP
NF = int(round(CYCLE * FPS))
T0 = 0.25


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def ease5(x):
    x = min(1.0, max(0.0, x)); return x * x * x * (x * (x * 6 - 15) + 10)


def u_at(tc):
    tc %= CYCLE; k = int(tc // STEP); lt = tc - k * STEP
    return STOPS[k] + (STOPS[k + 1] - STOPS[k]) * ease5(lt / MOVE), k, lt


def top_level(u):
    for k in reversed(ORDER):
        if u >= U_LEVEL[k] - 1e-9: return k, u - U_LEVEL[k]
    return "A", u


def nxt(k): return ORDER[(ORDER.index(k) + 1) % len(ORDER)]


_F = {}
def font(p, s):
    s = max(1, int(s))
    if (p, s) not in _F: _F[(p, s)] = ImageFont.truetype(p, s)
    return _F[(p, s)]


def P(x, y, s): return CX + x * s, CY + y * s
def lw(s, w=0.006): return max(1, int(w * s)) if w * s < 400 else 400


def circ(d, x, y, r, s, fill=None, ow=0.0):
    cx, cy = P(x, y, s); rr = r * s
    if rr < 0.4 or rr > 3e5: return
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=fill, outline=INK if ow else None, width=lw(s, ow) if ow else 0)


def ring(d, x, y, r0, r1, s, fill, ow=0.0):
    cx, cy = P(x, y, s); a, b = r0 * s, r1 * s
    if b < 0.4 or a > 3e5: return
    rm = (a + b) / 2; d.ellipse((cx - rm, cy - rm, cx + rm, cy + rm), outline=fill, width=max(1, int(b - a)))
    if ow:
        for rr in (a, b): d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=INK, width=lw(s, ow))


def poly(d, pts, s, fill, ow=0.006):
    p = [P(x, y, s) for x, y in pts]
    d.polygon(p, fill=fill)
    if ow: d.line(p + [p[0]], fill=INK, width=lw(s, ow), joint="curve")


def capsule(d, x0, y0, x1, y1, w, s, fill, ow=0.006):
    p0, p1 = P(x0, y0, s), P(x1, y1, s); ww = w * s; o = lw(s, ow)
    d.line([p0, p1], fill=INK, width=int(ww + 2 * o))
    for p in (p0, p1): d.ellipse((p[0] - ww / 2 - o, p[1] - ww / 2 - o, p[0] + ww / 2 + o, p[1] + ww / 2 + o), fill=INK)
    d.line([p0, p1], fill=fill, width=int(ww))
    for p in (p0, p1): d.ellipse((p[0] - ww / 2, p[1] - ww / 2, p[0] + ww / 2, p[1] + ww / 2), fill=fill)


def bg_grad(top, bot, s=None):
    yy = np.linspace(0, 1, H2 // 8, dtype=np.float32)[:, None, None]
    a = np.array(top, np.float32) * (1 - yy) + np.array(bot, np.float32) * yy
    a = np.repeat(a, W2 // 8, 1)
    return Image.fromarray(a.astype(np.uint8)).resize((W2, H2), Image.BILINEAR).convert("RGBA")


def soft_shadow(img, fn, blur):
    lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    if blur > 1 and blur < 300: lay = lay.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(lay)


def star(d, x, y, r, s, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    poly(d, pts, s, fill, 0)


# =============================================================== A: hand + EUR 1 coin
SKIN, SKIN2, NAIL, SLEEVE, SLEEVE2 = (247, 200, 160), (226, 168, 128), (252, 222, 205), (52, 120, 230), (36, 92, 190)
BR, BR2, BRL = (232, 186, 70), (196, 146, 40), (255, 226, 130)


PHOTO = Image.open("hand_photo.jpg").convert("RGBA")
PC, PR = (736.0, 1277.0), 178.0          # inner silver disc of the coin in the photo


def photo_at(s):
    k = (WR / R["A"]) * s / PR
    return PHOTO.transform((W2, H2), Image.AFFINE, (1 / k, 0, PC[0] - CX / k, 0, 1 / k, PC[1] - CY / k),
                           resample=Image.BILINEAR, fillcolor=(244, 240, 236, 255))


def draw_A(s):
    return photo_at(s)


def draw_A_vector(s):
    img = bg_grad((255, 252, 245), (250, 236, 214)); d = ImageDraw.Draw(img)
    soft_shadow(img, lambda dd: dd.ellipse((*P(-0.25, 0.55, s), *P(0.42, 0.66, s)), fill=(120, 80, 40, 60)), 0.02 * s)
    poly(d, [(0.13, 0.66), (0.42, 0.66), (0.35, 0.33), (0.12, 0.35)], s, SLEEVE)
    poly(d, [(0.11, 0.35), (0.35, 0.32), (0.34, 0.27), (0.10, 0.30)], s, SLEEVE2)
    circ(d, 0.07, 0.235, 0.16, s, SKIN, 0.006)
    soft_shadow(img, lambda dd: dd.ellipse((*P(0.04, 0.22, s), *P(0.22, 0.38, s)), fill=SKIN2 + (150,)), 0.03 * s)
    circ(d, 0.07, 0.235, 0.16, s, None, 0.006)
    for i, fx in enumerate((-0.105, -0.048, 0.009, 0.066)):
        tipy = 0.128 - (0.012 if i in (1, 2) else 0)
        capsule(d, fx + 0.03, 0.2, fx - 0.004, tipy, 0.054, s, SKIN)
        capsule(d, fx - 0.004, tipy + 0.004, fx - 0.004, tipy + 0.004, 0.026, s, NAIL, 0.003)
    soft_shadow(img, lambda dd: dd.ellipse((*P(-0.115, -0.09, s), *P(0.14, 0.165, s)), fill=(90, 50, 20, 110)), 0.012 * s)
    capsule(d, -0.07, 0.29, -0.152, 0.135, 0.062, s, SKIN)
    capsule(d, -0.152, 0.14, -0.152, 0.14, 0.03, s, NAIL, 0.003)
    return img


def over_A(img, s, f):
    r = WR / R["A"]; a = 1 - ease(f * 2.2)
    if a > 0.01:      # the real coin face dissolves into the engraved map
        ph = photo_at(s); rr = r * s * 1.002
        mask = Image.new("L", (W2, H2), 0); ImageDraw.Draw(mask).ellipse((CX - rr, CY - rr, CX + rr, CY + rr), fill=int(255 * a))
        mask = mask.filter(ImageFilter.GaussianBlur(max(1, rr * 0.01)))
        img.paste(ph, (0, 0), mask)
    return


def over_A_vector(img, s, f):
    d = ImageDraw.Draw(img); r = WR / R["A"]
    ring(d, 0, 0, r, r * 1.33, s, BR)
    ring(d, 0, 0, r * 1.18, r * 1.33, s, BR2)
    ring(d, 0, 0, r * 1.05, r * 1.1, s, BRL)
    for i in range(12):
        a = -math.pi / 2 + i * math.pi / 6
        star(d, math.cos(a) * r * 1.255, math.sin(a) * r * 1.255, r * 0.055, s, (150, 105, 25))
    ring(d, 0, 0, r * 0.995, r * 1.335, s, BR, 0.005)
    lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)     # specular highlight on the ring
    cx, cy = P(-0.6 * r, -0.75 * r, s); rr = 0.32 * r * s
    if rr < 3e4:
        dl.ellipse((cx - rr, cy - rr * 0.55, cx + rr, cy + rr * 0.55), fill=(255, 255, 255, 120))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(max(1, rr * 0.3))) if rr * 0.3 < 300 else lay)
    a = 1 - ease(f * 3)
    if a > 0.02 and r * s < 6000:
        lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.text(P(-0.5 * r, -0.08 * r, s), "1", font=font(POPX, 0.6 * r * s), fill=(80, 84, 96, int(235 * a)), anchor="mm")
        dl.text(P(0.42 * r, 0.6 * r, s), "EURO", font=font(POPX, 0.17 * r * s), fill=(80, 84, 96, int(235 * a)), anchor="mm")
        img.alpha_composite(lay)


# =============================================================== M: flat vector map centred on Zurich
def load(path, names=None, bbox=(-30, 25, 50, 72)):
    r = shapefile.Reader(path); fl = [x[0] for x in r.fields[1:]]; out = []
    key = "NAME" if "NAME" in fl else "name"
    for rec, sh in zip(r.records(), r.shapes()):
        b = sh.bbox
        if b[2] < bbox[0] or b[0] > bbox[2] or b[3] < bbox[1] or b[1] > bbox[3]: continue
        pts, parts = sh.points, list(sh.parts) + [len(sh.points)]
        nm = rec[fl.index(key)]
        for a, c in zip(parts, parts[1:]):
            ring_ = np.array(pts[a:c]); out.append((nm, ring_, (ring_[:, 0].min(), ring_[:, 1].min(), ring_[:, 0].max(), ring_[:, 1].max())))
    return out


C50 = load("/home/claude/v15/assets/ne50/ne_50m_admin_0_countries.shp")
C10 = load("ne/ne_10m_admin_0_countries.shp", bbox=(2, 43, 15, 50))
LAKES = load("ne/ne_10m_lakes_europe.shp", bbox=(2, 43, 15, 50)) + [x for x in load("ne/ne_10m_lakes.shp", bbox=(2, 43, 15, 50)) if x[0] in ("Lake Geneva", "Bodensee")]
EURO21 = {"Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Estonia", "Finland", "France", "Germany", "Greece", "Ireland", "Italy",
          "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Portugal", "Slovakia", "Slovenia", "Spain"}
OCEAN, LAND, EUROC, SWISS, LAKE = (124, 198, 240), (248, 234, 196), (120, 160, 245), (232, 57, 70), (124, 198, 240)


def my(lat): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


Y0 = my(ZUR[1])


def proj(arr, ppd):
    x = CX + (arr[:, 0] - ZUR[0]) * ppd
    y = CY - (np.degrees(np.log(np.tan(np.pi / 4 + np.radians(arr[:, 1]) / 2))) - Y0) * ppd
    return x, y


def draw_M(s):
    span = SPAN0 * H2 / s; ppd = W2 / span
    img = Image.new("RGBA", (W2, H2), OCEAN + (255,)); d = ImageDraw.Draw(img)
    if span > 3000: return img
    half_w = span / 2; half_h = span * H2 / W2 / 2 * 1.4
    vb = (ZUR[0] - half_w, ZUR[1] - half_h, ZUR[0] + half_w, ZUR[1] + half_h)
    data = C50 if span > 9 else C10
    o = max(1, min(int(0.0022 * s), 12))
    for nm, rg, b in data:
        if b[2] < vb[0] or b[0] > vb[2] or b[3] < vb[1] or b[1] > vb[3]: continue
        x, y = proj(rg, ppd)
        if x.max() - x.min() < 2 and y.max() - y.min() < 2: continue
        col = SWISS if nm == "Switzerland" else (EUROC if nm in EURO21 else LAND)
        pts = list(zip(x.tolist(), y.tolist()))
        d.polygon(pts, fill=col)
        d.line(pts + [pts[0]], fill=INK, width=o, joint="curve")
    if span < 14:
        for nm, rg, b in LAKES:
            if b[2] < vb[0] or b[0] > vb[2] or b[3] < vb[1] or b[1] > vb[3]: continue
            x, y = proj(rg, ppd); pts = list(zip(x.tolist(), y.tolist()))
            if len(pts) > 2: d.polygon(pts, fill=LAKE); d.line(pts + [pts[0]], fill=INK, width=max(1, o - 1), joint="curve")
    # Swiss cross on Switzerland once it is big
    if 1.2 < span < 12:
        x, y = proj(np.array([[8.23, 46.80]]), ppd); cs = 0.35 * ppd
        lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        a = int(255 * min(1, (12 - span) / 4) * min(1, (span - 1.2) / 1.5))
        dl.rectangle((x[0] - cs * 0.2, y[0] - cs * 0.62, x[0] + cs * 0.2, y[0] + cs * 0.62), fill=(255, 255, 255, a))
        dl.rectangle((x[0] - cs * 0.62, y[0] - cs * 0.2, x[0] + cs * 0.62, y[0] + cs * 0.2), fill=(255, 255, 255, a))
        img.alpha_composite(lay)
    return img


def over_M(img, s, f):
    d = ImageDraw.Draw(img); r = WR / R["M"]
    if r * s < 1.5: return
    # map pin: head = window ring, tail pointing down to Zurich-ish
    tail = [(-r * 0.75, r * 0.9), (r * 0.75, r * 0.9), (0, r * 2.4)]
    soft_shadow(img, lambda dd: dd.ellipse((*P(-r * 0.9, r * 2.25, s), *P(r * 0.9, r * 2.6, s)), fill=(0, 0, 0, 90)), max(1, min(200, r * s * 0.15)))
    poly(d, tail, s, SWISS, 0.0)
    ring(d, 0, 0, r, r * 1.32, s, SWISS)
    ring(d, 0, 0, r, r * 1.06, s, (255, 255, 255))
    pts = [P(x, y, s) for x, y in tail]
    d.line([pts[0], pts[2], pts[1]], fill=INK, width=lw(s, r * 0.06 / 1.0) if r * s > 10 else 2)
    cx, cy = P(0, 0, s); rr = r * 1.32 * s
    d.arc((cx - rr, cy - rr, cx + rr, cy + rr), 130, 50 + 360, fill=INK, width=max(1, int(r * 0.06 * s)))


# =============================================================== B: Swiss bank facade with a round oculus at the centre
STONE, STONE2, STONE3 = (244, 238, 226), (222, 212, 194), (196, 184, 162)


def draw_B(s):
    img = bg_grad((150, 210, 250), (214, 240, 255)); d = ImageDraw.Draw(img)
    for cx_, cy_, rr in ((-0.22, -0.36, 0.05), (-0.17, -0.37, 0.06), (0.2, -0.3, 0.045), (0.25, -0.31, 0.055)):
        circ(d, cx_, cy_, rr, s, (255, 255, 255))
    poly(d, [(-0.6, 0.44), (0.6, 0.44), (0.6, 0.7), (-0.6, 0.7)], s, (176, 200, 150), 0)
    poly(d, [(-0.27, 0.40), (0.27, 0.40), (0.27, 0.44), (-0.27, 0.44)], s, STONE3)
    poly(d, [(-0.25, 0.36), (0.25, 0.36), (0.25, 0.40), (-0.25, 0.40)], s, STONE2)
    poly(d, [(-0.23, 0.155), (0.23, 0.155), (0.23, 0.36), (-0.23, 0.36)], s, STONE2)
    poly(d, [(-0.07, 0.24), (0.07, 0.24), (0.07, 0.36), (-0.07, 0.36)], s, (120, 84, 50))
    for i in range(6):
        x = -0.2 + i * 0.08
        if abs(x) < 0.07: continue
        poly(d, [(x - 0.018, 0.17), (x + 0.018, 0.17), (x + 0.018, 0.36), (x - 0.018, 0.36)], s, STONE)
    poly(d, [(-0.25, 0.11), (0.25, 0.11), (0.25, 0.155), (-0.25, 0.155)], s, STONE)
    d.text(P(0, 0.133, s), "BANK", font=font(POPX, 0.03 * s), fill=INK, anchor="mm") if 0.03 * s < 5000 else None
    poly(d, [(-0.27, 0.11), (0.27, 0.11), (0, -0.165)], s, STONE)
    poly(d, [(-0.2, 0.09), (0.2, 0.09), (0, -0.115)], s, STONE2, 0.004)
    # flag on the roof
    d.line([P(0, -0.165, s), P(0, -0.27, s)], fill=INK, width=lw(s, 0.006))
    poly(d, [(0.0, -0.27), (0.075, -0.27), (0.075, -0.215), (0.0, -0.215)], s, SWISS, 0.004)
    poly(d, [(0.031, -0.258), (0.044, -0.258), (0.044, -0.227), (0.031, -0.227)], s, (255, 255, 255), 0)
    poly(d, [(0.022, -0.249), (0.053, -0.249), (0.053, -0.236), (0.022, -0.236)], s, (255, 255, 255), 0)
    return img


def over_B(img, s, f):
    d = ImageDraw.Draw(img); r = WR / R["B"]
    ring(d, 0, 0, r, r * 1.22, s, BR, 0.004)
    for i in range(12):
        a = i * math.pi / 6
        circ(d, math.cos(a) * r * 1.11, math.sin(a) * r * 1.11, r * 0.035, s, BRL)


# =============================================================== D: vault door with porthole
STEEL, STEEL2, STEEL3 = (196, 204, 216), (160, 170, 184), (120, 130, 146)


def draw_D(s):
    img = bg_grad((70, 76, 92), (36, 40, 52)); d = ImageDraw.Draw(img)
    for j in range(-6, 7):
        y = j * 0.12
        d.line([P(-1, y, s), P(1, y, s)], fill=(58, 64, 80), width=lw(s, 0.004))
    circ(d, 0, 0, 0.34, s, (54, 58, 70), 0.006)
    circ(d, 0, 0, 0.31, s, STEEL, 0.006)
    circ(d, 0, 0, 0.265, s, STEEL2, 0.005)
    for i in range(20):
        a = i * math.pi / 10
        circ(d, math.cos(a) * 0.288, math.sin(a) * 0.288, 0.011, s, (236, 240, 246), 0.003)
    poly(d, [(0.3, -0.1), (0.37, -0.1), (0.37, 0.1), (0.3, 0.1)], s, STEEL3)
    return img


def over_D(img, s, f):
    d = ImageDraw.Draw(img); r = WR / R["D"]
    for i in range(6):
        a = i * math.pi / 3 + 0.3
        capsule(d, math.cos(a) * r * 1.3, math.sin(a) * r * 1.3, math.cos(a) * 0.21, math.sin(a) * 0.21, 0.02, s, (236, 240, 246), 0.004)
    ring(d, 0, 0, 0.2, 0.222, s, (236, 240, 246), 0.004)
    ring(d, 0, 0, r, r * 1.25, s, BR, 0.004)
    for i in range(8):
        a = i * math.pi / 4 + 0.39
        circ(d, math.cos(a) * r * 1.125, math.sin(a) * r * 1.125, r * 0.04, s, BRL, 0.002)
    a = 1 - ease(f * 2.5)
    if a > 0.02 and r * s < 6000:
        lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        cx, cy = P(-0.32 * r, -0.4 * r, s); rr = r * s * 0.45
        dl.ellipse((cx - rr, cy - rr * 0.45, cx + rr, cy + rr * 0.45), fill=(255, 255, 255, int(90 * a)))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(max(1, rr * 0.25))))


# =============================================================== G: gold bars, stamp at the centre
GT, GF, GD, GL = (255, 216, 90), (240, 180, 40), (176, 118, 20), (255, 242, 170)


def bar(d, x, y, w, h, s):
    tw = w * 0.78
    poly(d, [(x - tw / 2, y - h / 2), (x + tw / 2, y - h / 2), (x + tw / 2 - h * 0.25, y - h / 2 - h * 0.3), (x - tw / 2 + h * 0.25, y - h / 2 - h * 0.3)], s, GT)
    poly(d, [(x - w / 2, y + h / 2), (x + w / 2, y + h / 2), (x + tw / 2, y - h / 2), (x - tw / 2, y - h / 2)], s, GF)
    poly(d, [(x - w / 2 + w * 0.07, y + h / 2 - h * 0.14), (x - tw / 2 + w * 0.05, y - h / 2 + h * 0.12), (x - tw / 2 + w * 0.1, y - h / 2 + h * 0.12), (x - w / 2 + w * 0.13, y + h / 2 - h * 0.14)], s, GL, 0)


def draw_G(s):
    img = bg_grad((92, 60, 40), (30, 20, 16)); d = ImageDraw.Draw(img)
    bw, bh = 0.46, 0.22
    for n, y in ((2, -0.52), (3, -0.26), (3, 0.26), (2, 0.52)):
        for i in range(n): bar(d, (i - (n - 1) / 2) * (bw + 0.03), y, bw, bh, s)
    for x in (-(bw + 0.03), bw + 0.03): bar(d, x, 0, bw, bh, s)
    bar(d, 0, 0, bw, bh, s)
    return img


def over_G(img, s, f):
    d = ImageDraw.Draw(img); r = WR / R["G"]
    ring(d, 0, 0, r, r * 1.14, s, GD)
    ring(d, 0, 0, r * 1.18, r * 1.23, s, GD)
    if 0.03 * s < 4000:
        for txt, x, y, sz in (("999.9", -0.16, -0.05, 0.026), ("FINE GOLD", 0.16, -0.05, 0.02), ("1 KG", -0.16, 0.05, 0.024), ("SWISS", 0.16, 0.05, 0.022)):
            d.text(P(x, y, s), txt, font=font(POPX, sz * s), fill=GD, anchor="mm")


# =============================================================== tints + recursion
def tint(img, kind, a):
    if a <= 0.01 or kind is None: return img
    arr = np.asarray(img).astype(np.float32)
    g = (arr[..., :3] @ np.array([0.3, 0.59, 0.11], np.float32))[..., None] / 255
    if kind == "silver": m = np.concatenate([g * 150 + 95, g * 155 + 97, g * 160 + 104], 2)
    else: m = np.concatenate([g * 150 + 105, g * 135 + 70, g * 70 + 15], 2)
    arr[..., :3] = arr[..., :3] * (1 - a) + m * a
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


DRAW = {"A": draw_A, "M": draw_M, "B": draw_B, "D": draw_D, "G": draw_G}
OVER = {"A": over_A, "M": over_M, "B": over_B, "D": over_D, "G": over_G}
TINT = {"A": "silver", "M": None, "B": None, "D": None, "G": "gold"}


def render_level(k, s, f, depth=0):
    img = DRAW[k](s)
    rr = WR / R[k] * s
    if depth < 3 and rr > 2:
        child = render_level(nxt(k), s / R[k], 0.0, depth + 1)
        child = tint(child, TINT[k], 1 - ease(f) if depth == 0 else 1.0)
        mask = Image.new("L", (W2, H2), 0)
        ImageDraw.Draw(mask).ellipse((CX - rr, CY - rr, CX + rr, CY + rr), fill=255)
        img.paste(child, (0, 0), mask)
    OVER[k](img, s, f if depth == 0 else 0.0)
    return img


VIG = None
GRAIN = np.random.default_rng(5).normal(0, 2.2, (H + 128, W + 128, 1)).astype(np.float32)


def frame(fi):
    global VIG
    tc = (T0 + fi / FPS) % CYCLE
    u, k, lt = u_at(tc)
    top, ul = top_level(u)
    s = H2 * math.exp(ul)
    img = render_level(top, s, ul / math.log(R[top])).resize((W, H), Image.LANCZOS).convert("RGB")
    # zoom blur proportional to zoom speed
    u2, _, _ = u_at(tc + 1 / FPS); v = (u2 - u) * FPS
    kb = min(0.07, v * 0.012)
    if kb > 0.004:
        acc = np.asarray(img).astype(np.float32); n = 1
        for q in (0.5, 1.0):
            z = 1 + kb * q; im2 = img.resize((int(W * z), int(H * z)), Image.BILINEAR)
            ox, oy = (im2.width - W) // 2, (im2.height - H) // 2
            acc += np.asarray(im2.crop((ox, oy, ox + W, oy + H))).astype(np.float32); n += 1
        arr = acc / n
    else:
        arr = np.asarray(img).astype(np.float32)
    if VIG is None:
        yy, xx = np.mgrid[0:H // 4, 0:W // 4]
        dd = np.sqrt(((xx - W / 8) / (W / 8)) ** 2 + ((yy - H / 8) / (H / 8)) ** 2)
        VIG = np.asarray(Image.fromarray((np.clip(1.0 - 0.22 * np.clip(dd - 0.6, 0, None) ** 1.5, 0.7, 1) * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR))[..., None] / 255.0
    arr = arr * VIG
    gy, gx = (fi * 37) % 128, (fi * 91) % 128
    arr += GRAIN[gy:gy + H, gx:gx + W]
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "still":
        for a in sys.argv[2:]: frame(int(a)).save(f"still_{int(a):04d}.png")
    elif cmd == "info":
        print("cycle", round(CYCLE, 2), "frames", NF, "stops", [round(x, 2) for x in STOPS])
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 30 == 0: print(fi, flush=True)
        p.stdin.close(); p.wait()
