"""v12: '¿Y si?' style Short — stock footage + light-grey flat infographics + blue cube.

python3 engine12.py prep          -> cut stock clips into 1080x1920 frame folders
python3 engine12.py info | still N | video A B out.mp4
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from script11 import LINES

W, H, FPS = 1080, 1920, 30
MONT = "Montserrat.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# palette sampled from the reference
BG = (232, 234, 237)
INK = (26, 26, 28)
LABEL = (45, 45, 48)
CUBE_TOP = (88, 116, 168)
CUBE_L = (62, 89, 140)
CUBE_R = (47, 70, 114)
CUBE_EDGE = (30, 46, 80)
WATER = (168, 210, 227)
LAND = (241, 237, 229)
BORDER = (200, 194, 184)
ARROW = (224, 49, 45)
GREY_T = (150, 152, 158)

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


def END(i):
    return starts[i] + D[i]


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


_F = {}


def font(size, weight="SemiBold"):
    key = (int(size), weight)
    if key not in _F:
        f = ImageFont.truetype(MONT, max(1, int(size)))
        f.set_variation_by_name(weight)
        _F[key] = f
    return _F[key]


# ---------------------------------------------------------------- shot list
def S(t0, t1, kind, **p):
    return dict(t0=t0, t1=t1, kind=kind, **p)


SHOTS = [
    S(0, WT(0, "single"), "clip", src="crowd", off=1.0,
      ov=[("num", "8,000,000,000", WT(0, "eight"))]),
    S(WT(0, "single"), starts[1] - 0.1, "clip", src="skyscraper_up", off=0.5, ov=[("qmark", WT(0, "building"))]),
    S(starts[1] - 0.1, starts[2] - 0.05, "clip", src="city_aerial", off=3.0, ov=[("qmark", starts[1])]),
    S(starts[2] - 0.05, WT(2, "almost"), "map", view="alaska", ov=[("arrow", -148.68, 60.77, WT(2, "Whittier") + 0.2)]),
    S(WT(2, "almost"), WT(2, "one"), "clip", src="alaska", off=0.5),
    S(WT(2, "one"), starts[3] - 0.05, "photo", src="begich", z=(1.0, 1.12), c=(0.5, 0.55, 0.47, 0.6)),
    S(starts[3] - 0.05, WT(3, "police"), "clip", src="post", off=1.0),
    S(WT(3, "police"), WT(3, "clinic") - 0.1, "clip", src="police", off=2.0),
    S(WT(3, "clinic") - 0.1, WT(3, "church") - 0.1, "clip", src="clinic", off=2.0),
    S(WT(3, "church") - 0.1, starts[4] - 0.05, "clip", src="church", off=3.0),
    S(starts[4] - 0.05, starts[5] - 0.05, "clip", src="crowd_aerial", off=5.0),
    S(starts[5] - 0.05, WT(5, "seats") - 0.1, "clip", src="race", off=1.0),
    S(WT(5, "seats") - 0.1, starts[6] - 0.05, "photo", src="indy", z=(1.0, 1.15), c=(0.5, 0.6, 0.45, 0.58),
      ov=[("num", "250,000", WT(5, "quarter"))]),
    S(starts[6] - 0.05, starts[7] - 0.05, "clip", src="mecca", off=2.0, ov=[("num", "2,000,000", WT(6, "two"))]),
    S(starts[7] - 0.05, starts[8] - 0.05, "info", draw="compare"),
    S(starts[8] - 0.05, starts[9] - 0.05, "info", draw="density"),
    S(starts[9] - 0.05, WT(9, "covers"), "photo", src="gigatx", z=(1.05, 1.2), c=(0.5, 0.5, 0.62, 0.5)),
    S(WT(9, "covers"), starts[10] - 0.05, "info", draw="factory"),
    S(starts[10] - 0.05, starts[11] - 0.05, "map", view="world", ov=[("country_num", WT(10, "three")),
                                                                      ("flag", -56.0, -32.8, "🇺🇾", WT(10, "country"))]),
    S(starts[11] - 0.05, WT(11, "biggest") - 0.1, "photo", src="boeing", z=(1.0, 1.15), c=(0.42, 0.5, 0.5, 0.5)),
    S(WT(11, "biggest") - 0.1, starts[12] - 0.05, "clip", src="jet", off=1.0),
    S(starts[12] - 0.05, starts[13] - 0.05, "info", draw="volume"),
    S(starts[13] - 0.05, starts[14] - 0.05, "info", draw="m3"),
    S(starts[14] - 0.05, starts[15] - 0.05, "info", draw="bigcube"),
    S(starts[15] - 0.05, starts[16] - 0.05, "sat", cam=((0.0, 55, 9000), (20.0, 48, 5200)), drop=WT(15, "Drop") + 0.2,
      park=WT(15, "Central")),
    S(starts[16] - 0.05, starts[17] - 0.05, "info", draw="heights"),
    S(starts[17] - 0.05, TOTAL, "sat", cam=((40.0, 50, 6500), (70.0, 44, 5400)), drop=-1, walker=WT(17, "walk")),
]
CUTS = [s["t0"] for s in SHOTS[1:]]


def shot_at(t):
    for s in SHOTS:
        if s["t0"] <= t < s["t1"]:
            return s
    return SHOTS[-1]


# ---------------------------------------------------------------- media
def prep():
    os.makedirs("frames", exist_ok=True)
    for s in SHOTS:
        if s["kind"] != "clip":
            continue
        dur = s["t1"] - s["t0"] + 0.2
        out = f"frames/{s['src']}_{int(s['off'] * 10)}"
        if os.path.isdir(out) and len(os.listdir(out)) >= int(dur * FPS):
            continue
        os.makedirs(out, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(s["off"]), "-t", f"{dur:.2f}",
                        "-i", f"media/{s['src']}.mp4", "-vf",
                        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=saturation=1.05",
                        "-q:v", "3", f"{out}/%05d.jpg"], check=True)
        print("clip", out, len(os.listdir(out)))


def clip_frame(s, t):
    d = f"frames/{s['src']}_{int(s['off'] * 10)}"
    n = len(os.listdir(d))
    i = min(n, int((t - s["t0"]) * FPS) + 1)
    return Image.open(f"{d}/{i:05d}.jpg").convert("RGB")


_PH = {}


def photo_frame(s, t):
    if s["src"] not in _PH:
        _PH[s["src"]] = Image.open(f"media/{s['src']}.jpg").convert("RGB")
    im = _PH[s["src"]]
    k = ease((t - s["t0"]) / max(0.1, s["t1"] - s["t0"]))
    z = s["z"][0] + (s["z"][1] - s["z"][0]) * k
    cxr = s["c"][0] + (s["c"][2] - s["c"][0]) * k
    cyr = s["c"][1] + (s["c"][3] - s["c"][1]) * k
    # cover-crop a 9:16 window
    bw = min(im.width, im.height * W / H) / z
    bh = bw * H / W
    cx, cy = cxr * im.width, cyr * im.height
    x0 = min(im.width - bw, max(0, cx - bw / 2))
    y0 = min(im.height - bh, max(0, cy - bh / 2))
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))


# ---------------------------------------------------------------- flat map
_SHP = shapefile.Reader("assets/ne50/ne_50m_admin_0_countries.shp")
_FLD = [f[0] for f in _SHP.fields[1:]]
SHAPES = []
for sr in _SHP.iterShapeRecords():
    pts = sr.shape.points
    parts = list(sr.shape.parts) + [len(pts)]
    for a, b in zip(parts[:-1], parts[1:]):
        SHAPES.append(np.array(pts[a:b]))


def merc_y(lat):
    lat = np.clip(lat, -85, 85)
    return np.degrees(np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)))


MAPVIEWS = {"alaska": ((-152.0, 63.5, 40.0), (-149.0, 62.0, 16.0)),
            "world": ((-20.0, 15.0, 300.0), (-40.0, 0.0, 260.0))}


def map_frame(s, t):
    (l0, a0, s0), (l1, a1, s1) = MAPVIEWS[s["view"]]
    k = ease((t - s["t0"]) / max(0.1, s["t1"] - s["t0"]))
    lon, lat, span = l0 + (l1 - l0) * k, a0 + (a1 - a0) * k, s0 * (s1 / s0) ** k
    ppd = W / span
    cy = merc_y(lat)
    img = Image.new("RGB", (W, H), WATER)
    d = ImageDraw.Draw(img)
    proj = lambda lo, la: ((lo - lon) * ppd + W / 2, (cy - merc_y(la)) * ppd + H / 2)  # noqa: E731
    for r in SHAPES:
        for shift in ((0,) if span < 200 else (-360, 0, 360)):
            x = (r[:, 0] + shift - lon) * ppd + W / 2
            y = (cy - merc_y(r[:, 1])) * ppd + H / 2
            if x.max() < 0 or x.min() > W or y.max() < 0 or y.min() > H:
                continue
            pts = list(zip(x.tolist(), y.tolist()))
            if len(pts) > 2:
                d.polygon(pts, fill=LAND, outline=BORDER)
    s["_proj"] = proj
    return img


# ---------------------------------------------------------------- drawing helpers
def text_c(d, xy, txt, size, fill=LABEL, weight="SemiBold", anchor="mm"):
    d.text(xy, txt, font=font(size, weight), fill=fill, anchor=anchor)


def white_number(img, txt, k, y=H * 0.45, size=150):
    if k <= 0:
        return
    a = int(255 * min(1, k))
    while font(size, "Bold").getlength(txt) > W - 90:
        size *= 0.92
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((W / 2 + 4, y + 6), txt, font=font(size, "Bold"), fill=(0, 0, 0, int(a * 0.6)),
                            anchor="mm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((W / 2, y), txt, font=font(size, "Bold"), fill=(255, 255, 255, a), anchor="mm")
    img.alpha_composite(lay)


def pictogram(d, x, y, h, col=INK, female=False):
    """Restroom-sign style person, feet at (x, y), height h px."""
    r = h * 0.085
    d.ellipse((x - r, y - h, x + r, y - h + 2 * r), fill=col)
    top = y - h + 2.4 * r
    bw = h * 0.24
    if female:
        d.polygon([(x - bw * 0.35, top), (x + bw * 0.35, top), (x + bw * 0.62, top + h * 0.42),
                   (x - bw * 0.62, top + h * 0.42)], fill=col)
    else:
        d.rounded_rectangle((x - bw / 2, top, x + bw / 2, top + h * 0.42), radius=bw * 0.18, fill=col)
    lw = bw * 0.2
    d.rounded_rectangle((x - bw / 2 - lw * 1.15, top + h * 0.02, x - bw / 2 - lw * 0.15, top + h * 0.36),
                        radius=lw / 2, fill=col)
    d.rounded_rectangle((x + bw / 2 + lw * 0.15, top + h * 0.02, x + bw / 2 + lw * 1.15, top + h * 0.36),
                        radius=lw / 2, fill=col)
    lg = bw * 0.22
    d.rounded_rectangle((x - lg * 1.05, top + h * 0.4, x - lg * 0.05, y), radius=lg / 2, fill=col)
    d.rounded_rectangle((x + lg * 0.05, top + h * 0.4, x + lg * 1.05, y), radius=lg / 2, fill=col)


def iso_cube(img, cx, base_y, size, k=1.0, alpha=255, labels=None, lab_t=None, t=0.0):
    """Navy cube in a light 3/4 view (like the reference). size = edge px. k = extrusion 0..1."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    dx, dy = size * 0.42, size * 0.22  # depth offset (receding to upper right)
    hgt = size * k
    x0, x1 = cx - size / 2 - dx / 2, cx + size / 2 - dx / 2
    yb = base_y
    front = [(x0, yb), (x1, yb), (x1, yb - hgt), (x0, yb - hgt)]
    side = [(x1, yb), (x1 + dx, yb - dy), (x1 + dx, yb - dy - hgt), (x1, yb - hgt)]
    top = [(x0, yb - hgt), (x1, yb - hgt), (x1 + dx, yb - dy - hgt), (x0 + dx, yb - dy - hgt)]
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).polygon([(x0 + 10, yb + 8), (x1 + 16, yb + 8), (x1 + dx + 16, yb - dy + 8),
                                    (x0 + dx + 10, yb - dy + 8)], fill=(0, 0, 0, 60))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14)))
    d.polygon(front, fill=CUBE_L + (alpha,))
    d.polygon(side, fill=CUBE_R + (alpha,))
    d.polygon(top, fill=CUBE_TOP + (alpha,))
    for poly in (front, side, top):
        d.line(poly + [poly[0]], fill=CUBE_EDGE + (255,), width=3)
    img.alpha_composite(lay)
    if labels:
        dd = ImageDraw.Draw(img)
        pos = [((x0 + x1) / 2, yb + 44, "mm"), (x1 + dx / 2 + 16, yb - dy / 2 + 40, "lm"),
               (x1 + dx + 22, yb - dy - hgt / 2, "lm")]
        for j, txt in enumerate(labels):
            if lab_t is None or t >= lab_t[j]:
                text_c(dd, pos[j][:2], txt, 44, LABEL, "SemiBold", pos[j][2])


