import engine52 as E
from PIL import Image, ImageDraw, ImageEnhance
def split(left, key, cx, cy, z, top, mid, bot, out):
    img = Image.new("RGBA", (E.W, E.H), (8, 6, 20, 255))
    src = Image.open(f"ai/{left}.jpg").convert("RGB"); tb = E.BARS.get(left, (0, 0)); w, h = src.size
    src = src.crop((0, int(h * tb[0]) + 6, w, h - int(h * tb[1]) - 6))
    L, _ = E.view(src, 1.0, 0.5, 0.5, 950, E.H)
    R, _ = E.view(E.sat(key), z, cx, cy, 950, E.H)
    img.paste(ImageEnhance.Color(L).enhance(1.25).convert("RGBA"), (0, 0)); img.paste(ImageEnhance.Contrast(R).enhance(1.15).convert("RGBA"), (970, 0))
    d = ImageDraw.Draw(img); d.rectangle((950, 0, 970, E.H), fill=E.PINK + (255,))
    E.pill(img, "VICE CITY", 475, 90, 44, (200, 30, 110)); E.pill(img, "REAL MIAMI", 1445, 90, 44, (30, 110, 200))
    r = 120; d.ellipse((960 - r, 540 - r, 960 + r, 540 + r), fill=(15, 10, 30, 255), outline=E.WHT + (255,), width=8)
    E.glow_text(img, (960, 540), mid, E.font(E.TITAN, 130), E.YEL, 1.0, "mm", E.PINK)
    E.grad_title(img, top, 960, 860, 200, 9, 0, maxw=1820)
    img.convert("RGB").resize((1280, 720), Image.LANCZOS).save(out, quality=92)
split("V2", "OB", 0.5, 0.5, 1.15, "IT'S REAL", "VS", "", "cover_a.jpg")
split("V4", "PORT", 0.6, 0.55, 1.0, "SAME PLACE?", "VS", "", "cover_b.jpg")
