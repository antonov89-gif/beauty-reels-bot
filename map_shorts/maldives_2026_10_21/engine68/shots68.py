"""Maldives Short v2 (silent, ~20 s, 124 BPM), engine68: built to the DNA report of rajography jTJ2UFF3B0I (principles only).
Reference rules applied: 3 s globe zoom + ONE white text block (thin shadow) -> hard cuts on the beat every ~2.4 s (8 cuts incl. loop),
different 'drone' angles (oblique push-in, orbit, pan, lift), no other text, no SFX, ends top-down, loops to the globe.
Beat = 60/124 s; ST[i] sit on beats 0, 6, 11, 16, 21, 26, 31, 36."""


def build(short, K, O, GK, GLOBE, OB, OBL, HOOK, ST, D):
    cut = lambda i: ST[i] - 0.05                                                    # noqa: E731
    end = ST[7] + D[7] + 0.9

    # S0 globe: fast vertical zoom onto the Maldives, hook text for 3 s
    GLOBE(0, cut(1))
    GK(0, 5, 22, 520)
    GK(cut(1), 73.2, 3.5, 2300)
    HOOK.append((0.1, cut(1), ["The sea is rising.", "Maldives: 1.5 m high"], True))

    OBL(cut(1), end)
    # S1 whole archipelago from high up, tilting in
    OB(cut(1), 73.4, 3.6, 1.7, 0.5, -8, cut=True)
    OB(cut(2) - 0.05, 73.45, 4.3, 1.1, 0.6, 6)
    # S2 Male: orbit + push-in
    OB(cut(2), 73.511, 4.180, 0.012, 0.6, -14, cut=True)
    OB(cut(3) - 0.05, 73.511, 4.178, 0.0085, 0.6, 8)
    # S3 airport island: pan along the runway, oblique
    OB(cut(3), 73.5285, 4.200, 0.011, 0.6, -8, cut=True)
    OB(cut(4) - 0.05, 73.5295, 4.180, 0.011, 0.6, 8, lin=True)
    # S4 Thulusdhoo island and its lagoon, oblique pan
    OB(cut(4), 73.6455, 4.370, 0.012, 0.6, 10, cut=True)
    OB(cut(5) - 0.05, 73.656, 4.381, 0.010, 0.6, -8)
    # S5 Fuvahmulah, low oblique orbit
    OB(cut(5), 73.4235, -0.2945, 0.016, 0.6, -14, cut=True)
    OB(cut(6) - 0.05, 73.4235, -0.2945, 0.012, 0.6, 8)
    # S6 Gan (Addu atoll): pan along the airfield, oblique
    OB(cut(6), 73.1475, -0.689, 0.010, 0.6, -10, cut=True)
    OB(cut(7) - 0.05, 73.1605, -0.697, 0.010, 0.6, 8, lin=True)
    # S7 straight down on the island, slow push-in, ends the loop
    OB(cut(7), 73.4235, -0.2945, 0.026, 0.0, 0, cut=True)
    OB(end - 0.9, 73.4235, -0.2945, 0.012, 0.0, 18)
    return None