# ---------------------------------------------------------------- infographic scenes
def info_bg():
    img = Image.new("RGBA", (W, H), BG + (255,))
    return img


def draw_compare(img, t, s):
    d = ImageDraw.Draw(img)
    i = 7
    if t < WT(i, "forget") - 0.05:
        text_c(d, (W / 2, 760), "2,000,000", 92, INK, "Bold")
        text_c(d, (W / 2, 860), "vs", 50, GREY_T, "Medium")
        text_c(d, (W / 2, 960), "8,000,000,000", 92, INK, "Bold")
        # tiny bar: the real proportion is invisible
        d.rounded_rectangle((140, 1110, 940, 1150), radius=20, outline=INK, width=4)
        d.rounded_rectangle((144, 1114, 148, 1146), radius=2, fill=ARROW)
    else:
        k = ease((t - WT(i, "forget") + 0.05) / 0.35)
        side = 520
        x0, y0 = W / 2 - side / 2, H / 2 - side / 2 - 60
        d.rectangle((x0, y0, x0 + side, y0 + side), outline=INK, width=6)
        if t >= WT(i, "measure"):
            text_c(d, (W / 2, y0 + side + 90), "m²", 70, LABEL, "SemiBold")


def draw_density(img, t, s):
    d = ImageDraw.Draw(img)
    i = 8
    side = 560
    x0, y0 = W / 2 - side / 2 + 40, H / 2 - side / 2 - 60
    d.rectangle((x0, y0, x0 + side, y0 + side), outline=INK, width=6)
    text_c(d, (x0 - 40, y0 + side / 2), "1 m²", 58, LABEL, "SemiBold", "rm")
    order = [(0.28, 0.48), (0.72, 0.48), (0.28, 0.95), (0.72, 0.95)]
    t_in = [WT(i, "Pack"), WT(i, "shoulder"), WT(i, "four"), WT(i, "four") + 0.25]
    for (fx, fy), tt in zip(order, t_in):
        if t >= tt:
            pictogram(d, x0 + side * fx, y0 + side * fy - 14, side * 0.4)


