"""Builds engine64.py from engine63.py: strict remake of the OneCriticalMoment look (globe + regional map, red route arrow,
unit icons, fort/fire markers, dated top banner, snow seasons, stamps, HUD cards). Run: python3 mk_engine64.py"""
s = open("engine63.py").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('"""Map Shorts engine v63: strict remake of the MapTrail reference style (5wEVWjvaX2k), vertical 1080x1920 @30 fps.',
    '"""Map Shorts engine v64: remake of the OneCriticalMoment reference style (q6L_j157rGo), vertical 1080x1920 @30 fps.\n'
    'Adds: orthographic globe, snow seasons, route arrow, unit icons, forts/fire, dated banner, stamps, thermometer, HUD card.\n'
    'Based on engine63 (MapTrail style).')
rep('sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/turkey_2026_10_24")', 'sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/russia_2026_10_24")')
rep('from sat63 import SP, size', 'from sat64 import SP, size')
rep('SHORT = os.environ.get("SHORT", "turkey")', 'SHORT = os.environ.get("SHORT", "russia")')
rep('MB, MX, BANG, OSW = "assets/Montserrat-Black.ttf", "assets/Montserrat-ExtraBold.ttf", "assets/Bangers.ttf", "assets/Oswald-Regular.ttf"',
    'MB, MX, BANG, OSW = "assets/Montserrat-Black.ttf", "assets/Montserrat-ExtraBold.ttf", "assets/Bangers.ttf", "assets/Oswald-Regular.ttf"\nOSWB = "assets/Oswald-Bold.ttf"')
rep('''_TR10 = sorted(_shp("assets/ne10/ne_10m_admin_0_countries.shp", "ADMIN")["Turkey"], key=len)
COUNTRY["Anatolia10"] = [_TR10[-1]]                                                 # 10m parts for close-ups of Istanbul
COUNTRY["Thrace10"] = [_TR10[-2]]
DEM = np.load("assets/dem/tr_dem.npy").astype(np.float32)          # lon 25..46.5, lat 43.5..35, step 0.02
_gy, _gx = np.gradient(DEM)
SHADE = np.clip(0.75 + (-_gx - _gy) / 120.0, 0.35, 1.25).astype(np.float32)
''', '''RIVERS = _shp("assets/ne_rivers/ne_10m_rivers_lake_centerlines.shp", "name")
''')
rep('p = f"sat63g/{key}.jpg"', 'p = f"sat64g/{key}.jpg"')
rep('os.makedirs("sat63g", exist_ok=True)', 'os.makedirs("sat64g", exist_ok=True)')
rep('grade(Image.open(f"sat63/{key}.jpg")', 'grade(Image.open(f"sat64/{key}.jpg")')

# captions: up to 3 words, yellow active word, ~20 % from the bottom
rep('''        if len(_cur) == 2 or _w[-1] in ",.?!:" or _j == len(_ws) - 1 or len(_w) >= 9:''',
    '''        if len(_cur) == 3 or _w[-1] in ",.?!:" or _j == len(_ws) - 1 or len(_w) >= 11:''')
rep('f = fit(MB, 72, " ".join(txts), 960)', 'f = fit(MB, 78, " ".join(txts), 980)')
rep('put(img, lay, x + wd / 2, 1382, k)', 'put(img, lay, x + wd / 2, 1500, k)')

i = s.index("# ------------------------------------------------------------------ build")
head = s[:i]
head = head.replace("sat63", "sat64")

