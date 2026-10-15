"""Cover from keyframe K1 (no extra generation)."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
YEL, WHT, BLK, RED = (255, 214, 10), (255, 255, 255), (0, 0, 0), (232, 36, 36)
def font(s): return ImageFont.truetype("Poppins-ExtraBold.ttf", int(s))
im = Image.open("kf/K1.jpg").convert("RGB")
box = (60, 230, 1476, 230 + int(1416 * 16 / 9))
im = im.crop(box).resize((W, H), Image.LANCZOS)
im = ImageEnhance.Color(im).enhance(1.15); im = ImageEnhance.Contrast(im).enhance(1.06)
a = np.asarray(im).astype(np.float32); g = np.clip(1 - np.linspace(0.6, 0, 640), 0, 1); a[:640] *= g[:, None, None]
img = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
def title(lines, y):
    d = ImageDraw.Draw(img)
    for txt, col, sz in lines:
        f = font(sz)
        while f.getlength(txt) > W - 70: f = font(f.size - 2)
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((W / 2 + 6, y + 10), txt, font=f, fill=(0, 0, 0, 200), anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0, 200))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
        d.text((W / 2, y), txt, font=f, fill=col, anchor="mm", stroke_width=12, stroke_fill=BLK); y += f.size * 1.08
title([("THEIR MONEY WEIGHS", WHT, 110), ("UP TO 4 TONS", YEL, 150)], 140)
# badge
f = font(54); txt = "YAP ISLAND"; tw = f.getlength(txt); d = ImageDraw.Draw(img)
x0, y0 = W / 2 - tw / 2 - 40, 430
d.rounded_rectangle((x0, y0, x0 + tw + 80, y0 + 90), 40, fill=RED + (255,), outline=WHT, width=6)
d.text((W / 2, y0 + 47), txt, font=f, fill=WHT, anchor="mm", stroke_width=3, stroke_fill=BLK)
img.convert("RGB").save("cover_yap.jpg", quality=93)
