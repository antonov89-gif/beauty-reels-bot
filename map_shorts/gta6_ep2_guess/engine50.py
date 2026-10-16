"""GTA 6 ep.2 'Guess the REAL Vice City spot' 9:16. python3 engine50.py info | still t.. | video A B out.mp4"""
import glob, json, math, os, subprocess, sys
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script50 import LINES

W, H, FPS = 1080, 1920, 30
POPX = "Poppins-ExtraBold.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (60, 200, 90), (80, 170, 255), (255, 255, 255), (0, 0, 0)
ORG, CYAN, PINK = (255, 140, 30), (90, 220, 255), (255, 80, 160)
TM = json.load(open("timing.json")); D, TW, V0 = TM["D"], TM["T"], TM["starts"]
SPOTS = json.load(open("spots.json")); ROUTES = json.load(open("routes.json"))
N = len(LINES)
LEAD = 0.25
GAP = {1: 1.8, 3: 2.6, 5: 2.6, 7: 2.6, 9: 2.6, 11: 2.6}      # animated interludes inserted BEFORE line i
ST, acc = [], 0.0
for i in range(N):
    acc += GAP.get(i, 0.0); ST.append(LEAD + V0[i] + acc)
END_CARD = 2.6
TOTAL = ST[-1] + D[-1] + 1.0 + END_CARD
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


# block boundaries: line block L_i = [BL[i], BL[i+1]-gap(i+1)) ; interlude I_i = [BL[i]-gap(i), BL[i])
BL = [0.0] + [ST[i] - 0.12 for i in range(1, N)] + [TOTAL]
def LB(i): return BL[i], BL[i + 1] - (GAP.get(i + 1, 0.0) if i + 1 < N else 0.0)
def IB(i): return BL[i] - GAP.get(i, 0.0), BL[i]
SP = {1: 1, 3: 2, 5: 3, 7: 4, 9: 5, 11: 6}                  # clue line -> spot number
CLUE = {1: ("A1", 0.0), 3: ("A2", 0.0), 5: ("A3", 0.0), 7: ("A4", 0.0), 9: ("A5", 0.0), 11: ("A6", 0.0)}
NAME = {2: "OCEAN DRIVE", 4: "MACARTHUR CAUSEWAY", 6: "KASEYA CENTER", 8: "METROMOVER", 10: "WYNWOOD", 12: "VENETIAN CAUSEWAY"}
SUB = {2: "MIAMI BEACH", 4: "DOWNTOWN TO SOUTH BEACH", 6: "HOME OF THE MIAMI HEAT", 8: "DOWNTOWN MIAMI", 10: "STREET ART DISTRICT", 12: "BISCAYNE BAY"}
PIN = {2: (0.38, 0.50), 4: (0.50, 0.37), 6: (0.50, 0.52), 8: (0.50, 0.50), 10: (0.50, 0.50), 12: (0.50, 0.50)}
GC = {"A3": (1.22, 0.62, 0.30)}   # crop: hides the AI-made game HUD and the LED text on the arena clip
SATK = {2: "S1", 4: "S2", 6: "S3", 8: "S4", 10: "S5", 12: "S6"}


def cover(im, z=1.0, cx=0.5, cy=0.5):
    iw, ih = im.size; s = max(W / iw, H / ih) * z
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    x0 = min(max(0, int(cx * nw - W / 2)), nw - W); y0 = min(max(0, int(cy * nh - H / 2)), nh - H)
    return im.resize((nw, nh), Image.BILINEAR).crop((x0, y0, x0 + W, y0 + H))


@lru_cache(maxsize=60)
def fr(name, idx): return Image.open(f"frames/{name}_{idx:04d}.jpg").convert("RGB")


def clip_frame(name, sec):
    n = len(glob.glob(f"frames/{name}_*.jpg"))
    if n == 0: return placeholder(name)
    f = min(n - 1.001, max(0.0, sec * 24)); i = int(f); u = f - i
    a = fr(name, i + 1)
    return a if u < 0.02 else Image.blend(a, fr(name, i + 2), u)


@lru_cache(maxsize=4)
def placeholder(name):
    k = {"A5": "S5"}.get(name, "S5")
    return cover(Image.open(f"sat/{k}.jpg").convert("RGB")).filter(ImageFilter.GaussianBlur(6))


@lru_cache(maxsize=12)
def satimg(k): return Image.open(f"sat/{k}.jpg").convert("RGB")


