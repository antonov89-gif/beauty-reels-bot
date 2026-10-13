"""Infinite-zoom loop Short (9:16): EUR 1 coin -> Europe -> Switzerland -> Zurich -> Paradeplatz hatch -> vault door
-> gold bar stamp -> the same hand with the coin.  Every level is drawn procedurally at any scale; children sit in a
circular window at the frame centre.  python3 engine29.py still N.. | info | prefetch | video A B out.mp4"""
import math, subprocess, sys
import numpy as np
import shapefile
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import tiles

W, H, FPS, SS = 1080, 1920, 30, 2
W2, H2 = W * SS, H * SS
POPX, POP = "Poppins-ExtraBold.ttf", "Poppins-Bold.ttf"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
BPM = 105.0
BEAT = 60.0 / BPM
CYCLE = 42 * BEAT                      # 7 phrases x 6 beats = 24.0 s
NF = int(round(CYCLE * FPS))
T0 = 0.35                              # video starts slightly into the first move (hook: motion at once)
HD = 0.5 * math.hypot(W, H)            # half diagonal in px (1x)
WR = 0.58                              # window radius (in child frame-heights) that covers the child frame

PAR = (8.5390, 47.3697)                # Paradeplatz, Zurich
SPAN0 = 40.0                           # map frame width in degrees at map zoom 1 (Europe)
SP_END = 0.00022
R = {"A": 6.0, "M": SPAN0 / SP_END, "D": 6.0, "G": 8.0}
ORDER = ["A", "M", "D", "G"]
# stops on the global log-zoom axis
U_LEVEL = {}
u = 0.0
for k in ORDER:
    U_LEVEL[k] = u; u += math.log(R[k])
U_TOTAL = u
STOPS = [0.0, U_LEVEL["M"], U_LEVEL["M"] + math.log(SPAN0 / 6.0), U_LEVEL["M"] + math.log(SPAN0 / 0.25),
         U_LEVEL["M"] + math.log(SPAN0 / 0.004), U_LEVEL["D"], U_LEVEL["G"], U_TOTAL]
LABELS = [("THE €1 COIN HAS A MAP ON IT", "🪙"), ("21 COUNTRIES USE THE EURO", "🇪🇺"), ("SWITZERLAND? IT USES THE FRANC", "🇨🇭"),
          ("ZURICH: SWISS BANKING CAPITAL", "🏦"), ("PARADEPLATZ: THE BANK SQUARE", "📍"), ("LEGEND: GOLD VAULTS BELOW", "🤫"),
          ("ONE GOOD DELIVERY BAR ≈ 12.4 KG", "🥇")]
MOVE, HOLD = 4 * BEAT, 2 * BEAT


def ease(x):
    x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)


def ease5(x):
    x = min(1.0, max(0.0, x)); return x * x * x * (x * (x * 6 - 15) + 10)


def u_at(tc):
    """global log zoom at cycle time tc; phrase k = move (4 beats) stop k -> k+1, then hold (2 beats) at k+1."""
    tc %= CYCLE
    k = int(tc // (MOVE + HOLD)); lt = tc - k * (MOVE + HOLD)
    a, b = STOPS[k], STOPS[k + 1]
    return a + (b - a) * ease5(lt / MOVE), k, lt


def top_level(u):
    for k in reversed(ORDER):
        if u >= U_LEVEL[k] - 1e-9: return k, u - U_LEVEL[k]
    return "A", u


def nxt(k): return ORDER[(ORDER.index(k) + 1) % len(ORDER)]


_F = {}
def font(p, s):
    s = max(1, int(s))
    if (p, s) not in _F: _F[(p, s)] = ImageFont.truetype(p, s)
    return _F[(p, s)]


# ------------------------------------------------------------------ geometry helpers (canvas = 2x)
CX, CY = W2 / 2, H2 / 2


def P(x, y, s):  # level units -> canvas px; s = canvas px per level unit
    return CX + x * s, CY + y * s


def circle(d, x, y, r, s, **kw):
    cx, cy = P(x, y, s); rr = r * s
    if rr < 0.3 or rr > 4e5: return
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), **kw)


def ring(d, x, y, r0, r1, s, fill):
    cx, cy = P(x, y, s); a, b = r0 * s, r1 * s
    if b < 0.3 or a > 4e5: return
    w = max(1, int(b - a))
    rm = (a + b) / 2
    d.ellipse((cx - rm, cy - rm, cx + rm, cy + rm), outline=fill, width=w)


