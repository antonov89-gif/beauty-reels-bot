"""GTA 6 ep.3 'Launch Day' 9:16, cinematic. python3 engine51.py info | still t.. | video A B out.mp4"""
import datetime, glob, json, math, os, subprocess, sys
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script51 import LINES

W, H, FPS = 1080, 1920, 30
POPX = "Poppins-ExtraBold.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (60, 200, 90), (80, 170, 255), (255, 255, 255), (0, 0, 0)
ORG, CYAN, PINK = (255, 140, 30), (90, 220, 255), (255, 80, 160)
TM = json.load(open("timing.json")); D, TW, V0 = TM["D"], TM["T"], TM["starts"]
N = len(LINES)
LEAD = 3.0
ST = [LEAD + v for v in V0]
TOTAL = ST[-1] + D[-1] + 3.6
NF = int(TOTAL * FPS)
exec(open("helpers_raw.py").read())


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def clean(w): return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word, nth=0):
    ws = [clean(w) for w in LINES[i].split()]; q = clean(word)
    hits = [j for j, w in enumerate(ws) if w == q] or [j for j, w in enumerate(ws) if q in w]
    if not hits: raise KeyError((i, word))
    return ST[i] + TW[i][hits[min(nth, len(hits) - 1)]]


BL = [LEAD - 0.12] + [ST[i] - 0.12 for i in range(1, N)] + [TOTAL]
CUT2 = WT(2, "trailer") - 0.15
CUT5 = WT(5, "streamers") - 0.12
C6 = [WT(6, "neon") - 0.15, WT(6, "bridges") - 0.15, WT(6, "world") - 0.15]
# shots: (t0, t1, kind, name, s0, rate, zoom0, zoom1, cx, cy)
SH = [
    (0.0, LEAD, "clip", "K1", 0.0, 1.0, 1.0, 1.08, 0.5, 0.5),
    (LEAD, BL[1], "clip", "K1", 3.0, 0.76, 1.0, 1.1, 0.5, 0.5),
    (BL[1], BL[2], "map", "night", 0, 0, 0, 0, 0, 0),
    (BL[2], CUT2, "clip", "K2", 0.0, 1.0, 1.0, 1.08, 0.5, 0.5),
    (CUT2, BL[3], "clip", "K3", 0.0, 0.9, 2.1, 2.2, 0.90, 0.22),
    (BL[3], BL[4], "clip", "K5", 0.0, 0.68, 1.0, 1.08, 0.5, 0.5),
    (BL[4], BL[5], "cal", "cal", 0, 0, 0, 0, 0, 0),
    (BL[5], CUT5, "clip", "K7", 0.0, 1.0, 1.0, 1.12, 0.5, 0.5),
    (CUT5, BL[6], "clip", "K8", 0.0, 0.95, 1.0, 1.08, 0.55, 0.5),
    (BL[6], C6[0], "clip", "A2", 0.0, 1.0, 1.0, 1.06, 0.5, 0.5),
    (C6[0], C6[1], "clip", "A1", 0.0, 1.0, 1.0, 1.08, 0.5, 0.5),
    (C6[1], C6[2], "clip", "A0", 0.0, 1.0, 1.0, 1.06, 0.5, 0.5),
    (C6[2], BL[7], "clip", "A6", 0.0, 1.0, 1.0, 1.08, 0.5, 0.5),
    (BL[7], BL[8], "clip", "K1", 6.0, 0.55, 1.05, 1.16, 0.5, 0.5),
    (BL[8], TOTAL, "clip", "K10", 0.0, 1.0, 1.0, 1.1, 0.5, 0.5),
]
CUTS = [s[0] for s in SH[1:]]
SHAKES = [0.35, WT(0, "zero"), WT(3, "eight") - 0.1, WT(3, "billion") - 0.1, WT(5, "servers") - 0.1, WT(7, "two") - 0.1, ST[8] + 0.6]


def shot_at(t):
    for k, s in enumerate(SH):
        if s[0] <= t < s[1]: return k
    return len(SH) - 1


