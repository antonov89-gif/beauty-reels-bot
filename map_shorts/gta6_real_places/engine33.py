"""GTA 6 real places Short 9:16. python3 engine33.py info | still t.. | prefetch | video A B out.mp4"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import tiles
from script33 import S, LINES

W, H, FPS = 1080, 1920, 30
tiles.W, tiles.H = W, H
POP, POPX = "Poppins-Bold.ttf", "Poppins-ExtraBold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (60, 200, 90), (60, 140, 255), (255, 255, 255), (0, 0, 0)
ORG, CYAN, PINK = (255, 140, 30), (90, 220, 255), (255, 80, 170)
TM = json.load(open("timing.json")); D, TW = TM["D"], TM["T"]
N = len(S)
LEAD = 0.3
ST = [LEAD + s for s in TM["starts"]]
SC = [0.0] + [ST[i] - 0.1 for i in range(1, N)]
TOTAL = ST[-1] + D[-1] + 2.6
SC.append(TOTAL + 1)
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


# ---------------------------------------------------------------- shot list: (line, kind, arg, share)
# C = game clip, M = real satellite map
MAPS = {
 "florida": dict(a=(-83.2, 27.6, 9.0), b=(-81.0, 25.5, 3.6)),
 "miami": dict(a=(-80.15, 25.79, 0.09), b=(-80.13, 25.78, 0.045), real="MIAMI BEACH, FLORIDA", game="VICE CITY", pin=(-80.130, 25.781)),
 "keys": dict(a=(-81.15, 24.70, 0.36), b=(-81.16, 24.695, 0.14), real="SEVEN MILE BRIDGE, FLORIDA KEYS", game="LEONIDA KEYS", pin=(-81.165, 24.695)),
 "everglades": dict(a=(-80.85, 25.55, 1.4), b=(-80.85, 25.5, 0.8), real="EVERGLADES, FLORIDA", game="GRASSRIVERS", pin=(-80.85, 25.5)),
 "gulf": dict(a=(-85.80, 30.19, 0.4), b=(-85.80, 30.18, 0.15), real="GULF COAST — PANAMA CITY BEACH", game="PORT GELLHORN", pin=(-85.80, 30.18)),
 "sugar": dict(a=(-80.95, 26.70, 0.32), b=(-80.93, 26.70, 0.17), real="CLEWISTON, FLORIDA — SUGAR TOWN", game="AMBROSIA", pin=(-80.93, 26.75)),
 "britton": dict(a=(-86.28, 30.99, 0.35), b=(-86.282, 30.988, 0.12), real="BRITTON HILL — FLORIDA'S HIGHEST POINT", game="MOUNT KALAGA", note="FLORIDA HAS NO MOUNTAINS", pin=(-86.282, 30.988)),
}
PLAN = [
 (0, "C", "G00", 1.0),
 (1, "M", "florida", 1.0),
 (2, "C", "G01", 0.46), (2, "M", "miami", 0.54),
 (3, "C", "G02", 0.46), (3, "M", "keys", 0.54),
 (4, "C", "G03", 0.46), (4, "M", "everglades", 0.54),
 (5, "C", "G04", 0.46), (5, "M", "gulf", 0.54),
 (6, "C", "G05", 0.46), (6, "M", "sugar", 0.54),
 (7, "M", "britton", 0.48), (7, "C", "G06", 0.52),
 (8, "C", "G07", 1.0),
]
TL = []
for i in range(N):
    sh = [p for p in PLAN if p[0] == i]
    a, b = SC[i], (SC[i + 1] if i + 1 < N else TOTAL)
    tw = sum(p[3] for p in sh); t = a
    for p in sh:
        d = (b - a) * p[3] / tw
        if i == 7: d = (WT(7, "meters") + 0.45 - a) if p[1] == "M" else (b - (WT(7, "meters") + 0.45))
        TL.append((t, t + d, i, p[1], p[2])); t += d
CUTS = [x[0] for x in TL[1:]]


def shot_at(t):
    for k, x in enumerate(TL):
        if x[0] <= t < x[1]: return k
    return len(TL) - 1


def cover(im, z=1.0, cx=0.5, cy=0.5):
    iw, ih = im.size; s = max(W / iw, H / ih) * z
    nw, nh = int(iw * s + 0.5), int(ih * s + 0.5)
    x0 = min(max(0, int(cx * nw - W / 2)), nw - W); y0 = min(max(0, int(cy * nh - H / 2)), nh - H)
    return im.resize((nw, nh), Image.BILINEAR).crop((x0, y0, x0 + W, y0 + H))


def clip_frame(name, sec):
    d = f"frames/{name}"; n = len(os.listdir(d)); idx = min(n, max(1, int(sec * 24) + 1))
    return Image.open(f"{d}/{idx:04d}.jpg").convert("RGB")


def grade(im, esri=False):
    a = np.asarray(im).astype(np.float32) / 255
    a = a ** (0.88 if esri else 0.82)
    g = a.mean(2, keepdims=True); a = g + (a - g) * 1.2
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def map_cam(key, t0, t1, t):
    m = MAPS[key]; k = ease((t - t0) / max(0.1, t1 - t0)); (la, lb), (pa, pb), (za, zb) = zip(m["a"], m["b"])
    return tiles.Cam(la + (lb - la) * k, pa + (pb - pa) * k, math.exp(math.log(za) + (math.log(zb) - math.log(za)) * k))


def tag(img, txt, col=(255, 255, 255)):
    d = ImageDraw.Draw(img); f = font(POP, 28); tw = f.getlength(txt)
    d.rounded_rectangle((28, 34, 28 + tw + 40, 34 + 52), 14, fill=(0, 0, 0, 150))
    d.text((48, 60), txt, font=f, fill=col, anchor="lm")


def pin(img, x, y, color, k):
    if k <= 0: return
    d = ImageDraw.Draw(img); r = 18 * min(k, 1.15)
    for rr, al in ((r * 3.2, 50), (r * 2.2, 90)):
        ov = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).ellipse((x - rr, y - rr, x + rr, y + rr), fill=color + (al,)); img.alpha_composite(ov)
    d.ellipse((x - r - 5, y - r - 5, x + r + 5, y + r + 5), fill=WHT); d.ellipse((x - r, y - r, x + r, y + r), fill=color)


def reveal(img, game, real, t, t0):
    k = ease((t - t0 - 0.25) / 0.3)
    if k <= 0: return
    d = ImageDraw.Draw(img); f1 = font(POPX, 72 * (0.85 + 0.15 * k)); f2 = font(POPX, 42)
    while f2.getlength(real) > W - 110: f2 = font(POPX, f2.size - 2)
    pan = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(pan)
    y0 = 150 - (1 - k) * 90
    pd.rounded_rectangle((36, y0, W - 36, y0 + 238), 26, fill=(8, 14, 28, int(225 * k)), outline=YEL + (int(255 * k),), width=5)
    img.alpha_composite(pan)
    d.text((W / 2, y0 + 62), game, font=f1, fill=YEL, anchor="mm", stroke_width=3, stroke_fill=BLK)
    d.text((W / 2, y0 + 128), "REPORTEDLY BASED ON", font=font(POP, 30), fill=(255, 255, 255, 220), anchor="mm")
    d.text((W / 2, y0 + 188), real, font=f2, fill=WHT, anchor="mm", stroke_width=2, stroke_fill=BLK)


def reveal_unsure(img, game, real, t, t0, note="NOT CONFIRMED · LOOKS LIKE"):
    k = ease((t - t0 - 0.25) / 0.3)
    if k <= 0: return
    d = ImageDraw.Draw(img); f1 = font(POPX, 66 * (0.85 + 0.15 * k)); f2 = font(POPX, 40)
    while f2.getlength(real) > W - 110: f2 = font(POPX, f2.size - 2)
    pan = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(pan)
    y0 = 150 - (1 - k) * 90
    pd.rounded_rectangle((36, y0, W - 36, y0 + 238), 26, fill=(8, 14, 28, int(225 * k)), outline=ORG + (int(255 * k),), width=5)
    img.alpha_composite(pan)
    d.text((W / 2, y0 + 58), game, font=f1, fill=YEL, anchor="mm", stroke_width=3, stroke_fill=BLK)
    d.text((W / 2, y0 + 122), note, font=font(POP, 28), fill=ORG, anchor="mm")
    d.text((W / 2, y0 + 184), real, font=f2, fill=WHT, anchor="mm", stroke_width=2, stroke_fill=BLK)


UNSURE = {"gulf", "sugar", "britton"}


def render_map(key, t0, t1, t, i):
    cam = map_cam(key, t0, t1, t); lt = t - t0
    img = grade(cam.render(), cam.src == "esri").convert("RGBA")
    d = ImageDraw.Draw(img); m = MAPS[key]
    if key == "florida":
        pts = [("VICE CITY = MIAMI", (-80.19, 25.77), -150, 0.6), ("GRASSRIVERS = EVERGLADES", (-80.9, 25.5), 120, 1.6), ("LEONIDA KEYS = FLORIDA KEYS", (-81.5, 24.66), 110, 2.6)]
        for q, (txt, (lo, la), dy, tt) in enumerate(pts):
            x, y = cam.xy(lo, la); k = ease((lt - tt) / 0.35); pin(img, x, y, GRN, k)
            if k > 0:
                f = font(POPX, 38); tw = f.getlength(txt); xx = min(max(x - tw / 2, 40), W - tw - 40)
                d.line([(x, y), (xx + tw / 2, y + dy)], fill=GRN + (255,), width=4)
                d.rounded_rectangle((xx - 16, y + dy - 36, xx + tw + 16, y + dy + 36), 14, fill=(8, 14, 28, int(235 * k)), outline=GRN + (255,), width=3)
                d.text((xx, y + dy + 2), txt, font=f, fill=WHT, anchor="lm")
        x, y = cam.xy(-82.8, 28.0)
        text_stroke(d, (W / 2, 330), "LEONIDA = FLORIDA", font(POPX, 70), YEL, stroke=9) if lt > 0.2 else None
        if lt > 3.2:
            k = ease((lt - 3.2) / 0.3)
            d.rounded_rectangle((60, 430, W - 60, 590), 24, fill=(8, 14, 28, int(235 * k)), outline=WHT + (255,), width=4)
            d.text((W / 2, 475), "3 WIDELY REPORTED", font=font(POPX, 44), fill=GRN, anchor="mm")
            d.text((W / 2, 545), "3 NOT REPORTED (?)", font=font(POPX, 44), fill=ORG, anchor="mm")
        tag(img, "REAL SATELLITE MAP")
    else:
        x, y = cam.xy(*m["pin"]); pin(img, x, y, ORG if key in UNSURE else RED, ease((lt - 0.15) / 0.3))
        (reveal_unsure(img, m["game"], m["real"], t, t0, m.get("note", "NOT CONFIRMED · LOOKS LIKE")) if key in UNSURE else reveal(img, m["game"], m["real"], t, t0))
        tag(img, "REAL SATELLITE VIEW · Esri")
        if key == "britton":
            try: ts = WT(i, "hundred") - 0.1
            except KeyError: ts = t0 + 1.2
            if t >= ts and t < t1 - 0.05:
                k = min(1, (t - ts) / 0.15); s = 1.6 - 0.6 * ease(k)
                text_stroke(d, (W / 2, 900), "105 M", font(POPX, 230 * s), YEL, stroke=16)
                text_stroke(d, (W / 2, 1060), "= 345 FT · HIGHEST POINT", font(POPX, 50), WHT, stroke=7)
    return img


def render_clip(name, t0, t1, t):
    k = (t - t0) / max(t1 - t0, 0.1)
    im = clip_frame(name, min(5.95, t - t0))
    return cover(im, 1.0 + 0.04 * k).convert("RGBA")


def hook_overlay(img, t):
    if t > 4.6: return
    k = ease(t / 0.25) * (1 - ease((t - 4.2) / 0.4)); d = ImageDraw.Draw(img)
    pan = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(pan)
    pd.rounded_rectangle((36, 150, W - 36, 470), 28, fill=(8, 14, 28, int(215 * k)), outline=YEL + (int(255 * k),), width=5)
    img.alpha_composite(pan)
    s = 1.0 + 0.12 * (1 - ease(t / 0.3))
    text_stroke(d, (W / 2, 245), "GTA 6 MAP", font(POPX, 120 * s), WHT, stroke=10)
    text_stroke(d, (W / 2, 370), "= REAL FLORIDA?", font(POPX, 100 * s), YEL, stroke=10)
    d.text((W / 2, 440), "O MAPA DE GTA 6 É A FLÓRIDA REAL?", font=font(POP, 34), fill=(255, 255, 255, int(255 * k)), anchor="mm", stroke_width=3, stroke_fill=BLK)


def end_overlay(img, t):
    t0 = ST[8]
    if t < t0: return
    k = ease((t - t0) / 0.3); d = ImageDraw.Draw(img)
    pan = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(pan)
    pd.rounded_rectangle((60, 380, W - 60, 640), 28, fill=(8, 14, 28, int(225 * k)), outline=YEL + (int(255 * k),), width=5)
    img.alpha_composite(pan)
    d.text((W / 2, 455), "YOUR THEORY?", font=font(POPX, 92), fill=YEL, anchor="mm", stroke_width=6, stroke_fill=BLK)
    d.text((W / 2, 560), "COMMENT BELOW  ·  RELEASE 19 NOV 2026", font=font(POP, 38), fill=WHT, anchor="mm", stroke_width=3, stroke_fill=BLK)


def caption(img, t):
    for i in range(N):
        if ST[i] - 0.05 <= t < ST[i] + D[i] + 0.2:
            words = LINES[i].split(); cur = 0
            for j, o in enumerate(TW[i]):
                if t >= ST[i] + o - 0.05: cur = j
            c0 = cur // 3 * 3; chunk = words[c0:c0 + 3]
            f = font(POPX, 76); gap = f.getlength(" ") * 1.1
            ws = [f.getlength(w) for w in chunk]; tot = sum(ws) + gap * (len(chunk) - 1)
            if tot > W - 60:
                f = font(POPX, 76 * (W - 60) / tot); gap = f.getlength(" ") * 1.1
                ws = [f.getlength(w) for w in chunk]; tot = sum(ws) + gap * (len(chunk) - 1)
            x = (W - tot) / 2; d = ImageDraw.Draw(img); y = 1500
            for j, (w, ww) in enumerate(zip(chunk, ws)):
                col = YEL if c0 + j == cur else WHT
                d.text((x + 4, y + 4), w, font=f, fill=(0, 0, 0, 170), anchor="lm")
                d.text((x, y), w, font=f, fill=col, anchor="lm", stroke_width=9, stroke_fill=BLK)
                x += ww + gap
            return


GRAIN = np.random.default_rng(5).normal(0, 2.5, (H + 256, W + 256, 1)).astype(np.float32)


def base(k, t):
    t0, t1, i, kind, arg = TL[k]
    if kind == "C":
        im = render_clip(arg, t0, t1, t); tag(im, "AI CONCEPT · NOT GAME FOOTAGE", (255, 220, 120)); return im
    return render_map(arg, t0, t1, t, i)


def frame(fi):
    t = fi / FPS; k = shot_at(t); t0 = TL[k][0]
    img = base(k, t)
    if k > 0 and t - t0 < 0.16:
        img = Image.blend(base(k - 1, t), img, ease((t - t0) / 0.16))
    if k > 0 and t - t0 < 0.12:
        z = 1.0 + 0.07 * (1 - ease((t - t0) / 0.12))
        img = img.resize((int(W * z), int(H * z)), Image.BILINEAR).crop((int(W * (z - 1) / 2), int(H * (z - 1) / 2), int(W * (z - 1) / 2) + W, int(H * (z - 1) / 2) + H))
    if k > 0 and t - t0 < 0.1:
        img.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(70 * (1 - (t - t0) / 0.1)))))
    hook_overlay(img, t); end_overlay(img, t); caption(img, t)
    rgb = np.asarray(img.convert("RGB")).astype(np.float32)
    yy, xx = np.mgrid[0:H // 4, 0:W // 4]; dd = np.sqrt(((xx - W / 8) / (W / 8)) ** 2 + ((yy - H / 8) / (H / 8)) ** 2)
    v = np.clip(1.0 - 0.32 * np.clip(dd - 0.6, 0, None) ** 1.4, 0.6, 1)
    rgb *= np.asarray(Image.fromarray((v * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR))[..., None] / 255.0
    if t > TOTAL - 0.8: rgb *= max(0, (TOTAL - t) / 0.8)
    rgb += GRAIN[(fi * 37) % 256:(fi * 37) % 256 + H, (fi * 91) % 256:(fi * 91) % 256 + W]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for x in TL: print(round(x[0], 2), round(x[1], 2), x[2], x[3], x[4])
    elif cmd == "still":
        os.makedirs("stills", exist_ok=True)
        for a in sys.argv[2:]: frame(int(float(a) * FPS)).save(f"stills/s_{float(a):05.1f}.jpg", quality=88)
    elif cmd == "prefetch":
        keys = []
        for k, (t0, t1, i, kind, arg) in enumerate(TL):
            if kind == "M":
                for q in range(9): keys += map_cam(arg, t0, t1, t0 + (t1 - t0) * q / 8).keys()
        print(tiles.prefetch(sorted(set(keys))))
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 150 == 0: print(fi, flush=True)
        p.stdin.close(); p.wait()
