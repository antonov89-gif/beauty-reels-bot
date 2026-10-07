"""New Year first/last map Short (GeoGlobeTales style). python3 engine24.py still N.. | info | prefetch | video A B out.mp4"""
import json, math, subprocess, sys
import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import tiles
from script24 import LINES

W, H, FPS = 1080, 1920, 30
POP, POPX = "Poppins-Bold.ttf", "Poppins-ExtraBold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (60, 200, 90), (60, 140, 255), (255, 255, 255), (0, 0, 0)
GOLD, ORG = (255, 190, 60), (255, 140, 30)
TM = json.load(open("timing.json")); D, TW = TM["D"], TM["T"]
LEAD = 0.3
ST = [LEAD + s for s in TM["starts"]]
TOTAL = ST[-1] + D[-1] + 1.4
NF = int(TOTAL * FPS)


def clean(w): return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word=None):
    if word is None: return ST[i]
    ws = [clean(w) for w in LINES[i].split()]; q = clean(word)
    for j, w in enumerate(ws):
        if w == q: return ST[i] + TW[i][j]
    for j, w in enumerate(ws):
        if q in w: return ST[i] + TW[i][j]
    raise KeyError(word)


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def pop(x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    return 1.15 * ease(x / 0.6) if x < 0.6 else 1.15 - 0.15 * ease((x - 0.6) / 0.4)


exec(open("helpers_raw.py").read())  # lerp, vignette, font, emoji_sprite, paste_emoji, text_stroke, badge, arrow, big

# ---------------------------------------------------------------- geo data
_R = shapefile.Reader("/home/claude/v15/assets/ne50/ne_50m_admin_0_countries.shp")
_F = [x[0] for x in _R.fields[1:]]
COUNTRY = {}
for rec, shp in zip(_R.records(), _R.shapes()):
    n = rec[_F.index("NAME")]
    if n in ("Kiribati", "Samoa", "American Samoa", "New Zealand", "Australia"):
        pts, parts = shp.points, list(shp.parts) + [len(shp.points)]
        COUNTRY[n] = [pts[a:b] for a, b in zip(parts, parts[1:])]

IDL = [(180, 85), (180, 75), (-169, 68), (-169, 65), (-172, 61), (180, 52), (170, 51.5), (170, 48), (180, 45), (180, -1.5),
       (-170, -1.5), (-170, 6), (-150, 6), (-150, -12), (-171.4, -12), (-171.4, -16), (-172.5, -45), (180, -51), (180, -85)]
OLD = [(180, 85), (180, 75), (-169, 68), (-169, 65), (-172, 61), (180, 52), (170, 51.5), (170, 48), (180, 45), (180, -1.5),
       (180, -1.5), (180, 6), (180, 6), (180, -12), (180, -12), (180, -16), (-172.5, -45), (180, -51), (180, -85)]
PLACES = {"tarawa": (173.0, 1.42), "kiritimati": (-157.4, 1.87), "london": (-157.475, 1.983), "banana": (-157.36, 1.975),
          "poland": (-157.55, 1.875), "apia": (-171.77, -13.83), "pago": (-170.70, -14.28), "baker": (-176.48, 0.195),
          "howland": (-176.62, 0.81), "auckland": (174.76, -36.85), "sydney": (151.2, -33.87), "tokyo": (139.7, 35.7),
          "la": (-118.2, 34.05), "rio": (-43.2, -22.9), "paris": (2.35, 48.85), "lagos": (3.4, 6.5), "ny": (-74, 40.7)}


def U(lon, ref):
    return lon + 360 * round((ref - lon) / 360)


def ipath(cam, pts):
    out, prev = [], None
    for lo, la in pts:
        lo = U(lo, cam.lon if prev is None else prev); prev = lo
        out.append(((lo - cam.lon) * cam.ppd + W / 2, (cam.Y - tiles.my(la)) * cam.ppd + H / 2))
    return out


def glow_line(img, pts, color, width, glow=1.0, dash=None, phase=0.0):
    if len(pts) < 2: return
    lay = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    dl.line([(x / 2, y / 2) for x, y in pts], fill=color + (int(200 * glow),), width=max(2, width), joint="curve")
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(9)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    if dash:
        on, off = dash
        for a, b in zip(pts, pts[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1]); s = -phase % (on + off)
            while s < L:
                e = min(L, s + on)
                if e > 0:
                    s0 = max(0, s)
                    d.line([(a[0] + (b[0] - a[0]) * s0 / L, a[1] + (b[1] - a[1]) * s0 / L), (a[0] + (b[0] - a[0]) * e / L, a[1] + (b[1] - a[1]) * e / L)], fill=WHT + (255,), width=width)
                s += on + off
    else:
        d.line(pts, fill=WHT + (255,), width=width + 6, joint="curve")
        d.line(pts, fill=color + (255,), width=width, joint="curve")


def partial(pts, k):
    if k >= 1: return pts
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; L = sum(seg) * max(0, k)
    out, acc = [pts[0]], 0
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if acc + s >= L:
            q = (L - acc) / max(s, 1e-6); out.append((a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q)); break
        out.append(b); acc += s
    return out


def hl_country(img, cam, name, color, alpha, outline=True, grow=0):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for ring in COUNTRY[name]:
        p = ipath(cam, ring)
        xs = [q[0] for q in p]; ys = [q[1] for q in p]
        if max(xs) < -50 or min(xs) > W + 50 or max(ys) < -50 or min(ys) > H + 50: continue
        if max(xs) - min(xs) < 14 and grow:
            cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
            d.ellipse((cx - grow, cy - grow, cx + grow, cy + grow), outline=color + (255,), width=6)
            continue
        if len(p) > 2:
            d.polygon(p, fill=color + (int(255 * alpha),))
            if outline: d.line(p + [p[0]], fill=WHT + (230,), width=4)
    img.alpha_composite(lay)


def pin(img, x, y, txt, color, k, emoji=None, up=True, size=50):
    if k <= 0: return
    d = ImageDraw.Draw(img)
    r = 13 * k
    d.ellipse((x - r - 4, y - r - 4, x + r + 4, y + r + 4), fill=WHT)
    d.ellipse((x - r, y - r, x + r, y + r), fill=color)
    ly = y - 95 * k if up else y + 95 * k
    d.line([(x, y), (x, ly)], fill=WHT, width=5)
    badge(img, x, ly + (-30 if up else 30) * k, txt, color, k, emoji, size)


def ring(img, x, y, r, color, k, width=7):
    if k <= 0: return
    d = ImageDraw.Draw(img); rr = r * (0.6 + 0.4 * k)
    d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=color + (int(255 * min(1, k)),), width=width)