NEW = r'''
# ================================================================== v64 additions
import cv2  # noqa: E402

SEASON = []     # (t, f): 0 = summer, 1 = deep winter


def SN(t, f):
    SEASON.append((t, f))


def season(t):
    ks = sorted(SEASON)
    if not ks:
        return 0.0
    if t <= ks[0][0]:
        return ks[0][1]
    for (a, fa), (b, fb) in zip(ks, ks[1:]):
        if a <= t < b:
            return fa + (fb - fa) * ease((t - a) / max(1e-3, b - a))
    return ks[-1][1]


FLASH = []      # white flashes (snow arrives, cuts with impact)


def winter_rgb(a, lat, f):
    """a: HxWx3 float32 graded imagery, lat: per-row latitude (H,), f: 0..1 -> bright snow on land (relief kept), ice on water."""
    w = np.clip((lat - 38.0) / 14.0, 0, 1)
    w = w * w * (3 - 2 * w)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    water = ((b > r + 6) & (lum < 125))[..., None]
    land = ~water
    snow = np.array([252, 254, 255], np.float32)
    k = (f * w)[:, None, None]
    detail = ((lum - 95.0) * 0.7)[..., None]                       # forest / relief texture shows through the snow
    sn = (snow + detail) * np.array([0.96, 0.985, 1.0], np.float32)
    out = a * (1 - 0.93 * k * land) + sn * 0.93 * k * land
    kw = k * water * 0.8
    out = out * (1 - kw) + np.array([84, 156, 226], np.float32) * kw
    return np.clip(out, 0, 255)


def winterize(im, v, f):
    if f <= 0.01:
        return im
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    lat = v.lat + (v.h / 2 - np.arange(v.h)) / v.ppd
    return Image.fromarray(np.clip(winter_rgb(a, lat, f), 0, 255).astype(np.uint8)).convert("RGBA")


def render_map64(v):
    """render_map + fill of the empty rows (no imagery north of ~72.5 N at this scale) from the world image."""
    im = render_map(v).convert("RGB")
    a = np.asarray(im)
    rows = a.sum(axis=2).mean(axis=1) < 22
    if rows.any() and covers("WLD", v):
        base = crop("WLD", v).convert("RGB")
        m = rows.astype(np.float32)
        m = np.convolve(m, np.ones(25) / 25, "same")[:, None, None]
        im = Image.fromarray((np.asarray(base) * m + a * (1 - m)).astype(np.uint8))
    return im.convert("RGBA")


# ------------------------------------------------------------------ globe
class GlobeView:
    def __init__(self, lon, lat, R, cx=540, cy=960):
        self.lon, self.lat, self.R, self.cx, self.cy = lon, lat, R, cx, cy
        self.w, self.h = W, H
        self.span = 0

    def _raw(self, lon, lat):
        la, lo, la0, lo0 = math.radians(lat), math.radians(lon), math.radians(self.lat), math.radians(self.lon)
        cosc = math.sin(la0) * math.sin(la) + math.cos(la0) * math.cos(la) * math.cos(lo - lo0)
        x = math.cos(la) * math.sin(lo - lo0)
        y = math.cos(la0) * math.sin(la) - math.sin(la0) * math.cos(la) * math.cos(lo - lo0)
        return x, y, cosc

    def xy(self, lon, lat):
        x, y, c = self._raw(lon, lat)
        if c < 0:
            n = math.hypot(x, y) or 1.0
            x, y = x / n, y / n
        return self.cx + x * self.R, self.cy - y * self.R

    def vis(self, lon, lat):
        return self._raw(lon, lat)[2] > 0.02

    def pts(self, ring):
        return [self.xy(lo, la) for lo, la in ring]

    def geo_bbox(self):
        return self.lon - 90, self.lon + 90, self.lat - 90, self.lat + 90


_GL = {}


def globe_assets():
    if not _GL:
        a = np.asarray(sat("WLD")).copy()
        a[:57] = a[57]                      # no imagery beyond 85 N / S: repeat the last row (polar streaks hide in the glow)
        a[1990:] = a[1989]
        tex_s = a
        lat = 90.0 - (np.arange(a.shape[0]) + 0.5) / a.shape[0] * 180.0
        tex_w = np.clip(winter_rgb(a.astype(np.float32), lat, 1.0), 0, 255).astype(np.uint8)
        YYg, XXg = np.mgrid[0:H, 0:W].astype(np.float32)
        rng = np.random.default_rng(64)
        stars = np.zeros((H, W, 3), np.float32)
        stars += np.array([0, 5, 17], np.float32)
        for _ in range(420):
            x, y = int(rng.integers(0, W)), int(rng.integers(0, H))
            b = float(rng.uniform(80, 255))
            stars[y:y + 2, x:x + 2] = (b, b, min(255.0, b * 1.1))
        _GL.update(tex_s=tex_s, tex_w=tex_w, XX=XXg, YY=YYg, stars=stars)
    return _GL


def globe_img(v, f):
    g = globe_assets()
    X = (g["XX"] - v.cx) / v.R
    Y = (v.cy - g["YY"]) / v.R
    r2 = X * X + Y * Y
    inside = r2 <= 1.0
    Z = np.sqrt(np.maximum(0.0, 1.0 - r2))
    p0 = math.radians(v.lat)
    sinp = np.clip(Z * math.sin(p0) + Y * math.cos(p0), -1, 1)
    phi = np.arcsin(sinp)
    lam = math.radians(v.lon) + np.arctan2(X, Z * math.cos(p0) - Y * math.sin(p0))
    th, tw_ = g["tex_s"].shape[:2]
    mu = ((np.degrees(lam) + 180.0) % 360.0) / 360.0 * tw_
    mv = (90.0 - np.degrees(phi)) / 180.0 * th
    mu = mu.astype(np.float32)
    mv = mv.astype(np.float32)
    col = cv2.remap(g["tex_s"], mu, mv, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP).astype(np.float32)
    if f > 0.01:
        colw = cv2.remap(g["tex_w"], mu, mv, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP).astype(np.float32)
        col = col * (1 - f) + colw * f
    r = np.sqrt(r2)
    limb = np.clip((r - 0.86) / 0.14, 0, 1)
    col = col * (0.58 + 0.42 * Z[..., None] ** 0.35)
    col = col + limb[..., None] * np.array([40, 95, 150], np.float32) * 0.55
    glow = np.exp(-np.maximum(r - 1.0, 0) * 22.0)[..., None] * np.array([79, 163, 227], np.float32) * 0.85
    bg = g["stars"] + glow * (r >= 1.0)[..., None]
    out = np.where(inside[..., None], col, bg)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")


GCAM = []       # (t, lon, lat, R)
SCN = []        # (t0, t1) globe scenes; everything else is the flat map


def GK(t, lon, lat, R):
    GCAM.append((t, lon, lat, R))


def GLOBE(t0, t1):
    SCN.append((t0, t1))


def globe_cam(t):
    ks = sorted(GCAM)
    if t <= ks[0][0]:
        return ks[0][1:]
    for a, b in zip(ks, ks[1:]):
        if a[0] <= t < b[0]:
            u = ease((t - a[0]) / max(1e-3, b[0] - a[0]))
            return tuple(a[i] + (b[i] - a[i]) * u for i in (1, 2, 3))
    return ks[-1][1:]


def in_globe(t):
    return any(a <= t < b for a, b in SCN)


# ------------------------------------------------------------------ new overlays
def smooth_path(pts, n=14):
    """Catmull-Rom through geo waypoints -> dense list."""
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            u = k / n
            out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * u + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * u * u
                                    + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * u ** 3) for c in (0, 1)))
    out.append(P[-2])
    return out


def path_screen(v, geo):
    """-> list of (x, y, visible) for a dense geo path."""
    if isinstance(v, GlobeView):
        return [(*v.xy(lo, la), v.vis(lo, la)) for lo, la in geo]
    return [(*v.xy(lo, la), True) for lo, la in geo]


def arrow(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    geo = o.setdefault("_geo", smooth_path(o["pts"]))
    sp = path_screen(v, geo)
    k = ease((t - o["t0"]) / o.get("dur", 1.4))
    n = max(2, int(len(sp) * k))
    seg, cur = [], []
    for x, y, vis in sp[:n]:
        if vis:
            cur.append((x, y))
        elif cur:
            seg.append(cur)
            cur = []
    if cur:
        seg.append(cur)
    a = clamp((o["t1"] - t) / 0.25)
    w = o.get("w", 14)
    col = o.get("col", (255, 30, 39))
    lay = Image.new("RGBA", (W // 4, H // 4), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    for s_ in seg:
        if len(s_) > 1:
            dl.line([(x / 4, y / 4) for x, y in s_], fill=col + (200,), width=max(3, w // 2), joint="curve")
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(3)).resize((W, H), Image.BILINEAR))
    d = ImageDraw.Draw(img)
    for s_ in seg:
        if len(s_) > 1:
            d.line(s_, fill=(0, 0, 0, int(150 * a)), width=w + 10, joint="curve")
            d.line(s_, fill=WHT + (int(255 * a),), width=w + 5, joint="curve")
            d.line(s_, fill=col + (int(255 * a),), width=w, joint="curve")
    if (k < 1 or o.get("keephead")) and seg and len(seg[-1]) > 2 and sp[min(n, len(sp)) - 1][2]:
        (x1, y1), (x0, y0) = seg[-1][-1], seg[-1][-3]
        ang = math.atan2(y1 - y0, x1 - x0)
        L = w * 3.4
        tip = (x1 + math.cos(ang) * L * 0.55, y1 + math.sin(ang) * L * 0.55)
        base = [(x1 + math.cos(ang + 2.5) * L * 0.8, y1 + math.sin(ang + 2.5) * L * 0.8),
                (x1 + math.cos(ang - 2.5) * L * 0.8, y1 + math.sin(ang - 2.5) * L * 0.8)]
        d.polygon([tip] + base, fill=col + (int(255 * a),), outline=WHT + (int(255 * a),))
        d.line([tip, base[0], base[1], tip], fill=WHT + (int(255 * a),), width=4, joint="curve")


def boat_sprite(sz):
    key = ("boat", int(sz))
    if key not in _GL:
        c = Image.new("RGBA", (120, 96), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        d.polygon([(8, 56), (112, 56), (96, 84), (24, 84)], fill=(255, 215, 0, 255), outline=(10, 10, 14, 255))
        d.line([(60, 56), (60, 10)], fill=(10, 10, 14, 255), width=6)
        d.polygon([(64, 14), (64, 50), (100, 50)], fill=(255, 255, 255, 255), outline=(10, 10, 14, 255))
        d.line([(8, 56), (112, 56), (96, 84), (24, 84), (8, 56)], fill=(10, 10, 14, 255), width=5, joint="curve")
        _GL[key] = c.resize((int(sz), int(sz * 0.8)), Image.LANCZOS)
    return _GL[key]


def units(img, v, o, t):
    """Boats (or riders) travelling along the route path."""
    if t < o["t0"] or t > o["t1"]:
        return
    geo = o.setdefault("_geo", smooth_path(o["pts"]))
    sp = path_screen(v, geo)
    u = ease((t - o["t0"]) / o.get("dur", 1.4))
    a = clamp((o["t1"] - t) / 0.25) * clamp((t - o["t0"]) / 0.15)
    sprite = boat_sprite(o.get("size", 70))
    for i in range(o.get("n", 4)):
        uu = u - i * o.get("gap", 0.018)
        if uu < 0:
            continue
        j = min(len(sp) - 1, int(uu * (len(sp) - 1)))
        x, y, vis = sp[j]
        if not vis:
            continue
        bob = math.sin(t * 5 + i * 1.7) * 4
        sp_ = sprite.copy()
        if a < 1:
            sp_.putalpha(sp_.getchannel("A").point(lambda q: int(q * a)))
        img.alpha_composite(sp_, (int(x - sp_.width / 2 + (i % 2) * 8), int(y - sp_.height + bob + (i % 2) * 6)))


def fort(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.35)
    a = clamp((o["t1"] - t) / 0.25)
    X, Y = v.xy(o["lon"], o["lat"])
    d = ImageDraw.Draw(img)
    pr = clamp((t - o["t0"]) / 0.7)
    if pr < 1:
        r = 20 + 90 * pr
        d.ellipse((X - r, Y - r, X + r, Y + r), outline=(255, 215, 0, int(230 * (1 - pr))), width=5)
    s_ = o.get("s", 1.0) * k
    if s_ > 0.05:
        poly = [(-26, 0), (-26, -30), (0, -52), (26, -30), (26, 0)]
        poly = [(X + px * s_, Y + py * s_) for px, py in poly]
        d.polygon(poly, fill=(150, 98, 52, int(255 * a)), outline=WHT + (int(255 * a),))
        d.line(poly + [poly[0]], fill=WHT + (int(255 * a),), width=4, joint="curve")
        for dx in (-13, 0, 13):
            d.line((X + dx * s_, Y, X + dx * s_, Y - 26 * s_), fill=(70, 44, 20, int(255 * a)), width=3)
        d.polygon([(X - 6 * s_, Y - 52 * s_), (X + 20 * s_, Y - 62 * s_), (X - 6 * s_, Y - 72 * s_)], fill=(255, 30, 39, int(255 * a)))
        d.line((X - 6 * s_, Y - 52 * s_, X - 6 * s_, Y - 78 * s_), fill=WHT + (int(255 * a),), width=3)
    lab = text_layer(o["txt"], font(OSWB, o.get("size", 54)), WHT, 3, True, a)
    side = o.get("side", 1)
    put(img, lab, X + side * (lab.width / 2 + 38), Y - 30, k)
    if o.get("year"):
        yl = text_layer(str(o["year"]), font(OSWB, o.get("size", 54) * 0.82), (255, 214, 0), 3, True, a)
        put(img, yl, X + side * (lab.width / 2 + 38), Y + 18, k)


def flame(d, X, Y, h, ph, a):
    w = h * 0.42
    for scale, col in ((1.0, (230, 40, 20)), (0.75, (255, 130, 20)), (0.45, (255, 220, 60))):
        hh, ww = h * scale, w * scale
        sway = math.sin(ph * 9 + scale * 3) * ww * 0.35
        pts = [(X - ww, Y), (X - ww * 1.05, Y - hh * 0.35), (X - ww * 0.5, Y - hh * 0.7), (X + sway, Y - hh),
               (X + ww * 0.6, Y - hh * 0.65), (X + ww * 1.05, Y - hh * 0.3), (X + ww, Y)]
        d.polygon(pts, fill=col + (int(235 * a),))


def fire(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    a = clamp((o["t1"] - t) / 0.3) * clamp((t - o["t0"]) / 0.12)
    X, Y = v.xy(o["lon"], o["lat"])
    d = ImageDraw.Draw(img)
    h = o.get("h", 120) * back((t - o["t0"]) / 0.4)
    for dx in (-0.55, 0.0, 0.5):
        flame(d, X + dx * h * 0.55, Y, h * (1.0 if dx == 0 else 0.7), t + dx, a)


def banner(img, v, o, t):
    """Top plaque: red pill (year / word, odometer roll) + dark banner (name) + season icon, like the reference."""
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.3) * clamp((o["t1"] - t) / 0.2)
    if k <= 0.02:
        return
    y = 108 - (1 - clamp(k)) * 140
    pill = o["pill"]
    if isinstance(pill, tuple):
        val = pill[0] + (pill[1] - pill[0]) * ease((t - o["t0"]) / o.get("roll", 0.55))
        pill = f"{val:.0f}"
    fp, fn_ = font(OSWB, 64), font(OSWB, 56)
    pw = max(190, fp.getlength(pill) + 70)
    nw = fn_.getlength(o["name"]) + 120
    x0 = 540 - (pw + nw) / 2
    lay = Image.new("RGBA", (int(pw + nw + 20), 120), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((10, 10, 10 + pw, 100), 24, fill=(226, 24, 30, 255), outline=WHT + (255,), width=4)
    d.rounded_rectangle((10 + pw - 18, 10, 10 + pw + nw, 100), 24, fill=(14, 20, 28, 235), outline=WHT + (255,), width=4)
    d.rounded_rectangle((10 + pw - 18, 10, 10 + pw + 6, 100), 8, fill=(226, 24, 30, 255))
    d.text((10 + pw / 2, 57), pill, font=fp, fill=WHT + (255,), anchor="mm")
    d.text((10 + pw + 28 + (nw - 120) / 2 + 20, 57), o["name"], font=fn_, fill=WHT + (255,), anchor="mm")
    ic = o.get("icon")
    cx, cy = 10 + pw + nw - 44, 55
    if ic == "snow":
        for ang in (0, 60, 120):
            dx, dy = math.cos(math.radians(ang)) * 24, math.sin(math.radians(ang)) * 24
            d.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=(170, 220, 255, 255), width=5)
    elif ic == "sun":
        d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=(255, 214, 0, 255))
        for ang in range(0, 360, 45):
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line((cx + dx * 16, cy + dy * 16, cx + dx * 25, cy + dy * 25), fill=(255, 214, 0, 255), width=4)
    put(img, lay, x0 + lay.width / 2 - 10, y + 50, 1.0)


def stamp(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    dt = t - o["t0"]
    k = 1.0 + 0.9 * clamp(1 - dt / 0.16)
    a = clamp((o["t1"] - t) / 0.2)
    f = fit(OSWB, o.get("size", 118), o["txt"], 900)
    tw = f.getlength(o["txt"])
    lay = Image.new("RGBA", (int(tw + 120), int(f.size * 1.45)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    col = o.get("col", (214, 20, 28))
    d.rounded_rectangle((6, 6, lay.width - 6, lay.height - 6), 16, outline=col + (int(255 * a),), width=10, fill=(0, 0, 0, int(120 * a)))
    d.text((lay.width / 2, lay.height / 2 + 4), o["txt"], font=f, fill=col + (int(255 * a),), anchor="mm", stroke_width=3, stroke_fill=WHT + (int(255 * a),))
    X, Y = (o["x"], o["y"]) if "x" in o else v.xy(o["lon"], o["lat"])
    put(img, lay, X, Y, k, o.get("angle", -6))


def thermo(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    k = back((t - o["t0"]) / 0.35) * clamp((o["t1"] - t) / 0.25)
    val = o["v0"] + (o["v1"] - o["v0"]) * ease((t - o["t0"] - 0.2) / o.get("dur", 1.6))
    x, y0, hgt = o.get("x", 150), o.get("y", 520), 640
    lay = Image.new("RGBA", (320, hgt + 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((10, 10, 310, hgt + 210), 28, fill=(8, 14, 22, 205), outline=WHT + (255,), width=3)
    tx0, tx1, ty0, ty1 = 80, 140, 40, 40 + hgt - 70
    d.rounded_rectangle((tx0, ty0, tx1, ty1 + 60), 30, fill=(30, 40, 52, 255), outline=WHT + (255,), width=4)
    frac = clamp((val + 70) / 100.0)
    my = ty1 - frac * (ty1 - ty0 - 10)
    col = (255, 60, 50) if val > 0 else (90, 200, 255)
    d.rounded_rectangle((tx0 + 12, my, tx1 - 12, ty1 + 50), 18, fill=col + (255,))
    d.ellipse((tx0 - 14, ty1 + 10, tx1 + 14, ty1 + 100), fill=col + (255,), outline=WHT + (255,), width=4)
    for tv in range(-60, 21, 20):
        yy = ty1 - clamp((tv + 70) / 100.0) * (ty1 - ty0 - 10)
        d.line((tx1 + 8, yy, tx1 + 34, yy), fill=WHT + (255,), width=3)
        d.text((tx1 + 42, yy), f"{tv}", font=font(OSW, 34), fill=WHT + (255,), anchor="lm")
    d.text((160, hgt + 150), f"{val:.0f}°C".replace("-", "−"), font=font(OSWB, 84), fill=col + (255,), anchor="mm", stroke_width=3, stroke_fill=BLK + (255,))
    put(img, lay, x + 10, y0 + lay.height / 2, k)


def hudcard(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    k = clamp((t - o["t0"]) / 0.3) * clamp((o["t1"] - t) / 0.25)
    rows = o["rows"]
    rh = 96
    hh = 120 + rh * len(rows)
    lay = Image.new("RGBA", (900, hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((4, 4, 896, hh - 4), 30, fill=(8, 14, 22, int(215 * k)), outline=WHT + (int(255 * k),), width=3)
    d.text((450, 56), o["title"], font=font(OSWB, 58), fill=(255, 214, 0, int(255 * k)), anchor="mm")
    for i, (txt, val, frac, col) in enumerate(rows):
        dt = t - o["t0"] - 0.35 - i * 0.28
        if dt < 0:
            continue
        p = ease(dt / 0.55)
        y = 120 + i * rh + rh / 2 - 4
        d.text((36, y - 26), txt, font=font(OSWB, 42), fill=WHT + (255,), anchor="lm")
        d.text((864, y - 26), val, font=font(OSWB, 42), fill=col + (255,), anchor="rm")
        d.rounded_rectangle((36, y + 4, 864, y + 30), 13, fill=(40, 52, 66, 255))
        if frac * p > 0.01:
            d.rounded_rectangle((36, y + 4, 36 + 828 * frac * p, y + 30), 13, fill=col + (255,))
    put(img, lay, o.get("x", 540), o.get("y", 960), 1.0)


def rivers(img, v, o, t):
    if t < o["t0"] or t > o["t1"]:
        return
    a = fade(o, t, 0.5, 0.3)
    d = ImageDraw.Draw(img)
    for nm in o["names"]:
        for ln in RIVERS.get(nm, []):
            p = v.pts(ln[:: o.get("step", 2)])
            xs = [q[0] for q in p]
            ys = [q[1] for q in p]
            if max(xs) < -50 or min(xs) > W + 50 or max(ys) < -50 or min(ys) > H + 50:
                continue
            d.line(p, fill=(150, 225, 255, int(255 * a)), width=o.get("w", 6), joint="curve")


def snowfall(img, t, f):
    if f < 0.25:
        return
    n = int(160 * f)
    rng = np.random.default_rng(7)
    xs = rng.uniform(0, W, n)
    ys = rng.uniform(0, H, n)
    sp = rng.uniform(90, 220, n)
    sz = rng.uniform(2.5, 6.5, n)
    ph = rng.uniform(0, 6.28, n)
    d = ImageDraw.Draw(img)
    for i in range(n):
        x = (xs[i] + math.sin(t * 1.4 + ph[i]) * 30) % W
        y = (ys[i] + t * sp[i]) % H
        d.ellipse((x - sz[i], y - sz[i], x + sz[i], y + sz[i]), fill=(255, 255, 255, 200))


_label0 = label


def label(img, v, o, t):
    if "lon" in o and not isinstance(v, GlobeView) and t >= o["t0"]:
        X, Y = v.xy(o["lon"], o["lat"])
        w_ = font(o.get("font", OSW), o.get("size", 60) * (1.2 if o.get("font", OSW) == OSW else 1.0)).getlength(o["txt"]) / 2 + 24
        if X < w_ or X > W - w_:
            o2 = dict(o)
            o2.pop("lon"); o2.pop("lat")
            o2["x"], o2["y"] = min(max(X, w_), W - w_), Y
            return _label0(img, v, o2, t)
    return _label0(img, v, o, t)


DRAW.update({"label": label, "arrow": arrow, "units": units, "fort": fort, "fire": fire, "banner": banner, "stamp": stamp, "thermo": thermo,
             "hudcard": hudcard, "rivers": rivers})
ORDER = ["fill", "rivers", "arrow", "units", "fort", "fire", "pin", "curved", "label", "counter", "stamp", "thermo", "hudcard", "banner"]


# ------------------------------------------------------------------ build
import shots64  # noqa: E402

shots64.build(SHORT, K, O, GK, GLOBE, SN, FLASH, WT, ST, D)
CUTS = sorted({k[0] for k in CAM if k[4]} | {a for a, b in SCN} | {b for a, b in SCN})
SHAKES = sorted([o["t0"] for o in OV if o["kind"] == "stamp"] + [o["t0"] for o in OV if o.get("shake")])


def credit(img, extra=""):
    ImageDraw.Draw(img).text((W - 16, H - 12), "Imagery © Esri, Maxar, Earthstar Geographics · Natural Earth" + extra,
                             font=font(MX, 16), fill=(255, 255, 255, 150), anchor="rs")


def frame(fi):
    t = fi / FPS
    f = season(t)
    glob = in_globe(t)
    if glob:
        v = GlobeView(*globe_cam(t))
        img = globe_img(v, f)
    else:
        v = View(*camera(t))
        img = winterize(render_map64(v), v, f)
    live = [o for o in OV if o["t0"] - 0.01 <= t <= o["t1"] + 0.01 and (o.get("scene", "flat") in (("globe", "both") if glob else ("flat", "both")))]
    for kind in ORDER:
        for o in live:
            if o["kind"] == kind:
                DRAW[kind](img, v, o, t)
    if not glob:
        snowfall(img, t, f)
    credit(img)
    caption(img, t)
    arr = np.asarray(img.convert("RGB")).astype(np.float32)
    for fl in FLASH:
        if 0 <= t - fl < 0.16:
            arr = arr + (255 - arr) * (1 - (t - fl) / 0.16) * 0.8
    sk = 0.0
    for s_ in SHAKES:
        if 0 <= t - s_ < 0.28:
            sk = max(sk, 14 * (1 - (t - s_) / 0.28))
    dx, dy = int(sk * math.sin(t * 90)), int(sk * math.cos(t * 77))
    if dx or dy:
        arr = np.roll(arr, (dy, dx), axis=(0, 1))
    a = (np.clip(arr, 0, 255).astype(np.uint16) * VIG) >> 8
    return a.astype(np.uint8)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        print(SHORT, "frames", NF, "total", round(TOTAL, 2), "keys", len(CAM), "overlays", len(OV), "cuts", [round(c, 2) for c in CUTS])
    elif cmd == "still":
        os.makedirs(f"{SHORT}/stills64", exist_ok=True)
        for a in sys.argv[2:]:
            Image.fromarray(frame(int(float(a) * FPS))).save(f"{SHORT}/stills64/{float(a):05.1f}.jpg", quality=86)
    elif cmd == "video":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                              "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).tobytes())
        p.stdin.close()
        p.wait()
'''
open("engine64.py", "w").write(head + NEW)
print("engine64.py written", len(head + NEW))
