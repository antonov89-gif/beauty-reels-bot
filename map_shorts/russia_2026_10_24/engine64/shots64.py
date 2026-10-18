"""Russia Short, beat-for-beat in the system of OneCriticalMoment q6L_j157rGo (engine64).
K(t, lon, lat, span, cut)   flat-map camera key (span = half-height in degrees of latitude)
GK(t, lon, lat, R)          globe camera key;  GLOBE(t0, t1) marks a globe scene
SN(t, f)                    season: 0 summer ... 1 deep winter;  FLASH list: white impact flashes
O(kind, t0, t1, ..., scene='flat'|'globe'|'both')"""
YEL, WHT, RED, CYAN = (255, 214, 0), (255, 255, 255), (255, 30, 39), (120, 225, 255)
GOLD = (255, 229, 0)
OSWB = "assets/Oswald-Bold.ttf"

PATH = [(57.2, 58.4), (60.0, 58.3), (63.0, 57.4), (65.53, 57.15), (68.27, 58.2), (76.5, 58.4), (84.95, 56.49), (92.87, 56.01),
        (99.5, 56.6), (105.7, 56.8), (111.0, 58.9), (114.9, 60.7), (129.73, 62.03), (136.0, 61.0), (140.0, 60.0), (143.0, 59.4)]
TYUMEN, TOBOLSK, QASHLIQ, TOMSK, KRAS, YAKUTSK, OKHOTSK = (65.53, 57.15), (68.27, 58.2), (68.42, 58.2), (84.95, 56.49), (92.87, 56.01), (129.73, 62.03), (143.0, 59.4)