def pulse(img, x, y, t, t0, color=YEL, r=120):
    if t < t0: return
    d = ImageDraw.Draw(img)
    for q in range(2):
        ph = ((t - t0) * 0.9 + q * 0.5) % 1.0
        rr = r * ph; a = int(220 * (1 - ph))
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=color + (a,), width=6)


def firework(img, x, y, t, t0, color=None, r=110, n=14):
    lt = t - t0
    if lt < 0 or lt > 1.4: return
    cols = [GOLD, (255, 80, 120), (90, 200, 255), (140, 255, 120)]
    col = color or cols[int(abs(x * 7 + y * 3)) % 4]
    d = ImageDraw.Draw(img)
    k = ease(lt / 0.7); a = int(255 * (1 - ease((lt - 0.5) / 0.9)))
    for q in range(n):
        ang = q / n * 2 * math.pi + x * 0.01
        x1, y1 = x + math.cos(ang) * r * k, y + math.sin(ang) * r * k + 30 * lt * lt
        x0, y0 = x + math.cos(ang) * r * k * 0.6, y + math.sin(ang) * r * k * 0.6 + 30 * lt * lt
        d.line([(x0, y0), (x1, y1)], fill=col + (a,), width=6)
        d.ellipse((x1 - 6, y1 - 6, x1 + 6, y1 + 6), fill=WHT + (a,))