def cover(im, z=1.0, cx=0.5, cy=0.5):
    iw, ih = im.size; s = max(W / iw, H / ih) * z
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    x0 = min(max(0, int(cx * nw - W / 2)), nw - W); y0 = min(max(0, int(cy * nh - H / 2)), nh - H)
    return im.resize((nw, nh), Image.BILINEAR).crop((x0, y0, x0 + W, y0 + H))


@lru_cache(maxsize=60)
def fr(name, idx): return Image.open(f"frames/{name}_{idx:04d}.jpg").convert("RGB")


def clip_frame(name, sec):
    n = len(glob.glob(f"frames/{name}_*.jpg"))
    f = min(n - 1.001, max(0.0, sec * 24)); i = int(f); u = f - i
    a = fr(name, i + 1)
    return a if u < 0.02 else Image.blend(a, fr(name, i + 2), u)


# ------------------------------------------------------------------ helpers
def fit(fname, size, txt, maxw=W - 90):
    f = font(fname, size)
    while f.getlength(txt) > maxw and f.size > 18: f = font(fname, f.size - 2)
    return f


def label(img, txt, x, y, t, t0, size=62, col=WHT, glow=None, hold=None):
    if t < t0 or (hold and t > t0 + hold): return
    k = min(1.0, (t - t0) / 0.16); s = 1.3 - 0.3 * ease(k)
    a = 1.0 if not hold else min(1.0, (t0 + hold - t) / 0.25)
    f = fit(POPX, size * s, txt); d = ImageDraw.Draw(img)
    if glow:
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).text((x, y), txt, font=f, fill=glow + (int(230 * a),), anchor="mm", stroke_width=int(size * 0.2), stroke_fill=glow + (int(230 * a),))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x + 4, y + 6), txt, font=f, fill=(0, 0, 0, int(150 * a)), anchor="mm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    d.text((x, y), txt, font=f, fill=col + (int(255 * a),), anchor="mm", stroke_width=max(3, int(size * 0.07)), stroke_fill=(0, 0, 0, int(220 * a)))


def pill(img, txt, cx, cy, sz, bg, fg=WHT):
    f = font(POPX, sz); pw, ph = int(f.getlength(txt) + sz * 1.2), int(sz * 1.7)
    d = ImageDraw.Draw(img); d.rounded_rectangle((cx - pw / 2, cy - ph / 2, cx + pw / 2, cy + ph / 2), int(ph * 0.35), fill=bg + (225,), outline=WHT + (255,), width=3)
    d.text((cx, cy), txt, font=f, fill=fg, anchor="mm")


def shade(img, h=640, a0=150, bottom=False):
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); px = ImageDraw.Draw(g)
    for yy in range(h):
        y = H - 1 - yy if bottom else yy
        px.line([(0, y), (W, y)], fill=(0, 0, 0, int(a0 * (1 - yy / h) ** 1.5)))
    img.alpha_composite(g)


def counter(img, v0, v1, fmt, x, y, t, t0, dur, size, col=YEL, glow=None):
    if t < t0: return
    v = v0 + (v1 - v0) * ease((t - t0) / dur); label(img, fmt.format(v), x, y, t, t0, size, col, glow=glow)


def grad_title(img, txt, cy, size, t, t0):
    if t < t0: return
    k = ease((t - t0) / 0.25); f = font("fonts/titan-one.ttf", size * (1.5 - 0.5 * k))
    while f.getlength(txt) > W - 80 and f.size > 20: f = font("fonts/titan-one.ttf", f.size - 2)
    d = ImageDraw.Draw(img)
    gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).text((W / 2, cy), txt, font=f, fill=PINK + (230,), anchor="mm", stroke_width=26, stroke_fill=PINK + (230,))
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(18)))
    d.text((W / 2, cy), txt, font=f, fill=BLK + (255,), anchor="mm", stroke_width=18, stroke_fill=BLK + (255,))
    d.text((W / 2, cy), txt, font=f, fill=WHT + (255,), anchor="mm", stroke_width=5, stroke_fill=WHT + (255,))
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).text((W / 2, cy), txt, font=f, fill=255, anchor="mm")
    bb = m.getbbox()
    if bb:
        g = np.zeros((H, W, 3), np.uint8); stops = ((255, 214, 64), (255, 132, 52), (255, 52, 140), (150, 50, 210))
        for y in range(bb[1], bb[3] + 1):
            tt = (y - bb[1]) / max(1, bb[3] - bb[1]); kk = tt * 3; i = min(int(kk), 2); u = kk - i
            g[y] = [int(stops[i][c] * (1 - u) + stops[i + 1][c] * u) for c in range(3)]
        layer = Image.fromarray(g).convert("RGBA"); layer.putalpha(m.filter(ImageFilter.MinFilter(9))); img.alpha_composite(layer)


