"""Vertical Shorts cut from 'Vice City vs REAL Miami' (reuses the long video's voice and assets).
SHORT=s1|s2|s3 python3 engine53.py info | still t.. | video A B out.mp4"""
import math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import engine52 as E

W, H, FPS = 1080, 1920, 30
YEL, RED, WHT, BLK, PINK, CYAN, ORG, BLU = E.YEL, E.RED, E.WHT, E.BLK, E.PINK, E.CYAN, E.ORG, E.BLU
SHORT = os.environ.get("SHORT", "s1")
WT, ST, D = E.WT, E.ST, E.D
LINES_OF = {"s1": (8, 9), "s2": (11, 12), "s3": (17, 17)}
A, B = LINES_OF[SHORT]
OFF = ST[A] - 0.25                       # global time of local t = 0
TOTAL = ST[B] + D[B] + 1.2 - OFF
NF = int(TOTAL * FPS)
def L(g): return g - OFF                 # global -> local time

SH = []
def S(g0, kind, *args): SH.append([L(g0) if g0 > OFF else 0.0, kind, args, []])
def O(fn, *args, **kw): SH[-1][3].append((fn, args, kw))

if SHORT == "s1":
    HOOK = ("GTA 6 COPIED", "REAL MIAMI?")
    S(OFF, "clipbox", "V4", 0.0, 0.8)
    O("quote", "ROCKSTAR ON VC PORT", "THE CRUISE SHIP CAPITAL OF THE WORLD", WT(8, "capital") - 0.5)
    O("badge", "text", 540, 395, WT(8, "capital"))
    S(WT(8, "PortMiami") - 0.25, "split", "V4", 3.0, "PORT", 1.0, 0.6, 0.55, "VC PORT", "PORTMIAMI")
    O("big", "SAME SLOGAN!", 540, 1420, WT(8, "slogan") - 0.4, 84, YEL, BLK)
    S(WT(8, "satellite") - 0.35, "sat", "PORT", 1.0, 1.35, 0.62, 0.6)
    O("pinll", "PORT", -80.1625, 25.7745, "PORTMIAMI", WT(8, "island") - 0.2)
    O("big", "CRUISE CAPITAL", 540, 330, WT(8, "satellite") - 0.1, 90, WHT, PINK)
    O("big", "OF THE WORLD", 540, 440, WT(8, "satellite") + 0.1, 90, WHT, PINK)
    S(ST[9] - 0.15, "sat", "MAC", 1.0, 1.25, 0.55, 0.62)
    O("routell", "MAC", [(-80.1875, 25.7852), (-80.1760, 25.7855), (-80.1650, 25.7812), (-80.1520, 25.7776), (-80.1400, 25.7746)], WT(9, "MacArthur") - 0.2, 2.2)
    O("big", "MACARTHUR CAUSEWAY", 540, 330, WT(9, "MacArthur") - 0.2, 70, WHT, PINK)
    O("counter", 0, 3.5, "~{:.1f} MILES", 540, 450, WT(9, "three") - 0.1, 1.2, 70, YEL, BLK)
    O("big", "OPENED 1920", 540, 560, WT(9, "twenty") - 0.4, 64, WHT, BLU)
    S(WT(9, "road", 1) - 0.2, "clipbox", E.best("V5"), 0.0, 0.85)
    O("big", "TOWERS ON ONE END", 540, 1440, WT(9, "towers") - 0.2, 60, YEL, BLK)
    O("big", "BEACH ON THE OTHER", 540, 1530, WT(9, "beach") - 0.2, 60, YEL, BLK)
elif SHORT == "s2":
    HOOK = ("GTA 6 HID A", "2,000-YEAR-OLD SECRET")
    S(OFF, "sign", "TEQUESTA", "V6")
    O("badge", "sign", 540, 1330, WT(11, "official") - 0.1)
    S(WT(11, "Fans") - 0.2, "split", "V6", 2.0, "BRK", 1.0, 0.55, 0.45, "TEQUESTA", "BRICKELL")
    S(WT(11, "Tequesta", 1) - 0.35, "sat", "BRK", 1.0, 1.4, 0.62, 0.38)
    O("pinll", "BRK", -80.1893, 25.7698, "MIAMI RIVER MOUTH", WT(11, "mouth") - 0.3)
    O("big", "THE TEQUESTA PEOPLE", 540, 330, WT(11, "Tequesta", 1) - 0.1, 76, WHT, PINK)
    S(ST[12] - 0.15, "clipbox", "V7", 0.0, 0.7)
    O("big", "1998 · BRICKELL", 540, 1450, ST[12] + 0.1, 76, YEL, BLK)
    S(WT(12, "perfect") - 0.25, "sat", "CIRC", 1.0, 1.5, 0.563, 0.648)
    O("pinf", 0.563, 0.648, "THE MIAMI CIRCLE", WT(12, "perfect"))
    S(WT(12, "thirty") - 0.2, "circ")
    S(WT(12, "So") - 0.2, "clipbox", "V7", 4.0, 0.6)
    O("big", "NAMED AFTER THE TEQUESTA", 540, 1450, WT(12, "named") - 0.3, 66, YEL, PINK)
