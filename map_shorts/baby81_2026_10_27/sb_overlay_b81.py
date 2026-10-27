"""Storyboard mock-up for the stories channel: our own graphics over the AI keyframes (white 1-3 word captions at ~78 % height, the number tag "12",
a memory bubble with a torn glowing outline, a DNA-lanes UI), then one contact sheet. AI never writes text.
Run: python3 sb_overlay_b81.py -> /home/claude/v88/sb/<shot>.jpg + /home/claude/v88/storyboard_b81.jpg"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

A = "/home/claude/v62/assets/"
MB, MX = A + "Montserrat-Black.ttf", A + "Montserrat-ExtraBold.ttf"
W, H = 1080, 1920
F = "/home/claude/v88/frames/"
ORDER = [  # shot, frame, caption, extras
    ("s01", "s01", "no name. Only a number.", []),
    ("s02", "s02", "wrote it on his wristband", []),
    ("s03", "s03", "twelve", ["tag12"]),
    ("s05", "s05", "three families said", []),
    ("s04", "s04", "None of them had papers.", ["bubble"]),
    ("s06b", "s06b", "how does he fall asleep?", []),
    ("s07b", "s07b", "She hummed a lullaby.", []),
    ("s08b", "s08b", "looked straight at her.", []),
    ("s07", "s07", "A DNA test", []),
    ("s08", "s08", "made it official.", ["dna"]),
    ("s10", "s10", "The flood took her home.", []),
    ("s11", "s11", "It could not take her song.", []),
]


def caption(img, txt):
    f = ImageFont.truetype(MX, 58)
    while f.getlength(txt) > 940:
        f = ImageFont.truetype(MX, f.size - 3)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((W / 2 + 3, 1498 + 6), txt, font=f, fill=(0, 0, 0, 160), stroke_width=7, stroke_fill=(0, 0, 0, 160), anchor="mm")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(img).text((W / 2, 1498), txt, font=f, fill=(255, 255, 255, 255), stroke_width=6, stroke_fill=(0, 0, 0, 255), anchor="mm")


def tag12(img):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cx, cy, r = 800, 760, 150
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 235), outline=(255, 214, 0, 255), width=10)
    d.text((cx, cy + 6), "12", font=ImageFont.truetype(MB, 190), fill=(20, 30, 60, 255), anchor="mm")
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(1.2)))
    img.alpha_composite(lay)


def torn_mask(cx, cy, rx, ry, seed=3):
    rnd = random.Random(seed); pts = []
    for i in range(120):
        a = 2 * math.pi * i / 120
        k = 1 + 0.10 * math.sin(5 * a + 1) + 0.07 * math.sin(11 * a + 2) + rnd.uniform(-0.035, 0.035)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


def bubble(img):
    inner = Image.open(F + "s04b.jpg").convert("RGBA").resize((W, H))
    cx, cy, rx, ry = 720, 470, 300, 360
    pts = torn_mask(cx, cy, rx, ry)
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).polygon(pts, fill=255)
    crop = inner.crop((int(cx - rx * 1.3), int(cy - ry * 1.3), int(cx + rx * 1.3), int(cy + ry * 1.3))).resize((int(rx * 2.4), int(ry * 2.4)))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); layer.paste(crop, (int(cx - rx * 1.2), int(cy - ry * 1.2)))
    img.alpha_composite(Image.composite(layer, Image.new("RGBA", img.size, (0, 0, 0, 0)), m))
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0)); dg = ImageDraw.Draw(glow)
    dg.line(pts + [pts[0]], fill=(255, 255, 255, 255), width=14, joint="curve")
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))
    ImageDraw.Draw(img).line(pts + [pts[0]], fill=(255, 255, 255, 255), width=8, joint="curve")


def dna(img):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = 130, 900, 950, 1330
    d.rounded_rectangle((x0, y0, x1, y1), radius=36, fill=(6, 14, 34, 215), outline=(0, 229, 255, 255), width=5)
    lanes = [("BABY", 300), ("MOTHER", 540), ("OTHER", 780)]
    pattern = [0.18, 0.34, 0.5, 0.63, 0.8]
    for name, x in lanes:
        d.rounded_rectangle((x - 70, y0 + 70, x + 70, y1 - 50), radius=16, fill=(14, 30, 64, 255))
        d.text((x, y0 + 40), name, font=ImageFont.truetype(MX, 34), fill=(255, 255, 255, 255), anchor="mm")
        pat = pattern if name != "OTHER" else [0.12, 0.3, 0.45, 0.7, 0.9]
        for p_ in pat:
            y = y0 + 90 + p_ * (y1 - y0 - 160)
            col = (60, 255, 150, 255) if name != "OTHER" else (150, 170, 200, 255)
            d.rounded_rectangle((x - 56, y - 8, x + 56, y + 8), radius=8, fill=col)
    d.rounded_rectangle((300 - 78, y0 + 80, 540 + 78, y1 - 40), radius=22, outline=(60, 255, 150, 255), width=6)
    d.text((540, y1 + 56), "MATCH", font=ImageFont.truetype(MB, 92), fill=(60, 255, 150, 255), stroke_width=7, stroke_fill=(0, 0, 0, 255), anchor="mm")
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)))
    img.alpha_composite(lay)


if __name__ == "__main__":
    os.makedirs("/home/claude/v88/sb", exist_ok=True)
    tiles = []
    for shot, fr, cap, ex in ORDER:
        p = F + fr + ".jpg"
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert("RGB").resize((W, H)).convert("RGBA")
        for e in ex:
            {"tag12": tag12, "bubble": bubble, "dna": dna}[e](im)
        caption(im, cap)
        im.convert("RGB").save(f"/home/claude/v88/sb/{shot}.jpg", quality=90); tiles.append((shot, im))
    TW, TH = 360, 640
    cols = 6
    rows = -(-len(tiles) // cols)
    sheet = Image.new("RGB", (10 + cols * (TW + 10), rows * (TH + 50) + 10), (18, 18, 24)); d = ImageDraw.Draw(sheet)
    fl = ImageFont.truetype(MB, 30)
    for k, (s, im) in enumerate(tiles):
        x, y = 10 + (k % cols) * (TW + 10), 10 + (k // cols) * (TH + 50)
        sheet.paste(im.convert("RGB").resize((TW, TH)), (x, y)); d.text((x, y + TH + 8), f"{k + 1} · {s}", font=fl, fill=(255, 214, 0))
    sheet.save("/home/claude/v88/storyboard_b81.jpg", quality=88)
    print("sheet", len(tiles))