def capsule(d, x0, y0, x1, y1, w, s, fill, outline=None, ow=0):
    p0, p1 = P(x0, y0, s), P(x1, y1, s); ww = w * s
    if outline:
        d.line([p0, p1], fill=outline, width=int(ww + 2 * ow * s))
        for p in (p0, p1): d.ellipse((p[0] - ww / 2 - ow * s, p[1] - ww / 2 - ow * s, p[0] + ww / 2 + ow * s, p[1] + ww / 2 + ow * s), fill=outline)
    d.line([p0, p1], fill=fill, width=int(ww))
    for p in (p0, p1): d.ellipse((p[0] - ww / 2, p[1] - ww / 2, p[0] + ww / 2, p[1] + ww / 2), fill=fill)


def poly(d, pts, s, **kw): d.polygon([P(x, y, s) for x, y in pts], **kw)


def radial_bg(c_in, c_out, s, cx=0.0, cy=0.0, rad=0.9):
    yy, xx = np.mgrid[0:H2 // 8, 0:W2 // 8].astype(np.float32)
    px, py = P(cx, cy, s)
    dd = np.sqrt((xx * 8 - px) ** 2 + (yy * 8 - py) ** 2) / max(1e-3, rad * s)
    k = np.clip(dd, 0, 1)[..., None]
    a = np.array(c_in, np.float32) * (1 - k) + np.array(c_out, np.float32) * k
    return Image.fromarray(a.astype(np.uint8)).resize((W2, H2), Image.BILINEAR).convert("RGBA")


def star(d, x, y, r, s, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * 0.45
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    poly(d, pts, s, fill=fill)


# ------------------------------------------------------------------ level A: hand holding a EUR 1 coin
SKIN, SKIN_D, SLEEVE = (240, 190, 150), (196, 136, 100), (40, 110, 200)
BRASS, BRASS_D, BRASS_L = (214, 172, 66), (150, 112, 30), (250, 222, 130)


def draw_A(s):
    img = radial_bg((255, 250, 236), (246, 214, 170), s, 0, -0.05, 0.75); d = ImageDraw.Draw(img)
    # arm + hand from bottom right, palm under the coin
    poly(d, [(0.14, 0.62), (0.40, 0.62), (0.33, 0.31), (0.12, 0.34)], s, fill=SLEEVE)
    poly(d, [(0.12, 0.34), (0.33, 0.31), (0.32, 0.27), (0.11, 0.30)], s, fill=(30, 85, 160))
    circle(d, 0.07, 0.24, 0.165, s, fill=SKIN_D); circle(d, 0.07, 0.235, 0.155, s, fill=SKIN)
    for i, fx in enumerate((-0.10, -0.045, 0.01, 0.065)):
        capsule(d, fx + 0.03, 0.2, fx - 0.005, 0.135 - (0.01 if i in (1, 2) else 0), 0.052, s, SKIN, SKIN_D, 0.006)
    # shadow of the coin on the fingers
    sh = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    cx, cy = P(0.012, 0.03, s); rr = 0.128 * s
    if rr < 4e5: ds.ellipse((cx - rr, cy - rr * 0.98, cx + rr, cy + rr * 0.98), fill=(90, 50, 20, 90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(max(1, 0.012 * s))) if 0.012 * s < 200 else sh)
    capsule(d, -0.16, 0.25, -0.155, 0.12, 0.058, s, SKIN, SKIN_D, 0.006)          # thumb, left of the coin
    return img


def over_A(img, s, f):
    d = ImageDraw.Draw(img); r = WR / R["A"]
    ring(d, 0, 0, r, r * 1.33, s, BRASS)
    ring(d, 0, 0, r * 1.29, r * 1.33, s, BRASS_D)
    ring(d, 0, 0, r * 1.0, r * 1.035, s, BRASS_D)
    ring(d, 0, 0, r * 1.05, r * 1.09, s, BRASS_L)
    for i in range(12):
        a = -math.pi / 2 + i * math.pi / 6
        star(d, math.cos(a) * r * 1.19, math.sin(a) * r * 1.19, r * 0.06, s, BRASS_D)
    a = 1 - ease(f * 3)
    if a > 0.02 and 0.2 * r * s < 3000:
        lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        f1 = font(POPX, 0.62 * r * s); f2 = font(POPX, 0.2 * r * s)
        x, y = P(-0.45 * r, -0.05 * r, s)
        dl.text((x, y), "1", font=f1, fill=(70, 74, 86, int(230 * a)), anchor="mm", stroke_width=max(1, int(0.02 * r * s)), stroke_fill=(235, 238, 245, int(200 * a)))
        x, y = P(0.35 * r, 0.55 * r, s)
        dl.text((x, y), "EURO", font=f2, fill=(70, 74, 86, int(230 * a)), anchor="mm")
        img.alpha_composite(lay)


# ------------------------------------------------------------------ level M: satellite map centred on Paradeplatz
_R = shapefile.Reader("/home/claude/v15/assets/ne50/ne_50m_admin_0_countries.shp")
_FL = [x[0] for x in _R.fields[1:]]
SWISS = []
for rec, shp in zip(_R.records(), _R.shapes()):
    if rec[_FL.index("NAME")] == "Switzerland":
        pts, parts = shp.points, list(shp.parts) + [len(shp.points)]
        SWISS = [pts[a:b] for a, b in zip(parts, parts[1:])]
EURO21 = {"Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Estonia", "Finland", "France", "Germany", "Greece", "Ireland", "Italy",
          "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands", "Portugal", "Slovakia", "Slovenia", "Spain"}
EUROZ = []
for rec, shp in zip(_R.records(), _R.shapes()):
    if rec[_FL.index("NAME")] in EURO21:
        pts, parts = shp.points, list(shp.parts) + [len(shp.points)]
        EUROZ += [pts[a:b] for a, b in zip(parts, parts[1:]) if b - a > 12]


def map_cam(s):
    span = SPAN0 * H2 / s
    return tiles.Cam(PAR[0], PAR[1], span, src="esri", zmax=19), span


def grade(im):
    a = np.asarray(im).astype(np.float32) / 255
    a = a ** 0.85; g = a.mean(2, keepdims=True); a = g + (a - g) * 1.25
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


STATE = {"stop": 0, "lt": 0.0, "top": "A"}


def draw_M(s):
    cam, span = map_cam(s)
    if span > 2000: return Image.new("RGBA", (W2, H2), (20, 50, 90, 255))
    im = grade(cam.render()).resize((W2, H2), Image.BILINEAR).convert("RGBA")
    # country highlights only while the map is the top level, at their stop
    if STATE["top"] == "M":
        st, lt = STATE["stop"], STATE["lt"]
        def hl(rings, col, a):
            if a <= 0: return
            lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            for rg in rings:
                p = [tuple(v * SS for v in cam.xy(lo, la)) for lo, la in rg]
                dl.polygon(p, fill=col + (int(80 * a),)); dl.line(p + [p[0]], fill=(255, 255, 255, int(230 * a)), width=5)
            im.alpha_composite(lay)
        # alpha: rises at the end of the move into that stop, falls during the next move
        def win(k):
            if st == k - 1: return ease((lt - MOVE * 0.7) / (MOVE * 0.3))
            if st == k: return 1 - ease(lt / (MOVE * 0.45))
            return 0
        hl(EUROZ, (40, 90, 220), win(1))
        hl(SWISS, (230, 40, 40), win(2))
    return im


def over_M(img, s, f):
    d = ImageDraw.Draw(img); r = WR / R["M"]
    if r * s < 1: return
    t = STATE["tc"]
    # glowing round hatch on the square
    glow = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); dg = ImageDraw.Draw(glow)
    pul = 1.0 + 0.12 * math.sin(t * 2 * math.pi / BEAT)
    if r * s * 1.9 < 6000:
        circle(dg, 0, 0, r * 1.75 * pul, s, fill=(255, 205, 60, 120))
        img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(1, r * s * 0.35))))
    ring(d, 0, 0, r, r * 1.32, s, (70, 74, 82))
    ring(d, 0, 0, r * 1.25, r * 1.32, s, (40, 42, 48))
    ring(d, 0, 0, r, r * 1.04, s, (150, 155, 165))
    for i in range(12):
        a = i * math.pi / 6
        circle(d, math.cos(a) * r * 1.16, math.sin(a) * r * 1.16, r * 0.045, s, fill=(185, 190, 200))