def grade(im, esri=False):
    a = np.asarray(im).astype(np.float32) / 255
    a = a ** (0.80 if not esri else 0.85)
    g = a.mean(2, keepdims=True); a = g + (a - g) * 1.2
    if esri:
        m = np.clip((0.30 - a.max(2, keepdims=True)) / 0.12, 0, 1)
        yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
        oc = np.array([0.05, 0.22, 0.42], np.float32) * (1 - 0.25 * yy) + 0.02
        a = a * (1 - m) + (oc + (a - a.mean(2, keepdims=True)) * 0.3) * m
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")


# ---------------------------------------------------------------- scenes
def kf(t, keys):
    """keys: list of (time, value tuple); smooth interpolation."""
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            k = ease((t - t0) / max(1e-3, t1 - t0)); return tuple(lerp(a, b, k) for a, b in zip(v0, v1))
    return keys[-1][1]


SC = [0.0] + [ST[i] - 0.12 for i in range(1, len(LINES))] + [TOTAL + 1]
CUTS = SC[1:-1]


def cam_for(i, t):
    a, b = SC[i], SC[i + 1]
    if i == 0: return kf(t, [(a, (170, 15, 175)), (b, (172, 12, 150))])
    if i == 1: return kf(t, [(a, (172, 12, 150)), (b, (176, 8, 140))])
    if i == 2: return kf(t, [(a, (178, 15, 130)), (b, (183, 2, 85))])
    if i == 3: return kf(t, [(a, (187, 0, 85)), (WT(3, "Kiribati") + 0.3, (193, -2, 55)), (b, (196, -1, 46))])
    if i == 4: return kf(t, [(a, (202.6, 1.9, 1.6)), (WT(4, 'London') - 0.2, (202.53, 1.93, 0.62)), (b, (202.53, 1.93, 0.5))])
    if i == 5: return kf(t, [(a, (190, 1, 70)), (b, (188, 1, 62))])
    if i == 6: return kf(t, [(a, (188, 0, 62)), (b, (194, -3, 70))])
    if i == 7:
        return kf(t, [(a, (178, -35, 70)), (WT(7, "Zealand"), (175, -38, 60)), (WT(7, "Australia"), (140, -27, 85)), (WT(7, "Asia"), (100, 25, 110)),
                      (WT(7, "Europe"), (15, 48, 80)), (WT(7, "Africa"), (18, 5, 95)), (WT(7, "Americas"), (-80, 10, 130)), (b, (-90, 5, 140))])
    if i == 8: return kf(t, [(a, (-170.7, -14.3, 1.4)), (b, (-170.72, -14.3, 1.0))])
    if i == 9: return kf(t, [(a, (-171.5, -14.0, 2.9)), (b, (-171.45, -14.0, 2.6))])
    if i == 10: return kf(t, [(a, (-171.45, -14.0, 2.6)), (b, (-171.25, -14.05, 2.0))])
    if i == 11: return kf(t, [(a, (-174.5, -2, 30)), (WT(11, "Baker"), (-176.55, 0.5, 2.6)), (b, (-176.55, 0.5, 2.1))])
    return kf(t, [(a, (-176.478, 0.196, 0.07)), (b, (-176.478, 0.196, 0.05))])


def midnight_lon(t):
    i = 7
    return kf(t, [(SC[i], (180,)), (WT(7, "Zealand"), (172,)), (WT(7, "Australia"), (145,)), (WT(7, "Asia"), (100,)), (WT(7, "Europe"), (25,)),
                  (WT(7, "Africa"), (10,)), (WT(7, "Americas"), (-70,)), (SC[8], (-95,))])[0]


