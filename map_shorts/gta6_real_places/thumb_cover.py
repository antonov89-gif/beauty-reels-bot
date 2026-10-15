"""GTA 6 Short cover: AI neon Miami (left) + real Esri satellite (right triangle). python3 cover38.py"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
YEL, PINK, WHT, BLK, RED = (255, 214, 10), (255, 60, 170), (255, 255, 255), (0, 0, 0), (232, 36, 36)
def font(s): return ImageFont.truetype("Poppins-ExtraBold.ttf", int(s))

def cover(im):
    iw, ih = im.size; s = max(W / iw, H / ih)
    im = im.resize((int(iw * s + .5), int(ih * s + .5)), Image.LANCZOS); x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((x0, y0, x0 + W, y0 + H))

ai = cover(Image.open("/home/claude/v37/gta_base.jpg").convert("RGB"))
ai = ImageEnhance.Contrast(ImageEnhance.Color(ai).enhance(1.12)).enhance(1.06)
sat = Image.open("sat_miami.jpg").convert("RGB")
sat = ImageEnhance.Color(sat).enhance(1.12); sat = ImageEnhance.Contrast(sat).enhance(1.08)
# warm tint so the two halves sit together
a = np.asarray(sat).astype(np.float32); a = a * 0.9 + np.array([255, 150, 90], np.float32) * 0.1
sat = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
sat = sat.resize((864, 1536), Image.LANCZOS)
SOFF = (300, -250)
sat_full = Image.new("RGB", (W, H)); sat_full.paste(sat, SOFF); sat = sat_full

P1, P2, P3 = (1080, 330), (1080, 1245), (430, 1245)      # satellite triangle
img = ai.convert("RGBA")
m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).polygon([P1, P2, P3], fill=255)
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(P1[0] - 6, P1[1] + 8), (P2[0], P2[1] + 10), (P3[0] - 6, P3[1] + 10)], fill=(0, 0, 0, 200))
img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
img.paste(sat, (0, 0), m)
d = ImageDraw.Draw(img)
d.line([P1, P3], fill=WHT, width=9); d.line([P3, P2], fill=WHT, width=9)

def stroke_text(txt, xy, f, fill, stroke, sw, anchor="mm", glow=None):
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(s).text((xy[0] + 6, xy[1] + 12), txt, font=f, fill=(0, 0, 0, 210), anchor=anchor, stroke_width=sw + 4, stroke_fill=(0, 0, 0, 210))
    img.alpha_composite(s.filter(ImageFilter.GaussianBlur(9)))
    ImageDraw.Draw(img).text(xy, txt, font=f, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=stroke)

def fit(txt, size, maxw):
    f = font(size)
    while f.getlength(txt) > maxw: f = font(f.size - 2)
    return f

# title (top dark veil so it reads on any sky)
veil = np.asarray(img.convert("RGB")).astype(np.float32); g = np.clip(1 - np.linspace(0.42, 0, 520), 0, 1)
veil[:520] *= g[:, None, None]; img = Image.fromarray(veil.astype(np.uint8)).convert("RGBA")
# redraw seam/shadow not needed above y=520 except triangle tip: re-paste triangle top part is untouched by veil? re-apply sat crop above veil
img.paste(sat, (0, 0), m); d = ImageDraw.Draw(img); d.line([P1, P3], fill=WHT, width=9); d.line([P3, P2], fill=WHT, width=9)
f1 = fit("GTA 6 =", 168, W - 80); stroke_text("GTA 6 =", (W / 2, 150), f1, WHT, (255, 40, 150), 14)
f2 = fit("REAL FLORIDA?", 150, W - 50); stroke_text("REAL FLORIDA?", (W / 2, 320), f2, YEL, BLK, 14)

def pill(txt, cx, cy, sz, bg, rot=0, fg=WHT):
    f = font(sz); pw, ph = int(f.getlength(txt) + sz * 1.0), int(sz * 1.7)
    lay = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
    dd.rounded_rectangle((20, 20, 20 + pw, 20 + ph), sz * 0.4, fill=bg + (255,), outline=WHT, width=5)
    dd.text((20 + pw / 2, 20 + ph / 2), txt, font=f, fill=fg, anchor="mm", stroke_width=2, stroke_fill=BLK)
    lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC)
    s = Image.new("RGBA", (W, H), (0, 0, 0, 0)); al = lay.split()[3].point(lambda v: int(v * .6))
    s.paste((0, 0, 0, 255), (int(cx - lay.width / 2 + 7), int(cy - lay.height / 2 + 11)), al)
    img.alpha_composite(s.filter(ImageFilter.GaussianBlur(9))); img.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

# red map pin on the beach strip inside the triangle
px, py = 765, 800
pin = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(pin)
pd.ellipse((px - 78, py + 44, px + 78, py + 90), fill=(0, 0, 0, 120))
pd.ellipse((px - 62, py - 150, px + 62, py - 26), fill=RED + (255,), outline=WHT, width=8)
pd.polygon([(px - 50, py - 62), (px + 50, py - 62), (px, py + 44)], fill=RED + (255,))
pd.ellipse((px - 22, py - 110, px + 22, py - 66), fill=WHT + (255,))
img.alpha_composite(pin)
pill("REAL", 930, 1180, 46, (20, 150, 90), -4)
pill("AI CONCEPT", 175, 1130, 36, (30, 30, 50), 0)
pill("VICE CITY = MIAMI?", 420, 690, 50, PINK, -6)
img.convert("RGB").save("cover_gta6.jpg", quality=93); print("ok")