OBJ = ["WAIT FOR MIDNIGHT", "SPREAD THE WAVE", "JOIN THE LINE", "COUNT THE MONEY", "SURVIVE THE BLAST ZONE", "HOLD THE SERVERS", "ENTER LEONIDA", "BREAK THE RECORD", "PRESS START"]


def hud(img, t, line):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((28, 40, 640, 150), 22, fill=(8, 8, 20, 200), outline=PINK + (255,), width=3)
    d.text((52, 66), "MISSION  ·  LAUNCH DAY", font=font(POPX, 26), fill=PINK + (255,), anchor="lm")
    d.text((52, 114), OBJ[line], font=font(POPX, 36), fill=WHT + (255,), anchor="lm")
    cx, cy, r = 930, 112, 72                                   # own-design radar
    rad = Image.new("RGBA", (2 * r + 8, 2 * r + 8), (0, 0, 0, 0)); rd = ImageDraw.Draw(rad); c = r + 4
    rd.ellipse((4, 4, 2 * r + 4, 2 * r + 4), fill=(6, 12, 24, 215), outline=CYAN + (255,), width=3)
    for q in (0.33, 0.66): rd.ellipse((c - r * q, c - r * q, c + r * q, c + r * q), outline=CYAN + (110,), width=1)
    rd.line((c, 6, c, 2 * r + 2), fill=CYAN + (90,), width=1); rd.line((6, c, 2 * r + 2, c), fill=CYAN + (90,), width=1)
    ang = (t * 1.6) % (2 * math.pi)
    for k in range(14): a_ = ang - k * 0.06; rd.line((c, c, c + r * math.cos(a_), c + r * math.sin(a_)), fill=GRN + (int(150 * (1 - k / 14)),), width=3)
    rng = np.random.default_rng(line * 7 + 1)
    for q in range(6):
        pa, pr = rng.uniform(0, 2 * math.pi), rng.uniform(0.25, 0.85) * r; vis = (ang - pa) % (2 * math.pi) < 2.2
        if vis: rd.ellipse((c + pr * math.cos(pa) - 5, c + pr * math.sin(pa) - 5, c + pr * math.cos(pa) + 5, c + pr * math.sin(pa) + 5), fill=PINK + (255,))
    rd.polygon([(c, c - 9), (c - 7, c + 7), (c + 7, c + 7)], fill=WHT + (255,))
    img.alpha_composite(rad, (cx - r - 4, cy - r - 4))


# ------------------------------------------------------------------ special scenes
@lru_cache(maxsize=1)
def night(): return Image.open("sat/night.jpg").convert("RGB")


