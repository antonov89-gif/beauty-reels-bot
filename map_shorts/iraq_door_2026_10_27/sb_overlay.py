"""Storyboard mock-up: our own text graphics over the AI keyframes (top banner, stamps, chips, 2-5 word caption with the active word yellow),
then one contact sheet. Run: python3 sb_overlay.py -> /home/claude/v86/sb/sNN.jpg + /home/claude/v86/storyboard_iraq.jpg"""
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

A = "/home/claude/v62/assets/"
MB, MX = A + "Montserrat-Black.ttf", A + "Montserrat-ExtraBold.ttf"
W, H = 1080, 1920
YEL, WHT, RED, NAVY = (255, 214, 0), (255, 255, 255), (220, 30, 30), (12, 22, 48)
OV = {   # banner, [(kind, text, y)], caption, active word
    "s01": ("ONE 58 KM DOOR?!", [("chip", "≈ 9 OF 10 OIL BARRELS", 1180)], "Iraq ships about nine in ten", "nine"),
    "s02": (None, [("chip", "46,000,000 PEOPLE", 330), ("stamp", "TINY DOOR", 760)], "one tiny door to the sea", "tiny"),
    "s03": (None, [("chip", "IRAN  ·  IRAQ  ·  KUWAIT", 330), ("stamp", "SQUEEZED", 780)], "Iran on one side, Kuwait on the other", "Kuwait"),
    "s04": (None, [("chip", "THE ONLY WAY OUT", 330)], "a narrow channel called Khor Abdullah", "Khor"),
    "s05": (None, [("chip", "BORDER: THE MIDDLE", 300), ("chip", "DEEP WATER: KUWAIT SIDE", 410)], "the deep water sits closer to Kuwait", "closer"),
    "s06": (None, [("stamp", "WAIT…", 700)], "a channel is still a channel, right?", "right?"),
    "s07": (None, [("chip", "KUWAIT: MUBARAK AL-KABEER PORT", 300), ("chip", "IRAQ: GRAND FAW PORT", 410)], "Kuwait built a giant port right on it", "giant"),
    "s08": (None, [("stamp", "CHOKE POINT?", 700), ("chip", "2023: IRAQ COURT SCRAPS THE DEAL", 1180)], "it could squeeze its only lane", "squeeze"),
    "s09": ("SMART MOVE OR CHOKEHOLD?", [], "Smart move by Kuwait, or a chokehold?", "chokehold?"),
}


def shadow_text(img, xy, txt, f, col, stroke=8, anchor="mm"):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((xy[0] + 4, xy[1] + 7), txt, font=f, fill=(0, 0, 0, 170), stroke_width=stroke, stroke_fill=(0, 0, 0, 170), anchor=anchor)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(5)))
    ImageDraw.Draw(img).text(xy, txt, font=f, fill=col, stroke_width=stroke, stroke_fill=(0, 0, 0), anchor=anchor)


def banner(img, txt):
    f = ImageFont.truetype(MB, 78)
    while f.getlength(txt) > 940:
        f = ImageFont.truetype(MB, f.size - 4)
    tw = f.getlength(txt); x0, x1 = (W - tw) / 2 - 36, (W + tw) / 2 + 36
    d = ImageDraw.Draw(img); d.rounded_rectangle((x0, 150, x1, 150 + f.size + 60), radius=22, fill=NAVY + (235,), outline=YEL + (255,), width=5)
    d.text((W / 2, 150 + (f.size + 60) / 2), txt, font=f, fill=YEL, anchor="mm")


def chip(img, txt, y):
    f = ImageFont.truetype(MX, 50)
    while f.getlength(txt) > 960:
        f = ImageFont.truetype(MX, f.size - 2)
    tw = f.getlength(txt)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle(((W - tw) / 2 - 34, y - 46, (W + tw) / 2 + 34, y + 46), radius=46, fill=(10, 16, 32, 215), outline=WHT + (255,), width=3)
    d.text((W / 2, y), txt, font=f, fill=WHT, anchor="mm"); img.alpha_composite(lay)


def stamp(img, txt, y):
    f = ImageFont.truetype(MB, 120)
    while f.getlength(txt) > 860:
        f = ImageFont.truetype(MB, f.size - 4)
    tw = f.getlength(txt)
    lay = Image.new("RGBA", (int(tw + 120), f.size + 110), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((8, 8, lay.width - 8, lay.height - 8), radius=18, outline=RED + (255,), width=12)
    d.text((lay.width / 2, lay.height / 2), txt, font=f, fill=RED + (255,), anchor="mm")
    lay = lay.rotate(-7, Image.BICUBIC, expand=True)
    img.alpha_composite(lay, (int(W / 2 - lay.width / 2), int(y - lay.height / 2)))


def caption(img, txt, active):
    f = ImageFont.truetype(MB, 62); words = txt.split()
    lines, cur = [], []
    for w in words:
        if f.getlength(" ".join(cur + [w])) > 900 and cur:
            lines.append(cur); cur = []
        cur.append(w)
    lines.append(cur)
    y = 1470 - (len(lines) - 1) * 40
    for ln in lines:
        sp = f.getlength(" "); tot = sum(f.getlength(w) for w in ln) + sp * (len(ln) - 1); x = (W - tot) / 2
        for w in ln:
            shadow_text(img, (x + f.getlength(w) / 2, y), w, f, YEL if w == active else WHT, 7)
            x += f.getlength(w) + sp
        y += 80


if __name__ == "__main__":
    os.makedirs("/home/claude/v86/sb", exist_ok=True)
    tiles = []
    for s, (ban, items, cap, act) in OV.items():
        src = f"/home/claude/v86/ai/{s}.jpg"
        if not os.path.exists(src):
            continue
        im = Image.open(src).convert("RGB").resize((W, H)).convert("RGBA")
        if ban:
            banner(im, ban)
        for kind, txt, y in items:
            (chip if kind == "chip" else stamp)(im, txt, y)
        caption(im, cap, act)
        im.convert("RGB").save(f"/home/claude/v86/sb/{s}.jpg", quality=90); tiles.append((s, im))
    TW, TH = 360, 640
    sheet = Image.new("RGB", (10 + 5 * (TW + 10), 2 * (TH + 50) + 10), (18, 18, 24)); d = ImageDraw.Draw(sheet)
    fl = ImageFont.truetype(MB, 30)
    for k, (s, im) in enumerate(tiles):
        x, y = 10 + (k % 5) * (TW + 10), 10 + (k // 5) * (TH + 50)
        sheet.paste(im.convert("RGB").resize((TW, TH)), (x, y)); d.text((x, y + TH + 8), s, font=fl, fill=YEL)
    sheet.save("/home/claude/v86/storyboard_iraq.jpg", quality=88)
    print("sheet", len(tiles))
