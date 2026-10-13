# ---- animation layer for engine28 (exec'd into engine namespace)
def clean(w): return "".join(c for c in w.lower() if c.isalnum())


def WT(i, word):
    ws = [clean(w) for w in LINES[i].split()]; q = clean(word)
    for j, w in enumerate(ws):
        if w == q: return ST[i] + TW[i][j]
    for j, w in enumerate(ws):
        if q in w: return ST[i] + TW[i][j]
    raise KeyError((i, word))


_FLIP = {}
def emoji_flip(ch):
    if ch not in _FLIP: _FLIP[ch] = emoji_sprite(ch).transpose(Image.FLIP_LEFT_RIGHT)
    return _FLIP[ch]


def paste_sprite(img, sp, x, y, size, alpha=1.0):
    if size < 4: return
    s = int(size * 170 / 120); sp = sp.resize((s, s), Image.BILINEAR)
    if alpha < 1: sp = sp.copy(); sp.putalpha(sp.split()[3].point(lambda v: int(v * alpha)))
    img.alpha_composite(sp, (int(x - s / 2), int(y - s / 2)))


def ship(img, x, y, right=True, size=72, alpha=1.0, ch="🚢"):
    if -80 < x < W + 80 and -80 < y < H + 80:
        paste_sprite(img, emoji_sprite(ch) if not right else emoji_flip(ch), x, y + math.sin(x * 0.05) * 2, size, alpha)


def along(pts, s):
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; L = sum(seg) * min(1, max(0, s)); acc = 0
    for (a, b), sl in zip(zip(pts, pts[1:]), seg):
        if acc + sl >= L:
            q = (L - acc) / max(sl, 1e-6); return a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q, b[0] >= a[0]
        acc += sl
    return pts[-1][0], pts[-1][1], True


SEA = [(50.2, 27.6), (51.8, 27.0), (53.5, 26.5), (55.0, 26.5), (55.9, 26.62), (56.35, 26.52), (56.62, 26.15), (57.1, 25.5), (58.2, 24.8), (60.5, 23.8)]
OMAN_SEA = [(56.5, 26.0), (56.7, 25.4), (56.75, 24.8), (57.6, 24.2), (59.5, 23.6)]


def traffic(img, cam, t, n=10, mode="flow", path=SEA, speed=0.018):
    pts = ipath(cam, path)
    for q in range(n):
        s = (q / n + (t * speed if mode == "flow" else 0) * (1 if q % 2 else -1)) % 1.0
        x, y, r = along(pts, s)
        off = 14 if q % 2 else -14
        if mode == "stuck":
            ship(img, x, y + off, True, 64, 0.85)
            d = ImageDraw.Draw(img); d.ellipse((x - 30, y + off - 30, x + 30, y + off + 30), outline=RED + (200,), width=4)
        else: ship(img, x, y + off, r if q % 2 else not r, 70)


def oil_flow(img, pts, t, color=(30, 30, 30), spacing=46, speed=120):
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]; L = sum(seg)
    if L < 10: return
    d = ImageDraw.Draw(img); s = (t * speed) % spacing
    while s < L:
        x, y, _ = along(pts, s / L)
        d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=color + (255,), outline=WHT + (255,), width=3); s += spacing


def mover(img, pts, t, t0, dur, ch, size=70, loop=False):
    if t < t0: return
    s = ((t - t0) / dur) % 1.0 if loop else ease((t - t0) / dur)
    x, y, r = along(pts, s); paste_sprite(img, emoji_flip(ch) if r else emoji_sprite(ch), x, y - 10, size)


