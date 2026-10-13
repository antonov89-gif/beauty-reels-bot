"""New Year first/last map Short (GeoGlobeTales style). python3 engine24.py still N.. | info | prefetch | video A B out.mp4"""
import json, math, subprocess, sys
import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import tiles
from script27 import LINES

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
    if n in ("Cook Is.",):
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



def kf(t, keys, logspan=False):
    if t <= keys[0][0]: return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            k = ease((t - t0) / max(1e-3, t1 - t0))
            out = [lerp(a, b, k) for a, b in zip(v0, v1)]
            if logspan: out[2] = math.exp(lerp(math.log(v0[2]), math.log(v1[2]), k))
            return tuple(out)
    return keys[-1][1]
SC = [0.0] + [ST[i] - 0.12 for i in range(1, len(LINES))] + [TOTAL + 1]
CUTS = SC[1:-1]
PAL = (-163.16, -18.05); RARO = (-159.78, -21.23); ENG = (-2.0, 52.0)
CLIPS = {5: "ai_1863.mp4", 6: "ai_1863.mp4", 10: "ai_date.mp4"}
_CF = {}
def clip_frame(name, t0, t1, t):
    if name not in _CF:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", name, "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        _CF[name] = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    fr = _CF[name]; n = len(fr)
    k = (t - t0) / max(0.1, t1 - t0)
    return Image.fromarray(fr[min(n - 1, max(0, int(k * (n - 1))))]).convert("RGBA")
def cam_for(i, t):
    a, b = SC[i], SC[i + 1]
    if i == 0: return kf(t, [(a, (-150, -12, 140)), (a + 1.2, (-158, -16, 60)), (WT(0, "Palmerston") - 0.2, (-163.16, -18.05, 0.6)), (b, (-163.16, -18.05, 0.32))], True)
    if i == 1: return kf(t, [(a, (-163.16, -18.05, 0.30)), (b, (-163.16, -18.05, 0.22))])
    if i == 2: return kf(t, [(a, (-162.2, -19.0, 10.0)), (b, (-161.6, -19.6, 7.5))])
    if i == 3: return kf(t, [(a, (-163.16, -18.05, 1.2)), (b, (-163.16, -18.05, 0.8))], True)
    if i == 4: return kf(t, [(a, (-95, 18, 260)), (b, (-100, 12, 230))])
    if i in (7, 8): return kf(t, [(a, (-163.165, -18.05, 0.20)), (b, (-163.165, -18.05, 0.17))])
    if i == 9: return kf(t, [(a, (-163.18, -18.03, 0.07)), (b, (-163.18, -18.03, 0.05))])
    return (-163.16, -18.05, 0.3)