def draw_factory(img, t, s):
    d = ImageDraw.Draw(img)
    i = 9
    # dark rounded block like the reference factory icon
    bx0, by0, bx1, by1 = 300, 520, 780, 1240
    d.rounded_rectangle((bx0 + 10, by0 + 14, bx1 + 10, by1 + 14), radius=70, fill=(200, 202, 206))
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=70, fill=(66, 68, 74), outline=(40, 41, 45), width=6)
    text_c(d, ((bx0 + bx1) / 2, by0 + 260), "GIGA", 70, (235, 235, 238), "Bold")
    text_c(d, ((bx0 + bx1) / 2, by0 + 350), "TEXAS", 70, (235, 235, 238), "Bold")
    if t >= WT(i, "square") - 0.2:
        text_c(d, ((bx0 + bx1) / 2, by1 - 160), "0.93 km²", 64, (255, 214, 120), "Bold")


def draw_volume(img, t, s):
    d = ImageDraw.Draw(img)
    i = 12
    cx, base = W / 2, 1180
    hpx = 600
    # transparent box around a standing person (0.413 m³)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    bw = 330
    ld.polygon([(cx - bw / 2, base), (cx + bw / 2, base), (cx + bw / 2, base - hpx), (cx - bw / 2, base - hpx)],
               fill=CUBE_L + (110,))
    ld.polygon([(cx + bw / 2, base), (cx + bw / 2 + 90, base - 50), (cx + bw / 2 + 90, base - hpx - 50),
                (cx + bw / 2, base - hpx)], fill=CUBE_R + (130,))
    ld.polygon([(cx - bw / 2, base - hpx), (cx + bw / 2, base - hpx), (cx + bw / 2 + 90, base - hpx - 50),
                (cx - bw / 2 + 90, base - hpx - 50)], fill=CUBE_TOP + (120,))
    img.alpha_composite(lay)
    pictogram(d, cx + 20, base - 6, hpx * 0.96)
    d.polygon([(cx - bw / 2, base), (cx + bw / 2, base), (cx + bw / 2, base - hpx), (cx - bw / 2, base - hpx)],
              outline=CUBE_EDGE, width=3)
    text_c(d, (cx, base - hpx - 130), "0.413 m³", 62, (40, 150, 70), "Bold")
    text_c(d, (cx - bw / 2 - 30, base - hpx / 2), "1.65 m", 44, LABEL, "SemiBold", "rm")
    if t >= WT(i, "thirty") - 0.2:
        text_c(d, (cx, base + 150), "32,000,000", 96, INK, "Bold")
        text_c(d, (cx, base + 240), "people", 48, GREY_T, "Medium")


