"""GTA 6 series ep.1 (Thrillbilly Mud Club) Short 9:16. python3 engine49.py info | still t.. | video A B out.mp4"""
import glob, json, math, os, subprocess, sys
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script49 import LINES

W, H, FPS = 1080, 1920, 30
POP, POPX = "Poppins-Bold.ttf", "Poppins-ExtraBold.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (60, 200, 90), (80, 170, 255), (255, 255, 255), (0, 0, 0)
ORG, CYAN, PINK = (255, 140, 30), (90, 220, 255), (255, 80, 160)
DAYS = 34
TM = json.load(open("timing.json")); D, TW = TM["D"], TM["T"]
N = len(LINES)
LEAD = 0.25
ST = [LEAD + s for s in TM["starts"]]
TOTAL = ST[-1] + D[-1] + 1.4
NF = int(TOTAL * FPS)


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


exec(open("helpers_raw.py").read())


def clean(w): return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word, nth=0):
    ws = [clean(w) for w in LINES[i].split()]; q = clean(word)
    hits = [j for j, w in enumerate(ws) if w == q] or [j for j, w in enumerate(ws) if q in w]
    if not hits: raise KeyError((i, word))
    return ST[i] + TW[i][hits[min(nth, len(hits) - 1)]]


B = [0.0] + [ST[i] - 0.12 for i in range(1, N)] + [TOTAL]
CUT0 = WT(0, "and") - 0.1      # hook: monster truck -> aerial reveal of "this place"
CUT1 = WT(1, "all") - 0.1       # line 2: ATV clip -> muddy crowd
CUT2 = WT(2, "fans") - 0.15     # line 3: pickup still -> real satellite map
# shots: (t0, t1, kind, name, s0, use, z0, z1, cy)  kind: clip | still | map
RAW = [
    (B[0], CUT0, "clip", "M1", 0.0, 2.4, 1.10, 1.18, 0.42),
    (CUT0, B[1], "clip", "M4b", 0.0, 3.0, 1.38, 1.06, 0.5),
    (B[1], CUT1, "clip", "M2", 0.0, 4.9, 1.0, 1.06, 0.5),
    (CUT1, B[2], "clip", "M3", 0.0, 2.8, 1.0, 1.06, 0.5),
    (B[2], CUT2, "clip", "M5", 0.0, 3.2, 1.0, 1.08, 0.5),
    (CUT2, B[3], "map", "pg", 0, 0, 1.0, 1.0, 0.5),
    (B[3], B[4], "clip", "M4", 0.0, 5.0, 1.0, 1.14, 0.5),
    (B[4], B[5], "still", "M7", 0, 0, 1.0, 1.14, 0.55),
    (B[5], B[6], "clip", "M6", 0.0, 6.0, 1.22, 1.30, 0.34),
]
TL = []
for (a, b, kind, name, s0, use, z0, z1, cy) in RAW:
    rate = max(0.45, min(1.25, use / max(0.1, b - a))) if kind == "clip" else 0
    TL.append((a, b, kind, name, s0, rate, z0, z1, cy))
CUTS = [x[0] for x in TL[1:]]


def shot_at(t):
    for k, x in enumerate(TL):
        if x[0] <= t < x[1]: return k
    return len(TL) - 1


def cover(im, z=1.0, cy=0.5, cx=0.5):
    iw, ih = im.size; s = max(W / iw, H / ih) * z
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    x0 = min(max(0, int(cx * nw - W / 2)), nw - W); y0 = min(max(0, int(cy * nh - H / 2)), nh - H)
    return im.resize((nw, nh), Image.BILINEAR).crop((x0, y0, x0 + W, y0 + H))


@lru_cache(maxsize=48)
def fr(name, idx): return Image.open(f"frames/{name}_{idx:04d}.jpg").convert("RGB")


def clip_frame(name, sec):
    n = len(glob.glob(f"frames/{name}_*.jpg")); f = min(n - 1.001, max(0.0, sec * 24)); i = int(f); u = f - i
    a = fr(name, i + 1)
    return a if u < 0.02 else Image.blend(a, fr(name, i + 2), u)


