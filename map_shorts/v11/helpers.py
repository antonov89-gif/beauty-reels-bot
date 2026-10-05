import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
POP = "assets/Poppins-Bold.ttf"
POPX = "assets/Poppins-ExtraBold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
YEL = (255, 214, 10)
RED = (232, 52, 52)
GRN = (60, 200, 90)
BLU = (60, 140, 255)
WHT = (255, 255, 255)
BLK = (0, 0, 0)


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def pop(x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    if x < 0.6:
        return 1.15 * ease(x / 0.6)
    return 1.15 - 0.15 * ease((x - 0.6) / 0.4)


_FONTS = {}


def font(path, size):
    key = (path, int(size))
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(path, max(1, int(size)))
    return _FONTS[key]


_EMO = {}


def emoji_sprite(ch):
    """Noto emoji at 109 px with a white sticker outline (cached)."""
    if ch not in _EMO:
        f = ImageFont.truetype(EMOJI, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((80, 80), ch, font=f, embedded_color=True, anchor="mm")
        a = im.split()[3]
        outline = a.filter(ImageFilter.MaxFilter(11))
        base = Image.new("RGBA", im.size, WHT + (0,))
        base.putalpha(outline)
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sh.putalpha(outline.point(lambda v: v * 0.35))
        out = Image.new("RGBA", (170, 170), (0, 0, 0, 0))
        out.alpha_composite(sh, (6, 8))
        out.alpha_composite(base, (2, 2))
        out.alpha_composite(im, (2, 2))
        _EMO[ch] = out
    return _EMO[ch]


def paste_emoji(img, ch, x, y, size):
    if size < 4:
        return
    sp = emoji_sprite(ch)
    s = int(size * 170 / 120)
    sp = sp.resize((s, s), Image.LANCZOS)
    img.alpha_composite(sp, (int(x - s / 2), int(y - s / 2)))


def text_stroke(d, xy, txt, f, fill, stroke=8, anchor="mm", sfill=BLK):
    d.text(xy, txt, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)


def badge(img, x, y, txt, color, k, emoji=None, size=56):
    """Rounded tag with optional emoji, popping in with scale k."""
    if k <= 0.01:
        return
    f = font(POP, size * k)
    d = ImageDraw.Draw(img)
    tw = f.getlength(txt)
    ew = size * 1.15 * k if emoji else 0
    pw, ph = tw + ew + 44 * k, size * 1.55 * k
    x0, y0 = min(W - 30 - pw, max(30, x - pw / 2)), y - ph / 2
    d.rounded_rectangle((x0 + 5, y0 + 7, x0 + pw + 5, y0 + ph + 7), radius=ph / 2.4, fill=(0, 0, 0, 110))
    d.rounded_rectangle((x0, y0, x0 + pw, y0 + ph), radius=ph / 2.4, fill=color + (255,), outline=WHT,
                        width=max(1, int(5 * k)))
    tx = x0 + 22 * k + ew
    d.text((tx, y + 2 * k), txt, font=f, fill=WHT, anchor="lm", stroke_width=max(1, int(3 * k)), stroke_fill=BLK)
    if emoji:
        paste_emoji(img, emoji, x0 + 22 * k + ew / 2 - 4 * k, y, size * 1.05 * k)


def arrow(img, pts, color, prog, width=22):
    """Progressively drawn thick arrow along pixel polyline pts."""
    if prog <= 0 or len(pts) < 2:
        return
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    total = sum(seg)
    L = total * min(1, prog)
    out, acc = [pts[0]], 0
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if acc + s >= L:
            k = (L - acc) / max(s, 1e-6)
            out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
            break
        out.append(b)
        acc += s
    sh = Image.new("RGBA", (W // 2, H // 2), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    ds.line([(x / 2 + 6, y / 2 + 8) for x, y in out], fill=(0, 0, 0, 120), width=int(width * 0.75), joint="curve")
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    (ax, ay), (bx, by) = out[-2], out[-1]
    ang = math.atan2(by - ay, bx - ax)
    hs = width * 2.0
    tip = (bx + math.cos(ang) * hs * 0.7, by + math.sin(ang) * hs * 0.7)
    l = (bx + math.cos(ang + 2.35) * hs, by + math.sin(ang + 2.35) * hs)
    r = (bx + math.cos(ang - 2.35) * hs, by + math.sin(ang - 2.35) * hs)
    d.line(out, fill=WHT + (255,), width=width + 12, joint="curve")
    d.polygon([tip, l, r], fill=WHT + (255,), outline=WHT + (255,), width=12)
    d.line(out, fill=color + (255,), width=width, joint="curve")
    d.polygon([tip, l, r], fill=color + (255,))
    lite = tuple(min(255, c + 70) for c in color)
    d.line(out, fill=lite + (255,), width=max(2, width // 4), joint="curve")


def big(img, txt, t, t0, y=520, size=150, color=YEL, sub=None):
    """Slam text: scale 1.6 -> 1 in 0.15 s."""
    if t < t0:
        return 0
    k = (t - t0) / 0.15
    s = 1.6 - 0.6 * ease(k) if k < 1 else 1.0
    f = font(POPX, size * s)
    d = ImageDraw.Draw(img)
    while f.getlength(txt) > W - 80 and f.size > 20:
        f = font(POPX, f.size * 0.9)
    text_stroke(d, (W / 2, y), txt, f, color, stroke=max(4, int(size * 0.09)))
    if sub:
        text_stroke(d, (W / 2, y + size * 0.8), sub, font(POP, size * 0.36), WHT, stroke=5)
    return 1


