"""Hormuz bypass long-form 16:9 map video. python3 engine28.py still N.. | info | prefetch | video A B out.mp4"""
import json, math, os, subprocess, sys
import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import tiles
from script28 import S, LINES

W, H, FPS = 1920, 1080, 30
POP, POPX = "Poppins-Bold.ttf", "Poppins-ExtraBold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (60, 200, 90), (60, 140, 255), (255, 255, 255), (0, 0, 0)
GOLD, ORG, NAVY = (255, 190, 60), (255, 140, 30), (10, 24, 48)
TM = json.load(open("timing.json")); D, TW = TM["D"], TM["T"]
LEAD = 0.4
ST = [LEAD + s for s in TM["starts"]]
TOTAL = ST[-1] + D[-1] + 1.6
NF = int(TOTAL * FPS)
N = len(S)


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def pop(x):
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    return 1.15 * ease(x / 0.6) if x < 0.6 else 1.15 - 0.15 * ease((x - 0.6) / 0.4)


exec(open("helpers_raw.py").read())

_R = shapefile.Reader("/home/claude/v15/assets/ne50/ne_50m_admin_0_countries.shp")
_FL = [x[0] for x in _R.fields[1:]]
COUNTRY = {}
for rec, shp in zip(_R.records(), _R.shapes()):
    n = rec[_FL.index("NAME")]
    if n in ("United Arab Emirates", "Saudi Arabia", "Iran", "Oman", "China", "India", "Japan", "South Korea"):
        pts, parts = shp.points, list(shp.parts) + [len(shp.points)]
        COUNTRY[n] = [pts[a:b] for a, b in zip(parts, parts[1:])]

P = {"hormuz": (56.35, 26.55, "STRAIT OF HORMUZ", RED), "fujairah": (56.35, 25.13, "FUJAIRAH", (0, 120, 200)),
     "habshan": (53.63, 23.77, "HABSHAN", (200, 120, 0)), "jebel": (55.03, 25.0, "JEBEL ALI", (30, 30, 30)),
     "dubai": (55.27, 25.2, "DUBAI", (30, 30, 30)), "khor": (56.36, 25.36, "KHOR FAKKAN", (0, 120, 200)),
     "ruwais": (52.73, 24.11, "RUWAIS", (30, 30, 30)), "khalifa": (54.65, 24.8, "KHALIFA PORT", (30, 30, 30)),
     "icad": (54.47, 24.35, "ICAD ABU DHABI", (200, 60, 50)), "sohar": (56.75, 24.45, "SOHAR", (0, 120, 200)),
     "duqm": (57.7, 19.67, "DUQM", (0, 120, 200)), "hajar": (56.15, 24.95, "HAJAR MTS", (110, 80, 40)),
     "saudi": (49.67, 25.93, "ABQAIQ", (30, 30, 30)), "yanbu": (38.06, 24.09, "YANBU (RED SEA)", (0, 120, 200)),
     "jask": (57.77, 25.65, "JASK (IRAN)", (30, 30, 30))}
SPOT_ONLY = {"uae", "gulf", "lanes", "gulfcoast", "eastcoast", "asia", "hajar"}
ROUTES = {
    "pipe": [[(53.63, 23.77), (54.4, 24.05), (55.1, 24.4), (55.75, 24.8), (56.35, 25.13)]],
    "pipe2": [[(53.63, 23.77), (54.4, 24.05), (55.1, 24.4), (55.75, 24.8), (56.35, 25.13)],
              [(53.63, 23.80), (54.4, 24.10), (55.1, 24.46), (55.75, 24.86), (56.33, 25.17)]],
    "crow": [[(55.27, 25.2), (56.35, 25.13)]],
    "rail": [[(52.73, 24.11), (53.6, 24.3), (54.47, 24.35), (54.65, 24.8), (55.03, 25.0), (55.5, 25.25), (56.0, 25.2), (56.35, 25.13)]],
    "rail2": [[(54.47, 24.35), (55.2, 24.75), (55.9, 25.0), (56.35, 25.13)]],
    "saudi": [[(49.67, 25.93), (44.0, 24.9), (38.06, 24.09)]],
    "asia": [[(56.35, 26.55), (68, 20), (78, 15)], [(56.35, 26.55), (80, 28), (105, 32)], [(56.35, 26.55), (85, 5), (125, 28), (139, 36)]],
}
ROUTES["all"] = ROUTES["pipe"] + ROUTES["rail2"]
LANES = [[(56.62, 26.18), (56.45, 26.47), (56.18, 26.62), (55.9, 26.72)], [(56.55, 26.12), (56.38, 26.40), (56.12, 26.56), (55.85, 26.66)]]
HLC = {"uae": ["United Arab Emirates"], "saudi": ["Saudi Arabia"], "asia": ["China", "India", "Japan", "South Korea"], "gulfcoast": ["United Arab Emirates"]}