def slam(img, txt, t, t0, y=H / 2 - 120, size=130, color=YEL, hold=2.2, sub=None):
    if t < t0 or t > t0 + hold: return
    k = (t - t0) / 0.15; s = 1.7 - 0.7 * ease(k) if k < 1 else 1.0
    a = 1.0 if t < t0 + hold - 0.3 else (t0 + hold - t) / 0.3
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = font(POPX, size * s)
    while f.getlength(txt) > W - 160: f = font(POPX, f.size * 0.9)
    text_stroke(d, (W / 2, y), txt, f, color, stroke=max(6, int(size * 0.08)))
    if sub: text_stroke(d, (W / 2, y + size * 0.85), sub, font(POPX, size * 0.4), WHT, stroke=6)
    if a < 1: lay.putalpha(lay.split()[3].point(lambda v: int(v * a)))
    img.alpha_composite(lay)


def epop(img, ch, x, y, t, t0, size=110, bob=True, hold=None):
    if t < t0 or (hold and t > t0 + hold): return
    k = pop((t - t0) / 0.3)
    paste_emoji(img, ch, x, y + (math.sin((t - t0) * 4) * 6 if bob else 0), size * k)


def flag_at(img, cam, ch, lon, lat, t, t0, size=90):
    x, y = cam.xy(lon, lat); epop(img, ch, x, y, t, t0, size)


