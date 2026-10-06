"""v20: 'Could You Spend $100 Billion?' long-form 1920x1080 in the jack pockets visual language.
Scenes come from script20.SCENES. python3 engine20.py still <frame> | info | video <f0> <f1> out.mp4"""
import json
import math
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from script20 import LINES, SCENES

W, H, FPS = 1920, 1080, 30
BG = (244, 245, 247)
TOP, LEFT, RIGHT = (221, 229, 236), (186, 200, 211), (148, 163, 184)
GREEN = (34, 197, 94)
RED = (239, 68, 68)
INK = (17, 24, 39)
GREY = (100, 110, 125)
WHT = (255, 255, 255)
START = 100_000_000_000

TM = json.load(open("timing.json"))
D, TW = TM["D"], TM["T"]
LEAD = 0.4
starts = [LEAD + s for s in TM["starts"]]
TOTAL = starts[-1] + D[-1] + 6.0
NF = int(TOTAL * FPS)
SCENE_T = [0.0] + [starts[i] - 0.08 for i in range(1, len(LINES))] + [TOTAL]


def clean(w):
    return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word=None):
    if word is None:
        return starts[i]
    ws = [clean(w) for w in LINES[i].split()]
    q = clean(word)
    for j, w in enumerate(ws):
        if w == q:
            return starts[i] + TW[i][j]
    for j, w in enumerate(ws):
        if q in w:
            return starts[i] + TW[i][j]
    raise KeyError(f"{word} not in line {i}")


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def back(x):
    x = min(1.0, max(0.0, x))
    return 1 + 3.2 * (x - 1) ** 3 + 2.2 * (x - 1) ** 2


# ---------------------------------------------------------------- spending ledger
BUYS = []  # (time, cost, label, price)
for i, sc in enumerate(SCENES):
    if sc.get("cost"):
        if sc.get("buy"):
            tb = WT(i, sc["buy"]) + 0.15
        else:
            tb = starts[i] + 0.6
        BUYS.append((tb, sc["cost"], sc.get("label") or sc.get("sub") or "", sc.get("price") or ""))


def spent(t):
    s = 0.0
    for tb, c, _, _ in BUYS:
        if t >= tb:
            s += c * ease((t - tb) / 0.6)
    return s


TOTAL_SPENT = sum(c for _, c, _, _ in BUYS)

# ---------------------------------------------------------------- drawing kit
_F = {}


def hand(txt):
    return txt.replace("≈", "~").replace("→", "to")


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


def red_arrow(d, x0, y0, x1, y1, width=10, k=1.0, color=RED):
    if k <= 0:
        return
    x1, y1 = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    ang = math.atan2(y1 - y0, x1 - x0)
    hl = width * 3.2
    bx, by = x1 - math.cos(ang) * hl, y1 - math.sin(ang) * hl
    d.line([(x0, y0), (bx, by)], fill=color, width=width)
    px, py = -math.sin(ang), math.cos(ang)
    d.polygon([(x1, y1), (bx + px * hl * 0.6, by + py * hl * 0.6), (bx - px * hl * 0.6, by - py * hl * 0.6)], fill=color)


_BGI = {}


def studio(dark=False):
    if dark not in _BGI:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.55) / H) ** 2)
        if dark:
            v = np.clip(0.22 - 0.25 * r, 0.02, 1)[..., None]
            base = np.array([60, 60, 66], np.float32)
            a = base * v / 0.22
        else:
            v = np.clip(1 - 0.6 * np.clip(r - 0.3, 0, None) ** 1.3, 0, 1)[..., None]
            a = np.array(BG, np.float32) * v
        _BGI[dark] = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    return _BGI[dark].copy()


def iso(x, y, z, cx, cy, s):
    return (cx + (x - y) * 0.866 * s, cy + (x + y) * 0.5 * s - z * s)


def person(d, x, y, h, col=(40, 44, 52)):
    d.ellipse((x - h * 0.09, y - h, x + h * 0.09, y - h * 0.82), fill=col)
    d.rounded_rectangle((x - h * 0.12, y - h * 0.8, x + h * 0.12, y - h * 0.38), radius=max(1, h * 0.05), fill=col)
    d.rectangle((x - h * 0.1, y - h * 0.4, x + h * 0.1, y), fill=col)