def draw_m3(img, t, s):
    d = ImageDraw.Draw(img)
    i = 13
    iso_cube(img, 380, 1050, 300)
    text_c(d, (335, 1120), "1 m³", 54, LABEL, "SemiBold")
    if t >= WT(i, "cubic") - 0.4:
        text_c(d, (800, 900), "×", 80, LABEL, "Medium")
        text_c(d, (800, 1000), "3,300,000,000", 58, INK, "Bold")


def draw_bigcube(img, t, s):
    i = 14
    k = ease((t - s["t0"]) / 0.9)
    iso_cube(img, W / 2 - 30, 1260, 560, k, labels=["1.5 km", "1.5 km", "1.5 km"],
             lab_t=[WT(i, "kilometer"), WT(i, "kilometer") + 0.25, WT(i, "every")], t=t)


def draw_heights(img, t, s):
    d = ImageDraw.Draw(img)
    i = 16
    ground = 1380
    sc = 0.62  # px per meter
    # the cube (1,500 m)
    k = ease((t - s["t0"]) / 0.6)
    side = 1500 * sc * 0.62  # front face drawn narrower than true scale is NOT used: keep height honest
    iso_cube(img, 400, ground, 1500 * sc * 0.6, 1.0)
    # NOTE: iso_cube draws an equal-sided cube; its height equals its edge
    edge = 1500 * sc * 0.6
    text_c(d, (400 - edge * 0.21, ground + 46), "1,500 m", 46, LABEL, "SemiBold")
    # Burj Khalifa silhouette at the same scale as the cube's height
    if t >= WT(i, "Burj") - 0.5:
        hb = 828 / 1500 * edge
        bx = 900
        poly = [(bx - 26, ground), (bx - 20, ground - hb * 0.45), (bx - 12, ground - hb * 0.7),
                (bx - 6, ground - hb * 0.86), (bx - 2, ground - hb), (bx + 2, ground - hb),
                (bx + 6, ground - hb * 0.86), (bx + 12, ground - hb * 0.7), (bx + 20, ground - hb * 0.45),
                (bx + 26, ground)]
        d.polygon(poly, fill=(170, 172, 178))
        text_c(d, (bx, ground + 46), "828 m", 46, LABEL, "SemiBold")
    d.line([(60, ground), (W - 60, ground)], fill=(190, 192, 196), width=3)