else:
    HOOK = ("THIS GTA 6 MARKET", "IS A REAL CITY")
    S(OFF, "clipbox", "V11", 0.0, 0.7)
    O("quote", "ROCKSTAR'S OWN COPY", "THE TISHA-WOCKA FLEA MARKET AND ITS BOOTLEG BRANDS", WT(17, "mentions") - 0.2)
    O("badge", "text", 540, 395, WT(17, "bootleg"))
    S(WT(17, "Say") - 0.2, "clipbox", "V10", 0.0, 0.5)
    O("big", "TISHA-WOCKA", 540, 1440, WT(17, "Say") - 0.1, 96, WHT, PINK)
    O("big", "= OPA-LOCKA", 540, 1545, WT(17, "Opa-locka") - 0.2, 96, YEL, BLK)
    S(WT(17, "small") - 0.6, "split", "V10", 2.0, "OPA", 1.0, 0.47, 0.5, "TISHA-WOCKA", "OPA-LOCKA")
    S(WT(17, "founded") - 0.3, "clipbox", "V10", 3.0, 0.65)
    O("big", "1926 · GLENN CURTISS", 540, 1450, WT(17, "founded") - 0.1, 64, YEL, BLK)
    O("tags", [("DOMES", WT(17, "domes") - 0.1), ("MINARETS", WT(17, "minarets") - 0.1), ("ARCHES", WT(17, "arches") - 0.1)])
    S(WT(17, "City", 1) - 0.25, "sat", "OPA", 1.0, 1.3, 0.5, 0.5)
    O("pinf", 0.47, 0.5, "OPA-LOCKA", WT(17, "City", 1))
    O("big", "A CITY HALL", 540, 330, WT(17, "City", 1) - 0.1, 84, WHT, PINK)
    O("big", "LIKE A PALACE", 540, 440, WT(17, "City", 1) + 0.1, 84, WHT, PINK)
    O("big", "~20 BUILDINGS ON THE NATIONAL REGISTER", 540, 560, WT(17, "twenty") - 0.2, 46, YEL, BLK)
    S(WT(17, "flea", 1) - 0.4, "clipbox", "V11", 4.0, 0.7)
    O("big", "A REAL FLEA MARKET TOO", 540, 1450, WT(17, "flea", 1) - 0.2, 64, YEL, BLK)
CUTS = [s[0] for s in SH[1:]]
SPLITS = [s[0] for s in SH if s[1] == "split"]


def scene_t(i): return SH[i][0], (SH[i + 1][0] if i + 1 < len(SH) else TOTAL)


def shot_at(t):
    for k in range(len(SH) - 1, -1, -1):
        if t >= SH[k][0]: return k
    return 0


def ease(x): return E.ease(x)


def gt(t): return t + OFF               # local -> global (for word anchors already converted, overlays use global)


# ------------------------------------------------------------------ helpers (vertical sizes)
def clip_panel(name, s0, rate, t, t0, t1, w, h, z0=1.0, z1=1.08):
    u = (t - t0) / max(0.1, t1 - t0); im, _ = E.view(E.clip_frame(name, s0 + (t - t0) * rate), z0 + (z1 - z0) * ease(u), 0.5, 0.5, w, h); return im


def sat_panel(key, z0, z1, cx, cy, t, t0, t1, w, h):
    u = (t - t0) / max(0.1, t1 - t0); return E.view(E.sat(key), z0 + (z1 - z0) * ease(u), cx, cy, w, h)


_BG = {}
def blurbg(name, sec):
    k = (name, round(sec * 4) / 4)
    if k not in _BG:
        if len(_BG) > 6: _BG.clear()
        im, _ = E.view(E.clip_frame(name, k[1]), 1.0, 0.5, 0.5, W, H)
        _BG[k] = Image.eval(im.filter(ImageFilter.GaussianBlur(22)), lambda v: int(v * 0.42)).convert("RGBA")
    return _BG[k].copy()


