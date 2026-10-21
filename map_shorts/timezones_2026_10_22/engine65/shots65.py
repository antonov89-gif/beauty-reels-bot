"""Time zones Short (France 12 vs Russia 11), engine65. Structure from the DNA report of XpYfmHoPEAs (principles only):
question hook -> obvious answer -> 'that's wrong' -> one absurd retracted line (Monaco) -> mechanism + number -> answer at the end, loop to the question.
K(t, lon, lat, span, cut)   flat-map camera key;  GK(t, lon, lat, R) globe camera key;  GLOBE(t0, t1) marks a globe scene
O(kind, t0, t1, ..., scene='flat'|'globe'|'both')"""
YEL, WHT, RED, CYAN = (255, 214, 0), (255, 255, 255), (255, 30, 39), (120, 225, 255)
GOLD = (255, 229, 0)
BLUE = (90, 150, 255)
GREEN = (30, 200, 110)
OSWB = "assets/Oswald-Bold.ttf"

# overseas France: (lon, lat, label) used for rings and pins
GUADELOUPE, MARTINIQUE, GUIANA, SPM = (-61.55, 16.25), (-61.0, 14.65), (-53.0, 4.0), (-56.3, 46.8)
REUNION, MAYOTTE, KERGUELEN, CROZET = (55.5, -21.1), (45.15, -12.8), (69.5, -49.3), (51.8, -46.4)
TAHITI, MARQUESAS, CLIPPERTON, NCAL, WALLIS, ADELIE = (-149.4, -17.6), (-139.5, -9.0), (-109.2, 10.3), (165.5, -21.3), (-176.2, -13.3), (140.0, -66.7)
MONACO, PARIS = (7.4228, 43.7384), (2.35, 48.86)
TERR = [GUADELOUPE, MARTINIQUE, GUIANA, SPM, REUNION, MAYOTTE, KERGUELEN, CROZET, TAHITI, MARQUESAS, CLIPPERTON, NCAL, WALLIS, ADELIE]
FR_NAMES = ["France", "French Polynesia", "New Caledonia", "Wallis and Futuna", "Saint Pierre and Miquelon", "French Southern and Antarctic Lands"]


