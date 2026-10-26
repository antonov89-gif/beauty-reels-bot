"""Cover for the lifeboat Short: real frame of the owner's clip S10 at 2.0 s (three captains, eyes open) + headline + the real own-child answers."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
F = "/home/claude/v38/fonts/bowlby-one.ttf"
bg = Image.open("/home/claude/v73/cov_bg.png").convert("RGB").resize((1080, 1920))
bg = ImageEnhance.Contrast(ImageEnhance.Color(bg).enhance(1.15)).enhance(1.08)
d = ImageDraw.Draw(bg, "RGBA")
# top dark band for the headline
for y in range(0, 560):
    d.line([(0, y), (1080, y)], fill=(0, 0, 0, int(200 * (1 - y / 560) ** 0.8)))
for y in range(1300, 1920):
    d.line([(0, y), (1080, y)], fill=(0, 0, 0, int(210 * ((y - 1300) / 620) ** 0.9)))
def text(xy, s, size, fill, anchor="mm", stroke=10):
    f = ImageFont.truetype(F, size); d.text(xy, s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))
text((540, 150), "3 AIs. 1 LIFEBOAT.", 92, (255, 255, 255))
text((540, 290), "LEAVE YOUR", 122, (255, 214, 0))
text((540, 430), "OWN CHILD?", 122, (255, 214, 0))
def chip(y, label, ans, col):
    f = ImageFont.truetype(F, 78); w = d.textlength(f"{label}  {ans}", font=f) + 70
    x0 = 540 - w / 2; d.rounded_rectangle([x0, y - 62, x0 + w, y + 62], 26, fill=col + (255,), outline=(0, 0, 0, 255), width=6)
    d.text((540, y), f"{label}  {ans}", font=f, fill=(255, 255, 255), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0))
chip(1430, "GPT", "YES", (60, 180, 80))
chip(1590, "GEMINI", "NO", (224, 60, 60))
chip(1750, "GROK", "NO", (224, 60, 60))
bg.save("/home/user/beauty-reels-bot/map_shorts/ai_lifeboat_2026_10_25/cover/cover_lifeboat.jpg", quality=90)