INFO = {"compare": draw_compare, "density": draw_density, "factory": draw_factory, "volume": draw_volume,
        "m3": draw_m3, "bigcube": draw_bigcube, "heights": draw_heights}

# ---------------------------------------------------------------- tilted satellite + 3D cube
META = json.load(open("manhattan_meta.json"))
_SAT = None
CP = (40.7829, -73.9654)
CP_CORNERS = [(40.7644, -73.9730), (40.7968, -73.9496), (40.8006, -73.9580), (40.7681, -73.9819)]


def ll_to_m(lat, lon):
    """Local metres (east, north) from Central Park centre."""
    return ((lon - CP[1]) * 111320 * math.cos(math.radians(CP[0])), (lat - CP[0]) * 110540)


def m_to_sat_px(e, n):
    mpp = META["mpp"]
    x = (META["cx"] - META["x0"]) * 256 + e / mpp
    y = (META["cy"] - META["y0"]) * 256 - n / mpp
    return x, y


def camera(heading, tilt, dist):
    h, tl = math.radians(heading), math.radians(tilt)
    target = np.array([0.0, 0.0, 300.0])
    back = np.array([-math.sin(h), -math.cos(h), 0.0])
    cam = target + dist * (math.sin(tl) * back + math.cos(tl) * np.array([0, 0, 1.0]))
    f = target - cam
    f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.0])
    r /= np.linalg.norm(r)
    u = np.cross(r, f)
    F = (H / 2) / math.tan(math.radians(26))
    return cam, f, r, u, F


