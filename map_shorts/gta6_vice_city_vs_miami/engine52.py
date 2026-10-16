"""GTA 6 'Vice City vs REAL Miami' 16:9 long video. python3 engine52.py info | still t.. | video A B out.mp4"""
import glob, json, math, os, subprocess, sys
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script52 import LINES

W, H, FPS = 1920, 1080, 30
POPX, POPB, TITAN = "Poppins-ExtraBold.ttf", "Poppins-Bold.ttf", "fonts/titan-one.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (70, 205, 100), (80, 170, 255), (255, 255, 255), (0, 0, 0)
ORG, CYAN, PINK, MONEY = (255, 150, 40), (90, 220, 255), (255, 80, 160), (110, 220, 110)
TM = json.load(open("timing.json")); D, TW, V0 = TM["D"], TM["T"], TM["starts"]
N = len(LINES); LEAD = 3.0
ST = [LEAD + v for v in V0]
TOTAL = ST[-1] + D[-1] + 4.0
NF = int(TOTAL * FPS)
_FONTS = {}


def font(path, size):
    k = (path, int(size))
    if k not in _FONTS: _FONTS[k] = ImageFont.truetype(path, max(8, int(size)))
    return _FONTS[k]


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def clean(w): return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word, nth=0):
    ws = [clean(w) for w in LINES[i].split()]; q = clean(word)
    hits = [j for j, w in enumerate(ws) if w == q] or [j for j, w in enumerate(ws) if q in w]
    if not hits: raise KeyError((i, word))
    return ST[i] + TW[i][hits[min(nth, len(hits) - 1)]]


BL = [0.0] + [ST[i] - 0.15 for i in range(1, N)] + [TOTAL]

# ------------------------------------------------------------------ geo
SP = {"FL": (-83.0, 27.6, 3.6), "MIA": (-80.20, 25.80, 0.16), "OB": (-80.1310, 25.7800, 0.008), "PORT": (-80.1650, 25.7770, 0.012),
      "MAC": (-80.1600, 25.7860, 0.014), "BRK": (-80.1920, 25.7640, 0.010), "CIRC": (-80.18925, 25.76985, 0.0012), "PCK": (-80.2405, 25.7275, 0.004),
      "OPA": (-80.2506, 25.9017, 0.003), "LH": (-80.2193, 25.7656, 0.003), "WYN": (-80.1993, 25.8011, 0.003), "KAS": (-80.1881, 25.7814, 0.003),
      "MET": (-80.1930, 25.7745, 0.004), "VEN": (-80.1600, 25.7915, 0.012), "KEYS": (-81.165, 24.705, 0.03), "EVG": (-80.70, 25.45, 0.5)}


def geo(key, lon, lat):
    lon0, lat0, d = SP[key]; dl = d * (16 / 9) / math.cos(math.radians(lat0))
    return ((lon - (lon0 - dl)) / (2 * dl), (lat0 + d - lat) / (2 * d))


@lru_cache(maxsize=20)
def sat(key): return Image.open(f"sat/{key}.jpg").convert("RGB")


def view(im, z, cx, cy, w=W, h=H):
    """crop+resize with float box; returns image and (x0, y0, scale) to map source px -> screen"""
    iw, ih = im.size; s = max(w / iw, h / ih) * z; bw, bh = w / s, h / s
    x0 = min(max(0.0, cx * iw - bw / 2), iw - bw); y0 = min(max(0.0, cy * ih - bh / 2), ih - bh)
    return im.resize((w, h), Image.BILINEAR, box=(x0, y0, x0 + bw, y0 + bh)), (x0, y0, s)


# ------------------------------------------------------------------ clips
BARS = json.load(open("bars.json"))


@lru_cache(maxsize=80)
def fr(name, idx):
    im = Image.open(f"frames/{name}_{idx:04d}.jpg").convert("RGB"); tb = BARS.get(name)
    if tb and (tb[0] or tb[1]):
        w, h = im.size; im = im.crop((0, int(h * tb[0]) + 3 if tb[0] else 0, w, h - int(h * tb[1]) - 3 if tb[1] else h))
    return im


@lru_cache(maxsize=40)
def nfr(name): return len(glob.glob(f"frames/{name}_[0-9][0-9][0-9][0-9].jpg"))


def clip_frame(name, sec):
    n = nfr(name); f = max(0.0, sec * 24); per = 2 * (n - 1.001)
    f = f % per; f = per - f if f > n - 1.001 else f                 # ping-pong if the shot is longer than the clip
    i = int(f); u = f - i; a = fr(name, i + 1)
    return a if u < 0.03 or i + 2 > n else Image.blend(a, fr(name, i + 2), u)


def best(name):                                                     # prefer the Kling take where we have one
    return name + "_kling" if os.path.exists(f"frames/{name}_kling_0001.jpg") else name


# ------------------------------------------------------------------ text helpers
def fit(fname, size, txt, maxw):
    f = font(fname, size)
    while f.getlength(txt) > maxw and f.size > 14: f = font(fname, f.size - 2)
    return f


def glow_text(img, xy, txt, f, col, a=1.0, anchor="mm", glow=None, stroke=None):
    x, y = xy; bb = ImageDraw.Draw(img).textbbox((x, y), txt, font=f, anchor=anchor, stroke_width=(stroke or 3))
    pad = 40; box = (int(bb[0] - pad), int(bb[1] - pad), int(bb[2] + pad), int(bb[3] + pad))
    pw, ph = box[2] - box[0], box[3] - box[1]
    if pw <= 0 or ph <= 0: return
    loc = (x - box[0], y - box[1])
    if glow:
        g = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); ImageDraw.Draw(g).text(loc, txt, font=f, fill=glow + (int(220 * a),), anchor=anchor, stroke_width=max(6, int(f.size * 0.18)), stroke_fill=glow + (int(220 * a),))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(12)), (box[0], box[1]))
    sh = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((loc[0] + 3, loc[1] + 5), txt, font=f, fill=(0, 0, 0, int(160 * a)), anchor=anchor)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), (box[0], box[1]))
    ImageDraw.Draw(img).text((x, y), txt, font=f, fill=col + (int(255 * a),), anchor=anchor, stroke_width=stroke or max(2, int(f.size * 0.06)), stroke_fill=(0, 0, 0, int(220 * a)))


def pop_k(t, t0, dur=0.18): return ease((t - t0) / dur)


def label(img, txt, x, y, t, t0, size=64, col=WHT, glow=None, anchor="mm", maxw=W - 160, fname=POPX):
    if t < t0: return
    k = pop_k(t, t0); s = 1.25 - 0.25 * k
    glow_text(img, (x, y), txt, fit(fname, size * s, txt, maxw * s), col, min(1.0, k * 1.5), anchor, glow)


def pill(img, txt, cx, cy, sz, bg, fg=WHT, a=1.0, anchor="mm"):
    f = font(POPX, sz); pw, ph = f.getlength(txt) + sz * 1.3, sz * 1.75
    x0 = cx - pw / 2 if anchor == "mm" else cx if anchor == "lm" else cx - pw
    d = ImageDraw.Draw(img); d.rounded_rectangle((x0, cy - ph / 2, x0 + pw, cy + ph / 2), int(ph * 0.3), fill=bg + (int(230 * a),), outline=WHT + (int(255 * a),), width=2)
    d.text((x0 + pw / 2, cy), txt, font=f, fill=fg + (int(255 * a),), anchor="mm")
    return pw


BADGE = {"text": ("OFFICIAL  ·  ROCKSTAR TEXT", (30, 150, 80)), "sign": ("OFFICIAL  ·  SEEN ON A SIGN", (30, 110, 200)),
         "region": ("OFFICIAL  ·  REGION NAME", (30, 150, 80)), "fan": ("FAN MATCH  ·  NOT CONFIRMED", (220, 110, 20)),
         "wiki": ("FAN WIKIS", (220, 110, 20)), "real": ("REAL HISTORY", (120, 60, 170))}