# ---------------------------------------------------------------- scene: slab
def slab(frac, lt, counter_text, color=INK, zoom=1.0, note=None, note_t=0.5):
    img = studio()
    s = 285 * zoom
    Lx, Ly, Hz = 1.9, 1.15, 0.42
    cx, cy = W / 2 - (Lx - Ly) / 2 * 0.866 * s, H * 0.62 - (Lx + Ly) / 2 * 0.5 * s + Hz * s * 0.6
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pts = [iso(x, y, 0, cx + 26, cy + 20, s) for x, y in ((0, 0), (Lx, 0), (Lx, Ly), (0, Ly))]
    ImageDraw.Draw(sh).polygon(pts, fill=(0, 0, 0, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)))
    d = ImageDraw.Draw(img)

    def box(x0, x1, top, left, right):
        d.polygon([iso(x0, 0, Hz, cx, cy, s), iso(x1, 0, Hz, cx, cy, s), iso(x1, Ly, Hz, cx, cy, s), iso(x0, Ly, Hz, cx, cy, s)], fill=top)
        d.polygon([iso(x0, Ly, 0, cx, cy, s), iso(x1, Ly, 0, cx, cy, s), iso(x1, Ly, Hz, cx, cy, s), iso(x0, Ly, Hz, cx, cy, s)], fill=left)
        if right is not None:
            d.polygon([iso(Lx, 0, 0, cx, cy, s), iso(Lx, Ly, 0, cx, cy, s), iso(Lx, Ly, Hz, cx, cy, s), iso(Lx, 0, Hz, cx, cy, s)], fill=right)

    box(0, Lx, TOP, LEFT, RIGHT)
    frac = min(1.0, max(0.0, frac))
    split = Lx * (1 - frac)
    if frac > 0.0005:
        box(split, Lx, (248, 113, 113), (220, 38, 38), None)
    for a, b in ((iso(0, Ly, Hz, cx, cy, s), iso(Lx, Ly, Hz, cx, cy, s)), (iso(Lx, Ly, Hz, cx, cy, s), iso(Lx, 0, Hz, cx, cy, s)),
                 (iso(Lx, Ly, 0, cx, cy, s), iso(Lx, Ly, Hz, cx, cy, s))):
        d.line([a, b], fill=(255, 255, 255, 170), width=2)
    hx, hy = iso(Lx * 0.12, Ly + 0.3, 0, cx, cy, s)
    person(d, hx, hy, 0.2 * s)
    f = font("sans", 78 * zoom, True)
    tw = int(f.getlength(counter_text)) + 40
    lay = Image.new("RGBA", (tw, 130), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((20, 65), counter_text, font=f, fill=color, anchor="lm")
    lay = lay.rotate(12, resample=Image.BICUBIC, expand=True)
    x0, y0 = iso(0, 0, Hz, cx, cy, s)
    img.alpha_composite(lay, (int(min(W - lay.width - 30, max(30, x0 - 80))), int(y0 - lay.height + 30)))
    if note and lt > note_t:
        k = ease((lt - note_t) / 0.3)
        bx, by = iso((split + Lx) / 2 if frac > 0.002 else Lx * 0.75, Ly, Hz * 0.5, cx, cy, s)
        tx, ty = min(W - 260, bx + 260), min(H - 70, by + 230)
        red_arrow(d, tx - 120, ty - 40, bx + 8, by + 18, 10, k)
        d.text((tx, ty), hand(note), font=font("hand", 70), fill=RED, anchor="mm")
    return img


# ---------------------------------------------------------------- photos
_IMG, _MSK = {}, {}
import os as _os
VID = {("lambo", True): "lambo2", ("jet", True): "jet", ("yacht", True): "yacht", ("yacht", False): "yacht",
       ("island", True): "island", ("island", False): "island", ("la", True): "la", ("la", False): "la",
       ("burj", True): "burj", ("burj", False): "burj", ("sphere", True): "sphere", ("sphere", False): "sphere",
       ("suburb", True): "suburb", ("suburb", False): "suburb", ("bank", True): "bank", ("louvre", True): "louvre",
       ("louvre", False): "louvre", ("nfl", True): "stadium_v", ("ship", True): "ship_v", ("desert", True): "desert_v",
       ("cash", True): "cash"}
_NV = {}
_SESS = None


def vid_for(sc):
    return VID.get((sc.get("key"), bool(sc.get("plain")))) if sc.get("t") in ("photo", "failed") else None


def vframe(name, idx):
    if name not in _NV:
        _NV[name] = len([f for f in _os.listdir(f"vframes/{name}") if f.endswith(".jpg")])
    idx = max(0, min(_NV[name] - 1, idx))
    return idx, Image.open(f"vframes/{name}/{idx + 1:05d}.jpg").convert("RGB")


def vmask(name, idx, im):
    global _SESS
    p = f"vmasks/{name}/{idx:05d}.png"
    if _os.path.exists(p):
        return Image.open(p).convert("L")
    from rembg import remove, new_session
    if _SESS is None:
        _SESS = new_session("u2net")
    _os.makedirs(f"vmasks/{name}", exist_ok=True)
    m = remove(im.resize((960, 540)), session=_SESS, only_mask=True).resize((1920, 1080), Image.BILINEAR)
    m.save(p)
    return m


def scene_vid_offset(i, name, dur):
    n = _NV.get(name) or len([f for f in _os.listdir(f"vframes/{name}") if f.endswith(".jpg")])
    uses = [j for j, sc in enumerate(SCENES) if vid_for(sc) == name]
    k = uses.index(i) if i in uses else 0
    return int(min(max(0, n - dur * 30 - 1), k * 75))


def load(key):
    if key not in _IMG:
        _IMG[key] = Image.open(f"img/{key}.jpg").convert("RGB")
        _MSK[key] = Image.open(f"masks/{key}.png").convert("L")
    return _IMG[key], _MSK[key]


def video_crop(name, idx, zoom, need_mask):
    idx, im = vframe(name, idx)
    cw, ch = W / zoom, H / zoom
    box = ((W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2)
    img = im.resize((W, H), Image.BICUBIC, box=box).convert("RGBA") if zoom != 1.0 else im.convert("RGBA")
    if need_mask:
        m = vmask(name, idx, im)
        m = m.resize((W, H), Image.BILINEAR, box=box) if zoom != 1.0 else m
    else:
        m = Image.new("L", (W, H), 0)
    return img, m


def photo_crop(key, zoom, focus=True):
    im, m = load(key)
    bb = m.getbbox() or (0, 0, im.width, im.height)
    cxm, cym = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    cw = im.width / zoom
    ch = cw * H / W
    if ch > im.height:
        ch = im.height / zoom
        cw = ch * W / H
    x0 = min(im.width - cw, max(0, (cxm if focus else im.width / 2) - cw / 2))
    y0 = min(im.height - ch, max(0, (cym if focus else im.height / 2) - ch / 2))
    box = (x0, y0, x0 + cw, y0 + ch)
    return im.resize((W, H), Image.BICUBIC, box=box).convert("RGBA"), m.resize((W, H), Image.BILINEAR, box=box)


def green(img, m, k):
    if k <= 0:
        return img
    g = Image.new("RGBA", img.size, GREEN + (255,))
    out = img.copy()
    out.paste(g, (0, 0), m.point(lambda v: int(v * 0.78 * min(1.0, k))))
    return out


def mask_top(m):
    a = np.asarray(m.resize((W // 4, H // 4))).astype(np.float32)
    if a.sum() < 10:
        return W / 2, H / 2
    cx = int((a.sum(0) * np.arange(a.shape[1])).sum() / a.sum(0).sum())
    rows = np.where(a[:, max(0, cx - 3):cx + 4].max(1) > 128)[0]
    return cx * 4, (rows[0] if len(rows) else a.shape[0] // 2) * 4


GRIDS = {5: (3, 2), 10: (4, 3), 20: (5, 4), 40: (8, 5)}
_TILE = {}


def tile(key, tw, th, gk):
    k2 = (key, tw, th)
    if k2 not in _TILE:
        if _os.path.exists(f"img/{key}.jpg"):
            im, m = load(key)
        else:
            _, im = vframe(key, 60)
            m = vmask(key, 60, im)
        bb = m.getbbox() or (0, 0, im.width, im.height)
        w = min(im.width, (bb[2] - bb[0]) * 1.2)
        h = w * th / tw
        if h > im.height:
            h = im.height
            w = h * tw / th
        cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
        x0, y0 = min(im.width - w, max(0, cx - w / 2)), min(im.height - h, max(0, cy - h / 2))
        box = (x0, y0, x0 + w, y0 + h)
        _TILE[k2] = (im.resize((tw, th), Image.LANCZOS, box=box).convert("RGBA"), m.resize((tw, th), Image.BILINEAR, box=box))
    a, mm = _TILE[k2]
    return green(a, mm, gk)


def top_counter(img, t):
    soft_text(img, (W / 2, 70), "${:,}".format(int(START - spent(t))), font("sans", 60, True), WHT + (255,), sh=200, blur=6)


def scene_photo(i, sc, t, lt, dur):
    key = sc["key"]
    tpt = WT(i, sc["pt"]) if sc.get("pt") else None
    punch = tpt is not None and t >= tpt
    vname = vid_for(sc)
    tb = WT(i, sc["buy"]) + 0.15 if sc.get("buy") else None
    if vname:
        z = 1.0 if not punch else 1.15
        fidx = scene_vid_offset(i, vname, dur) + int(lt * FPS)
        need = (tb is not None and t >= tb - 0.2) or (sc.get("label") and not sc.get("plain"))
        img, m = video_crop(vname, fidx, z, bool(need))
    else:
        z = (1.0 + 0.05 * ease(lt / dur)) if not punch else (1.22 + 0.04 * ease((t - tpt) / max(0.5, dur - (tpt - SCENE_T[i]))))
        img, m = photo_crop(key, z)
    gk = 0 if (tb is None or t < tb) else min(1.0, (t - tb) / 0.12) * (1 + 0.25 * max(0, 1 - (t - tb) / 0.3))
    if sc.get("grid") and tb is not None and t >= tb - 0.15:
        cols, rows = GRIDS.get(sc["grid"], (5, 2))
        tw, th = W // cols, H // rows
        base = Image.new("RGBA", (W, H), (12, 12, 12, 255))
        n = min(sc["grid"], 1 + int((t - (tb - 0.15)) / 0.05))
        if key == "suburb":
            _, fr = vframe("suburb", 60 + int(lt * 10) % 200)
            small = fr.resize((tw - 4, th - 4), Image.BILINEAR).convert("RGBA")
            if gk > 0:
                small = Image.blend(small, Image.new("RGBA", small.size, GREEN + (255,)), 0.45 * min(1, gk))
        else:
            small = tile(key, tw - 4, th - 4, gk)
        for k in range(n):
            base.alpha_composite(small, ((k % cols) * tw + 2, (k // cols) * th + 2))
        img = base
    else:
        img = green(img, m, gk)
        if sc.get("label") and not sc.get("plain") or (sc.get("plain") and sc.get("label")):
            tx, ty = mask_top(m)
            if ty > H * 0.6:
                ty = H * 0.42
            lk = ease((lt - 0.2) / 0.25)
            if lk > 0:
                ly = max(230, ty - 150)
                tx = min(W - 300, max(300, tx))
                soft_text(img, (tx, ly - 36), sc["label"], font("sans", 46), WHT + (int(255 * lk),))
                if not sc.get("plain"):
                    red_arrow(ImageDraw.Draw(img), tx - 26, ly, tx, max(ly + 40, ty - 16), 8, lk)
            if punch and sc.get("price"):
                pk = back((t - tpt) / 0.25)
                ly = max(230, ty - 150)
                soft_text(img, (tx, ly - 104), sc["price"], font("sans", 92 * (0.6 + 0.4 * pk), True), WHT + (255,))
    if not sc.get("plain"):
        top_counter(img, t)
    return img


def scene_failed(i, sc, t, lt):
    if vid_for(sc):
        img, m = video_crop(vid_for(sc), scene_vid_offset(i, vid_for(sc), 6) + int(lt * FPS), 1.0, False)
    elif sc.get("key"):
        img, m = photo_crop(sc["key"], 1.0 + 0.04 * ease(lt / 4))
    else:
        img = studio()
    ta = WT(i, sc["at"])
    if t >= ta:
        k = ease((t - ta) / 0.35)
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        off = (1 - k) * -900
        for j in range(-6, 30):
            x = j * 120 + off
            dl.polygon([(x, H), (x + 56, H), (x + 56 + H * 0.45, 0), (x + H * 0.45, 0)], fill=(220, 20, 30, 210))
        img.alpha_composite(lay)
        sk = back((t - ta - 0.25) / 0.3)
        if sk > 0:
            txt = sc.get("text") or "transaction failed"
            f = font("sans", 96 * (0.6 + 0.4 * sk), True)
            tl = Image.new("RGBA", (int(f.getlength(txt)) + 80, 180), (0, 0, 0, 0))
            dd = ImageDraw.Draw(tl)
            dd.rounded_rectangle((0, 0, tl.width - 1, 179), radius=20, fill=(255, 255, 255, 235), outline=RED, width=8)
            dd.text((tl.width / 2, 90), txt, font=f, fill=RED, anchor="mm")
            tl = tl.rotate(-8, resample=Image.BICUBIC, expand=True)
            img.alpha_composite(tl, (int(W / 2 - tl.width / 2), int(H * 0.56 - tl.height / 2)))
    if sc.get("label"):
        f = font("sans", 56, True)
        w_ = f.getlength(sc["label"])
        ImageDraw.Draw(img).rounded_rectangle((W / 2 - w_ / 2 - 30, 100, W / 2 + w_ / 2 + 30, 180), radius=16, fill=(15, 15, 18, 220))
        ImageDraw.Draw(img).text((W / 2, 140), sc["label"], font=f, fill=WHT, anchor="mm")
    return img


# ---------------------------------------------------------------- scene: cards, counters, years
def scene_card(i, sc, t, lt):
    dark = sc.get("bg") == "black"
    img = studio(dark) if dark else studio()
    if dark:
        img = Image.new("RGBA", (W, H), (8, 8, 10, 255))
    d = ImageDraw.Draw(img)
    lines = sc["lines"]
    steps = sc.get("steps") or []
    n0 = len(lines) - len(steps)
    big = len(lines) == 1
    size = 210 if big else (120 if len(lines) <= 3 else 96)
    gap = size * 1.15
    y0 = H / 2 - gap * (len(lines) - 1) / 2
    col = WHT if dark else INK
    for k, ln in enumerate(lines):
        ta = SCENE_T[i] + 0.05 * k if k < n0 else WT(i, steps[k - n0])
        if t < ta:
            continue
        kk = back((t - ta) / 0.3)
        f = font("hand", size * (0.7 + 0.3 * kk))
        y = y0 + k * gap
        d.text((W / 2, y), hand(ln), font=f, fill=col, anchor="mm")
        if k in (sc.get("strike") or []):
            sk = ease((t - ta - 0.6) / 0.3)
            if sk > 0:
                w = f.getlength(ln)
                d.line([(W / 2 - w / 2 - 10, y + 8), (W / 2 - w / 2 - 10 + (w + 20) * sk, y - 8)], fill=RED, width=10)
    if sc.get("arrow"):
        f = font("hand", size)
        w = f.getlength(lines[-1])
        ex = W / 2 - w / 2 - 30
        red_arrow(d, ex - 260, y0 + gap * (len(lines) - 1) + 200, ex - 10, y0 + gap * (len(lines) - 1) + 20, 16, ease((lt - 0.15) / 0.35))
    return img


def scene_count(i, sc, t, lt):
    img = studio()
    d = ImageDraw.Draw(img)
    k = ease((lt - 0.15) / 1.1)
    v = sc["value"] * k
    col = GREEN if sc.get("green") else INK
    f = font("sans", 150, True)
    txt = sc["fmt"].format(int(round(v)))
    while f.getlength(txt) > W - 160:
        f = font("sans", f.size - 8, True)
    d.text((W / 2, H * 0.45), txt, font=f, fill=col, anchor="mm")
    if sc.get("sub"):
        d.text((W / 2, H * 0.45 + 150), hand(sc["sub"]), font=font("hand", 72), fill=GREY, anchor="mm")
    return img


def scene_tick(i, sc, t, lt):
    img = studio()
    d = ImageDraw.Draw(img)
    v = sc["rate"] * max(0.0, lt)
    d.text((W / 2, H * 0.45), sc["label"].format(int(v)), font=font("sans", 170, True), fill=GREEN, anchor="mm")
    d.text((W / 2, H * 0.45 + 160), hand(sc["sub"]), font=font("hand", 70), fill=GREY, anchor="mm")
    return img


def scene_years(i, sc, t, lt):
    img = studio()
    d = ImageDraw.Draw(img)
    k = ease((lt - 0.1) / 1.6)
    v = int(sc["value"] * k)
    d.text((W / 2, 300), "{:,} years".format(v), font=font("sans", 150, True), fill=INK, anchor="mm")
    d.text((W / 2, 430), hand(sc["label"]), font=font("hand", 70), fill=GREY, anchor="mm")
    cols, rows = 40, 8
    cell = 30
    gx0, gy0 = W / 2 - cols * cell / 2, 520
    filled = int(cols * rows * k)
    for c in range(cols * rows):
        x, y = gx0 + (c % cols) * cell, gy0 + (c // cols) * cell
        d.rounded_rectangle((x + 3, y + 3, x + cell - 3, y + cell - 3), radius=4,
                            fill=(RED if c < filled else (210, 216, 224)))
    return img


# ---------------------------------------------------------------- scene: stack of bills
def scene_stack(i, sc, t, lt):
    img = studio()
    hm = sc["height_m"]
    ref = sc["ref"]
    view = {"human": 2.6, "burj": 1500.0, "space": 140000.0}[ref]
    k = ease((lt - 0.2) / 1.6)
    scale = (H * 0.78) / view
    ground = H * 0.88
    if ref == "space":
        sky = np.zeros((H, W, 3), np.float32)
        yy = np.linspace(0, 1, H)[:, None, None]
        sky[:] = np.array([8, 10, 26]) * (1 - yy) + np.array([120, 170, 230]) * yy ** 3
        img = Image.fromarray(sky.astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(img)
    d.line([(0, ground), (W, ground)], fill=(120, 128, 140), width=3)
    sx = W * 0.42
    colw = 70 if ref == "human" else 46
    h = hm * scale * k
    for yy in range(int(ground - h), int(ground), 6):
        d.line([(sx - colw / 2, yy), (sx + colw / 2, yy)], fill=(122, 160, 110) if yy % 12 else (150, 190, 132), width=6)
    d.rectangle((sx - colw / 2, ground - h, sx + colw / 2, ground), outline=(70, 110, 70), width=2)
    rx = W * 0.62
    if ref == "human":
        person(d, rx, ground, 1.8 * scale, (40, 44, 52))
        d.text((rx, ground - 1.8 * scale - 40), "you (1.8 m)", font=font("hand", 56), fill=GREY, anchor="mm")
    elif ref == "burj":
        bh = 828 * scale
        pts = [(rx - 60, ground), (rx - 40, ground - bh * 0.4), (rx - 22, ground - bh * 0.7), (rx - 8, ground - bh * 0.9), (rx, ground - bh),
               (rx + 8, ground - bh * 0.9), (rx + 22, ground - bh * 0.7), (rx + 40, ground - bh * 0.4), (rx + 60, ground)]
        d.polygon(pts, fill=(150, 160, 175))
        d.text((rx + 90, ground - bh), "burj khalifa (828 m)", font=font("hand", 54), fill=GREY, anchor="lm")
    else:
        ky = ground - 100000 * scale
        for x in range(0, W, 40):
            d.line([(x, ky), (x + 22, ky)], fill=(255, 255, 255, 200), width=3)
        d.text((W - 60, ky - 34), "space begins (~100 km)", font=font("hand", 54), fill=WHT, anchor="rm")
    lab_col = WHT if ref == "space" else INK
    d.text((sx, max(80, ground - h - 60)), sc["label"], font=font("sans", 56, True), fill=lab_col, anchor="mm")
    hm_txt = ("≈{:.1f} m" if hm < 10 else "≈{:,.0f} m" if hm < 5000 else "≈{:,.0f} km").format(hm if hm < 5000 else hm / 1000)
    d.text((sx - colw / 2 - 30, ground - h / 2), hand(hm_txt), font=font("hand", 60), fill=RED, anchor="rm")
    return img


# ---------------------------------------------------------------- scene: spotlight objects
def draw_object(d, kind, cx, cy, s, gk):
    fillc = tuple(int(a + (b - a) * min(1, gk)) for a, b in zip((205, 170, 90), GREEN))
    if kind == "painting":
        d.rectangle((cx - 1.0 * s, cy - 1.3 * s, cx + 1.0 * s, cy + 1.3 * s), fill=fillc)
        d.rectangle((cx - 0.85 * s, cy - 1.15 * s, cx + 0.85 * s, cy + 1.15 * s), fill=(40, 30, 25))
        d.ellipse((cx - 0.35 * s, cy - 0.75 * s, cx + 0.35 * s, cy - 0.05 * s), fill=(95, 70, 50))
        d.rounded_rectangle((cx - 0.6 * s, cy, cx + 0.6 * s, cy + 1.1 * s), radius=0.3 * s, fill=(70, 55, 45))
    elif kind == "watch":
        d.rounded_rectangle((cx - 0.3 * s, cy - 1.4 * s, cx + 0.3 * s, cy + 1.4 * s), radius=0.1 * s, fill=(60, 40, 30))
        d.ellipse((cx - 0.75 * s, cy - 0.75 * s, cx + 0.75 * s, cy + 0.75 * s), fill=fillc)
        d.ellipse((cx - 0.62 * s, cy - 0.62 * s, cx + 0.62 * s, cy + 0.62 * s), fill=(245, 240, 228))
        d.line([(cx, cy), (cx, cy - 0.45 * s)], fill=INK, width=max(2, int(s * 0.05)))
        d.line([(cx, cy), (cx + 0.32 * s, cy + 0.1 * s)], fill=INK, width=max(2, int(s * 0.05)))
    elif kind == "diamond":
        pink = tuple(int(a + (b - a) * min(1, gk)) for a, b in zip((245, 140, 190), GREEN))
        d.polygon([(cx - 0.9 * s, cy - 0.3 * s), (cx - 0.5 * s, cy - 0.8 * s), (cx + 0.5 * s, cy - 0.8 * s), (cx + 0.9 * s, cy - 0.3 * s),
                   (cx, cy + 0.9 * s)], fill=pink)
        d.line([(cx - 0.9 * s, cy - 0.3 * s), (cx + 0.9 * s, cy - 0.3 * s)], fill=WHT, width=3)
        d.line([(cx - 0.5 * s, cy - 0.8 * s), (cx - 0.25 * s, cy - 0.3 * s), (cx, cy + 0.9 * s), (cx + 0.25 * s, cy - 0.3 * s), (cx + 0.5 * s, cy - 0.8 * s)],
               fill=WHT, width=3)
    elif kind in ("card", "comic"):
        w_, h_ = (0.75, 1.05) if kind == "card" else (0.95, 1.35)
        d.rectangle((cx - w_ * s, cy - h_ * s, cx + w_ * s, cy + h_ * s), fill=fillc if kind == "card" else (230, 60, 50))
        d.rectangle((cx - (w_ - 0.08) * s, cy - (h_ - 0.08) * s, cx + (w_ - 0.08) * s, cy + (h_ - 0.08) * s),
                    fill=(240, 235, 220) if kind == "card" else (250, 205, 60))
        d.text((cx, cy), "52" if kind == "card" else "#1", font=font("sans", 0.6 * s, True), fill=INK, anchor="mm")


def scene_spot(i, sc, t, lt):
    img = Image.new("RGBA", (W, H), (6, 6, 8, 255))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    dl.polygon([(W / 2 - 110, 0), (W / 2 + 110, 0), (W / 2 + 420, H * 0.86), (W / 2 - 420, H * 0.86)], fill=(255, 250, 235, 26))
    dl.ellipse((W / 2 - 420, H * 0.8, W / 2 + 420, H * 0.92), fill=(255, 250, 235, 200))
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(img)
    tb = WT(i, sc["buy"]) + 0.15 if sc.get("buy") else None
    gk = 0 if (tb is None or t < tb) else min(1.0, (t - tb) / 0.12)
    kind = sc.get("icon", "painting")
    k = back(lt / 0.4)
    draw_object(d, kind, W / 2, H * 0.55, 190 * k, gk)
    soft_text(img, (W / 2, 120), sc["label"], font("sans", 50), WHT + (255,))
    if sc.get("pt") and t >= WT(i, sc["pt"]):
        pk = back((t - WT(i, sc["pt"])) / 0.25)
        col = GREEN if gk > 0 else WHT
        soft_text(img, (W / 2, 205), sc["price"], font("sans", 76 * (0.6 + 0.4 * pk), True), col + (255,))
    if sc.get("cost"):
        soft_text(img, (W / 2, H - 50), "${:,}".format(int(START - spent(t))), font("sans", 44, True), (200, 200, 200, 255))
    return img


# ---------------------------------------------------------------- scene: people grid
def scene_people(i, sc, t, lt):
    img = studio()
    d = ImageDraw.Draw(img)
    n = sc["n"]
    cols = max(1, int(math.ceil(math.sqrt(n * 2.2))))
    rows = int(math.ceil(n / cols))
    cell = min((W - 300) / cols, (H - 330) / max(1, rows), 330)
    x0 = W / 2 - cols * cell / 2
    y0 = 250 + ((H - 330) - rows * cell) / 2
    col = GREEN if sc.get("green") else (40, 44, 52)
    for k in range(n):
        tk = SCENE_T[i] + 0.15 + 1.2 * k / max(1, n)
        if t < tk:
            break
        kk = back((t - tk) / 0.25)
        x = x0 + (k % cols + 0.5) * cell
        y = y0 + (k // cols + 1) * cell
        person(d, x, y, cell * 0.85 * kk, col)
    d.text((W / 2, 140), hand(sc["label"]), font=font("hand", 84), fill=INK, anchor="mm")
    return img


# ---------------------------------------------------------------- scene: chart
def scene_chart(i, sc, t, lt):
    img = studio()
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 260, 200, W - 200, H - 170
    d.line([(x0, y0), (x0, y1), (x1, y1)], fill=INK, width=4)
    k = ease((lt - 0.2) / 2.2)
    mode = sc["mode"]
    N = 120
    xs = np.linspace(0, 1, N)
    rng = np.random.default_rng(7)
    if mode == "race":
        a = 0.8 - 0.45 * xs
        b = 0.8 - 0.45 * xs + 0.30 * xs ** 1.3
        series = [(a, RED, "spending"), (b, GREEN, "interest refills")]
        title = "you vs. interest"
    elif mode == "flat":
        series = [(0.55 + 0.01 * np.sin(xs * 12), INK, "your balance")]
        title = "balance stays flat"
    elif mode == "double":
        series = [(0.35 * 2 ** xs, GREEN, "$59B to ~$118B")]
        title = "18 years at 4%"
    elif mode == "crash":
        series = [(0.75 - 0.05 * xs + np.where(xs > 0.6, -(xs - 0.6) * 1.4, 0), RED, "share price if they sell")]
        title = "selling everything"
    elif mode == "borrow":
        series = [(0.3 + 0.55 * xs ** 1.4, GREEN, "shares"), (0.12 + 0.12 * xs, RED, "loans")]
        title = "borrow, don't sell"
    else:
        walk = np.cumsum(rng.normal(0, 0.04, N))
        series = [(0.55 + walk - walk.mean() * 0, INK, "net worth")]
        title = "one day on the stock market"
    d.text((W / 2, 120), title, font=font("hand", 84), fill=INK, anchor="mm")
    for ys, col, lab in series:
        n = max(2, int(N * k))
        pts = [(x0 + (x1 - x0) * xs[j], y1 - (y1 - y0) * float(np.clip(ys[j], 0.02, 0.98))) for j in range(n)]
        d.line(pts, fill=col, width=8, joint="curve")
        if k > 0.98:
            d.text((pts[-1][0] - 10, pts[-1][1] - 50), hand(lab), font=font("hand", 56), fill=col, anchor="rm")
    return img


# ---------------------------------------------------------------- scene: checkout
def scene_checkout(i, sc, t, lt):
    img = studio()
    d = ImageDraw.Draw(img)
    pw, ph = 1100, 900
    px, py = W / 2 - pw / 2, H / 2 - ph / 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((px + 10, py + 16, px + pw + 10, py + ph + 16), radius=28, fill=(0, 0, 0, 70))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((px, py, px + pw, py + ph), radius=28, fill=WHT)
    d.text((px + 50, py + 60), "your cart", font=font("sans", 54, True), fill=INK, anchor="lm")
    items = [(lab, c) for _, c, lab, _ in BUYS if lab]
    rowh = 62
    view_h = ph - 260
    off = 0
    if sc.get("scroll"):
        off = max(0, len(items) * rowh - view_h) * ease((lt - 0.4) / max(1.0, (SCENE_T[i + 1] - SCENE_T[i]) - 1.0))
    lay = Image.new("RGBA", (pw - 80, view_h), (255, 255, 255, 0))
    dl = ImageDraw.Draw(lay)
    for j, (lab, c) in enumerate(items):
        y = j * rowh - off + rowh / 2
        if -rowh < y < view_h + rowh:
            dl.text((10, y), lab[:40], font=font("sans", 38), fill=INK, anchor="lm")
            dl.text((pw - 100, y), "${:,}".format(int(c)), font=font("sans", 38, True), fill=INK, anchor="rm")
            dl.line([(10, y + rowh / 2 - 2), (pw - 100, y + rowh / 2 - 2)], fill=(230, 232, 236), width=2)
    img.alpha_composite(lay, (int(px + 40), int(py + 110)))
    d = ImageDraw.Draw(img)
    d.line([(px + 40, py + ph - 140), (px + pw - 40, py + ph - 140)], fill=INK, width=3)
    if sc.get("total"):
        k = ease((lt - 0.2) / 1.0)
        d.text((px + 50, py + ph - 80), "total", font=font("sans", 50, True), fill=INK, anchor="lm")
        d.text((px + pw - 330, py + ph - 80), "${:,}".format(int(TOTAL_SPENT * k)), font=font("sans", 50, True), fill=GREEN, anchor="rm")
        d.rounded_rectangle((px + pw - 300, py + ph - 115, px + pw - 50, py + ph - 45), radius=14, fill=GREEN)
        d.text((px + pw - 175, py + ph - 80), "checkout", font=font("sans", 36, True), fill=WHT, anchor="mm")
        if lt > 1.3:  # confetti
            rng = np.random.default_rng(3)
            for _ in range(160):
                x, vy, ph_, c = rng.uniform(0, W), rng.uniform(250, 600), rng.uniform(0, 1), rng.integers(0, 4)
                y = (lt - 1.3) * vy - 60 + ph_ * 80
                if y < H:
                    colr = [GREEN, RED, (59, 130, 246), (250, 204, 21)][c]
                    d.rectangle((x, y, x + 12, y + 18), fill=colr)
    return img


def scene_end(i, sc, t, lt):
    img = studio()
    d = ImageDraw.Draw(img)
    d.text((W / 2, 170), "what would you buy first?", font=font("hand", 90), fill=INK, anchor="mm")
    for j, x in enumerate((W * 0.3, W * 0.7)):
        d.rounded_rectangle((x - 360, 330, x + 360, 740), radius=26, outline=(RED if j else INK), width=8)
        d.text((x, 535), "next video" if j else "subscribe", font=font("sans", 64, True), fill=(RED if j else INK), anchor="mm")
    return img


# ---------------------------------------------------------------- dispatcher
def scene_at(t):
    for i in range(len(LINES)):
        if SCENE_T[i] <= t < SCENE_T[i + 1]:
            return i
    return len(LINES) - 1


def frame(fi):
    t = fi / FPS
    i = scene_at(t)
    sc = SCENES[i]
    t0 = SCENE_T[i]
    lt = t - t0
    dur = SCENE_T[i + 1] - t0
    kind = sc["t"]
    if kind == "photo":
        img = scene_photo(i, sc, t, lt, dur)
    elif kind == "slab":
        sp = sc["spent_override"] if "spent_override" in sc else spent(t)
        frac = sp / START
        if "spent_override" in sc:
            frac *= ease((lt - 0.3) / 0.6)
        zoom = sc.get("zoom", 1.0) * (1.0 + 0.06 * ease(lt / max(1.0, dur)))
        if dur > 4.5 and lt > dur * 0.55:  # second angle: punch in on the slice
            zoom *= 1.18
        txt = "${:,}".format(int(START - (sp if "spent_override" not in sc else sc["spent_override"] * ease((lt - 0.3) / 0.6))))
        img = slab(frac, lt, txt, zoom=zoom, note=sc.get("note"))
    elif kind == "card":
        img = scene_card(i, sc, t, lt)
    elif kind == "count":
        img = scene_count(i, sc, t, lt)
    elif kind == "tick":
        img = scene_tick(i, sc, t, lt)
    elif kind == "years":
        img = scene_years(i, sc, t, lt)
    elif kind == "stack":
        img = scene_stack(i, sc, t, lt)
    elif kind == "failed":
        img = scene_failed(i, sc, t, lt)
    elif kind == "spot":
        img = scene_spot(i, sc, t, lt)
    elif kind == "people":
        img = scene_people(i, sc, t, lt)
    elif kind == "chart":
        img = scene_chart(i, sc, t, lt)
    elif kind == "checkout":
        img = scene_checkout(i, sc, t, lt)
    else:
        img = scene_end(i, sc, t, lt)
    return img.convert("RGB")


if __name__ == "__main__":
    if sys.argv[1] == "still":
        fi = int(sys.argv[2])
        frame(fi).save(f"still_{fi:05d}.png")
    elif sys.argv[1] == "info":
        print("frames", NF, "total", round(TOTAL, 2), "spent", TOTAL_SPENT, "buys", len(BUYS))
    elif sys.argv[1] == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "14", "-pix_fmt",
                              "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 300 == 0:
                print(fi, flush=True)
        p.stdin.close()
        p.wait()
