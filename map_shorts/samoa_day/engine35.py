"""Samoa day Short 9:16. python3 engine34.py info | still t.. | video A B out.mp4"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script35 import LINES

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
 (B[0], B[1], "S1", 0.0, 1.1, 1.0, 1.05, 0.5),
 (B[1], B[2], "S2", 0.0, 0.8, 1.0, 1.05, 0.5),
 (B[2], B[3], "S3", 0.0, 0.7, 1.6, 1.68, 0.7),
 (B[3], B[4], "S4", 0.0, 1.0, 1.0, 1.06, 0.5),
 (B[4], B[5], "S5", 0.0, 1.55, 1.0, 1.0, 0.5),
 (B[5], B[6], "S6", 0.0, 1.0, 1.0, 1.06, 0.5),
]
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


def strike(img, x, y, w, t, t0):
    if t < t0: return
    k = ease((t - t0) / 0.35); d = ImageDraw.Draw(img)
    d.line([(x - w / 2, y + 8), (x - w / 2 + w * k, y - 8)], fill=RED, width=16)


def overlays(img, t):
    if t < B[1]:
        label(img, "MONDAY", 540, 260, t, 0.3, 84, WHT)
        label(img, "4 JULY 1892", 540, 360, t, 0.45, 92, YEL)
        if t >= WT(0, "twice") - 0.1: label(img, "x2", 540, 480, t, WT(0, "twice") - 0.1, 130, RED)
    elif t < B[2]:
        label(img, "1892", 540, 250, t, B[1] + 0.1, 96, WHT)
        if t >= WT(1, "american", 1) - 0.1: label(img, "AMERICAN DATE", 540, 360, t, WT(1, "american", 1) - 0.1, 70, YEL)
        if t >= WT(1, "fourth") - 0.1:
            label(img, "MON 4 JULY", 540, 470, t, WT(1, "fourth") - 0.1, 64, WHT)
            label(img, "MON 4 JULY", 540, 550, t, WT(1, "fourth") + 0.25, 64, WHT)
    elif t < B[3]:
        if t >= WT(2, "century") - 0.1: label(img, "+119 YEARS", 540, 250, t, WT(2, "century") - 0.1, 80, WHT)
        if t >= WT(2, "zealand") - 0.1: label(img, "NZ & AUSTRALIA: FRIDAY", 540, 360, t, WT(2, "zealand") - 0.1, 56, CYAN)
        if t >= WT(2, "behind") - 0.1:
            label(img, "SAMOA: THURSDAY", 540, 440, t, WT(2, "behind") - 0.1, 56, YEL)
            label(img, "1 DAY BEHIND", 540, 540, t, WT(2, "behind") + 0.2, 80, RED)
    elif t < B[4]:
        label(img, "2011", 540, 250, t, WT(3, "2011") - 0.1 if True else 0, 104, WHT)
        if t >= WT(3, "friday") - 0.1:
            label(img, "FRIDAY 30 DEC", 540, 380, t, WT(3, "friday") - 0.1, 84, YEL)
            strike(img, 540, 380, 680, t, WT(3, "friday") + 0.45)
    elif t < B[5]:
        if t >= WT(4, "thursday") - 0.1: label(img, "THU 29 DEC", 540, 280, t, WT(4, "thursday") - 0.1, 76, WHT)
        if t >= WT(4, "saturday") - 0.1: label(img, "SAT 31 DEC", 540, 390, t, WT(4, "saturday") - 0.1, 76, YEL)
    else:
        if t >= WT(5, "birthday") - 0.1: label(img, "BIRTHDAY: FRI 30", 540, 280, t, WT(5, "birthday") - 0.1, 70, WHT)
        if t >= WT(5, "business") - 0.1: label(img, "BUSINESS FIRST", 540, 390, t, WT(5, "business") - 0.1, 86, YEL)


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
