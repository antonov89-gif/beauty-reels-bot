from PIL import Image, ImageDraw, ImageFont, ImageFilter
src = Image.open('s_60.png').convert('RGB')           # 1920x1080
for yy in range(343, 354):                              # remove the baked dashed line
    for xx in range(0, 1920):
        src.putpixel((xx, yy), src.getpixel((xx, 340)))

W, H = 1280, 720
# clean gradient background: replicate a text-free column
col = src.crop((300, 0, 301, 1080)).resize((1, 720))
bg = col.resize((W, H))
# stack crop (green bundle) from the frame, stretched to full usable height
stack = src.crop((783, 287, 830, 950))
top_y = 60                       # top of stack in thumbnail
base_y = 700
sh = base_y - top_y
stack = stack.resize((150, sh), Image.LANCZOS)
sx = 1010
# glow
glow = Image.new('RGB', (W, H), (0, 0, 0)); ImageDraw.Draw(glow).rectangle([sx-10, top_y-10, sx+160, base_y], fill=(80, 255, 120))
glow = glow.filter(ImageFilter.GaussianBlur(40))
bg = Image.blend(bg, Image.eval(Image.composite(glow, bg, Image.new('L', (W, H), 255)), lambda v: v), 0.0)
from PIL import ImageChops
bg = ImageChops.add(bg, Image.eval(glow, lambda v: int(v*0.35)))
bg.paste(stack, (sx, top_y))
d = ImageDraw.Draw(bg)
# dashed "space" line
y = 210
for x in range(0, W, 36): d.line([(x, y), (x+20, y)], fill=(255, 255, 255), width=4)
F = '/home/claude/v38/fonts/bowlby-one.ttf'
def txt(xy, s, size, fill, stroke=10):
    f = ImageFont.truetype(F, size)
    d.text(xy, s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
txt((50, 250), "$100 BILLION", 92, (255, 255, 255))
txt((50, 360), "REACHES", 130, (255, 214, 0))
txt((50, 500), "SPACE", 170, (255, 214, 0))
sm = ImageFont.truetype('/home/claude/v20/fonts/GochiHand.ttf', 54)
d.text((60, 140), "space begins ~100 km", font=sm, fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
d.text((730, 640), "~110 km", font=ImageFont.truetype('/home/claude/v20/fonts/GochiHand.ttf', 64), fill=(255, 90, 90), stroke_width=5, stroke_fill=(0, 0, 0))
bg.save('thumb_100b_long.jpg', quality=92)