# ------------------------------------------------------------------ level D: steel vault door with a porthole
def draw_D(s):
    img = radial_bg((92, 96, 104), (30, 32, 38), s, 0, 0, 0.8); d = ImageDraw.Draw(img)
    for i in range(-6, 7):        # concrete panel joints
        x0, _ = P(i * 0.16, 0, s)
        if -50 < x0 < W2 + 50: d.line([(x0, 0), (x0, H2)], fill=(60, 62, 68), width=max(1, int(0.003 * s)))
    for j in range(-8, 9):
        _, y0 = P(0, j * 0.16, s)
        if -50 < y0 < H2 + 50: d.line([(0, y0), (W2, y0)], fill=(60, 62, 68), width=max(1, int(0.003 * s)))
    circle(d, 0, 0, 0.33, s, fill=(48, 50, 56))
    circle(d, 0, 0, 0.31, s, fill=(150, 156, 166))
    circle(d, 0, 0, 0.27, s, fill=(118, 124, 134))
    ring(d, 0, 0, 0.255, 0.262, s, (90, 95, 104))
    for i in range(20):
        a = i * math.pi / 10
        circle(d, math.cos(a) * 0.29, math.sin(a) * 0.29, 0.011, s, fill=(205, 210, 218))
    # hinge
    poly(d, [(0.30, -0.10), (0.37, -0.10), (0.37, 0.10), (0.30, 0.10)], s, fill=(70, 74, 82))
    return img


