"""Walk It #1 on engine83. Route = 7 segments drawn in sync with the voice; the camera follows the walker head.
Waypoints are an approximate Pan-American route (credited on screen as 'route approximate')."""
YEL, RED, CYAN, WHT, GRN, BLUE, ORANGE = (255, 214, 0), (229, 57, 53), (0, 229, 255), (255, 255, 255), (60, 220, 90), (30, 136, 229), (255, 152, 0)

WP = [(-148.34, 70.25), (-147.72, 64.84), (-135.05, 60.72), (-120.24, 55.76), (-113.49, 53.55),       # 0 Prudhoe Bay .. 4 Edmonton
      (-114.07, 51.05), (-111.30, 47.50), (-104.99, 39.74), (-106.65, 35.08), (-106.49, 31.76),         # 5 Calgary .. 9 El Paso
      (-106.08, 28.63), (-99.13, 19.43), (-96.72, 17.06), (-90.51, 14.63), (-89.19, 13.69),             # 10 Chihuahua .. 14 San Salvador
      (-87.19, 14.07), (-86.24, 12.11), (-84.08, 9.93), (-79.52, 8.98), (-77.69, 8.16),                 # 15 Tegucigalpa .. 19 Yaviza
      (-76.73, 8.09), (-75.58, 6.24), (-76.53, 3.45), (-78.47, -0.18), (-77.04, -12.05),                # 20 Turbo .. 24 Lima
      (-71.54, -16.41), (-70.31, -18.48), (-70.40, -23.65), (-70.67, -33.45), (-72.94, -41.47),         # 25 Arequipa .. 29 Puerto Montt
      (-69.22, -51.62), (-68.30, -54.80)]                                                               # 30 Rio Gallegos, 31 Ushuaia
PB, YAV, TUR, USH = WP[0], WP[19], WP[20], WP[31]