def build(short, K, O, GK, GLOBE, SN, FLASH, WT, ST, D):
    end = lambda i: ST[i] + D[i]                                                   # noqa: E731

    # ---------------- L0-L2: globe hook (frame 0 = loop frame): banner, gold Russia, 58-year arrow, boats
    GLOBE(0, ST[3] - 0.02)
    GK(0, 95, 56, 560)
    GK(ST[3] - 0.05, 100, 58, 660)
    SN(0, 0.0)
    O("banner", -1, ST[3] - 0.02, scene="both", pill="RUSSIA", name="11 TIME ZONES")
    O("fill", -1, ST[3] - 0.02, scene="globe", name="Russia", col=GOLD, alpha=0.2, glow=GOLD, border=GOLD, bw=5)
    O("arrow", WT(1, "Crossing") - 0.1, ST[3] - 0.02, scene="globe", pts=PATH, dur=2.4, w=12, keephead=True)
    O("counter", WT(1, "fifty-eight") - 0.1, ST[3] - 0.02, scene="both", x=540, y=1000, v0=0, v1=58, fmt="{:.0f} YEARS", dur=1.1, size=118, col=YEL, shake=True)
    O("units", WT(2, "Cossacks") - 0.2, ST[3] - 0.02, scene="globe", pts=PATH, dur=2.6, n=4, size=62)
    O("label", WT(2, "Cossacks") + 0.1, ST[3] - 0.02, scene="both", x=540, y=1130, txt="A FEW HUNDRED COSSACKS", font=OSWB, size=58, col=WHT)

    # ---------------- L3: 1581 Yermak, Ural Mountains (hard cut to the flat map, beat hit)
    K(ST[3] - 0.05, 59.3, 58.4, 3.6, cut=True)
    K(end(3) + 0.2, 61.2, 58.3, 3.0)
    O("banner", ST[3] - 0.02, WT(4, "sledges") - 0.05, pill=(1500, 1581), name="YERMAK", icon="sun", roll=0.75)
    O("label", ST[3] + 0.3, end(3) + 0.2, lon=59.0, lat=59.5, txt="URAL MOUNTAINS", size=56, col=WHT)
    O("arrow", ST[3] + 0.1, end(3) + 0.5, pts=PATH[:5], dur=2.6, w=14)
    O("units", ST[3] + 0.1, end(3) + 0.5, pts=PATH[:5], dur=2.6, n=4, size=66)

    # ---------------- L4: rivers are the roads; boats in summer, sledges over ice (snow arrives)
    K(ST[4] - 0.05, 63.8, 57.9, 3.4)
    K(WT(4, "summer") + 0.4, 66.5, 57.9, 3.8)
    K(end(4) + 0.2, 69.0, 58.1, 3.0)
    O("rivers", ST[4], ST[5] - 0.1, names=["Chusovaya", "Tura", "Tobol", "Irtysh"], w=6, step=1)
    O("label", WT(4, "rivers") - 0.1, WT(4, "sledges") - 0.2, x=540, y=640, txt="RIVERS = ROADS", font=OSWB, size=76, col=CYAN, shake=True)
    SN(WT(4, "sledges") - 0.5, 0.0)
    SN(WT(4, "sledges") + 0.5, 1.0)
    FLASH.append(WT(4, "sledges") - 0.1)
    O("banner", WT(4, "sledges") - 0.05, ST[5] - 0.05, pill="1581", name="YERMAK", icon="snow")

    # ---------------- L5: 1582 Qashliq, fire and stamp
    K(ST[5] - 0.05, 68.4, 58.2, 1.1, cut=True)
    K(end(5) + 0.2, 68.4, 58.2, 0.7)
    SN(ST[5], 0.6)
    O("banner", ST[5] - 0.02, ST[6] - 0.05, pill=(1581, 1582), name="QASHLIQ", icon="snow")
    O("pin", WT(5, "Qashliq") - 0.1, end(5) + 0.1, lon=QASHLIQ[0], lat=QASHLIQ[1], txt="Qashliq", len=190, size=84)
    O("fire", WT(5, "took") - 0.05, end(5) + 0.3, lon=QASHLIQ[0] - 0.01, lat=QASHLIQ[1] - 0.03, h=150)
    O("stamp", WT(5, "took") + 0.1, end(5) + 0.1, x=540, y=560, txt="CAPITAL TAKEN", size=104, angle=-5)

    # ---------------- L6: forts, banner year odometer, camera pan east
    SN(ST[6], 1.0)
    K(ST[6] - 0.05, 66.2, 57.7, 2.4, cut=True)
    K(WT(6, "Tyumen") + 0.3, TYUMEN[0], TYUMEN[1], 1.7)
    K(WT(6, "Tobolsk") + 0.3, TOBOLSK[0], TOBOLSK[1], 1.7)
    K(WT(6, "Tomsk") - 0.2, 77.0, 57.5, 5.0)
    K(WT(6, "Tomsk") + 0.9, TOMSK[0], TOMSK[1], 2.4)
    K(end(6) + 0.3, 88.0, 56.4, 3.2)
    O("banner", ST[6] - 0.02, WT(6, "Tobolsk") - 0.05, pill=(1582, 1586), name="TYUMEN", icon="snow", roll=0.5)
    O("banner", WT(6, "Tobolsk") - 0.05, WT(6, "Tomsk") - 0.05, pill=(1586, 1587), name="TOBOLSK", icon="snow", roll=0.4)
    O("banner", WT(6, "Tomsk") - 0.05, ST[8], pill=(1587, 1604), name="TOMSK", icon="snow", roll=0.8)
    O("fort", WT(6, "Tyumen") - 0.05, ST[7] + 0.5, lon=TYUMEN[0], lat=TYUMEN[1], txt="Tyumen", year=1586, size=56, side=-1)
    O("fort", WT(6, "Tobolsk") - 0.05, ST[7] + 0.5, lon=TOBOLSK[0], lat=TOBOLSK[1], txt="Tobolsk", year=1587, size=56, side=1)
    O("fort", WT(6, "Tomsk") - 0.05, ST[8] + 0.5, lon=TOMSK[0], lat=TOMSK[1], txt="Tomsk", year=1604, size=60, side=1)
    O("arrow", ST[6] + 0.1, WT(6, "Tomsk") + 1.5, pts=PATH[4:7], dur=3.4, w=14)

    # ---------------- L7-L8: soft gold and tribute (stamp slams)
    K(ST[7] - 0.05, 86.0, 56.6, 3.0)
    K(end(8) + 0.2, 91.0, 56.6, 3.4)
    O("stamp", WT(7, "soft") - 0.1, end(7) + 0.2, x=540, y=560, txt="SOFT GOLD", col=YEL, size=120, angle=-5)
    O("label", WT(7, "fur") - 0.05, WT(7, "soft") - 0.2, x=540, y=700, txt="THE GOAL: FUR", font=OSWB, size=80, col=WHT, shake=True)
    O("label", ST[8] + 0.1, end(8) + 0.3, x=540, y=760, txt="FUR TRIBUTE (YASAK)", font=OSWB, size=72, col=(255, 120, 110))

    # ---------------- L9: Krasnoyarsk 1628, Yakutsk 1632 (long pan between the Yenisei and the Lena)
    K(ST[9] - 0.05, KRAS[0], KRAS[1], 2.2, cut=True)
    K(WT(9, "Yakutsk") - 0.5, KRAS[0] + 3, KRAS[1] + 0.5, 3.6)
    K(WT(9, "Yakutsk") + 0.6, YAKUTSK[0], YAKUTSK[1], 3.0)
    K(end(9) + 0.2, YAKUTSK[0], YAKUTSK[1], 2.6)
    O("banner", ST[9] - 0.02, WT(9, "Yakutsk") - 0.3, pill=(1604, 1628), name="KRASNOYARSK", icon="snow", roll=0.7)
    O("banner", WT(9, "Yakutsk") - 0.3, ST[10], pill=(1628, 1632), name="YAKUTSK", icon="snow", roll=0.5)
    O("fort", WT(9, "Krasnoyarsk") - 0.05, WT(9, "Yakutsk") - 0.2, lon=KRAS[0], lat=KRAS[1], txt="Krasnoyarsk", year=1628, size=52, side=1)
    O("fort", WT(9, "Yakutsk") + 0.1, end(9) + 0.4, lon=YAKUTSK[0], lat=YAKUTSK[1], txt="Yakutsk", year=1632, size=58, side=1)
    O("rivers", ST[9], ST[10], names=["Yenisey", "Lena", "Angara"], w=6, step=1)
    O("arrow", ST[9] + 0.1, end(9) + 0.3, pts=PATH[7:13], dur=4.8, w=14)

    # ---------------- L10: brutal winter, thermometer to -60
    K(ST[10] - 0.05, YAKUTSK[0], YAKUTSK[1], 2.6)
    K(end(10) + 0.2, YAKUTSK[0] + 1.0, YAKUTSK[1] - 0.3, 3.2)
    SN(ST[10], 1.0)
    FLASH.append(WT(10, "brutal") - 0.05)
    O("banner", ST[10] - 0.02, ST[11] - 0.05, pill="YAKUTIA", name="WINTER", icon="snow")
    O("thermo", WT(10, "brutal") - 0.2, ST[11] - 0.05, x=170, y=900, v0=18, v1=-62, dur=2.0)

    # ---------------- L11: 1639 Moskvitin reaches the Sea of Okhotsk (cut, snow melts)
    K(ST[11] - 0.05, 141.0, 59.9, 5.2, cut=True)
    K(end(11) + 0.3, OKHOTSK[0], OKHOTSK[1], 2.6)
    SN(ST[11], 1.0)
    SN(WT(11, "Okhotsk") + 0.3, 0.15)
    O("banner", ST[11] - 0.02, ST[12] + 1.0, pill=(1632, 1639), name="MOSKVITIN", icon="snow", roll=0.8)
    O("arrow", ST[11] + 0.1, end(11) + 0.6, pts=PATH[12:], dur=3.0, w=14, keephead=True)
    O("pin", WT(11, "Okhotsk") - 0.1, end(12) + 0.3, lon=OKHOTSK[0], lat=OKHOTSK[1], txt="Sea of Okhotsk", len=200, size=72)

    # ---------------- L12: Pacific, HUD card with years after 1581, straight-line distance
    K(ST[12] - 0.05, OKHOTSK[0], OKHOTSK[1], 2.6)
    K(end(12) + 0.4, OKHOTSK[0] - 4.0, OKHOTSK[1] + 0.5, 5.0)
    O("stamp", ST[12] + 0.05, WT(12, "four") - 0.3, x=540, y=420, txt="PACIFIC OCEAN", col=(60, 170, 255), size=112, angle=-4)
    O("hudcard", WT(12, "four") - 0.1, ST[13] - 0.05, x=540, y=830, title="YEARS AFTER 1581", rows=[
        ("TYUMEN", "+5", 5 / 58, YEL), ("TOBOLSK", "+6", 6 / 58, YEL), ("TOMSK", "+23", 23 / 58, YEL),
        ("KRASNOYARSK", "+47", 47 / 58, YEL), ("YAKUTSK", "+51", 51 / 58, YEL), ("SEA OF OKHOTSK", "+58", 1.0, RED)])
    O("counter", WT(12, "four") + 0.2, ST[13] - 0.05, x=540, y=1260, v0=0, v1=4500, fmt="~{:,.0f} KM", dur=1.4, size=96, col=YEL, shake=True)

    # ---------------- L13: honest cost, calm pull-out
    K(ST[13] - 0.05, OKHOTSK[0] - 4.0, OKHOTSK[1] + 0.5, 5.0)
    K(end(13) + 0.3, OKHOTSK[0] - 8.0, OKHOTSK[1] + 1.0, 9.0)
    SN(ST[13], 0.15)
    O("label", ST[13] + 0.1, end(13) + 0.3, x=540, y=700, txt="LOST LAND · FORCED TRIBUTE", font=OSWB, size=70, col=WHT)

    # ---------------- L14-L15: back to the globe, gold Russia (loop frame), 17.1M km2
    GLOBE(ST[14] - 0.05, 1e9)
    GK(ST[14] - 0.05, 95, 56, 700)
    GK(end(15) + 0.3, 95, 56, 560)
    SN(ST[14] - 0.05, 0.0)
    O("banner", ST[14] - 0.05, 1e9, scene="both", pill="RUSSIA", name="11 TIME ZONES")
    O("fill", ST[14] - 0.05, 1e9, scene="globe", name="Russia", col=GOLD, alpha=0.2, glow=GOLD, border=GOLD, bw=5)
    O("counter", WT(14, "seventeen") - 0.1, end(14) + 0.3, scene="both", x=540, y=1000, v0=0, v1=17.1, fmt="{:.1f}M KM²", dur=1.2, size=118, col=YEL, shake=True)
    O("label", WT(15, "Eleven") - 0.05, end(15) + 0.3, scene="both", x=540, y=1000, txt="11 ZONES · 58 YEARS", font=OSWB, size=96, col=WHT)
    return None
