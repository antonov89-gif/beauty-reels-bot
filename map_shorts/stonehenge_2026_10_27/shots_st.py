"""Stonehenge: how it was built (AI reconstruction). SB-v1 = STYLE v2 (game-engine CG, prompts/style_zackd_3d_render.md) + SCENE LOCK + SHOT DELTA.
Usage: python3 shots_st.py s01 s02 ...  -> /home/claude/v85/frames/<id>.jpg (Nano Banana 2.1, 1K, $0.02 each)."""
import subprocess
import sys

LOCK = ("Neolithic Britain about 2500 BC, Salisbury Plain chalk grassland, overcast soft daylight. People: Neolithic farmers in plain "
        "undyed wool tunics and leather wraps, bare heads, long hair and beards, no metal, no helmets, no modern items. Ropes are thick "
        "twisted plant-fibre ropes. Stones are grey-brown sarsen sandstone, rough hammered surfaces. ")
SHOTS = {
    "s01": "Wide low-angle shot of the finished Stonehenge sarsen circle with lintels on top, at sunrise, a small group of Neolithic people "
           "standing in front holding stone hammers and coiled ropes, monument huge compared to them.",
    "s02": "A giant rectangular sarsen stone, about four times taller than a man, lying on a wooden sledge at the edge of a forest clearing, "
           "dozens of people in two long lines pulling thick ropes, leaning forward with effort.",
    "s03": "Close low shot along the ground: the wooden sledge with the huge stone sliding over parallel timber rails laid on the grass, "
           "logs and rails in the foreground, feet and straining legs of the pullers.",
    "s04": "A huge sarsen stone lying at the edge of a deep rectangular pit, its end tipping down into the pit, a team holding ropes and "
           "wooden levers behind it, dust in the air.",
    "s05": "The same giant stone half-raised at a steep angle from the pit, a wooden A-frame of timber beams behind it, many people pulling "
           "ropes from the far side to haul it upright.",
    "s06": "Two upright sarsen stones with a horizontal lintel stone being raised on top using a tall crib of stacked timber logs, people on "
           "the timber platform pushing the lintel with levers; on the top of each upright a small rounded stone knob (tenon) is visible.",
    "s07": "Aerial view of rolling green Welsh hills, a long line of people dragging a smaller blue-grey stone on a sledge along a valley path.",
    "s08": "Inside the stone circle, a long flat reddish-grey sandstone slab lying on the grass in the centre, low golden light, mist, "
           "the uprights around it in soft focus, no people, mysterious mood.",
}
if __name__ == "__main__":
    for s in sys.argv[1:]:
        subprocess.Popen(["python3", "/home/user/beauty-reels-bot/map_shorts/stonehenge_2026_10_27/gen_frame.py", f"/home/claude/v85/frames/{s}.jpg",
                          LOCK + SHOTS[s]], stdout=open(f"/home/claude/v85/frames/{s}.log", "w"), stderr=subprocess.STDOUT)