def build(SEGMENT, K, O, WT, ST, D, G):
    end = lambda i: ST[i] + D[i]                                                      # noqa: E731
    TOT = end(11) + 0.9
    seg = lambda i0, i1, ta, tb, **kw: O("route", ta, 1e9, pts=WP[i0:i1 + 1], ta=ta, tb=tb, **kw)  # noqa: E731

    SEGMENT(0, ST[2], "globe")
    SEGMENT(ST[2], ST[10], "flat")
    SEGMENT(ST[10], 99, "globe")

    # L0 hook: the whole Americas on the globe, walker at the top, end pin at the bottom
    K("globe", 0.0, -92, 8, 700)
    K("globe", ST[1], -92, 8, 760, lin=True)
    O("badge", -0.5, ST[2], lon=PB[0], lat=PB[1], icon="walker", col=ORANGE, r=46)
    O("badge", -0.5, ST[2], lon=USH[0], lat=USH[1], icon="flag", col=GRN, r=40)
    O("label", -0.5, ST[1], xy=(540, 130), txt="CAN YOU WALK IT?", size=88, col=YEL)

    # L1 scale: the highway previewed as a thin white line + km counter
    K("globe", ST[1], -92, 8, 820)
    K("globe", ST[2], -95, 10, 900, lin=True)
    O("route", ST[1] + 0.2, ST[2], pts=WP, ta=ST[1] + 0.2, tb=end(1) - 0.3, col=WHT, w=6, head=False)
    O("pill", WT(1, "Pan-American"), ST[2], xy=(540, 130), txt="PAN-AMERICAN HIGHWAY", size=54, col=YEL)
    O("counter", WT(1, "thirty") - 0.1, ST[2], xy=(540, 1240), v0=0, v1=30000, fmt="≈ {:,.0f} km", dur=1.0, size=110)

    # L2 Prudhoe Bay, Arctic Ocean
    O("flash", ST[2], ST[2] + 0.12)
    K("flat", ST[2], -148.5, 69.0, 4.0)
    K("flat", ST[3], -146.0, 66.5, 6.0)
    O("pin", WT(2, "Prudhoe"), ST[3] + 0.3, lon=PB[0], lat=PB[1], txt="PRUDHOE BAY", len=160)
    O("badge", WT(2, "Arctic"), ST[3], xy=(540, 360), icon="snow", col=CYAN, r=60, txt="ARCTIC OCEAN")
    O("pill", ST[2] + 0.1, ST[3], xy=(540, 220), txt="START · ALASKA", size=52)
    seg(0, 4, WT(2, "Arctic"), ST[4] - 0.2)                                              # Alaska + Canada

    # L3 Canada + USA
    K("flat", ST[3] + 0.6, -128.0, 58.0, 9.0)
    K("flat", ST[4], -110.0, 44.0, 12.0)
    O("label", WT(3, "Canada"), WT(3, "United") + 0.4, xy=(540, 300), txt="CANADA", size=96, col=WHT)
    O("label", WT(3, "United"), ST[4], xy=(540, 300), txt="USA", size=110, col=WHT)
    seg(4, 9, ST[4] - 0.2, ST[4] + 0.6)                                                  # USA

    # L4 Mexico + Central America
    K("flat", ST[4] + 0.6, -101.0, 24.0, 10.0)
    K("flat", ST[5] - 0.2, -84.0, 12.0, 7.0)
    O("label", WT(4, "Mexico"), WT(4, "Central") - 0.1, xy=(540, 300), txt="MEXICO", size=104, col=WHT)
    O("label", WT(4, "Central"), ST[5], xy=(540, 300), txt="CENTRAL AMERICA", size=88, col=WHT)
    O("badge", WT(4, "Central") + 0.2, ST[5], xy=(540, 470), icon="sun", col=ORANGE, r=52)
    seg(9, 18, ST[4] + 0.6, ST[5] - 0.1)

    # L5 the road just stops (Panama)
    K("flat", ST[5] + 0.4, -79.0, 8.6, 2.6)
    K("flat", ST[6], -78.2, 8.4, 1.9)
    O("pill", WT(5, "Panama"), ST[6], xy=(540, 220), txt="PANAMA", size=56)
    seg(18, 19, WT(5, "Panama"), WT(5, "stops") - 0.1, head_end=True, head_until=ST[7] + 0.2)
    O("badge", WT(5, "stops"), ST[6] + 1.2, lon=YAV[0], lat=YAV[1] + 0.25, icon="x", col=RED, r=56)
    O("label", WT(5, "stops") + 0.05, ST[6], xy=(540, 360), txt="ROAD ENDS", size=110, col=RED)

    # L6 Darien Gap
    K("flat", ST[6] + 0.8, -77.25, 8.15, 1.4)
    K("flat", ST[7], -77.2, 8.1, 1.3, lin=True)
    O("pill", WT(6, "Darién"), ST[8], xy=(540, 220), txt="DARIÉN GAP", size=64, col=RED)
    O("measure", WT(6, "hundred") - 0.2, ST[7] - 0.1, a=YAV, b=TUR, v0=0, v1=100, fmt="≈ {:.0f} km", dur=0.8, size=78)
    O("badge", WT(6, "jungle"), ST[7], xy=(240, 1130), icon="jungle", col=GRN, r=54, txt="JUNGLE")
    O("badge", WT(6, "swamp"), ST[7], xy=(540, 1130), icon="ice", col=BLUE, r=54, txt="SWAMP")
    O("badge", WT(6, "rivers"), ST[7], xy=(840, 1130), icon="ice", col=CYAN, r=54, txt="RIVERS")
    O("label", WT(6, "no"), ST[7], xy=(540, 380), txt="NO ROAD AT ALL", size=96, col=WHT)

    # L7 crossing on foot: red dashed walk across the gap, heat + armed gangs
    seg(19, 20, ST[7] + 0.2, end(7) - 0.2, col=RED, hcol=RED, step=0.05)
    O("counter", WT(7, "days") - 0.1, ST[8], xy=(540, 360), v0=1, v1=4, fmt="DAY {:.0f}", dur=2.6, size=110, col=WHT)
    O("badge", WT(7, "mud"), ST[8], xy=(240, 1130), icon="jungle", col=(121, 85, 72), r=54, txt="MUD")
    O("badge", WT(7, "heat"), ST[8], xy=(540, 1130), icon="sun", col=ORANGE, r=54, txt="HEAT")
    O("badge", WT(7, "armed"), ST[8], xy=(840, 1130), icon="skull", col=RED, r=54, txt="ARMED GANGS")

    # L8 Colombia + the Andes
    K("flat", ST[8] + 0.3, -76.5, 5.0, 4.5)
    K("flat", WT(8, "Ecuador"), -77.5, -3.0, 9.0)
    K("flat", WT(8, "Peru"), -75.0, -13.0, 11.0)
    K("flat", ST[9], -71.0, -30.0, 13.0)
    O("pill", WT(8, "Colombia"), WT(8, "Andes"), xy=(540, 220), txt="COLOMBIA", size=56)
    O("badge", WT(8, "Andes"), ST[9], xy=(540, 380), icon="mountain", col=(141, 110, 99), r=62, txt="THE ANDES")
    O("label", WT(8, "Ecuador"), WT(8, "Peru"), xy=(540, 1180), txt="ECUADOR", size=88)
    O("label", WT(8, "Peru"), WT(8, "Chile"), xy=(540, 1180), txt="PERU", size=96)
    O("label", WT(8, "Chile"), ST[9], xy=(540, 1180), txt="CHILE", size=96)
    seg(20, 28, ST[8] + 0.3, ST[9] - 0.1)

    # L9 Ushuaia
    K("flat", ST[9] + 0.6, -70.0, -46.0, 9.0)
    K("flat", ST[10] - 0.2, -68.4, -54.6, 3.2)
    seg(28, 31, ST[9] + 0.2, WT(9, "Ushuaia") + 0.2, head_end=True)
    O("pin", WT(9, "Ushuaia"), ST[10], lon=USH[0], lat=USH[1], txt="USHUAIA", len=170, dot=GRN)
    O("badge", WT(9, "Ushuaia") + 0.15, ST[10], xy=(540, 250), icon="flag", col=GRN, r=62)
    O("label", WT(9, "end"), ST[10], xy=(540, 420), txt="THE END OF THE WORLD", size=86, col=YEL)

    # L10 George Meegan: the whole route on the globe + 2,425 days
    O("flash", ST[10], ST[10] + 0.12)
    K("globe", ST[10], -80, -5, 760)
    K("globe", ST[11], -88, 6, 800, lin=True)
    O("badge", WT(10, "George"), ST[11], xy=(540, 330), icon="walker", col=ORANGE, r=60, txt="GEORGE MEEGAN")
    O("label", WT(10, "other"), ST[11], xy=(540, 1180), txt="SOUTH → NORTH · 1977–1983", size=66, col=WHT)
    O("counter", WT(10, "seven") - 0.3, ST[11], xy=(540, 520), v0=0, v1=2425, fmt="{:,.0f} DAYS", dur=1.0, size=96)

    # L11 question + loop back to the frame-0 framing
    K("globe", ST[11] + 0.3, -92, 8, 700)
    K("globe", TOT, -92, 8, 700)
    O("label", ST[11], TOT + 1, xy=(540, 130), txt="WOULD YOU TRY?", size=88, col=YEL)
    O("badge", ST[11] + 0.1, TOT + 1, lon=PB[0], lat=PB[1], icon="walker", col=ORANGE, r=46)