def map_frame(t):
    a, b = SH[2][0], SH[2][1]; p = ease((t - a) / (b - a)); im = night(); iw, ih = im.size
    front = 178 - 356 * p                                   # launch front, degrees longitude (moves west)
    cw = 1500; cx = (front + 180) / 360 * iw; x0 = int(min(max(0, cx - cw / 2), iw - cw)); y0 = 80
    crop = im.crop((x0, y0, x0 + cw, y0 + int(cw * 600 / 1080))).resize((1080, 600), Image.LANCZOS)
    arr = np.asarray(crop).astype(np.float32)
    lon = ((x0 + np.arange(1080) / 1080 * cw) / iw) * 360 - 180
    lum = arr.max(axis=2) / 255.0
    launched = np.clip((lon - front) / 4.0, 0, 1)[None, :]
    boost = (lum ** 0.6) * launched
    glow = np.asarray(Image.fromarray(np.clip(boost * 255, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(10))).astype(np.float32) / 255.0
    col = np.array([255, 70, 170], np.float32); cy_ = np.array([90, 220, 255], np.float32)
    arr = arr * 0.95 + (boost[..., None] * 230 + glow[..., None] * 170) * (col / 255.0)
    band = np.exp(-((lon - front) / 2.0) ** 2)[None, :, None] * 190
    arr = np.clip((arr + band * (cy_ / 255.0)) * 1.25, 0, 255)
    img = Image.new("RGBA", (W, H), (6, 6, 18, 255)); d = ImageDraw.Draw(img)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=(6 + int(10 * yy / H), 6, 20 + int(26 * yy / H), 255))
    img.paste(Image.fromarray(arr.astype(np.uint8)).convert("RGBA"), (0, 660))
    d = ImageDraw.Draw(img); d.rectangle((0, 656, W, 660), fill=PINK + (255,)); d.rectangle((0, 1260, W, 1264), fill=PINK + (255,))
    hrs = int(round(19 * p)); bx0 = 90; bw = (W - 180) / 19
    for q in range(19):
        c = (255, 70, 170, 255) if q < hrs else (40, 40, 70, 255)
        d.rounded_rectangle((bx0 + q * bw + 2, 1380, bx0 + (q + 1) * bw - 2, 1440), 6, fill=c)
    label(img, f"LOCAL MIDNIGHT ROLLS WEST  +{hrs} H", 540, 1330, t, a + 0.3, 44, WHT)
    label(img, "NEW ZEALAND FIRST", 300, 1490, t, a + 0.5, 34, YEL)
    label(img, "~19 HOURS LATER: LAST", 790, 1490, t, b - 1.6, 34, YEL)
    label(img, "LAUNCH WAVE", 540, 330, t, a + 0.05, 112, WHT, glow=PINK)
    label(img, "MIDNIGHT, TIME ZONE BY TIME ZONE", 540, 470, t, WT(1, "millions") - 0.1, 50, YEL)
    pill(img, "NASA NIGHT LIGHTS \u00b7 ROLLOUT AS REPORTED FROM STORE LISTINGS", 540, 1790, 24, (20, 90, 160))
    return img


def cal_frame(t):
    a, b = SH[6][0], SH[6][1]; img = Image.new("RGBA", (W, H), (8, 8, 20, 255)); d = ImageDraw.Draw(img)
    for yy in range(H): d.line([(0, yy), (W, yy)], fill=(8 + int(14 * yy / H), 6, 26 + int(20 * yy / H), 255))
    d = ImageDraw.Draw(img)
    start = datetime.date(2026, 10, 19); cell = 108; gx, gy = (W - 7 * cell) // 2, 640
    launch = datetime.date(2026, 11, 19); tmove = WT(4, "moved") - 0.1; tblast = WT(4, "blast") - 0.1
    mv = ease((t - tmove) / 1.0); zone = min(1.0, max(0.0, (t - tblast) / 0.4))
    for w in range(8):
        for dd in range(7):
            day = start + datetime.timedelta(days=w * 7 + dd); x = gx + dd * cell; y = gy + w * cell
            inzone = abs((day - launch).days) <= 21; isl = day == launch
            fill = (22, 24, 46, 255)
            if inzone: fill = (60 + int(60 * zone), 20, 40, 255) if zone > 0 else (32, 34, 62, 255)
            if isl: fill = (230, 50, 140, 255)
            d.rounded_rectangle((x + 4, y + 4, x + cell - 4, y + cell - 4), 14, fill=fill)
            d.text((x + cell / 2, y + cell / 2), str(day.day), font=font(POPX, 34 if not isl else 46), fill=WHT + (255,) if inzone or isl else (150, 150, 180, 255), anchor="mm")
    rng = np.random.default_rng(11); cols = [(80, 200, 255), (255, 180, 60), (130, 240, 130), (230, 120, 255), (255, 110, 110)]
    cards = []
    for k in range(12):
        w = int(rng.integers(0, 8)); dd = int(rng.integers(0, 7)); day = start + datetime.timedelta(days=w * 7 + dd)
        if day == launch: continue
        cards.append((w, dd, abs((day - launch).days) <= 21, cols[k % 5], 1 if dd >= 3 else -1))
    for w, dd, inz, c, side in cards:
        x = gx + dd * cell; y = gy + w * cell; off = (mv * 1500 * side) if inz else 0
        if inz and t < tmove - 1.2: off += 4 * math.sin(t * 20 + w)
        if -cell < x + off < W + cell: d.rounded_rectangle((x + 10 + off, y + 14, x + cell - 10 + off, y + cell - 14), 12, fill=c + (255,), outline=WHT + (255,), width=3); d.text((x + cell / 2 + off, y + cell / 2), "NEW", font=font(POPX, 24), fill=BLK + (255,), anchor="mm")
    if zone > 0:
        z0 = gy + 1.0 * cell; z1 = gy + 7.0 * cell - 4
        for q in range(3): d.rounded_rectangle((gx - 10 - q * 2, z0 - 10 - q * 2, gx + 7 * cell + 10 + q * 2, z1 + 10 + q * 2), 22, outline=RED + (int((200 - q * 60) * (0.6 + 0.4 * math.sin(t * 8))),), width=5)
    label(img, "NOVEMBER 2026", 540, 330, t, a + 0.05, 84, WHT, glow=PINK)
    label(img, "THE BLAST ZONE", 540, 460, t, tblast, 100, RED, glow=BLK)
    label(img, "3 WEEKS BEFORE AND AFTER", 540, 560, t, tblast + 0.3, 46, YEL)
    pill(img, "ILLUSTRATION · NO REAL RELEASE DATES SHOWN", 540, 1790, 28, (40, 40, 50))
    return img


