"""Kiribati New Year Short 9:16. python3 engine40.py info | still t.. | video A B out.mp4"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script46 import LINES

W, H, FPS = 1080, 1920, 30
POP, POPX = "Poppins-Bold.ttf", "Poppins-ExtraBold.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (60, 200, 90), (80, 170, 255), (255, 255, 255), (0, 0, 0)
ORG, CYAN = (255, 140, 30), (90, 220, 255)
TM = json.load(open("timing.json")); D, TW = TM["D"], TM["T"]
N = len(LINES)
LEAD = 0.25
ST = [LEAD + s for s in TM["starts"]]
TOTAL = ST[-1] + D[-1] + 1.3
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
CLIPS = ["K1", "K2", "K3", "K4", "K5", "K6"]
# shots: (t0, t1, clip, clip_start_sec, rate, zoom0, zoom1, cy)
TL = []
OV = {2: dict(z0=1.05, z1=1.12), 5: dict(start=2.0, use=3.0)}   # K3: light zoom (only one official moves); K6: use the 2-5 s range (close-up of the girl and the cake)
for i, c in enumerate(CLIPS):
    dur = B[i + 1] - B[i]; o = OV.get(i, {})
    rate = max(0.3, min(1.25, o.get("use", 5.8) / dur))
    TL.append((B[i], B[i + 1], c, o.get("start", 0.0), rate, o.get("z0", 1.0), o.get("z1", 1.05), o.get("cy", 0.5)))
CUTS = [x[0] for x in TL[1:]]


def shot_at(t):
    for k, x in enumerate(TL):
        if x[0] <= t < x[1]: return k
    return len(TL) - 1


def cover(im, z=1.0, cy=0.5):
    iw, ih = im.size; s = max(W / iw, H / ih) * z
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5); x0 = (nw - W) // 2; y0 = min(max(0, int(cy * nh - H / 2)), nh - H)
    return im.resize((nw, nh), Image.BILINEAR).crop((x0, y0, x0 + W, y0 + H))


def clip_frame(name, sec):
    d = f"frames/{name}"; n = len(os.listdir(d)); idx = min(n, max(1, int(sec * 24) + 1))
    return Image.open(f"{d}/{idx:04d}.jpg").convert("RGB")


def base(k, t):
    t0, t1, name, s0, rate, z0, z1, cy = TL[k]; u = (t - t0) / max(0.1, t1 - t0)
    return cover(clip_frame(name, min(5.95, s0 + (t - t0) * rate)), z0 + (z1 - z0) * ease(u), cy).convert("RGBA")


# ---------------------------------------------------------------- overlays
def label(img, txt, x, y, t, t0, size=62, col=WHT, hold=None, glow=None):
    if t < t0 or (hold and t > t0 + hold): return
    k = min(1.0, (t - t0) / 0.18); s = 1.25 - 0.25 * ease(k)
    a = 1.0 if not hold else min(1.0, (t0 + hold - t) / 0.25)
    f = font(POPX, size * s); d = ImageDraw.Draw(img)
    if glow:
        gl = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).text((x, y), txt, font=f, fill=glow + (int(230 * a),), anchor="mm", stroke_width=int(size * 0.2), stroke_fill=glow + (int(230 * a),))
        img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(14)))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x + 4, y + 6), txt, font=f, fill=(0, 0, 0, int(150 * a)), anchor="mm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    d.text((x, y), txt, font=f, fill=col + (int(255 * a),), anchor="mm", stroke_width=max(3, int(size * 0.07)), stroke_fill=(0, 0, 0, int(220 * a)))


def counter(img, v0, v1, fmt, x, y, t, t0, dur=1.0, size=78, col=YEL, sub=None, glow=None):
    if t < t0: return
    v = v0 + (v1 - v0) * ease((t - t0) / dur)
    label(img, fmt.format(v), x, y, t, t0, size, col, glow=glow)
    if sub: label(img, sub, x, y + size * 0.85, t, t0 + 0.1, size * 0.42, WHT)


def arrows(img, t, t0, x, y0, y1):
    if t < t0: return
    k = ease((t - t0) / 0.4); d = ImageDraw.Draw(img); h = (y1 - y0) / 2 * k; yc = (y0 + y1) / 2
    for sgn in (-1, 1):
        ya, yb = yc + sgn * 40, yc + sgn * h
        if abs(yb - ya) > 8:
            d.line([(x, ya), (x, yb)], fill=BLK, width=16); d.line([(x, ya), (x, yb)], fill=RED, width=9)
            d.polygon([(x, yb + sgn * 26), (x - 20, yb - sgn * 6), (x + 20, yb - sgn * 6)], fill=RED, outline=BLK)


def bars(img, t, t0):
    if t < t0: return
    d = ImageDraw.Draw(img); x0, w0 = 120, 840
    rows = (("ISLAND SPLIT: 180 M YEARS AGO", 180, CYAN, 0), ("FIRST LIONS: 2 M YEARS AGO", 2, YEL, 0.35))
    for q, (txt, val, col, dl) in enumerate(rows):
        k = ease((t - t0 - dl) / 0.9)
        if k <= 0: continue
        y = 330 + q * 150; wd = max(14, int(w0 * val / 180 * k))
        d.rounded_rectangle((x0 - 6, y - 6, x0 + w0 + 6, y + 66), 18, fill=(0, 0, 0, 120))
        d.rounded_rectangle((x0, y, x0 + wd, y + 60), 14, fill=col + (255,))
        d.text((x0 + 4, y - 30), txt, font=font(POPX, 38), fill=WHT, anchor="lm", stroke_width=4, stroke_fill=BLK)


def strike(img, x, y, w, t, t0):
    if t < t0: return
    k = ease((t - t0) / 0.3); d = ImageDraw.Draw(img)
    d.line([(x - w / 2, y + 10), (x - w / 2 + w * k, y - 10)], fill=BLK, width=22); d.line([(x - w / 2, y + 10), (x - w / 2 + w * k, y - 10)], fill=RED, width=13)


def overlays(img, t):
    if t < B[1]:
        label(img, "1994", 540, 250, t, WT(0, "1994") - 0.1, 104, WHT)
        label(img, "NEW YEAR'S EVE", 540, 380, t, WT(0, "deleted") - 0.1, 76, YEL)
        strike(img, 540, 380, 700, t, WT(0, "deleted") + 0.35)
    elif t < B[2]:
        label(img, "KIRIBATI", 540, 250, t, WT(1, "kiribati") - 0.1, 104, WHT)
        label(img, "EAST: ALMOST 1 DAY BEHIND", 540, 380, t, WT(1, "almost") - 0.1, 56, YEL)
    elif t < B[3]:
        label(img, "ONLY 4 DAYS", 540, 250, t, WT(2, "four") - 0.1, 110, WHT, glow=RED)
        label(img, "A WEEK", 540, 380, t, WT(2, "four") + 0.1, 90, YEL)
    elif t < B[4]:
        label(img, "LINE MOVED ~1,000 KM", 540, 250, t, WT(3, "moved") - 0.1, 66, WHT)
        label(img, "FRI 30 DEC", 540, 380, t, WT(3, "friday") - 0.1, 92, YEL)
        label(img, "SUN 1 JAN", 540, 500, t, WT(3, "sunday") - 0.1, 92, WHT)
    elif t < B[5]:
        label(img, "UTC+14", 540, 260, t, WT(4, "islands") - 0.15, 120, YEL, glow=RED)
        label(img, "FIRST ON EARTH", 540, 400, t, WT(4, "before") - 0.1, 76, WHT)
    else:
        label(img, "NO NEW YEAR'S EVE", 540, 260, t, WT(5, "no") - 0.1, 76, WHT)
        label(img, "BUSINESS FIRST", 540, 390, t, WT(5, "business") - 0.1, 92, YEL)


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
    overlays(img, t); caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    if t > TOTAL - 0.5: rgb *= max(0, (TOTAL - t) / 0.5)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for x in TL: print(round(x[0], 2), round(x[1], 2), x[2], "rate", round(x[4], 2))
    elif cmd == "still":
        os.makedirs("stills", exist_ok=True)
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills/s_{float(a):05.1f}.jpg", quality=88)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(fi).tobytes())
        p.stdin.close(); p.wait()