# ------------------------------------------------------------------ helpers
def fit(fname, size, txt, maxw=W - 90):
    f = font(fname, size)
    while f.getlength(txt) > maxw and f.size > 18: f = font(fname, f.size - 2)
    return f


def label(img, txt, x, y, t, t0, size=62, col=WHT, glow=None, hold=None):
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


def shade(img, h=620, a0=150, bottom=False):
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); px = ImageDraw.Draw(g)
    for yy in range(h):
        y = H - 1 - yy if bottom else yy
        px.line([(0, y), (W, y)], fill=(0, 0, 0, int(a0 * (1 - yy / h) ** 1.5)))
    img.alpha_composite(g)


def ring(img, cx, cy, r, frac, col, width=16):
    d = ImageDraw.Draw(img); d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(0, 0, 0, 150), width=width + 6)
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * frac, fill=col + (255,), width=width)


def counter(img, v0, v1, fmt, x, y, t, t0, dur, size, col=YEL, glow=None):
    if t < t0: return
    v = v0 + (v1 - v0) * ease((t - t0) / dur); label(img, fmt.format(v), x, y, t, t0, size, col, glow=glow)


def badge(img, n, t):
    pill(img, f"SPOT {n} / 6", 190, 110, 38, (210, 40, 120))
    if n > 1: pill(img, "SCORE: ?", 880, 110, 38, (30, 30, 50))


# ------------------------------------------------------------------ frame builders
def hook_frame(t):
    t0 = 0.0; img = cover(clip_frame("A0", t * 0.62), 1.0 + 0.04 * t / 10).convert("RGBA")
    shade(img, 600)
    label(img, "GUESS THE REAL PLACE", 540, 300, t, 0.4, 84, WHT, glow=PINK)
    label(img, "6 SPOTS · 2 SECONDS EACH", 540, 430, t, WT(0, "two") - 0.1, 60, YEL)
    if t >= IB(1)[0] + 0.1:
        u = t - IB(1)[0]; n = 3 - int(min(2.99, u / 0.5))
        if u < 1.7:
            k = (u % 0.5) / 0.5; label(img, str(n), 540, 960, t, t - k * 0.5, 300, WHT, glow=PINK)
    return img


def clue_frame(i, t):
    n = SP[i]; a, b = LB(i); name, s0 = CLUE[i]
    zb, cxx, cyy = GC.get(name, (1.0, 0.5, 0.5))
    img = cover(clip_frame(name, s0 + (t - a) * 1.0), zb + 0.05 * (t - a) / max(0.1, b - a), cxx, cyy).convert("RGBA")
    shade(img, 520, 130)
    badge(img, n, t)
    left = max(0.0, 2.0 - (t - a - 0.15)); frac = left / 2.0
    label(img, "GUESS?", 540, 330, t, a + 0.05, 120, WHT, glow=PINK)
    ring(img, 540, 560, 100, frac if t > a + 0.15 else 1.0, YEL)
    ImageDraw.Draw(img).text((540, 560), f"{left:0.1f}", font=font(POPX, 66), fill=WHT, anchor="mm", stroke_width=4, stroke_fill=BLK)
    return img


def sat_view(i, t, a, b):
    k = SATK[i]; im = satimg(k); px, py = PIN[i]
    u = ease((t - a) / max(0.1, b - a)); z = 1.0 + 0.55 * u
    cx = 0.5 + (px - 0.5) * u * 0.9; cy = 0.5 + (py - 0.5) * u * 0.9
    base = cover(im, z, cx, cy)
    iw, ih = im.size; s = max(W / iw, H / ih) * z; nw, nh = iw * s, ih * s
    x0 = min(max(0, cx * nw - W / 2), nw - W); y0 = min(max(0, cy * nh - H / 2), nh - H)
    return base.convert("RGBA"), (px * nw - x0, py * nh - y0)


