"""Cover = real frame of the video (c07 at 3.4 s, the liver almost regrown into its outline) + own title. Output cover_liver.jpg"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
F = "/home/claude/v38/fonts/bowlby-one.ttf"
bg = ImageEnhance.Contrast(Image.open("/home/claude/v81/cover_bg.png").convert("RGB")).enhance(1.08)
d = ImageDraw.Draw(bg, "RGBA")
for y in range(0, 560): d.line([(0, y), (1080, y)], fill=(0, 30, 50, int(170 * (1 - y / 560) ** 0.9)))
def t(xy, s, size, fill):
    d.text(xy, s, font=ImageFont.truetype(F, size), fill=fill, anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
t((540, 150), "YOUR LIVER", 120, (255, 255, 255)); t((540, 320), "GROWS BACK", 120, (255, 215, 40))
t((540, 1720), "HALF TO FULL", 90, (255, 255, 255)); t((540, 1820), "IN ~2 MONTHS", 70, (255, 215, 40))
f = ImageFont.truetype(F, 28); d.rounded_rectangle([40, 1862, 330, 1904], 10, fill=(0, 0, 0, 170)); d.text((58, 1883), "AI ANIMATION", font=f, fill=(255, 255, 255), anchor="lm")
bg.save("/home/user/beauty-reels-bot/map_shorts/liver_regrow_2026_10_26/cover/cover_liver.jpg", quality=90)
