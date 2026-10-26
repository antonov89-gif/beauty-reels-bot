from PIL import Image, ImageDraw, ImageFont, ImageEnhance
F = "/home/claude/v38/fonts/bowlby-one.ttf"
bg = Image.open("/home/claude/v74/s01.jpg").convert("RGB").resize((1080, 1920), Image.LANCZOS)
bg = ImageEnhance.Contrast(bg).enhance(1.08)
d = ImageDraw.Draw(bg, "RGBA")
for y in range(0, 620): d.line([(0, y), (1080, y)], fill=(0, 0, 0, int(190 * (1 - y / 620) ** 0.9)))
for y in range(1350, 1920): d.line([(0, y), (1080, y)], fill=(0, 0, 0, int(200 * ((y - 1350) / 570) ** 0.9)))
def t(xy, s, size, fill):
    d.text(xy, s, font=ImageFont.truetype(F, size), fill=fill, anchor="mm", stroke_width=9, stroke_fill=(0, 0, 0))
t((540, 150), "THE ISLAND THAT", 88, (255, 255, 255)); t((540, 290), "HAD TO LEAVE", 118, (255, 214, 0))
t((540, 1640), "264 PEOPLE · 1 NIGHT", 62, (255, 255, 255)); t((540, 1740), "2 YEARS AWAY", 80, (255, 214, 0))
f = ImageFont.truetype(F, 30); d.rounded_rectangle([40, 1830, 560, 1880], 10, fill=(0, 0, 0, 170)); d.text((60, 1855), "FICTION · BASED ON REAL EVENTS", font=f, fill=(255, 255, 255), anchor="lm")
bg.save("/home/user/beauty-reels-bot/map_shorts/tristan_fiction_2026_10_26/cover/cover_tristan.jpg", quality=90)