def badge(img, kind, cx, cy, t, t0, sz=26, anchor="mm"):
    if t < t0: return
    txt, c = BADGE[kind]; k = pop_k(t, t0, 0.22)
    pill(img, txt, cx + (1 - k) * (-60 if anchor == "lm" else 0), cy, sz, c, a=k, anchor=anchor)


def shade(img, h=360, a0=170, bottom=False):
    g = np.zeros((h, 1), np.float32); g[:, 0] = a0 * (1 - np.arange(h) / h) ** 1.4
    m = Image.fromarray(g.astype(np.uint8)).resize((W, h))
    if bottom: m = m.transpose(Image.FLIP_TOP_BOTTOM)
    img.alpha_composite(Image.merge("RGBA", (Image.new("L", (W, h), 0),) * 3 + (m,)), (0, H - h if bottom else 0))


def counter(img, v0, v1, fmt, x, y, t, t0, dur, size, col=YEL, glow=None, anchor="mm"):
    if t < t0: return
    v = v0 + (v1 - v0) * ease((t - t0) / dur); label(img, fmt.format(v), x, y, t, t0, size, col, glow, anchor)


def grad_title(img, txt, cx, cy, size, t, t0, maxw=W - 200):
    if t < t0: return
    k = ease((t - t0) / 0.25); f = font(TITAN, size * (1.4 - 0.4 * k))
    while f.getlength(txt) > maxw and f.size > 20: f = font(TITAN, f.size - 2)
    bb = ImageDraw.Draw(img).textbbox((cx, cy), txt, font=f, anchor="mm", stroke_width=20)
    pad = 40; box = (int(bb[0] - pad), int(bb[1] - pad), int(bb[2] + pad), int(bb[3] + pad)); pw, ph = box[2] - box[0], box[3] - box[1]
    loc = (cx - box[0], cy - box[1]); lay = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    gl = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); ImageDraw.Draw(gl).text(loc, txt, font=f, fill=PINK + (220,), anchor="mm", stroke_width=24, stroke_fill=PINK + (220,))
    lay.alpha_composite(gl.filter(ImageFilter.GaussianBlur(16)))
    d = ImageDraw.Draw(lay); d.text(loc, txt, font=f, fill=BLK + (255,), anchor="mm", stroke_width=16, stroke_fill=BLK + (255,))
    d.text(loc, txt, font=f, fill=WHT + (255,), anchor="mm", stroke_width=5, stroke_fill=WHT + (255,))
    m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).text(loc, txt, font=f, fill=255, anchor="mm"); b2 = m.getbbox()
    if b2:
        g = np.zeros((ph, pw, 3), np.uint8); stops = ((255, 214, 64), (255, 132, 52), (255, 52, 140), (150, 50, 210))
        for y in range(b2[1], b2[3] + 1):
            tt = (y - b2[1]) / max(1, b2[3] - b2[1]); kk = tt * 3; i = min(int(kk), 2); u = kk - i
            g[y] = [int(stops[i][c] * (1 - u) + stops[i + 1][c] * u) for c in range(3)]
        gi = Image.fromarray(g).convert("RGBA"); gi.putalpha(m.filter(ImageFilter.MinFilter(7))); lay.alpha_composite(gi)
    if k < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * min(1.0, k * 1.6))))
    img.alpha_composite(lay, (box[0], box[1]))


def quote(img, lead, txt, t, t0, y=250):
    if t < t0: return
    k = ease((t - t0) / 0.3); f = font(POPX, 50); f2 = font(POPB, 26)
    lines = []; cur = ""
    for w in txt.split():
        if f.getlength(cur + " " + w) > 1180 and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur); h = 70 + 64 * len(lines); x0 = 120 - (1 - k) * 80
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((x0, y, x0 + 1300, y + h), 18, fill=(10, 8, 24, int(205 * k))); d.rectangle((x0, y, x0 + 10, y + h), fill=PINK + (int(255 * k),))
    d.text((x0 + 40, y + 34), lead, font=f2, fill=PINK + (int(255 * k),), anchor="lm")
    for q, l in enumerate(lines): d.text((x0 + 40, y + 82 + q * 64), l, font=f, fill=WHT + (int(255 * k),), anchor="lm")
    img.alpha_composite(lay)


def tags(img, items, t, x=120, y0=300, dy=78, size=40):
    for q, (txt, t0) in enumerate(items):
        if t < t0: continue
        k = ease((t - t0) / 0.2); f = font(POPX, size); w = f.getlength(txt) + 60; y = y0 + q * dy; xx = x - (1 - k) * 120
        d = ImageDraw.Draw(img); d.rounded_rectangle((xx, y - 30, xx + w, y + 30), 14, fill=(10, 8, 24, int(200 * k)), outline=CYAN + (int(255 * k),), width=3)
        d.text((xx + 30, y), txt, font=f, fill=WHT + (int(255 * k),), anchor="lm")


def pin(img, X, Y, txt, t, t0, col=PINK, side=1):
    if t < t0: return
    k = ease((t - t0) / 0.3); d = ImageDraw.Draw(img); pul = 0.5 + 0.5 * math.sin((t - t0) * 6)
    for r in (46 + 30 * pul, 30):
        d.ellipse((X - r, Y - r, X + r, Y + r), outline=col + (int((90 if r > 31 else 255) * k),), width=4)
    d.ellipse((X - 11, Y - 11, X + 11, Y + 11), fill=col + (int(255 * k),), outline=WHT + (255,), width=3)
    if txt:
        f = font(POPX, 34); w = f.getlength(txt) + 40; lx = X + 60 if side > 0 else X - 60 - w; ly = Y - 80
        d.line((X, Y - 12, lx + (0 if side > 0 else w), ly + 22), fill=WHT + (int(255 * k),), width=3)
        d.rounded_rectangle((lx, ly - 4, lx + w, ly + 48), 12, fill=(10, 8, 24, int(215 * k)), outline=col + (int(255 * k),), width=3)
        d.text((lx + 20, ly + 22), txt, font=f, fill=WHT + (int(255 * k),), anchor="lm")


def route(img, pts, t, t0, dur=1.6, col=CYAN, width=9):
    if t < t0 or len(pts) < 2: return
    k = ease((t - t0) / dur); L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(L) * k; out = [pts[0]]
    for i, l in enumerate(L):
        if tot <= 0: break
        u = min(1.0, tot / l); out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u)); tot -= l
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).line(out, fill=col + (200,), width=width * 3, joint="curve")
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(img); d.line(out, fill=WHT + (255,), width=width, joint="curve"); d.line(out, fill=col + (255,), width=max(3, width - 4), joint="curve")


def credit(img, txt="Imagery © Esri, Maxar, Earthstar Geographics"):
    ImageDraw.Draw(img).text((W - 24, H - 18), txt, font=font(POPB, 18), fill=(255, 255, 255, 170), anchor="rs")


# ------------------------------------------------------------------ shot list
SH = []          # (t0, kind, args, overlays)


def S(t0, kind, *args): SH.append([t0, kind, args, []])


def O(fn, *args, **kw): SH[-1][3].append((fn, args, kw))


def scene_t(i): return SH[i][0], (SH[i + 1][0] if i + 1 < len(SH) else TOTAL)


CHAP = {}        # line -> chapter label for the HUD
REAL = []        # times when a "real twin" is revealed (HUD counter)


def chapter(line, n, title, bg, s0=0.0):
    S(BL[line], "card", n, title, bg, s0); CHAP[line] = f"CH.{n} · {title}"


def vs(t0, clip, s0, key, z, cx, cy, left, right, kind):
    S(t0, "vs", clip, s0, key, z, cx, cy, left, right, kind); REAL.append(t0)