def ipath(cam, pts):
    return [cam.xy(lo, la) for lo, la in pts]


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
                    seg = [(a[0] + (b[0] - a[0]) * s0 / L, a[1] + (b[1] - a[1]) * s0 / L), (a[0] + (b[0] - a[0]) * e / L, a[1] + (b[1] - a[1]) * e / L)]
                    d.line(seg, fill=(0, 0, 0, 255), width=width + 6); d.line(seg, fill=color + (255,), width=width)
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


def smooth(pts, n=12):
    if len(pts) < 3: return pts
    out = []
    for i in range(len(pts) - 1):
        p0 = pts[max(0, i - 1)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(len(pts) - 1, i + 2)]
        for s in range(n):
            t = s / n
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t * t + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t ** 3) for k in range(2)))
    out.append(pts[-1]); return out


def hl_country(img, cam, names, color, alpha):
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for nm in names:
        for ring in COUNTRY.get(nm, []):
            p = ipath(cam, ring); xs = [q[0] for q in p]; ys = [q[1] for q in p]
            if max(xs) < -50 or min(xs) > W + 50 or max(ys) < -50 or min(ys) > H + 50 or len(p) < 3: continue
            d.polygon(p, fill=color + (int(255 * alpha),)); d.line(p + [p[0]], fill=WHT + (230,), width=4)
    img.alpha_composite(lay)


def pin(img, x, y, txt, color, k, up=True, size=44):
    if k <= 0: return
    d = ImageDraw.Draw(img); r = 11 * k
    d.ellipse((x - r - 4, y - r - 4, x + r + 4, y + r + 4), fill=WHT); d.ellipse((x - r, y - r, x + r, y + r), fill=color)
    ly = y - 70 * k if up else y + 70 * k
    d.line([(x, y), (x, ly)], fill=WHT, width=4)
    badge(img, x, ly + (-24 if up else 24) * k, txt, color, k, None, size)


def pulse(img, x, y, t, t0, color=YEL, r=90):
    if t < t0: return
    d = ImageDraw.Draw(img)
    for q in range(2):
        ph = ((t - t0) * 0.8 + q * 0.5) % 1.0
        d.ellipse((x - r * ph, y - r * ph, x + r * ph, y + r * ph), outline=color + (int(220 * (1 - ph)),), width=5)


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


SC = [0.0] + [ST[i] - 0.1 for i in range(1, N)] + [TOTAL + 1]
CUTS = [c for i, c in enumerate(SC[1:-1], 1) if S[i][1]["t"] == "map" and S[i - 1][1]["t"] == "map"]


def cam_for(i, t):
    a, b = SC[i], SC[i + 1]; sc = S[i][1]
    lo, la, z = sc["lon"], sc["lat"], sc["z"]
    k = ease((t - a) / max(1.0, b - a))
    if i == 0:
        kk = ease((t - a - 5.3) / 4.5); zz = math.exp(lerp(math.log(z * 5), math.log(z), kk)); return lo, la, zz
    dur = b - a; mk = [m for m in sc.get("mark", []) if m in P]
    if dur > 7.5 and mk and not sc.get("route") and mk[-1] != "hormuz":
        tx, ty = P[mk[-1]][0], P[mk[-1]][1]
        k1 = ease((t - a) / (dur * 0.5)); k2 = ease((t - a - dur * 0.55) / 2.5)
        zz = math.exp(lerp(math.log(z * 1.15), math.log(z), k1)); zz = math.exp(lerp(math.log(zz), math.log(z * 0.62), k2))
        return lerp(lo, lerp(lo, tx, 0.6), k2), lerp(la, lerp(la, ty, 0.6), k2), zz
    zz = math.exp(lerp(math.log(z * 1.18), math.log(z * 0.94), k))
    return lo + 0.02 * z * (k - 0.5), la, zz


