"""Continents drift Short 9:16. python3 engine34.py info | still t.. | video A B out.mp4"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script34 import LINES

W, H, FPS = 1080, 1920, 30
POP, POPX = "Poppins-Bold.ttf", "Poppins-ExtraBold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
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
# shots: (t0, t1, clip, clip_start_sec, rate, zoom0, zoom1)
TL = [
 (B[0], B[1], "S1", 0.0, 0.6, 1.0, 1.06),
 (B[1], WT(1, "slower") - 0.1, "S2a", 0.0, 0.5, 1.0, 1.05),
 (WT(1, "slower") - 0.1, B[2], "S2b", 0.0, 1.0, 1.0, 1.05),
 (B[2], WT(2, "thats") - 0.1, "S3a", 0.0, 1.0, 1.0, 1.04),
 (WT(2, "thats") - 0.1, B[3], "S3b", 0.0, 1.0, 1.0, 1.05),
 (B[3], WT(3, "those") - 0.1, "S4a", 0.0, 0.12, 1.0, 1.04),
 (WT(3, "those") - 0.1, B[4], "S4b", 0.0, 1.0, 1.08, 1.0),
 (B[4], B[5], "S5", 0.0, 1.0, 1.0, 1.0),
 (B[5], B[6], "S6", 0.6, 1.5, 1.0, 1.0),
]
CUTS = [x[0] for x in TL[1:]]


def shot_at(t):
    for k, x in enumerate(TL):
        if x[0] <= t < x[1]: return k
    return len(TL) - 1


def cover(im, z=1.0):
    iw, ih = im.size; s = max(W / iw, H / ih) * z
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5); x0, y0 = (nw - W) // 2, (nh - H) // 2
    return im.resize((nw, nh), Image.BILINEAR).crop((x0, y0, x0 + W, y0 + H))


def clip_frame(name, sec):
    d = f"frames/{name}"; n = len(os.listdir(d)); idx = min(n, max(1, int(sec * 24) + 1))
    return Image.open(f"{d}/{idx:04d}.jpg").convert("RGB")


def base(k, t):
    t0, t1, name, s0, rate, z0, z1 = TL[k]; u = (t - t0) / max(0.1, t1 - t0)
    return cover(clip_frame(name, min(5.95, s0 + (t - t0) * rate)), z0 + (z1 - z0) * ease(u)).convert("RGBA")


# ---------------------------------------------------------------- overlays
def label(img, txt, x, y, t, t0, size=62, col=WHT, hold=None):
    if t < t0 or (hold and t > t0 + hold): return
    k = min(1.0, (t - t0) / 0.18); s = 1.25 - 0.25 * ease(k)
    a = 1.0 if not hold else min(1.0, (t0 + hold - t) / 0.25)
    f = font(POPX, size * s); d = ImageDraw.Draw(img)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x + 4, y + 6), txt, font=f, fill=(0, 0, 0, int(150 * a)), anchor="mm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    d.text((x, y), txt, font=f, fill=col + (int(255 * a),), anchor="mm", stroke_width=max(3, int(size * 0.07)), stroke_fill=(0, 0, 0, int(220 * a)))


def counter(img, v0, v1, fmt, x, y, t, t0, dur=1.0, size=78, col=YEL, sub=None):
    if t < t0: return
    v = v0 + (v1 - v0) * ease((t - t0) / dur)
    label(img, fmt.format(v), x, y, t, t0, size, col)
    if sub: label(img, sub, x, y + size * 0.85, t, t0 + 0.1, size * 0.45, WHT)


def bars(img, t, t0):
    if t < t0: return
    d = ImageDraw.Draw(img); x0, w0 = 120, 840
    for q, (txt, val, col) in enumerate((("YOUR NAILS  ~4 CM/YR", 4.2, YEL), ("ATLANTIC  2.5 CM/YR", 2.5, BLU))):
        k = ease((t - t0 - 0.15 * q) / 0.9); y = 330 + q * 150
        d.rounded_rectangle((x0 - 6, y - 6, x0 + w0 + 6, y + 66), 18, fill=(0, 0, 0, 120))
        d.rounded_rectangle((x0, y, x0 + int(w0 * val / 4.2 * k), y + 60), 14, fill=col + (255,))
        d.text((x0 + 4, y - 30), txt, font=font(POPX, 40), fill=WHT, anchor="lm", stroke_width=4, stroke_fill=BLK)


def drift_arrows(img, t, t0):
    if t < t0: return
    k = ease((t - t0) / 0.5); d = ImageDraw.Draw(img); y = 470
    label(img, "AMERICA", 250, y - 70, t, t0, 48); label(img, "EUROPE", 830, y - 70, t, t0, 48)
    for sgn, cx in ((-1, 400), (1, 680)):
        L = 150 * k; x1 = cx + sgn * L
        if L > 5:
            d.line([(cx, y), (x1, y)], fill=WHT, width=12)
            d.polygon([(x1 + sgn * 34, y), (x1 - sgn * 4, y - 26), (x1 - sgn * 4, y + 26)], fill=WHT)


def overlays(img, t):
    drift_arrows(img, t, WT(0, "drifting") - 0.1) if t < B[1] else None
    if B[1] <= t < TL[1][1]: counter(img, 2.5, 2.5, "{:.1f} CM", 540, 380, t, WT(1, "two") - 0.1, 0.8, 110, YEL, "PER YEAR")
    if TL[2][0] <= t < B[2]: bars(img, t, TL[2][0] + 0.1)
    if B[2] <= t < B[3]:
        counter(img, 1492, 2026, "{:.0f}", 540, 330, t, WT(2, "columbus") - 0.15, 1.6, 120, WHT, None) if t < TL[4][0] + 0.05 else None
        if t >= TL[4][0]:
            label(img, "1492 - 2026", 540, 260, t, TL[4][0], 54, WHT)
            counter(img, 0, 13, "+{:.0f} M", 540, 380, t, WT(2, "thirteen") - 0.1, 0.7, 120, YEL)
            label(img, "BUS ~12 M", 540, 520, t, WT(2, "bus") - 0.1, 66, CYAN)
    if B[3] <= t < B[4]:
        counter(img, 0, 175, "{:.0f} MILLION", 540, 330, t, WT(3, "hundred") - 0.15, 1.4, 104, YEL, "YEARS")
        if t >= WT(3, "ocean") - 0.1: label(img, "ATLANTIC OCEAN", 540, 560, t, WT(3, "ocean") - 0.1, 58, CYAN)
    if B[4] <= t < B[5]:
        label(img, "ICELAND", 540, 300, t, WT(4, "iceland") - 0.1, 96, WHT)
        label(img, "THE SEAM ABOVE WATER", 540, 400, t, WT(4, "seam") - 0.1, 50, YEL)
    if t >= B[5]:
        label(img, "NAILS 1 : 0 OCEAN", 540, 330, t, WT(5, "nails") - 0.1, 92, YEL)


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
    if k > 0 and t - t0 < (0.6 if TL[k][2] == "S4b" else 0.08):
        img = Image.blend(base(k - 1, t), img, ease((t - t0) / (0.6 if TL[k][2] == "S4b" else 0.08)))
    overlays(img, t); caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    if t > TOTAL - 0.5: rgb *= max(0, (TOTAL - t) / 0.5)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for x in TL: print(round(x[0], 2), round(x[1], 2), x[2])
    elif cmd == "still":
        os.makedirs("stills", exist_ok=True)
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills/s_{float(a):05.1f}.jpg", quality=88)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(fi).tobytes())
        p.stdin.close(); p.wait()