def reveal_frame(i, t):
    a, b = LB(i); n = SP[i - 1]; name, s0 = CLUE[i - 1]
    sat, pxy = sat_view(i, t, a, b)
    wipe = ease((t - a) / 0.9)
    if wipe < 1.0:
        zb, cxx, cyy = GC.get(name, (1.0, 0.5, 0.5))
        gm = cover(clip_frame(name, s0 + (LB(i - 1)[1] - LB(i - 1)[0]) + (t - a)), zb + 0.08, cxx, cyy).convert("RGBA")
        xw = int(W * wipe); img = gm.copy(); img.paste(sat.crop((0, 0, xw, H)), (0, 0))
        d = ImageDraw.Draw(img); d.rectangle((xw - 5, 0, xw + 5, H), fill=WHT + (255,))
        if 0 < xw < W - 60: pill(img, "REAL", max(100, xw - 90), 960, 40, (20, 150, 90))
        if xw < W - 180: pill(img, "GAME", min(W - 100, xw + 100), 960, 40, (210, 40, 120))
    else:
        img = sat
    shade(img, 560, 150)
    shade(img, 700, 170, bottom=True)
    badge(img, n, t)
    if wipe >= 0.9:
        x, y = pxy; k = ease((t - a - 0.8) / 0.3)
        d = ImageDraw.Draw(img)
        for q in range(2):
            ph = ((t - a) * 0.8 + q * 0.5) % 1.0; r = 22 + 100 * ph
            d.ellipse((x - r, y - r, x + r, y + r), outline=RED + (int(230 * (1 - ph)),), width=6)
        r = 28 * k; d.ellipse((x - r, y - r, x + r, y + r), fill=RED + (255,), outline=WHT + (255,), width=8)
    label(img, NAME[i], 540, 290, t, WT(i, {2: "ocean", 4: "macarthur", 6: "kaseya", 8: "metromover", 10: "wynwood", 12: "venetian"}[i]) - 0.15, 96, WHT, glow=PINK)
    label(img, SUB[i], 540, 400, t, WT(i, {2: "ocean", 4: "macarthur", 6: "kaseya", 8: "metromover", 10: "wynwood", 12: "venetian"}[i]) + 0.1, 52, YEL)
    pill(img, "REAL SATELLITE · Esri", 540, 1790, 30, (20, 150, 90))
    facts(img, i, t)
    return img


def facts(img, i, t):
    if i == 2:
        counter(img, 0, 800, "~{:0.0f} BUILDINGS", 540, 1180, t, WT(2, "eight") - 0.2, 1.2, 90, WHT, GRN)
        label(img, "PROTECTED SINCE 1979", 540, 1300, t, WT(2, "1979") - 0.2, 64, YEL)
    elif i == 4:
        counter(img, 0, 3.5, "{:0.1f} MILES", 540, 1180, t, WT(4, "three") - 0.2, 1.1, 110, WHT, GRN)
        label(img, "OPEN SINCE 1920", 540, 1300, t, WT(4, "1920") - 0.2, 70, YEL)
    elif i == 6:
        counter(img, 0, 19600, "{:,.0f} SEATS", 540, 1180, t, WT(6, "nineteen") - 0.2, 1.6, 100, WHT, GRN)
        label(img, "MIAMI HEAT ARENA", 540, 1300, t, WT(6, "heat") - 0.2, 64, YEL)
    elif i == 8:
        label(img, "FREE TO RIDE", 540, 1180, t, WT(8, "free") - 0.2, 100, WHT, glow=GRN)
        label(img, "SINCE 1986", 540, 1310, t, WT(8, "1986") - 0.2, 90, YEL)
    elif i == 10:
        label(img, "WYNWOOD WALLS", 540, 1180, t, WT(10, "2009") - 0.4, 84, WHT, glow=PINK)
        label(img, "2009 · STREET ART GALLERY", 540, 1300, t, WT(10, "2009") - 0.2, 56, YEL)
    elif i == 12:
        counter(img, 0, 12, "{:0.0f} BRIDGES", 540, 1180, t, WT(12, "twelve") - 0.2, 1.0, 110, WHT, GRN)
        label(img, "2 STILL LIFT FOR BOATS", 540, 1310, t, WT(12, "two") - 0.1, 60, YEL)


