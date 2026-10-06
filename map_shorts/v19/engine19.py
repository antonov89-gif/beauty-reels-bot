"""v19: '$100 billion in 60 seconds' Short in the jack pockets visual language (apFPtyZHuns audit):
white studio + pale-blue money slab + black counter, real photos with tiny lowercase labels, red arrows, price tags,
green 'bought' silhouettes (rembg masks), grid multiplier, handwritten cards, hard cuts, no running subtitles.
python3 engine19.py still <frame> | info | video <f0> <f1> out.mp4"""
import json
import math
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from script19 import LINES

W, H, FPS = 1080, 1920, 30
BG = (244, 245, 247)
TOP, LEFT, RIGHT = (221, 229, 236), (186, 200, 211), (148, 163, 184)
GREEN = (34, 197, 94)
RED = (239, 68, 68)
INK = (17, 24, 39)
WHT = (255, 255, 255)

TM = json.load(open("timing.json"))
D, TW = TM["D"], TM["T"]
LEAD = 0.3
starts = [LEAD + s for s in TM["starts"]]
TOTAL = starts[-1] + D[-1] + 1.0
NF = int(TOTAL * FPS)


def clean(w):
    return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word=None):
    if word is None:
        return starts[i]
    ws = [clean(w) for w in LINES[i].split()]
    q = clean(word)
    for j, w in enumerate(ws):
        if w == q or q in w:
            return starts[i] + TW[i][j]
    raise KeyError(word)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def back(x):
    x = min(1.0, max(0.0, x))
    return 1 + 3.2 * (x - 1) ** 3 + 2.2 * (x - 1) ** 2


_F = {}


def font(kind, size, bold=False):
    key = (kind, int(size), bold)
    if key not in _F:
        f = ImageFont.truetype("fonts/Arimo.ttf" if kind == "sans" else "fonts/GochiHand.ttf", max(1, int(size)))
        if kind == "sans":
            try:
                f.set_variation_by_name("Bold" if bold else "Regular")
            except Exception:
                pass
        _F[key] = f
    return _F[key]


def soft_text(img, xy, txt, f, fill, anchor="mm", sh=170, blur=4):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((xy[0] + 2, xy[1] + 3), txt, font=f, fill=(0, 0, 0, sh), anchor=anchor)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).text(xy, txt, font=f, fill=fill, anchor=anchor)


def red_arrow(d, x0, y0, x1, y1, width=10, k=1.0):
    if k <= 0:
        return
    x1, y1 = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    ang = math.atan2(y1 - y0, x1 - x0)
    hl = width * 3.2
    bx, by = x1 - math.cos(ang) * hl, y1 - math.sin(ang) * hl
    d.line([(x0, y0), (bx, by)], fill=RED, width=width)
    px, py = -math.sin(ang), math.cos(ang)
    d.polygon([(x1, y1), (bx + px * hl * 0.6, by + py * hl * 0.6), (bx - px * hl * 0.6, by - py * hl * 0.6)], fill=RED)


# ---------------------------------------------------------------- studio + slab
_BGI = None


def studio():
    global _BGI
    if _BGI is None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.55) / H) ** 2)
        v = np.clip(1 - 0.55 * np.clip(r - 0.25, 0, None) ** 1.3, 0, 1)[..., None]
        _BGI = Image.fromarray((np.array(BG, np.float32) * v).astype(np.uint8)).convert("RGBA")
    return _BGI.copy()


def iso(x, y, z, cx, cy, s):
    return (cx + (x - y) * 0.866 * s, cy + (x + y) * 0.5 * s - z * s)