# ------------------------------------------------------------------ per-block overlays
def overlays(img, t, line):
    if t < LEAD:
        grad_title(img, "GTA 6", 700, 280, t, 0.25)
        grad_title(img, "LAUNCH DAY", 960, 130, t, 0.7)
        label(img, "19.11.2026", 540, 1120, t, 1.1, 90, YEL, glow=BLK)
        return
    if line == 0:
        tz = WT(0, "zero"); n = int(math.ceil(max(0.0, tz - t)))
        label(img, f"T-00:00:{n:02d}" if t < tz else "00:00:00", 540, 310, t, ST[0] + 0.1, 112, WHT if t < tz else YEL, glow=PINK)
        if t >= tz: label(img, "GO!", 540, 450, t, tz, 150, YEL, glow=RED, hold=1.4)
    elif line == 1: pass
    elif line == 2:
        if t < CUT2:
            label(img, "THE LINES", 540, 300, t, WT(2, "lines") - 0.1, 110, WHT, glow=PINK)
            label(img, "MIDNIGHT. DOORS OPEN.", 540, 420, t, WT(2, "midnight") - 0.1, 56, YEL)
        else:
            counter(img, 0, 90421491, "{:,.0f}", 540, 300, t, WT(2, "ninety") - 0.1, 1.6, 100, WHT, PINK)
            label(img, "VIEWS IN 24 HOURS", 540, 420, t, WT(2, "ninety") + 0.1, 66, YEL)
            label(img, "RECORD FOR A GAME REVEAL", 540, 520, t, WT(2, "record") - 0.1, 50, WHT)
    elif line == 3:
        shade(img, 700, 120)
        label(img, "THE MONEY", 540, 290, t, ST[3] + 0.1, 112, WHT, glow=PINK)
        tb = [WT(3, "eight") - 0.1, WT(3, "billion") - 0.1, WT(3, "nobody") - 0.1]
        base_y = 1380; hmax = 560; xs = [270, 540, 810]; hs = [0.8 * hmax * 0.6, hmax * 0.75, hmax]
        d = ImageDraw.Draw(img)
        for q, (x, h) in enumerate(zip(xs, [0.62 * hmax, 0.80 * hmax, 1.0 * hmax])):
            k = ease((t - tb[q]) / 0.9)
            if k <= 0: continue
            hh = h * k
            if q < 2:
                d.rounded_rectangle((x - 80, base_y - hh, x + 80, base_y), 18, fill=(GRN if q == 0 else CYAN) + (255,), outline=WHT + (255,), width=4)
            else:
                pul = 0.5 + 0.5 * math.sin(t * 7)
                d.rounded_rectangle((x - 80, base_y - hh, x + 80, base_y), 18, outline=PINK + (255,), fill=(255, 80, 160, int(70 + 80 * pul)), width=6)
                d.text((x, base_y - hh / 2), "?", font=font(POPX, 150), fill=WHT + (255,), anchor="mm", stroke_width=6, stroke_fill=BLK)
        label(img, "$800 MILLION", 270, base_y - 0.62 * hmax - 60, t, tb[0] + 0.4, 38, GRN)
        label(img, "$1 BILLION", 540, base_y - 0.80 * hmax - 60, t, tb[1] + 0.4, 40, CYAN)
        label(img, "GTA 6", 810, base_y - hmax - 60, t, tb[2] + 0.4, 44, PINK)
        label(img, "GTA 5: DAY 1", 270, base_y + 54, t, tb[0] + 0.3, 30, WHT); label(img, "GTA 5: 3 DAYS", 540, base_y + 54, t, tb[1] + 0.3, 30, WHT); label(img, "NOBODY KNOWS", 810, base_y + 54, t, tb[2] + 0.3, 30, WHT)
    elif line == 4:
        pass
    elif line == 5:
        if t < CUT5:
            label(img, "SERVERS BRACE", 540, 290, t, WT(5, "servers") - 0.1, 96, WHT, glow=CYAN)
            ld = ease((t - WT(5, "millions")) / 1.1) if t > WT(5, "millions") else 0
            d = ImageDraw.Draw(img); d.rounded_rectangle((140, 400, 940, 450), 18, fill=(0, 0, 0, 170), outline=WHT + (255,), width=3)
            if ld > 0: d.rounded_rectangle((146, 406, 146 + 788 * ld, 444), 14, fill=(255 - int(120 * (1 - ld)), 70 + int(130 * (1 - ld)), 90, 255))
            label(img, f"LOGIN QUEUE {int(ld * 100)}%", 540, 500, t, WT(5, "millions"), 44, YEL)
        else:
            label(img, "STREAMERS GO LIVE", 540, 290, t, WT(5, "streamers") - 0.1, 84, WHT, glow=PINK)
            pill(img, "● LIVE", 200, 410, 44, (220, 30, 50)) if (t * 2) % 2 < 1.4 else None
    elif line == 6:
        label(img, "WELCOME TO LEONIDA", 540, 290, t, WT(6, "wakes") - 0.5, 80, WHT, glow=PINK)
        if C6[0] <= t < C6[1]: label(img, "NEON BEACHES", 540, 410, t, C6[0] + 0.1, 70, YEL)
        elif C6[1] <= t < C6[2]: label(img, "BRIDGES OVER OPEN SEA", 540, 410, t, C6[1] + 0.1, 62, YEL)
        elif t >= C6[2]: label(img, "A WORLD WITH A LIFE OF ITS OWN", 540, 410, t, C6[2] + 0.1, 48, YEL)
    elif line == 7:
        shade(img, 800, 130)
        counter(img, 0, 200000000, "{:,.0f}+", 540, 330, t, WT(7, "two") - 0.1, 2.0, 110, WHT, GRN)
        label(img, "COPIES SOLD BY GTA 5", 540, 450, t, WT(7, "two") + 0.1, 60, YEL)
        n = int(round(13 * ease((t - WT(7, "thirteen") + 0.8) / 1.2))) if t > WT(7, "thirteen") - 0.8 else 0
        label(img, "SINCE 2013", 540, 560, t, WT(7, "thirteen") - 1.2, 60, WHT)
        label(img, f"{n} YEARS", 540, 690, t, WT(7, "thirteen") - 0.8, 96, YEL, glow=PINK)
        label(img, "DAY ONE IS ONLY THE BEGINNING", 540, 1280, t, WT(7, "beginning") - 0.4, 54, YEL, glow=BLK)
    elif line == 8:
        shade(img, 760, 150)
        label(img, "WHERE WILL YOU BE", 540, 300, t, WT(8, "where") - 0.1, 88, WHT, glow=PINK)
        label(img, "AT MIDNIGHT?", 540, 430, t, WT(8, "midnight") - 0.2, 120, YEL, glow=BLK)
        label(img, "19.11.2026", 540, 1300, t, ST[8] + 1.2, 110, WHT, glow=PINK)


