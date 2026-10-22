"""Turkey Short, beat-for-beat remake of the MapTrail 'Spain' reference (engine63).
K(t, lon, lat, span, cut=False)  camera keyframe (span = half-height in degrees of latitude); eased, span interpolated exponentially
O(kind, t0, t1, ...)             overlay on the global timeline (see engine63.DRAW)
TILT(t0, t1, ...)                tilted world card segment"""
# colours sampled from the reference frame (thumbnail = frame at ~0:39): violet, magenta, cyan, lime
PURPLE, CYAN, YEL, WHT = (112, 72, 255), (0, 229, 255), (255, 230, 0), (255, 255, 255)
SKY, MAGENTA, LIME, TEAL_F, AMBER, PINK = (40, 196, 240), (214, 32, 228), (200, 240, 0), (0, 214, 170), (255, 170, 0), (255, 64, 129)
SEA_T = (38, 198, 218)

TR = (35.2, 39.2)                        # Turkey framing centre
FACE = (34.4, 38.9)
SH_L, SH_R = (27.0, 40.95), (43.8, 39.8)    # shoulders just inside the west and east borders (arms stay on screen)
IST = (28.98, 41.01)
NARROW = ((29.0568, 41.0874), (29.0658, 41.0874))   # Rumelihisari, measured on Esri imagery
OTTOMAN = ["Turkey", "Greece", "Bulgaria", "North Macedonia", "Albania", "Kosovo", "Republic of Serbia", "Bosnia and Herzegovina",
           "Montenegro", "Hungary", "Cyprus", "Northern Cyprus", "Syria", "Lebanon", "Israel", "Palestine", "Jordan", "Iraq", "Egypt"]


