"""LOOP 03: Indonesia is wider than the USA. Indonesia ~5,120 km east-west (Wikipedia, Geography of Indonesia); contiguous USA
greatest coast-to-coast distance ~4,500 km (Wikipedia, Contiguous United States: 2,802 mi / 4,509 km). True-size overlay: the real
Indonesia outline is moved on the sphere with north kept up (no Mercator distortion). 8 s, seamless loop."""
YEL, WHT, ORANGE, BLUE = (255, 214, 0), (255, 255, 255), (255, 152, 0), (30, 136, 229)
TOTAL = 8.0
CREDIT = "NASA Blue Marble (GIBS) · Natural Earth · true-size overlay, same scale"
SRC, DST = (118.0, -2.5), (263.0, 37.0)              # Indonesia centre -> centre of the lower 48 (lon unwrapped: east across the Pacific)
US = (263.0, 37.0, 1150, 860)
MID = (190.0, 22.0, 600, 860)                        # pulled out over the Pacific during the slide
ID = (118.0, -1.0, 980, 860)
K_BAR = [(2.8, 1.0), (2.85, 0.0), (7.0, 0.0), (7.7, 1.0)]       # full -> (invisible reset) -> grows back before the loop point
A_BAR = [(2.3, 1.0), (2.75, 0.0), (6.95, 0.0), (7.0, 1.0)]      # fades out at full value


def build(SEGMENT, K, O, G):
    SEGMENT(0, 99, "globe")
    K("globe", 0.0, *US)
    K("globe", 2.4, US[0], US[1], 1110, US[3], lin=True)
    K("globe", 3.5, *MID)
    K("globe", 4.5, *ID)
    K("globe", 5.5, ID[0], ID[1], 1010, ID[3], lin=True)
    K("globe", 6.5, *MID)
    K("globe", 7.4, *US)
    K("globe", TOTAL, *US)

    lower48 = [r for r in G["COUNTRY"]["United States of America"] if 24 < r[:, 1].mean() < 50 and -126 < r[:, 0].mean() < -66]
    O("fill", -1, 99, rings=lower48, col=BLUE, alpha=0.45, border=WHT, bw=3)
    O("truesize", -1, 99, name="Indonesia", src=SRC, dst=DST, north=True, col=ORANGE, alpha=0.75, glow=YEL, ghost=True,
      legs=[(-99, -98, 1.0), (2.5, 4.5, -1.0), (5.6, 7.4, 1.0)])

    O("title", -1, 99, lines=[("INDONESIA IS WIDER", ORANGE), ("THAN THE USA", WHT)], size=96, y=150, scrim=430)
    O("label", -1, 99, xy=(540, 352), txt="(WITHOUT ALASKA & HAWAII)", size=42, stroke=6, col=WHT)     # claim = the 48 contiguous states
    O("pill", 4.3, 5.7, xy=(540, 1330), txt="SAME SHAPE · SAME SIZE · REAL PLACE", size=52, col=YEL)
    O("bars", -1, 99, y=1330, gap=150, x0=100, maxw=820, h=66, vmax=5600, fmt="{:,.0f} KM", vsize=44,
      items=[dict(txt="USA · COAST TO COAST", val=4500, col=BLUE, k=K_BAR, ak=A_BAR),
             dict(txt="INDONESIA · EAST TO WEST", val=5120, col=ORANGE, k=K_BAR, ak=A_BAR)])
