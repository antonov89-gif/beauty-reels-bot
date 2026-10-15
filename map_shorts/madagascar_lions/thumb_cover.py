"""Madagascar Short cover: user's generated base (lion/zebra vs lemur/fossa) + real NASA map strip + red 419 KM. python3 cover41.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
YEL, WHT, BLK, RED = (255, 214, 10), (255, 255, 255), (0, 0, 0), (235, 40, 40)
def tf(s): return ImageFont.truetype("titan-one.ttf", int(s))
def pf(s): return ImageFont.truetype("Poppins-ExtraBold.ttf", int(s))
base = Image.open("base.jpg").convert("RGB"); base = base.resize((1080, int(base.height * 1080 / base.width)), Image.LANCZOS)
base = ImageEnhance.Contrast(ImageEnhance.Color(base).enhance(1.12)).enhance(1.06)
OFF = 330
img = Image.new("RGBA", (W, H), (20, 40, 80, 255)); sky = base.crop((0, 0, 1080, 40)).resize((1080, OFF + 40), Image.BILINEAR); img.paste(sky, (0, 0)); img.paste(base, (0, OFF))
# map strip (real NASA Blue Marble) at the very top, fading into the sky
MC0 = 60
mp = Image.open("map_strip.jpg").convert("RGB").crop((0, MC0, 1080, MC0 + 300)); mp = ImageEnhance.Contrast(mp).enhance(1.1)
m = np.ones((300, 1080), np.float32); m[220:] = np.linspace(1, 0, 80)[:, None]
img.paste(mp, (0, 0), Image.fromarray((m * 255).astype(np.uint8)))
d = ImageDraw.Draw(img)
def dashed(x0, x1, y, col, w, dash=20, gap=12):
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + dash, x1), y)], fill=col, width=w); x += dash + gap
MY = 190 - MC0   # narrowest part of the channel on the map
dashed(500, 662, MY, BLK, 14); dashed(500, 662, MY, RED, 8)
for xx, sg in ((500, 1), (662, -1)):
    d.polygon([(xx - sg * 4, MY), (xx + sg * 22, MY - 14), (xx + sg * 22, MY + 14)], fill=RED, outline=BLK)

def gtext(txt, cy, size, fill, sw=16, glow=None, maxw=W - 80):
    f = tf(size)
    while f.getlength(txt) > maxw: f = tf(f.size - 2)
    global img
    if glow:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).text((W / 2, cy), txt, font=f, fill=glow + (230,), anchor="mm", stroke_width=sw + 8, stroke_fill=glow + (230,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(16)))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 5, cy + 12), txt, font=f, fill=(0, 0, 0, 220), anchor="mm", stroke_width=sw + 4, stroke_fill=(0, 0, 0, 220))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(img).text((W / 2, cy), txt, font=f, fill=fill, anchor="mm", stroke_width=sw, stroke_fill=BLK)

gtext("NO LIONS", 365, 150, YEL, sw=14); gtext("HERE?", 520, 150, WHT, sw=14)
# 419 KM in the channel, with a horizontal double arrow across the gap
gtext("419 KM", 1245, 150, WHT, sw=14, glow=RED, maxw=380)
d = ImageDraw.Draw(img)
ay, ax0, ax1 = 1345, 385, 772
d.line([(ax0 + 20, ay), (ax1 - 20, ay)], fill=BLK, width=20); d.line([(ax0 + 20, ay), (ax1 - 20, ay)], fill=RED, width=11)
for xx, sg in ((ax0, 1), (ax1, -1)):
    d.polygon([(xx, ay), (xx + sg * 44, ay - 30), (xx + sg * 44, ay + 30)], fill=BLK); d.polygon([(xx + sg * 5, ay), (xx + sg * 40, ay - 24), (xx + sg * 40, ay + 24)], fill=RED)
# AI tag (small)
f = pf(30); txt = "AI CONCEPT"; pw = int(f.getlength(txt) + 34)
d.rounded_rectangle((30, 1840, 30 + pw, 1892), 14, fill=(30, 30, 50, 235), outline=WHT, width=3); d.text((30 + pw / 2, 1866), txt, font=f, fill=WHT, anchor="mm")
img.convert("RGB").save("cover_madagascar.jpg", quality=93); print("ok")
