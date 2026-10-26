"""Cover = real frame of the video (c01 at 1.0 s, the strike) + own title. Output cover_sullivan.jpg"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
F = "/home/claude/v38/fonts/bowlby-one.ttf"
bg = Image.open("/home/claude/v78/cover_bg.png").convert("RGB")
bg = ImageEnhance.Contrast(bg).enhance(1.1)
d = ImageDraw.Draw(bg, "RGBA")
for y in range(0, 560): d.line([(0, y), (1080, y)], fill=(0, 0, 0, int(200 * (1 - y / 560) ** 0.9)))
for y in range(1450, 1920): d.line([(0, y), (1080, y)], fill=(0, 0, 0, int(210 * ((y - 1450) / 470) ** 0.9)))
for w, a in ((22, 70), (12, 255)):                       # ring on the truck, same graphic as in the video
    d.ellipse([551 - 125, 1430 - 92, 551 + 125, 1430 + 92], outline=(255, 215, 40, a), width=w)
def t(xy, s, size, fill):
    d.text(xy, s, font=ImageFont.truetype(F, size), fill=fill, anchor="mm", stroke_width=10, stroke_fill=(0, 0, 0))
t((540, 160), "HIT BY LIGHTNING", 92, (255, 255, 255)); t((540, 330), "7 TIMES", 190, (255, 215, 40))
t((540, 1700), "AND HE KEPT", 70, (255, 255, 255)); t((540, 1800), "WORKING OUTSIDE", 70, (255, 255, 255))
f = ImageFont.truetype(F, 28); d.rounded_rectangle([40, 1862, 420, 1904], 10, fill=(0, 0, 0, 170)); d.text((58, 1883), "AI RECONSTRUCTION", font=f, fill=(255, 255, 255), anchor="lm")
bg.save("cover_sullivan.jpg", quality=90)