# line 0: hook
S(0.0, "clip", "V0", 0.0, 0.8, 1.0, 1.12, 0.5, 0.5)
O("title_intro")
S(WT(0, "That") - 0.15, "clip", best("V1"), 0.0, 0.85, 1.0, 1.08, 0.5, 0.5)
O("big", "THE DARKEST SIDE OF THE SUNNIEST PLACE", 960, 200, WT(0, "That") - 0.1, 58, WHT, PINK)
O("badge", "text", 960, 285, WT(0, "That") + 0.2)
S(WT(0, "But") - 0.15, "clip", "V2", 0.0, 0.9, 1.0, 1.1, 0.5, 0.5)
O("big", "EVERY STREET HAS A REAL ADDRESS?", 960, 200, WT(0, "address") - 0.4, 62, YEL, BLK)
vs(WT(0, "Today") - 0.15, "V4", 0.0, "MIA", 1.0, 0.56, 0.45, "VICE CITY", "MIAMI", None)
PB = WT(0, "place", 1) - 0.1
for q, (k, off) in enumerate([("OB", 0.0), ("PORT", 0.55), ("BRK", 1.0), ("OPA", 1.4), ("LH", 1.75), ("WYN", 2.05), ("KAS", 2.3)]):
    S(PB + off, "sat", k, 1.15, 1.35, 0.5, 0.5)
    if q == 6: O("big", "PLACE BY PLACE", 960, 200, PB + off + 0.2, 90, WHT, PINK)