def stamp(img, txt, t, t0, x=W / 2, y=H / 2, color=RED, size=120, ang=-12):
    if t < t0: return
    k = (t - t0) / 0.18; s = 2.0 - 1.0 * ease(k) if k < 1 else 1.0
    f = font(POPX, size * s); tw = f.getlength(txt)
    lay = Image.new("RGBA", (int(tw + 120), int(size * s * 1.8)), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((10, 10, lay.width - 10, lay.height - 10), 20, outline=color + (255,), width=int(12 * s))
    d.text((lay.width / 2, lay.height / 2), txt, font=f, fill=color + (255,), anchor="mm")
    lay = lay.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(lay, (int(x - lay.width / 2), int(y - lay.height / 2)))


def ev_safe(f):
    try: f()
    except KeyError: pass


SHAKES = []


def map_anim(img, cam, i, t, lt):
    def g(lon, lat): return cam.xy(lon, lat)
    w = lambda word: WT(i, word)
    if i == 0:
        traffic(img, cam, t, 14)
        epop(img, "🛢️", W * 0.78, H * 0.30, t, w("oil"), 130)
        slam(img, "1/5 OF THE WORLD'S OIL", t, w("fifth"), H * 0.78 - 60, 96, YEL, 3.0)
    elif i == 1:
        traffic(img, cam, t, 12, "flow" if t < w("shut") else "stuck")
        stamp(img, "ALMOST SHUT", t, w("shut"), W / 2, H / 2 + 160, RED, 110)
    elif i == 2:
        flag_at(img, cam, "🇦🇪", 54.3, 23.9, t, w("country"), 120)
        epop(img, "🏜️", W * 0.32, H * 0.62, t, w("desert"), 120)
        epop(img, "⛰️", W * 0.62, H * 0.40, t, w("mountains"), 120)
    elif i == 3:
        traffic(img, cam, t, 12)
        for word, ch, lo, la in (("Saudi", "🇸🇦", 47.0, 24.5), ("Iraq", "🇮🇶", 46.5, 31.6), ("Kuwait", "🇰🇼", 47.6, 29.4), ("Qatar", "🇶🇦", 51.2, 25.2), ("Emirates", "🇦🇪", 54.5, 23.8)):
            ev_safe(lambda: flag_at(img, cam, ch, lo, la, t, w(word), 100))
        hx, hy = g(56.4, 26.5); epop(img, "🍾", hx + 90, hy - 40, t, w("bottle"), 130)
    elif i == 4:
        traffic(img, cam, t, 8, path=SEA[3:8])
        a, b = g(56.42, 26.35), g(56.30, 26.84)
        k = ease((t - w("thirtythree")) / 0.8)
        if k > 0:
            d = ImageDraw.Draw(img); bx, by = lerp(a[0], b[0], k), lerp(a[1], b[1], k)
            d.line([a, (bx, by)], fill=YEL + (255,), width=8)
            for (x, y) in (a, (bx, by)): d.line([(x - 26, y), (x + 26, y)], fill=YEL + (255,), width=8)
            if k >= 1: badge(img, (a[0] + b[0]) / 2 + 300, (a[1] + b[1]) / 2, "~33 KM", (30, 30, 30), pop((t - w("thirtythree") - 0.8) / 0.3), "📏", 48)
    elif i == 5:
        for q, ln in enumerate(LANES):
            pts = ipath(cam, ln if q == 0 else ln[::-1])
            for n in range(4): x, y, r = along(pts, (n / 4 + t * 0.03) % 1.0); ship(img, x, y, r, 72)
        slam(img, "ONLY A FEW KM WIDE", t, w("few"), H * 0.80 - 60, 90, YEL, 2.6)
    elif i == 7:
        for r in ROUTES["asia"]:
            pts = smooth(ipath(cam, r))
            if t > SC[i] + 2.5:
                for n in range(2): x, y, rr = along(pts, (n / 2 + t * 0.08) % 1.0); ship(img, x, y, rr, 64)
        for word, ch, lo, la in (("China", "🇨🇳", 103, 34), ("India", "🇮🇳", 78, 21), ("Japan", "🇯🇵", 139, 37), ("Korea", "🇰🇷", 127.8, 36.3)):
            ev_safe(lambda: flag_at(img, cam, ch, lo, la, t, w(word), 100))
        ev_safe(lambda: epop(img, "❌", *g(10, 50), t, w("Europe"), 90))
    elif i == 9:
        traffic(img, cam, t, 10, "stuck")
        ev_safe(lambda: slam(img, "CEASEFIRE", t, w("ceasefire"), H * 0.25, 110, GRN, 1.4))
        ev_safe(lambda: slam(img, "FIGHTING AGAIN", t, w("fighting"), H * 0.25, 110, RED, 2.0))
        ev_safe(lambda: epop(img, "❓", W * 0.75, H * 0.45, t, w("agree"), 130))
    elif i == 11:
        traffic(img, cam, t, 8, path=SEA[2:8])
        k = ease((t - w("other")) / 1.0)
        if k > 0:
            p = [g(55.0, 25.6), g(55.9, 26.2), g(56.8, 25.4)]
            arrow(img, smooth(p), YEL, k, 16)
    elif i == 12:
        traffic(img, cam, t, 6, path=OMAN_SEA, speed=0.03)
        x, y = g(*P["fujairah"][:2]); epop(img, "⚓", x + 120, y + 40, t, w("Fujairah"), 100)
        slam(img, "ALREADY PAST THE STRAIT ✓" .replace(" ✓", ""), t, w("past"), H * 0.78 - 60, 90, GRN, 2.6)
    elif i == 13:
        hx, hy = g(56.3, 26.4); epop(img, "🚫", hx, hy, t, w("bottleneck"), 110)
        mover(img, ipath(cam, ROUTES["pipe"][0]), t, w("cargo"), 3.0, "📦", 80, loop=True)
    elif i == 14:
        mover(img, ipath(cam, ROUTES["crow"][0]), t, w("crow"), 2.2, "🐦", 90)
    elif i in (15, 17, 32, 34):
        for r in ROUTES["pipe2" if i == 17 else "pipe"]:
            if t > SC[i] + 2.2: oil_flow(img, ipath(cam, r), t)
        if i == 15: ev_safe(lambda: slam(img, "2012", t, w("2012"), H * 0.24, 140, YEL, 2.0))
        if i == 17:
            x, y = g(55.1, 24.45); ev_safe(lambda: epop(img, "🏗️", x, y - 70, t, w("built"), 120))
            ev_safe(lambda: slam(img, "START: 2027", t, w("expected"), H * 0.80 - 60, 96, YEL, 2.8))
        if i == 32:
            x, y = g(55.1, 24.4)
            ev_safe(lambda: epop(img, "⚠️", x, y - 80, t, w("weakness"), 130))
            ev_safe(lambda: epop(img, "🎯", x + 30, y + 10, t, w("missile"), 120))
        if i == 34:
            mover(img, ipath(cam, ROUTES["rail2"][0]), t, SC[i] + 2.0, 4.0, "🚆", 70, loop=True)
            ev_safe(lambda: slam(img, "PLAN B", t, w("insurance"), H * 0.80 - 70, 120, YEL, 3.0))
    elif i == 21:
        traffic(img, cam, t, 5, path=[(54.6, 25.3), (54.95, 25.05), (55.05, 24.98)], speed=0.04)
        ev_safe(lambda: slam(img, "#1 PORT IN THE MIDDLE EAST", t, w("biggest"), H * 0.78 - 60, 84, YEL, 2.6))
        x, y = g(*P["jebel"][:2]); ev_safe(lambda: epop(img, "🔒", x + 140, y - 90, t, w("behind"), 110))
    elif i == 22:
        a = g(*P["jebel"][:2])
        for q, key in enumerate(("fujairah", "khor")):
            b = g(*P[key][:2]); pts = [(a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s - math.sin(math.pi * s) * 160) for s in np.linspace(0, 1, 30)]
            ev_safe(lambda: mover(img, pts, t, w("move") + q * 0.4, 1.6, "📦", 80, loop=True))
    elif i == 23:
        flag_at(img, cam, "🇴🇲", 56.8, 22.0, t, w("Oman"), 110)
        for key, word in (("sohar", "Sohar"), ("duqm", "Duqm")):
            x, y = g(*P[key][:2]); ev_safe(lambda: epop(img, "⚓", x - 90, y + 30, t, w(word), 90))
    elif i in (25, 26):
        rpts = ipath(cam, ROUTES["rail" if i == 25 else "rail2"][0])
        if t > SC[i] + 2.0: mover(img, rpts if i == 25 else rpts[::-1], t, SC[i] + 2.0, 5.0, "🚆", 76, loop=True)
        if i == 26:
            x, y = g(*P["icad"][:2]); ev_safe(lambda: epop(img, "🏭", x + 170, y + 70, t, w("Industrial"), 110))
            ev_safe(lambda: slam(img, "~200 KM", t, w("two"), H * 0.80 - 60, 100, YEL, 2.4))
    elif i == 28:
        mover(img, ipath(cam, ROUTES["rail2"][0])[::-1], t, SC[i], 5.0, "🚆", 76, loop=True)
        epop(img, "🤐", W * 0.30, H * 0.30, t, w("not"), 130)
        ev_safe(lambda: epop(img, "🗺️", W * 0.70, H * 0.30, t, w("map"), 130))
    elif i == 29:
        for word, ch, dx, dy in (("tunnels", "🚇", -300, 220), ("bridges", "🌉", 0, 260), ("cuttings", "⛏️", 300, 220)):
            ev_safe(lambda: epop(img, ch, W / 2 + dx, H / 2 + dy, t, w(word), 120))
    elif i == 30:
        if t > SC[i] + 2.5: oil_flow(img, ipath(cam, ROUTES["saudi"][0])[::-1][::-1], t, speed=160, spacing=60)
        flag_at(img, cam, "🇸🇦", 44.5, 23.0, t, w("Saudi"), 110)
        flag_at(img, cam, "🇮🇷", 55.5, 30.0, t, w("Iran"), 110)
        x, y = g(*P["jask"][:2]); ev_safe(lambda: epop(img, "❓", x + 30, y + 110, t, w("helped"), 100))
    elif i == 35:
        traffic(img, cam, t, 10, "stuck")
        ev_safe(lambda: epop(img, "🚪", W * 0.75, H * 0.35, t, w("door"), 150))
        ev_safe(lambda: slam(img, "1/5 OF WORLD OIL", t, w("fifth"), H * 0.78 - 60, 100, YEL, 2.6))


CARD_ICONS = {10: ["📈", "🚫", "👷"], 31: ["💸", "🐢", "🎯"], 36: ["⛽", "🌾", "🚢"], 37: ["🚪", "👇"]}


def screen_anim(img, i, t, lt, on_clip=False):
    sc = S[i][1]; w = lambda word: WT(i, word)
    if sc["t"] == "card" and i in CARD_ICONS and not on_clip:
        n = len(sc["lines"]); y0 = H / 2 - (n - 1) * 110
        for q, ch in enumerate(CARD_ICONS[i]):
            k = pop((lt - 0.4 - q * 0.7) / 0.35)
            if k > 0:
                f = font(POPX, 110); tw = min(f.getlength(sc["lines"][q]), W - 160)
                paste_emoji(img, ch, W / 2 - tw / 2 - 110, y0 + q * 220 + math.sin(t * 3 + q) * 6, 110 * k)
                paste_emoji(img, ch, W / 2 + tw / 2 + 110, y0 + q * 220 + math.cos(t * 3 + q) * 6, 110 * k)
    if sc["t"] == "bar" and not on_clip:
        icons = ("🛢️", "🛢️") if i == 19 else ("🚢", "🚆")
        for q in range(2):
            k = ease((lt - 0.4 - q * 0.6) / 1.2)
            if k > 0.05:
                cx = W / 2 + (-330 if q == 0 else 330)
                epop(img, icons[q], cx, H - 230 + 140, t, SC[i] + 0.4 + q * 0.6, 90)
    if sc["t"] == "count" and not on_clip:
        if i == 8:
            ev_safe(lambda: stamp(img, "CLOSED", t, w("closed"), W * 0.78, H * 0.30, RED, 110))
        if i in (16, 18):
            v = sc["value"] * ease((lt - 0.3) / 1.8); n = int(round(v * 10))
            for q in range(n): paste_emoji(img, "🛢️", 230 + (q % 15) * 98, 170 + (q // 15) * 100, 80 * pop((lt - 0.3 - q * 0.05) / 0.25))
        if i == 24:
            n = int(20 * ease((lt - 0.3) / 1.8))
            for q in range(n): paste_emoji(img, "📦", 300 + (q % 10) * 132, 300 - (q // 10) * 112, 96)
        if i == 27:
            for q in range(3):
                x = lerp(-200, 560 + q * 400, ease((lt - 0.3 - q * 0.4) / 0.8)); paste_emoji(img, "🚆", x, 260, 150)
    if "clip" in sc:
        if i == 12: ev_safe(lambda: slam(img, "ALREADY PAST THE STRAIT", t, w("past"), H * 0.78 - 60, 90, GRN, 2.6))
        if i == 0: ev_safe(lambda: slam(img, "SO NARROW...", t, w("narrow"), H * 0.78 - 60, 100, WHT, 2.4))
        if i == 9:
            ev_safe(lambda: slam(img, "CEASEFIRE", t, w("ceasefire"), H * 0.25, 110, GRN, 1.4)); ev_safe(lambda: slam(img, "FIGHTING AGAIN", t, w("fighting"), H * 0.25, 110, RED, 2.0))
        if i == 35: ev_safe(lambda: epop(img, "🚪", W * 0.75, H * 0.35, t, w("door"), 150))
        if i == 20:
            for q, (word, ch) in enumerate((("food", "🍎"), ("medicine", "💊"), ("cars", "🚗"), ("machines", "⚙️"))):
                ev_safe(lambda: epop(img, ch, 420 + q * 360, H * 0.42, t, w(word), 140))
        if i == 3:
            for word, ch, x in (("Saudi", "🇸🇦", 360), ("Iraq", "🇮🇶", 660), ("Kuwait", "🇰🇼", 960), ("Qatar", "🇶🇦", 1260), ("Emirates", "🇦🇪", 1560)):
                ev_safe(lambda: epop(img, ch, x, 220, t, w(word), 110))
