"""Lofoten Short, globe part only (engine69): fast zoom onto the Lofoten islands + the one white text block for ~3 s.
The 7 drone shots are real footage cut in ffmpeg on the same beat grid (see assemble69.sh). Camera API as in shots68."""


def build(short, K, O, GK, GLOBE, OB, OBL, HOOK, ST, D, BLEND=None):
    cut = lambda i: ST[i] - 0.05                                                    # noqa: E731
    # fast vertical zoom (reference: globe -> coast -> satellite frame -> hard cut to the drone):
    # globe 0-1.35 s, crossfade, then the flat satellite map falls from the whole region down to Reine (WLD -> NOR -> LOF -> REI imagery)
    tg = 1.35
    GLOBE(0, tg)
    GK(0, 42, 47, 520)
    GK(tg, 14.0, 62.0, 2200)
    BLEND.append((tg - 0.2, tg))
    K(tg, 14.0, 62.0, 25.0, cut=True)
    K(1.75, 13.8, 68.0, 3.6, lin=True)
    K(2.35, 13.12, 67.97, 0.195, lin=True)                 # constant zoom rate; centre reaches the islands early, then dives onto Reine
    K(cut(1), 13.06, 67.945, 0.022, lin=True)
    HOOK.append((0.1, cut(1), ["This is Lofoten, Norway.", "Above the Arctic Circle"], "NO"))
    return None
