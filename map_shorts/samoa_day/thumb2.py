"""Clickable cover variants from thumb_base.jpg (no paid generation). python3 thumb2.py"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
W, H = 1080, 1920
POPX = "Poppins-ExtraBold.ttf"
YEL, RED, WHT, BLK = (255, 214, 10), (232, 36, 36), (255, 255, 255), (0, 0, 0)
def font(s): return ImageFont.truetype(POPX, int(s))

def coeffs(src, dst):
    # perspective coefficients mapping output (dst) points to input (src) points
    A, b = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; b += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(b, float)).tolist()

def base(box):
    im = Image.open("thumb_base.jpg").convert("RGB").crop(box).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Color(im).enhance(1.18); im = ImageEnhance.Contrast(im).enhance(1.08)
    # soft top darkening for the title
    a = np.asarray(im).astype(np.float32); g = np.clip(1 - np.linspace(0.55, 0, 620), 0, 1)
    a[:620] *= g[:, None, None]; return Image.fromarray(a.astype(np.uint8)).convert("RGBA")

def page(img, quad, draw_fn, size=(800, 1000)):
    lay = Image.new("RGBA", size, (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(lay), size)
    w = lay.transform((W, H), Image.PERSPECTIVE, coeffs([(0, 0), (size[0], 0), (size[0], size[1]), (0, size[1])], quad), Image.BICUBIC)
    img.alpha_composite(w)

def title(img, lines, y0):
    d = ImageDraw.Draw(img); y = y0
    for txt, col, sz in lines:
        f = font(sz)
        while f.getlength(txt) > W - 70: f = font(f.size - 2)
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((W / 2 + 6, y + 10), txt, font=f, fill=(0, 0, 0, 200), anchor="mm", stroke_width=14, stroke_fill=(0, 0, 0, 200))
        img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
        d.text((W / 2, y), txt, font=f, fill=col, anchor="mm", stroke_width=12, stroke_fill=BLK)
        y += f.size * 1.08

def cal_X(d, s):
    w, h = s; cx = w * 0.40
    d.text((cx, h * 0.12), "DEC 2011", font=font(h * 0.08), fill=(70, 70, 70), anchor="mm")
    d.text((cx, h * 0.29), "FRIDAY", font=font(h * 0.16), fill=RED, anchor="mm")
    d.text((cx, h * 0.64), "30", font=font(h * 0.50), fill=(25, 25, 25), anchor="mm")
    # one red strike-through: 'deleted', the number stays readable
    d.line([(cx - w * 0.36, h * 0.80), (cx + w * 0.36, h * 0.46)], fill=RED + (235,), width=int(w * 0.065))

def badge(img, txt, cx, cy, sz=58, bg=RED, rot=-6):
    # '>' in txt is drawn as an arrow (Poppins has no arrow glyph)
    f = font(sz); parts = txt.split(">"); aw = sz * 1.2
    tw = sum(f.getlength(p) for p in parts) + aw * (len(parts) - 1); pw, ph = int(tw + sz * 1.1), int(sz * 1.75)
    lay = Image.new("RGBA", (pw + 40, ph + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((20, 20, 20 + pw, 20 + ph), sz * 0.4, fill=bg + (255,), outline=WHT, width=6)
    x = 20 + sz * 0.55; yc = 20 + ph / 2
    for k, p in enumerate(parts):
        d.text((x, yc), p, font=f, fill=WHT, anchor="lm", stroke_width=3, stroke_fill=BLK); x += f.getlength(p)
        if k < len(parts) - 1:
            a0, a1 = x + sz * 0.15, x + aw - sz * 0.15
            d.line([(a0, yc), (a1 - sz * 0.3, yc)], fill=YEL, width=int(sz * 0.18))
            d.polygon([(a1, yc), (a1 - sz * 0.42, yc - sz * 0.3), (a1 - sz * 0.42, yc + sz * 0.3)], fill=YEL); x += aw
    lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); a = lay.split()[3].point(lambda v: v * 0.6)
    sh.paste((0, 0, 0, 255), (int(cx - lay.width / 2 + 8), int(cy - lay.height / 2 + 12)), a)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    img.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

# crop: tighter on page + face (base 1536x2752)
BOX = (96, 185, 1440, 185 + int(1344 * 16 / 9))
sx = W / (BOX[2] - BOX[0]); sy = H / (BOX[3] - BOX[1])
def P(x, y): return ((x - BOX[0]) * sx, (y - BOX[1]) * sy)
QUAD = [P(150, 726), P(615, 660), P(835, 1210), P(462, 1305)]  # front face of the blank page (base px)

if __name__ == "__main__":
    import sys
    # B: curiosity title + crossed-out Friday + THU -> SAT badge
    im = base(BOX); page(im, QUAD, cal_X)
    title(im, [("FRIDAY NEVER", WHT, 118), ("HAPPENED HERE", YEL, 118)], 150)
    badge(im, "THU 29 > SAT 31", 800, 965, 52)
    im.convert("RGB").save("thumb2/cover_B.jpg", quality=93)
    # C: short shock title
    im = base(BOX); page(im, QUAD, cal_X)
    title(im, [("THEY DELETED", WHT, 112), ("FRIDAY!", YEL, 150)], 120)
    badge(im, "THU 29 > SAT 31", 800, 965, 52)
    im.convert("RGB").save("thumb2/cover_C.jpg", quality=93)
    print("ok", QUAD)