def build(short, K, O, GK, GLOBE, SN, FLASH, WT, ST, D):
    end = lambda i: ST[i] + D[i]                                                   # noqa: E731
    SN(0, 0.0)

    # ---------------- globe A (0 - Monaco joke): question hook, Russia, USA, "wrong"
    GLOBE(0, ST[5] - 0.05)
    GK(0, 5, 42, 560)
    GK(ST[1] - 0.05, 30, 40, 600)
    GK(ST[2] - 0.05, 60, 52, 640)
    GK(WT(2, "Kamchatka") + 0.2, 140, 56, 700)
    GK(ST[3] - 0.05, 165, 50, 650)
    GK(ST[3] + 1.7, 262, 40, 690)
    GK(ST[4] - 0.05, 262, 40, 690)
    GK(ST[5] - 0.1, 215, 45, 620)

    # L0 hook
    O("banner", -1, ST[5] - 0.05, scene="both", pill="QUIZ", name="MOST TIME ZONES")
    O("label", -1.3, ST[1] - 0.05, scene="both", x=540, y=1000, txt="WHICH COUNTRY?", font=OSWB, size=112, col=WHT, shake=True)
    O("label", 0.5, ST[1] - 0.05, scene="both", x=540, y=1130, txt="MOST TIME ZONES", font=OSWB, size=78, col=YEL)

    # L1 "Easy... or maybe not"
    O("stamp", WT(1, "Easy") - 0.1, WT(1, "maybe") - 0.1, scene="both", x=540, y=560, txt="EASY", col=GREEN, size=130, angle=-4)
    O("stamp", WT(1, "maybe") - 0.1, ST[2] - 0.05, scene="both", x=540, y=560, txt="NOT SO FAST", col=RED, size=110, angle=-4)
    FLASH.append(WT(1, "maybe") - 0.12)

    # L2 Russia, 11 zones, Kaliningrad to Kamchatka
    O("fill", ST[2] - 0.02, ST[4] - 0.2, scene="globe", name="Russia", col=GOLD, alpha=0.22, glow=GOLD, border=GOLD, bw=5)
    O("fill", ST[4] - 0.2, ST[5] - 0.05, scene="globe", name="Russia", col=GOLD, alpha=0.22, glow=GOLD, border=GOLD, bw=5)
    O("chips", WT(2, "eleven") - 0.3, ST[3] - 0.05, scene="globe", x=540, y=1210, cols=6, size=44, rh=84, per=0.17,
      items=[("UTC", RED)] + [(f"+{n}", YEL) for n in range(2, 13)])
    O("counter", WT(2, "eleven") - 0.05, ST[3] - 0.05, scene="globe", x=540, y=1000, v0=0, v1=11, fmt="{:.0f} TIME ZONES", dur=2.4, size=100, col=WHT)
    O("pin", WT(2, "Kaliningrad") - 0.1, ST[3] - 0.05, scene="globe", lon=20.5, lat=54.7, txt="Kaliningrad", len=170, size=76)
    O("pin", WT(2, "Kamchatka") - 0.1, ST[3] - 0.05, scene="globe", lon=158.0, lat=56.0, txt="Kamchatka", len=170, size=76)

    # L3 USA
    O("fill", ST[3] + 0.9, ST[5] - 0.05, scene="globe", name="United States of America", col=BLUE, alpha=0.3, glow=BLUE, border=BLUE, bw=5)
    O("counter", WT(3, "eleven") - 0.05, ST[4] - 0.05, scene="globe", x=540, y=1000, v0=0, v1=11, fmt="{:.0f} TIME ZONES", dur=1.4, size=100, col=BLUE)
    O("pin", WT(3, "Alaska") - 0.1, ST[4] - 0.05, scene="globe", lon=-150.0, lat=64.0, txt="Alaska", len=150, size=70)
    O("pin", WT(3, "Hawaii") - 0.1, ST[4] - 0.05, scene="globe", lon=-157.0, lat=20.5, txt="Hawaii", len=150, size=70)

    # L4 "Russia, or the United States. But that's wrong."
    O("hudcard", WT(4, "winner") - 0.1, WT(4, "wrong") - 0.1, scene="globe", x=540, y=830, title="TIME ZONES", rows=[
        ("RUSSIA", "11", 1.0, YEL), ("USA", "11", 1.0, BLUE)])
    O("stamp", WT(4, "wrong") - 0.1, ST[5] - 0.05, scene="globe", x=540, y=560, txt="WRONG", col=RED, size=140, angle=-5)
    FLASH.append(WT(4, "wrong") - 0.12)

    # ---------------- flat B: Monaco joke (cut to the Riviera, zoom into the smallest country)
    K(ST[5] - 0.05, 7.3, 44.7, 2.2, cut=True)
    K(WT(5, "Monaco") - 0.4, 7.35, 44.0, 0.9)
    K(WT(5, "joking") - 0.9, MONACO[0], MONACO[1], 0.11)
    O("banner", ST[5] - 0.02, ST[6] - 0.05, pill="MONACO", name="~2 KM²")
    O("pin", WT(5, "Monaco") - 0.05, ST[6] - 0.05, lon=MONACO[0], lat=MONACO[1], txt="Monaco", len=200, size=84)
    O("ring", WT(5, "Monaco") - 0.05, ST[6] - 0.05, lon=MONACO[0], lat=MONACO[1], r=40)
    O("label", WT(5, "one") - 0.05, WT(5, "joking") - 0.1, x=540, y=700, txt="1 TIME ZONE", font=OSWB, size=96, col=WHT, shake=True)
    O("stamp", WT(5, "joking") - 0.1, ST[6] - 0.05, x=540, y=560, txt="I'M JOKING", col=RED, size=120, angle=-5)
    FLASH.append(WT(5, "joking") - 0.12)

    # L6 "The real winner is France."
    K(ST[6] - 0.05, 2.5, 46.6, 9.0, cut=True)
    K(end(6) + 0.2, 2.5, 46.6, 8.2)
    O("fill", ST[6] - 0.02, ST[8] - 0.05, name="France", col=GOLD, alpha=0.88, glow=GOLD, border=WHT, bw=4)
    O("stamp", WT(6, "France") - 0.1, ST[7] - 0.05, x=540, y=560, txt="FRANCE", col=YEL, size=140, angle=-4)

    # L7 mainland: one time, same as Berlin
    K(ST[7] - 0.05, 2.5, 46.6, 8.2)
    K(end(7) + 0.2, 3.0, 46.6, 6.6)
    O("banner", ST[7] - 0.02, ST[8] - 0.05, pill="MAINLAND", name="UTC+1")
    O("pin", WT(7, "Mainland") - 0.05, ST[8] - 0.05, lon=PARIS[0], lat=PARIS[1], txt="Paris", len=190, size=78)
    O("chips", WT(7, "single") - 0.1, ST[8] - 0.05, x=540, y=1250, cols=2, size=50, rh=90, per=0.5, gap=26,
      items=[("PARIS 12:00", YEL), ("BERLIN 12:00", WHT)])
    O("label", WT(7, "same") - 0.05, ST[8] - 0.05, x=540, y=730, txt="SAME CLOCK AS BERLIN", font=OSWB, size=70, col=WHT, shake=True)

    # ---------------- globe C: territories, regions, clocks, answer
    GLOBE(ST[8] - 0.05, 1e9)
    GK(ST[8] - 0.05, -30, 18, 560)
    GK(ST[9] - 0.05, -55, 12, 640)
    GK(WT(9, "Caribbean") - 0.25, -62, 15, 980)
    GK(WT(9, "South") - 0.25, -54, 4, 980)
    GK(WT(9, "Indian") - 0.25, 55, -18, 980)
    GK(WT(9, "Pacific") - 0.25, 210, -17, 980)
    GK(WT(9, "Pacific") + 0.75, 210, -17, 980)
    GK(WT(9, "Antarctica") - 0.25, 140, -62, 960)
    GK(ST[10] - 0.05, 160, -45, 560)
    GK(ST[10] + 1.2, 220, -10, 620)
    GK(ST[11] - 0.05, 197, -15, 820)
    GK(end(11) + 0.2, 197, -15, 760)
    GK(ST[12] - 0.05, 250, 5, 580)
    GK(WT(12, "thirteen") - 0.3, 380, -5, 580)
    GK(ST[13] - 0.05, 460, -10, 560)
    GK(ST[14] - 0.15, 362.5, 40, 640)
    GK(end(14) + 0.3, 365, 42, 560)
    for n in FR_NAMES:
        O("fill", ST[8] - 0.05, 1e9, scene="globe", name=n, col=GOLD, alpha=0.85, glow=GOLD, border=GOLD, bw=4)
    O("banner", ST[8] - 0.05, 1e9, scene="both", pill="FRANCE", name="OVERSEAS")
    for i, (lo, la) in enumerate(TERR):
        O("ring", WT(8, "owns") - 0.1 + 0.18 * i, 1e9, scene="globe", lon=lo, lat=la, r=22)

    # L8 / L9 regions
    regs = [("Caribbean", "CARIBBEAN", "Guadeloupe · Martinique", GUADELOUPE), ("South", "SOUTH AMERICA", "French Guiana", GUIANA),
            ("Indian", "INDIAN OCEAN", "Réunion · Mayotte", REUNION), ("Pacific", "PACIFIC", "Tahiti", TAHITI),
            ("Antarctica", "ANTARCTICA", "Adélie Land (claim)", ADELIE)]
    for i, (w, title, place, ll) in enumerate(regs):
        t0 = WT(9, w) - 0.1
        t1 = (WT(9, regs[i + 1][0]) - 0.1) if i + 1 < len(regs) else ST[10] - 0.05
        O("label", t0, t1, scene="globe", x=540, y=330, txt=title, font=OSWB, size=92, col=YEL, shake=(i == 0))
        O("pin", t0 + 0.15, t1, scene="globe", lon=ll[0], lat=ll[1], txt=place, len=170, size=62)

    # L10 own clock
    O("chips", ST[10] + 0.05, ST[11] - 0.05, scene="globe", x=540, y=340, cols=1, size=48, rh=82, per=0.32, items=[
        ("TAHITI  −10:00", YEL), ("GUADELOUPE  −4:00", YEL), ("PARIS  +1:00", WHT), ("RÉUNION  +4:00", YEL), ("NEW CALEDONIA  +11:00", YEL)])

    # L11 French Polynesia (10 h behind) to Wallis and Futuna (12 h ahead)
    O("pin", WT(11, "Polynesia") - 0.1, ST[12] - 0.05, scene="globe", lon=TAHITI[0], lat=TAHITI[1], txt="French Polynesia", len=160, size=64)
    O("pin", WT(11, "Wallis") - 0.1, ST[12] - 0.05, scene="globe", lon=WALLIS[0], lat=WALLIS[1], txt="Wallis & Futuna", len=330, size=64)
    O("label", WT(11, "ten") - 0.15, WT(11, "Wallis") - 0.2, scene="globe", x=540, y=620, txt="10 HOURS BEHIND GREENWICH", font=OSWB, size=64, col=CYAN, shake=True)
    O("label", WT(11, "twelve") - 0.15, ST[12] - 0.05, scene="globe", x=540, y=620, txt="12 HOURS AHEAD", font=OSWB, size=76, col=YEL, shake=True)

    # L12 the count
    O("counter", WT(12, "twelve") - 0.1, WT(12, "thirteen") - 0.15, scene="globe", x=540, y=1000, v0=0, v1=12, fmt="{:.0f} TIME ZONES", dur=1.3, size=104, col=GOLD, shake=True)
    O("counter", WT(12, "thirteen") - 0.15, ST[13] - 0.05, scene="globe", x=540, y=1000, v0=12, v1=13, fmt="{:.0f} TIME ZONES", dur=0.5, size=104, col=GOLD, shake=True)
    O("label", WT(12, "Antarctic") - 0.1, ST[13] - 0.05, scene="globe", x=540, y=1130, txt="+ ANTARCTIC CLAIM", font=OSWB, size=70, col=WHT)

    # L13 one capital, clocks around the planet
    O("label", WT(13, "capital") - 0.15, WT(13, "clocks") - 0.2, scene="globe", x=540, y=600, txt="CAPITAL: ONE ZONE", font=OSWB, size=84, col=WHT, shake=True)
    O("label", WT(13, "clocks") - 0.2, ST[14] - 0.05, scene="globe", x=540, y=600, txt="CLOCKS ON EVERY OCEAN", font=OSWB, size=76, col=YEL, shake=True)

    # L14 answer, loop to the question
    O("label", ST[14] - 0.05, WT(14, "France") - 0.1, scene="globe", x=540, y=1000, txt="MOST TIME ZONES?", font=OSWB, size=96, col=WHT, shake=True)
    O("stamp", WT(14, "France") - 0.1, 1e9, scene="globe", x=540, y=560, txt="FRANCE", col=YEL, size=150, angle=-4)
    O("counter", WT(14, "France") + 0.1, 1e9, scene="globe", x=540, y=1000, v0=0, v1=12, fmt="{:.0f} TIME ZONES", dur=1.0, size=104, col=GOLD)
    return None
