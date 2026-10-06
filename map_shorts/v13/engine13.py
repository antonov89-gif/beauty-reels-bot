"""v13: long-form 16:9 'The No.1 company of every country' in the ¿Y si? style.

Map cards (teal water / cream land, flag + country top-left, red pin, company plate, number badge)
alternate with stock footage. Small phrase subtitles.

python3 engine13.py prep | info | still N | video A B out.mp4
"""
import json
import math
import os
import subprocess
import sys

import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from script13 import SCRIPT, LINES

W, H, FPS = 1920, 1080, 30
MONT = "/home/claude/v12/Montserrat.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
NE = "/home/claude/v10/assets/ne50/ne_50m_admin_0_countries.shp"

WATER = (79, 157, 186)
LAND = (241, 234, 216)
BORDER = (205, 196, 176)
PIN = (226, 47, 43)
NAVY = (24, 44, 72)
INK = (30, 30, 34)

TM = json.load(open("timing.json"))
D, TW = TM["D"], TM["T"]
LEAD = TM.get("voice_offset", 0.4)
starts = [LEAD + s for s in TM["starts"]]
TOTAL = starts[-1] + D[-1] + 2.0
NF = int(TOTAL * FPS)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


_F = {}


def font(size, weight="Bold"):
    key = (int(size), weight)
    if key not in _F:
        f = ImageFont.truetype(MONT, max(1, int(size)))
        f.set_variation_by_name(weight)
        _F[key] = f
    return _F[key]


# ---------------------------------------------------------------- timeline
NARR_CLIPS = {0: "intro", 2: "sugar", 18: "cargo", len(SCRIPT) - 1: "outro"}
SHOTS = []
num = 0
for i, (text, card) in enumerate(SCRIPT):
    t0 = 0.0 if i == 0 else starts[i] - 0.15
    t1 = (starts[i + 1] - 0.15) if i + 1 < len(SCRIPT) else TOTAL
    if card is None:
        SHOTS.append(dict(t0=t0, t1=t1, kind="clip", src=NARR_CLIPS.get(i, "intro"), line=i))
        continue
    num += 1
    seg = t1 - t0
    if card.get("clip") and seg > 4.2:
        mid = t0 + max(2.8, min(4.0, seg * 0.5))
        SHOTS.append(dict(t0=t0, t1=mid, kind="card", card=card, num=num, line=i))
        SHOTS.append(dict(t0=mid, t1=t1, kind="clip", src=card["clip"], line=i))
    else:
        SHOTS.append(dict(t0=t0, t1=t1, kind="card", card=card, num=num, line=i))


def shot_at(t):
    for s in SHOTS:
        if s["t0"] <= t < s["t1"]:
            return s
    return SHOTS[-1]


# ---------------------------------------------------------------- clips
def clip_dir(s):
    return f"frames/{s['src']}_{int(s['t0'] * 10)}"


def prep():
    os.makedirs("frames", exist_ok=True)
    used = {}
    for s in SHOTS:
        if s["kind"] != "clip":
            continue
        src = f"media/{s['src']}.mp4"
        dur = s["t1"] - s["t0"] + 0.2
        probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                               capture_output=True, text=True).stdout.strip()
        clen = float(probe or 0)
        # use a different part of the clip each time it is reused
        off = used.get(s["src"], 0.5)
        if off + dur > clen:
            off = max(0, clen - dur - 0.1)
        used[s["src"]] = off + dur
        speed = 1.0 if clen >= dur else clen / dur * 0.98
        out = clip_dir(s)
        if os.path.isdir(out) and len(os.listdir(out)) >= int(dur * FPS) - 2:
            continue
        os.makedirs(out, exist_ok=True)
        vf = (f"setpts={1 / speed:.4f}*PTS,scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
              f"fps=30")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{off:.2f}", "-i", src, "-t",
                        f"{dur / speed if speed < 1 else dur:.2f}", "-vf", vf, "-frames:v", str(int(dur * FPS) + 2),
                        "-q:v", "3", f"{out}/%05d.jpg"], check=True)
        print("clip", out, len(os.listdir(out)), flush=True)


def clip_frame(s, t):
    d = clip_dir(s)
    n = len([f for f in os.listdir(d) if f.endswith(".jpg")])
    i = max(1, min(n, int((t - s["t0"]) * FPS) + 1))
    return Image.open(f"{d}/{i:05d}.jpg").convert("RGB")


# ---------------------------------------------------------------- map
_SHP = shapefile.Reader(NE)
RINGS = []
for sr in _SHP.iterShapeRecords():
    pts = sr.shape.points
    parts = list(sr.shape.parts) + [len(pts)]
    for a, b in zip(parts[:-1], parts[1:]):
        RINGS.append(np.array(pts[a:b]))


def merc(lat):
    lat = np.clip(lat, -84, 84)
    return np.degrees(np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)))


def base_map(card, scale=1.18):
    """Render the card's map once at scale x frame size (cropped per frame for a slow push-in)."""
    w, h = int(W * scale), int(H * scale)
    span = card["span"] * scale
    ppd = w / span
    cy = merc(card["lat"])
    img = Image.new("RGB", (w * 2, h * 2), WATER)  # 2x supersample
    d = ImageDraw.Draw(img)
    for r in RINGS:
        for shift in (-360, 0, 360):
            x = ((r[:, 0] + shift) - card["lon"]) * ppd * 2 + w
            y = (cy - merc(r[:, 1])) * ppd * 2 + h
            if x.max() < 0 or x.min() > 2 * w or y.max() < 0 or y.min() > 2 * h:
                continue
            pts = list(zip(x.tolist(), y.tolist()))
            if len(pts) > 2:
                d.polygon(pts, fill=LAND, outline=BORDER, width=3)
    return img.resize((w, h), Image.LANCZOS)


