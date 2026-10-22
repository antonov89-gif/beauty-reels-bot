"""Lofoten v5 (engine69): ONE hero subject, Reine village, every shot of the same place (reference: one temple from all angles).
Map/globe -> satellite dive through clouds down to the rooftops of Reine (top-down), hard cut to drone shots of Reine, finale straight down
on Reine's rooftops with a slow clockwise turn, loop to the globe. Beat grid of the music track: 125 BPM (cuts at beats 6/14/20/28/30/32)."""
CUT_FRAMES = [87, 202, 285, 400, 429, 458]          # snapped to the measured drum hits of the track (beats 6/14/20/28/30/32 at ~125 BPM)
CUTS = [f / 30 for f in CUT_FRAMES]
REINE = (13.0886, 67.9326)


def build(short, K, O, GK, GLOBE, OB, OBL, HOOK, ST, D, BLEND=None):
    end0 = CUTS[0]
    # globe 0-1.35 s (clouds pass in front at ~0.8-1.6 s), crossfade, then the satellite dive to the rooftops (~350 m view), top-down
    tg = 1.35
    GLOBE(0, tg)
    GK(0, 42, 47, 520)
    GK(tg, 14.0, 62.0, 2200)
    BLEND.append((tg - 0.2, tg))
    K(tg, 14.0, 62.0, 25.0, cut=True)                  # flat view only for the globe crossfade
    # the dive itself runs on the oblique camera with terrain relief: the view tilts like a Google-Earth fly-in, then levels to straight down
    OBL(tg, end0)
    OB(tg, 14.0, 62.0, 25.0, 0.0, 0, cut=True)
    OB(1.75, 13.6, 67.8, 2.4, 0.35, -6, lin=True)
    OB(2.25, 13.12, 67.94, 0.07, 0.45, 5, lin=True)
    OB(2.6, 13.092, 67.934, 0.008, 0.15, 3, lin=True)
    OB(end0, REINE[0], REINE[1], 0.0017, 0.0, 0, lin=True)  # level, straight down on the roofs
    HOOK.append((0.1, end0 - 0.02, ["Above the Arctic Circle.", "Yet the sea doesn't freeze"], "EMOJI:\U0001F30A"))
    # finale (after the drone shots): straight down on the rooftops, slow descent + clockwise turn, then the loop cut to the globe
    t6 = CUTS[5]
    OBL(t6, 99)
    OB(t6, REINE[0] + 0.0004, REINE[1] - 0.0002, 0.0023, 0.0, 0, cut=True)
    OB(19.84, REINE[0] + 0.0004, REINE[1] - 0.0002, 0.0017, 0.0, 24)
    return None
