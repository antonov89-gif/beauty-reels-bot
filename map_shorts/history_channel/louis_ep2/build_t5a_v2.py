"""Builds the v2 clip script of piece 5a (owner 07.11: 'Переделать') from the v1 script, applying the clip-inspector and reference-comparator findings of v1: eyes stay OPEN on the look at the ceiling, visible torso and left-hand motion, delight with closed eyes only 9.0-9.8 s, operator's thumb only 8.5-9.1 s, camera lower. Output pilot_frames/TAKE_t5a_seedance_v2.mp4."""
import os, re
H = os.path.dirname(os.path.abspath(__file__)) + "/"
src = open(H + "gen_take_t5a_" + "seedance.py").read()
s = src

def rep(old, new):
    global s
    assert old in s, old[:60]
    s = s.replace(old, new)

rep("very low at the near corner of the long table looking along it. ",
    "very low at the near corner of the long table looking along it, the lens about 15 centimetres above the tablecloth, the edge of the tablecloth and the dishes fill the bottom 15 percent of the frame. ")
rep("his eyes roll up to the ceiling for 0.4 s, a short breath through the nose, brows up, then his eyes return to the lens with an amused surrender, both shoulders give a small shrug at 3.2 s; ",
    "his eyes stay OPEN and look up to the ceiling for 0.4 s, the lids never close, a short breath through the nose, brows up, then his eyes return to the lens with an amused surrender, both shoulders lift visibly by about 3 centimetres at 3.2 s and his torso rocks back a little; ")
rep("the other hand rests on the cloth beside the dish of peas; at 1.5 s",
    "the other hand rests on the cloth beside the dish of peas and at 3 s and again at 7 s it lifts and drums its fingers on the cloth; at 1.5 s")
rep("two fingers pick up ONE pea and lift it toward the lens; ",
    "two fingers pick up ONE pea and lift it toward the lens, his torso leans 3 centimetres toward the pea at 6 s; ")
rep("the pea goes into his mouth, his eyes close for at most 0.8 s in delight, the head tips back 5 degrees, then his eyes OPEN again, a closed-lip chew, one corner of the mouth up, a happy hum; ",
    "at 9.0 s the pea goes into his mouth, from 9.0 to 9.8 s his eyes are closed in delight and the head tips back 5 degrees, at 9.8 s his eyes OPEN again and stay open, a closed-lip chew, one corner of the mouth up, a happy hum, his torso leans back at 9 s; ")
rep("in the last second his eyes drift down and to the right to the next dish; ",
    "at 10.5 s his eyes drift down and to the right to the next dish, at 11.3 s they glance into the lens; ")
rep("the tip of Marcel's thumb enters at the bottom right edge, 12 percent of the width, for 0.6 s, far from the face and from the pea hand; ",
    "the tip of Marcel's thumb enters at the bottom right edge, 12 percent of the width, from 8.5 to 9.1 s only, then it leaves the frame and the bottom edge stays clear for the rest of the clip, far from the face and from the pea hand; ")
rep("POSE SCORE as verbs: count, shrug, roll eyes, lift, pick, hold, look, tilt, eat, close eyes briefly, open, hum, glance; ",
    "POSE SCORE as verbs: count, shrug, look up, drum, lift, pick, lean, hold, look, tilt, eat, close eyes briefly, open, hum, glance; ")
rep("Acting limits: the eyes are open except the one delight beat,",
    "Acting limits: the eyes are open at every moment except 9.0 to 9.8 s,")
for a, b in [("take_t5a_seedance_prompt.txt", "take_t5a_seedance_v2_prompt.txt"),
             ("TAKE_t5a_seedance.task_id", "TAKE_t5a_seedance_v2.task_id"),
             ("TAKE_t5a_seedance.status.json", "TAKE_t5a_seedance_v2.status.json"),
             ("TAKE_t5a_seedance.mp4", "TAKE_t5a_seedance_v2.mp4"),
             ("gen_take_t5a_seedance.py", "gen_take_t5a_seedance_v2.py")]:
    s = s.replace(a, b)
i = s.index('"""', 3)
doc = ('"""Take 5 piece 5a CLIP v2 on Seedance 2.5 LITE i2v (owner 07.11: Переделать): first frame ONLY (refs/t5a_start_4k.jpg), 720p, 12 s, 9:16, $0.15/s = $1.80, audio off. '
       'Fixes against v1 (inspector + comparator): eyes stay open on the ceiling look, visible torso and left-hand motion, delight eyes closed only 9.0-9.8 s, operator thumb 8.5-9.1 s, lower camera. '
       'One call, no retries without a new yes. Run: python3 gen_take_t5a_seedance_v2.py go\nBRIEF: briefs/brief_t5_t7.md\n"""')
open(H + "gen_take_t5a_seedance_" + "v2.py", "w").write(doc + s[i + 3:])
print("built")