def route(img, pts, t, t0, dur=1.6, col=CYAN, width=10):
    if t < t0 or len(pts) < 2: return
    k = ease((t - t0) / dur); Ls = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(Ls) * k; out = [pts[0]]
    for i, l in enumerate(Ls):
        if tot <= 0: break
        u = min(1.0, tot / l); out.append((pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u)); tot -= l
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).line(out, fill=col + (200,), width=width * 3, joint="curve")
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(img); d.line(out, fill=WHT + (255,), width=width, joint="curve"); d.line(out, fill=col + (255,), width=max(3, width - 4), joint="curve")


def quote(img, lead, txt, t, t0, y=1375):
    if t < t0: return
    k = ease((t - t0) / 0.3); f = E.font(E.POPX, 50); f2 = E.font(E.POPB, 26); lines = []; cur = ""
    for w in txt.split():
        if f.getlength(cur + " " + w) > 900 and cur: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur); h = 70 + 62 * len(lines); x0 = 60 + (1 - k) * 60
    d = ImageDraw.Draw(img); d.rounded_rectangle((x0, y, x0 + 960, y + h), 18, fill=(10, 8, 24, int(215 * k))); d.rectangle((x0, y, x0 + 10, y + h), fill=PINK + (int(255 * k),))
    d.text((x0 + 36, y + 34), lead, font=f2, fill=PINK + (int(255 * k),), anchor="lm")
    for q, l in enumerate(lines): d.text((x0 + 36, y + 82 + q * 62), l, font=f, fill=WHT + (int(255 * k),), anchor="lm")


def credit(img, y=None):
    ImageDraw.Draw(img).text((W - 20, y or H - 14), "Imagery © Esri, Maxar, Earthstar Geographics", font=E.font(E.POPB, 16), fill=(255, 255, 255, 170), anchor="rs")


# ------------------------------------------------------------------ scenes
PANEL = (330, 1350)                      # clipbox: y range of the sharp clip panel


def clipbox(t, k):
    t0, t1 = scene_t(k); name, s0, rate = SH[k][2]; img = blurbg(name, s0 + (t - t0) * rate)
    y0, y1 = PANEL; p = clip_panel(name, s0, rate, t, t0, t1, W, y1 - y0).convert("RGBA")
    img.paste(p, (0, y0)); d = ImageDraw.Draw(img); d.rectangle((0, y0 - 6, W, y0), fill=PINK + (255,)); d.rectangle((0, y1, W, y1 + 6), fill=PINK + (255,))
    E.pill(img, "AI CONCEPT · NOT GAME FOOTAGE", 540, y1 - 40, 20, (40, 40, 50))
    return img


def split(t, k):
    t0, t1 = scene_t(k); name, s0, key, z, cx, cy, left, right = SH[k][2]; sl = ease((t - t0) / 0.35)
    img = Image.new("RGBA", (W, H), (8, 6, 20, 255)); top = clip_panel(name, s0, 0.7, t, t0, t1, W, 950).convert("RGBA")
    bot, m = sat_panel(key, z, z * 1.25, cx, cy, t, t0, t1, W, 950)
    img.paste(top, (int(-W * (1 - sl)), 0)); img.paste(bot.convert("RGBA"), (int(W * (1 - sl)), 970))
    d = ImageDraw.Draw(img); d.rectangle((0, 950, W, 970), fill=PINK + (255,))
    E.pill(img, "IN THE GAME", 540, 200, 26, (20, 20, 40), a=sl); E.label(img, left, 540, 290, t, t0 + 0.2, 80, WHT, PINK, maxw=980)
    E.pill(img, "REAL MIAMI", 540, 1060, 26, (20, 20, 40), a=sl); E.label(img, right, 540, 1150, t, t0 + 0.35, 84, YEL, BLK, maxw=980)
    E.pill(img, "AI CONCEPT · NOT GAME FOOTAGE", 540, 905, 20, (40, 40, 50), a=sl)
    if t > t0 + 0.3:
        sv = ease((t - t0 - 0.3) / 0.2); r = 70 * (1.6 - 0.6 * sv)
        d.ellipse((540 - r, 960 - r, 540 + r, 960 + r), fill=(15, 10, 30, 255), outline=WHT + (255,), width=5)
        E.glow_text(img, (540, 960), "VS", E.font(E.TITAN, int(r * 0.95)), YEL, 1.0, "mm", PINK)
    credit(img); return img