# line 1: rules
S(BL[1], "legend")
# line 2: Leonida
S(BL[2], "fl")
# line 3: county
S(BL[3], "sat", "MIA", 1.0, 1.25, 0.62, 0.5)
O("big", "VICE-DALE COUNTY", 640, 200, WT(3, "Vice-Dale") - 0.2, 70, PINK, BLK)
O("badge", "wiki", 640, 280, WT(3, "Vice-Dale") + 0.1)
O("big", "MIAMI-DADE COUNTY", 1280, 420, WT(3, "Miami-Dade") - 0.3, 70, YEL, BLK)
O("badge", "real", 1280, 500, WT(3, "Miami-Dade"))
O("credit")
# ch.1 Ocean Beach
chapter(4, 1, "OCEAN BEACH", "V2", 3.0)
S(BL[5], "clip", "V2", 1.0, 0.75, 1.0, 1.1, 0.5, 0.5)
O("quote", "ROCKSTAR'S DESCRIPTION OF OCEAN BEACH", "PASTEL ART DECO HOTELS AND BRIGHT WHITE SANDS", WT(5, "pastel") - 0.3)
O("badge", "text", 120, 470, WT(5, "pastel") + 0.4, anchor="lm")
vs(WT(5, "real") - 0.35, "V2", 3.0, "OB", 1.0, 0.5, 0.5, "OCEAN BEACH", "SOUTH BEACH · OCEAN DRIVE", "text")
S(WT(5, "Architectural") - 0.4, "sat", "OB", 1.0, 1.45, 0.5, 0.5)
O("counter", 0, 800, "~{:,.0f}", 960, 190, WT(5, "eight") - 0.1, 1.4, 120, WHT, PINK)
O("big", "HISTORIC BUILDINGS", 960, 300, WT(5, "historic") - 0.2, 56, YEL, BLK)
O("big", "NATIONAL REGISTER · 14 MAY 1979", 960, 400, WT(5, "fourteenth") - 0.3, 52, WHT, BLU)
O("credit")
S(WT(5, "Most") - 0.15, "clip", "V2", 4.0, 0.7, 1.05, 1.15, 0.5, 0.5)
O("big", "BUILT 1930s–40s", 960, 170, WT(5, "thirties") - 0.3, 64, YEL, BLK)
O("tags", [("ROUNDED CORNERS", WT(5, "rounded") - 0.1), ("RACING STRIPES", WT(5, "racing") - 0.1), ("PORTHOLE WINDOWS", WT(5, "porthole") - 0.1), ("NEON AT NIGHT", WT(5, "neon") - 0.1)])
S(BL[6], "clip", "V3", 0.0, 0.75, 1.0, 1.1, 0.5, 0.5)
O("big", "1970s: SLATED FOR DEMOLITION", 960, 190, WT(6, "seventies") - 0.3, 62, RED, BLK)
O("big", "LOCALS FOUGHT BACK", 960, 290, WT(6, "fought") - 0.2, 60, YEL, BLK)
S(WT(6, "neon") - 0.2, "clip", "V1", 0.0, 0.8, 1.0, 1.08, 0.5, 0.5)
O("big", "AND THEY WON", 960, 200, WT(6, "won") - 0.3, 84, WHT, PINK)
# ch.2 The port
chapter(7, 2, "THE PORT", "V4", 2.0)
S(BL[8], "clip", "V4", 0.0, 0.75, 1.0, 1.12, 0.5, 0.5)
O("quote", "ROCKSTAR ON VC PORT", "THE CRUISE SHIP CAPITAL OF THE WORLD", WT(8, "capital") - 0.5)
O("badge", "text", 120, 410, WT(8, "capital"), anchor="lm")
vs(WT(8, "PortMiami") - 0.25, "V4", 3.0, "PORT", 1.0, 0.6, 0.55, "VC PORT", "PORTMIAMI", "text")
S(WT(8, "satellite") - 0.35, "sat", "PORT", 1.0, 1.3, 0.62, 0.6)
O("pinll", "PORT", -80.1625, 25.7745, "PORTMIAMI", WT(8, "island") - 0.2)
O("big", "CRUISE CAPITAL OF THE WORLD", 960, 170, WT(8, "satellite") - 0.1, 56, YEL, BLK)
O("credit")
S(BL[9], "sat", "MAC", 1.0, 1.2, 0.5, 0.62)
O("routell", "MAC", [(-80.1875, 25.7852), (-80.1760, 25.7855), (-80.1650, 25.7812), (-80.1520, 25.7776), (-80.1400, 25.7746)], WT(9, "MacArthur") - 0.2, 2.2)
O("big", "MACARTHUR CAUSEWAY", 960, 170, WT(9, "MacArthur") - 0.2, 70, WHT, PINK)
O("counter", 0, 3.5, "~{:.1f} MILES", 760, 290, WT(9, "three") - 0.1, 1.2, 60, YEL, BLK)
O("big", "OPENED 1920", 1220, 290, WT(9, "twenty") - 0.4, 60, WHT, BLU)
O("credit")
S(WT(9, "road", 1) - 0.2, "clip", best("V5"), 0.0, 0.85, 1.0, 1.08, 0.5, 0.5)
O("big", "TOWERS ON ONE END, BEACH ON THE OTHER", 960, 190, WT(9, "towers") - 0.2, 52, YEL, BLK)
# ch.3 Tequesta
chapter(10, 3, "TEQUESTA", "V6", 1.0)
S(BL[11], "sign", "TEQUESTA", "route", "V6")
O("badge", "sign", 960, 760, WT(11, "official") - 0.1)
vs(WT(11, "Fans") - 0.2, "V6", 2.0, "BRK", 1.0, 0.5, 0.5, "TEQUESTA", "BRICKELL", "sign")
S(WT(11, "Tequesta", 1) - 0.35, "sat", "BRK", 1.0, 1.35, 0.62, 0.38)
O("pinll", "BRK", -80.1893, 25.7698, "MOUTH OF THE MIAMI RIVER", WT(11, "mouth") - 0.3)
O("big", "THE TEQUESTA PEOPLE", 960, 170, WT(11, "Tequesta", 1) - 0.1, 66, WHT, PINK)
O("credit")
S(BL[12], "clip", "V7", 0.0, 0.7, 1.0, 1.1, 0.5, 0.5)
O("big", "1998 · BRICKELL", 960, 180, ST[12] + 0.1, 70, YEL, BLK)
O("big", "ARCHAEOLOGIST ROBERT CARR'S TEAM", 960, 280, WT(12, "Robert") - 0.3, 46, WHT, BLK)
S(WT(12, "perfect") - 0.25, "sat", "CIRC", 1.0, 1.5, 0.563, 0.648)
O("pinf", 0.563, 0.648, "THE MIAMI CIRCLE TODAY", WT(12, "perfect"))
O("credit")
S(WT(12, "thirty") - 0.2, "circ")
S(WT(12, "So") - 0.2, "clip", "V7", 4.0, 0.6, 1.05, 1.15, 0.5, 0.5)
O("big", "TEQUESTA → TEQUESTA", 960, 200, WT(12, "named") - 0.3, 76, YEL, PINK)
S(BL[13], "clip", "V6", 3.0, 0.7, 1.0, 1.1, 0.5, 0.5)
O("big", "TODAY: A FINANCIAL DISTRICT", 960, 180, ST[13] + 0.3, 62, WHT, PINK)
O("counter", 0, 40000, "~{:,.0f} RESIDENTS", 960, 290, WT(13, "forty") - 0.2, 1.3, 64, YEL, BLK)
# ch.4 Peacock Bay
chapter(14, 4, "PEACOCK BAY", "V8", 1.0)
S(BL[15], "sign", "PEACOCK BAY", "exit", "V8")
O("badge", "sign", 960, 760, WT(15, "exit"))
O("big", "TRAILER 2 · 0:35", 960, 840, WT(15, "thirty") - 0.2, 46, YEL, BLK)
vs(WT(15, "Miami") - 0.2, "V8", 1.0, "PCK", 1.0, 0.5, 0.5, "PEACOCK BAY", "PEACOCK PARK · COCONUT GROVE", "sign")
S(WT(15, "family") - 0.5, "clip", "V9", 0.0, 0.65, 1.0, 1.12, 0.5, 0.5)
O("timeline", WT(15, "eighteen") - 0.3, WT(15, "nineteen") - 0.3)
O("big", "FIRST HOTEL ON BISCAYNE BAY", 960, 180, WT(15, "first") - 0.2, 60, YEL, BLK)
S(WT(15, "Rockstar") - 0.2, "sat", "PCK", 1.0, 1.3, 0.5, 0.5)
O("pinf", 0.5, 0.5, "PEACOCK PARK", WT(15, "Rockstar"))
O("big", "THE NAME STAYED", 960, 170, WT(15, "Rockstar") - 0.1, 70, WHT, PINK)
O("credit")
# ch.5 Tisha-Wocka
chapter(16, 5, "TISHA-WOCKA", "V11", 1.0)
S(BL[17], "clip", "V11", 0.0, 0.7, 1.0, 1.1, 0.5, 0.5)
O("quote", "ROCKSTAR'S COPY", "THE TISHA-WOCKA FLEA MARKET AND ITS BOOTLEG BRANDS", WT(17, "mentions") - 0.2)
O("badge", "text", 120, 470, WT(17, "bootleg"), anchor="lm")
S(WT(17, "Say") - 0.2, "clip", "V10", 0.0, 0.5, 1.0, 1.05, 0.5, 0.5)
O("sound")
vs(WT(17, "small") - 0.6, "V10", 2.0, "OPA", 1.0, 0.47, 0.5, "TISHA-WOCKA", "OPA-LOCKA", "text")
S(WT(17, "founded") - 0.3, "clip", "V10", 3.0, 0.65, 1.0, 1.12, 0.5, 0.5)
O("big", "FOUNDED 1926 · GLENN CURTISS", 960, 180, WT(17, "founded") - 0.1, 58, YEL, BLK)
O("tags", [("DOMES", WT(17, "domes") - 0.1), ("MINARETS", WT(17, "minarets") - 0.1), ("ARCHES", WT(17, "arches") - 0.1)], y0=320)
S(WT(17, "City") - 0.25, "sat", "OPA", 1.0, 1.3, 0.5, 0.5)
O("pinf", 0.47, 0.5, "OPA-LOCKA", WT(17, "City"))
O("big", "A CITY HALL LIKE A PALACE", 960, 170, WT(17, "City") - 0.1, 62, WHT, PINK)
O("big", "~20 BUILDINGS ON THE NATIONAL REGISTER", 960, 270, WT(17, "twenty") - 0.2, 46, YEL, BLK)
O("credit")
S(WT(17, "flea", 1) - 0.4, "clip", "V11", 4.0, 0.7, 1.05, 1.12, 0.5, 0.5)
O("big", "A REAL, FAMOUS FLEA MARKET", 960, 190, WT(17, "flea", 1) - 0.2, 62, YEL, BLK)
# ch.6 Little Cuba
chapter(18, 6, "LITTLE CUBA", "V12", 1.0)
S(BL[19], "clip", "V13", 0.0, 0.7, 1.0, 1.1, 0.5, 0.5)
O("quote", "THE OFFICIAL DESCRIPTION", "THE BUSTLING PANADERÍAS OF LITTLE CUBA", WT(19, "talks") - 0.2)
O("badge", "text", 120, 410, WT(19, "panaderias") + 0.3, anchor="lm")
O("big", "PANADERÍA = BAKERY", 960, 820, WT(19, "bakeries") - 0.3, 60, YEL, BLK)
vs(WT(19, "Miami") - 0.2, "V12", 0.0, "LH", 1.0, 0.5, 0.5, "LITTLE CUBA", "LITTLE HAVANA", "text")
S(WT(19, "After") - 0.2, "sat", "LH", 1.0, 1.3, 0.5, 0.5)
O("routell", "LH", [(-80.2250, 25.76545), (-80.2135, 25.76540)], WT(19, "Calle") - 0.3, 1.2, YEL)
O("big", "AFTER 1959: CUBAN EXILES", 960, 170, WT(19, "After"), 62, WHT, PINK)
O("big", "CALLE OCHO · 8TH STREET", 960, 270, WT(19, "Calle") - 0.2, 54, YEL, BLK)
O("credit")
S(WT(19, "Since") - 0.2, "clip", "V12", 2.0, 0.65, 1.0, 1.12, 0.5, 0.5)
O("big", "DOMINO PARK", 960, 170, WT(19, "Domino") - 0.4, 76, WHT, PINK)
O("big", "SINCE THE EARLY 1970s", 960, 270, WT(19, "seventies") - 0.2, 50, YEL, BLK)
S(WT(19, "If") - 0.2, "clip", "V13", 3.0, 0.65, 1.05, 1.15, 0.5, 0.5)
# ch.7 Stockyard
chapter(20, 7, "STOCKYARD", "V14", 1.0)
S(BL[21], "sign", "STOCKYARD", "street", "V14")
O("badge", "sign", 960, 760, WT(21, "sign"))
O("big", "TRAILER 1", 960, 840, WT(21, "trailer") - 0.2, 46, YEL, BLK)
vs(WT(21, "Fans") - 0.2, "V14", 0.0, "WYN", 1.0, 0.5, 0.5, "STOCKYARD", "WYNWOOD", "fan")
S(WT(21, "two") - 0.25, "clip", "V14", 2.0, 0.7, 1.0, 1.12, 0.5, 0.5)
O("big", "WYNWOOD WALLS · 2009", 960, 180, WT(21, "two") - 0.1, 66, YEL, BLK)
S(WT(21, "Now") - 0.2, "clip", "V14", 5.0, 0.6, 1.1, 1.2, 0.4, 0.5)
O("big", "AN OPEN-AIR GALLERY", 960, 190, WT(21, "open-air") - 0.3, 62, WHT, PINK)
S(WT(21, "remember") - 0.3, "sat", "WYN", 1.0, 1.25, 0.5, 0.5)
O("pinf", 0.5, 0.5, "WYNWOOD WALLS", WT(21, "remember"))
O("badge", "fan", 960, 180, WT(21, "fan") - 0.2, 40)
O("credit")
# ch.8 Landmarks
chapter(22, 8, "THE LANDMARKS", "V15", 1.0)
S(BL[23], "clip", "V15", 0.0, 0.7, 1.0, 1.1, 0.5, 0.5)
vs(WT(23, "Kaseya") - 0.35, "V15", 2.0, "KAS", 1.0, 0.52, 0.5, "THE ARENA", "KASEYA CENTER", "fan")
O("big", "OPENED 1999 · 19,600 SEATS", 960, 850, WT(23, "opened") - 0.2, 46, YEL, BLK)
S(WT(23, "little") - 0.2, "clip", "V16", 0.0, 0.75, 1.0, 1.1, 0.5, 0.5)
vs(WT(23, "Metromover") - 0.25, "V16", 2.0, "MET", 1.0, 0.5, 0.5, "THE LITTLE TRAIN", "METROMOVER", "fan")
O("big", "OPENED 1986 · FREE SINCE 2002", 960, 850, WT(23, "eighty") - 0.4, 46, YEL, BLK)
S(WT(23, "road") - 0.25, "clip", "V17", 0.0, 0.8, 1.0, 1.1, 0.5, 0.5)
vs(WT(23, "Venetian") - 0.3, "V17", 2.5, "VEN", 1.0, 0.5, 0.5, "ISLAND-HOPPING ROAD", "VENETIAN CAUSEWAY", "fan")
O("big", "12 BRIDGES · 2 DRAWBRIDGES", 960, 850, WT(23, "twelve") - 0.2, 50, YEL, BLK)
# ch.9 Beyond the city
chapter(24, 9, "BEYOND THE CITY", "V18", 1.0)
S(BL[25], "clip", best("V18"), 0.0, 0.8, 1.0, 1.08, 0.5, 0.5)
O("big", "LEONIDA KEYS", 960, 180, WT(25, "Keys") - 0.4, 80, WHT, PINK)
O("badge", "region", 960, 270, WT(25, "Keys"))
S(WT(25, "real") - 0.25, "sat", "KEYS", 1.0, 1.25, 0.5, 0.6)
REAL.append(WT(25, "real") - 0.25)
O("routef", [(0.0, 0.84), (0.47, 0.66), (0.93, 0.48)], WT(25, "Seven") - 0.3, 1.4)
O("big", "THE REAL FLORIDA KEYS", 960, 170, WT(25, "real"), 66, WHT, PINK)
O("counter", 0, 113, "~{:.0f} MILES", 700, 280, WT(25, "hundred") - 0.4, 1.2, 60, YEL, BLK)
O("counter", 0, 42, "{:.0f} BRIDGES", 1220, 280, WT(25, "forty") - 0.2, 1.0, 60, YEL, BLK)
O("big", "SEVEN MILE BRIDGE", 960, 860, WT(25, "Seven") - 0.2, 56, WHT, BLU)
O("credit")
S(WT(25, "Its") - 0.25, "clip", "V18", 2.0, 0.6, 1.0, 1.15, 0.5, 0.5)
O("big", "FLAGLER'S RAILROAD · 1912", 960, 180, WT(25, "Flagler's") - 0.3, 62, YEL, BLK)
O("big", "1935 HURRICANE: TRAINS END", 960, 280, WT(25, "hurricane") - 0.3, 56, RED, BLK)
S(BL[26], "clip", best("V19"), 0.0, 0.8, 1.0, 1.08, 0.5, 0.5)
O("big", "GRASSRIVERS", 960, 180, WT(26, "Grassrivers") - 0.4, 84, WHT, PINK)
O("badge", "region", 960, 270, WT(26, "Grassrivers"))
S(WT(26, "real") - 0.25, "sat", "EVG", 1.0, 1.2, 0.45, 0.45)
REAL.append(WT(26, "real") - 0.25)
O("big", "EVERGLADES NATIONAL PARK", 960, 170, WT(26, "Everglades") - 0.3, 64, WHT, PINK)
O("big", "SINCE 1947", 700, 270, WT(26, "forty") - 0.5, 56, YEL, BLK)
O("big", "~1.5 MILLION ACRES", 1240, 270, WT(26, "million") - 0.4, 56, YEL, BLK)
O("credit")
S(WT(26, "only") - 0.25, "clip", "V19", 0.0, 0.6, 1.0, 1.12, 0.5, 0.5)
O("big", "ALLIGATORS + CROCODILES", 960, 180, WT(26, "alligators") - 0.3, 66, YEL, BLK)
O("big", "ONLY PLACE ON EARTH THEY LIVE SIDE BY SIDE", 960, 270, WT(26, "side") - 0.6, 44, WHT, PINK)
O("big", "TRAILER 1: AN ALLIGATOR WALKS INTO A STORE", 960, 840, WT(26, "store") - 0.6, 44, WHT, BLK)
# the count
S(BL[27], "score")
CHAP[27] = "THE COUNT"
# finale
S(BL[28], "clip", "V20", 0.0, 0.55, 1.0, 1.12, 0.5, 0.5)
O("big", "MIAMI · 28 JULY 1896", 960, 180, WT(28, "July") - 0.3, 70, YEL, BLK)
O("big", "JULIA TUTTLE", 960, 290, WT(28, "Julia") - 0.3, 66, WHT, PINK)
O("badge", "real", 960, 370, WT(28, "Julia"))
S(WT(28, "She") - 0.2, "flagler")
S(WT(28, "Without") - 0.2, "clip", "V20", 5.0, 0.6, 1.05, 1.15, 0.5, 0.5)
O("big", "NO RAILROAD, NO MIAMI", 960, 200, WT(28, "Without"), 76, WHT, PINK)
S(BL[29], "clip", "V21", 0.0, 0.75, 1.0, 1.12, 0.5, 0.5)
O("big", "GTA 6 · 19 NOVEMBER 2026", 960, 190, ST[29] + 0.1, 66, YEL, BLK)
O("big", "WHICH PLACE WOULD YOU VISIT FIRST?", 960, 300, WT(29, "Which") - 0.2, 56, WHT, PINK)
O("big", "TELL ME IN THE COMMENTS ↓", 960, 820, WT(29, "Tell") - 0.2, 52, YEL, BLK)
CHAP.update({0: "INTRO", 28: "FINALE"})
CUTS = [s[0] for s in SH[1:]]
SHAKES = [REAL[i] + 0.25 for i in range(len(REAL))] + [s[0] + 0.5 for s in SH if s[1] == "card"]


