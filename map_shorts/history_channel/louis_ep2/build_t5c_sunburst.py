"""Builds the Sunburst (non-Lite) START still script of piece 5c from the Lite script, with the lessons of 07.11 applied: positive-only wording, light grey-hazel eyes, frame math (face 36 %, wig 68 %, margins 16 %), no device words."""
import os, re
H = os.path.dirname(os.path.abspath(__file__)) + "/"
src = open(H + "gen_t5c_" + "start.py").read()
s = src.replace('"model": "gpt-image-2.5-sunburst-lite"', '"model": "gpt-image-2.5-sunburst"')
s = s.replace("t5c_start_prompt.txt", "t5c_start_sunburst_prompt.txt").replace("pilot_frames/anchors/t5c_start_4k.jpg", "pilot_frames/anchors/t5c_start_sunburst_4k.jpg")

def rep(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new)

rep("real skin texture, no beauty filter. ", "real unretouched natural skin texture. ")
rep("same heavy-lidded eyes,", "same heavy-lidded light grey-hazel eyes,")
rep("the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden),", "the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light),")
rep('"do not copy its neutral pose or backdrop. "', '"take only the face, wig and costume from it. "')
rep("looking DOWN at him from about 55 degrees above as he leans back in a gilded armchair (a high angle, never eye level), rolled about 14 degrees to the right; ",
    "looking DOWN at him from about 55 degrees above as he leans back in a gilded armchair (a clearly high angle), rolled about 14 degrees to the right; ")
rep("his face fills about 40 percent of the frame width with its centre at 50 percent, the whole tall wig about 75 percent of the width and inside the frame,",
    "his face fills about 36 percent of the frame width with its centre at 50 percent, the whole tall wig about 68 percent of the width with at least 15 percent free space on each side,")
rep("the carved gilded armchair and the candlelit gilded hall blurred, no chandelier, and on the right and right-centre blurred figures far below: ",
    "the carved gilded armchair and the candlelit gilded hall blurred, lit by wall sconces with the ceiling out of frame, and on the right and right-centre blurred figures far below: ")
rep('"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "',
    '"One king only, natural light rouge. The table and the armchair hold only plates, gold dishes, silver platters, napkins and candle holders. Clean picture with no text or lettering, no modern objects, only things of the 1680s. "')
i = s.index('"""', 3)
doc = ('"""Take 5 piece 5c START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Setup S12 (from above, leaning back, eyes closed in a long happy sigh, hands on the belly). '
       'Refs in order: K4_master_neutral_O8.png, K4_angle_high_O13.png. Result: pilot_frames/anchors/t5c_start_sunburst_4k.jpg. Run: python3 gen_t5c_start_sunburst.py go\nBRIEF: briefs/brief_t5_t7.md\n"""')
open(H + "gen_t5c_start_" + "sunburst.py", "w").write(doc + s[i + 3:])
print("built")
