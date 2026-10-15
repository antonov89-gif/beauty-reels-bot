"""GTA 6-style covers from the already-paid in-engine keyframes (free). python3 cover_v2.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
WHT, BLK, RED = (255, 255, 255), (0, 0, 0), (232, 36, 36)
def font(s): return ImageFont.truetype("Poppins-ExtraBold.ttf", int(s))
def cover(p):
    im = Image.open(p).convert("RGB"); iw, ih = im.size; s = max(W / iw, H / ih)
    im = im.resize((int(iw * s + .5), int(ih * s + .5)), Image.LANCZOS); x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x0, y0, x0 + W, y0 + H))
def grade(im, warm=0.10, sat=1.18, con=1.10):
    im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(sat)).enhance(con)
    a = np.asarray(im).astype(np.float32); a = a * (1 - warm) + np.array([255, 120, 120], np.float32) * warm
    # vignette
    yy, xx = np.mgrid[0:H, 0:W]; v = 1 - 0.32 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    return Image.fromarray(np.clip(a * v[..., None], 0, 255).astype(np.uint8))
def grad_text(img, txt, cy, size, maxw=W - 110, sw=14, stops=((255, 190, 40), (255, 70, 120), (170, 60, 220))):
    f = font(size)
    while f.getlength(txt) > maxw: f = font(f.size - 2)
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).text((W / 2, cy), txt, font=f, fill=255, anchor="mm")
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 6, cy + 14), txt, font=f, fill=(0, 0, 0, 220), anchor="mm", stroke_width=sw + 6, stroke_fill=(0, 0, 0, 220))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(img).text((W / 2, cy), txt, font=f, fill=(0, 0, 0, 255), anchor="mm", stroke_width=sw, stroke_fill=WHT)
    bb = m.getbbox(); y0, y1 = bb[1], bb[3]
    g = np.zeros((H, W, 3), np.uint8)
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0); k = t * (len(stops) - 1); i = min(int(k), len(stops) - 2); u = k - i
        g[y] = [int(stops[i][c] * (1 - u) + stops[i + 1][c] * u) for c in range(3)]
    layer = Image.fromarray(g).convert("RGBA"); layer.putalpha(m); img.alpha_composite(layer)
def pill(img, txt, cx, cy, sz, bg, rot=0):
    f = font(sz); pw, ph = int(f.getlength(txt) + sz), int(sz * 1.7)
    lay = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), sz * .4, fill=bg + (255,), outline=WHT, width=5)
    d.text((20 + pw / 2, 20 + ph / 2), txt, font=f, fill=WHT, anchor="mm", stroke_width=2, stroke_fill=BLK)
    lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); al = lay.split()[3].point(lambda v: int(v * .6))
    s.paste((0, 0, 0, 255), (int(cx - lay.width / 2 + 7), int(cy - lay.height / 2 + 11)), al)
    img.alpha_composite(s.filter(ImageFilter.GaussianBlur(9))); img.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))
def inset(img, cx, cy, r):
    sat = Image.open("sat_miami.jpg").convert("RGB").crop((380, 700, 380 + 520, 700 + 520)).resize((2 * r, 2 * r), Image.LANCZOS)
    m = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((cx - r + 6, cy - r + 14, cx + r + 6, cy + r + 14), fill=(0, 0, 0, 200))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((cx - r - 9, cy - r - 9, cx + r + 9, cy + r + 9), fill=WHT)
    img.alpha_composite(ring); sat = sat.convert("RGBA"); sat.putalpha(m); img.alpha_composite(sat, (cx - r, cy - r))
    d = ImageDraw.Draw(img); d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=RED, outline=WHT, width=6)
    pill(img, "REAL MIAMI", cx, cy + r + 52, 38, (20, 150, 90), -3)
def make(src, out, title2="REAL FLORIDA?", crop_y=0):
    img = grade(cover(src)).convert("RGBA")
    a = np.asarray(img.convert("RGB")).astype(np.float32); g = np.clip(1 - np.linspace(0.55, 0, 620), 0, 1); a[:620] *= g[:, None, None]
    img = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    grad_text(img, "GTA 6 =", 165, 190); grad_text(img, title2, 345, 160)
    inset(img, 790, 1380, 190)
    pill(img, "AI CONCEPT", 175, 1130 + 520, 34, (30, 30, 50), 0)
    img.convert("RGB").save(out, quality=93)

def make_hero(src, out):
    img = grade(cover(src), warm=0.06, sat=1.22, con=1.12).convert("RGBA")
    a = np.asarray(img.convert("RGB")).astype(np.float32); g = np.clip(1 - np.linspace(0.62, 0, 640), 0, 1); a[:640] *= g[:, None, None]
    img = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
    grad_text(img, "GTA 6 =", 165, 190); grad_text(img, "REAL FLORIDA?", 345, 160)
    inset(img, 805, 1560, 185)
    pill(img, "AI CONCEPT", 175, 1810, 34, (30, 30, 50), 0)
    img.convert("RGB").save(out, quality=93)
make_hero("hero.jpg", "cover_hero.jpg"); print("ok")