def project(P, C):
    cam, f, r, u, F = C
    v = np.asarray(P, float) - cam
    zc = v @ f
    return W / 2 + F * (v @ r) / zc, H / 2 - F * (v @ u) / zc, zc


def homography(src, dst):
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    b = [c for p in dst for c in p]
    return np.linalg.solve(np.array(A, float), np.array(b, float))


def sat_frame(s, t, img_out=None):
    global _SAT
    if _SAT is None:
        _SAT = Image.open("manhattan_z15.jpg").convert("RGB")
    k = ease((t - s["t0"]) / max(0.1, s["t1"] - s["t0"]))
    (h0, t0_, d0), (h1, t1_, d1) = s["cam"]
    C = camera(h0 + (h1 - h0) * k, t0_ + (t1_ - t0_) * k, d0 + (d1 - d0) * k)
    # ground plane homography: screen -> satellite pixels
    ground = [(-2500, -2500), (2500, -2500), (2500, 2500), (-2500, 2500)]
    scr = [project((e, n, 0), C)[:2] for e, n in ground]
    sat = [m_to_sat_px(e, n) for e, n in ground]
    coef = homography(scr, sat)
    img = _SAT.transform((W, H), Image.PERSPECTIVE, tuple(coef), Image.BILINEAR, fillcolor=(150, 170, 185))
    # haze toward the horizon
    yy = np.linspace(0, 1, H)[:, None, None]
    a = np.asarray(img).astype(np.float32)
    haze = np.clip(1 - yy * 2.2, 0, 1) ** 1.5 * 0.55
    a = a * (1 - haze) + np.array([196, 210, 222]) * haze
    img = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    if s.get("park") and t >= s["park"]:
        pk = ease((t - s["park"]) / 0.4)
        pts = [project((*ll_to_m(la, lo), 0), C)[:2] for la, lo in CP_CORNERS]
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).polygon(pts, fill=(80, 200, 110, int(60 * pk)), outline=(80, 200, 110, int(230 * pk)),
                                    width=5)
        img.alpha_composite(lay)
    # the cube: 1.5 km footprint aligned with the Manhattan grid (29 deg)
    drop_k = 1.0 if s["drop"] < 0 else ease((t - s["drop"]) / 0.9)
    if drop_k > 0:
        a29 = math.radians(29)
        hs = 750
        base = []
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            e = sx * hs * math.cos(a29) + sy * hs * math.sin(a29)
            n = -sx * hs * math.sin(a29) + sy * hs * math.cos(a29)
            base.append((e, n))
        z1 = 1500 * drop_k
        P0 = [(e, n, 0) for e, n in base]
        P1 = [(e, n, z1) for e, n in base]
        faces = [P1]  # top
        for j in range(4):
            faces.append([P0[j], P0[(j + 1) % 4], P1[(j + 1) % 4], P1[j]])
        cols = [CUBE_TOP, CUBE_L, CUBE_R, CUBE_L, CUBE_R]
        proj = [[project(p, C) for p in f] for f in faces]
        order = sorted(range(len(faces)), key=lambda j: -np.mean([p[2] for p in proj[j]]))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        for j in order:
            pts = [(p[0], p[1]) for p in proj[j]]
            ld.polygon(pts, fill=cols[j] + (175,))
            ld.line(pts + [pts[0]], fill=CUBE_EDGE + (255,), width=3)
        img.alpha_composite(lay)
        if drop_k > 0.98:
            pa = project(P0[0], C)
            pb = project(P0[1], C)
            text_c(ImageDraw.Draw(img), ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2 + 50), "1.5 km", 46,
                   (255, 255, 255), "Bold")
    if s.get("walker") and t >= s["walker"]:
        wk = ease((t - s["walker"]) / 2.4)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle((W / 2 - 230, 230, W / 2 + 230, 350), radius=60, fill=(255, 255, 255, 230))
        img.alpha_composite(lay)
        dd = ImageDraw.Draw(img)
        pictogram(dd, W / 2 - 150, 330, 86)
        text_c(dd, (W / 2 + 40, 290), f"{int(round(20 * wk))} min", 64, INK, "Bold")
    return img