def caption(img, t):
    for i in range(N):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.15:
            words = LINES[i].split(); cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05: cur = j
            c0 = cur // 3 * 3; txt = " ".join(words[c0:c0 + 3]); f = fit(POPX, 64, txt, W - 120)
            sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 3, 1560 + 5), txt, font=f, fill=(0, 0, 0, 170), anchor="mm")
            img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
            ImageDraw.Draw(img).text((W / 2, 1560), txt, font=f, fill=WHT, anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 200)); return


def base(k, t):
    t0, t1, kind, name, s0, rate, z0, z1, cx, cy = SH[k]
    if kind == "map": return map_frame(t)
    if kind == "cal": return cal_frame(t)
    u = (t - t0) / max(0.1, t1 - t0); z = z0 + (z1 - z0) * ease(u)
    img = cover(clip_frame(name, s0 + (t - t0) * rate), z, cx, cy).convert("RGBA")
    return img


def line_at(t):
    if t < LEAD: return -1
    for i in range(N - 1, -1, -1):
        if t >= BL[i] if i else t >= LEAD: return i
    return 0


# ------------------------------------------------------------------ cinematic post
def post(img, t, k):
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    sk = 0.0
    for s in SHAKES:
        if 0 <= t - s < 0.3: sk = max(sk, 16 * (1 - (t - s) / 0.3))
    dx = int(sk * math.sin(t * 90)); dy = int(sk * math.cos(t * 77))
    if dx or dy: a = np.roll(a, (dy, dx), axis=(0, 1))
    ca = 1 + int(sk * 0.25)                                    # chromatic aberration
    a[..., 0] = np.roll(a[..., 0], ca, axis=1); a[..., 2] = np.roll(a[..., 2], -ca, axis=1)
    yy, xx = np.mgrid[0:H, 0:W]; v = 1 - 0.30 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    a = a * v[..., None]
    a = (a - 128) * 1.07 + 128 + np.array([4, 0, 6], np.float32)       # contrast + slight teal/pink grade
    rng = np.random.default_rng(int(t * 30) % 997); g = rng.normal(0, 5.5, (H // 2, W // 2)).astype(np.float32)
    a += np.kron(g, np.ones((2, 2), np.float32))[..., None]       # film grain
    cut = min([abs(t - c) for c in CUTS] + [9])
    if cut < 0.12: a += 70 * (1 - cut / 0.12) * np.array([1.0, 0.75, 0.9], np.float32)   # light-leak flash on cuts
    return np.clip(a, 0, 255).astype(np.uint8)


def whip(prev, nxt, u):
    p = np.asarray(prev.convert("RGB")).astype(np.float32); n = np.asarray(nxt.convert("RGB")).astype(np.float32)
    k = int(60 * math.sin(math.pi * u)); out = np.zeros_like(p)
    for s in range(-3, 4): out += np.roll(p if u < 0.5 else n, int(s * k / 3), axis=1)
    out /= 7
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")


def frame(fi):
    t = fi / FPS; k = shot_at(t); t0 = SH[k][0]; line = line_at(t)
    img = base(k, t)
    if k > 0 and t - t0 < 0.14: img = whip(base(k - 1, t), img, (t - t0) / 0.14)
    overlays(img, t, line)
    if line >= 0:
        hud(img, t, line)
        if SH[k][2] not in ("map", "cal"): pill(img, "AI CONCEPT · NOT GAME FOOTAGE", 540, 1790, 28, (40, 40, 50))
    caption(img, t)
    a = post(img, t, k)
    if t > TOTAL - 0.6: a = (a * max(0.0, (TOTAL - t) / 0.6)).astype(np.uint8)
    return Image.fromarray(a)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for s in SH: print(round(s[0], 2), round(s[1], 2), s[2], s[3])
    elif cmd == "still":
        os.makedirs("stills", exist_ok=True)
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills/s_{float(a):05.1f}.jpg", quality=88)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(fi).tobytes())
        p.stdin.close(); p.wait()
