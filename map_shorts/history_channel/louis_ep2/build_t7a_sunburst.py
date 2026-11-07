"""Builds the Sunburst (non-Lite) START still script of piece 7a (S16, the king thinks and looks around the hall) from the Lite script, with the lessons of 07.11 applied: positive-only wording, light grey-hazel eyes, hall ref as mood only, the self-filmed vlog look (close, off-centre, head tilted, wide-angle phone lens, imperfect), frame math with margins, a hand cut by the frame edge, no device words."""
import os
H = os.path.dirname(os.path.abspath(__file__)) + "/"
src = open(H + "gen_t7a_" + "start.py").read()
s = src.replace('"model": "gpt-image-2.5-sunburst-lite"', '"model": "gpt-image-2.5-sunburst"')
s = s.replace("t7a_start_prompt.txt", "t7a_start_sunburst_prompt.txt").replace("pilot_frames/anchors/t7a_start_4k.jpg", "pilot_frames/anchors/t7a_start_sunburst_4k.jpg")

def rep(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new)

rep("real skin texture, no beauty filter. ", "real unretouched natural skin texture. ")
rep("same heavy-lidded eyes,", "same heavy-lidded light grey-hazel eyes,")
rep("the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden),", "the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light),")
rep('"do not copy its neutral pose or backdrop. "', '"take only the face, wig and costume from it. "')
rep("take the camera angle and the head pose from it, the face and the wig from reference 1. ", "take the head turn from it, the face and the wig from reference 1. ")
rep('"Reference 3 shows only the hall: "\n"ignore its angle, and do NOT copy its crystal glasses or the people at its table; "',
    '"Reference 3 gives only the gilded walls and the warm candlelight of the hall; the table, the people and the dishes are new. "')
rep("hand-held, held at arm's length a little BELOW his eye level, wide lens, so that the hall can be seen: ",
    "the look of a frame from a hand-held vlog that he films of himself at arm's-length distance, not a studio portrait, held a little BELOW his eye level, a wide-angle lens with visible perspective, spontaneous and a little imperfect, so that the hall can be seen: ")
rep("his head with the wig fills about 60 percent of the frame width (his face about 30 percent) with its centre at 40 percent (a little left of centre), the head turned about 30 degrees toward the viewer's right with the beauty mark still visible; ",
    "his head with the whole wig fills about 58 percent of the frame width with at least 14 percent free wall at the left (his face about 28 percent) with its centre at 42 percent, the top of the wig 8 percent of the frame height below the top edge, the head turned about 30 degrees toward the viewer's right and tilted about 6 degrees with the beauty mark still visible; ")
rep("a strip of the gilded ceiling at the top edge; \"\n\"no chandelier; \"\n", "the gilded wall above; \"\n\"the hall is lit by wall sconces; \"\n")
rep("one hand resting on the chair arm at the lower edge. ", "the cuff of his scarlet sleeve and the back of one relaxed hand rest on the chair arm at the lower right edge, cut off by the frame edge, holding nothing. ")
rep('"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "',
    '"One king only, natural light rouge. Clean picture with no text or lettering, no modern objects, only gold, velvet, lace and candles of the 1680s. "')
i = s.index('"""', 3)
doc = ('"""Take 7 piece 7a START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Setup S16 (in front and slightly right below eye level, wide, hall on the right; leaned back, chin raised, eyes up-right at the hall). '
       'Refs in order: K4_master_neutral_O8.png, K4_angle_34right_O11.png, R10_hall_clean.jpg. Result: pilot_frames/anchors/t7a_start_sunburst_4k.jpg. Run: python3 gen_t7a_start_sunburst.py go\nBRIEF: briefs/brief_t5_t7.md\n"""')
open(H + "gen_t7a_start_" + "sunburst.py", "w").write(doc + s[i + 3:])
print("built")
