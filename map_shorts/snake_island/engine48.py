"""Snake Island Short 9:16. python3 engine48.py info | still t.. | video A B out.mp4"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script48 import LINES

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
CUT3 = WT(3, "still") - 0.1     # line 4: K4 scientist -> K1 aerial (rock the size of football fields)
CUT5 = WT(5, "one") - 0.1       # line 6: K6 bird -> K10 macro (venom five times stronger)
# shots: (t0, t1, clip, clip_start_sec, use_sec, zoom0, zoom1, cy)
RAW = [
    (B[0], B[1], "K1", 0.0, 3.4, 1.0, 1.08, 0.5),
    (B[1], B[2], "K2", 0.0, 5.8, 1.0, 1.06, 0.5),
    (B[2], B[3], "K3", 0.0, 5.8, 1.0, 1.06, 0.5),
    (B[3], CUT3, "K4", 0.0, 3.0, 1.0, 1.06, 0.5),
    (CUT3, B[4], "K1", 2.0, 3.6, 1.12, 1.22, 0.5),
    (B[4], B[5], "K5", 0.0, 5.8, 1.0, 1.06, 0.5),
    (B[5], CUT5, "K6", 0.0, 5.8, 1.0, 1.08, 0.5),
    (CUT5, B[6], "K10", 0.0, 5.8, 1.0, 1.1, 0.5),
    (B[6], B[7], "K7", 0.0, 5.8, 1.0, 1.06, 0.5),
    (B[7], B[8], "K8", 0.0, 5.8, 1.0, 1.06, 0.5),
    (B[8], B[9], "K9", 0.0, 5.8, 1.0, 1.06, 0.5),
    (B[9], B[10], "K10", 0.8, 5.0, 1.2, 1.3, 0.5),
    (B[10], B[11], "K11", 0.0, 5.8, 1.0, 1.06, 0.5),
    (B[11], B[12], "K12", 0.0, 5.8, 1.0, 1.06, 0.5),
]
TL = []
for (a, b, c, s0, use, z0, z1, cy) in RAW:
    rate = max(0.35, min(1.25, use / max(0.1, b - a)))
    TL.append((a, b, c, s0, rate, z0, z1, cy))
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
def fit(fname, size, txt):
    f = font(fname, size)
    while f.getlength(txt) > W - 90 and f.size > 20: f = font(fname, f.size - 2)
    return f


def label(img, txt, x, y, t, t0, size=62, col=WHT, hold=None, glow=None, strike=None):
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
    if strike is not None and t >= strike:
        w = f.getlength(txt); kk = ease((t - strike) / 0.2); x0 = x - w / 2 - 14
        d.line([(x0, y + 6), (x0 + (w + 28) * kk, y - 6)], fill=BLK, width=22)
        d.line([(x0, y + 6), (x0 + (w + 28) * kk, y - 6)], fill=RED, width=14)


def shade_top(img, h=760, a0=150):
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); px = ImageDraw.Draw(g)
    for yy in range(h): px.line([(0, yy), (W, yy)], fill=(0, 0, 0, int(a0 * (1 - yy / h) ** 1.5)))
    img.alpha_composite(g)


def overlays(img, t):
    if t < B[1]:
        label(img, "BRAZIL BANNED IT", 540, 270, t, WT(0, "banned") - 0.15, 104, WHT, glow=RED)
    elif t < B[2]:
        label(img, "33 KM OFFSHORE", 540, 270, t, WT(1, "thirty") - 0.1, 90, WHT)
        label(img, "43 HECTARES", 540, 390, t, WT(1, "forty") - 0.1, 92, YEL)
    elif t < B[3]:
        label(img, "1 SNAKE / m²", 540, 250, t, WT(2, "one") - 0.1, 86, WHT, strike=WT(2, "myth") - 0.05)
        label(img, "400,000 SNAKES", 540, 370, t, WT(2, "four") - 0.1, 86, WHT, strike=WT(2, "myth") - 0.05)
        label(img, "MYTH", 540, 520, t, WT(2, "myth") - 0.05, 140, RED, glow=BLK)
    elif t < B[4]:
        label(img, "2,400–2,900", 540, 270, t, WT(3, "twentyfour") - 0.1, 124, WHT, glow=GRN)
        label(img, "GOLDEN LANCEHEADS", 540, 395, t, WT(3, "golden") - 0.05, 66, YEL)
        label(img, "60 FOOTBALL FIELDS", 540, 520, t, WT(3, "sixty") - 0.1, 84, WHT, glow=BLU) if t >= WT(3, "sixty") - 0.1 else None
    elif t < B[5]:
        shade_top(img)
        label(img, "THOUSANDS OF YEARS AGO", 540, 270, t, WT(4, "thousands") - 0.1, 76, WHT)
        label(img, "SEA LEVEL RISES", 540, 385, t, WT(4, "rising") - 0.1, 84, CYAN)
    elif t < B[6]:
        label(img, "NO MAMMALS = BIRDS", 540, 270, t, WT(5, "mammals") - 0.1, 78, WHT)
        label(img, "5x STRONGER", 540, 270, t, WT(5, "five") - 0.1, 104, WHT, glow=RED) if t >= WT(5, "five") - 0.1 else None
        label(img, "VENOM", 540, 400, t, WT(5, "five") + 0.05, 104, YEL) if t >= WT(5, "five") + 0.05 else None
    elif t < B[7]:
        label(img, "LIGHTHOUSE: 1909", 540, 270, t, WT(6, "1909") - 0.1, 84, WHT)
        label(img, "1920s: LAST PEOPLE LEFT", 540, 390, t, WT(6, "1920s") - 0.5, 66, YEL)
    elif t < B[8]:
        label(img, "NAVY + SCIENTISTS ONLY", 540, 270, t, WT(7, "navy") - 0.1, 76, WHT)
        label(img, "EVERYONE ELSE: BANNED", 540, 390, t, WT(7, "banned") - 0.3, 70, RED, glow=BLK)
    elif t < B[9]:
        label(img, "OFFERS · 2008", 540, 260, t, WT(8, "2008") - 0.1, 70, WHT)
        label(img, "UP TO $30,000", 540, 390, t, WT(8, "thirty") - 0.1, 112, YEL, glow=GRN)
    elif t < B[10]:
        label(img, "CRITICALLY", 540, 250, t, WT(9, "critically") - 0.1, 100, RED, glow=BLK)
        label(img, "ENDANGERED", 540, 360, t, WT(9, "endangered") - 0.1, 100, RED, glow=BLK)
        label(img, "< 3,000 LEFT", 540, 500, t, WT(9, "fewer") - 0.1, 96, WHT)
    elif t < B[11]:
        label(img, "LAST REFUGE", 540, 270, t, WT(10, "last") - 0.1, 110, YEL, glow=BLK)
    else:
        label(img, "0 REVIEWS", 540, 270, t, WT(11, "zero") - 0.1, 112, YEL, glow=BLK)


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
