"""Storyboard sheet: stills of one loop side by side with their time and a one-line note. Usage: sheet.py stills_dir out.jpg "t=note" ..."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

src, out, notes = sys.argv[1], sys.argv[2], dict(a.split("=", 1) for a in sys.argv[3:])
files = sorted(f for f in os.listdir(src) if f.endswith(".jpg"))
TW, TH, PAD, HEAD = 360, 640, 14, 92
f1 = ImageFont.truetype("/home/claude/v62/assets/Montserrat-Black.ttf", 26)
f2 = ImageFont.truetype("/home/claude/v62/assets/Montserrat-ExtraBold.ttf", 18)
sheet = Image.new("RGB", (PAD + len(files) * (TW + PAD), TH + HEAD + 2 * PAD), (18, 18, 24))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    x = PAD + i * (TW + PAD)
    sheet.paste(Image.open(os.path.join(src, f)).resize((TW, TH)), (x, PAD))
    t = f[:-4].lstrip("0") or "0"
    d.text((x, TH + PAD + 10), f"{t if not t.startswith('.') else '0' + t} s", font=f1, fill=(255, 214, 0))
    note = notes.get(f[:-4], "")
    words, line, y = note.split(), "", TH + PAD + 44
    for w in words:
        if d.textlength(line + " " + w, font=f2) > TW:
            d.text((x, y), line.strip(), font=f2, fill=(230, 230, 230))
            line, y = w, y + 22
        else:
            line += " " + w
    d.text((x, y), line.strip(), font=f2, fill=(230, 230, 230))
sheet.save(out, quality=88)
print(out, sheet.size)