def label_banner(img, text, k):
    if k <= 0: return
    f = font(POPX, 46); d = ImageDraw.Draw(img); tw = f.getlength(text)
    x0, y0 = 60 - (1 - ease(k)) * 600, 56; w = tw + 76; h = 86
    d.rounded_rectangle((x0 + 5, y0 + 7, x0 + w + 5, y0 + h + 7), 18, fill=(0, 0, 0, 120))
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 18, fill=(12, 20, 38, 235), outline=WHT, width=4)
    d.rectangle((x0 + 14, y0 + 14, x0 + 26, y0 + h - 14), fill=YEL)
    d.text((x0 + 48, y0 + h / 2 + 2), text, font=f, fill=WHT, anchor="lm")


def bg_dark(t):
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]; xx = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
    base = np.array([10, 24, 48], np.float32) * (1 - 0.45 * yy) + np.array([20, 50, 90], np.float32) * 0.35 * (1 - ((xx - 0.5) ** 2 + (yy - 0.45) ** 2) * 2)
    im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert("RGBA"); d = ImageDraw.Draw(im)
    off = (t * 20) % 80
    for x in range(-80, W + 80, 80): d.line([(x + off, 0), (x + off, H)], fill=(255, 255, 255, 12), width=2)
    for y in range(-80, H + 80, 80): d.line([(0, y + off), (W, y + off)], fill=(255, 255, 255, 12), width=2)
    return im