def hav(a, b):
    R = 3958.8; la1, la2 = math.radians(a[1]), math.radians(b[1]); dl = math.radians(b[0] - a[0]); dp = la2 - la1
    h = math.sin(dp / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def proj(key, lon, lat):
    c = ROUTES[key]; cx, cy, d = c; dlon = d * (W / H) / math.cos(math.radians(cy))
    return (lon - (cx - dlon)) / (2 * dlon) * W, (cy + d - lat) / (2 * d) * H


def interlude_frame(i, t):
    a, b = IB(i); n = SP[i]; u = ease((t - a) / max(0.1, (b - a) * 0.85))
    key = f"R{n - 1}"; im = satimg(key).copy().convert("RGBA")
    s0, s1 = SPOTS[f"S{n - 1}"], SPOTS[f"S{n}"]
    p0, p1 = proj(key, *s0), proj(key, *s1)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 90)); im.alpha_composite(sh)
    d = ImageDraw.Draw(im)
    ex = p0[0] + (p1[0] - p0[0]) * u; ey = p0[1] + (p1[1] - p0[1]) * u
    d.line([p0, (ex, ey)], fill=(0, 0, 0, 255), width=22); d.line([p0, (ex, ey)], fill=PINK + (255,), width=12)
    for p, c in ((p0, GRN), (p1, YEL)):
        d.ellipse((p[0] - 22, p[1] - 22, p[0] + 22, p[1] + 22), fill=c + (255,), outline=WHT + (255,), width=6)
    d.ellipse((ex - 18, ey - 18, ex + 18, ey + 18), fill=WHT + (255,), outline=BLK + (255,), width=5)
    miles = hav(s0, s1) * u
    label(im, f"NEXT: SPOT {n} / 6", 540, 330, t, a + 0.05, 92, WHT, glow=PINK)
    label(im, f"{miles:0.1f} MILES", 540, 470, t, a + 0.1, 80, YEL)
    badge(im, n - 1, t)
    return im


def final_frame(t):
    a = LB(13)[0]; im = satimg("ALL").copy().convert("RGBA"); im.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 120)))
    d = ImageDraw.Draw(im); k = (t - a) / 3.0
    for q in range(1, 7):
        x, y = proj("ALL", *SPOTS[f"S{q}"]); on = ease(k * 6 - (q - 1)); r = 24 * on
        d.ellipse((x - r, y - r, x + r, y + r), fill=RED + (255,), outline=WHT + (255,), width=6)
        if on > 0.5: d.text((x, y - 52), str(q), font=font(POPX, 46), fill=WHT, anchor="mm", stroke_width=5, stroke_fill=BLK)
    label(im, "HOW MANY DID YOU GET?", 540, 330, t, a + 0.05, 78, WHT, glow=PINK)
    label(im, "SCORE ? / 6", 540, 480, t, WT(13, "score") - 0.1, 120, YEL, glow=BLK)
    label(im, "COMMENT BELOW", 540, 1360, t, WT(13, "comments") - 0.1, 70, WHT)
    return im


def caption(img, t):
    for i in range(N):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.15:
            words = LINES[i].split(); cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05: cur = j
            c0 = cur // 3 * 3; txt = " ".join(words[c0:c0 + 3])
            f = fit(POPX, 64, txt, W - 120)
            sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 3, 1560 + 5), txt, font=f, fill=(0, 0, 0, 170), anchor="mm")
            img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
            ImageDraw.Draw(img).text((W / 2, 1560), txt, font=f, fill=WHT, anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 200))
            return


def frame_at(t):
    if t < LB(0)[1]: return hook_frame(t)
    for i in (1, 3, 5, 7, 9, 11):
        if IB(i)[0] <= t < IB(i)[1]:
            return hook_frame(t) if i == 1 else interlude_frame(i, t)
    for i in range(1, N):
        a, b = LB(i)
        if a <= t < b:
            if i in SP: return clue_frame(i, t)
            if i == 13: return final_frame(t)
            return reveal_frame(i, t)
    return final_frame(t)


def frame(fi):
    t = fi / FPS; img = frame_at(t)
    pill_tag(img, t)
    caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    if t > TOTAL - 0.5: rgb *= max(0, (TOTAL - t) / 0.5)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def pill_tag(img, t):
    real = any(LB(i)[0] + 0.9 < t < LB(i)[1] for i in NAME) or any(IB(i)[0] <= t < IB(i)[1] for i in SP if i != 1) or t >= LB(13)[0]
    if not real: pill(img, "AI CONCEPT · NOT GAME FOOTAGE", 540, 1790, 30, (40, 40, 50))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for i in range(N): print(i, round(ST[i], 2), "L", [round(x, 2) for x in LB(i)], "I", [round(x, 2) for x in IB(i)] if i in GAP else "")
    elif cmd == "still":
        os.makedirs("stills", exist_ok=True)
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills/s_{float(a):05.1f}.jpg", quality=88)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(fi).tobytes())
        p.stdin.close(); p.wait()
