"""Suez Short cover from the already generated keyframe K3 (free). python3 cover44.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
YEL, WHT, BLK, RED = (255, 214, 10), (255, 255, 255), (0, 0, 0), (235, 40, 40)
def tf(s): return ImageFont.truetype("titan-one.ttf", int(s))
def pf(s): return ImageFont.truetype("Poppins-ExtraBold.ttf", int(s))
base = Image.open("base.jpg").convert("RGB"); base = base.resize((1080, int(base.height * 1080 / base.width)), Image.LANCZOS)
base = ImageEnhance.Contrast(ImageEnhance.Color(base).enhance(1.12)).enhance(1.08)
OFF = 200
img = Image.new("RGBA", (W, H), (14, 22, 48, 255))
sky = base.crop((0, 0, 1080, 30)).resize((1080, OFF + 30), Image.BILINEAR); img.paste(sky, (0, 0)); img.paste(base, (0, OFF))
def gtext(txt, cy, size, fill, sw=16, glow=None, maxw=W - 80):
    global img
    f = tf(size)
    while f.getlength(txt) > maxw: f = tf(f.size - 2)
    if glow:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).text((W / 2, cy), txt, font=f, fill=glow + (230,), anchor="mm", stroke_width=sw + 8, stroke_fill=glow + (230,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(16)))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 5, cy + 12), txt, font=f, fill=(0, 0, 0, 220), anchor="mm", stroke_width=sw + 4, stroke_fill=(0, 0, 0, 220))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(img).text((W / 2, cy), txt, font=f, fill=fill, anchor="mm", stroke_width=sw, stroke_fill=BLK)
gtext("THE MOON", 150, 190, YEL); gtext("FIXED IT?", 330, 190, WHT)
gtext("$400 M / HOUR", 935, 112, WHT, sw=13, glow=RED, maxw=980)
d = ImageDraw.Draw(img)
f = pf(30); txt = "AI CONCEPT"; pw = int(f.getlength(txt) + 34)
d.rounded_rectangle((30, 1840, 30 + pw, 1892), 14, fill=(30, 30, 50, 235), outline=WHT, width=3); d.text((30 + pw / 2, 1866), txt, font=f, fill=WHT, anchor="mm")
img.convert("RGB").save("cover_suez.jpg", quality=93); print("ok")
