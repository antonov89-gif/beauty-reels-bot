"""Lofoten v5 (engine69): ONE hero subject, Reine village, every shot of the same place (reference: one temple from all angles).
Map/globe -> satellite dive through clouds down to the rooftops of Reine (top-down), hard cut to drone shots of Reine, finale straight down
on Reine's rooftops with a slow clockwise turn, loop to the globe. Beat grid of the music track: 125 BPM (cuts at beats 6/14/20/28/30/32)."""
T = 60 / 125
F = lambda j: round(j * T * 30) / 30                                              # noqa: E731  beat j -> time of its frame
CUTS = [F(j) for j in (6, 14, 20, 28, 30, 32)]                                    # 2.867, 6.733, 9.6, 13.433, 14.4, 15.367
REINE = (13.0886, 67.9326)


def build(short, K, O, GK, GLOBE, OB, OBL, HOOK, ST, D, BLEND=None):
    end0 = CUTS[0]
    # globe 0-1.35 s (clouds pass in front at ~0.8-1.6 s), crossfade, then the satellite dive to the rooftops (~350 m view), top-down
    tg = 1.35
    GLOBE(0, tg)
    GK(0, 42, 47, 520)
    GK(tg, 14.0, 62.0, 2200)
    BLEND.append((tg - 0.2, tg))
    K(tg, 14.0, 62.0, 25.0, cut=True)
    K(1.75, 13.6, 67.8, 2.4, lin=True)                 # exponential dive
    K(2.25, 13.12, 67.94, 0.07, lin=True)
    K(2.55, 13.092, 67.934, 0.008, lin=True)
    K(end0, REINE[0], REINE[1], 0.0017, lin=True)      # short settle on the roofs
    HOOK.append((0.1, end0 - 0.02, ["Above the Arctic Circle.", "Yet the sea doesn't freeze"], "EMOJI:\U0001F30A"))
    # finale (after the drone shots): straight down on the rooftops, slow descent + clockwise turn, then the loop cut to the globe
    t6 = CUTS[5]
    OBL(t6, 99)
    OB(t6, REINE[0] + 0.0004, REINE[1] - 0.0002, 0.0023, 0.0, 0, cut=True)
    OB(19.84, REINE[0] + 0.0004, REINE[1] - 0.0002, 0.0017, 0.0, 24)
    return None
