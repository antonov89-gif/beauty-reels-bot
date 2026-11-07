"""Builds the Sunburst (non-Lite) START still script of piece 6 (the verdict, S13, frontal eye level close) from the Lite script, with the lessons of 07.11 applied: positive-only wording, light grey-hazel eyes, hall ref as mood only, frame math (face 28 %, wig 55 %, margins >= 20 %), no device words."""
import os
H = os.path.dirname(os.path.abspath(__file__)) + "/"
src = open(H + "gen_t6_" + "start.py").read()
s = src.replace('"model": "gpt-image-2.5-sunburst-lite"', '"model": "gpt-image-2.5-sunburst"')
s = s.replace("t6_start_prompt.txt", "t6_start_sunburst_prompt.txt").replace("pilot_frames/anchors/t6_start_4k.jpg", "pilot_frames/anchors/t6_start_sunburst_4k.jpg")

def rep(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new)

rep("real skin texture, no beauty filter. ", "real unretouched natural skin texture. ")
rep("same heavy-lidded eyes,", "same heavy-lidded light grey-hazel eyes,")
rep("the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden),", "the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light),")
rep('"do not copy its neutral pose or backdrop. "', '"take only the face, wig and costume from it. "')
rep('"Reference 2 shows only the hall: "\n"ignore its angle, and do NOT copy its crystal glasses or the people at its table; "',
    '"Reference 2 gives only the mood of the hall: gilded walls, warm candlelight, standing courtiers in grey wigs; take no objects and no people from it, the table and the people are new. "')
rep("his face fills about 30 percent of the frame width with its centre at 50 percent of the frame width, the whole tall wig about 70 percent of the width and fully inside the frame, sharp; ",
    "his face fills about 28 percent of the frame width with its centre at 50 percent of the frame width, the whole tall wig about 55 percent of the width with at least 20 percent free space on each side and a band of empty gilded wall about 10 percent of the frame height above the wig, sharp; ")
rep("at the lower edge a gold plate with a few small clean bird bones, soft. ", "at the lower edge a gold plate with a few small clean bird bones, soft, and nothing else on the table but plates, gold dishes and a candle holder. ")
rep("the candlelit gilded hall, standing courtiers in plain wigs, at the back right a lady with a fan and two courtiers whispering, no chandelier. ",
    "the candlelit gilded hall lit by wall sconces with the ceiling out of frame, standing courtiers in plain wigs, at the back right a lady with an open fan and two courtiers whispering. ")
rep('"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "',
    '"One king only, natural light rouge. Clean picture with no text or lettering, no modern objects, only things of the 1680s. "')

rep("his heavy-lidded eyes looking down at the bones on the plate with a complacent faint smirk, the lips closed. ", "both eyes open, the irises visible under the heavy upper lids, looking down at the bones on the plate, a complacent faint smirk, the lips closed. ")
rep("the whole tall wig about 55 percent of the width with at least 20 percent free space on each side and a band of empty gilded wall about 10 percent of the frame height above the wig, sharp; ", "the powdered wig puff about 50 percent of the frame width, the whole wig with its long side curls about 62 percent, so at least 18 percent of free gilded wall at each side, and a band of empty wall about 10 percent of the frame height above the wig, sharp; ")
rep("Reference 2 gives only the mood of the hall: gilded walls, warm candlelight, standing courtiers in grey wigs; take no objects and no people from it, the table and the people are new. ", "Reference 2 gives only the mood of the hall: gilded walls and warm candlelight. Its people, its crystal glasses and its chandelier are not used; the table and the people are new. ")
rep("on a single lace napkin held in one hand just below the frame,", "on a single lace napkin held in one hand just below the frame, both hands are below the lower edge of the frame, no hand and no napkin visible,")

rep("hand-held at arm's length at EYE LEVEL, frontal, close: ", "hand-held at the end of his own stretched arm at EYE LEVEL, frontal, close, his right arm reaches toward the camera and stays out of the frame, the view is from the end of that arm: ")
rep("on a single lace napkin held in one hand just below the frame, both hands are below the lower edge of the frame, no hand and no napkin visible,", "on a single lace napkin held in his left hand just below the frame, the hand and the napkin are below the lower edge of the frame and not visible,")
i = s.index('"""', 3)
doc = ('"""Take 6 (the verdict) START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Setup S13 (frontal, eye level, close; wiping the fingers, eyes down on the bones, complacent smirk). '
       'Refs in order: K4_master_neutral_O8.png, R10_hall_clean.jpg. Result: pilot_frames/anchors/t6_start_sunburst_4k.jpg. Run: python3 gen_t6_start_sunburst.py go\nBRIEF: briefs/brief_t5_t7.md\n"""')
open(H + "gen_t6_start_" + "sunburst.py", "w").write(doc + s[i + 3:])
print("built")
