"""Maldives Short (silent, 17 s, 124 BPM), engine67. Structure from the DNA report of rajography jTJ2UFF3B0I (principles only):
globe zoom + 3 s text hook -> hard cuts on the beat -> top-down finish -> loop to the hook.
Scene windows ST[i] sit on beats 0, 6, 10, 16, 22, 28 (beat = 60/124 s).  Camera/overlay API as in shots66."""
YEL, WHT, RED, CYAN = (255, 214, 0), (255, 255, 255), (255, 30, 39), (120, 225, 255)
OSWB = "assets/Oswald-Bold.ttf"
MALE, VELANA, MALDIVES = (73.508, 4.178), (73.5295, 4.192), (73.2, 3.2)


def build(short, K, O, GK, GLOBE, SN, FLASH, WT, ST, D, ISO=None, ISO_PINS=None):
    SN(0, 0.0)
    cut = lambda i: ST[i] - 0.05                                                    # noqa: E731

    # ---------------- S0 globe zoom onto the Maldives + text hook (3 s)
    GLOBE(0, cut(1))
    GK(0, 5, 22, 520)
    GK(cut(1), 73.2, 3.5, 2300)
    O("neon", 0.15, cut(1), scene="globe", x=540, y=300, txt="THE SEA IS RISING", size=78, track=5)
    O("neon", 1.35, cut(1), scene="globe", x=540, y=430, txt="THIS COUNTRY: 1.5 M HIGH", size=80, track=4)
    O("ring", 1.5, cut(1), scene="globe", lon=73.2, lat=3.5, r=34)

    # ---------------- S1 whole archipelago, slow push toward Male
    K(cut(1), 73.3, 3.2, 4.2, cut=True)
    K(cut(2), 73.45, 4.2, 2.0)
    O("banner", ST[1], cut(2), pill="MALDIVES", name="~1,190 ISLANDS")
    O("ring", ST[1] + 0.9, cut(2), lon=73.51, lat=4.18, r=34)
    FLASH.append(ST[2] - 0.12)

    # ---------------- S2 Male: the capital on one island (push-in)
    K(cut(2), 73.512, 4.192, 0.024, cut=True)
    K(cut(3) - 0.05, 73.510, 4.176, 0.0115)
    O("label", ST[2] + 0.05, cut(3), x=540, y=300, txt="CAPITAL ON ONE ISLAND", font=OSWB, size=76, col=WHT, shake=True)
    O("pin", ST[2] + 0.5, cut(3), lon=MALE[0], lat=MALE[1], txt="MALÉ", len=330, size=96)

    # ---------------- S3 the airport island, pan along the runway (top-down)
    K(cut(3), 73.529, 4.2025, 0.014, cut=True)
    K(cut(4) - 0.05, 73.529, 4.184, 0.014, lin=True)
    O("label", ST[3] + 0.05, cut(4), x=540, y=300, txt="THE AIRPORT HAS ITS OWN ISLAND", font=OSWB, size=70, col=YEL, shake=True)
    O("pin", ST[3] + 0.3, ST[3] + 2.0, lon=VELANA[0], lat=VELANA[1], txt="VELANA AIRPORT", len=260, size=70)

    # ---------------- S4 the number: average height vs a person
    K(cut(4), 73.3, 3.2, 4.2, cut=True)
    K(cut(5) - 0.05, 73.3, 3.2, 3.0)
    O("hudcard", ST[4] + 0.05, cut(5), x=540, y=520, title="AVERAGE HEIGHT", rows=[
        ("MALDIVES, ABOVE SEA", "1.5 M", 0.88, CYAN), ("ADULT PERSON", "~1.7 M", 1.0, YEL)])
    O("counter", ST[4] + 0.1, cut(5), x=540, y=1100, v0=0, v1=1.5, fmt="{:.1f} M ABOVE SEA", dur=1.1, size=88, col=CYAN)
    O("stamp", ST[4] + 1.5, cut(5), x=540, y=1330, txt="LOWEST-LYING COUNTRY", col=RED, size=80, angle=-4)
    FLASH.append(ST[4] - 0.12)

    # ---------------- S5 pull-out to the globe, question, loop to the hook
    GLOBE(cut(5), 1e9)
    GK(cut(5), 73.2, 3.5, 2300)
    GK(ST[5] + D[5] - 0.1, 40, 18, 520)
    O("label", ST[5] + 0.7, 1e9, scene="globe", x=540, y=1350, txt="WOULD YOU LIVE HERE?", font=OSWB, size=86, col=WHT, shake=True)
    O("ring", ST[5] + 0.1, 1e9, scene="globe", lon=73.2, lat=3.5, r=34)
    FLASH.append(ST[5] - 0.12)
    return None
