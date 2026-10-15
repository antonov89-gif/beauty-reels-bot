"""Yap stone money map Short (Palmerston format). python3 engine36.py still N.. | info | prefetch | video A B out.mp4"""
import json, math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import tiles
from script36 import LINES

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
        m = np.clip((0.40 - a.max(2, keepdims=True)) / 0.14, 0, 1)
        yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
        oc = np.array([0.05, 0.22, 0.42], np.float32) * (1 - 0.25 * yy) + 0.02
        a = a * (1 - m) + (oc + (a - a.mean(2, keepdims=True)) * 0.3) * m
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")



def kf(t, keys, logspan=False):
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            k = ease((t - t0) / max(1e-3, t1 - t0))
            out = [lerp(a, b, k) for a, b in zip(v0, v1)]
            if logspan: out[2] = math.exp(lerp(math.log(v0[2]), math.log(v1[2]), k))
            return tuple(out)
    return keys[-1][1]

YAP = (138.13, 9.53); PALAU = (134.55, 7.45); SEA = (136.6, 8.9)
SC = [0.0] + [ST[i] - 0.12 for i in range(1, len(LINES))] + [TOTAL + 1]
CUTS = SC[1:-1]
CLIPS = {5: "clips/K1.mp4", 6: "clips/K1.mp4", 11: "clips/K2.mp4"}
STONE = (196, 192, 180)
_CF = {}


def clip_frame(name, t0, t1, t):
    if name not in _CF:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", name, "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        _CF[name] = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    fr = _CF[name]; n = len(fr)
    k = (t - t0) / max(0.1, t1 - t0)
    return Image.fromarray(fr[min(n - 1, max(0, int(k * (n - 1))))]).convert("RGBA")


def stone(img, x, y, r, k=1.0, alpha=1.0, ghost=False):
    """Code-drawn rai stone: limestone disk with a hole, soft shading, speckles."""
    if k <= 0.01 or r * k < 3: return
    r = r * k; a = int(255 * alpha)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if ghost:
        d.ellipse((x - r, y - r, x + r, y + r), outline=WHT + (a,), width=8)
        d.ellipse((x - r * 0.24, y - r * 0.24, x + r * 0.24, y + r * 0.24), outline=WHT + (a,), width=6)
        img.alpha_composite(lay); return
    d.ellipse((x - r + 10, y - r + 16, x + r + 10, y + r + 16), fill=(0, 0, 0, int(a * 0.45)))
    for q in range(12):
        f = 1 - q / 12; c = tuple(int(v * (0.80 + 0.22 * q / 12)) for v in STONE)
        d.ellipse((x - r * f - r * 0.06 * q / 12, y - r * f - r * 0.08 * q / 12, x + r * f - r * 0.06 * q / 12, y + r * f - r * 0.08 * q / 12), fill=c + (a,))
    rng = np.random.default_rng(int(r) + 7)
    for _ in range(int(40 + r * 0.6)):
        ang = rng.random() * 2 * math.pi; rr = r * (0.3 + 0.65 * rng.random()); s = 1 + rng.random() * r * 0.025
        cx, cy = x + math.cos(ang) * rr, y + math.sin(ang) * rr; g = int(120 + 60 * rng.random())
        d.ellipse((cx - s, cy - s, cx + s, cy + s), fill=(g, g - 4, g - 12, int(a * 0.55)))
    h = r * 0.24
    d.ellipse((x - h - 4, y - h - 4, x + h + 4, y + h + 4), fill=(150, 146, 136, a))
    d.ellipse((x - h, y - h, x + h, y + h), fill=(40, 46, 52, a))
    d.ellipse((x - r, y - r, x + r, y + r), outline=(60, 58, 52, a), width=max(3, int(r * 0.03)))
    img.alpha_composite(lay)


def dim(img, a=0.55):
    img.alpha_composite(Image.new("RGBA", (W, H), (6, 14, 34, int(255 * a))))


