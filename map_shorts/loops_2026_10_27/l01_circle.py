"""LOOP 01: more people live inside this circle than outside it. Circle = A. Rae (2022): 4,000 km around Yuxi, Yunnan, ~4.32B (55 %).
8 s, no narration; t=8.0 renders the same frame as t=0 (seamless loop)."""
YEL, WHT, ORANGE = (255, 214, 0), (255, 255, 255), (255, 152, 0)
TOTAL = 8.0
CREDIT = "NASA Blue Marble (GIBS) · Natural Earth · circle: A. Rae 2022, 4,000 km around Yuxi"
YUXI = (102.54, 24.35)
HOME = (100.5, 21.0, 760, 960)                       # lon, lat, R, globe centre y: circle + edge labels fit the width
OUT = (66.0, 20.0, 540, 930)                         # pulled out over the Arabian Sea: Africa + Europe visible = "outside"


def build(SEGMENT, K, O, G):
    SEGMENT(0, 99, "globe")
    K("globe", 0.0, *HOME)
    K("globe", 2.5, HOME[0], HOME[1], 800, HOME[3], lin=True)            # slow push while the labels pop
    K("globe", 3.7, *OUT)                                                # pull out: the rest of the world appears
    K("globe", 5.4, OUT[0] - 6, OUT[1], OUT[2], OUT[3], lin=True)        # slow drift while the two pills hold
    K("globe", 7.0, *HOME)
    K("globe", TOTAL, *HOME)

    O("circle", -1, 99, c=YUXI, r=4000, draw=[(0, 1.0)], dim=[(0, 0.62)], tint=[(0, 0.07)], w=10)
    O("title", -1, 99, lines=[("MORE PEOPLE LIVE", WHT), ("INSIDE THIS CIRCLE", YEL), ("THAN OUTSIDE IT", WHT)], size=86, y=150, scrim=420)

    for i, (txt, lon, lat) in enumerate([("CHINA", 104.0, 33.5), ("INDIA", 78.0, 18.0), ("INDONESIA", 112.0, -4.0), ("PAKISTAN", 70.0, 29.5),
                                         ("BANGLADESH", 91.0, 25.8), ("JAPAN", 138.5, 36.5), ("PHILIPPINES", 123.5, 10.5), ("VIETNAM", 105.0, 20.5)]):
        O("label", 0.25 + 0.25 * i, 3.1, lon=lon, lat=lat, txt=txt, size=50, stroke=7, col=WHT)

    O("pill", 3.6, 5.9, xy=(540, 1330), txt="INSIDE: MORE THAN HALF OF HUMANITY", size=54, col=YEL)
    O("pill", 3.9, 5.9, xy=(540, 1450), txt="OUTSIDE: EVERYONE ELSE", size=54, col=WHT)
    O("pill", 6.2, 7.75, xy=(540, 1420), txt="ARE YOU INSIDE?", size=60, col=YEL)
