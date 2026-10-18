"""Shot list for the Turkey country-profile Short (E5: continuous camera, reference = MapTrail 'Spain').
S(t, "sat", key, z0, z1, cx, cy[, "cont"])   satellite scene; cx = (lon, lat) or ((lon0, lat0), (lon1, lat1)) for a pan;
                                             "cont" = continues the previous shot without whip/flash (match z and centre!)
S(t, "tilt", key, z0, z1, cx, cy, u0, u1, p0, p1)   tilted 3D card; u = tilt 0..1, p = card scale
O(fn, ...)                                    overlays, see engine62.overlays; on a tilt card: arc / dot / clabel.
build() returns the hook (two title lines)."""
YEL, RED, GRN, BLU, WHT, BLK = (255, 214, 10), (232, 52, 52), (70, 205, 100), (80, 170, 255), (255, 255, 255), (0, 0, 0)
ORG, CYAN, PINK, PUR = (255, 150, 40), (90, 220, 255), (255, 80, 160), (170, 110, 255)

HOOK = ("1 COUNTRY", "2 CONTINENTS")
TR_C = (35.0, 39.0)                     # hook framing centre
EYES = (34.6, 38.95)
SPLIT = [(29.13, 41.24), (29.02, 41.0), (28.3, 40.8), (27.3, 40.55), (26.65, 40.3), (26.2, 40.03)]   # Bosphorus-Marmara-Dardanelles (schematic)
AZ_BORDER = [(44.7683, 39.7035), (44.7834, 39.6847), (44.8172, 39.6504)]                           # Natural Earth shared vertices
NARROW = [(29.0568, 41.0874), (29.0658, 41.0874)]                                                   # Rumelihisari, ~750 m E-W on Esri imagery; usual figure ~700 m
IST = (28.98, 41.01)