def bubble(img, x, y, s, k, left=True, size=62):
    if k <= 0: return
    f = font(POPX, size * k); tw = f.getlength(s)
    dd = ImageDraw.Draw(img); x0, y0 = x - tw / 2 - 30, y - 50 * k
    dd.rounded_rectangle((x0, y0, x0 + tw + 60, y0 + 100 * k), 30, fill=WHT, outline=BLK, width=5)
    tx = x0 + (50 if left else tw + 10); dd.polygon([(tx, y0 + 98 * k), (tx + 40, y0 + 98 * k), (tx + (0 if left else 40), y0 + 150 * k)], fill=WHT)
    dd.text((x, y), s, font=f, fill=BLK, anchor="mm")


def cam_for(i, t):
    a, b = SC[i], SC[i + 1]
    if i == 0: return kf(t, [(a, (150, 8, 120)), (WT(0, "zoom"), (141, 9, 22)), (WT(0, "find"), (138.13, 9.53, 1.1)), (b, (138.13, 9.53, 0.62))], True)
    if i == 1: return kf(t, [(a, (138.13, 9.53, 0.6)), (b, (138.13, 9.53, 0.48))], True)
    if i == 2: return (138.13, 9.53, 0.5)
    if i == 3: return kf(t, [(a, (138.13, 9.53, 1.2)), (WT(3, "Palau") - 0.3, (136.35, 8.5, 7.2)), (b, (136.35, 8.5, 6.6))], True)
    if i == 4: return kf(t, [(a, (136.35, 8.5, 6.6)), (b, (136.35, 8.5, 6.2))])
    if i == 7: return kf(t, [(a, (136.35, 8.5, 6.4)), (b, (136.35, 8.5, 6.0))])
    if i == 8: return kf(t, [(a, (138.15, 9.55, 0.30)), (b, (138.15, 9.55, 0.24))], True)
    if i == 9: return kf(t, [(a, (SEA[0], SEA[1], 3.2)), (b, (SEA[0], SEA[1], 2.8))])
    if i == 10: return kf(t, [(a, (138.13, 9.53, 0.55)), (b, (138.13, 9.53, 0.45))], True)
    return (138.13, 9.53, 0.6)


def route(cam):
    yx, yy = cam.xy(*YAP); px, py = cam.xy(*PALAU)
    return [(px + (yx - px) * s, py + (yy - py) * s - math.sin(math.pi * s) * 90) for s in np.linspace(0, 1, 40)]


