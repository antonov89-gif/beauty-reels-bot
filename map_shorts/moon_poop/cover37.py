"""Cover from keyframe S8_v2 (no extra generation)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
YEL, WHT, BLK, RED = (255, 214, 10), (255, 255, 255), (0, 0, 0), (232, 36, 36)
def font(s): return ImageFont.truetype("Poppins-ExtraBold.ttf", int(s))
im = Image.open("/home/user/beauty-reels-bot/map_shorts/moon_poop/keyframes/S1.jpg").convert("RGB")
iw, ih = im.size; s = max(W / iw, H / ih); im = im.resize((int(iw * s) + 1, int(ih * s) + 1), Image.LANCZOS)
im = im.crop(((im.width - W) // 2, 0, (im.width - W) // 2 + W, H))
im = ImageEnhance.Contrast(im).enhance(1.08)
img = im.convert("RGBA")
def title(lines, y):
    d = ImageDraw.Draw(img)
    for txt, col, sz in lines:
        f = font(sz)
        while f.getlength(txt) > W - 70: f = font(f.size - 2)
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((W / 2 + 6, y + 10), txt, font=f, fill=(0, 0, 0, 200), anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0, 200))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
        d.text((W / 2, y), txt, font=f, fill=col, anchor="mm", stroke_width=12, stroke_fill=BLK); y += f.size * 1.08
title([("96 BAGS OF", WHT, 140), ("POOP ON THE MOON", YEL, 120)], 150)
f = font(52); txt = "LEFT ON PURPOSE"; tw = f.getlength(txt); d = ImageDraw.Draw(img)
x0, y0 = W / 2 - tw / 2 - 40, 440
d.rounded_rectangle((x0, y0, x0 + tw + 80, y0 + 90), 40, fill=RED + (255,), outline=WHT, width=6)
d.text((W / 2, y0 + 47), txt, font=f, fill=WHT, anchor="mm", stroke_width=3, stroke_fill=BLK)
img.convert("RGB").save("cover_moon.jpg", quality=93)