def build(short, S, O, WT, ST, D):
    def turkey(ts=-0.3, fill=0.42):
        O("country", "Turkey", ts, RED, fill)

    # L0 hook: Turkey in red, Europe/Asia split, mascot eyes, flag
    S(0, "sat", "TUR", 1.0, 1.12, TR_C, 0)
    turkey()
    O("route", SPLIT, -1, 0.1, YEL, 9, True)
    O("geolabel", 30.0, 42.6, "EUROPE", -0.3, 58, CYAN)
    O("geolabel", 39.6, 40.55, "ASIA", -0.3, 58, YEL)
    O("eyes", EYES[0], EYES[1], 46, -0.3, ST[2] - 0.1)
    O("flag", "TR", 540, 560, 190, -0.3)

    # L1 97 % / 3 %: slow push towards Thrace (continuous)
    S(ST[1] - 0.1, "sat", "TUR", 1.12, 1.45, (TR_C, (32.0, 39.8)), 0, "cont")
    turkey()
    O("route", SPLIT, -1, 0.1, YEL, 9, True)
    O("geolabel", 29.0, 42.3, "EUROPE", -1, 58, CYAN)
    O("eyes", EYES[0], EYES[1], 46, -0.3, ST[2] - 0.1)
    O("counter", 0, 97, "{:.0f}% IN ASIA", 540, 520, WT(1, "Ninety-seven") - 0.1, 0.8, 86, YEL, BLK)
    O("counter", 0, 3, "{:.0f}% IN EUROPE", 540, 640, WT(1, "three") - 0.1, 0.4, 70, CYAN, BLK)

    # L2-L4 neighbours: pull out to the wide map, then one continuous pan west -> east -> south -> Nakhchivan
    z = 1.25
    S(ST[2] - 0.1, "sat", "NBR", 1.1, z, ((31.0, 39.5), (27.5, 40.5)), 0)
    turkey(-1, 0.25)
    O("country", "Greece", WT(2, "Greece") - 0.1, BLU, 0.4)
    O("geolabel", 22.3, 39.6, "GREECE", WT(2, "Greece"), 54, WHT)
    O("country", "Bulgaria", WT(2, "Bulgaria") - 0.1, GRN, 0.4)
    O("geolabel", 25.2, 42.75, "BULGARIA", WT(2, "Bulgaria"), 54, WHT)
    O("counter", 0, 8, "{:.0f} NEIGHBOURS", 540, 470, WT(2, "around") - 0.1, 2.0, 70, YEL, BLK)

    t_e = WT(2, "Bulgaria") + 0.35
    S(t_e, "sat", "NBR", z, z, ((27.5, 40.5), (39.5, 39.5)), 0, "cont")
    turkey(-1, 0.25)
    O("country", "Greece", -1, BLU, 0.4)
    O("country", "Bulgaria", -1, GRN, 0.4)
    O("geolabel", 22.3, 39.6, "GREECE", -1, 54, WHT)
    O("geolabel", 25.2, 42.75, "BULGARIA", -1, 54, WHT)
    O("country", "Georgia", WT(3, "Georgia") - 0.1, ORG, 0.45)
    O("geolabel", 41.9, 42.1, "GEORGIA", WT(3, "Georgia"), 52, WHT)
    O("country", "Armenia", WT(3, "Armenia") - 0.1, PINK, 0.5)
    O("geolabel", 44.2, 40.35, "ARMENIA", WT(3, "Armenia"), 46, WHT)
    O("country", "Iran", WT(3, "Iran") - 0.1, PUR, 0.4)
    O("geolabel", 45.6, 37.4, "IRAN", WT(3, "Iran"), 56, WHT)
    O("counter", 8, 8, "{:.0f} NEIGHBOURS", 540, 470, -1, 0.01, 70, YEL, BLK)

    t_s = WT(3, "Iran") + 0.3
    S(t_s, "sat", "NBR", z, z, ((39.5, 39.5), (39.0, 36.5)), 0, "cont")
    turkey(-1, 0.25)
    for n, c in (("Georgia", ORG), ("Armenia", PINK), ("Iran", PUR)):
        O("country", n, -1, c, 0.4)
    O("geolabel", 41.9, 42.1, "GEORGIA", -1, 52, WHT)
    O("geolabel", 44.2, 40.35, "ARMENIA", -1, 46, WHT)
    O("geolabel", 45.6, 37.4, "IRAN", -1, 56, WHT)
    O("country", "Iraq", WT(3, "Iraq") - 0.1, GRN, 0.4)
    O("geolabel", 43.6, 34.2, "IRAQ", WT(3, "Iraq"), 56, WHT)
    O("country", "Syria", WT(3, "Syria") - 0.1, CYAN, 0.4)
    O("geolabel", 38.3, 35.2, "SYRIA", WT(3, "Syria"), 56, WHT)
    O("counter", 8, 8, "{:.0f} NEIGHBOURS", 540, 470, -1, 0.01, 70, YEL, BLK)

    S(ST[4] - 0.15, "sat", "NBR", z, 3.4, ((39.0, 36.5), (44.6, 39.6)), 0, "cont")
    turkey(-1, 0.25)
    for n, c in (("Iran", PUR), ("Armenia", PINK), ("Iraq", GRN), ("Syria", CYAN), ("Georgia", ORG)):
        O("country", n, -1, c, 0.4)
    O("country", "Azerbaijan", WT(4, "Azerbaijan") - 0.2, YEL, 0.5)
    O("route", AZ_BORDER, WT(4, "less") - 0.1, 0.4, RED, 14, False)
    O("pin", 44.783, 39.685, "< 20 KM BORDER", WT(4, "less") - 0.05, RED)
    O("geolabel", 45.15, 39.1, "AZERBAIJAN", WT(4, "Azerbaijan"), 46, YEL)
    O("counter", 8, 8, "{:.0f} NEIGHBOURS", 540, 470, -1, 0.01, 70, YEL, BLK)

    # L5 four seas: continuous pull-out back to the whole region
    S(ST[5] - 0.15, "sat", "NBR", 3.4, 1.1, ((44.6, 39.6), (33.0, 38.5)), 0, "cont")
    turkey(-1, 0.3)
    O("counter", 0, 4, "{:.0f} SEAS", 540, 470, WT(5, "Four") - 0.1, 0.6, 84, CYAN, BLK)
    O("geolabel", 36.0, 43.3, "BLACK SEA", WT(5, "Black"), 54, CYAN)
    O("geolabel", 31.0, 34.3, "MEDITERRANEAN", WT(5, "Mediterranean"), 50, CYAN)
    O("geolabel", 25.0, 38.3, "AEGEAN", WT(5, "Aegean"), 50, CYAN)
    O("geolabel", 28.0, 40.25, "MARMARA", WT(5, "Marmara"), 40, CYAN)

    # L6 surprise: fast punch-in on Istanbul
    S(ST[6] - 0.1, "sat", "MAR", 1.0, 2.4, (29.02, 41.05), 0)
    O("slam", "THE REAL SURPRISE", 540, 520, ST[6] + 0.05, 74, WHT, PINK)
    O("pin", IST[0], IST[1], "ISTANBUL", ST[6] + 0.3, ORG)

    # L7 Bosphorus: city -> narrows
    S(ST[7] - 0.1, "sat", "IST", 1.0, 1.6, (29.04, 41.07), 0)
    O("geolabel", 28.93, 41.10, "EUROPE", WT(7, "Europe"), 64, CYAN)
    O("geolabel", 29.15, 41.03, "ASIA", WT(7, "Asia"), 64, YEL)
    O("pin", 29.06, 41.09, "BOSPHORUS", WT(7, "Bosphorus") - 0.1, CYAN)
    S(WT(7, "narrowest") - 0.25, "sat", "BOS", 1.0, 1.35, (29.0615, 41.0877), 0)
    O("route", NARROW, WT(7, "narrowest") + 0.1, 0.6, YEL, 12, False)
    O("counter", 0, 700, "~{:.0f} M", 540, 520, WT(7, "seven") - 0.1, 0.8, 120, YEL, BLK)
    O("geolabel", 29.0505, 41.0935, "EUROPE", WT(7, "narrowest"), 60, CYAN)
    O("geolabel", 29.0725, 41.0815, "ASIA", WT(7, "narrowest") + 0.1, 60, YEL)

    # L8 commute: ferries and bridges between continents
    S(ST[8] - 0.1, "sat", "IST", 1.5, 1.2, (29.02, 41.04), 0)
    O("geolabel", 28.95, 41.075, "EUROPE", ST[8], 60, CYAN)
    O("geolabel", 29.09, 41.0, "ASIA", ST[8] + 0.1, 60, YEL)
    O("route", [(29.024, 40.992), (28.99, 41.005), (28.974, 41.018)], WT(8, "commute") - 0.1, 1.0, YEL, 9, True)
    O("route", [(29.015, 41.027), (29.004, 41.035), (29.0, 41.041)], WT(8, "commute") + 0.2, 1.0, YEL, 9, True)
    O("route", [(29.05, 41.03), (29.02, 41.05), (29.005, 41.06)], WT(8, "Europe") - 0.1, 1.0, CYAN, 9, True)
    O("big", "ASIA TO EUROPE", 540, 520, WT(8, "Asia") - 0.1, 76, WHT, PINK)
    O("pill", "DAILY COMMUTE", 540, 640, 44, WT(8, "work") - 0.2)

    # L9 size: back to the hook framing, area counter + bars
    S(ST[9] - 0.1, "sat", "TUR", 1.0, 1.1, TR_C, 0)
    turkey(-1, 0.42)
    O("counter", 0, 783562, "{:,.0f} KM²", 540, 520, WT(9, "seven") - 0.1, 1.3, 84, YEL, BLK)
    O("tint", BLK, 110, WT(9, "twice") - 0.3)
    O("bars", WT(9, "twice") - 0.2, [("TURKEY", 783562, RED, 0.0), ("GERMANY × 2", 715176, (90, 90, 110), 0.35)], 1020)

    # L10 Ararat: continuous pan east, then cut to the mountain
    S(ST[10] - 0.1, "sat", "TUR", 1.1, 2.6, (TR_C, (43.4, 39.6)), 0, "cont")
    turkey(-1, 0.3)
    O("pin", 44.298, 39.702, "MOUNT ARARAT", WT(10, "east") - 0.1, ORG)
    S(WT(10, "Ararat") - 0.15, "sat", "ARA", 1.0, 1.6, (44.2983, 39.7016), 0)
    O("pin", 44.2983, 39.7016, "MOUNT ARARAT", WT(10, "Ararat"), ORG)
    O("counter", 0, 5137, "{:,.0f} M", 540, 520, WT(10, "five") - 0.1, 0.9, 110, WHT, BLK)
    O("pill", "NOAH'S ARK · LEGEND", 540, 650, 42, WT(10, "Noah's") - 0.1)

    # L11-L12 Ottoman reach: pull out into the tilted world card, arcs to three continents
    S(ST[11] - 0.1, "tilt", "OTT", 1.0, 1.12, (24.0, 37.0), 0, 0.0, 1.0, 1.9, 1.0)
    O("dot", IST[0], IST[1], -1)
    O("arc", IST, (19.04, 47.50), WT(11, "Ottoman") - 0.1, YEL)        # Budapest
    O("arc", IST, (44.37, 33.31), WT(11, "Empire"), YEL)               # Baghdad
    O("arc", IST, (31.24, 30.04), WT(11, "ruled") - 0.1, YEL)          # Cairo
    O("arc", IST, (3.06, 36.75), WT(11, "parts"), YEL)                 # Algiers
    O("arc", IST, (39.83, 21.42), WT(11, "continents") - 0.2, YEL)     # Mecca
    O("counter", 0, 3, "{:.0f} CONTINENTS", 540, 470, WT(11, "three") - 0.1, 0.5, 84, YEL, BLK)
    O("clabel", 12.0, 49.5, "EUROPE", WT(12, "Europe") - 0.1, 70, CYAN)
    O("clabel", 52.0, 41.0, "ASIA", WT(12, "Asia") - 0.1, 70, YEL)
    O("clabel", 14.0, 24.0, "AFRICA", WT(12, "Africa") - 0.1, 70, ORG)
    O("counter", 1299, 1922, "{:.0f}", 540, 1360, WT(12, "six") - 0.3, 1.0, 110, WHT, BLK)
    O("big", "600+ YEARS", 540, 1480, WT(12, "years") - 0.1, 70, YEL, PINK)

    # L13 loop: pull back out to the hook framing, eyes return
    S(ST[13] - 0.1, "sat", "TUR", 1.7, 1.0, ((29.5, 40.6), TR_C), 0)
    turkey(ST[13], 0.42)
    O("route", SPLIT, ST[13] + 0.2, 0.9, YEL, 9, True)
    O("geolabel", 30.0, 42.6, "EUROPE", WT(13, "bridge") - 0.2, 58, CYAN)
    O("geolabel", 39.6, 40.55, "ASIA", WT(13, "two") - 0.1, 58, YEL)
    O("eyes", EYES[0], EYES[1], 46, WT(13, "started") - 0.2, 999)
    return HOOK