def shot_at(t):
    for k in range(len(SH) - 1, -1, -1):
        if t >= SH[k][0]: return k
    return 0


def chap_at(line):
    for i in range(line, -1, -1):
        if i in CHAP: return CHAP[i]
    return "INTRO"


def line_at(t):
    for i in range(N - 1, -1, -1):
        if t >= BL[i]: return i
    return 0


# ------------------------------------------------------------------ scenes
def clip_img(name, s0, rate, z0, z1, cx, cy, t, t0, t1, w=W, h=H):
    u = (t - t0) / max(0.1, t1 - t0); z = z0 + (z1 - z0) * ease(u)
    im, _ = view(clip_frame(name, s0 + (t - t0) * rate), z, cx, cy, w, h); return im


def sat_img(key, z0, z1, cx, cy, t, t0, t1, w=W, h=H):
    u = (t - t0) / max(0.1, t1 - t0); z = z0 + (z1 - z0) * ease(u)
    return view(sat(key), z, cx, cy, w, h)


def to_screen(m, fx, fy, key, ox=0):
    x0, y0, s = m; iw, ih = sat(key).size; return ox + (fx * iw - x0) * s, (fy * ih - y0) * s


@lru_cache(maxsize=4)
def blurred(name, sec):
    im, _ = view(clip_frame(name, sec), 1.05, 0.5, 0.5)
    return Image.eval(im.filter(ImageFilter.GaussianBlur(14)), lambda v: int(v * 0.45)).convert("RGBA")


def bg_blur(name, t):                       # blurred background, updated 6x per second to save time
    return blurred(name, round(t * 6) / 6 * 0.5).copy()


def card(t, k):
    t0, t1 = scene_t(k); n, title, bg, s0 = SH[k][2]; img = bg_blur(bg, s0 + t - t0)
    d = ImageDraw.Draw(img); u = ease((t - t0) / 0.4)
    d.rectangle((0, 470, W * u, 476), fill=PINK + (255,)); d.rectangle((W * (1 - u), 700, W, 706), fill=CYAN + (255,))
    label(img, f"CHAPTER {n}", 960, 420, t, t0 + 0.05, 46, PINK)
    grad_title(img, title, 960, 590, 150, t, t0 + 0.15)
    label(img, "IN THE GAME", 960, 760, t, t0 + 0.5, 32, WHT)
    return img


