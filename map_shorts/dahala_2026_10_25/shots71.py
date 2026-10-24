"""Dahala Khagrabari Short on engine71 (text + music + SFX, no voice). Beat map from the DNA of Younes Zarou HBTl6U1zefo (principles only):
quiet build -> riser -> shock at 3.4 s (nested outlines pop in, flash + hit) -> answer ("REAL") in the video -> loop back to the opening globe.
K(mode, t, ...) camera keys: globe (lon, lat, R px) | flat (lon, lat, span deg); O(kind, t0, t1, ...) overlays; WT unused (no voice)."""
import math
import numpy as np

YEL, RED, CYAN, WHT, GRN, ORANGE, BLUE = (255, 214, 0), (229, 57, 53), (0, 229, 255), (255, 255, 255), (60, 220, 90), (255, 152, 0), (30, 136, 229)
LON, LAT = 88.76196, 26.14974


def blob(cx, cy, r, seed, wob=0.12, n=90):
    """Irregular closed outline around (cx, cy), radius r deg (lat), simplified drawing of an enclave."""
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6.28, 4)
    out = []
    for i in range(n + 1):
        a = 2 * math.pi * i / n
        k = 1 + wob * (math.sin(2 * a + ph[0]) * 0.6 + math.sin(3 * a + ph[1]) * 0.5 + math.sin(5 * a + ph[2]) * 0.3)
        out.append((cx + r * k * math.cos(a) / math.cos(math.radians(cy)) * 1.15, cy + r * k * math.sin(a)))
    return np.array(out)


def build(SEGMENT, K, O, WT, ST, D, G):
    # outlines (simplified, not surveyed): outer Bangladesh, India enclave, Bangladesh enclave
    RB = [blob(LON, LAT, 0.16, 1, 0.10)]
    RI = [blob(LON, LAT, 0.046, 2, 0.14)]
    RE = [blob(LON, LAT, 0.019, 3, 0.15)]
    box_lat, box_lon = 0.00075, 0.00084                                   # true size of the plot, 84 m x 75 m, centred on the Wikipedia coordinates
    RDS = [blob(LON, LAT, 0.0065, 4, 0.16)]                                  # schematic nested outline (not to scale)
    RD = [np.array([(LON - box_lon / 2, LAT - box_lat / 2), (LON + box_lon / 2, LAT - box_lat / 2), (LON + box_lon / 2, LAT + box_lat / 2),
                    (LON - box_lon / 2, LAT + box_lat / 2), (LON - box_lon / 2, LAT - box_lat / 2)])]

    SEGMENT(0, 1.6, "globe")
    SEGMENT(1.6, 14.6, "flat")
    SEGMENT(14.6, 99, "globe")

    # 0-1.6 s: globe push-in to South Asia, quiet
    K("globe", 0.0, 80, 24, 560)
    K("globe", 1.55, LON, LAT, 1700)
    O("label", 0.25, 3.35, xy=(540, 330), txt="THIS LOOKS LIKE A", size=62, col=WHT)
    O("label", 0.45, 3.35, xy=(540, 440), txt="PHOTOSHOP ERROR", size=92, col=YEL)

    # 1.6-3.4 s: tension zoom through the border region (silence, riser)
    K("flat", 1.6, LON, LAT, 3.0)
    K("flat", 3.4, LON, LAT, 0.34)

    # 3.4 s: SHOCK, nested outlines pop in, one every 0.7 s, camera keeps pushing in
    O("flash", 3.4, 3.55)
    K("flat", 5.9, LON, LAT, 0.115)
    O("fill", 3.5, 7.6, rings=RB, col=GRN, alpha=0.20, glow=GRN, border=WHT, bw=4)
    O("pill", 3.6, 7.6, xy=(540, 1560), txt="BANGLADESH", size=54, col=GRN, edge=GRN)
    O("fill", 4.2, 7.6, rings=RI, col=ORANGE, alpha=0.34, glow=ORANGE, border=WHT, bw=4)
    O("pill", 4.3, 7.6, xy=(540, 1450), txt="INSIDE IT: INDIA", size=54, col=ORANGE, edge=ORANGE)
    O("fill", 4.9, 7.6, rings=RE, col=GRN, alpha=0.4, glow=GRN, border=WHT, bw=4)
    O("pill", 5.0, 7.6, xy=(540, 1340), txt="INSIDE THAT: BANGLADESH", size=54, col=GRN, edge=GRN)
    O("fill", 5.6, 7.6, rings=RDS, col=ORANGE, alpha=0.6, glow=YEL, border=YEL, bw=5, pulse=True)
    O("fill", 7.5, 12.9, rings=RD, col=ORANGE, alpha=0.55, glow=YEL, border=YEL, bw=5, pulse=True)
    O("pill", 5.7, 7.6, xy=(540, 1230), txt="INSIDE THAT: INDIA", size=54, col=YEL, edge=YEL)
    O("pill", 3.7, 7.6, xy=(540, 230), txt="SIMPLIFIED OUTLINES, NOT SURVEYED", size=34, col=WHT)

    # 5.9-9.6 s: the real plot, true size marker, area counter
    K("flat", 7.6, LON, LAT, 0.0042)
    K("flat", 9.7, LON, LAT, 0.0040)
    O("pin", 7.6, 12.9, lon=LON, lat=LAT + box_lat / 2, txt="DAHALA KHAGRABARI", len=210, dot=YEL, size=58)
    O("counter", 7.7, 9.8, xy=(540, 560), v0=0, v1=7000, fmt="≈ {:,.0f} m²", dur=1.1, size=100, col=YEL)
    O("pill", 7.7, 12.9, xy=(540, 1560), txt="TRUE SIZE · APPROXIMATE LOCATION", size=34, col=WHT)

    # 9.7-12.9 s: the answer
    O("label", 10.0, 12.9, xy=(540, 330), txt="ONLY ONE IN THE WORLD", size=66, col=WHT)
    O("label", 10.8, 12.9, xy=(540, 440), txt="UNTIL 2015", size=96, col=YEL)
    O("badge", 11.5, 12.9, xy=(540, 840), icon="trophy", col=ORANGE, r=64, txt="3RD-ORDER ENCLAVE")

    # 13.1-14 s: REAL
    O("label", 13.15, 14.6, xy=(540, 380), txt="REAL.", size=170, col=GRN)
    O("badge", 13.3, 14.6, xy=(540, 640), icon="check", col=GRN, r=80)
    O("label", 13.45, 14.6, xy=(540, 900), txt="HANDED TO BANGLADESH", size=58, col=WHT)
    O("label", 13.7, 14.6, xy=(540, 1000), txt="1 AUGUST 2015", size=74, col=YEL)

    # 14-17 s: fast pull-out to the opening globe (loop)
    K("globe", 14.6, LON, LAT, 1700)
    K("globe", 16.5, 80, 24, 560)
    O("flash", 14.6, 14.72)