def over_D(img, s, f):
    d = ImageDraw.Draw(img); r = WR / R["D"]
    for i in range(6):            # handle wheel spokes outside the porthole
        a = i * math.pi / 3 + 0.3
        capsule(d, math.cos(a) * r * 1.25, math.sin(a) * r * 1.25, math.cos(a) * 0.205, math.sin(a) * 0.205, 0.016, s, (210, 214, 222), (60, 64, 72), 0.003)
    ring(d, 0, 0, 0.198, 0.214, s, (210, 214, 222))
    ring(d, 0, 0, r, r * 1.22, s, (196, 158, 70))
    ring(d, 0, 0, r * 1.17, r * 1.22, s, (120, 90, 30))
    for i in range(8):
        a = i * math.pi / 4 + 0.39
        circle(d, math.cos(a) * r * 1.11, math.sin(a) * r * 1.11, r * 0.035, s, fill=(240, 220, 150))
    a = 1 - ease(f * 2.5)       # glass glare
    if a > 0.02 and r * s < 6000:
        lay = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        cx, cy = P(-0.3 * r, -0.35 * r, s); rr = r * s * 0.5
        dl.ellipse((cx - rr, cy - rr * 0.5, cx + rr, cy + rr * 0.5), fill=(255, 255, 255, int(70 * a)))
        img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(max(1, rr * 0.2))))


# ------------------------------------------------------------------ level G: stacked gold bars, stamp at centre
GOLD_T, GOLD_F, GOLD_D, GOLD_L = (255, 214, 92), (232, 176, 48), (150, 100, 20), (255, 238, 160)


def bar(d, x, y, w, h, s):
    tw = w * 0.78
    poly(d, [(x - w / 2, y + h / 2), (x + w / 2, y + h / 2), (x + tw / 2, y - h / 2), (x - tw / 2, y - h / 2)], s, fill=GOLD_F, outline=GOLD_D, width=max(1, int(0.004 * s)))
    poly(d, [(x - tw / 2, y - h / 2), (x + tw / 2, y - h / 2), (x + tw / 2 - h * 0.25, y - h / 2 - h * 0.28), (x - tw / 2 + h * 0.25, y - h / 2 - h * 0.28)], s, fill=GOLD_T, outline=GOLD_D, width=max(1, int(0.004 * s)))
    poly(d, [(x - w / 2 + w * 0.06, y + h / 2 - h * 0.12), (x - tw / 2 + w * 0.04, y - h / 2 + h * 0.1), (x - tw / 2 + w * 0.09, y - h / 2 + h * 0.1), (x - w / 2 + w * 0.12, y + h / 2 - h * 0.12)], s, fill=GOLD_L)


def draw_G(s):
    img = radial_bg((120, 80, 30), (18, 14, 10), s, 0, 0, 0.75); d = ImageDraw.Draw(img)
    bw, bh = 0.46, 0.22
    for row, (n, y) in enumerate(((2, -0.5), (3, -0.25), (2, 0.25), (3, 0.5))):
        for i in range(n):
            bar(d, (i - (n - 1) / 2) * (bw + 0.03), y, bw, bh, s)
    for x in (-(bw + 0.03), bw + 0.03): bar(d, x, 0, bw, bh, s)
    bar(d, 0, 0, bw, bh, s)
    return img


def over_G(img, s, f):
    d = ImageDraw.Draw(img); r = WR / R["G"]
    ring(d, 0, 0, r, r * 1.12, s, GOLD_D)
    ring(d, 0, 0, r * 1.16, r * 1.2, s, GOLD_D)
    if 0.03 * s < 3000:
        for txt, x, y, sz in (("999.9", -0.165, -0.045, 0.026), ("FINE GOLD", 0.165, -0.045, 0.02), ("≈12.4 KG", -0.165, 0.05, 0.022), ("SWISS", 0.165, 0.05, 0.022)):
            px, py = P(x, y, s)
            d.text((px, py), txt, font=font(POPX, sz * s), fill=GOLD_D, anchor="mm")