def vs_scene(t, k):
    t0, t1 = scene_t(k); clip, s0, key, z, cx, cy, left, right, kind = SH[k][2]
    img = Image.new("RGBA", (W, H), (8, 6, 20, 255)); sl = ease((t - t0) / 0.35)
    L = clip_img(clip, s0, 0.7, 1.0, 1.1, 0.5, 0.5, t, t0, t1, 950, H).convert("RGBA")
    R, m = sat_img(key, z, z * 1.25, cx, cy, t, t0, t1, 950, H)
    img.paste(L, (int(-950 * (1 - sl)), 0)); img.paste(R.convert("RGBA"), (970 + int(950 * (1 - sl)), 0))
    d = ImageDraw.Draw(img); d.rectangle((950, 0, 970, H), fill=PINK + (255,))
    for (txt, sub, x) in ((left, "IN THE GAME", 475), (right, "REAL MIAMI" if key not in ("KEYS", "EVG") else "REAL FLORIDA", 1445)):
        pill(img, sub, x, 160, 24, (20, 20, 40), a=sl)
        label(img, txt, x, 240, t, t0 + 0.25, 60, WHT if x < 960 else YEL, PINK if x < 960 else BLK, maxw=860)
    pill(img, "AI CONCEPT · NOT GAME FOOTAGE", 475, 930, 18, (40, 40, 50), a=sl)
    ImageDraw.Draw(img).text((1910, 1062), "Imagery © Esri, Maxar, Earthstar Geographics", font=font(POPB, 16), fill=(255, 255, 255, 170), anchor="rs")
    sv = ease((t - t0 - 0.3) / 0.2); r = 74 * (1.6 - 0.6 * sv)
    if t > t0 + 0.3:
        d.ellipse((960 - r, 540 - r, 960 + r, 540 + r), fill=(15, 10, 30, 255), outline=WHT + (255,), width=5)
        glow_text(img, (960, 540), "VS", font(TITAN, int(r * 0.95)), YEL, 1.0, "mm", PINK)
    if kind: badge(img, kind, 1445, 325, t, t0 + 0.5, 24)
    return img


def legend(t, k):
    t0, t1 = scene_t(k); img = bg_blur("V21", t - t0)
    label(img, "THE RULES", 960, 200, t, t0 + 0.05, 110, WHT, PINK)
    label(img, "ROCKSTAR NEVER PUBLISHED A LIST OF REAL PLACES", 960, 330, t, WT(1, "never") - 0.1, 44, YEL)
    rows = [("text", "NAMED IN ROCKSTAR'S OWN TEXT", WT(1, "named") - 0.1), ("sign", "SPOTTED ON AN OFFICIAL SIGN", WT(1, "official") - 0.1),
            ("region", "AN OFFICIAL REGION NAME", WT(1, "material") - 0.1), ("fan", "SPOTTED BY FANS, MATCHED TO A MAP", WT(1, "fans") - 0.1)]
    for q, (kind, txt, ts) in enumerate(rows):
        y = 470 + q * 110; badge(img, kind, 340, y, t, ts, 30, "lm")
        label(img, txt, 1020, y, t, ts + 0.15, 40, WHT, anchor="lm", maxw=820)
    return img


REG = [("VICE CITY", "Vice"), ("LEONIDA KEYS", "Keys"), ("GRASSRIVERS", "Grassrivers"), ("PORT GELLHORN", "Gellhorn"), ("AMBROSIA", "Ambrosia"), ("MOUNT KALAGA N.P.", "Kalaga")]


def fl_scene(t, k):
    t0, t1 = scene_t(k); tput = WT(2, "Put") - 0.2; zz = ease((t - tput) / 3.0) if t > tput else 0.0
    tcity = WT(2, "city", 1) - 0.3; zc = ease((t - tcity) / 2.2) if t > tcity else 0.0
    z = 1.0 + 1.2 * zz + 2.2 * zc; cx = 0.55 + 0.17 * zz + 0.05 * zc; cy = 0.55 + 0.15 * zz + 0.02 * zc
    im, m = view(sat("FL"), z, cx, cy); img = im.convert("RGBA")
    def P(lon, lat): fx, fy = geo("FL", lon, lat); return to_screen(m, fx, fy, "FL")
    if t < tput + 1.0:                                              # side panel with the 6 official regions
        a = 1.0 if t < tput else max(0.0, 1 - (t - tput))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rounded_rectangle((80, 120, 760, 900), 26, fill=(10, 8, 24, int(215 * a)))
        img.alpha_composite(lay)
        if a > 0.05:
            label(img, "LEONIDA", 420, 210, t, WT(2, "Leonida") - 0.2, 96, WHT, PINK, maxw=600)
            label(img, "6 OFFICIAL REGIONS", 420, 310, t, WT(2, "six") - 0.2, 40, YEL, maxw=600)
            for q, (nm, w) in enumerate(REG):
                label(img, nm, 140, 400 + q * 82, t, WT(2, w) - 0.15, 44, WHT, anchor="lm", maxw=580)
    tk = WT(2, "islands") - 0.2
    if t > tk:
        route(img, [P(-80.35, 25.25), P(-80.55, 25.0), P(-80.85, 24.8), P(-81.2, 24.68), P(-81.6, 24.58), P(-81.8, 24.55)], t, tk, 1.2, CYAN, 8)
        label(img, "FLORIDA KEYS", P(-81.2, 24.4)[0], P(-81.2, 24.4)[1], t, tk + 0.3, 40, CYAN)
    te = WT(2, "swamp") - 0.2
    if t > te:
        X, Y = P(-80.85, 25.75); r = (P(-80.4, 25.75)[0] - X) * ease((t - te) / 0.5)
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((X - r, Y - r * 1.2, X + r, Y + r * 1.2), fill=GRN + (90,), outline=GRN + (255,), width=5); img.alpha_composite(g)
        label(img, "EVERGLADES", X, Y, t, te + 0.3, 40, WHT, GRN)
    if t > tcity:
        X, Y = P(-80.19, 25.77); pin(img, X, Y, "MIAMI", t, tcity + 0.4)
    label(img, "FLORIDA", 1500, 160, t, tput, 70, WHT, BLU)
    credit(img); return img


def circ_scene(t, k):
    t0, t1 = scene_t(k); im, _ = view(sat("CIRC"), 1.8, 0.563, 0.648)
    img = Image.eval(im.filter(ImageFilter.GaussianBlur(3)), lambda v: int(v * 0.4)).convert("RGBA"); d = ImageDraw.Draw(img)
    cx, cy, R = 1260, 450, 270; u = ease((t - t0) / 1.0)
    d.arc((cx - R, cy - R, cx + R, cy + R), -90, -90 + 360 * u, fill=YEL + (255,), width=8)
    th = WT(12, "twenty") - 0.2; nh = int(min(24, max(0, (t - th) / 0.07))) if t > th else 0
    for q in range(nh):
        a = -math.pi / 2 + q * 2 * math.pi / 24; x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=(30, 20, 10, 255), outline=ORG + (255,), width=4)
    if t > t0 + 0.6:
        d.line((cx - R, cy + R + 60, cx + R, cy + R + 60), fill=WHT + (255,), width=4)
        for x in (cx - R, cx + R): d.line((x, cy + R + 44, x, cy + R + 76), fill=WHT + (255,), width=4)
        label(img, "38 FT  (~11.5 M)", cx, cy + R + 110, t, t0 + 0.6, 44, WHT)
    counter(img, 0, 24, "{:.0f} HOLES", 430, 380, t, th, 24 * 0.07, 76, ORG, BLK)
    label(img, "THE MIAMI CIRCLE", 430, 240, t, WT(12, "called") - 0.3, 64, WHT, PINK, maxw=760)
    label(img, "UP TO ~2,000 YEARS OLD", 430, 520, t, WT(12, "two") - 0.3, 48, YEL, maxw=760)
    label(img, "AGE STILL DEBATED", 430, 590, t, WT(12, "two") + 0.3, 32, WHT, maxw=760)
    label(img, "NATIONAL HISTORIC LANDMARK", 430, 700, t, WT(12, "Landmark") - 0.5, 42, WHT, BLU, maxw=760)
    pill(img, "SCHEMATIC · NOT TO SCALE WITH THE PHOTO", 1260, 920, 20, (40, 40, 50))
    return img