def scene_count(i, t, lt):
    sc = S[i][1]; img = bg_dark(t); d = ImageDraw.Draw(img)
    k = ease((lt - 0.3) / 1.8); v = sc["value"] * k if sc["value"] > 10 or sc.get("dec") else sc["value"]
    s = (f"{v:.{sc.get('dec', 0)}f}" if sc.get("dec") else f"{int(round(v)):,}")
    txt = sc["fmt"].replace("{:,}", s).replace("{:.1f}", s)
    col = RED if sc.get("down") else YEL
    f = font(POPX, 150); 
    while f.getlength(txt) > W - 160: f = font(POPX, f.size * 0.92)
    sl = 1.0 + 0.04 * math.sin(lt * 3)
    if "ships" in sc["fmt"]:
        if sc.get("down"):
            gone = ease((lt - 0.8) / 2.0)
            for q in range(19):
                x, y = 330 + (q % 10) * 140, 190 + (q // 10) * 130
                if q < 2: paste_emoji(img, "🚢", x, y, 100)
                elif gone < 1: paste_emoji(img, "🚢", x, y + gone * 400 * (0.5 + (q % 3) * 0.3), 100 * (1 - gone))
        else:
            nshow = max(1, int(round(v / 5)))
            for q in range(nshow): paste_emoji(img, "🚢", 330 + (q % 10) * 140, 190 + (q // 10) * 130, 100 * pop((lt - 0.2 - q * 0.04) / 0.25))
    text_stroke(d, (W / 2, H / 2 + 120), txt, f, col, stroke=10)
    text_stroke(d, (W / 2, H / 2 + 260), sc["sub"].upper(), font(POP, 46), WHT, stroke=5)
    return img


def scene_bar(i, t, lt):
    sc = S[i][1]; img = bg_dark(t); d = ImageDraw.Draw(img)
    def hgt(v): return (math.log10(v) / math.log10(max(sc["a"], sc["b"])) if sc.get("log") else v / max(sc["a"], sc["b"]))
    base = H - 230; mx = 560
    for q, (v, lab, col) in enumerate(((sc["a"], sc["la"], RED), (sc["b"], sc["lb"], GRN))):
        k = ease((lt - 0.4 - q * 0.6) / 1.2); h = max(8, hgt(v) * mx * k) if k > 0 else 0
        cx = W / 2 + (-330 if q == 0 else 330)
        if h > 0:
            d.rounded_rectangle((cx - 150, base - h, cx + 150, base), 18, fill=col + (255,), outline=WHT, width=5)
            vt = (f"{int(v):,}" if v >= 1 else f"{v}") 
            text_stroke(d, (cx, base - h - 48), vt, font(POPX, 64), WHT, stroke=6)
        text_stroke(d, (cx, base + 62), lab, font(POP, 40), WHT, stroke=5)
    if sc.get("unit"): text_stroke(d, (W / 2, 120), sc["unit"], font(POPX, 54), YEL, stroke=6)
    return img


def scene_card(i, t, lt):
    sc = S[i][1]; img = bg_dark(t); d = ImageDraw.Draw(img)
    n = len(sc["lines"]); y0 = H / 2 - (n - 1) * 110
    for q, ln in enumerate(sc["lines"]):
        k = pop((lt - 0.4 - q * 0.7) / 0.35)
        if k <= 0: continue
        col = YEL if q != n - 1 or n < 3 else RED
        f = font(POPX, 110 * k)
        while f.getlength(ln) > W - 160: f = font(POPX, f.size * 0.92)
        text_stroke(d, (W / 2, y0 + q * 220), ln, f, WHT if q % 2 else YEL, stroke=9)
    return img


_CI = {}
def clip_img(name, k):
    import os
    n = len(os.listdir(f"clips/{name}")); idx = min(n, max(1, int(k * 30) + 1))
    return Image.open(f"clips/{name}/{idx:04d}.jpg").convert("RGBA")


def base_render(i, t, lt, sc):
    if sc["t"] in ("count", "bar", "card"):
        img = {"count": scene_count, "bar": scene_bar, "card": scene_card}[sc["t"]](i, t, lt)
        screen_anim(img, i, t, lt); return img
    return render_map(i, t, lt, sc)


def render(t, fi):
    i = max(j for j in range(N) if SC[j] <= t) if t >= 0 else 0
    lt = t - SC[i]; sc = S[i][1]
    if "clip" in sc:
        cn, f0 = sc["clip"][0], sc["clip"][1]; f1 = sc["clip"][2] if len(sc["clip"]) > 2 else 1.0
        ts = SC[i] + (SC[i + 1] - SC[i]) * f0; te = SC[i] + (SC[i + 1] - SC[i]) * f1
        if ts <= t < te + (0.0 if f1 >= 1.0 else 0.4):
            nfr = len(os.listdir(f"clips/{cn}")); rate = min(1.0, max(0.55, nfr / 30 / max(0.5, te - ts)))
            im = clip_img(cn, (t - ts) * rate)
            z = 1.0 + 0.05 * ease((t - ts) / 8.0)
            im = im.resize((int(W * z), int(H * z)), Image.BILINEAR).crop((int(W * (z - 1) / 2), int(H * (z - 1) / 2), int(W * (z - 1) / 2) + W, int(H * (z - 1) / 2) + H))
            a = 1.0 if f0 == 0.0 else ease((t - ts) / 0.4)
            if f1 < 1.0 and t > te: a = 1 - ease((t - te) / 0.4)
            if a < 1: im = Image.blend(base_render(i, t, lt, sc), im, a)
            label_banner(im, "AI-GENERATED ILLUSTRATION" if cn.startswith("ai_") else "ILLUSTRATIVE STOCK FOOTAGE", 1)
            screen_anim(im, i, t, lt, True)
            return im
    return base_render(i, t, lt, sc)


def render_map(i, t, lt, sc):
    lo, la, z = cam_for(i, t)
    cam = tiles.Cam(lo, la, z)
    img = grade(cam.render(), cam.src == "esri")
    for tag, nm in HLC.items():
        if tag in sc["mark"]: hl_country(img, cam, nm, (255, 200, 0) if tag != "asia" else (255, 120, 60), 0.28 * ease(lt / 1.0))
    if "lanes" in sc["mark"]:
        for q, ln in enumerate(LANES): glow_line(img, partial(smooth(ipath(cam, ln)), ease((lt - 0.4 - q * 0.4) / 1.4)), WHT, 7, 0.6, dash=(30, 18), phase=t * 50)
    if "gulfcoast" in sc["mark"] and lt > 1.0:
        dd = ImageDraw.Draw(img); f = font(POPX, 52)
        x, y = cam.xy(54.6, 25.25); text_stroke(dd, (x, y), "INSIDE THE GULF", f, RED, stroke=7)
        x, y = cam.xy(57.0, 25.0); text_stroke(dd, (x, y), "OUTSIDE", f, GRN, stroke=7) if lt > 2.0 else None
    if "gulf" in sc["mark"]:
        cx, cy = cam.xy(51.5, 27.0); f = font(POPX, 80)
        text_stroke(ImageDraw.Draw(img), (cx, cy), "PERSIAN GULF", f, WHT, stroke=7)
    q = 0
    for key in sc["mark"]:
        if key in P:
            x, y = cam.xy(P[key][0], P[key][1])
            if key == "hormuz": pulse(img, x, y, t, SC[i] + 0.5, RED, 100)
            pin(img, x, y, P[key][2], P[key][3], pop((lt - 0.5 - q * 0.35) / 0.3), up=(key not in ("khalifa", "icad", "dubai", "ruwais")), size=44)
            q += 1
    rt = sc.get("route")
    if rt:
        for ri, r in enumerate(ROUTES[rt]):
            col = {"pipe": ORG, "pipe2": ORG, "crow": WHT, "rail": (90, 220, 255), "rail2": (90, 220, 255), "saudi": ORG, "asia": RED, "all": ORG}[rt]
            if rt == "all" and ri == 1: col = (90, 220, 255)
            dur = min(3.5, max(1.5, (SC[i + 1] - SC[i]) * 0.5)); kk = ease((lt - 0.9) / dur)
            pts = smooth(ipath(cam, r)) if rt == "asia" else ipath(cam, r)
            if rt == "asia": arrow(img, partial(pts, kk), col, 1.0, 12) if kk > 0 else None
            else: glow_line(img, partial(pts, kk), col, 10, 0.8, dash=(26, 16) if rt in ("pipe", "pipe2", "all") else None, phase=t * 60)
    map_anim(img, cam, i, t, lt)
    if sc.get("label"): label_banner(img, sc["label"], (lt - 0.1) / 0.5)
    if rt and rt not in ("crow", "asia"):
        ImageDraw.Draw(img).text((W - 40, H - 150), "Routes simplified", font=font(POP, 26), fill=(255, 255, 255, 200), anchor="rm", stroke_width=3, stroke_fill=BLK)
    return img


def caption(img, t):
    for i in range(N):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.15:
            words = LINES[i].split(); cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05: cur = j
            c0 = cur // 5 * 5; chunk = words[c0:c0 + 5]
            f = font(POPX, 46); gap = f.getlength(" ") * 1.4
            ws = [f.getlength(w) for w in chunk]; tot = sum(ws) + gap * (len(chunk) - 1)
            if tot > W - 120:
                f = font(POPX, 46 * (W - 120) / tot); gap = f.getlength(" ") * 1.4
                ws = [f.getlength(w) for w in chunk]; tot = sum(ws) + gap * (len(chunk) - 1)
            x = (W - tot) / 2; d = ImageDraw.Draw(img)
            for j, (w, ww) in enumerate(zip(chunk, ws)):
                col = YEL if c0 + j == cur else WHT
                d.text((x + 3, H - 78 + 3), w, font=f, fill=(0, 0, 0, 160), anchor="lm")
                d.text((x, H - 78), w, font=f, fill=col, anchor="lm", stroke_width=6, stroke_fill=BLK)
                x += ww + gap
            return


GRAIN = np.random.default_rng(3).normal(0, 2.5, (H + 256, W + 256, 1)).astype(np.float32)


def frame(fi):
    t = fi / FPS
    img = render(t, fi)
    i0 = max(j for j in range(N) if SC[j] <= t) if t >= 0 else 0; lt0 = t - SC[i0]
    if i0 > 0 and lt0 < 0.35:
        z = 1.0 + 0.12 * (1 - ease(lt0 / 0.35))
        img = img.resize((int(W * z), int(H * z)), Image.BILINEAR).crop((int(W * (z - 1) / 2), int(H * (z - 1) / 2), int(W * (z - 1) / 2) + W, int(H * (z - 1) / 2) + H))
    for st in SHAKE_T:
        if 0 <= t - st < 0.4:
            a = (1 - (t - st) / 0.4) * 16; dx, dy = int(math.sin(fi * 2.3) * a), int(math.cos(fi * 3.1) * a)
            img = img.transform(img.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy), fillcolor=(0, 0, 0, 255))
    for ct in CUTS:
        if 0 <= t - ct < 0.15:
            a = 1 - (t - ct) / 0.15
            img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(55 * a))))
    caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32) * vignette()
    if t < 0.8: rgb *= t / 0.8
    if t > TOTAL - 1.2: rgb *= max(0, (TOTAL - t) / 1.2)
    gy, gx = (fi * 37) % 256, (fi * 91) % 256
    rgb += GRAIN[gy:gy + H, gx:gx + W]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


exec(open("anim28.py").read())
SHAKE_T = []
for _i, _w in ((1, "shut"), (8, "closed")):
    try: SHAKE_T.append(WT(_i, _w))
    except KeyError: pass


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "still":
        for a in sys.argv[2:]: frame(int(a)).save(f"still_{int(a):05d}.png")
    elif cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2)); print([round(x, 1) for x in SC])
    elif cmd == "prefetch":
        keys = []
        for fi in range(0, NF, 6):
            t = fi / FPS; i = max(j for j in range(N) if SC[j] <= t) if t >= 0 else 0
            if S[i][1]["t"] != "map": continue
            keys += tiles.Cam(*cam_for(i, t)).keys()
        print(tiles.prefetch(keys))
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 60 == 0: print(fi, flush=True)
        p.stdin.close(); p.wait()
