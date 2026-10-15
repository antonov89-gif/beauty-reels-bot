"""Gold cube Short covers from the already generated keyframes (free). python3 gold_cover.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
WHT, BLK, RED, YEL = (255, 255, 255), (0, 0, 0), (232, 36, 36), (255, 214, 10)
KF = "keyframes/"
def tf(s): return ImageFont.truetype("fonts/titan-one.ttf", int(s))
def pf(s): return ImageFont.truetype("Poppins-ExtraBold.ttf", int(s))
def cover(p, dy=0):
    im = Image.open(p).convert("RGB"); iw, ih = im.size; s = max(W / iw, H / ih)
    im = im.resize((int(iw * s + .5), int(ih * s + .5)), Image.LANCZOS); x0, y0 = (im.width - W) // 2, (im.height - H) // 2 + dy
    return im.crop((x0, y0, x0 + W, y0 + H))
def grade(im):
    return ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(1.15)).enhance(1.08)
def gold_text(img, txt, cy, size, maxw=W - 90, sw=16, fill_stops=((255, 245, 170), (255, 205, 40), (214, 140, 10))):
    f = tf(size)
    while f.getlength(txt) > maxw: f = tf(f.size - 2)
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).text((W / 2, cy), txt, font=f, fill=255, anchor="mm")
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 5, cy + 14), txt, font=f, fill=(0, 0, 0, 230), anchor="mm", stroke_width=sw + 4, stroke_fill=(0, 0, 0, 230))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    d = ImageDraw.Draw(img); d.text((W / 2, cy), txt, font=f, fill=BLK, anchor="mm", stroke_width=sw, stroke_fill=BLK)
    d.text((W / 2, cy), txt, font=f, fill=WHT, anchor="mm", stroke_width=5, stroke_fill=WHT)
    y0, y1 = m.getbbox()[1], m.getbbox()[3]; g = np.zeros((H, W, 3), np.uint8)
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0); k = t * (len(fill_stops) - 1); i = min(int(k), len(fill_stops) - 2); u = k - i
        g[y] = [int(fill_stops[i][c] * (1 - u) + fill_stops[i + 1][c] * u) for c in range(3)]
    layer = Image.fromarray(g).convert("RGBA"); layer.putalpha(m.filter(ImageFilter.MinFilter(9))); img.alpha_composite(layer)
def plain_text(img, txt, cy, size, col=WHT, maxw=W - 90, sw=12):
    f = tf(size)
    while f.getlength(txt) > maxw: f = tf(f.size - 2)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 5, cy + 12), txt, font=f, fill=(0, 0, 0, 220), anchor="mm", stroke_width=sw + 4, stroke_fill=(0, 0, 0, 220))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(img).text((W / 2, cy), txt, font=f, fill=col, anchor="mm", stroke_width=sw, stroke_fill=BLK)
def pill(img, txt, cx, cy, sz, bg, rot=0, fg=WHT):
    f = pf(sz); pw, ph = int(f.getlength(txt) + sz), int(sz * 1.7)
    lay = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), sz * .4, fill=bg + (255,), outline=WHT, width=5)
    d.text((20 + pw / 2, 20 + ph / 2), txt, font=f, fill=fg, anchor="mm", stroke_width=2, stroke_fill=BLK)
    lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); al = lay.split()[3].point(lambda v: int(v * .6))
    s.paste((0, 0, 0, 255), (int(cx - lay.width / 2 + 7), int(cy - lay.height / 2 + 11)), al)
    img.alpha_composite(s.filter(ImageFilter.GaussianBlur(9))); img.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))
def ring_arrow(img, tx, ty, r, ax, ay):
    d = ImageDraw.Draw(img)
    d.ellipse((tx - r - 5, ty - r - 5, tx + r + 5, ty + r + 5), outline=BLK, width=18); d.ellipse((tx - r, ty - r, tx + r, ty + r), outline=RED, width=10)
    import math
    ang = math.atan2(ty - ay, tx - ax); ex, ey = tx - math.cos(ang) * (r + 12), ty - math.sin(ang) * (r + 12)
    d.line([(ax, ay), (ex, ey)], fill=BLK, width=22); d.line([(ax, ay), (ex, ey)], fill=RED, width=12)
    hx, hy = ex, ey; L = 46
    pts = [(hx, hy), (hx - math.cos(ang - .5) * L, hy - math.sin(ang - .5) * L), (hx - math.cos(ang + .5) * L, hy - math.sin(ang + .5) * L)]
    d.polygon(pts, fill=BLK); d.polygon([(hx - math.cos(ang) * 6, hy - math.sin(ang) * 6)] + pts[1:], fill=RED)
def veil(img, h=620, k=0.5):
    a = np.asarray(img.convert("RGB")).astype(np.float32); g = np.clip(1 - np.linspace(k, 0, h), 0, 1); a[:h] *= g[:, None, None]
    return Image.fromarray(a.astype(np.uint8)).convert("RGBA")

# A: cube under the Eiffel Tower
img = veil(grade(cover(KF + "kf_s4.jpg")).convert("RGBA"), 560, .42)
gold_text(img, "ALL THE GOLD", 150, 175); plain_text(img, "EVER MINED?", 330, 150, WHT)
pill(img, "ONLY 22.5 m WIDE", 560, 1000, 52, (200, 40, 40), -4)
img.convert("RGB").save("cover_gold_A.jpg", quality=93)
# B: your share
img = veil(grade(cover(KF + "kf_s7b.jpg")).convert("RGBA"), 560, .42)
gold_text(img, "YOUR SHARE OF", 150, 150); gold_text(img, "ALL THE GOLD?", 330, 150)
ring_arrow(img, 486, 1290, 74, 800, 1010)
pill(img, "ONLY 35 g", 790, 960, 54, (200, 40, 40), -5)
img.convert("RGB").save("cover_gold_B.jpg", quality=93)
sh = Image.new("RGB", (2 * 550, 960), "white")
for i, k in enumerate("AB"): sh.paste(Image.open(f"cover_gold_{k}.jpg").resize((540, 960)), (i * 550, 0))
sh.save("compare.jpg", quality=88); print("ok")