_BASE = {}


def flag_img(flag, height):
    if flag == "🏴":  # Scotland: draw the saltire
        w = int(height * 1.5)
        im = Image.new("RGBA", (w, height), (0, 94, 184, 255))
        d = ImageDraw.Draw(im)
        th = max(3, height // 6)
        d.line([(0, 0), (w, height)], fill=(255, 255, 255, 255), width=th)
        d.line([(0, height), (w, 0)], fill=(255, 255, 255, 255), width=th)
        return im
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (150, 136), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((75, 68), flag, font=f, embedded_color=True, anchor="mm")
    im = im.crop(im.getbbox())
    return im.resize((int(im.width * height / im.height), height), Image.LANCZOS)


def card_frame(s, t):
    c = s["card"]
    key = id(s)
    if key not in _BASE:
        _BASE[key] = base_map(c)
    base = _BASE[key]
    k = ease((t - s["t0"]) / max(0.1, s["t1"] - s["t0"]))
    z = 1.0 + 0.12 * k  # slow push-in on the pin
    bw, bh = base.width / z, base.height / z
    x0, y0 = (base.width - bw) / 2, (base.height - bh) / 2
    img = base.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh)).convert("RGBA")
    d = ImageDraw.Draw(img)
    # pin at the card centre (the map is centred on the company location)
    px, py = W / 2, H / 2
    pk = ease((t - s["t0"] - 0.15) / 0.25)
    if pk > 0:
        r = 21 * pk
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse((px - 12, py - 4, px + 12, py + 6), fill=(0, 0, 0, 90))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
        d.polygon([(px, py), (px - r * 0.85, py - r * 1.5), (px + r * 0.85, py - r * 1.5)], fill=PIN)
        d.ellipse((px - r, py - r * 2.6, px + r, py - r * 0.6), fill=PIN)
        d.ellipse((px - r * 0.4, py - r * 2.0, px + r * 0.4, py - r * 1.2), fill=(255, 255, 255))
    # company plate (logo-style wordmark on a white card), offset from the pin
    ck = ease((t - s["t0"] - 0.35) / 0.3)
    if ck > 0:
        fz = font(54 if len(c["company"]) < 16 else 44, "ExtraBold")
        tw = fz.getlength(c["company"])
        bx, by = px + 60, py - 150
        if bx + tw + 70 > W - 60:
            bx = px - 60 - tw - 70
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        a = int(255 * ck)
        ld.rounded_rectangle((bx + 6, by + 8, bx + tw + 70 + 6, by + 100 + 8), radius=18, fill=(0, 0, 0, int(60 * ck)))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(6)))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle((bx, by, bx + tw + 70, by + 100), radius=18, fill=(255, 255, 255, a))
        ld.text((bx + 35, by + 50), c["company"], font=fz, fill=NAVY + (a,), anchor="lm")
        img.alpha_composite(lay)
    # title: flag + COUNTRY, top-left
    fl = flag_img(c["flag"], 70)
    img.alpha_composite(fl, (60, 52))
    name = c["country"].upper()
    tf = font(68, "ExtraBold")
    tx = 60 + fl.width + 26
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((tx + 3, 88 + 4), name, font=tf, fill=(0, 0, 0, 140), anchor="lm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
    d = ImageDraw.Draw(img)
    d.text((tx, 88), name, font=tf, fill=(255, 255, 255), anchor="lm", stroke_width=4, stroke_fill=(20, 30, 45))
    # number badge, bottom-left
    cx, cy = 96, H - 96
    d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), fill=(255, 255, 255), outline=NAVY, width=5)
    d.text((cx, cy + 2), str(s["num"]), font=font(40, "ExtraBold"), fill=NAVY, anchor="mm")
    return img


# ---------------------------------------------------------------- subtitles
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
            y = H - 70
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(lay)
            d.rounded_rectangle((W / 2 - w_ / 2 - 18, y - 27, W / 2 + w_ / 2 + 18, y + 27), radius=12,
                                fill=(0, 0, 0, 125))
            d.text((W / 2, y), txt, font=f, fill=(255, 255, 255, 245), anchor="mm")
            img.alpha_composite(lay)
            return


def title_overlay(img, t):
    if t < 0.6 or t > starts[1] - 0.3:
        return
    k = ease((t - 0.6) / 0.5)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, int(90 * k)))
    img.alpha_composite(lay)
    d = ImageDraw.Draw(img)
    a = int(255 * k)
    d.text((W / 2, H / 2 - 40), "THE No.1 COMPANY", font=font(110, "ExtraBold"), fill=(255, 255, 255, a), anchor="mm")
    d.text((W / 2, H / 2 + 80), "OF EVERY COUNTRY", font=font(84, "Bold"), fill=(255, 214, 120, a), anchor="mm")
    d.text((W / 2, H / 2 + 170), "PART 1", font=font(44, "SemiBold"), fill=(255, 255, 255, a), anchor="mm")


def frame(fi):
    t = fi / FPS
    s = shot_at(t)
    if s["kind"] == "clip":
        img = clip_frame(s, t).convert("RGBA")
    else:
        img = card_frame(s, t)
    if s["line"] == 0:
        title_overlay(img, t)
    subtitles(img, t)
    return img.convert("RGB")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prep":
        prep()
    elif cmd == "info":
        print("frames", NF, "total", round(TOTAL, 1), "shots", len(SHOTS))
    elif cmd == "still":
        frame(int(sys.argv[2])).save(f"still_{sys.argv[2]}.png")
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "fast",
                              "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 60 == 0:
                print(fi, flush=True)
        p.stdin.close()
        p.wait()
