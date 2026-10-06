"""v14: 'AI will change everything' (2026 edition), 1920x1080, stock footage + flat animated infographics.

python3 engine14.py prep | info | still N | video A B out.mp4
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from script14 import SCRIPT, LINES

W, H, FPS = 1920, 1080, 30
MONT = "/home/claude/v12/Montserrat.ttf"

NAVY = (17, 30, 52)
NAVY2 = (28, 50, 84)
PAPER = (244, 246, 249)
INK = (22, 32, 48)
GREY = (176, 184, 196)
YELLOW = (255, 200, 55)
ORANGE = (238, 138, 38)
GREEN = (44, 168, 98)
BLUE = (58, 118, 200)
TEAL = (60, 170, 190)
RED = (226, 60, 52)
WHITE = (255, 255, 255)

TM = json.load(open("timing.json"))
D, TW = TM["D"], TM["T"]
LEAD = TM.get("voice_offset", 0.4)
starts = [LEAD + s for s in TM["starts"]]
TOTAL = starts[-1] + D[-1] + 2.2
NF = int(TOTAL * FPS)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def out_back(x, s=1.70158):
    x = min(1.0, max(0.0, x))
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def out_cubic(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


_F = {}


def font(size, weight="Bold"):
    key = (int(size), weight)
    if key not in _F:
        f = ImageFont.truetype(MONT, max(1, int(size)))
        f.set_variation_by_name(weight)
        _F[key] = f
    return _F[key]


# ------------------------------------------------------------------ shots
def build_shots():
    shots = []
    for i, (text, sc) in enumerate(SCRIPT):
        scs = sc if isinstance(sc, list) else [sc]
        t0 = 0.0 if i == 0 else starts[i] - 0.15
        t1 = (starts[i + 1] - 0.15) if i + 1 < len(SCRIPT) else TOTAL
        ws = [s.get("w", 1.0) for s in scs]
        tot = sum(ws)
        durs = [(t1 - t0) * w / tot for w in ws]
        # generated clips are only 4 s long: hand the excess to a neighbour that is not a generated clip
        for k, s in enumerate(scs):
            if s["t"] == "clip" and s["src"].startswith("gen:") and durs[k] > 4.0:
                extra = durs[k] - 4.0
                durs[k] = 4.0
                others = [j for j, o in enumerate(scs) if j != k and not (o["t"] == "clip" and o["src"].startswith("gen:"))]
                if others:
                    durs[others[0]] += extra
                else:
                    durs[k] += extra  # nothing else to give it to: the clip will hold its last frame
        t = t0
        for k, (s, d) in enumerate(zip(scs, durs)):
            shots.append(dict(t0=t, t1=t + d, sc=s, line=i, k=k))
            t += d
    return shots


SHOTS = build_shots()


def shot_at(t):
    lo, hi = 0, len(SHOTS) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if SHOTS[mid]["t1"] <= t:
            lo = mid + 1
        else:
            hi = mid
    return SHOTS[lo]


# ------------------------------------------------------------------ clips
def clip_dir(s):
    return f"frames/{s['line']:02d}_{s['k']}"


def bars(src):
    out = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", "1.5", "-i", src, "-frames:v", "1", "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], capture_output=True).stdout
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                            "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(",")
    w, h = int(probe[0]), int(probe[1])
    a = np.frombuffer(out, np.uint8)[: w * h].reshape(h, w).astype(np.float32)
    rows = np.where(a.mean(1) > 12)[0]
    return (int(rows[0]), int(rows[-1]) + 1, w, h) if len(rows) else (0, h, w, h)


def prep():
    os.makedirs("frames", exist_ok=True)
    used = {}
    for s in SHOTS:
        sc = s["sc"]
        if sc["t"] != "clip":
            continue
        dur = s["t1"] - s["t0"] + 0.25
        out = clip_dir(s)
        os.makedirs(out, exist_ok=True)
        name = sc["src"]
        if name.startswith("gen:"):
            src = f"gen/{name[4:]}.mp4"
            top, bot, w, h = bars(src)
            ph = bot - top
            cw = min(w, int(ph * 16 / 9))
            ch = int(cw * 9 / 16)
            x0 = (w - cw) // 2
            y0 = top + (ph - ch) // 2
            vf = f"crop={cw}:{ch}:{x0}:{y0},scale=1920:1080:flags=lanczos,fps=30,eq=contrast=1.03:saturation=1.05"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", vf, "-frames:v",
                            str(int(min(dur, 4.0) * FPS)), "-start_number", "1", "-q:v", "3", f"{out}/%05d.jpg"],
                           check=True)
        else:
            src = f"media/{name}.mp4"
            clen = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                         "csv=p=0", src], capture_output=True, text=True).stdout.strip() or 0)
            off = used.get(name, 0.4)
            if off + dur > clen:
                off = max(0, clen - dur - 0.05)
            used[name] = off + dur
            speed = 1.0 if clen - off >= dur else max(0.3, (clen - off) / dur * 0.98)
            vf = (f"setpts={1 / speed:.4f}*PTS,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                  f"fps=30,eq=contrast=1.04:saturation=1.06")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{off:.2f}", "-i", src, "-t",
                            f"{dur * speed:.2f}", "-vf", vf, "-frames:v", str(int(dur * FPS) + 2), "-start_number", "1",
                            "-q:v", "3", f"{out}/%05d.jpg"], check=True)
        print("clip", out, len(os.listdir(out)), flush=True)


_NCACHE = {}


def clip_frame(s, t):
    d = clip_dir(s)
    if d not in _NCACHE:
        _NCACHE[d] = len([f for f in os.listdir(d) if f.endswith(".jpg")])
    n = _NCACHE[d]
    i = max(1, min(n, int((t - s["t0"]) * FPS) + 1))
    img = Image.open(f"{d}/{i:05d}.jpg").convert("RGB")
    p = (t - s["t0"]) / max(0.01, s["t1"] - s["t0"])
    z = 1.0 + 0.055 * p if s["k"] % 2 == 0 else 1.055 - 0.055 * p
    cw, ch = int(W / z), int(H / z)
    x0, y0 = (W - cw) // 2, (H - ch) // 2
    return img.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR).convert("RGBA")


# ------------------------------------------------------------------ drawing helpers
_BG = {}


def background(kind):
    if kind in _BG:
        return _BG[kind].copy()
    if kind == "navy":
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt((xx - W * 0.62) ** 2 + (yy - H * 0.38) ** 2) / (W * 0.75)
        k = np.clip(1 - r, 0, 1)[..., None]
        a = np.array(NAVY, np.float32) * (1 - k) + np.array(NAVY2, np.float32) * k
        im = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
        d = ImageDraw.Draw(im)
        for x in range(0, W, 120):
            d.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
        for y in range(0, H, 120):
            d.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)
    else:
        im = Image.new("RGBA", (W, H), PAPER + (255,))
        d = ImageDraw.Draw(im)
        for x in range(0, W, 80):
            d.line([(x, 0), (x, H)], fill=(0, 0, 0, 9), width=1)
        for y in range(0, H, 80):
            d.line([(0, y), (W, y)], fill=(0, 0, 0, 9), width=1)
    _BG[kind] = im
    return im.copy()


def text(d, xy, s, size, weight="Bold", fill=INK, anchor="mm", stroke=0, stroke_fill=(0, 0, 0)):
    d.text(xy, s, font=font(size, weight), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)


def wrap(s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if f.getlength(trial) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def rrect(d, box, r, fill=None, outline=None, width=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def paste_scaled(base, lay, cx, cy, s, alpha=1.0):
    """composite `lay` onto base scaled around (cx, cy)."""
    if s <= 0.01 or alpha <= 0:
        return
    if alpha < 1:
        lay = lay.copy()
        a = lay.getchannel("A").point(lambda v: int(v * alpha))
        lay.putalpha(a)
    if abs(s - 1) > 0.003:
        lay = lay.resize((max(1, int(W * s)), max(1, int(H * s))), Image.BILINEAR)
        ox, oy = int(cx - cx * s), int(cy - cy * s)
        full = layer()
        full.alpha_composite(lay, (ox, oy)) if (ox >= 0 and oy >= 0) else full.paste(lay, (ox, oy))
        lay = full
    base.alpha_composite(lay)


# ------------------------------------------------------------------ scenes
def scene_title(sc, p, lt):
    img = background("navy")
    d = ImageDraw.Draw(img)
    lines = sc["lines"]
    num = lines[0] if lines[0].isdigit() else None
    body = lines[1:] if num else lines
    x0 = 300 if num else W // 2
    anchor = "lm" if num else "mm"
    if num:
        k = out_back(lt / 0.45)
        r = int(120 * k)
        d.ellipse((190 - r, H // 2 - r, 190 + r, H // 2 + r), fill=YELLOW)
        text(d, (190, H // 2 + 4), num, int(150 * k), "ExtraBold", NAVY)
    size = 150 if len(body) == 1 else (128 if len(body) == 2 else 108)
    if max(font(size, "ExtraBold").getlength(b) for b in body) > (1450 if num else 1700):
        size = int(size * (1450 if num else 1700) / max(font(size, "ExtraBold").getlength(b) for b in body))
    total_h = len(body) * size * 1.08
    y = H // 2 - total_h / 2 + size * 0.54 - (40 if sc.get("sub") else 0)
    for j, b in enumerate(body):
        k = out_cubic((lt - 0.12 * j - 0.1) / 0.45)
        lay = layer()
        ld = ImageDraw.Draw(lay)
        col = YELLOW if j == len(body) - 1 and len(body) > 1 else WHITE
        ld.text((x0, y + j * size * 1.08 + (1 - k) * 60), b, font=font(size, "ExtraBold"), fill=col, anchor=anchor)
        a = lay.getchannel("A").point(lambda v, kk=k: int(v * kk))
        lay.putalpha(a)
        img.alpha_composite(lay)
    if sc.get("sub"):
        k = out_cubic((lt - 0.5) / 0.5)
        bw = int(font(44, "SemiBold").getlength(sc["sub"]) * k)
        yy = y + (len(body) - 1) * size * 1.08 + size * 0.78 + 28
        d2 = ImageDraw.Draw(img)
        d2.rectangle((x0 - (0 if num else bw / 2), yy - 16, x0 + (bw if num else bw / 2), yy - 10), fill=YELLOW)
        lay = layer()
        ld = ImageDraw.Draw(lay)
        ld.text((x0, yy + 30), sc["sub"], font=font(44, "SemiBold"), fill=(205, 215, 230), anchor=anchor)
        a = lay.getchannel("A").point(lambda v, kk=k: int(v * kk))
        lay.putalpha(a)
        img.alpha_composite(lay)
    return img


def sig(x):
    k = 10.0
    lo, hi = 1 / (1 + math.exp(k * 0.5)), 1 / (1 + math.exp(-k * 0.5))
    return (1 / (1 + math.exp(-k * (x - 0.5))) - lo) / (hi - lo)


CX0, CX1, CY0, CY1 = 260, 1660, 790, 200


def cpt(x):
    return CX0 + x * (CX1 - CX0), CY0 - sig(x) * (CY0 - CY1)


def phase_color(x):
    return ORANGE if x < 0.30 else (GREEN if x < 0.72 else BLUE)


def scene_curve(sc, p, lt):
    img = background("paper")
    d = ImageDraw.Draw(img)
    # axes
    d.line([(CX0 - 30, CY0 + 20), (CX0 - 30, CY1 - 80)], fill=INK, width=6)
    d.line([(CX0 - 30, CY0 + 20), (CX1 + 70, CY0 + 20)], fill=INK, width=6)
    d.polygon([(CX0 - 30, CY1 - 110), (CX0 - 46, CY1 - 78), (CX0 - 14, CY1 - 78)], fill=INK)
    d.polygon([(CX1 + 100, CY0 + 20), (CX1 + 68, CY0 + 4), (CX1 + 68, CY0 + 36)], fill=INK)
    text(d, (CX1 + 20, CY0 + 66), "TIME", 34, "Bold", INK)
    lay = Image.new("RGBA", (300, 60), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((150, 30), "PROGRESS", font=font(34, "Bold"), fill=INK, anchor="mm")
    lay = lay.rotate(90, expand=True)
    img.alpha_composite(lay, (CX0 - 120, int((CY0 + CY1) / 2) - 150))
    # faint full curve
    pts = [cpt(i / 240) for i in range(241)]
    d.line(pts, fill=(205, 211, 221), width=10, joint="curve")
    a, b = sc["a"], sc["b"]
    cur = a + (b - a) * ease(min(1.0, p * 1.5))
    if sc.get("full", True) is False:
        start = 0.0
    else:
        start = 0.0
    # coloured part: from 0 to cur
    n = int(240 * cur)
    for i in range(n):
        x = i / 240
        d.line([cpt(x), cpt((i + 1) / 240)], fill=phase_color(x), width=16)
    hx, hy = cpt(cur)
    d.ellipse((hx - 20, hy - 20, hx + 20, hy + 20), fill=WHITE, outline=phase_color(cur), width=8)
    # phase chips
    names = [("SLOW", 0.15, ORANGE), ("RAPID", 0.51, GREEN), ("STABLE", 0.86, BLUE)]
    for j, (nm, xm, col) in enumerate(names):
        active = j == sc["phase"]
        px, py = CX0 + xm * (CX1 - CX0), CY0 + 110
        f = font(40, "ExtraBold")
        wdt = f.getlength(nm) + 60
        rrect(d, (px - wdt / 2, py - 34, px + wdt / 2, py + 34), 34, fill=col if active else (226, 230, 237))
        text(d, (px, py), nm, 40, "ExtraBold", WHITE if active else (140, 148, 162))
    if sc.get("label"):
        rrect(d, (CX0 + 20, 120, CX0 + 20 + 330, 200), 40, fill=INK)
        text(d, (CX0 + 20 + 165, 160), f"{sc['label']} curve", 40, "ExtraBold", WHITE)
    # pins
    for j, (px_, label, appear) in enumerate(sc.get("pins", [])):
        k = out_back((p - appear * 0.6) / 0.25)
        if k <= 0.02 or px_ > cur + 0.02:
            continue
        x, y = cpt(px_)
        up = -1
        cy_ = y - 150 * up * -1 if False else y - 130
        f = font(38, "Bold")
        wdt = f.getlength(label) + 56
        lay = layer()
        ld = ImageDraw.Draw(lay)
        ld.line([(x, y), (x, cy_ + 34)], fill=INK, width=4)
        ld.ellipse((x - 11, y - 11, x + 11, y + 11), fill=INK)
        rrect(ld, (x - wdt / 2, cy_ - 34, x + wdt / 2, cy_ + 34), 20, fill=WHITE, outline=INK, width=4)
        ld.text((x, cy_), label, font=f, fill=INK, anchor="mm")
        paste_scaled(img, lay, x, y, k)
    return img


def scene_list(sc, p, lt):
    img = background("paper")
    d = ImageDraw.Draw(img)
    items = sc["items"]
    head = sc.get("head")
    top = 150
    if head:
        text(d, (W // 2, 150), head.upper(), 56, "ExtraBold", INK)
        top = 270
    n = len(items)
    rowh = min(150, (H - top - 150) / n)
    for j, it in enumerate(items):
        appear = 0.08 + 0.7 * j / n
        k = out_back((p - appear) / 0.14)
        if k <= 0.01:
            continue
        y = top + j * rowh + rowh / 2
        lay = layer()
        ld = ImageDraw.Draw(lay)
        f = font(60, "ExtraBold")
        wdt = f.getlength(it) + 190
        x0 = W // 2 - wdt / 2
        rrect(ld, (x0, y - rowh * 0.4, x0 + wdt, y + rowh * 0.4), 36, fill=WHITE, outline=(200, 207, 218), width=3)
        col = [BLUE, GREEN, ORANGE, TEAL, RED][j % 5]
        ld.ellipse((x0 + 26, y - 34, x0 + 94, y + 34), fill=col)
        ld.line([(x0 + 44, y), (x0 + 56, y + 14), (x0 + 78, y - 12)], fill=WHITE, width=9, joint="curve")
        ld.text((x0 + 120, y), it, font=f, fill=INK, anchor="lm")
        paste_scaled(img, lay, W // 2, y, k)
    return img


def scene_counter(sc, p, lt):
    img = background("navy")
    d = ImageDraw.Draw(img)
    text(d, (W // 2, 170), sc["label"].upper(), 50, "Bold", (170, 190, 220))
    val = int(sc["to"] * ease(min(1.0, p * 1.4)))
    cx, cy, r = W // 2, 540, 290
    d.arc((cx - r, cy - r, cx + r, cy + r), 0, 360, fill=(255, 255, 255, 30), width=26)
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * ease(min(1.0, p * 1.4)), fill=YELLOW, width=26)
    text(d, (cx, cy - 20), f"{val}", 260, "ExtraBold", WHITE)
    text(d, (cx, cy + 150), sc["unit"], 52, "Bold", YELLOW)
    text(d, (W // 2, 905), sc["sub"], 44, "SemiBold", (205, 215, 230))
    return img


def scene_timeline(sc, p, lt):
    img = background("paper")
    d = ImageDraw.Draw(img)
    items = sc["items"]
    n = len(items)
    xs = [W / 2] if n == 1 else [300 + j * (W - 600) / (n - 1) for j in range(n)]
    y = 560
    prog = ease(min(1.0, p * 1.2))
    d.line([(xs[0] - 140, y), (xs[-1] + 140, y)], fill=(205, 211, 221), width=10)
    d.line([(xs[0] - 140, y), (xs[0] - 140 + (xs[-1] - xs[0] + 280) * prog, y)], fill=BLUE, width=10)
    for j, (big, cap) in enumerate(items):
        appear = 0.05 + 0.75 * j / max(1, n)
        k = out_back((p - appear) / 0.16)
        if k <= 0.02:
            continue
        lay = layer()
        ld = ImageDraw.Draw(lay)
        col = [BLUE, GREEN, ORANGE][j % 3]
        x = xs[j]
        ld.ellipse((x - 26, y - 26, x + 26, y + 26), fill=WHITE, outline=col, width=12)
        size = 104 if len(big) <= 6 else 72
        ld.text((x, y - 140), big, font=font(size, "ExtraBold"), fill=col, anchor="mm")
        f = font(42, "SemiBold")
        for q, ln in enumerate(wrap(cap, f, 470 if n < 3 else 400)):
            ld.text((x, y + 100 + q * 54), ln, font=f, fill=INK, anchor="mm")
        paste_scaled(img, lay, x, y, k)
    return img


def typed(s, p):
    n = int(len(s) * min(1.0, max(0.0, p)))
    return s[:n]


def scene_chat(sc, p, lt):
    img = background("paper")
    d = ImageDraw.Draw(img)
    f = font(50, "SemiBold")
    pr = typed(sc["prompt"], (p - 0.05) / 0.3)
    rp = typed(sc["reply"], (p - 0.5) / 0.4)
    # user bubble (right)
    if pr:
        lines = wrap(sc["prompt"], f, 900)
        bw = max(f.getlength(l) for l in lines) + 90
        bh = len(lines) * 66 + 60
        x1 = W - 260
        rrect(d, (x1 - bw, 230, x1, 230 + bh), 44, fill=BLUE)
        shown = wrap(pr, f, 900) if pr else []
        for q, l in enumerate(wrap(sc["prompt"], f, 900)):
            vis = pr[sum(len(x) + 1 for x in lines[:q]):][: len(l)] if q < len(shown) or pr else ""
            vis = pr[sum(len(x) + 1 for x in lines[:q]): sum(len(x) + 1 for x in lines[:q]) + len(l)]
            d.text((x1 - bw + 45, 262 + q * 66), vis, font=f, fill=WHITE, anchor="lt")
    # assistant bubble (left)
    if p > 0.36:
        lines = wrap(sc["reply"], f, 1000)
        bw = max(f.getlength(l) for l in lines) + 90
        bh = len(lines) * 66 + 60
        y0 = 230 + (len(wrap(sc["prompt"], f, 900)) * 66 + 60) + 70
        rrect(d, (260, y0, 260 + bw, y0 + bh), 44, fill=WHITE, outline=(200, 207, 218), width=4)
        d.ellipse((190, y0 + 10, 250, y0 + 70), fill=INK)
        text(d, (220, y0 + 40), "AI", 28, "ExtraBold", WHITE)
        if not rp:
            for q in range(3):
                a = 0.5 + 0.5 * math.sin(lt * 9 - q)
                c = int(190 - 80 * a)
                d.ellipse((300 + q * 40, y0 + bh / 2 - 9, 318 + q * 40, y0 + bh / 2 + 9), fill=(c, c, c + 10))
        for q, l in enumerate(lines):
            off = sum(len(x) + 1 for x in lines[:q])
            vis = rp[off: off + len(l)]
            d.text((260 + 45, y0 + 30 + q * 66), vis, font=f, fill=INK, anchor="lt")
    return img


def draw_hand(d, cx, cy, s, fingers=7, jitter=0.0, col=(224, 180, 150)):
    d.ellipse((cx - 150 * s, cy - 40 * s, cx + 150 * s, cy + 190 * s), fill=col)
    for j in range(fingers):
        a = -math.pi * (0.1 + 0.8 * j / (fingers - 1))
        L = (190 + 40 * math.sin(j * 1.9)) * s
        bx, by = cx + 110 * s * math.cos(a), cy + 20 * s + 80 * s * math.sin(a)
        ex = bx + L * math.cos(a) + jitter * math.sin(j * 7) * 20
        ey = by + L * math.sin(a)
        d.line([(bx, by), (ex, ey)], fill=col, width=int(44 * s))
        d.ellipse((ex - 22 * s, ey - 22 * s, ex + 22 * s, ey + 22 * s), fill=col)


def panel_art(kind, d, box, lt, bad):
    x0, y0, x1, y1 = box
    w_, h_ = x1 - x0, y1 - y0
    if kind == "image":
        if bad:
            d.rectangle(box, fill=(198, 190, 214))
            draw_hand(d, x0 + w_ / 2, y0 + h_ * 0.42, 1.05, 7, 1.0)
            for j in range(6):
                yy = y0 + ((j * 97 + int(lt * 60)) % int(h_))
                d.rectangle((x0, yy, x1, yy + 7), fill=(140, 130, 170))
        else:
            for yy in range(int(h_)):
                k = yy / h_
                d.line([(x0, y0 + yy), (x1, y0 + yy)], fill=(int(255 - 70 * k), int(176 + 20 * k), int(110 + 90 * k)))
            d.ellipse((x0 + w_ * 0.62, y0 + h_ * 0.18, x0 + w_ * 0.62 + 140, y0 + h_ * 0.18 + 140), fill=(255, 238, 190))
            d.polygon([(x0, y1), (x0 + w_ * 0.32, y0 + h_ * 0.52), (x0 + w_ * 0.58, y1)], fill=(52, 80, 112))
            d.polygon([(x0 + w_ * 0.35, y1), (x0 + w_ * 0.7, y0 + h_ * 0.42), (x1, y1)], fill=(36, 62, 92))
            d.rectangle((x0, y0 + h_ * 0.86, x1, y1), fill=(26, 46, 70))
    else:  # video
        if bad:
            bs = 36
            rng = np.random.default_rng(int(lt * 8))
            for gx in range(int(w_ // bs) + 1):
                for gy in range(int(h_ // bs) + 1):
                    v = int(rng.integers(70, 190))
                    d.rectangle((x0 + gx * bs, y0 + gy * bs, min(x1, x0 + gx * bs + bs), min(y1, y0 + gy * bs + bs)),
                                fill=(v, v - 10, v + 20))
            text(d, ((x0 + x1) / 2, (y0 + y1) / 2), "0:02", 110, "ExtraBold", WHITE)
        else:
            art = (x0, y0, x1, y1)
            panel_art("image", d, art, lt, False)
            for j in range(40):
                hh = 20 + 70 * abs(math.sin(j * 0.7 + lt * 7))
                cxx = x0 + 40 + j * (w_ - 80) / 39
                d.rectangle((cxx - 5, y1 - 40 - hh, cxx + 5, y1 - 40), fill=WHITE)
            text(d, (x1 - 110, y0 + 50), "0:30", 54, "ExtraBold", WHITE)


def scene_compare(sc, p, lt):
    img = background("paper")
    d = ImageDraw.Draw(img)
    (ly, lc), (ry, rc) = sc["left"], sc["right"]
    plain = sc.get("plain")
    kind = "video" if "second" in lc else "image"
    L = (130, 250, 930, 800)
    R = (990, 250, 1790, 800)
    for side, (yr, cap), box, bad, col in (("l", (ly, lc), L, True, RED), ("r", (ry, rc), R, False, GREEN)):
        appear = 0.08 if side == "l" else 0.38
        k = out_back((p - appear) / 0.2)
        if k <= 0.02:
            continue
        lay = layer()
        ld = ImageDraw.Draw(lay)
        rrect(ld, (box[0] - 14, box[1] - 14, box[2] + 14, box[3] + 14), 30, fill=WHITE, outline=col, width=8)
        if plain:
            ld.rectangle(box, fill=(236, 240, 246))
            col2 = ORANGE if side == "l" else RED
            f = font(64, "ExtraBold")
            for q, ln in enumerate(wrap(cap, f, 680)):
                ld.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2 - 40 + q * 84), ln, font=f,
                        fill=GREEN if yr == "could" and side == "l" else RED, anchor="mm")
        else:
            if sc.get("reveal") and side == "r":
                wipe = ease((p - 0.4) / 0.45)
                tmp = layer()
                td = ImageDraw.Draw(tmp)
                panel_art(kind, td, box, lt, bad)
                crop = tmp.crop((box[0], box[1], box[0] + int((box[2] - box[0]) * wipe), box[3]))
                lay.alpha_composite(crop, (box[0], box[1]))
            else:
                panel_art(kind, ld, box, lt, bad)
        ld.text(((box[0] + box[2]) / 2, box[1] - 80), yr, font=font(76, "ExtraBold"), fill=col, anchor="mm")
        if not plain:
            ld.text(((box[0] + box[2]) / 2, box[3] + 80), cap, font=font(46, "SemiBold"), fill=INK, anchor="mm")
        paste_scaled(img, lay, (box[0] + box[2]) / 2, (box[1] + box[3]) / 2, k)
    return img


def scene_bars(sc, p, lt):
    img = background("paper")
    d = ImageDraw.Draw(img)
    text(d, (W // 2, 130), sc["head"].upper(), 50, "ExtraBold", INK)
    if sc.get("doubling"):
        n = 6
        base = 840
        for j in range(n):
            k = out_back((p - 0.05 - j * 0.11) / 0.18)
            if k <= 0.02:
                continue
            h_ = 40 * (2 ** j) * 0.62 * min(1, k)
            x = 330 + j * 240
            col = [ORANGE, ORANGE, GREEN, GREEN, BLUE, BLUE][j]
            rrect(d, (x, base - h_, x + 170, base), 18, fill=col)
            text(d, (x + 85, base + 40), f"x{2 ** j}", 40, "ExtraBold", INK)
        text(d, (W // 2, 935), "illustrative: each step doubles", 38, "SemiBold", (110, 120, 138))
    elif sc.get("drop"):
        zero = 700
        k1 = ease((p - 0.1) / 0.3)
        k2 = ease((p - 0.4) / 0.4)
        rrect(d, (520, zero - 260 * k1, 820, zero), 14, fill=GREEN)
        rrect(d, (1100, zero, 1400, zero + 300 * k2), 14, fill=RED)
        d.line([(380, zero), (1540, zero)], fill=INK, width=6)
        text(d, (670, zero + 70), "Less exposed", 44, "Bold", INK)
        text(d, (1250, zero - 60), "Most AI-exposed", 44, "Bold", INK)
        text(d, (W // 2, 935), "illustrative: direction of change since 2022, not exact figures", 36, "SemiBold",
             (110, 120, 138))
    else:
        items = sc["items"]
        for j, (lab, frac) in enumerate(items):
            k = ease((p - 0.08 - j * 0.12) / 0.3)
            y = 330 + j * 150
            text(d, (520, y), lab, 52, "Bold", INK, "rm")
            rrect(d, (560, y - 40, 560 + 1000 * frac * k, y + 40), 22, fill=[BLUE, GREEN, ORANGE, TEAL][j % 4])
    return img


def scene_stat(sc, p, lt):
    img = background("navy")
    d = ImageDraw.Draw(img)
    big = sc["big"]
    size = 300
    while font(size, "ExtraBold").getlength(big) > 1650:
        size -= 10
    k = out_back(lt / 0.4)
    lay = layer()
    ld = ImageDraw.Draw(lay)
    ld.text((W // 2, H // 2 - 50), big, font=font(size, "ExtraBold"), fill=WHITE, anchor="mm")
    paste_scaled(img, lay, W // 2, H // 2 - 50, 0.6 + 0.4 * min(1.1, k), min(1.0, lt / 0.2))
    bw = font(size, "ExtraBold").getlength(big) * ease((lt - 0.2) / 0.5)
    d.rectangle((W // 2 - bw / 2, H // 2 + size * 0.42, W // 2 + bw / 2, H // 2 + size * 0.42 + 12), fill=YELLOW)
    a = ease((lt - 0.45) / 0.4)
    lay = layer()
    ImageDraw.Draw(lay).text((W // 2, H // 2 + size * 0.42 + 100), sc["small"], font=font(60, "SemiBold"),
                             fill=YELLOW, anchor="mm")
    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(lay)
    return img


def scene_wave(sc, p, lt):
    img = background("navy")
    d = ImageDraw.Draw(img)
    text(d, (W // 2, 180), sc["label"].upper(), 56, "ExtraBold", WHITE)
    n = 70
    for row, (cy, col, show) in enumerate(((480, TEAL, True), (780, YELLOW, p > 0.4))):
        if not show:
            continue
        for j in range(n):
            amp = abs(math.sin(j * 0.45 + lt * (6 + row * 2)) * math.sin(j * 0.13 + lt * 3 + row)) * 130 + 12
            x = 190 + j * (W - 380) / (n - 1)
            d.rounded_rectangle((x - 9, cy - amp, x + 9, cy + amp), radius=9, fill=col)
    text(d, (W // 2, 905), "original  ·  copy" if p > 0.4 else "original", 40, "SemiBold", (170, 190, 220))
    return img


_NODES = None


def scene_network(sc, p, lt):
    global _NODES
    img = background("navy")
    d = ImageDraw.Draw(img)
    layers = [4, 6, 6, 3]
    if _NODES is None:
        _NODES = [[(300 + li * 440, 260 + (j + 0.5) * 560 / n) for j in range(n)] for li, n in enumerate(layers)]
    for li in range(len(layers) - 1):
        for a_ in _NODES[li]:
            for b_ in _NODES[li + 1]:
                d.line([a_, b_], fill=(255, 255, 255, 26), width=2)
    # pulses
    for li in range(len(layers) - 1):
        for ia, a_ in enumerate(_NODES[li]):
            for ib, b_ in enumerate(_NODES[li + 1]):
                ph = (lt * 0.9 + (ia * 7 + ib * 3 + li * 5) * 0.137) % 1.0
                if ph < 0.35:
                    t_ = ph / 0.35
                    x, y = a_[0] + (b_[0] - a_[0]) * t_, a_[1] + (b_[1] - a_[1]) * t_
                    d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=YELLOW)
    for li, ns in enumerate(_NODES):
        for j, (x, y) in enumerate(ns):
            glow = 0.5 + 0.5 * math.sin(lt * 3 + li + j)
            r = 22
            d.ellipse((x - r, y - r, x + r, y + r), fill=(int(40 + 40 * glow), int(120 + 60 * glow), 200))
            d.ellipse((x - r, y - r, x + r, y + r), outline=WHITE, width=3)
    k = out_back(lt / 0.5)
    lay = layer()
    ImageDraw.Draw(lay).text((W // 2, 900), sc["label"], font=font(84, "ExtraBold"), fill=WHITE, anchor="mm",
                             stroke_width=8, stroke_fill=NAVY)
    paste_scaled(img, lay, W // 2, 900, 0.7 + 0.3 * min(1.0, k), min(1.0, lt / 0.25))
    return img


def scene_quote(sc, p, lt):
    img = background("navy")
    d = ImageDraw.Draw(img)
    f = font(104, "ExtraBold")
    lines = wrap(sc["text"], f, 1500)
    text(d, (W // 2, 230), "“", 330, "ExtraBold", YELLOW)
    shown = typed(sc["text"], (p - 0.05) / 0.55)
    y0 = H // 2 - (len(lines) - 1) * 62 + 30
    off = 0
    for q, l in enumerate(lines):
        vis = shown[off: off + len(l)]
        off += len(l) + 1
        d.text((W // 2, y0 + q * 124), vis, font=f, fill=WHITE, anchor="mm")
    return img


SCENES = dict(title=scene_title, curve=scene_curve, list=scene_list, counter=scene_counter, timeline=scene_timeline,
              chat=scene_chat, compare=scene_compare, bars=scene_bars, stat=scene_stat, wave=scene_wave,
              network=scene_network, quote=scene_quote)


# ------------------------------------------------------------------ subtitles
def build_cues(max_words=8):
    cues = []
    for i, line in enumerate(LINES):
        words = line.split()
        n = math.ceil(len(words) / max_words)
        size = len(words) / n
        bounds = [round(size * k) for k in range(n + 1)]
        for j, k in zip(bounds[:-1], bounds[1:]):
            t0 = starts[i] + TW[i][j] - 0.08
            t1 = starts[i] + TW[i][k] - 0.05 if k < len(words) else starts[i] + D[i] + 0.25
            cues.append((t0, t1, " ".join(words[j:k])))
    return cues


CUES = build_cues()


def subtitles(img, t):
    for t0, t1, txt in CUES:
        if t0 <= t < t1:
            f = font(38, "SemiBold")
            w_ = f.getlength(txt)
            y = H - 62
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            d.rounded_rectangle((W / 2 - w_ / 2 - 18, y - 27, W / 2 + w_ / 2 + 18, y + 27), radius=12,
                                fill=(0, 0, 0, 135))
            d.text((W / 2, y), txt, font=f, fill=(255, 255, 255, 245), anchor="mm")
            img.alpha_composite(lay)
            return


def frame(fi):
    t = fi / FPS
    s = shot_at(t)
    sc = s["sc"]
    p = (t - s["t0"]) / max(0.01, s["t1"] - s["t0"])
    lt = t - s["t0"]
    if sc["t"] == "clip":
        img = clip_frame(s, t)
    else:
        img = SCENES[sc["t"]](sc, p, lt)
        # slow push-in so graphics are never static
        z = 1.0 + 0.025 * p
        cw, ch = int(W / z), int(H / z)
        x0, y0 = (W - cw) // 2, (H - ch) // 2
        img = img.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.BILINEAR)
    subtitles(img, t)
    return img.convert("RGB")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prep":
        prep()
    elif cmd == "info":
        print("frames", NF, "total", round(TOTAL, 1), "shots", len(SHOTS))
        from collections import Counter
        print(Counter(s["sc"]["t"] for s in SHOTS))
    elif cmd == "still":
        frame(int(sys.argv[2])).save(f"still_{sys.argv[2]}.png")
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                              f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                              "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 60 == 0:
                print(fi, flush=True)
        p.stdin.close()
        p.wait()