# ---------------------------------------------------------------- frame
def overlays(img, s, t):
    for o in s.get("ov", []):
        kind = o[0]
        if kind == "num" and t >= o[2]:
            white_number(img, o[1], (t - o[2]) / 0.25)
        elif kind == "qmark" and t >= o[1]:
            white_number(img, "?", (t - o[1]) / 0.2, y=H * 0.42, size=420)
        elif kind == "arrow" and t >= o[3]:
            x, y = s["_proj"](o[1], o[2])
            k = ease((t - o[3]) / 0.3)
            d = ImageDraw.Draw(img)
            sx, sy = x + 210, y - 260
            ex, ey = sx + (x - sx) * k, sy + (y - sy) * k
            d.line([(sx, sy), (ex, ey)], fill=ARROW, width=9)
            if k > 0.9:
                ang = math.atan2(y - sy, x - sx)
                for da in (2.6, -2.6):
                    d.line([(x, y), (x + 40 * math.cos(ang + da), y + 40 * math.sin(ang + da))], fill=ARROW,
                           width=9)
                text_c(d, (sx + 10, sy - 50), "Whittier", 52, INK, "SemiBold")
        elif kind == "flag" and t >= o[4]:
            x, y = s["_proj"](o[1], o[2])
            k = ease((t - o[4]) / 0.25)
            f = ImageFont.truetype(EMOJI, 109)
            fl = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
            ImageDraw.Draw(fl).text((80, 80), o[3], font=f, embedded_color=True, anchor="mm")
            sz = int(120 * k) + 1
            img.alpha_composite(fl.resize((sz, sz), Image.LANCZOS), (int(x - sz / 2), int(y - sz / 2)))
        elif kind == "country_num" and t >= o[1]:
            d = ImageDraw.Draw(img)
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ImageDraw.Draw(lay).rounded_rectangle((170, 300, 910, 470), radius=30, fill=(255, 255, 255, 235))
            img.alpha_composite(lay)
            text_c(ImageDraw.Draw(img), (W / 2, 385), "3,700,000", 96, INK, "Bold")


def frame(fi):
    t = fi / FPS
    s = shot_at(t)
    k = s["kind"]
    if k == "clip":
        img = clip_frame(s, t).convert("RGBA")
    elif k == "photo":
        img = photo_frame(s, t).convert("RGBA")
    elif k == "map":
        img = map_frame(s, t).convert("RGBA")
    elif k == "sat":
        img = sat_frame(s, t)
    else:
        img = info_bg()
        INFO[s["draw"]](img, t, s)
    overlays(img, s, t)
    return img.convert("RGB")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prep":
        prep()
    elif cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for s in SHOTS:
            print(round(s["t0"], 2), round(s["t1"], 2), s["kind"], s.get("src") or s.get("draw") or s.get("view") or "")
    elif cmd == "still":
        frame(int(sys.argv[2])).save(f"still_{sys.argv[2]}.png")
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