def render(t, fi):
    i = max(j for j in range(len(LINES)) if SC[j] <= t) if t >= 0 else 0
    lt = t - SC[i]
    lo, la, sp = cam_for(i, t)
    sp *= 1 + 0.004 * math.sin(t * 1.3)
    cam = tiles.Cam(lo, la, sp)
    img = grade(cam.render(), cam.src == "esri")
    d = ImageDraw.Draw(img)
    xy = lambda name: cam.xy(*PLACES[name])
    if i == 0:
        for q, (n, dt) in enumerate((("auckland", 0.2), ("sydney", 0.6), ("tokyo", 1.0), ("la", 1.4))):
            x, y = xy(n); firework(img, x, y, t, SC[0] + dt + 0.0, r=90); firework(img, x, y, t, SC[0] + dt + 1.6, r=70)
        big(img, "FIRST?", t, WT(0, "first"), 420, 170, GRN)
        big(img, "LAST?", t, WT(0, "last"), 1150, 170, RED)
    elif i == 1:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        nshow = int(24 * ease((t - SC[1]) / 2.2)) if t < WT(1, "zigzag") else 24
        for z in range(24):
            if z >= nshow: break
            lon0 = -180 + z * 15 - 7.5
            p = ipath(cam, [(lon0, 80), (lon0, -80)]); q = ipath(cam, [(lon0 + 15, 80), (lon0 + 15, -80)])
            x0 = p[0][0]; x1 = x0 + 15 * cam.ppd
            if z % 2 == 0: dl.rectangle((x0, 0, x1, H), fill=(255, 255, 255, 34))
            dl.line([(x0, 0), (x0, H)], fill=(255, 255, 255, 120), width=3)
        img.alpha_composite(lay)
        if t >= WT(1, "twentyfour"): big(img, "24", t, WT(1, "twentyfour"), 430, 230, YEL, None)
        if t >= WT(1, "twentyfour") + 0.2: badge(img, W / 2, 600, "TIME ZONES", (30, 30, 30), pop((t - WT(1, "twentyfour") - 0.2) / 0.3), "🕛", 56)
        if t >= WT(1, "zigzag"):
            p = partial(ipath(cam, IDL), ease((t - WT(1, "zigzag")) / 1.0)); glow_line(img, p, (255, 255, 255), 6, 0.6, dash=(26, 16), phase=t * 60)
    elif i == 2:
        p = partial(ipath(cam, IDL), ease((t - SC[2]) / 2.0)); glow_line(img, p, RED, 12, 1.0)
        x, y = cam.xy(180, 30)
        if t >= WT(2, "International"): badge(img, x, 520, "INTERNATIONAL DATE LINE", RED, pop((t - WT(2, "International")) / 0.3), None, 50)
        if t >= WT(2, "new"):
            k = pop((t - WT(2, "new")) / 0.3); xa, ya = cam.xy(180, -20)
            badge(img, xa - 200, ya, "TODAY", (40, 40, 40), k, None, 52); badge(img, xa + 230, ya, "YESTERDAY", (40, 40, 40), k, None, 52)
            badge(img, W / 2, 780, "NEW DAY STARTS HERE", GOLD, k, "🌅", 46)
    elif i == 3:
        glow_line(img, ipath(cam, IDL), RED, 10, 0.8)
        a = 0.45 + 0.15 * math.sin(t * 6)
        hl_country(img, cam, "Kiribati", YEL, a * ease((t - WT(3, "Kiribati")) / 0.3), grow=26 if t >= WT(3, "Kiribati") else 0)
        for g, (glon, glat, r) in enumerate(((173.5, 0.5, 4.5), (-172, -3.8, 3.5), (-157.5, -1, 6))):
            x, y = cam.xy(glon, glat); ring(img, x, y, r * cam.ppd, YEL, ease((t - WT(3, "Kiribati") - g * 0.15) / 0.3))
        if t >= WT(3, "Kiribati"): badge(img, W / 2, 470, "KIRIBATI", (0, 120, 200), pop((t - WT(3, "Kiribati")) / 0.3), "🇰🇮", 66)
        if t >= WT(3, "first"): big(img, "1st", t, WT(3, "first"), 300, 170, GRN)
        if t >= WT(3, "hundred"): badge(img, W / 2, 1180, "120,000", (30, 30, 30), pop((t - WT(3, "hundred")) / 0.3), "👥", 56)
        if t >= WT(3, "thirtythree"): badge(img, W / 2, 1290, "33 ISLANDS", (30, 30, 30), pop((t - WT(3, "thirtythree")) / 0.3), "🏝️", 56)
    elif i == 4:
        if t >= WT(4, "Kiritimati"): badge(img, W / 2, 330, "KIRITIMATI ISLAND", (0, 120, 200), pop((t - WT(4, "Kiritimati")) / 0.3), "🇰🇮", 54)
        for n, word, col, up in (("london", "London", RED, True), ("banana", "Banana", (200, 150, 0), False), ("poland", "Poland", BLU, False)):
            if t >= WT(4, word):
                x, y = xy(n); pin(img, x, y, word.upper(), col, pop((t - WT(4, word)) / 0.3), None, up)
        for q, (fx_, fy_) in enumerate(((180, 560), (900, 520), (160, 1150), (920, 1120), (540, 470), (300, 820))):
            if t >= WT(4, "celebrate"):
                firework(img, fx_, fy_, t, WT(4, "celebrate") + q * 0.22, r=105)
        if t >= WT(4, "before"): big(img, "FIRST ON EARTH", t, WT(4, "before"), 1270, 92, GRN)
    elif i in (5, 6):
        if i == 5:
            glow_line(img, ipath(cam, OLD), WHT, 7, 0.5, dash=(30, 18), phase=t * 50)
            big(img, "BEFORE 1995", t, WT(5, "nineteen"), 330, 110, YEL)
            x1, y1 = xy("tarawa"); x2, y2 = xy("kiritimati")
            pin(img, x1, y1, "CAPITAL", (30, 30, 30), pop((t - WT(5, "capital")) / 0.3), "🏛️", True, 44)
            pin(img, x2, y2, "EAST", (30, 30, 30), pop((t - WT(5, "eastern")) / 0.3), "🏝️", True, 44)
            if t >= WT(5, "whole"):
                mid = [(x1 + (x2 - x1) * s, y1 + 90 - math.sin(math.pi * s) * 160 + 120) for s in np.linspace(0, 1, 30)]
                arrow(img, partial(mid, ease((t - WT(5, "whole")) / 0.5)), RED, 1.0, 14)
                badge(img, (x1 + x2) / 2, y1 + 330, "1 DAY APART", RED, pop((t - WT(5, "whole") - 0.3) / 0.3), "📅", 50)
        else:
            k = ease((t - SC[6]) / 1.6)
            pts = [(lerp(U(a[0], 180), U(b[0], 180), k), lerp(a[1], b[1], k)) for a, b in zip(OLD, IDL)]
            glow_line(img, ipath(cam, pts), RED, 12, 1.0)
            if t >= WT(6, "moved"): big(img, "MOVED!", t, WT(6, "moved"), 330, 140, YEL)
            if t >= WT(6, "thousands"):
                x0, y0 = cam.xy(180, 9); x1, _ = cam.xy(-150, 9)
                arrow(img, [(x0, y0), (x1, y0)], YEL, ease((t - WT(6, "thousands")) / 0.6), 18)
                badge(img, (x0 + x1) / 2, y0 - 100, "~3,000 KM EAST", (30, 30, 30), pop((t - WT(6, "thousands") - 0.3) / 0.3), None, 46)
    elif i == 7:
        M = midnight_lon(t)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        xm = (U(M, cam.lon) - cam.lon) * cam.ppd + W / 2
        xe = xm + (U(180, M + 180) - U(M, M)) * cam.ppd
        dl.rectangle((xm, 0, max(xm, xe), H), fill=GOLD + (55,))
        img.alpha_composite(lay)
        glow_line(img, [(xm, 0), (xm, H)], GOLD, 8, 1.0)
        badge(img, min(W - 120, max(160, xm)), 300, "00:00", (20, 20, 20), 1.0, "🎆", 52)
        for word, place, lab in (("Zealand", "auckland", "NEW ZEALAND"), ("Australia", "sydney", "AUSTRALIA"), ("Asia", "tokyo", "ASIA"),
                                 ("Europe", "paris", "EUROPE"), ("Africa", "lagos", "AFRICA"), ("Americas", "ny", "AMERICAS")):
            tw = WT(7, word)
            if tw - 0.1 <= t:
                x, y = xy(place)
                firework(img, x, y, t, tw, r=100); firework(img, x + 60, y - 80, t, tw + 0.5, r=70)
                if t < tw + 2.2: badge(img, W / 2, 1180, lab, (30, 30, 30), pop((t - tw) / 0.25), None, 60)
    elif i == 8:
        x, y = xy("pago"); pulse(img, x, y, t, SC[8], RED, 260); ring(img, x, y, 170, RED, ease((t - SC[8]) / 0.4), 9)
        badge(img, W / 2, 420, "AMERICAN SAMOA", RED, pop((t - WT(8, "American")) / 0.3), "🇦🇸", 60)
        if t >= WT(8, "last"): big(img, "ONE OF THE LAST", t, WT(8, "last"), 1180, 90, RED)
    elif i in (9, 10):
        glow_line(img, ipath(cam, IDL), RED, 10, 1.0)
        ring(img, *cam.xy(-171.75, -13.93), 0.42 * cam.ppd, GRN, 1.0, 7); ring(img, *cam.xy(-170.70, -14.30), 0.22 * cam.ppd, RED, 1.0, 7)
        xa, ya = cam.xy(-172.1, -13.6); xb, yb = cam.xy(-170.7, -14.3)
        if i == 9:
            badge(img, xb, yb - 200, "DEC 31", RED, pop((t - SC[9] - 0.2) / 0.3), "🇦🇸", 50)
            if t >= WT(9, "Samoa"): badge(img, xa, ya - 230, "JAN 1", GRN, pop((t - WT(9, "Samoa")) / 0.3), "🇼🇸", 50)
            if t >= WT(9, "seventy"):
                p1, p2 = cam.xy(-171.42, -14.06), cam.xy(-170.84, -14.29)
                arrow(img, [p2, p1], YEL, ease((t - WT(9, "seventy")) / 0.5), 12)
                badge(img, (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 120, "~70 KM", (30, 30, 30), pop((t - WT(9, "seventy") - 0.2) / 0.3), None, 50)
            if t >= WT(9, "full"): big(img, "+1 DAY", t, WT(9, "full"), 1260, 130, GRN)
        else:
            x1, y1 = xy("apia"); x2, y2 = xy("pago")
            firework(img, x1, y1, t, SC[10] + 0.1, r=90)
            k = ease((t - WT(10, "fly")) / 1.6)
            if t >= WT(10, "fly"):
                arc = [(x1 + (x2 - x1) * s, y1 + (y2 - y1) * s - math.sin(math.pi * s) * 220) for s in np.linspace(0, 1, 40)]
                glow_line(img, partial(arc, k), WHT, 5, 0.5, dash=(18, 14))
                j = min(39, int(k * 39)); paste_emoji(img, "✈️", arc[j][0], arc[j][1], 110)
            if k >= 1: firework(img, x2, y2, t, WT(10, "fly") + 1.6, r=90)
            if t >= WT(10, "twice"): big(img, "2× NEW YEAR", t, WT(10, "twice"), 1180, 120, YEL)
    elif i == 11:
        glow_line(img, ipath(cam, IDL), RED, 10, 0.8)
        for n, lab, tw in (("baker", "BAKER", WT(11, "Baker")), ("howland", "HOWLAND", WT(11, "Howland"))):
            if t >= tw:
                x, y = xy(n); pulse(img, x, y, t, tw); pin(img, x, y, lab, (30, 30, 30), pop((t - tw) / 0.3), "🇺🇸", n == "howland", 46)
        if t >= WT(11, "very"): big(img, "UTC −12", t, WT(11, "very"), 330, 120, YEL)
        if t >= WT(11, "nobody"): badge(img, W / 2, 1180, "POPULATION: 0", RED, pop((t - WT(11, "nobody")) / 0.3), "👤", 56)
    else:
        img.alpha_composite(Image.new("RGBA", (W, H), (5, 10, 30, int(120 * ease(lt / 0.6)))))
        for q in range(7):
            firework(img, 160 + (q * 157) % 760, 380 + (q * 97) % 420, t, SC[12] + 0.3 + q * 0.45, r=120)
        bx0, by0 = xy("baker")
        for q, (bx, by) in enumerate(((bx0 - 200, by0 + 20), (bx0, by0 - 30), (bx0 + 200, by0 + 20))):
            if t >= WT(12, "seabirds") - 0.1 + q * 0.12:
                kk = pop((t - WT(12, "seabirds") + 0.1 - q * 0.12) / 0.3)
                paste_emoji(img, "🐦", bx, by + math.sin(t * 5 + q) * 10, 150 * kk)
                paste_emoji(img, "🥂" if q == 1 else "🎉", bx + 70, by - 70, 80 * kk)
        if t >= WT(12, "final"): badge(img, W / 2, 1180, "LAST PARTY ON EARTH", (30, 30, 30), pop((t - WT(12, "final")) / 0.3), "🎆", 50)
    return img


def caption(img, t):
    for i in range(len(LINES)):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.15:
            words = LINES[i].split(); cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05: cur = j
            c0 = cur // 3 * 3; chunk = words[c0:c0 + 3]
            f = font(POPX, 76); gap = f.getlength(" ") * 1.6
            ws = [f.getlength(w.upper()) for w in chunk]; tot = sum(ws) + gap * (len(chunk) - 1)
            if tot > W - 70:
                f = font(POPX, 76 * (W - 70) / tot); gap = f.getlength(" ") * 1.6
                ws = [f.getlength(w.upper()) for w in chunk]; tot = sum(ws) + gap * (len(chunk) - 1)
            x = (W - tot) / 2; d = ImageDraw.Draw(img)
            for j, (w, ww) in enumerate(zip(chunk, ws)):
                col = YEL if c0 + j == cur else WHT
                d.text((x + 4, 1456), w.upper(), font=f, fill=(0, 0, 0, 160), anchor="lm")
                d.text((x, 1450), w.upper(), font=f, fill=col, anchor="lm", stroke_width=9, stroke_fill=BLK)
                x += ww + gap
            return


GRAIN = np.random.default_rng(3).normal(0, 3.0, (H + 256, W + 256, 1)).astype(np.float32)


def frame(fi):
    t = fi / FPS
    img = render(t, fi)
    for ct in CUTS:
        if 0 <= t - ct < 0.18:
            a = 1 - (t - ct) / 0.18; n = int(60 * a * a)
            if n > 2:
                arr = np.asarray(img).astype(np.float32)
                img = Image.fromarray((sum(np.roll(arr, int(s), axis=1) for s in np.linspace(-n, n, 7)) / 7).astype(np.uint8), "RGBA")
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(60 * a))))
    caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32) * vignette()
    gy, gx = (fi * 37) % 256, (fi * 91) % 256
    rgb += GRAIN[gy:gy + H, gx:gx + W]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "still":
        for a in sys.argv[2:]: frame(int(a)).save(f"still_{int(a):05d}.png")
    elif cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2)); print([round(x, 2) for x in SC])
    elif cmd == "prefetch":
        keys = []
        for fi in range(0, NF, 3):
            t = fi / FPS; i = max(j for j in range(len(LINES)) if SC[j] <= t) if t >= 0 else 0
            keys += tiles.Cam(*cam_for(i, t)).keys()
        print(tiles.prefetch(keys))
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 30 == 0: print(fi, flush=True)
        p.stdin.close(); p.wait()
