"""Moon poop Short 9:16. python3 engine37.py info | still t.. | video A B out.mp4"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from script37 import LINES

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
# shots: (t0, t1, clip, clip_start_sec, rate, zoom0, zoom1, cy, scene_cut)
TL = [
 (B[0], 2.45, "V1", 0.0, 1.0, 1.0, 1.08, 0.5, 0),
 (2.45, B[1], "V2", 0.0, 1.0, 1.0, 1.06, 0.5, 0),
 (B[1], 7.7, "V3", 0.3, 1.0, 1.45, 1.55, 0.30, 1),
 (7.7, B[2], "V3", 2.6, 1.2, 1.0, 1.0, 0.5, 0),
 (B[2], 12.4, "V4", 0.0, 1.0, 1.0, 1.06, 0.5, 1),
 (12.4, 14.8, "V4", 2.6, 1.0, 1.35, 1.45, 0.45, 0),
 (14.8, B[3], "V2", 3.3, 1.0, 1.0, 1.0, 0.5, 0),
 (B[3], 19.4, "V5", 0.0, 1.0, 1.0, 1.05, 0.5, 1),
 (19.4, B[4], "V5", 3.2, 1.0, 1.0, 1.1, 0.5, 0),
 (B[4], 23.9, "V6", 0.0, 1.0, 1.0, 1.04, 0.5, 1),
 (23.9, B[5], "V6", 3.0, 1.0, 1.0, 1.04, 0.5, 0),
 (B[5], 29.0, "V7", 0.0, 1.05, 1.0, 1.0, 0.5, 1),
 (29.0, B[6], "V7", 3.8, 1.0, 1.0, 1.0, 0.5, 0),
 (B[6], 33.9, "V8", 0.0, 1.0, 1.0, 1.0, 0.5, 1),
 (33.9, B[7], "V8", 5.7, 1.0, 1.0, 1.0, 0.5, 0),
]
CUTS = [x[0] for x in TL[1:]]
SCENE_CUTS = [x[0] for x in TL[1:] if x[8]]
_FB = {"V4": "keyframes/S4.jpg", "V6": "keyframes/S6.jpg"}


def shot_at(t):
    for k, x in enumerate(TL):
        if x[0] <= t < x[1]: return k
    return len(TL) - 1


def cover(im, z=1.0, cy=0.5):
    iw, ih = im.size; s = max(W / iw, H / ih) * z
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5); x0 = (nw - W) // 2; y0 = min(max(0, int(cy * nh - H / 2)), nh - H)
    return im.resize((nw, nh), Image.BICUBIC).crop((x0, y0, x0 + W, y0 + H))


def clip_frame(name, sec):
    d = f"frames/{name}"
    if not os.path.isdir(d):
        fb = _FB.get(name)
        return Image.open(fb).convert("RGB") if fb and os.path.exists(fb) else Image.new("RGB", (720, 1280), (30, 30, 30))
    n = len(os.listdir(d)); idx = min(n, max(1, int(sec * 24) + 1))
    return Image.open(f"{d}/{idx:04d}.jpg").convert("RGB")


PUNCH = []  # filled below after WT is usable


def punch(t):
    z = 0.0
    for tp in PUNCH:
        if tp <= t < tp + 0.28: z = max(z, 0.06 * (1 - (t - tp) / 0.28))
    return 1 + z


def base(k, t):
    t0, t1, name, s0, rate, z0, z1, cy, _ = TL[k]; u = (t - t0) / max(0.1, t1 - t0)
    return cover(clip_frame(name, min(7.9, s0 + (t - t0) * rate)), (z0 + (z1 - z0) * ease(u)) * punch(t), cy).convert("RGBA")


PUNCH += [WT(0, "ninetysix"), WT(0, "purpose"), WT(1, "rocket"), WT(3, "three"), WT(4, "moon"), WT(4, "earth"), WT(5, "survived"), WT(6, "pickup")]


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
    if t >= WT(0, "ninetysix") - 0.05 and t < B[1]:
        label(img, "96 BAGS", 540, 280, t, WT(0, "ninetysix") - 0.05, 128, YEL, hold=2.2)
        label(img, "OF POOP", 540, 400, t, WT(0, "ninetysix") + 0.15, 84, WHT, hold=2.0)
    if t >= WT(0, "purpose") - 0.1 and t < B[1]: label(img, "ON PURPOSE", 540, 300, t, WT(0, "purpose") - 0.1, 96, RED)
    if B[1] <= t < B[2]:
        if t >= WT(1, "kilo") - 0.1: label(img, "EVERY KG", 540, 280, t, WT(1, "kilo") - 0.1, 96, WHT)
        if t >= WT(1, "fuel") - 0.1: label(img, "= FUEL", 540, 400, t, WT(1, "fuel") - 0.1, 110, YEL)
    if B[2] <= t < B[3]:
        for w, txt, y, col in (("boots", "BOOTS", 270, WHT), ("backpacks", "BACKPACKS", 370, WHT), ("bags", "WASTE BAGS", 480, YEL)):
            if t >= WT(2, w) - 0.1: label(img, txt, 540, y, t, WT(2, w) - 0.1, 76 if w != "bags" else 92, col)
    if B[3] <= t < B[4]:
        if t >= WT(3, "three") - 0.1:
            label(img, "380+ KG", 540, 270, t, WT(3, "three") - 0.1, 124, YEL)
            label(img, "OF MOON ROCKS", 540, 390, t, WT(3, "three") + 0.1, 70, WHT)
    if B[4] <= t < B[5]:
        if t >= WT(4, "moon") - 0.1: label(img, "MOON: POOP", 540, 230, t, WT(4, "moon") - 0.1, 90, WHT)
        if t >= WT(4, "earth") - 0.1: label(img, "EARTH: ROCKS", 540, 1230, t, WT(4, "earth") - 0.1, 90, YEL)
    if B[5] <= t < B[6]:
        if t >= WT(5, "fifty") - 0.1: label(img, "50+ YEARS LATER", 540, 270, t, WT(5, "fifty") - 0.1, 78, WHT)
        if t >= WT(5, "survived") - 0.1: label(img, "STILL ALIVE?", 540, 390, t, WT(5, "survived") - 0.1, 104, GRN)
    if t >= B[6] and t >= WT(6, "pickup") - 0.1:
        label(img, "POOP PICKUP", 540, 300, t, WT(6, "pickup") - 0.1, 112, YEL)
        paste_emoji(img, "\U0001F680", 540, 450, 130 * min(1.0, (t - WT(6, "pickup")) / 0.25 + 0.1))


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



def whip(img, a, n):
    if n < 3: return img
    arr = np.asarray(img).astype(np.float32)
    out = sum(np.roll(arr, int(s), axis=1) for s in np.linspace(-n, n, 7)) / 7
    return Image.fromarray(out.astype(np.uint8), "RGBA")


def frame(fi):
    t = fi / FPS; k = shot_at(t); t0 = TL[k][0]
    img = base(k, t)
    if k > 0 and t - t0 < 0.07:
        img = Image.blend(base(k - 1, t), img, ease((t - t0) / 0.07))
    for ct in CUTS:
        if 0 <= t - ct < 0.2:
            a = 1 - (t - ct) / 0.2; n = int((70 if ct in SCENE_CUTS else 28) * a * a)
            img = whip(img, a, n)
            if ct in SCENE_CUTS: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(40 * a))))
    hk = WT(0, "ninetysix")
    if 0 <= t - hk < 0.25: img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(130 * (1 - (t - hk) / 0.25)))))
    overlays(img, t); caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    if t > TOTAL - 0.5: rgb *= max(0, (TOTAL - t) / 0.5)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for x in TL: print(round(x[0], 2), round(x[1], 2), x[2], x[3])
    elif cmd == "still":
        os.makedirs("stills", exist_ok=True)
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills/s_{float(a):05.1f}.jpg", quality=88)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b): p.stdin.write(frame(fi).tobytes())
        p.stdin.close(); p.wait()
