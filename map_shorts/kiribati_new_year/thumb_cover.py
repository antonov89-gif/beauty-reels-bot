"""Kiribati Short cover from keyframe K6 (free): title + torn calendar page 'DEC 31' crossed out. python3 cover47.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
YEL, WHT, BLK, RED = (255, 214, 10), (255, 255, 255), (0, 0, 0), (235, 40, 40)
def tf(s): return ImageFont.truetype("titan-one.ttf", int(s))
def pf(s): return ImageFont.truetype("Poppins-ExtraBold.ttf", int(s))
base = Image.open("base.jpg").convert("RGB")
s = max(W / base.width, H / base.height); base = base.resize((int(base.width * s + .5), int(base.height * s + .5)), Image.LANCZOS)
Z = 1.08; base = base.resize((int(base.width * Z), int(base.height * Z)), Image.LANCZOS); x0 = (base.width - W) // 2; y0 = int(base.height * 0.58 - H / 2); y0 = max(0, min(y0, base.height - H)); base = base.crop((x0, y0, x0 + W, y0 + H))
base = ImageEnhance.Contrast(ImageEnhance.Color(base).enhance(1.15)).enhance(1.08)
img = base.convert("RGBA")
a = np.asarray(img.convert("RGB")).astype(np.float32); g = np.clip(1 - np.linspace(0.45, 0, 560), 0, 1); a[:560] *= g[:, None, None]
img = Image.fromarray(a.astype(np.uint8)).convert("RGBA")
def gtext(txt, cy, size, fill, sw=16, maxw=W - 70):
    global img
    f = tf(size)
    while f.getlength(txt) > maxw: f = tf(f.size - 2)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).text((W / 2 + 5, cy + 12), txt, font=f, fill=(0, 0, 0, 220), anchor="mm", stroke_width=sw + 4, stroke_fill=(0, 0, 0, 220))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(img).text((W / 2, cy), txt, font=f, fill=fill, anchor="mm", stroke_width=sw, stroke_fill=BLK)
gtext("THEY DELETED", 140, 150, YEL, sw=14); gtext("NEW YEAR'S EVE!", 320, 150, WHT, sw=14)
# torn calendar page with DEC 31 crossed out (own drawing, no real calendar), rotated and dropped on the right
pw, ph = 340, 400
pg = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(pg)
d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), 18, fill=(250, 250, 250, 255), outline=(190, 190, 190, 255), width=4)
d.rectangle((20, 20, 20 + pw, 20 + 96), fill=RED + (255,)); d.text((20 + pw / 2, 20 + 50), "DEC", font=pf(64), fill=WHT, anchor="mm")
for k in range(9):  # torn top edge dots (binding holes)
    d.ellipse((50 + k * 38, 34, 64 + k * 38, 48), fill=(160, 20, 20, 255))
d.text((20 + pw / 2, 20 + 270), "31", font=tf(210), fill=(30, 30, 30, 255), anchor="mm")
d.line([(60, 70 + ph - 60), (20 + pw - 40, 140 + 20)], fill=BLK, width=34); d.line([(60, 70 + ph - 60), (20 + pw - 40, 140 + 20)], fill=RED + (255,), width=22)
pg = pg.rotate(-9, expand=True, resample=Image.BICUBIC)
cx, cy = 800, 650
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); al = pg.split()[3].point(lambda v: int(v * .55)); sh.paste((0, 0, 0, 255), (int(cx - pg.width / 2 + 10), int(cy - pg.height / 2 + 16)), al)
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12))); img.alpha_composite(pg, (int(cx - pg.width / 2), int(cy - pg.height / 2)))
d = ImageDraw.Draw(img)
f = pf(30); txt = "AI CONCEPT"; pw2 = int(f.getlength(txt) + 34)
d.rounded_rectangle((30, 1840, 30 + pw2, 1892), 14, fill=(30, 30, 50, 235), outline=WHT, width=3); d.text((30 + pw2 / 2, 1866), txt, font=f, fill=WHT, anchor="mm")
img.convert("RGB").save("cover_kiribati.jpg", quality=93); print("ok")
