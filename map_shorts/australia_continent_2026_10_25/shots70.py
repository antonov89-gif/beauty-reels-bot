"""Australia vs Greenland Short on engine70, beat structure from the DNA of GeoGlobeTales xGmyqt_Ild0 (principles, not content).
SEGMENT(t0, t1, mode)     camera mode on the timeline: globe | flat | merc
K(mode, t, a, b, c)       camera key: globe (lon, lat, R px) | flat (lon, lat, span deg) | merc (lon, lat, px per deg)
O(kind, t0, t1, ...)      overlay (see engine70.DRAW); every overlay start becomes a sound event"""
YEL, RED, CYAN, WHT, GRN, BLUE, ORANGE = (255, 214, 0), (229, 57, 53), (0, 229, 255), (255, 255, 255), (60, 220, 90), (30, 136, 229), (255, 152, 0)
AUS, GRL = (134.0, -25.5), (-41.0, 72.0)
STEEP, BYRON = (113.15, -26.15), (153.64, -28.64)


def build(SEGMENT, K, O, WT, ST, D, G):
    end = lambda i: ST[i] + D[i]                                                  # noqa: E731
    big = G["big"]
    C = G["COUNTRY"]
    aus = big(C["Australia"], 2)
    grl = big(C["Greenland"], 1)

    SEGMENT(0, 7.6, "globe")
    SEGMENT(7.6, 26.0, "merc")
    SEGMENT(26.0, 48.1, "globe")
    SEGMENT(48.1, 58.1, "merc")
    SEGMENT(58.1, 99, "globe")

    # L0 hook: fast push-in on the globe, AUSTRALIA pin, ISLAND struck out -> CONTINENT
    K("globe", 0.0, AUS[0], AUS[1], 560)
    K("globe", 1.3, AUS[0], AUS[1], 900)
    K("globe", 3.4, AUS[0] + 2, AUS[1], 960)
    O("fill", 0.3, 3.5, rings=aus, col=YEL, alpha=0.18, glow=YEL, border=WHT, bw=3)
    O("pin", WT(0, "Australia") - 0.1, 3.45, lon=AUS[0], lat=AUS[1] + 2, txt="AUSTRALIA", len=170)
    O("strike", WT(0, "island"), 3.45, xy=(540, 380), old="ISLAND", new="CONTINENT", ts=WT(0, "but") - 0.05, tr=WT(0, "continent"), size=130)
    O("fill", WT(0, "continent"), 3.5, rings=aus, col=YEL, alpha=0.5, glow=YEL, border=WHT, bw=4, pulse=True)

    # L1 Greenland: whip rotation of the globe to the far north
    K("globe", 3.5, AUS[0] + 2, AUS[1], 960)
    K("globe", 4.9, GRL[0], GRL[1] - 4, 760)
    K("globe", 7.5, GRL[0], GRL[1] - 2, 1050)
    O("fill", WT(1, "Greenland") + 0.4, 7.6, rings=grl, col=CYAN, alpha=0.45, glow=CYAN, border=WHT, bw=3)
    O("pin", WT(1, "Greenland") + 0.5, 7.6, lon=-41, lat=74, txt="GREENLAND", len=160, dot=CYAN)
    O("arrow", WT(1, "way"), 7.6, axy=(250, 380), blon=-50, blat=70, bend=-0.3)
    O("label", WT(1, "way") + 0.05, 7.6, xy=(270, 300), txt="WAY UP HERE", size=60)
    O("label", WT(1, "island"), 7.6, xy=(540, 1180), txt="ISLAND", size=110, col=WHT)
    O("badge", WT(1, "island") + 0.15, 7.6, xy=(820, 1180), icon="check", col=GRN, r=56)

    # L2 Mercator world: Greenland looks bigger than Australia
    O("flash", 7.6, 7.75)
    K("merc", 7.6, 48, 15, 3.9)
    K("merc", 9.2, 48, 15, 4.3)
    K("merc", 11.6, 48, 14, 4.35)
    O("pill", 7.75, 11.6, xy=(540, 230), txt="A COMMON WORLD MAP", size=46)
    O("fill", WT(2, "Greenland"), 18.6, rings=grl, col=CYAN, alpha=0.5, glow=CYAN, border=WHT, bw=3)
    O("label", WT(2, "Greenland") + 0.1, 11.6, lon=-38, lat=62, txt="GREENLAND", size=46)
    O("fill", WT(2, "Australia"), 22.5, rings=aus, col=YEL, alpha=0.45, glow=YEL, border=WHT, bw=3)
    O("label", WT(2, "Australia") + 0.05, 11.6, lon=132, lat=-12, txt="AUSTRALIA", size=46)
    O("label", WT(2, "bigger") - 0.05, 11.6, xy=(540, 1240), txt="LOOKS BIGGER?", size=96, col=YEL)
    O("badge", WT(2, "looks"), 11.6, xy=(230, 1000), icon="q", col=RED, r=52)

    # L3 true-size slide: Greenland moved along a great circle onto Australia, shrinking on the Mercator map
    K("merc", 11.7, 48, 14, 4.35)
    K("merc", 14.4, 134, -26, 13.5)
    O("truesize", 11.75, 18.6, src=GRL, dst=(137.0, -24.0), ta=WT(3, "slide"), tb=WT(3, "shrink") + 0.3, col=CYAN, alpha=0.55, glow=WHT,
      rings=grl)
    O("pill", WT(3, "slide"), 14.9, xy=(540, 230), txt="TRUE SIZE", size=54, col=YEL)
    O("label", WT(3, "shrink"), 14.9, xy=(540, 1240), txt="SHRINK!", size=100, col=CYAN)

    # L4 3.5x: big counter, area labels
    K("merc", 15.0, 134, -26, 13.5)
    K("merc", 18.8, 133, -26, 14.5, lin=True)
    O("counter", WT(4, "three") - 0.1, 22.5, xy=(540, 330), v0=1.0, v1=3.5, fmt="{:.1f}x BIGGER", dur=1.0, size=120)
    O("label", WT(4, "Australia"), 18.9, xy=(540, 1250), txt="AUSTRALIA ≈ 7.7 MILLION km²", size=58, col=YEL)
    O("label", WT(4, "half"), 18.9, xy=(540, 1330), txt="GREENLAND ≈ 2.2 MILLION km²", size=58, col=CYAN)

    # L5 width: zoom in, measurement arrow coast to coast
    K("merc", 18.9, 133, -26, 14.5)
    K("merc", 19.9, 133.4, -26.5, 22.0)
    K("merc", 22.6, 133.4, -26.5, 23.0, lin=True)
    O("measure", WT(5, "stretches"), 22.6, a=STEEP, b=BYRON, v0=0, v1=4000, fmt="~{:,.0f} km", sub="≈ 2,500 MILES", dur=1.3, size=80)
    O("badge", WT(5, "coast"), 22.6, xy=(540, 520), icon="ruler", col=BLUE, r=56, txt="COAST TO COAST")

    # L6 interrupt: pull-out, JUST SIZE? -> red X NOT QUITE
    K("merc", 22.7, 133.4, -26.5, 23.0)
    K("merc", 24.6, 125, -20, 9.0)
    K("merc", 26.0, 122, -18, 8.0, lin=True)
    O("label", WT(6, "just"), 26.0, xy=(540, 420), txt="JUST SIZE?", size=120, col=WHT)
    O("badge", WT(6, "not"), 26.0, xy=(540, 640), icon="x", col=RED, r=70)
    O("label", WT(6, "not") + 0.1, 26.0, xy=(540, 800), txt="NOT QUITE", size=90, col=RED)

    # L7 no official rule: globe with continents colour-coded
    K("globe", 26.0, 110, -5, 520)
    K("globe", 29.2, 80, 10, 560, lin=True)
    O("continents", WT(7, "no") + 0.2, 30.4)
    O("pill", WT(7, "official"), 29.1, xy=(540, 260), txt="NO OFFICIAL RULE", size=60, col=YEL)
    O("badge", WT(7, "rule"), 29.1, xy=(540, 1180), icon="book", col=RED, r=62, txt="WHAT IS A CONTINENT?")

    # L8 plates: rotate to Oceania, plate boundaries draw on
    K("globe", 29.2, 80, 10, 560)
    K("globe", 31.4, 140, -15, 620)
    K("globe", 32.9, 140, -18, 660, lin=True)
    O("plates", WT(8, "underneath") - 0.2, 36.5, draw=1.4)
    O("badge", WT(8, "tectonic"), 33.1, xy=(540, 260), icon="plate", col=ORANGE, r=62)
    O("label", WT(8, "tectonic") + 0.1, 33.1, xy=(540, 1200), txt="TECTONIC PLATES", size=92, col=ORANGE)

    # L9 Australian Plate
    K("globe", 32.9, 140, -18, 660)
    K("globe", 34.4, 132, -22, 860)
    K("globe", 36.8, 131, -22, 900, lin=True)
    O("fill", WT(9, "Australia"), 36.8, rings=aus, col=YEL, alpha=0.5, glow=YEL, border=WHT, bw=3, pulse=True)
    O("fill", WT(9, "own"), 36.8, plate="AU", col=ORANGE, alpha=0.32, glow=ORANGE, border=WHT, bw=3)
    O("pill", WT(9, "Australian") - 0.05, 36.8, xy=(540, 260), txt="AUSTRALIAN PLATE", size=60, col=ORANGE)

    # L10 North American Plate: whip to North America
    K("globe", 36.85, 131, -22, 900)
    K("globe", 38.1, -78, 55, 700)
    K("globe", 41.9, -80, 54, 740, lin=True)
    O("fill", WT(10, "Greenland") + 0.4, 42.2, rings=grl, col=CYAN, alpha=0.5, glow=CYAN, border=WHT, bw=3)
    O("fill", WT(10, "North"), 42.2, plate="NA", col=CYAN, alpha=0.25, glow=CYAN, border=WHT, bw=3)
    O("pill", WT(10, "American") - 0.05, 42.2, xy=(540, 260), txt="NORTH AMERICAN PLATE", size=56, col=CYAN)
    O("fill", WT(10, "Canada"), 42.2, name="Canada", col=(255, 64, 129), alpha=0.35, border=WHT, bw=2)
    O("pin", WT(10, "Canada"), 42.2, lon=-100, lat=58, txt="CANADA", len=120)
    O("fill", WT(10, "United"), 42.2, name="United States of America", col=GRN, alpha=0.35, border=WHT, bw=2)
    O("pin", WT(10, "United"), 42.2, lon=-98, lat=40, txt="USA", len=120)
    O("pin", WT(10, "Greenland") + 0.5, 42.2, lon=-41, lat=74, txt="GREENLAND", len=120, dot=CYAN)

    # L11 Greenland belongs to North America, largest island
    K("globe", 42.2, -80, 54, 740)
    K("globe", 43.8, -48, 66, 1150)
    K("globe", 48.0, -45, 68, 1250, lin=True)
    O("fill", WT(11, "Greenland"), 48.1, rings=grl, col=CYAN, alpha=0.5, glow=CYAN, border=WHT, bw=4, pulse=True)
    O("fill", WT(11, "Greenland"), 46.2, plate="NA", col=CYAN, alpha=0.18, glow=None, border=WHT, bw=2)
    O("label", WT(11, "belongs"), 46.0, xy=(540, 300), txt="PART OF NORTH AMERICA", size=70, col=CYAN)
    O("arrow", WT(11, "belongs") + 0.1, 46.0, axy=(540, 360), blon=-90, blat=55, bend=0.3)
    O("badge", WT(11, "largest"), 48.1, xy=(540, 300), icon="trophy", col=YEL, r=62, txt="WORLD'S LARGEST ISLAND")
    O("label", WT(11, "island"), 48.1, xy=(540, 1220), txt="≈ 2.2 MILLION km²", size=74, col=WHT)

    # L12 why so huge on maps? back to the Mercator world
    O("flash", 48.1, 48.25)
    K("merc", 48.1, -30, 62, 9.0)
    K("merc", 50.6, -35, 60, 7.2)
    K("merc", 51.7, -30, 55, 6.5, lin=True)
    O("fill", 48.15, 57.9, rings=grl, col=CYAN, alpha=0.5, glow=CYAN, border=WHT, bw=3, pulse=True)
    O("label", WT(12, "why"), 51.7, xy=(540, 380), txt="WHY SO HUGE?", size=120, col=YEL)
    O("badge", WT(12, "huge"), 51.7, xy=(540, 1200), icon="q", col=RED, r=64)

    # L13 Mercator projection, 1569, stretched near the poles
    K("merc", 51.7, -30, 55, 6.5)
    K("merc", 53.4, 10, 15, 4.6)
    K("merc", 58.0, 15, 12, 4.4, lin=True)
    O("graticule", WT(13, "Mercator"), 58.0)
    O("pill", WT(13, "Mercator"), 54.0, xy=(540, 230), txt="MERCATOR PROJECTION", size=56, col=YEL)
    O("badge", WT(13, "sailors"), 56.2, xy=(540, 1120), icon="compass", col=BLUE, r=60, txt="MADE FOR SAILORS")
    O("counter", WT(13, "1569") - 0.05, 56.2, xy=(540, 260), v0=1500, v1=1569, fmt="{:.0f}", dur=0.7, size=130)
    O("stretch", WT(13, "stretches"), 58.0, lon=-41, lat=72, len=260)
    O("stretch", WT(13, "stretches") + 0.2, 58.0, lon=40, lat=-75, len=220)
    O("label", WT(13, "poles") - 0.2, 58.0, xy=(540, 1180), txt="STRETCHED NEAR THE POLES", size=66, col=YEL)

    # L14 resolution + loop back to frame 0 (globe on Australia)
    K("globe", 58.1, GRL[0], GRL[1] - 3, 760)
    K("globe", 59.5, GRL[0], GRL[1] - 3, 820)
    K("globe", 60.6, AUS[0], AUS[1], 640)
    K("globe", 63.5, AUS[0], AUS[1], 580, lin=True)
    O("fill", 58.15, 60.0, rings=grl, col=CYAN, alpha=0.5, glow=CYAN, border=WHT, bw=3)
    O("pill", WT(14, "biggest"), 60.0, xy=(540, 300), txt="BIGGEST ISLAND", size=64, col=CYAN)
    O("fill", WT(14, "Australia"), 99, rings=aus, col=YEL, alpha=0.5, glow=YEL, border=WHT, bw=4, pulse=True)
    O("label", WT(14, "smallest"), 99, xy=(540, 380), txt="SMALLEST CONTINENT", size=96, col=YEL)
