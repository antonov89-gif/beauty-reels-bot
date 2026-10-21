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
    end0 = 6 * 60 / 124                                # first cut exactly on beat 6 (2.903 s)
    K(1.75, 13.8, 68.0, 2.7, lin=True)                 # exponential dive (constant zoom rate), then a short settle (reference: slight settle at the end)
    K(2.35, 13.1, 67.96, 0.097, lin=True)
    K(2.62, 13.07, 67.947, 0.024, lin=True)
    K(end0, 13.06, 67.945, 0.011, lin=True)
    HOOK.append((0.1, end0 - 0.02, ["This is Lofoten, Norway.", "Above the Arctic Circle"], "NO"))
    # footage cut points (beats of 60/124 s) for the audio accents: the drone shots themselves are cut in assemble69.sh
    bt = 60 / 124
    b = [6, 14, 20, 28, 30, 32, 41]
    for i in range(len(b) - 1):
        OBL(b[i] * bt, b[i + 1] * bt)                     # exact beats: cuts land on the kick
    return None