def sat_full(t, k):
    t0, t1 = scene_t(k); key, z0, z1, cx, cy = SH[k][2]; im, m = sat_panel(key, z0, z1, cx, cy, t, t0, t1, W, H)
    img = im.convert("RGBA"); credit(img); return img


def sign(t, k):
    t0, t1 = scene_t(k); text, bg = SH[k][2]; img = blurbg(bg, t - t0)
    sc = ease((t - t0) / 0.35); w, h = 960 * (0.85 + 0.15 * sc), 330 * (0.85 + 0.15 * sc); x0, y0 = 540 - w / 2, 900 - h / 2
    d = ImageDraw.Draw(img)
    for x in (540 - 250, 540 + 250): d.line((x, y0 + h, x, H), fill=(120, 120, 130, 255), width=24)
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 30, fill=(0, 112, 60, 255), outline=WHT + (255,), width=10)
    d.ellipse((x0 + 34, y0 + h / 2 - 70, x0 + 174, y0 + h / 2 + 70), fill=WHT, outline=BLK, width=6)
    d.text((x0 + 104, y0 + h / 2), "3", font=E.font(E.POPX, 80), fill=BLK, anchor="mm")
    d.text((540 + 80, y0 + h / 2), text, font=E.fit(E.POPX, 110, text, w - 260), fill=WHT, anchor="mm")
    E.pill(img, "SIGN RECREATED FOR THIS VIDEO", 540, 1240, 20, (40, 40, 50))
    return img


def circ(t, k):
    t0, t1 = scene_t(k); im, _ = E.view(E.sat("CIRC"), 2.2, 0.563, 0.648, W, H)
    img = Image.eval(im.filter(ImageFilter.GaussianBlur(3)), lambda v: int(v * 0.4)).convert("RGBA"); d = ImageDraw.Draw(img)
    cx, cy, R = 540, 900, 330; u = ease((t - t0) / 1.0)
    d.arc((cx - R, cy - R, cx + R, cy + R), -90, -90 + 360 * u, fill=YEL + (255,), width=9)
    th = WT(12, "twenty") - 0.2 - OFF; nh = int(min(24, max(0, (t - th) / 0.07))) if t > th else 0
    for q in range(nh):
        a = -math.pi / 2 + q * 2 * math.pi / 24; x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=(30, 20, 10, 255), outline=ORG + (255,), width=4)
    E.label(img, "THE MIAMI CIRCLE", 540, 330, t, WT(12, "called") - 0.3 - OFF, 80, WHT, PINK, maxw=980)
    E.counter(img, 0, 24, "{:.0f} HOLES", 540, 900, t, th, 24 * 0.07, 90, ORG, BLK)
    E.label(img, "38 FT ACROSS", 540, 1300, t, t0 + 0.5, 64, WHT, BLK, maxw=980)
    E.label(img, "UP TO ~2,000 YEARS OLD", 540, 450, t, WT(12, "two") - 0.3 - OFF, 58, YEL, BLK, maxw=980)
    E.label(img, "NATIONAL HISTORIC LANDMARK", 540, 1400, t, WT(12, "Landmark") - 0.5 - OFF, 48, WHT, BLU, maxw=980)
    return img


def base(k, t):
    return {"clipbox": clipbox, "split": split, "sat": sat_full, "sign": sign, "circ": circ}[SH[k][1]](t, k)


def sat_map(k, t):
    t0, t1 = scene_t(k); key, z0, z1, cx, cy = SH[k][2]; _, m = sat_panel(key, z0, z1, cx, cy, t, t0, t1, W, H); return key, m


def overlays(img, t, k):
    for fn, args, kw in SH[k][3]:
        a = list(args)
        if fn == "big": txt, x, y, ts, size, col, glow = a; E.label(img, txt, x, y, t, ts - OFF, size, col, glow, maxw=1000)
        elif fn == "badge": E.badge(img, a[0], a[1], a[2], t, a[3] - OFF, 28)
        elif fn == "counter": E.counter(img, a[0], a[1], a[2], a[3], a[4], t, a[5] - OFF, a[6], a[7], a[8], a[9])
        elif fn == "quote": quote(img, a[0], a[1], t, a[2] - OFF)
        elif fn == "tags": E.tags(img, [(x, ts - OFF) for x, ts in a[0]], t, x=60, y0=470, dy=84, size=44)
        elif fn == "pinll":
            key, lon, lat, txt, ts = a; _, m = sat_map(k, t); fx, fy = E.geo(key, lon, lat); E.pin(img, *E.to_screen(m, fx, fy, key), txt, t, ts - OFF, side=-1 if E.to_screen(m, fx, fy, key)[0] > 600 else 1)
        elif fn == "pinf":
            fx, fy, txt, ts = a; key, m = sat_map(k, t); X, Y = E.to_screen(m, fx, fy, key); E.pin(img, X, Y, txt, t, ts - OFF, side=-1 if X > 600 else 1)
        elif fn == "routell":
            key, pts, ts, dur = a[:4]; _, m = sat_map(k, t); route(img, [E.to_screen(m, *E.geo(key, lo, la), key) for lo, la in pts], t, ts - OFF, dur)