def sign_scene(t, k):
    t0, t1 = scene_t(k); text, style, bg = SH[k][2]; img = bg_blur(bg, t - t0)
    sc = ease((t - t0) / 0.35); w, h = 1100 * (0.8 + 0.2 * sc), 340 * (0.8 + 0.2 * sc); x0, y0 = 960 - w / 2, 420 - h / 2
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line((960 - 300, y0 + h, 960 - 300, H), fill=(120, 120, 130, 255), width=26); d.line((960 + 300, y0 + h, 960 + 300, H), fill=(120, 120, 130, 255), width=26)
    col = (0, 112, 60) if style != "street" else (20, 90, 160)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 30, fill=col + (255,), outline=WHT + (255,), width=10)
    if style == "exit":
        d.rounded_rectangle((x0 + w - 230, y0 - 70, x0 + w - 20, y0 + 6), 12, fill=col + (255,), outline=WHT + (255,), width=6)
        d.text((x0 + w - 125, y0 - 32), "EXIT", font=font(POPX, 40), fill=WHT, anchor="mm")
    if style == "route":
        d.ellipse((x0 + 40, y0 + h / 2 - 80, x0 + 200, y0 + h / 2 + 80), fill=WHT, outline=BLK, width=6)
        d.text((x0 + 120, y0 + h / 2), "3", font=font(POPX, 90), fill=BLK, anchor="mm")
    d.text((960 + (70 if style == "route" else 0), y0 + h / 2), text, font=fit(POPX, 120, text, w - 260), fill=WHT, anchor="mm")
    lay = lay.rotate(0, center=(960, 420)); img.alpha_composite(lay)
    pill(img, "SIGN RECREATED FOR THIS VIDEO", 960, 960, 20, (40, 40, 50))
    return img


SCORE = [("OCEAN BEACH", "SOUTH BEACH", "text", ("Ocean", 0)), ("VC PORT", "PORTMIAMI", "text", ("VC", 0)), ("TISHA-WOCKA", "OPA-LOCKA", "text", ("Tisha-Wocka", 0)),
         ("LITTLE CUBA", "LITTLE HAVANA", "text", ("Cuba", 0)), ("TEQUESTA", "BRICKELL", "sign", ("Tequesta", 0)), ("PEACOCK BAY", "COCONUT GROVE", "sign", ("Peacock", 0)),
         ("LEONIDA KEYS", "FLORIDA KEYS", "region", ("Keys", 0)), ("GRASSRIVERS", "EVERGLADES", "region", ("Grassrivers", 0)),
         ("STOCKYARD", "WYNWOOD", "fan", ("Stockyard", 0)), ("THE LANDMARKS", "KASEYA · METROMOVER · VENETIAN", "fan", ("landmarks", 0))]


def score_scene(t, k):
    t0, t1 = scene_t(k); img = bg_blur("V21", t - t0)
    label(img, "HOW REAL IS VICE CITY?", 960, 90, t, t0 + 0.05, 64, WHT, PINK)
    d = ImageDraw.Draw(img)
    for q, (g, r, kind, (w, nth)) in enumerate(SCORE):
        ts = WT(27, w, nth) - 0.15; y = 190 + q * 80
        if t < ts: continue
        a = ease((t - ts) / 0.25); x = (1 - a) * -200
        d.rounded_rectangle((90 + x, y - 34, 1830 + x, y + 34), 14, fill=(12, 10, 28, int(210 * a)))
        d.text((130 + x, y), g, font=font(POPX, 36), fill=WHT + (int(255 * a),), anchor="lm")
        d.text((560 + x, y), "→", font=font(POPX, 36), fill=PINK + (int(255 * a),), anchor="mm")
        d.text((620 + x, y), r, font=fit(POPX, 36, r, 640), fill=YEL + (int(255 * a),), anchor="lm")
        txt, c = BADGE[kind]; f = font(POPX, 22); pw = f.getlength(txt) + 30
        d.rounded_rectangle((1810 - pw + x, y - 22, 1810 + x, y + 22), 12, fill=c + (int(230 * a),)); d.text((1810 - pw / 2 + x, y), txt, font=f, fill=WHT + (int(255 * a),), anchor="mm")
    tt = WT(27, "satellite") - 0.2
    if t > tt: label(img, "8 OFFICIAL  ·  2 FAN MATCHES", 960, 1000, t, tt, 44, YEL, BLK)
    return img


def flagler_scene(t, k):
    t0, t1 = scene_t(k); u = ease((t - t0) / max(1.0, t1 - t0))
    im, m = view(sat("FL"), 1.3 + 0.3 * u, 0.68, 0.42 + 0.1 * u); img = im.convert("RGBA")
    def P(lon, lat): fx, fy = geo("FL", lon, lat); return to_screen(m, fx, fy, "FL")
    pts = [P(-81.66, 30.33), P(-81.31, 29.89), P(-81.02, 29.21), P(-80.60, 28.08), P(-80.39, 27.64), P(-80.05, 26.71), P(-80.14, 26.12), P(-80.19, 25.77)]
    route(img, pts, t, t0 + 0.3, 3.0, YEL, 8)
    pin(img, *P(-80.19, 25.77), "MIAMI · APRIL 1896", t, t0 + 3.2, side=-1)
    label(img, "HENRY FLAGLER'S RAILROAD", 760, 170, t, WT(28, "Flagler") - 0.4, 60, WHT, PINK, maxw=1200)
    label(img, "EAST COAST OF FLORIDA", 760, 260, t, WT(28, "Flagler") + 0.2, 40, YEL, maxw=1200)
    credit(img); return img


def base(k, t):
    t0, t1 = scene_t(k); kind, a = SH[k][1], SH[k][2]
    if kind == "clip": return clip_img(a[0], a[1], a[2], a[3], a[4], a[5], a[6], t, t0, t1).convert("RGBA")
    if kind == "sat": im, _ = sat_img(a[0], a[1], a[2], a[3], a[4], t, t0, t1); return im.convert("RGBA")
    return {"card": card, "vs": vs_scene, "legend": legend, "fl": fl_scene, "circ": circ_scene, "sign": sign_scene, "score": score_scene, "flagler": flagler_scene}[kind](t, k)


def sat_map(k, t):
    t0, t1 = scene_t(k); a = SH[k][2]; _, m = sat_img(a[0], a[1], a[2], a[3], a[4], t, t0, t1); return a[0], m


