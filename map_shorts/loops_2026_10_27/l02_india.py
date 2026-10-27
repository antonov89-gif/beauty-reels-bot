"""LOOP 02: India has more people than Europe + USA + Canada combined (UN WPP 2024, year 2024: India ~1.45B vs ~1.13B).
India outline = Natural Earth worldview IND (how India officially draws itself). 8 s, seamless loop."""
YEL, WHT, ORANGE, BLUE = (255, 214, 0), (255, 255, 255), (255, 152, 0), (30, 136, 229)
TOTAL = 8.0
CREDIT = "NASA Blue Marble (GIBS) · Natural Earth (India: IND view) · population 2024: UN World Population Prospects 2024"
ATL = (-36.0, 46.0, 520, 900)                        # Atlantic: North America + Europe on one hemisphere
IND = (80.0, 22.0, 700, 900)


def _europe(G):
    out = []
    for n, rings in G["COUNTRY"].items():
        if G["CONTINENT"].get(n) == "Europe":
            out += [r for r in rings if r[:, 1].mean() > 34 and r[:, 0].mean() > -32]      # drop overseas parts (French Guiana, Réunion ...)
    return out


def build(SEGMENT, K, O, G):
    SEGMENT(0, 99, "globe")
    K("globe", 0.0, *ATL)
    K("globe", 1.4, ATL[0] + 5, ATL[1], 545, ATL[3], lin=True)
    K("globe", 2.8, *IND)
    K("globe", 5.0, IND[0] + 3, IND[1], 730, IND[3], lin=True)
    K("globe", 6.5, *ATL)
    K("globe", TOTAL, *ATL)

    west = G["COUNTRY"]["United States of America"] + G["COUNTRY"]["Canada"] + _europe(G)
    O("fill", -1, 99, rings=west, col=(20, 110, 255), alpha=0.68, border=(200, 225, 255), bw=1)
    O("fill", 2.5, 6.6, rings=G["INDIA_IN"], col=ORANGE, alpha=0.7, glow=YEL, glow_w=22, border=WHT, bw=3, pulse=True)

    for t0, t1 in ((-1, 1.9), (7.0, 99)):                              # back on screen before the loop point
        O("label", t0, t1, lon=-100.0, lat=40.0, txt="USA", size=60, stroke=7)
        O("label", t0 + 0.12, t1, lon=-106.0, lat=58.0, txt="CANADA", size=56, stroke=7)
        O("label", t0 + 0.24, t1, lon=20.0, lat=50.0, txt="EUROPE", size=60, stroke=7)
    O("label", 3.0, 5.1, lon=78.5, lat=21.0, txt="INDIA", size=76, stroke=8, col=WHT)

    O("title", -1, 99, lines=[("INDIA HAS", ORANGE), ("MORE PEOPLE THAN", WHT), ("ALL THE BLUE", (90, 170, 255))], size=86, y=140, scrim=430)
    O("bars", -1, 99, y=1330, gap=150, x0=100, maxw=820, h=66, vmax=1.5, fmt="{:.2f} BILLION", vsize=44,
      items=[dict(txt="EUROPE + USA + CANADA", val=1.13, col=BLUE, k=[(0, 1.0)]),
             dict(txt="INDIA", val=1.45, col=ORANGE, k=[(2.9, 0.0), (4.4, 1.0), (6.8, 1.0), (6.85, 0.0)], ak=[(6.2, 1.0), (6.7, 0.0), (6.9, 0.0), (6.95, 1.0)])])