def slab(spent_frac, t, lt, counter_value, counter_color=INK, zoom=1.0, human=True, counter_text=None):
    img = studio()
    s = 360 * zoom
    cx, cy = W / 2 - 0.375 * 0.866 * s, 1060
    Lx, Ly, Hz = 1.9, 1.15, 0.42
    # contact shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pts = [iso(x, y, 0, cx + 30, cy + 22, s) for x, y in ((0, 0), (Lx, 0), (Lx, Ly), (0, Ly))]
    ImageDraw.Draw(sh).polygon(pts, fill=(0, 0, 0, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28)))
    d = ImageDraw.Draw(img)

    def box(x0, x1, top, left, right):
        d.polygon([iso(x0, 0, Hz, cx, cy, s), iso(x1, 0, Hz, cx, cy, s), iso(x1, Ly, Hz, cx, cy, s), iso(x0, Ly, Hz, cx, cy, s)], fill=top)
        d.polygon([iso(x0, Ly, 0, cx, cy, s), iso(x1, Ly, 0, cx, cy, s), iso(x1, Ly, Hz, cx, cy, s), iso(x0, Ly, Hz, cx, cy, s)], fill=left)
        if x1 >= Lx - 1e-6 and right is not None:
            d.polygon([iso(Lx, 0, 0, cx, cy, s), iso(Lx, Ly, 0, cx, cy, s), iso(Lx, Ly, Hz, cx, cy, s), iso(Lx, 0, Hz, cx, cy, s)], fill=right)

    split = Lx * (1 - spent_frac)
    box(0, Lx, TOP, LEFT, RIGHT)
    if spent_frac > 0:
        rk = min(1.0, lt / 0.4)
        red_top = tuple(int(a + (b - a) * rk) for a, b in zip(TOP, (248, 113, 113)))
        red_l = tuple(int(a + (b - a) * rk) for a, b in zip(LEFT, (220, 38, 38)))
        red_r = tuple(int(a + (b - a) * rk) for a, b in zip(RIGHT, (185, 28, 28)))
        box(split, Lx, red_top, red_l, None)
    # edges
    for a, b in ((iso(0, Ly, Hz, cx, cy, s), iso(Lx, Ly, Hz, cx, cy, s)), (iso(Lx, Ly, Hz, cx, cy, s), iso(Lx, 0, Hz, cx, cy, s)),
                 (iso(Lx, Ly, 0, cx, cy, s), iso(Lx, Ly, Hz, cx, cy, s))):
        d.line([a, b], fill=(255, 255, 255, 160), width=2)
    if human:  # tiny person for scale, standing in front of the slab
        hx, hy = iso(Lx * 0.18, Ly + 0.32, 0, cx, cy, s)
        hh = 0.2 * s
        d.ellipse((hx - hh * 0.09, hy - hh, hx + hh * 0.09, hy - hh * 0.82), fill=(40, 44, 52))
        d.rounded_rectangle((hx - hh * 0.12, hy - hh * 0.8, hx + hh * 0.12, hy - hh * 0.38), radius=hh * 0.05, fill=(30, 41, 59))
        d.rectangle((hx - hh * 0.1, hy - hh * 0.4, hx + hh * 0.1, hy), fill=(51, 65, 85))
        sh2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh2).ellipse((hx - hh * 0.25, hy - 6, hx + hh * 0.35, hy + 8), fill=(0, 0, 0, 70))
        img.alpha_composite(sh2.filter(ImageFilter.GaussianBlur(5)))
    # counter laid along the top edge (rotated like the reference)
    txt = counter_text or "${:,}".format(int(counter_value))
    f = font("sans", 84 * zoom, True)
    tw = int(f.getlength(txt)) + 40
    lay = Image.new("RGBA", (tw, 140), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((20, 70), txt, font=f, fill=counter_color, anchor="lm")
    lay = lay.rotate(12, resample=Image.BICUBIC, expand=True)
    x0, y0 = iso(0, 0, Hz, cx, cy, s)
    img.alpha_composite(lay, (int(W / 2 - lay.width / 2), int(y0 - lay.height + 30)))
    return img, (cx, cy, s, Lx, Ly, Hz, split)


# ---------------------------------------------------------------- photos
_IMG, _MSK = {}, {}


def photo_crop(key, zoom):
    if key not in _IMG:
        _IMG[key] = Image.open(f"img/{key}.jpg").convert("RGB")
        _MSK[key] = Image.open(f"masks/{key}.png").convert("L")
    im, m = _IMG[key], _MSK[key]
    bx = m.getbbox() or (0, 0, im.width, im.height)
    cxm = (bx[0] + bx[2]) / 2
    ch = im.height / zoom
    cw = ch * W / H
    if cw > im.width:
        cw = im.width
        ch = cw * H / W
    x0 = min(im.width - cw, max(0, cxm - cw / 2))
    y0 = (im.height - ch) / 2
    box = (x0, y0, x0 + cw, y0 + ch)
    return (im.resize((W, H), Image.BICUBIC, box=box).convert("RGBA"), m.resize((W, H), Image.BILINEAR, box=box),
            box)


def green(img, m, k):
    if k <= 0:
        return img
    g = Image.new("RGBA", img.size, GREEN + (255,))
    a = m.point(lambda v: int(v * 0.78 * k))
    out = img.copy()
    out.paste(g, (0, 0), a)
    return out


_TILE = {}


def tile(key, gk):
    if key not in _TILE:
        im, m = _IMG[key], _MSK[key]
        bb = m.getbbox() or (0, 0, im.width, im.height)
        tw_, th_ = W // 2 - 4, H // 5 - 4
        w = min(im.width, (bb[2] - bb[0]) * 1.15)
        h = w * th_ / tw_
        if h > im.height:
            h = im.height
            w = h * tw_ / th_
        cx_, cy_ = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        x0 = min(im.width - w, max(0, cx_ - w / 2))
        y0 = min(im.height - h, max(0, cy_ - h / 2))
        box = (x0, y0, x0 + w, y0 + h)
        _TILE[key] = (im.resize((tw_, th_), Image.LANCZOS, box=box).convert("RGBA"), m.resize((tw_, th_), Image.BILINEAR, box=box))
    a, mm = _TILE[key]
    return green(a, mm, gk)


def mask_top(m):
    a = np.asarray(m.resize((W // 4, H // 4))).astype(np.float32)
    if a.sum() < 10:
        return W / 2, H / 2
    cx = int((a.sum(0) * np.arange(a.shape[1])).sum() / a.sum(0).sum())
    rows = np.where(a[:, max(0, cx - 3):cx + 4].max(1) > 128)[0]
    top = rows[0] if len(rows) else a.shape[0] // 2
    return cx * 4, top * 4


# ---------------------------------------------------------------- story
SPEND = [("lambo", 5_000_000), ("jet", 70_000_000), ("yacht", 500_000_000), ("ship", 2_000_000_000),
         ("sphere", 2_300_000_000), ("carrier", 13_000_000_000)]
START = 100_000_000_000


def spent_before(key):
    tot = 0
    for k, v in SPEND:
        if k == key:
            return tot
        tot += v
    return tot


TOTAL_SPENT = sum(v for _, v in SPEND)
PHOTO = {
    1: dict(key="lambo", label="lamborghini aventador", price="$500k each", pt="Lamborghinis", buy="five", grid="ten"),
    2: dict(key="jet", label="gulfstream g650", price="$70m", pt="seventy", buy="million"),
    3: dict(key="yacht", label="superyacht", price="$500m", pt="Half", buy="billion"),
    5: dict(key="ship", label="icon of the seas", price="$2B", pt="two", buy="billion"),
    6: dict(key="sphere", label="sphere, las vegas", price="$2.3B", pt="two", buy="billion"),
    7: dict(key="carrier", label="uss gerald r. ford", price="$13B", pt="thirteen", buy="billion"),
}
SCENE_T = [0.0] + [starts[i] - 0.08 for i in range(1, len(LINES))] + [TOTAL]
BANK_T = WT(10, "bank")


def scene_at(t):
    for i in range(len(LINES)):
        if SCENE_T[i] <= t < SCENE_T[i + 1]:
            return i
    return len(LINES) - 1


def counter_photo(img, value, t, tchange, prev):
    if t < tchange:
        v = prev
    else:
        v = prev + (value - prev) * ease((t - tchange) / 0.6)
    soft_text(img, (W / 2, 210), "${:,}".format(int(v)), font("sans", 70, True), WHT + (255,), sh=200, blur=6)


def frame(fi):
    t = fi / FPS
    i = scene_at(t)
    t0 = SCENE_T[i]
    lt = t - t0
    if i in PHOTO:
        p = PHOTO[i]
        key = p["key"]
        img, m, _ = photo_crop(key, 1.0 + 0.07 * ease(lt / max(0.5, SCENE_T[i + 1] - t0)))
        tb = WT(i, p["buy"]) + 0.15
        gk = 0 if t < tb else min(1.0, (t - tb) / 0.12) * (1.0 + 0.25 * max(0, 1 - (t - tb) / 0.3))
        if p.get("grid") and t >= WT(i, p["grid"]):
            small = tile(key, gk)
            base = Image.new("RGBA", (W, H), (10, 10, 10, 255))
            n = min(10, 1 + int((t - WT(i, p["grid"])) / 0.07))
            for k in range(n):
                base.alpha_composite(small, ((k % 2) * (W // 2) + 2, (k // 2) * (H // 5) + 2))
            img = base
        else:
            img = green(img, m, gk)
            d = ImageDraw.Draw(img)
            tx, ty = mask_top(m)
            lk = ease((lt - 0.15) / 0.2)
            if lk > 0:
                ly = max(330, ty - 190)
                soft_text(img, (tx, ly - 38), p["label"], font("sans", 54), WHT + (int(255 * lk),))
                red_arrow(ImageDraw.Draw(img), tx - 30, ly, tx, max(ly + 40, ty - 18), 9, lk)
            if t >= WT(i, p["pt"]):
                pk = back((t - WT(i, p["pt"])) / 0.25)
                ly = max(330, ty - 190)
                soft_text(img, (tx, ly - 118), p["price"], font("sans", 100 * (0.6 + 0.4 * pk), True), WHT + (255,))
        prev = START - spent_before(key)
        counter_photo(img, prev - dict(SPEND)[key], t, tb, prev)
    elif i == 0:
        z = 1.08 - 0.08 * ease(lt / 3.5)
        img, g = slab(0, t, lt, START, zoom=z)
        d = ImageDraw.Draw(img)
        if lt > 0.25:
            d.text((W / 2, 1560), "your balance", font=font("hand", 80), fill=INK, anchor="mm")
        k = ease((t - WT(0, "minute")) / 0.3)
        if k > 0:
            red_arrow(d, W / 2, 380, W / 2, 560, 12, k)
            d.text((W / 2, 320), "60 seconds", font=font("hand", 90), fill=RED, anchor="mm")
    elif i in (4, 8):
        frac = (spent_before("ship") if i == 4 else TOTAL_SPENT) / START
        img, (cx, cy, s, Lx, Ly, Hz, split) = slab(frac, t, lt, START - frac * START)
        d = ImageDraw.Draw(img)
        k = ease((lt - 0.6) / 0.3)
        ax, ay = iso((split + Lx) / 2, 0, Hz, cx, cy, s)
        bx, by = iso((split + Lx) / 2, Ly, Hz * 0.5, cx, cy, s)
        red_arrow(d, W / 2, 1560, bx, by + 30, 12, k)
        msg = "barely a dent" if i == 4 else "spent: ~$18B"
        if k > 0:
            d.text((W / 2, 1640), msg, font=font("hand", 84), fill=RED, anchor="mm")
    elif i == 9:
        img = Image.new("RGBA", (W, H), (8, 8, 10, 255))
        d = ImageDraw.Draw(img)
        k = back(lt / 0.3)
        d.text((W / 2 + 60, H / 2), "catch:", font=font("hand", 190 * (0.7 + 0.3 * k)), fill=WHT, anchor="mm")
        red_arrow(d, 150, H / 2 + 230, 330, H / 2 + 60, 16, ease(lt / 0.35))
    elif i in (10, 11, 12):
        rem = START - TOTAL_SPENT
        if i == 10:
            per_day = 9_000_000
            v = per_day * ease((t - WT(10, "nine")) / 0.8) if t >= WT(10, "nine") else 0
            img, g = slab(0, t, lt, rem, counter_text="${:,}".format(int(rem)))
            d = ImageDraw.Draw(img)
            if t >= BANK_T:
                d.text((W / 2, 330), "bank: 4% a year", font=font("hand", 84), fill=INK, anchor="mm")
            if t >= WT(10, "nine"):
                soft_text(img, (W / 2, 1560), "+${:,} / day".format(int(v)), font("sans", 82, True), GREEN + (255,), sh=60)
        elif i == 11:
            img, g = slab(0, t, lt, rem, counter_text="${:,}".format(int(rem + 104 * lt)))
            d = ImageDraw.Draw(img)
            soft_text(img, (W / 2, 1560), "≈ $100 / second", font("sans", 86, True), GREEN + (255,), sh=60)
            red_arrow(d, 300, 360, 380, 560, 12, ease(lt / 0.3))
        else:
            earned = 104 * t
            img, g = slab(0, t, lt, rem, counter_text="+${:,}".format(int(earned)), counter_color=GREEN)
            d = ImageDraw.Draw(img)
            d.text((W / 2, 330), "since this video started", font=font("hand", 74), fill=INK, anchor="mm")
    else:  # 13: good luck
        img, g = slab(TOTAL_SPENT / START, t, 1.0, START - TOTAL_SPENT, zoom=1.0 + 0.08 * ease(lt / 1.8))
        d = ImageDraw.Draw(img)
        k = back(lt / 0.3)
        d.text((W / 2, 360), "good luck.", font=font("hand", 150 * (0.7 + 0.3 * k)), fill=INK, anchor="mm")
    return img.convert("RGB")


if __name__ == "__main__":
    if sys.argv[1] == "still":
        fi = int(sys.argv[2])
        frame(fi).save(f"still_{fi:05d}.png")
    elif sys.argv[1] == "info":
        print("frames", NF, "total", round(TOTAL, 2))
        for i in range(len(LINES)):
            print(i, round(SCENE_T[i], 2))
    elif sys.argv[1] == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt",
                              "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 60 == 0:
                print(fi, flush=True)
        p.stdin.close()
        p.wait()