def hook(img, t):
    if t > 3.2 and t < TOTAL - 2.6:
        top, bot = HOOK; d = ImageDraw.Draw(img)            # small persistent title band once the hook is done
        d.rounded_rectangle((70, 70, 1010, 150), 22, fill=(8, 8, 20, 190), outline=PINK + (255,), width=3)
        d.text((540, 110), f"{top} {bot}", font=E.fit(E.POPX, 34, f"{top} {bot}", 900), fill=WHT, anchor="mm"); return
    if t <= 3.2:
        a, b = HOOK
        E.grad_title(img, a, 540, 175 if SH[shot_at(t)][1] != "split" else 470, 105, t, 0.0, maxw=1000)
        E.grad_title(img, b, 540, 300 if SH[shot_at(t)][1] != "split" else 610, 105, t, 0.25, maxw=1000)
    else:
        E.grad_title(img, "FULL VIDEO", 540, 760, 120, t, TOTAL - 2.6, maxw=1000)
        E.label(img, "VICE CITY vs REAL MIAMI · 8 MIN", 540, 900, t, TOTAL - 2.3, 56, YEL, BLK, maxw=1000)


def caption(img, t):
    g = t + OFF
    for i in range(A, B + 1):
        if ST[i] - 0.05 <= g < ST[i] + D[i] + 0.15:
            words = E.LINES[i].split(); cur = 0
            for j, o in enumerate(E.TW[i]):
                if g >= ST[i] + o - 0.05: cur = j
            c0 = cur // 3 * 3; txt = " ".join(words[c0:c0 + 3]); f = E.fit(E.POPX, 68, txt, 960)
            E.glow_text(img, (540, 1640), txt, f, WHT, 1.0, "mm", None, 4); return


YY, XX = np.mgrid[0:H, 0:W]
VIG = (1 - 0.30 * (((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2) / 2).astype(np.float32)[..., None]
del YY, XX
SHAKES = [s + 0.3 for s in SPLITS]


def post(img, t):
    a = np.asarray(img.convert("RGB")).astype(np.float32); sk = 0.0
    for s in SHAKES:
        if 0 <= t - s < 0.3: sk = max(sk, 14 * (1 - (t - s) / 0.3))
    dx = int(sk * math.sin(t * 90)); dy = int(sk * math.cos(t * 77))
    if dx or dy: a = np.roll(a, (dy, dx), axis=(0, 1))
    a = (a * VIG - 128) * 1.06 + 128 + np.array([4, 0, 6], np.float32)
    rng = np.random.default_rng(int(t * 30) % 997); g = rng.normal(0, 4.5, (H // 2, W // 2)).astype(np.float32)
    a += np.repeat(np.repeat(g, 2, 0), 2, 1)[..., None]
    cut = min([abs(t - c) for c in CUTS] + [9])
    if cut < 0.1: a += 55 * (1 - cut / 0.1) * np.array([1.0, 0.75, 0.9], np.float32)
    return np.clip(a, 0, 255).astype(np.uint8)


def frame(fi):
    t = fi / FPS; k = shot_at(t); img = base(k, t)
    if k > 0 and t - SH[k][0] < 0.12: img = E.whip(base(k - 1, t), img, (t - SH[k][0]) / 0.12)
    overlays(img, t, k); hook(img, t); caption(img, t)
    a = post(img, t)
    if t > TOTAL - 0.4: a = (a * max(0.0, (TOTAL - t) / 0.4)).astype(np.uint8)
    return Image.fromarray(a)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print(SHORT, "frames", NF, "total", round(TOTAL, 2), "off", round(OFF, 2))
        for i, s in enumerate(SH): print(i, round(s[0], 2), round(scene_t(i)[1] - s[0], 2), s[1], s[2][:1])
    elif cmd == "still":
        os.makedirs("stills53", exist_ok=True)
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills53/{SHORT}_{float(a):05.1f}.jpg", quality=86)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(fi).tobytes())
        p.stdin.close(); p.wait()