@lru_cache(maxsize=8)
def still(name): return Image.open(f"kf/{name}.jpg").convert("RGB")


PIN = (758 / 2160, 1654 / 3840)


@lru_cache(maxsize=1)
def satimg(): return Image.open("sat_pg.jpg").convert("RGB")


def map_base(t, k):
    t0, t1 = TL[k][0], TL[k][1]; u = ease((t - t0) / max(0.1, t1 - t0))
    z = 1.0 + 1.9 * u; im = satimg(); iw, ih = im.size
    cw, ch = W / z * (iw / W) / (iw / W), 0
    vw = iw / z; vh = vw * H / W
    if vh > ih: vh = ih; vw = vh * W / H
    px, py = PIN[0] * iw, PIN[1] * ih
    cxm = (0.5 + (PIN[0] - 0.5) * u) * iw; cym = (0.5 + (PIN[1] - 0.5) * u) * ih
    x0 = min(max(0, cxm - vw / 2), iw - vw); y0 = min(max(0, cym - vh / 2), ih - vh)
    out = im.crop((int(x0), int(y0), int(x0 + vw), int(y0 + vh))).resize((W, H), Image.BILINEAR).convert("RGBA")
    return out, ((px - x0) / vw * W, (py - y0) / vh * H)


def base(k, t):
    t0, t1, kind, name, s0, rate, z0, z1, cy = TL[k]; u = (t - t0) / max(0.1, t1 - t0)
    z = z0 + (z1 - z0) * ease(u)
    if kind == "clip": return cover(clip_frame(name, s0 + (t - t0) * rate), z, cy).convert("RGBA")
    if kind == "still": return cover(still(name), z, cy).convert("RGBA")
    return map_base(t, k)[0]


# ---------------------------------------------------------------- overlays
def fit(fname, size, txt):
    f = font(fname, size)
    while f.getlength(txt) > W - 90 and f.size > 20: f = font(fname, f.size - 2)
    return f


def label(img, txt, x, y, t, t0, size=62, col=WHT, hold=None, glow=None):
    if t < t0 or (hold and t > t0 + hold): return
    k = min(1.0, (t - t0) / 0.18); s = 1.25 - 0.25 * ease(k)
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


def shade_top(img, h=700, a0=140):
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); px = ImageDraw.Draw(g)
    for yy in range(h): px.line([(0, yy), (W, yy)], fill=(0, 0, 0, int(a0 * (1 - yy / h) ** 1.5)))
    img.alpha_composite(g)


def pin(img, t, t0, xy):
    if t < t0: return
    x, y = xy; k = ease((t - t0) / 0.3); d = ImageDraw.Draw(img)
    for q in range(2):
        ph = ((t - t0) * 0.9 + q * 0.5) % 1.0; r = 20 + 90 * ph
        d.ellipse((x - r, y - r, x + r, y + r), outline=RED + (int(220 * (1 - ph)),), width=6)
    r = 26 * k; d.ellipse((x - r, y - r, x + r, y + r), fill=RED + (255,), outline=WHT + (255,), width=7)