def render(t, fi):
    i = max(j for j in range(len(LINES)) if SC[j] <= t) if t >= 0 else 0
    if i in CLIPS:
        if i in (5, 6):
            img = clip_frame(CLIPS[i], SC[5], SC[7], t)
            if t >= SC[5] + 0.15: badge(img, W / 2, 330, "PALAU, CENTURIES AGO", (0, 120, 200), pop((t - SC[5] - 0.15) / 0.3), "⛵", 50)
            if i == 6:
                if t < WT(6, "sank") - 0.1: bubble(img, 560, 760, "Don't. Let. Go.", pop((t - SC[6] - 0.2) / 0.3), True)
                else:
                    big(img, "MANY SANK", t, WT(6, "sank"), 560, 150, RED)
                    paste_emoji(img, "🌊", W / 2, 760, 170 * pop((t - WT(6, "sank")) / 0.3))
        else:
            img = clip_frame(CLIPS[i], SC[11], SC[12] - 1.2, t)
            if t < WT(11, "bottom") - 0.1: bubble(img, 420, 720, "My money? Right there.", pop((t - SC[11] - 0.2) / 0.3), True, 56)
            else:
                big(img, "AT THE BOTTOM", t, WT(11, "bottom"), 300, 110, WHT); big(img, "OF THE OCEAN", t, WT(11, "ocean"), 450, 130, YEL)
        return img
    lo, la, sp = cam_for(i, t)
    cam = tiles.Cam(lo, la, sp)
    img = grade(cam.render(), cam.src == "esri")
    yx, yy = cam.xy(*YAP)
    if i == 0:
        if sp > 0.9: pulse(img, yx, yy, t, SC[0] + 0.3, YEL, 140); ring(img, yx, yy, 46, YEL, 1.0)
        big(img, "WESTERN PACIFIC", t, WT(0, "western"), 560, 76, YEL) if t < WT(0, "zoom") + 0.4 else None
        if t >= WT(0, "Yap"): badge(img, W / 2, 330, "YAP, MICRONESIA", (0, 120, 200), pop((t - WT(0, "Yap")) / 0.3), "🇫🇲", 56)
    elif i == 1:
        if t >= WT(1, "eleven"): badge(img, W / 2, 330, "~11,000 PEOPLE", (30, 30, 30), pop((t - WT(1, "eleven")) / 0.3), "👥", 58)
        if t >= WT(1, "money"):
            k = pop((t - WT(1, "money")) / 0.35); stone(img, W / 2, 1120, 150, k)
            badge(img, W / 2, 900, "MONEY = STONE", (200, 140, 20), k, "💰", 52)
    elif i == 2:
        dim(img, 0.62)
        if t >= WT(2, "smallest"):
            k = pop((t - WT(2, "smallest")) / 0.3); stone(img, 170, 1150, 26, k)
            badge(img, 170, 1040, "COIN-SIZED", (30, 30, 30), k, None, 40)
        if t >= WT(2, "biggest"):
            k = pop((t - WT(2, "biggest")) / 0.4); stone(img, 650, 900, 300, k)
            if t >= WT(2, "biggest") + 0.4: paste_emoji(img, "🧍", 960, 1060, 290 * pop((t - WT(2, "biggest") - 0.4) / 0.3))
        if t >= WT(2, "four"): big(img, "~4 TONS", t, WT(2, "four"), 380, 170, YEL)
    elif i in (3, 4, 7):
        pts = route(cam); px, py = cam.xy(*PALAU)
        ring(img, yx, yy, 34, YEL, 1.0)
        if i == 3:
            if t >= WT(3, "no"): big(img, "NOT ON YAP", t, WT(3, "no"), 330, 110, RED)
            if t >= WT(3, "Palau"):
                glow_line(img, partial(pts, ease((t - WT(3, "Palau")) / 0.9)), WHT, 6, 0.6, dash=(24, 16), phase=t * 40)
                pin(img, px, py, "PALAU", (30, 30, 30), pop((t - WT(3, "Palau") - 0.2) / 0.3), "🇵🇼", False, 46)
                pin(img, yx, yy, "YAP", (0, 120, 200), 1.0, "🇫🇲", True, 46)
            if t >= WT(3, "four"): badge(img, (px + yx) / 2, (py + yy) / 2 - 170, "400+ KM", (30, 30, 30), pop((t - WT(3, "four")) / 0.3), None, 52)
        else:
            glow_line(img, pts, WHT, 6, 0.6, dash=(24, 16), phase=t * 40)
            pin(img, px, py, "PALAU", (30, 30, 30), 1.0, "🇵🇼", False, 46); pin(img, yx, yy, "YAP", (0, 120, 200), 1.0, "🇫🇲", True, 46)
            if i == 4:
                big(img, "HOW?", t, WT(4, "how"), 330, 230, YEL)
                badge(img, W / 2, 520, "STONE WHEEL = MONEY?", (30, 30, 30), pop((t - WT(4, "stone")) / 0.3), "🤔", 48) if t >= WT(4, "stone") else None
            else:
                s = ease((t - SC[7] - 0.2) / max(0.5, SC[8] - SC[7] - 0.6))
                q = min(len(pts) - 1, int(s * (len(pts) - 1))); stone(img, pts[q][0], pts[q][1] - 40, 42, 1.0)
                x0, y0, y1 = 985, 1350, 900
                dd = ImageDraw.Draw(img)
                dd.rounded_rectangle((x0 - 34, y1 - 10, x0 + 34, y0 + 10), 30, fill=(0, 0, 0, 150), outline=WHT, width=5)
                dd.rounded_rectangle((x0 - 24, y0 - (y0 - y1) * s, x0 + 24, y0), 22, fill=GOLD + (255,))
                paste_emoji(img, "💰", x0, y1 - 70, 90)
                if t >= WT(7, "harder"): big(img, "HARDER TRIP", t, WT(7, "harder"), 330, 110, WHT)
                if t >= WT(7, "worth"): big(img, "= MORE VALUE", t, WT(7, "worth"), 470, 110, YEL)
    elif i == 8:
        stone(img, W / 2, 980, 190, 1.0)
        if t >= WT(8, "twist"): big(img, "THE TWIST", t, WT(8, "twist"), 330, 120, YEL) if t < WT(8, "never") else None
        if t >= WT(8, "never"): big(img, "IT NEVER MOVES", t, WT(8, "never"), 330, 100, WHT); paste_emoji(img, "🔒", W / 2, 980, 110 * pop((t - WT(8, "never")) / 0.3))
        if t >= WT(8, "island"):
            for q in range(8):
                ang = q / 8 * 2 * math.pi - math.pi / 2
                paste_emoji(img, "👥", W / 2 + math.cos(ang) * 330, 980 + math.sin(ang) * 330, 100 * pop((t - WT(8, "island") - q * 0.06) / 0.3))
        if t >= WT(8, "owns"): badge(img, W / 2, 1420 - 140, "OWNERSHIP = MEMORY", (200, 60, 50), pop((t - WT(8, "owns")) / 0.3), "🧠", 50)
    elif i == 9:
        s = ease((t - WT(9, "fell")) / 2.2) if t >= WT(9, "fell") else 0
        y = 700 + 480 * s
        if t >= WT(9, "fell"):
            stone(img, W / 2, y, 150, 1.0, alpha=max(0.0, 1 - s * 1.2)) if s < 0.83 else None
            if s > 0.3:
                for q in range(6): paste_emoji(img, "🫧", W / 2 - 120 + q * 50, y - 120 - ((t * 120 + q * 40) % 200), 44)
        if t >= WT(9, "never"): big(img, "NEVER SEEN AGAIN", t, WT(9, "never"), 330, 90, WHT) if t < WT(9, "agreed") else None
        if t >= WT(9, "agreed"):
            stone(img, W / 2, 1180, 150, 1.0, alpha=0.9, ghost=True)
            big(img, "STILL OWNED", t, WT(9, "agreed"), 330, 120, GRN); paste_emoji(img, "✅", W / 2, 520, 120 * pop((t - WT(9, "agreed")) / 0.3))
        if t >= WT(9, "trading"):
            for q, (ox, oy) in enumerate(((-300, -60), (300, 40), (-240, 260), (260, 300))):
                badge(img, W / 2 + ox, 1180 + oy - 200, "SOLD", (30, 30, 30), pop((t - WT(9, "trading") - q * 0.12) / 0.3), "🤝", 40)
    elif i == 10:
        if t >= WT(10, "today"): badge(img, W / 2, 330, "STILL USED TODAY", (0, 120, 200), pop((t - WT(10, "today")) / 0.3), None, 52)
        for word, emo, x, y in (("dollars", "💵", 260, 820), ("weddings", "💍", 820, 820), ("land", "🏡", 540, 1150)):
            if t >= WT(10, word): paste_emoji(img, emo, x, y + math.sin(t * 4) * 8, 160 * pop((t - WT(10, word)) / 0.3))
        if t >= WT(10, "stones"): stone(img, 540, 620, 90, pop((t - WT(10, "stones")) / 0.3))
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
            if i in CLIPS: continue
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