def render(t, fi):
    i = max(j for j in range(len(LINES)) if SC[j] <= t) if t >= 0 else 0
    lt = t - SC[i]
    if i in CLIPS:
        t0 = SC[5] if i in (5, 6) else SC[10]; t1 = SC[7] if i in (5, 6) else SC[11] - 1.0
        img = clip_frame(CLIPS[i], t0, t1, t)
        if i == 5:
            if t >= WT(5, "wife"): badge(img, W / 2, 330, "WIFE #1", (200, 60, 120), pop((t - WT(5, "wife")) / 0.3), "💍", 56)
            if t >= WT(5, "cousins"): badge(img, W / 2, 470, "+2 COUSINS", (60, 120, 200), pop((t - WT(5, "cousins")) / 0.3), "🛶", 56)
        elif i == 6:
            big(img, "3 WIVES", t, SC[6] + 0.1, 360, 170, YEL); big(img, "1 ISLAND", t, WT(6, "one"), 560, 120, WHT)
        else:
            if t >= WT(10, "check"): big(img, "CHECK THE", t, WT(10, "check"), 300, 110, WHT); big(img, "FAMILY TREE", t, WT(10, "family"), 450, 130, YEL)
        return img
    lo, la, sp = cam_for(i, t)
    cam = tiles.Cam(lo, la, sp)
    img = grade(cam.render(), cam.src == "esri")
    d = ImageDraw.Draw(img)
    px, py = cam.xy(*PAL)
    if i == 0:
        if sp > 0.9: pulse(img, px, py, t, SC[0] + 0.3, YEL, 140); ring(img, px, py, 46, YEL, 1.0)
        if t >= WT(0, "Palmerston"): badge(img, W / 2, 330, "PALMERSTON ISLAND", (0, 120, 200), pop((t - WT(0, "Palmerston")) / 0.3), "🇨🇰", 56)
        big(img, "MIDDLE OF NOWHERE", t, WT(0, "middle"), 1180, 82, YEL) if t < WT(0, "zoom") + 0.6 else None
    elif i == 1:
        if t >= WT(1, "thirtyfive"): badge(img, W / 2, 330, "~35 PEOPLE", (30, 30, 30), pop((t - WT(1, "thirtyfive")) / 0.3), "👥", 60)
        if t >= WT(1, "Marsters") - 0.2:
            for q, (ox, oy) in enumerate(((-300, -150), (260, -260), (-200, 220), (300, 140), (0, -30), (-330, 420), (250, 480))):
                badge(img, W / 2 + ox, 960 + oy, "MARSTERS", (200, 60, 50), pop((t - WT(1, "Marsters") + 0.2 - q * 0.08) / 0.3), None, 40)
    elif i == 2:
        rx, ry = cam.xy(*RARO)
        k = ease((t - WT(2, "airport")) / 0.8)
        if k > 0:
            glow_line(img, partial([(px, py), (rx, ry)], k), WHT, 6, 0.6, dash=(24, 16), phase=t * 40)
        if t >= WT(2, "airport"): pin(img, rx, ry, "AIRPORT", (30, 30, 30), pop((t - WT(2, "airport") - 0.4) / 0.3), "✈️", False, 46)
        if t >= WT(2, "five"): badge(img, (px + rx) / 2 + 120, (py + ry) / 2, "~500 KM", YEL and (30, 30, 30), pop((t - WT(2, "five")) / 0.3), None, 50)
        ring(img, px, py, 40, YEL, 1.0)
        if t >= WT(2, "supply"):
            s = ease((t - WT(2, "supply")) / 2.4); paste_emoji(img, "🚢", lerp(rx, px, s), lerp(ry, py, s) - 30, 110)
        if t >= WT(2, "few"): badge(img, W / 2, 330, "A FEW TIMES A YEAR", (200, 60, 50), pop((t - WT(2, "few")) / 0.3), "🚢", 50)
    elif i == 3:
        big(img, "HOW?", t, WT(3, "how"), 560, 260, YEL)
        badge(img, W / 2, 1150, "ONE FAMILY = ONE ISLAND", (30, 30, 30), pop((t - WT(3, "family")) / 0.3), "🏝️", 48) if t >= WT(3, "family") else None
    elif i == 4:
        ex, ey = cam.xy(*ENG)
        pts = [(ex + (px - ex) * s, ey + (py - ey) * s - math.sin(math.pi * s) * 260) for s in np.linspace(0, 1, 40)]
        arrow(img, partial(pts, ease((t - WT(4, "Englishman")) / 1.4)), RED, 1.0, 16) if t >= WT(4, "Englishman") else None
        big(img, "1863", t, WT(4, "eighteen"), 330, 170, YEL)
        if t >= WT(4, "William"): pin(img, ex, ey, "WILLIAM MARSTERS", (30, 30, 30), pop((t - WT(4, "William")) / 0.3), "🇬🇧", True, 44)
        if t >= WT(4, "coconut"): paste_emoji(img, "🥥", px, py - 60, 120 * pop((t - WT(4, "coconut")) / 0.3))
    elif i in (7, 8):
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        cx, cy = W / 2, H / 2 - 40; R = 620
        cols = [(255, 200, 0), (0, 200, 140), (240, 90, 160)]
        k = ease((t - WT(7, "three")) / 0.8) if i == 7 else 1.0
        for q in range(3):
            if k > q / 3:
                dl.pieslice((cx - R, cy - R, cx + R, cy + R), -90 + q * 120, -90 + q * 120 + 120 * min(1, (k - q / 3) * 3), fill=cols[q] + (70,), outline=WHT + (230,), width=6)
        img.alpha_composite(lay)
        if k > 0.9:
            for q in range(3):
                ang = math.radians(-90 + q * 120 + 60)
                badge(img, cx + math.cos(ang) * 330, cy + math.sin(ang) * 330, f"BRANCH {q + 1}", (30, 30, 30), 1.0, None, 40)
        if i == 7 and t >= WT(7, "family"): paste_emoji(img, "👪", W / 2, 330, 150 * pop((t - WT(7, "family")) / 0.3))
        if i == 8:
            big(img, "ONE RULE", t, WT(8, "rule"), 300, 120, YEL)
            if t >= WT(8, "no"):
                badge(img, W / 2, 1180, "NO MARRYING INSIDE YOUR BRANCH", (200, 40, 40), pop((t - WT(8, "no")) / 0.3), "❌", 40)
    elif i == 9:
        for word, emo, x, y in (("fish", "🐟", 300, 700), ("farm", "🌴", 780, 760), ("ship", "🚢", 540, 1150)):
            if t >= WT(9, word): paste_emoji(img, emo, x, y + math.sin(t * 4) * 8, 150 * pop((t - WT(9, word)) / 0.3))
        if t >= WT(9, "descendants"): badge(img, W / 2, 330, "STILL HERE TODAY", (0, 120, 200), pop((t - WT(9, "descendants")) / 0.3), None, 52)
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