def overlays(img, t, k):
    t0, t1 = scene_t(k)
    for fn, args, kw in SH[k][3]:
        if fn == "big": txt, x, y, ts, size, col, glow = args; label(img, txt, x, y, t, ts, size, col, glow)
        elif fn == "badge": badge(img, args[0], args[1], args[2], t, args[3], *args[4:], **kw)
        elif fn == "counter": counter(img, *args[:5], t, *args[5:])
        elif fn == "quote": quote(img, args[0], args[1], t, args[2])
        elif fn == "tags": tags(img, args[0], t, **kw)
        elif fn == "credit": credit(img)
        elif fn == "title_intro":
            if t < LEAD + 0.6:
                a = 1.0 if t < LEAD else max(0.0, 1 - (t - LEAD) / 0.6)
                if a > 0.02:
                    grad_title(img, "VICE CITY", 960, 380, 190, t, 0.25); label(img, "VS", 960, 545, t, 0.7, 90, YEL, PINK)
                    grad_title(img, "REAL MIAMI", 960, 700, 170, t, 1.0)
        elif fn == "pinll":
            key, lon, lat, txt, ts = args; key2, m = sat_map(k, t); fx, fy = geo(key, lon, lat); pin(img, *to_screen(m, fx, fy, key), txt, t, ts)
        elif fn == "pinf":
            fx, fy, txt, ts = args; key, m = sat_map(k, t); pin(img, *to_screen(m, fx, fy, key), txt, t, ts)
        elif fn == "routell":
            key, pts, ts, dur = args[:4]; col = args[4] if len(args) > 4 else CYAN; _, m = sat_map(k, t)
            route(img, [to_screen(m, *geo(key, lo, la), key) for lo, la in pts], t, ts, dur, col)
        elif fn == "routef":
            pts, ts, dur = args; key, m = sat_map(k, t); route(img, [to_screen(m, fx, fy, key) for fx, fy in pts], t, ts, dur, YEL)
        elif fn == "timeline":
            ta, tb = args; d = ImageDraw.Draw(img); y = 840
            if t > ta:
                u = ease((t - ta) / max(0.5, tb - ta)); d.rounded_rectangle((360, y - 10, 360 + 1200 * u, y + 10), 10, fill=YEL + (255,))
                label(img, "1882 · BAY VIEW HOUSE", 360, y - 60, t, ta, 40, WHT, anchor="lm")
            if t > tb: label(img, "1926 · TORN DOWN", 1560, y - 60, t, tb, 40, RED, anchor="rm"); d.ellipse((1545, y - 18, 1581, y + 18), fill=RED + (255,))
        elif fn == "sound":
            label(img, "TISHA-WOCKA", 600, 420, t, WT(17, "Say") - 0.1, 100, WHT, PINK, maxw=900)
            label(img, "≈", 960, 560, t, WT(17, "hear") - 0.3, 120, YEL)
            label(img, "OPA-LOCKA", 1320, 700, t, WT(17, "Opa-locka") - 0.2, 100, YEL, BLK, maxw=900)


def caption(img, t):
    for i in range(N):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.15:
            words = LINES[i].split(); cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05: cur = j
            c0 = cur // 5 * 5; txt = " ".join(words[c0:c0 + 5]); f = fit(POPX, 46, txt, 1150)
            glow_text(img, (960, 1005), txt, f, WHT, 1.0, "mm", None, 3); return


# ------------------------------------------------------------------ HUD (own design, GTA-like)
def minimap_src(line):
    c = {0: (-80.19, 25.78), 3: (-80.19, 25.78), 4: (-80.131, 25.780), 7: (-80.165, 25.777), 10: (-80.192, 25.764), 14: (-80.2405, 25.7275),
         16: (-80.2506, 25.9017), 18: (-80.2193, 25.7656), 20: (-80.1993, 25.8011), 22: (-80.1881, 25.7814), 27: (-80.19, 25.78)}
    for i in range(line, -1, -1):
        if i in c: return c[i]
    return (-80.19, 25.78)


@lru_cache(maxsize=16)
def minimap(lon, lat, r=96):
    fx, fy = geo("MIA", lon, lat); im = sat("MIA"); iw, ih = im.size; R = 60
    crop = im.crop((int(fx * iw - R), int(fy * ih - R), int(fx * iw + R), int(fy * ih + R))).resize((2 * r, 2 * r), Image.BILINEAR)
    crop = Image.eval(crop, lambda v: int(v * 0.85)).convert("RGBA"); m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    crop.putalpha(m); return crop


def hud(img, t, line):
    if line >= 24 and line <= 26: lon, lat = (-81.165, 24.705) if line < 26 else (-80.75, 25.45); src = None
    else: lon, lat = minimap_src(line); src = minimap(lon, lat)
    r = 96; cx, cy = 140, 930
    if src is not None: img.alpha_composite(src, (cx - r, cy - r))
    else: ImageDraw.Draw(img).ellipse((cx - r, cy - r, cx + r, cy + r), fill=(10, 30, 50, 230))
    d = ImageDraw.Draw(img); d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(20, 20, 30, 255), width=8); d.ellipse((cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4), outline=CYAN + (200,), width=2)
    ang = (t * 1.4) % (2 * math.pi)
    for q in range(10): a_ = ang - q * 0.07; d.line((cx, cy, cx + (r - 8) * math.cos(a_), cy + (r - 8) * math.sin(a_)), fill=GRN + (int(110 * (1 - q / 10)),), width=3)
    d.polygon([(cx, cy - 14), (cx - 10, cy + 10), (cx, cy + 4), (cx + 10, cy + 10)], fill=WHT + (255,), outline=BLK + (255,))
    d.text((cx, cy - r + 16), "N", font=font(POPX, 18), fill=WHT, anchor="mm")
    d.rounded_rectangle((28, 28, 560, 118), 18, fill=(8, 8, 20, 200), outline=PINK + (255,), width=3)
    d.text((50, 52), "VICE CITY  vs  REAL MIAMI", font=font(POPX, 22), fill=PINK + (255,), anchor="lm")
    d.text((50, 92), chap_at(line), font=fit(POPX, 32, chap_at(line), 490), fill=WHT + (255,), anchor="lm")
    n = sum(1 for x in REAL if t >= x + 0.3)
    glow_text(img, (1890, 64), f"REAL TWINS {n:02d}", font(TITAN, 46), MONEY, 1.0, "rm", None, 4)


# ------------------------------------------------------------------ cinematic post
YY, XX = np.mgrid[0:H, 0:W]
VIG = (1 - 0.32 * (((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) / 2).astype(np.float32)[..., None]
del YY, XX


def post(img, t):
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    sk = 0.0
    for s in SHAKES:
        if 0 <= t - s < 0.3: sk = max(sk, 14 * (1 - (t - s) / 0.3))
    dx = int(sk * math.sin(t * 90)); dy = int(sk * math.cos(t * 77))
    if dx or dy: a = np.roll(a, (dy, dx), axis=(0, 1))
    ca = 1 + int(sk * 0.25)
    a[..., 0] = np.roll(a[..., 0], ca, axis=1); a[..., 2] = np.roll(a[..., 2], -ca, axis=1)
    a = (a * VIG - 128) * 1.06 + 128 + np.array([4, 0, 6], np.float32)
    rng = np.random.default_rng(int(t * 30) % 997); g = rng.normal(0, 5.0, (H // 2, W // 2)).astype(np.float32)
    a += np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None]
    cut = min([abs(t - c) for c in CUTS] + [9])
    if cut < 0.1: a += 55 * (1 - cut / 0.1) * np.array([1.0, 0.75, 0.9], np.float32)
    return np.clip(a, 0, 255).astype(np.uint8)


def whip(prev, nxt, u):
    p = np.asarray(prev.convert("RGB")).astype(np.float32); n = np.asarray(nxt.convert("RGB")).astype(np.float32)
    k = int(80 * math.sin(math.pi * u)); src = p if u < 0.5 else n; out = np.zeros_like(p)
    for s in range(-3, 4): out += np.roll(src, int(s * k / 3), axis=1)
    return Image.fromarray(np.clip(out / 7, 0, 255).astype(np.uint8)).convert("RGBA")


AIK = ("clip", "card", "sign")


def frame(fi):
    t = fi / FPS; k = shot_at(t); t0 = SH[k][0]; line = line_at(t)
    img = base(k, t)
    if k > 0 and t - t0 < 0.13: img = whip(base(k - 1, t), img, (t - t0) / 0.13)
    overlays(img, t, k)
    if t >= LEAD:
        hud(img, t, line)
        if SH[k][1] == "clip": pill(img, "AI CONCEPT · NOT GAME FOOTAGE", 1890, 130, 18, (40, 40, 50), anchor="rm")
    caption(img, t)
    a = post(img, t)
    if t > TOTAL - 1.0: a = (a * max(0.0, (TOTAL - t) / 1.0)).astype(np.uint8)
    return Image.fromarray(a)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2), "shots", len(SH))
        for i, s in enumerate(SH): print(i, round(s[0], 2), round(scene_t(i)[1] - s[0], 2), s[1], s[2][:1])
    elif cmd == "still":
        os.makedirs("stills", exist_ok=True)
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills/s_{float(a):06.1f}.jpg", quality=86)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "21", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(fi).tobytes())
        p.stdin.close(); p.wait()
