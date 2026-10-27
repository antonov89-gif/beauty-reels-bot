"""Storyboard base frames for the Iraq Short: accurate geography (Esri-free imagery /home/claude/v86/img/{A,B,C}.jpg + Natural Earth 10m
borders) with the shot's highlight drawn in. These go to Nano Banana as the layout reference for the premium 3D restyle.
Run: python3 sb_base.py -> /home/claude/v86/base/sNN.jpg"""
import math

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
VIEWS = {"A": (44.3, 31.5, 7.2), "B": (48.0, 29.9, 1.3), "C": (48.2, 29.9, 0.5)}
UMM_QASR, MUBARAK, GRAND_FAW = (47.95, 30.03), (48.318, 29.865), (48.441, 29.915)
r = shapefile.Reader("/home/claude/v62/assets/ne10/ne_10m_admin_0_countries.shp")
fl = [f[0] for f in r.fields[1:]]
SHP = {}
for sr in r.iterShapeRecords():
    n = dict(zip(fl, sr.record))["ADMIN"]
    pts, parts = sr.shape.points, list(sr.shape.parts) + [len(sr.shape.points)]
    SHP[n] = [np.array(pts[a:b]) for a, b in zip(parts[:-1], parts[1:])]


def proj(view):
    lon, lat, d = VIEWS[view]
    dl = d * (W / H) / math.cos(math.radians(lat))
    l0, b0, l1, b1 = lon - dl, lat - d, lon + dl, lat + d
    return lambda p: ((p[0] - l0) / (l1 - l0) * W, (b1 - p[1]) / (b1 - b0) * H)


def fill(img, view, name, col, a, border=(255, 255, 255), bw=3, glow=None):
    P = proj(view)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for ring in SHP[name]:
        xy = [P(p) for p in ring]
        d.polygon(xy, fill=col + (int(255 * a),))
    if glow:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
        for ring in SHP[name]:
            dg.line([P(p) for p in ring] + [P(ring[0])], fill=glow + (255,), width=18)
        lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(10)))
    for ring in SHP[name]:
        d.line([P(p) for p in ring] + [P(ring[0])], fill=border + (255,), width=bw)
    img.alpha_composite(lay)


def line(img, view, pts, col, w=10, glow=True, dash=False):
    P = proj(view); xy = [P(p) for p in pts]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if dash:
        for a, b in zip(xy, xy[1:]):
            n = int(math.hypot(b[0] - a[0], b[1] - a[1]) // 28) or 1
            for i in range(0, n, 2):
                d.line([(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n),
                        (a[0] + (b[0] - a[0]) * (i + 1) / n, a[1] + (b[1] - a[1]) * (i + 1) / n)], fill=col + (255,), width=w)
    else:
        d.line(xy, fill=col + (255,), width=w, joint="curve")
    if glow:
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(9)))
    img.alpha_composite(lay)


def dot(img, view, p, col, r=22):
    x, y = proj(view)(p)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse((x - r, y - r, x + r, y + r), fill=col + (255,), outline=(255, 255, 255, 255), width=6)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6))); img.alpha_composite(lay)


RED, KUW, IRN, SAU = (214, 40, 40), (120, 70, 200), (60, 110, 160), (150, 130, 90)
IRAQ_COAST = [(47.94, 30.04), (48.2, 29.98), (48.45, 29.93), (48.55, 29.95)]          # approx coast trace for the glowing bracket
CHANNEL = [(47.95, 30.02), (48.10, 29.97), (48.25, 29.90), (48.40, 29.84), (48.55, 29.76)]   # Khor Abdullah centreline (approx)
DEEP = [(47.96, 30.00), (48.11, 29.95), (48.26, 29.88), (48.41, 29.82), (48.56, 29.74)]      # deep lane nearer Kuwait (schematic)


def base(view):
    return Image.open(f"/home/claude/v86/img/{view}.jpg").convert("RGBA")


SHOTS = {}
def shot(fn):
    SHOTS[fn.__name__] = fn
    return fn


@shot
def s01():
    im = base("A"); fill(im, "A", "Iraq", RED, 0.55, glow=(255, 80, 80))
    for n, c in (("Kuwait", KUW), ("Iran", IRN), ("Saudi Arabia", SAU)): fill(im, "A", n, c, 0.25, bw=2)
    line(im, "A", IRAQ_COAST, (255, 214, 0), w=14); return im

@shot
def s02():
    im = s01(); w, h = im.size; z = 1.25
    return im.crop((int(w * (1 - 1 / z) / 2), int(h * (1 - 1 / z) / 2), int(w * (1 + 1 / z) / 2), int(h * (1 + 1 / z) / 2))).resize((W, H))

@shot
def s03():
    im = base("B"); fill(im, "B", "Iraq", RED, 0.5, glow=(255, 80, 80)); fill(im, "B", "Kuwait", KUW, 0.45); fill(im, "B", "Iran", IRN, 0.45)
    line(im, "B", IRAQ_COAST, (255, 214, 0), w=10); return im

@shot
def s04():
    im = base("C"); fill(im, "C", "Iraq", RED, 0.35); fill(im, "C", "Kuwait", KUW, 0.35)
    line(im, "C", CHANNEL, (0, 229, 255), w=26); dot(im, "C", UMM_QASR, (255, 214, 0)); return im

@shot
def s05():
    im = base("C"); fill(im, "C", "Iraq", RED, 0.35); fill(im, "C", "Kuwait", KUW, 0.35)
    line(im, "C", CHANNEL, (255, 255, 255), w=8, dash=True); line(im, "C", DEEP, (0, 229, 255), w=22); return im

@shot
def s06():
    im = s04(); return im

@shot
def s07():
    im = base("C"); fill(im, "C", "Iraq", RED, 0.35); fill(im, "C", "Kuwait", KUW, 0.35)
    line(im, "C", CHANNEL, (0, 229, 255), w=18); dot(im, "C", MUBARAK, (160, 90, 255)); dot(im, "C", GRAND_FAW, (255, 80, 80)); return im

@shot
def s08():
    im = s07(); return im

@shot
def s09():
    return s01()


if __name__ == "__main__":
    for k, fn in SHOTS.items():
        fn().convert("RGB").save(f"/home/claude/v86/base/{k}.jpg", quality=90)
    print("ok", list(SHOTS))