# ------------------------------------------------------------------ tints for children seen through windows
def tint(img, kind, a):
    if a <= 0.01 or kind is None: return img
    arr = np.asarray(img).astype(np.float32)
    g = (arr[..., :3] @ np.array([0.3, 0.59, 0.11], np.float32))[..., None] / 255
    if kind == "silver":
        m = np.concatenate([g * 175 + 70, g * 180 + 72, g * 190 + 78], 2)
    else:
        m = np.concatenate([g * 170 + 85, g * 140 + 55, g * 70 + 10], 2)
    arr[..., :3] = arr[..., :3] * (1 - a) + m * a
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


DRAW = {"A": draw_A, "M": draw_M, "D": draw_D, "G": draw_G}
OVER = {"A": over_A, "M": over_M, "D": over_D, "G": over_G}
TINT = {"A": "silver", "M": None, "D": None, "G": "gold"}      # tint of the CHILD seen through this level's window


def render_level(k, s, f, depth=0):
    img = DRAW[k](s)
    rr = WR / R[k] * s
    if depth < 3 and rr > 2:
        c = nxt(k)
        child = render_level(c, s / R[k], 0.0, depth + 1)
        child = tint(child, TINT[k], 1 - ease(f) if depth == 0 else 1.0)
        mask = Image.new("L", (W2, H2), 0)
        ImageDraw.Draw(mask).ellipse((CX - rr, CY - rr, CX + rr, CY + rr), fill=255)
        img.paste(child, (0, 0), mask)
    OVER[k](img, s, f if depth == 0 else 0.0)
    return img


# ------------------------------------------------------------------ labels
_EMO = {}
def emoji(ch, size):
    if ch not in _EMO:
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((80, 80), ch, font=ImageFont.truetype(EMOJI, 109), embedded_color=True, anchor="mm")
        _EMO[ch] = im
    return _EMO[ch].resize((int(size), int(size)), Image.LANCZOS)


def label(img, txt, ch, k):
    if k <= 0.02: return
    f = font(POPX, 50); tw = f.getlength(txt)
    pw, ph = tw + 150, 104
    lay = Image.new("RGBA", (int(pw) + 20, ph + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((10, 10, 10 + pw, 10 + ph), 52, fill=(12, 18, 32, 235), outline=(255, 255, 255, 255), width=5)
    d.text((10 + 120, 10 + ph / 2 + 2), txt, font=f, fill=(255, 255, 255), anchor="lm")
    lay.alpha_composite(emoji(ch, 74), (10 + 28, 10 + 15))
    sc = 0.6 + 0.4 * min(1.0, k * 1.15) if k < 1 else 1.0
    lay = lay.resize((max(1, int(lay.width * sc)), max(1, int(lay.height * sc))), Image.BILINEAR)
    if k < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * min(1, k * 1.4))))
    img.alpha_composite(lay, (int(W / 2 - lay.width / 2), int(300 - lay.height / 2)))


def frame(fi):
    tc = (T0 + fi / FPS) % CYCLE
    u, k, lt = u_at(tc)
    top, ul = top_level(u)
    STATE.update(stop=k, lt=lt, top=top, tc=tc)
    s = H2 * math.exp(ul)
    f = ul / math.log(R[top])
    img = render_level(top, s, f)
    out = img.resize((W, H), Image.LANCZOS)
    # label of the stop we are arriving at / holding
    st = k + 1 if lt > MOVE * 0.75 else k
    if st == 7: st = 0
    if lt > MOVE * 0.75: kk = (lt - MOVE * 0.75) / 0.25
    else: kk = 1 - ease((lt - MOVE * 0.25) / 0.25)
    label(out, *LABELS[st], kk)
    return out.convert("RGB")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "still":
        for a in sys.argv[2:]: frame(int(a)).save(f"still_{int(a):04d}.png")
    elif cmd == "info":
        print("cycle", round(CYCLE, 3), "frames", NF, "R_M", round(R["M"]), "stops", [round(x, 2) for x in STOPS])
    elif cmd == "prefetch":
        keys = []
        for fi in range(0, NF, 2):
            tc = (T0 + fi / FPS) % CYCLE; u, k, lt = u_at(tc)
            for lvl in ORDER:   # map whenever it is drawn large enough (top or child)
                pass
            top, ul = top_level(u); s = H2 * math.exp(ul)
            ss = {"M": s, "A": s / R["A"]}.get(top)
            if ss is None: continue
            cam, span = map_cam(ss)
            if span < 2000: keys += cam.keys()
        print(tiles.prefetch(keys, 24))
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
            if fi % 30 == 0: print(fi, flush=True)
        p.stdin.close(); p.wait()
