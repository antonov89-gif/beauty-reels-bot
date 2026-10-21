"""Lofoten Short, globe part only (engine69): fast zoom onto the Lofoten islands + the one white text block for ~3 s.
The 7 drone shots are real footage cut in ffmpeg on the same beat grid (see assemble69.sh). Camera API as in shots68."""


def build(short, K, O, GK, GLOBE, OB, OBL, HOOK, ST, D):
    cut = lambda i: ST[i] - 0.05                                                    # noqa: E731
    GLOBE(0, cut(1))
    GK(0, 42, 47, 520)
    GK(cut(1), 13.6, 63.0, 2600)
    HOOK.append((0.1, cut(1), ["This is Lofoten, Norway.", "Above the Arctic Circle"], "NO"))
    return None