def overlays(img, t, k):
    kind = TL[k][2]
    if t < B[1]:
        label(img, "34 DAYS TO GTA 6", 540, 270, t, WT(0, "thirtyfour") - 0.1, 96, WHT, glow=PINK)
        label(img, "THIS PLACE IS REAL?", 540, 400, t, WT(0, "real") - 0.3, 78, YEL)
    elif t < B[2]:
        label(img, "THRILLBILLY MUD CLUB", 540, 270, t, WT(1, "thrillbilly") - 0.1, 86, WHT, glow=ORG)
        label(img, "ATVs · BUGGIES · MONSTER TRUCKS", 540, 385, t, WT(1, "atvs") - 0.1, 56, YEL)
        label(img, "COVERED IN MUD", 540, 500, t, WT(1, "covered") - 0.1, 84, WHT, glow=BLK)
    elif t < B[3]:
        if kind != "map":
            shade_top(img)
            label(img, "NOT CONFIRMED BY ROCKSTAR", 540, 270, t, WT(2, "hasnt") - 0.1, 66, YEL)
            label(img, "FAN THEORY", 540, 390, t, WT(2, "based") - 0.1, 100, WHT, glow=RED)
        else:
            _, xy = map_base(t, k)
            pin(img, t, CUT2 + 0.35, xy)
            label(img, "PUNTA GORDA, FLORIDA", 540, 270, t, WT(2, "punta") - 0.1, 78, WHT, glow=BLK)
            label(img, "REDNECK MUD PARK?", 540, 385, t, WT(2, "redneck") - 0.1, 88, YEL, glow=BLK)
            pill(img, "REAL SATELLITE · Esri", 540, 1790, 34, (20, 150, 90))
    elif t < B[4]:
        label(img, "~800 ACRES", 540, 270, t, WT(3, "eight") - 0.15, 130, WHT, glow=GRN)
        label(img, "≈ 320 HECTARES", 540, 410, t, WT(3, "eight") + 0.25, 64, YEL)
        label(img, "HUGE EVENTS", 540, 520, t, WT(3, "events") - 0.1, 84, WHT, glow=BLK)
    elif t < B[5]:
        shade_top(img)
        label(img, "GRASSRIVERS", 540, 270, t, WT(4, "grassrivers") - 0.1, 104, WHT, glow=GRN)
        label(img, "WIDELY REPORTED", 540, 395, t, WT(4, "reported") - 0.1, 62, WHT)
        label(img, "= EVERGLADES?", 540, 505, t, WT(4, "everglades") - 0.1, 100, YEL, glow=BLK)
    else:
        shade_top(img)
        label(img, "WHICH LOCATION NEXT?", 540, 270, t, WT(5, "which") - 0.1, 84, WHT, glow=PINK)
        label(img, f"{DAYS} DAYS LEFT", 540, 400, t, WT(5, "trailer") - 0.1, 110, YEL, glow=BLK)
        label(img, "COMMENT BELOW", 540, 520, t, WT(5, "check") - 0.1, 70, WHT)
    if t >= B[1]:
        pill(img, f"{DAYS} DAYS TO GTA 6", 540, 110, 36, (210, 40, 120))
    if TL[k][2] != "map":
        pill(img, "AI CONCEPT · NOT GAME FOOTAGE", 540, 1790, 30, (40, 40, 50))


def caption(img, t):
    for i in range(N):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.15:
            words = LINES[i].split(); cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05: cur = j
            c0 = cur // 3 * 3; txt = " ".join(words[c0:c0 + 3])
            f = font(POPX, 64)
            while f.getlength(txt) > W - 120: f = font(POPX, f.size - 2)
            sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 3, 1500 + 5), txt, font=f, fill=(0, 0, 0, 170), anchor="mm")
            img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
            ImageDraw.Draw(img).text((W / 2, 1500), txt, font=f, fill=WHT, anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 200))
            return


def frame(fi):
    t = fi / FPS; k = shot_at(t); t0 = TL[k][0]
    img = base(k, t)
    if k > 0 and t - t0 < 0.08:
        img = Image.blend(base(k - 1, t), img, ease((t - t0) / 0.08))
    overlays(img, t, k); caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    if t > TOTAL - 0.5: rgb *= max(0, (TOTAL - t) / 0.5)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2), "cut1", round(CUT1, 2), "cut2", round(CUT2, 2))
        for x in TL: print(round(x[0], 2), round(x[1], 2), x[2], x[3], "rate", round(x[5], 2))
    elif cmd == "still":
        os.makedirs("stills", exist_ok=True)
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills/s_{float(a):05.1f}.jpg", quality=88)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(fi).tobytes())
        p.stdin.close(); p.wait()