def build(short, K, O, TILT, WT, ST, D):
    end = lambda i: ST[i] + D[i]                                               # noqa: E731

    # L0 flag fill + pin, slow push-in
    K(0, TR[0], TR[1] + 0.3, 21.0)
    K(ST[1] + 0.2, TR[0], TR[1], 20.5)
    O("flagfill", -1, ST[1] + 0.25, name="Turkey", code="TR")
    O("pin", 0.05, ST[1] + 0.1, lon=33.0, lat=39.6, txt="Turkey", len=230)

    # L1 purple glow + angry flexing character (the country is the body)
    O("fill", ST[1], WT(8, "Istanbul") - 0.3, name="Turkey", col=PURPLE, alpha=0.7)
    O("char", WT(1, "actually") - 0.1, ST[2] + 0.05, mood="angry", arms=True, lon=FACE[0], lat=FACE[1], left=SH_L, right=SH_R, s=44, arm_s=72)
    K(ST[2] - 0.05, TR[0], TR[1], 20.0)

    # myth hook (v2): first spoken words as text, then the 3% of Turkey that lies in Europe (East Thrace) lights up
    O("label", 0.15, end(0) + 0.15, x=540, y=470, txt="NOT IN EUROPE?", size=76, col=YEL)
    O("fill", WT(1, "three") - 0.1, ST[2] + 0.1, name="Thrace10", col=(0, 184, 212), alpha=0.8, glow=YEL)
    O("counter", WT(1, "three") - 0.05, ST[2] + 0.1, x=540, y=470, v0=0, v1=3, fmt="{:.0f}% IN EUROPE", dur=0.8, size=84)

    # L2 tilted world card: cyan arcs from Istanbul
    TILT(ST[2] - 0.05, ST[3] - 0.05, cam=(22.0, 36.0, 16.0), origin=IST, s0=2.6, s1=1.0, roll=-5,
         arcs=[((19.04, 47.50), WT(2, "once")), ((31.24, 30.04), WT(2, "ruled")), ((44.37, 33.31), WT(2, "huge")),
               ((3.06, 36.75), WT(2, "part")), ((39.83, 21.42), WT(2, "world") - 0.1)])

    # L3 back to Turkey: happy character looking around, slow push
    K(ST[3] - 0.05, TR[0], TR[1], 17.5, cut=True)
    K(end(3) + 0.3, TR[0], TR[1] - 0.2, 15.5)
    O("char", ST[3] + 0.05, end(3) + 0.35, mood="happy", lon=FACE[0], lat=FACE[1], s=48)

    # L4-L6 neighbours: one continuous camera, pans west -> east -> south
    K(WT(4, "west") - 0.15, TR[0], TR[1] - 0.2, 15.5)
    K(WT(4, "Bulgaria") + 0.3, 27.0, 40.6, 9.5)
    O("fill", WT(4, "Greece") - 0.1, WT(8, "Istanbul") - 0.3, name="Greece", col=SKY, alpha=0.7)
    O("pin", WT(4, "Greece"), ST[5] + 0.3, lon=22.6, lat=39.9, txt="Greece", len=150)
    O("fill", WT(4, "Bulgaria") - 0.1, WT(8, "Istanbul") - 0.3, name="Bulgaria", col=MAGENTA, alpha=0.75)
    O("pin", WT(4, "Bulgaria"), ST[5] + 0.3, lon=25.3, lat=42.6, txt="Bulgaria", len=150)

    K(WT(5, "east") - 0.1, 27.0, 40.6, 9.5)
    K(WT(5, "Azerbaijan") + 0.2, 41.6, 40.3, 9.5)
    for word, name, col, lon, lat, ln in (("Georgia", "Georgia", LIME, 43.5, 42.0, 120), ("Armenia", "Armenia", AMBER, 44.9, 40.25, 200),
                                         ("Azerbaijan", "Azerbaijan", TEAL_F, 45.4, 39.3, 110), ("Iran", "Iran", PINK, 45.2, 37.4, 110)):
        O("fill", WT(5, word) - 0.1, WT(8, "Istanbul") - 0.3, name=name, col=col, alpha=0.72)
        O("pin", WT(5, word), ST[6] + 0.4, lon=lon, lat=lat, txt=name, len=ln)

    K(WT(6, "south") - 0.1, 41.6, 40.3, 9.5)
    K(WT(6, "Syria") + 0.2, 39.8, 36.9, 9.5)
    O("fill", WT(6, "Iraq") - 0.1, WT(8, "Istanbul") - 0.3, name="Iraq", col=SKY, alpha=0.7)
    O("pin", WT(6, "Iraq"), ST[7] + 0.2, lon=43.6, lat=34.6, txt="Iraq", len=150)
    O("fill", WT(6, "Syria") - 0.1, WT(8, "Istanbul") - 0.3, name="Syria", col=MAGENTA, alpha=0.72)
    O("pin", WT(6, "Syria"), ST[7] + 0.2, lon=38.6, lat=35.3, txt="Syria", len=150)

    # L7 seas: turquoise fills + curved names, pan north then south-west
    K(WT(7, "north") - 0.1, 39.8, 36.9, 9.5)
    K(WT(7, "Black") + 0.3, 34.5, 42.4, 8.5)
    O("fill", WT(7, "Black") - 0.1, ST[8] + 0.6, sea="Black Sea", col=SEA_T, alpha=0.38, glow=None, bw=2, flat=True)
    O("curved", WT(7, "Black"), ST[8] + 0.6, lon=34.3, lat=43.25, txt="Black Sea", radius=1100, angle=-6, size=64)
    K(WT(7, "south") - 0.1, 34.5, 42.4, 8.5)
    K(WT(7, "Mediterranean") + 0.3, 31.5, 35.2, 8.5)
    O("fill", WT(7, "Mediterranean") - 0.1, ST[8] + 0.6, sea="Mediterranean Sea", col=SEA_T, alpha=0.38, glow=None, bw=2, flat=True)
    O("curved", WT(7, "Mediterranean"), ST[8] + 0.6, lon=31.0, lat=34.4, txt="Mediterranean Sea", radius=1000, angle=8, size=58)

    # L8 surprise: high-speed continuous push into the Bosphorus, ruler counting up
    K(WT(8, "surprise") - 0.2, 31.5, 35.2, 8.5)
    K(WT(8, "Istanbul") + 0.1, 29.02, 41.06, 0.9)
    K(WT(8, "Asia") + 0.1, 29.061, 41.0874, 0.022)
    K(end(8) + 0.25, 29.0613, 41.0874, 0.019)
    O("pin", WT(8, "Istanbul") - 0.2, WT(8, "Asia") - 0.3, lon=IST[0], lat=IST[1], txt="Istanbul", len=160)
    O("label", WT(8, "Asia") - 0.15, end(8) + 0.4, lon=29.0505, lat=41.0925, txt="EUROPE", size=70, col=(120, 230, 255))
    O("label", WT(8, "Asia") + 0.05, end(8) + 0.4, lon=29.0722, lat=41.0828, txt="ASIA", size=70, col=YEL)
    O("ruler", WT(8, "only") - 0.1, end(8) + 0.4, a=NARROW[0], b=NARROW[1], v0=100, v1=700, fmt="~{:.0f} m", dur=1.1, size=72)

    # L9 zoom out over Istanbul: European side and Asian side light up (reference: Morocco reveal)
    K(ST[9] - 0.05, 29.061, 41.0874, 0.019)
    K(WT(9, "continents") + 0.2, 29.05, 41.1, 0.75)
    K(end(9) + 0.25, 29.05, 41.1, 0.7)
    O("fill", WT(9, "cross") - 0.2, ST[10] + 0.5, name="Thrace10", col=(0, 184, 212), alpha=0.6)
    O("fill", WT(9, "two") - 0.1, ST[10] + 0.5, name="Anatolia10", col=LIME, alpha=0.62, glow=YEL)
    O("pin", WT(9, "cross"), ST[10] + 0.3, lon=28.75, lat=41.25, txt="Europe", len=170)
    O("pin", WT(9, "continents") - 0.1, ST[10] + 0.3, lon=29.4, lat=40.95, txt="Asia", len=170)

    # L10 size: zoom back out, yellow outline, area counter at the centre
    K(ST[10] - 0.05, 29.05, 41.1, 0.7)
    K(WT(10, "massive") + 0.2, TR[0], TR[1], 12.5)
    K(end(10) + 0.3, TR[0], TR[1], 12.0)
    O("fill", WT(10, "massive") - 0.3, WT(12, "Ararat") - 0.3, name="Turkey", col=PURPLE, alpha=0.7, glow=YEL, border=YEL, bw=4)
    O("pin", WT(10, "Turkey") - 0.1, end(10) + 0.3, lon=34.6, lat=38.6, txt="Turkey", len=210, sub=(51074, 302535, "{:,.0f} sq. miles", 1.4), sub_t=WT(10, "more") - 0.1)

    # L11 mountains: orange elevation texture, pulsing glow
    K(WT(11, "Turkey") - 0.2, TR[0], TR[1], 12.0)
    K(end(11) + 0.2, 38.0, 39.3, 10.5)
    O("elev", WT(11, "mountainous") - 0.4, WT(12, "Ararat") - 0.3, name="Turkey", min=1500)

    # L12 Ararat: continuous zoom to the peak, height counter
    K(ST[12] - 0.05, 38.0, 39.3, 10.5)
    K(WT(12, "Ararat") + 0.3, 44.298, 39.70, 0.32)
    K(end(12) + 0.3, 44.298, 39.70, 0.26)
    O("pin", WT(12, "Ararat") - 0.1, end(12) + 0.3, lon=44.2983, lat=39.7016, txt="Mount Ararat", len=200)
    O("counter", WT(12, "almost") - 0.1, end(12) + 0.3, x=540, y=470, v0=0, v1=16854, fmt="{:,.0f} ft", dur=1.2, size=90)
    O("label", WT(12, "Noah's") - 0.1, end(12) + 0.3, x=540, y=1160, txt="NOAH'S ARK? (LEGEND)", size=50, col=YEL)

    # L13 tilted world card: Ottoman Empire in red, beams to three continents
    TILT(ST[13] - 0.05, ST[14] - 0.05, cam=(22.0, 36.0, 16.0), origin=IST, s0=2.6, s1=1.0, roll=5,
         red=OTTOMAN, red_t=WT(13, "Ottoman") - 0.1, note="SIMPLIFIED",
         arcs=[((19.04, 47.50), WT(13, "ruled")), ((31.24, 30.04), WT(13, "parts")), ((44.37, 33.31), WT(13, "three"))],
         labels=[("Europe", 12.0, 49.0, WT(13, "three"), (120, 230, 255)), ("Asia", 50.0, 41.0, WT(13, "continents") - 0.15, YEL),
                 ("Africa", 14.0, 26.0, WT(13, "continents"), (255, 160, 60))])
    O("counter", WT(13, "six") - 0.2, ST[14] - 0.05, x=540, y=1500, v0=0, v1=600, fmt="{:.0f}+ YEARS", dur=0.9, size=84)

    # L14 speech bubbles multiplying along a pan from Istanbul to western Europe
    K(ST[14] - 0.05, 24.9, 42.3, 7.0, cut=True)
    K(end(14) + 0.3, 23.9, 43.2, 7.0, lin=True)
    for word, txt, lon, lat in (("coffee", "COFFEE?", 28.97, 41.01), ("yogurt", "YOGURT!", 26.1, 44.43), ("kiosk", "KIOSK!", 23.32, 42.70),
                                ("came", "TULIP!", 20.46, 44.82), ("Turkish", "CAVIAR!", 19.04, 47.50)):
        O("bubble", WT(14, word) - 0.05, end(14) + 0.4, lon=lon, lat=lat, txt=txt, size=80)

    # L15 loop: fly back to Turkey, happy face, flag fades in for the loop to frame 0
    K(ST[15] - 0.05, 23.9, 43.2, 7.0)
    K(end(15) + 0.2, TR[0], TR[1] + 0.3, 21.0)
    O("fill", ST[15] + 0.4, end(15) + 0.4, name="Turkey", col=PURPLE, alpha=0.7)
    O("char", WT(15, "bridge") - 0.1, end(15) - 0.15, mood="happy", lon=FACE[0], lat=FACE[1], s=40)
    O("flagfill", end(15) - 0.15, end(15) + 2, name="Turkey", code="TR")
