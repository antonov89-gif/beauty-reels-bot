"""Writes the gen_*.py scripts (start still, end still, clip) for the REMAINING pieces of ep.2 (06.11, owner: "Составить пока все промпты оставшиеся и проверить"). Nothing is generated and nothing is spent: every script runs only with the argument go, and each go needs its own owner "да" after she has seen the refs and the Russian prompt.
Run: python3 make_remaining_scripts.py   (rewrites gen_<key>_start.py, gen_<key>_end.py, gen_take_<key>.py)"""
import os, re
H0 = os.path.dirname(os.path.abspath(__file__)) + "/"

KING = ("the same king in every frame, always the face and look of the reference: the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, "
        "a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white "
        "(NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat")
MARCEL = ("Marcel exactly as in the reference (his face only; the terrified look is described in words): a young frightened servant with freckles, thick dark brows, a plain white wig and a plain blue livery coat, nothing of the king's red coat or tall silver wig")
HALL_NOTE = ("Reference 2 shows only the hall: ignore its angle, and do NOT copy its crystal glasses or the people at its table; ")
ENDQ = ("QUALITY: keep the full resolution, sharpness and fine detail of the original photo: the face, the moustache hairs, the wig curls, the lace and the gold embroidery must stay exactly as crisp and detailed as in the photo; "
        "no smoothing, no blur, no softening, no painted or mottled texture on the skin; natural detail, no over-sharpening, no halos. Real phone footage, fine film grain, real skin texture, no beauty filter. "
        "No text, no logos, no modern objects, no extra fingers, only one king.")
STILLQ = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. ")
STILLTAIL = " No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king."
CLIPHEAD = ("@first_frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. ")
CLIPTAIL = ("Acting limits: heavy eyelids stay except in the laugh beats, no wide-open eyes for the king, the face stays natural, hands have five natural fingers. "
            "No whip pans and no zoom lens, all moves by hand; no gimbal, no dolly or flying camera. "
            "Sound: only diegetic, low murmur of a large hall, fabric, cutlery, candle flicker, his voice and breath; no music at all. "
            "No text or captions, no modern objects, no clear glass or crystal glass anywhere, only one king in the frame (no second king, no double).")

P = {}

# ---------------------------------------------------------------- Take 4, piece 4b-2: Marcel through the wine (S10)
P["t4b2"] = dict(
    title="Take 4 piece 4b-2 Marcel through the wine (setup S10)", sec=8,
    lines='LOUIS (off screen): "And nobody will see you again." [Marcel freezes; pause] "Joking." MARCEL (quietly): "Sorry, Sire."',
    refs=["R8_marcel_full.jpg", "R10_hall_clean.jpg"],
    start=(STILLQ + "Reference 1 is Marcel (a full-figure card: use only his face, wig and costume, not its pose or background): " + MARCEL + ". Do not copy its pose or background. " + HALL_NOTE +
           "Camera: the king's own phone seen from where the king sits, a little LOW looking up at the standing Marcel from about 15 degrees below his eye level, hand-held, rolled about 6 degrees to the right, close: Marcel's face fills about 52 percent of the frame width, his face centre at about 54 percent of the frame width, blue livery coat and a strip of white lace at the lower edge, the top of the white wig cropped a little by the top edge. "
           "A deep red wine film is on the LEFT THIRD of the lens (thick dark irregular curved edge between 25 and 33 percent of the frame width, thin and transparent inside with runs and drops, never touching Marcel's face), the right two thirds sharp. "
           "Pose and emotion: Marcel stands rigid and pale, lips pressed together, eyes on the lens, a bead of sweat at the temple, terrified but trying to look calm; both arms down at his sides, not visible. "
           "Behind him, blurred: the candlelit gilded hall, standing courtiers in plain wigs, at the back right a lady with an open fan, at the left behind the wine film a servant in livery; no chandelier." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same camera position, the same low angle, the same roll, the same framing and crop, the same head size and head position (face centre at 54 percent of the frame width), the same white wig, the same blue livery coat and lace, the same hall behind, and the same wine film on the left third of the lens (same edge, same drops). "
         "Keep Marcel's face, freckles, thick brows, age and skin EXACTLY (do not redraw his identity). Change ONLY his expression and head: he has just heard 'Joking' and is relieved but shaken, saying quietly 'Sorry, Sire': the head bowed forward about 8 degrees with the chin tucked, the eyes looking up into the lens under raised brows, a tiny trembling forced half-smile, the lips slightly parted in the middle of a word, the shoulders dropped a little; the head, the top of the wig and the face centre stay within 3 percent of the photo. " + ENDQ),
    clip=("{HEAD}{MARCEL}, in the same candlelit gilded hall, filmed on the king's own hand-held phone from a seated eye level, looking slightly up at Marcel, a red wine film on the left third of the lens that stays there all the time (it never grows past 35 percent of the width and never touches Marcel's face). "
          "At the end, 8 s, the frame is exactly as @last_frame (Marcel bowed a little, relieved, mid-word 'Sorry, Sire'); the room and Marcel are in the same place in both frames. Realistic live action, real skin texture, no beauty filter. The king never appears: his voice is off screen and the lens is his. "
          "0-1 s: Marcel stands rigid and pale, lips pressed, eyes on the lens, a bead of sweat at his temple; at 0.5 s his eyes flick to the left toward the wine film and back; behind him at the right back the lady with the fan stops fanning and turns her head toward him. "
          "1-3.3 s: the king's voice says off screen, flat and quiet: \"And nobody will see you again.\" Marcel's eyes widen a little and his throat swallows at 2 s, his breathing quickens, his lips tremble once, the rest of him does not move; at 2 s a courtier behind his right shoulder glances at him and away. "
          "3.3-4.6 s: the silent beat of one and a half seconds: Marcel freezes completely, only one eyelid twitches and the sweat bead runs down; the candle flames flicker; the camera keeps moving. "
          "4.6-5.4 s: the king's voice, light: \"Joking.\" and a short exhale of a laugh; Marcel's shoulders drop and the breath leaves him, the head bowing forward. "
          "5.4-6.8 s: Marcel says very quietly, his lips moving: \"Sorry, Sire.\" while bowing his head forward about 8 degrees and looking up into the lens, a trembling half-smile. "
          "6.8-8 s: he straightens a little and glances away to the right at the courtier, then back at the lens, the frame settling to @last_frame. "
          "CAMERA SCORE in absolute amounts (the king's own phone in one hand; Marcel and the room stay in place while the frame moves; Marcel's face is at 52 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 20 percent on each side): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a slow drift to the right by 8 percent with the roll easing by 3 degrees and a push-in of 5 percent; 2-4 s a small push-in and a shake of the king's hand as he speaks, then a sag to the left by 8 percent; 4-5 s the phone jerks up and comes back as he laughs; 5-7 s a slow sway to the right by 8 percent and a tilt down by 4 degrees; at about 5.5 s (the allowed window is 3.5 to 7.5 s) the king's own pink thumb slips into the lower right corner covering the lower right 20 percent of the frame width (never more than 25 percent) for 0.7 s and never Marcel's face (phone mistake); 7-8 s a last small sway back to the framing of @last_frame. "
          "POSE SCORE as verbs: stiffen, flick, swallow, tremble, freeze, twitch, exhale, bow, glance; Marcel's head moves about a third of its own width (about 17 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; never a stillness of the camera longer than 2 seconds. "
          "THE ROOM IS ALIVE: candle flames flicker; at 1 s the lady with the fan at the right back turns her head; at 2 s the courtier behind Marcel's right shoulder glances at him; at 6 s a servant behind the wine film walks across from left to right. "
          "{TAIL}")
)

# ---------------------------------------------------------------- Take 5a: peas (S11)
P["t5a"] = dict(
    title="Take 5 piece 5a salad, ham, pastry, fruit, peas (setup S11)", sec=12,
    lines='LOUIS: "Then salad, ham, pastry, fruit. [gives up counting] In under an hour. [holds a pea to the lens, softly] And peas. The court talks of nothing else. [eats it, delighted]"',
    refs=["R1_king_card_A3_white_wig.jpg", "R10_hall_clean.jpg"],
    start=(STILLQ + "Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white like the pale grey in reference 1, NOT beige, NOT cream, NOT golden, the candlelight must not tint it, the scarlet velvet coat with gold suns, lace cravat; do not copy its pose or background. " + HALL_NOTE +
           "Camera (filmed by Marcel): LOW, from the near corner at the END of the long table, the lens only about 25 centimetres above the tablecloth, looking along the table toward the king who sits at its far end; NOT across the table and NOT from above, rolled about 10 degrees to the left. In the foreground, soft and out of focus at the lower edge and the right edge: a silver platter with a glazed ham, a pyramid of small pastries, a dish of fruit and a tureen of green peas (all food on the table, plates and gold dishes only). The king sits at the far end, his face fills about 42 percent of the frame width with its centre at 60 percent of the frame width, sharp, turned three-quarter toward the lens, napkin tucked into the lace cravat. "
           "Pose and emotion: he is counting the dishes on his fingers, just giving up, with a tolerant amused look, heavy lids half-lowered, lips closed in a faint smirk, one hand raised showing a few fingers; the other hand rests on the cloth. Behind him: the candlelit gilded hall, standing courtiers in plain wigs, at the back left a lady with an open fan, a servant in livery far behind at the right; no chandelier." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same camera position, the same low angle along the table, the same roll, the same framing and crop, the same food in the foreground, the same head size and head position (the face centre at 60 percent of the frame width), the same wig, the same coat and napkin, the same hall behind. "
         "Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); the wig keeps its cool silver-grey and white. "
         "Change ONLY the pose and expression: he now holds a single green pea between his thumb and forefinger toward the lens (the hand at about the height of his chin, the pea clearly visible), the other hand lowered out of frame; the head tilted forward about 6 degrees with the chin down, the eyes looking at the pea and then at the lens under heavy lids, a soft delighted half-smile with the lips closed; the head, the top of the wig and the face centre stay within 3 percent of the photo. " + ENDQ),
    clip=("{HEAD}{KING}, the candlelit gilded hall behind him, filmed by Marcel with a hand-held phone held very low at the near corner of the long table looking along it; the foreground food (ham, pastries, fruit, a tureen of peas) soft at the edges. At the end, 12 s, the frame is exactly as @last_frame (he holds a green pea to the lens, a soft delighted half-smile); the king and the room are in the same place in both frames. Realistic live action, real skin texture, no beauty filter. "
          "0-2.5 s: he counts the dishes on his raised fingers with small nods, then shrugs and lets the hand fall: \"Then salad, ham, pastry, fruit.\" at 2.5 s he gives up counting with a tolerant sigh; at 1 s a servant in livery at the right back bends to move a dish. "
          "2.5-5 s: \"In under an hour.\" he lifts his chin proudly, then glances down along the table at the food; at 4 s the lady with the fan at the left back leans to whisper to her neighbour. "
          "5-7 s: a silent beat of two seconds: he reaches toward the tureen with two fingers and picks up one pea, looking at it tenderly; the camera keeps moving. "
          "7-9.5 s: he lifts the pea toward the lens, softly: \"And peas.\" then leans a little toward the lens with raised brows: \"The court talks of nothing else.\" "
          "9.5-12 s: he eats the pea, closes his eyes and hums with delight, the head tipping back a little, then settles into the pose of @last_frame with the pea back between his fingers; at 10 s a courtier behind him nods approvingly. "
          "CAMERA SCORE in absolute amounts (Marcel's phone, low and hand-held; the king and the room stay in place while the frame moves; the king's face is at 42 percent of the width so every move keeps his face and wig inside the frame, the free margin is about 25 percent on each side): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a slow creep along the table toward the king, a push-in of 6 percent and the roll easing by 3 degrees; 2-4 s a drift to the right by 9 percent over the food; 4-6 s a dip lower by 5 percent and a sag, then a lift; 6-8 s a push-in of 8 percent toward the pea as it rises; at about 7 s (the allowed window is 5 to 9 s) the focus hunts: the picture goes soft for half a second and snaps back sharp; 8-10 s a sway to the left by 8 percent; at about 10.5 s (the allowed window is 8.5 to 11.5 s) Marcel's sleeve of blue brushes the left edge of the lens for 0.6 s; 10-12 s the frame settles back to the framing of @last_frame. "
          "POSE SCORE as verbs: count, nod, shrug, lift, glance, reach, pick, lift, lean, eat, hum; the head moves about half of its own width (about 20 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; never a hold longer than 2 seconds. "
          "THE ROOM IS ALIVE: candle flames flicker; at 1 s the servant at the right back bends to a dish; at 4 s the lady with the fan whispers to her neighbour; at 8 s a courtier behind the king's left shoulder shifts his weight; at 10 s a courtier nods. "
          "{TAIL}")
)

# ---------------------------------------------------------------- Take 5b: the laden table (S11b)
P["t5b"] = dict(
    title="Take 5 piece 5b Marcel films the laden table and the king eating (no words)", sec=5,
    lines="[Marcel films the laden table and the king eating, about 4 s, no words: chewing, a happy hum, the murmur of the crowd]",
    refs=["R1_king_card_A3_white_wig.jpg", "R10_hall_clean.jpg"],
    start=(STILLQ + "Reference 1 is the king's face and costume: exactly the same man, heavy-lidded eyes, thin dark waxed moustache with curled tips, the beauty mark on the viewer's right of the mouth, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns; do not copy its pose. " + HALL_NOTE +
           "Camera (filmed by Marcel): hand-held, held a little ABOVE the dishes and tilted down about 25 degrees, a medium-close look at the laden table: in sharp focus in the foreground a gold platter of roast pheasant, a ham, a pyramid of pastries, a bowl of fruit and a gold dish of peas, all heaped, plates and gold dishes only; the king sits far behind them at the top of the frame, small and softly out of focus (his face about 14 percent of the frame width, centre at 45 percent), chewing, a napkin in his cravat; rolled about 7 degrees to the right. Behind him the candlelit hall, standing courtiers in plain wigs, at the back left a lady with a fan, no chandelier." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same hall, table, dishes and food positions, the same wig and coat; change ONLY the camera and the king: the camera has tilted UP about 20 degrees and moved in a little, so that now the king is the subject, sharp, his face filling about 46 percent of the frame width (centre at 50 percent), the food now soft at the lower edge; his cheeks full of food, chewing happily with a closed mouth, eyes closed under heavy lids in bliss, one hand holding a golden spoon near the lower edge. "
         "Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); the wig keeps its cool silver-grey and white. " + ENDQ),
    clip=("{HEAD}{KING}, far at the top behind the laden table in the first frame; filmed by Marcel on a hand-held phone in the candlelit gilded hall. At the end, 5 s, the frame is exactly as @last_frame (the camera has tilted up and moved in on the sharp, chewing king). Realistic live action, real skin texture. No spoken words: only chewing, a happy hum and the murmur of the crowd. "
          "0-1.5 s: the camera lingers on the heaped dishes in sharp focus, the king chews far behind, a servant in livery at the right edge places one more dish; "
          "1.5-3.5 s: the camera tilts up and pushes in, the focus hunts for half a second at about 2 s and then pulls to the king; he chews with relish, closes his eyes in bliss and hums; "
          "3.5-5 s: the frame settles on the king as in @last_frame, a satisfied small nod while chewing; behind him the lady with the fan fans herself and a courtier watches him eat. "
          "CAMERA SCORE in absolute amounts: every 2 seconds the frame moves by 8 to 10 percent of its width: 0-2 s a slow drift to the left by 8 percent and a roll easing by 3 degrees; 2-4 s a tilt up of 20 degrees with a push-in of 9 percent and a re-aim to the right by 6 percent; at about 2 s a focus hunt; 4-5 s a small sway and settle to the framing of @last_frame; at about 4 s (the allowed window is 2.5 to 4.5 s) Marcel's blue sleeve brushes the lower left of the lens for 0.5 s. "
          "POSE SCORE as verbs: chew, hum, close, nod, swallow; the king's head moves about a third of its own width in each 2-second window and ends near the centre. "
          "THE ROOM IS ALIVE: candle flames flicker; at 1 s a servant at the right edge sets down a dish; at 3 s the lady with the fan turns her head toward the king; at 4 s a courtier behind him shifts his weight. "
          "{TAIL}")
)

# ---------------------------------------------------------------- Take 5c: "I wasn't born to work" (S12)
P["t5c"] = dict(
    title="Take 5 piece 5c Ohh, I wasn't born to work (setup S12, from above)", sec=12,
    lines='LOUIS (OWNER): "[leans back, hands on the belly, a long happy sigh] Ohh... I wasn\'t born to work. I was born for happiness, love, pleasure... and a good rest. [a joyful laugh at his own line]"',
    refs=["R1_king_card_A3_white_wig.jpg"],
    start=(STILLQ + "Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; do not copy its pose or background. "
           "Camera: the king's own arm's-length phone held HIGH and slightly behind and above his head, looking DOWN at his face from about 55 degrees above as he leans back in a gilded armchair (a high angle, never eye level), rolled about 8 degrees to the right; his face fills about 52 percent of the frame width with its centre at 50 percent, the top of the wig at the top edge, the chin and the lace cravat in the lower middle, sharp. "
           "Pose and emotion: he has just leaned back into the carved gilded armchair, the head resting against its back, the eyes closed under heavy lids in a long happy sigh, the lips parted a little, a deeply contented face; both hands rest on his belly over the scarlet coat, five natural fingers each, at the lower edge. Around the edges of the frame: the carved gilded armchair top and the candlelit gilded hall blurred, no chandelier, no glass on the table, nobody close." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same camera position, the same high angle, the same roll, the same framing and crop, the same head size and head position (the face centre at 50 percent of the frame width), the same wig, the coat, the armchair and the hall. "
         "Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); the wig keeps its cool silver-grey and white. "
         "Change ONLY the expression and the hands: he is laughing joyfully at his own line, the head tipped back a few degrees into the armchair, the eyes squeezed shut, one eyebrow up, laugh creases, the mouth open in a big happy laugh with the upper teeth visible, natural and slightly uneven; the hands have moved up and one rests flat on his chest on the lace cravat, the other still on his belly; the head, the top of the wig and the face centre stay within 3 percent of the photo. " + ENDQ),
    clip=("{HEAD}{KING}, in a carved gilded armchair in the candlelit gilded hall, his own hand-held phone held high above and slightly behind his head, looking down at his face. At the end, 12 s, the frame is exactly as @last_frame (he laughs joyfully, one hand on his chest); the king and the room are in the same place in both frames. Realistic live action, real skin texture, no beauty filter. "
          "0-2.5 s: his eyes closed, he lets out a long happy sigh, his chest rising and falling, his fingers drumming softly on his belly: \"Ohh...\" "
          "2.5-6 s: he opens his eyes under heavy lids, looks up lazily into the lens and says dreamily: \"I wasn't born to work.\" with a small slow shake of the head; at 4 s he rolls his head to the left to look at the court, then back; "
          "6-9 s: \"I was born for happiness, love, pleasure...\" his eyes drift up and away as if remembering, a soft smile; a silent beat of one second after \"pleasure\" at 8 s with a lazy blink; "
          "9-10.5 s: \"...and a good rest.\" he closes his eyes again and sinks deeper into the armchair; "
          "10.5-12 s: a joyful laugh at his own line: the head tips back, the shoulders shake, one hand rises to his chest, settling into the pose of @last_frame. "
          "CAMERA SCORE in absolute amounts (his own hand-held phone high above; the king and the room stay in place while the frame moves; his face is at 52 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 22 percent on each side): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a slow drift to the right by 8 percent and a push-in of 5 percent; 2-4 s a sway to the left by 8 percent with the roll easing by 3 degrees; 4-6 s a dip down toward his chin by 5 percent and a lift; 6-8 s a drift to the right by 9 percent; at about 8 s (the allowed window is 6 to 10 s) his own pink thumb slips into the lower left corner covering the lower left 20 percent of the frame width (never more than 25 percent) for 0.7 s and never his face (phone mistake); 8-10 s a small push-back of 5 percent; 10-12 s the shake of his laughter by 8 percent, then settling to the framing of @last_frame. "
          "POSE SCORE as verbs: sigh, drum, open, roll, drift, blink, sink, laugh; the head moves about half of its own width (about 18 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; never a hold longer than 2.5 seconds (the silent beat at 8 s keeps the camera moving). "
          "THE ROOM IS ALIVE: candle flames flicker; at the edge of the frame at 3 s a servant in livery crosses from right to left far below; at 5 s a courtier's powdered wig edge and shoulder at the right edge shifts; at 9 s the lady with the fan, small at the lower left, fans faster. "
          "{TAIL}")
)

# ---------------------------------------------------------------- Take 6: the verdict (S13)
P["t6"] = dict(
    title="Take 6 the verdict (setup S13, frontal close, slow push-in)", sec=12,
    lines='LOUIS (OWNER): "[wipes his fingers, sits up, glances at the bones on his plate, pushes the plate a little away] So. Do I eat too much? ...No. I eat like a king. [chin up] Don\'t be afraid of getting fat. Be afraid of being a loser. [haughty laugh]"',
    refs=["R1_king_card_A3_white_wig.jpg", "R10_hall_clean.jpg"],
    start=(STILLQ + "Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; do not copy its pose or background. " + HALL_NOTE +
           "Camera: hand-held at arm's length at EYE LEVEL, frontal, close: his face fills about 56 percent of the frame width with its centre at 50 percent of the frame width, the wig top slightly cropped, sharp; a slight roll of about 4 degrees to the left; at the lower edge a gold plate with a few clean chicken bones and a crumpled white napkin, soft. "
           "Pose and emotion: he is wiping his fingers on a lace napkin held in one hand just below the frame, his chin slightly lowered, his heavy-lidded eyes looking down at the bones on the plate with a complacent faint smirk, the lips closed. Behind him, blurred: the candlelit gilded hall, standing courtiers in plain wigs, at the back left a lady with a fan, no chandelier." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same camera position, the same eye-level frontal angle, the same roll, the same framing and crop, the same head size and head position (the face centre at 50 percent of the frame width), the same wig, the coat and the hall; the gold plate with the bones has been pushed a little away toward the right of the lower edge. "
         "Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); the wig keeps its cool silver-grey and white. "
         "Change ONLY the pose and expression: the chin lifted high, the head tipped back a few degrees, looking down his nose into the lens with a haughty look under heavy lids, laughing a haughty short laugh with the mouth open slightly and the upper teeth just showing, one eyebrow raised; the head, the top of the wig and the face centre stay within 3 percent of the photo. " + ENDQ),
    clip=("{HEAD}{KING}, the candlelit gilded hall behind him, his own hand-held phone at eye level, frontal and close, slowly pushing in. At the end, 12 s, the frame is exactly as @last_frame (chin up, a haughty laugh, the plate pushed a little away); the king and the room are in the same place in both frames. Realistic live action, real skin texture, no beauty filter. "
          "0-2 s: he wipes his fingers on the lace napkin, glances down at the bones on the plate with a complacent smirk, then sits up straighter; "
          "2-3.5 s: he pushes the plate a little away with two fingers and looks into the lens: \"So.\" a short pause, then \"Do I eat too much?\" with a raised eyebrow; at 3 s the lady with the fan at the left back turns her head; "
          "3.5-5.5 s: the silent beat of one and a half seconds: he lets the question hang, looking at the court with a slow blink, then back; the camera keeps moving; "
          "5.5-8 s: \"...No. I eat like a king.\" the chin rising slowly; "
          "8-10.5 s: \"Don't be afraid of getting fat. Be afraid of being a loser.\" he says it softly and flatly, the eyes half closed, a small contemptuous head tilt to the left; at 9 s a courtier behind his right shoulder bows his head slightly; "
          "10.5-12 s: the haughty laugh, the chin up, settling into the pose of @last_frame. "
          "CAMERA SCORE in absolute amounts (his own hand-held phone; the king and the room stay in place while the frame moves; his face is at 56 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 20 percent on each side): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a slow push-in of 6 percent and a drift to the left by 8 percent with the roll easing by 3 degrees; 2-4 s a sway to the right by 9 percent; 4-6 s a sag down by 5 percent and a lift while the roll swings the other way by 4 degrees; at about 5 s (the allowed window is 3 to 7 s) the focus hunts: the picture goes soft for half a second and snaps back sharp; 6-8 s a drift to the left by 8 percent with a push-in of 5 percent; at about 9 s (the allowed window is 7 to 11 s) his own pink thumb slips into the lower right corner covering the lower right 20 percent of the frame width (never more than 25 percent) for 0.7 s and never his face; 8-10 s a sway to the right; 10-12 s a small push-back and the haughty laugh shake of 8 percent, settling to the framing of @last_frame. "
          "POSE SCORE as verbs: wipe, glance, sit up, push, lift, blink, tilt, bow, laugh; the head moves about half of its own width (about 20 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; never a hold longer than 2 seconds. "
          "THE ROOM IS ALIVE: candle flames flicker; at 3 s the lady with the fan turns her head; at 6 s a servant in livery far behind on the right crosses from right to left; at 9 s the courtier behind his right shoulder bows his head. "
          "{TAIL}")
)

# ---------------------------------------------------------------- Take 7a: "what else to show you" (S13b)
P["t7a"] = dict(
    title="Take 7 piece 7a I was wondering what else to show you (setup S16, three-quarter right)", sec=10,
    lines='LOUIS (OWNER): "[leans back, thinks, looks around the hall] So... I was wondering what else to show you here. [pause, a short laugh] Ha. Probably... nothing."',
    refs=["R1_king_card_A3_white_wig.jpg", "R10_hall_clean.jpg"],
    start=(STILLQ + "Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; do not copy its pose or background. " + HALL_NOTE +
           "Camera: hand-held, held at arm's length a little BELOW his eye level and to his left, wide lens, so that the hall can be seen: his face fills about 40 percent of the frame width with its centre at 42 percent (a little left of centre), turned three-quarter toward the viewer's right; to the right of him a wide view of the candlelit gilded hall with standing courtiers in plain wigs and ladies in wide gowns at the sides of the table, at the back right a lady with an open fan, a servant in livery far behind, a strip of the gilded ceiling at the top edge; no chandelier; rolled about 5 degrees to the right. "
           "Pose and emotion: he has leaned back in the armchair, his chin raised, thoughtful, his heavy-lidded eyes looking up and away to the right at the hall as if searching for an idea, the lips closed and pursed a little; one hand resting on the chair arm at the lower edge." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same camera position, the same angle, the same roll, the same framing and crop, the same head size and head position (the face centre at 42 percent of the frame width), the same wig, the coat and the hall with the people. "
         "Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); the wig keeps its cool silver-grey and white. "
         "Change ONLY the expression: his eyes are back on the lens and he has just said 'probably nothing' and is giving a short dry laugh, the mouth slightly open with a smirk, the upper teeth just visible, one eyebrow raised, the head tipped a few degrees toward the viewer's left; the head, the top of the wig and the face centre stay within 3 percent of the photo. " + ENDQ),
    clip=("{HEAD}{KING}, leaning back in the candlelit gilded hall, filmed by his own hand-held phone held below eye level so that the hall behind him is visible. At the end, 10 s, the frame is exactly as @last_frame (a short dry laugh, the eyes on the lens); the king and the room are in the same place in both frames. Realistic live action, real skin texture, no beauty filter. "
          "0-2.5 s: he leans back, looks slowly around the hall from right to left, thoughtful, the lips pursed; "
          "2.5-5.5 s: he brings his eyes to the lens: \"So... I was wondering what else to show you here.\" with a small frown and a tilt of the head to the right; at 4 s a lady at the back right closes her fan; "
          "5.5-7 s: the silent beat of one and a half seconds: he looks around the hall again and the corners of his mouth rise; the camera keeps moving; "
          "7-8.5 s: a short dry laugh: \"Ha.\" with a small shoulder shake; "
          "8.5-10 s: \"Probably... nothing.\" lightly, with a shrug of one shoulder, settling into the pose of @last_frame. "
          "CAMERA SCORE in absolute amounts (his own hand-held phone; the king and the room stay in place while the frame moves; his face is at 40 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 30 percent on each side): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a slow swing to the right by 10 percent following his gaze and a roll easing by 3 degrees; 2-4 s a swing back to the left by 9 percent with a push-in of 5 percent; 4-6 s a sag down by 5 percent and a lift; at about 5 s (the allowed window is 3 to 7 s) the phone tilts up to the ceiling for half a second and comes back; 6-8 s a drift to the right by 8 percent; at about 8.5 s (the allowed window is 6.5 to 9.5 s) his own pink thumb slips into the lower left corner covering the lower left 20 percent of the frame width (never more than 25 percent) for 0.6 s and never his face; 8-10 s a small push-in and settle to the framing of @last_frame. "
          "POSE SCORE as verbs: lean, scan, frown, tilt, glance, smirk, laugh, shrug; the head moves about half of its own width (about 15 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; never a hold longer than 2 seconds. "
          "THE ROOM IS ALIVE: candle flames flicker; at 1 s a servant in livery far behind crosses from left to right; at 3 s a courtier at the right edge of the table turns to his neighbour; at 4 s the lady at the back right closes her fan; at 7 s a courtier shifts his weight. "
          "{TAIL}")
)

# ---------------------------------------------------------------- Take 7b: he stands, the crowd bows, the end (S14)
P["t7b"] = dict(
    title="Take 7 piece 7b he stands, the crowd bows, bye, subscribe (setup S14, low swing up)", sec=14,
    lines='LOUIS (OWNER): "[stands up, the crowd bows] That\'s all. Bye. I\'m busy. [beat, points at the lens] ...And you: subscribe to my stunning channel. And like. [pause, a lazy wave of the hand, he looks away, bored] Or... whatever." Hard cut on "Or... whatever." to the end card.',
    refs=["R1_king_card_A3_white_wig.jpg", "R10_hall_clean.jpg"],
    start=(STILLQ + "Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; do not copy its pose or background. " + HALL_NOTE +
           "Camera: his own phone in his outstretched hand held LOW, near the level of the table, looking UP at him as he rises from the gilded armchair: a low angle of about 30 degrees from below, wide lens, rolled about 8 degrees to the left; his face fills about 44 percent of the frame width with its centre at 50 percent, sharp, his chin raised; behind and above him the gilded ceiling edge and the candlelit hall; no chandelier. "
           "Pose and emotion: he is half risen, one hand pressing on the white tablecloth at the lower edge (five natural fingers), the look haughty and bored under heavy lids, the lips closed in a faint smirk; behind him at both sides the courtiers in plain wigs and the ladies in wide gowns are just starting to bow, their heads dipping at different depths." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same camera position, the same low angle, the same roll, the same framing and crop, the same head size and head position (the face centre at 50 percent of the frame width), the same wig, the coat and the hall. "
         "Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); the wig keeps its cool silver-grey and white. "
         "Change ONLY the pose and the crowd: he now stands fully upright, the head a little higher in the frame, looking away to the viewer's left with a bored expression under heavy lids, the chin up; one hand raised to the right of the frame at shoulder height in a lazy wave, the fingers loose, five natural fingers; the courtiers and the ladies behind him are now all bowing deeply, their heads low; the head, the top of the wig and the face centre stay within 4 percent of the photo. " + ENDQ),
    clip=("{HEAD}{KING}, rising from his gilded armchair in the candlelit gilded hall, filmed by his own hand-held phone held low and swinging up with him; the courtiers and ladies behind him bow. At the end, 14 s, the frame is exactly as @last_frame (he stands, a lazy wave, looking away bored, the crowd bowing deeply); the king and the room are in the same place in both frames. Realistic live action, real skin texture, no beauty filter. "
          "0-2.5 s: he rises from the armchair, the camera rising with him; behind him the courtiers begin to bow, one lady at the left curtsies; "
          "2.5-5.5 s: \"That's all. Bye. I'm busy.\" he says with a bored sigh, looking down at the lens from above; at 4 s a courtier on the right bows lowest of all; "
          "5.5-7.5 s: the silent beat of one and a half seconds: he lets the bowing crowd hold, glancing over them with satisfaction; the camera keeps moving; "
          "7.5-9.5 s: he points a finger at the lens, with a small lift of the eyebrow: \"...And you:\" "
          "9.5-12 s: \"subscribe to my stunning channel. And like.\" he nods slowly, smug; "
          "12-14 s: a silent pause, a lazy wave of the hand, he looks away to the side, bored: \"Or... whatever.\" and the frame settles to the pose of @last_frame. "
          "CAMERA SCORE in absolute amounts (his own hand-held phone; the king and the room stay in place while the frame moves; his face is at 44 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 28 percent on each side): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a swing up with his rising of 10 percent with the roll easing by 4 degrees; 2-4 s a drift to the right by 9 percent and a push-in of 5 percent; 4-6 s a sway to the left by 8 percent; at about 6 s (the allowed window is 4 to 8 s) the focus hunts for half a second; 6-8 s a push-in of 6 percent as he points; 8-10 s a drift to the right by 8 percent; at about 10 s (the allowed window is 8 to 12 s) his own pink thumb slips into the lower right corner covering the lower right 20 percent of the frame width (never more than 25 percent) for 0.7 s and never his face; 10-12 s a sag and a lift; 12-14 s a sway to the left by 8 percent and settle to the framing of @last_frame. "
          "POSE SCORE as verbs: rise, sigh, glance, point, nod, wave, look away; the head moves about half of its own width (about 20 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; never a hold longer than 2 seconds. "
          "THE ROOM IS ALIVE: candle flames flicker; at 1 s the lady at the left curtsies; at 3 s the courtiers on both sides dip their heads; at 4 s a courtier on the right bows lowest; at 6 s a servant behind the crowd lowers his tray; at 11 s a child page at the right peeks up and is pushed down by a hand. "
          "{TAIL}")
)

# ---------------------------------------------------------------- Take 1 new setups (viewer: split the 37 s single pose)
P["t1na"] = dict(
    title="Take 1 NEW piece 1a: Is it on / Ah there I am / Bonjour / Welcome to Versailles (setup S1, extreme low selfie)", sec=12,
    lines='LOUIS: "[phone too close, muffled] Is it... is it on? [pulls it back, sees himself, pleased] Ah. There I am. [clears throat] Bonjour. I am Louis, King of France. Welcome to Versailles."',
    refs=["R1_king_card_A3_white_wig.jpg"],
    start=(STILLQ + "Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; do not copy its pose or background. "
           "Camera: his own phone held far too close and LOW, an extreme low selfie from under his chin looking up at about 50 degrees, wide lens, rolled about 12 degrees to the left: his face fills about 80 percent of the frame width, foreshortened from below, the chin and the underside of the moustache nearest the lens, the tall wig cropped by the top edge, behind and above him the painted ceiling of a gilded palace hall with soft cloud and sky paintings and a gold cornice, candlelit; his pink thumb and the edge of the phone case are visible at the lower right corner; the face is still sharp and readable. "
           "Pose and emotion: he is squinting at the phone screen with a puzzled frown, heavy lids half-lowered, one eyebrow raised, the lips slightly parted as he mumbles 'is it on'." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same low selfie angle from under the chin, the same roll, the same ceiling and cornice behind, the same wig, coat and cravat. "
         "Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); the wig keeps its cool silver-grey and white. "
         "Change ONLY the distance and the expression: the phone has been pulled back, so that his face now fills about 56 percent of the frame width with its centre at 50 percent, more of the painted ceiling and the gold cornice visible above; the thumb is gone from the lower right corner (a strip of the scarlet coat and lace at the lower edge instead); he has seen himself on the screen and is pleased: heavy lids, the eyes now on the lens, the lips closed in a smug faint smile, the chin slightly lifted. " + ENDQ),
    clip=("{HEAD}{KING}, filmed on his own hand-held phone from far too close and low, then pulled back; the painted ceiling and gilded cornice of the candlelit palace hall behind and above him. At the end, 12 s, the frame is exactly as @last_frame (the phone pulled back, he looks pleased into the lens); the king and the room are in the same place in both frames. Realistic live action, real skin texture, no beauty filter. "
          "0-2.5 s: his face huge and low in the lens, squinting at the screen with a frown, muffled: \"Is it... is it on?\" the thumb at the lower right corner fumbles over the screen; "
          "2.5-4.5 s: he pulls the phone back and sees himself; the picture drifts up and down as the focus hunts for half a second; his face brightens: \"Ah. There I am.\" "
          "4.5-6 s: a silent beat of one and a half seconds: he admires himself, smoothing his moustache with one finger; the camera keeps moving; "
          "6-8 s: he clears his throat: \"Hm-hm.\" and straightens: \"Bonjour.\" "
          "8-12 s: \"I am Louis, King of France. Welcome to Versailles.\" the chin rising, the eyes on the lens, settling into the pose of @last_frame. "
          "CAMERA SCORE in absolute amounts (his own hand-held phone; the king and the room stay in place while the frame moves; the face is at 80 percent of the width at the start and 56 percent at the end, so every move keeps the face and wig inside the frame): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a fumbling drift to the left by 9 percent with the roll swinging 4 degrees; 2-4 s the pull-back of about 25 percent of the face size with a drift to the right by 9 percent; at about 3 s the focus hunts for half a second; 4-6 s a sway to the left by 8 percent and a dip; 6-8 s a push-in of 5 percent and a re-centring jerk; at about 7 s (the allowed window is 5 to 9 s) the phone tilts up to the painted ceiling for half a second and comes back; 8-10 s a drift to the right by 8 percent; 10-12 s a small sag and settle to the framing of @last_frame. "
          "POSE SCORE as verbs: squint, frown, pull back, brighten, smooth the moustache, clear the throat, straighten, lift the chin; the head moves about half of its own width in each 2-second window, alternating left and right and ending near the centre; never a hold longer than 2 seconds. "
          "THE ROOM IS ALIVE: candle flames flicker and painted clouds on the ceiling catch the light; at the lower edge at 5 s the head of a courtier in a plain wig passes behind him from right to left; at 9 s a tiny servant's shoulder in livery at the left edge. "
          "{TAIL}")
)

P["t1nb"] = dict(
    title="Take 1 NEW piece 1b: And this is my channel / Sun King / handsome (setup S2, table height, rolled)", sec=10,
    lines='LOUIS: "And this is my channel. They call me the Sun King. Yes... I\'m that handsome. [a satisfied sigh]"',
    refs=["R1_king_card_A3_white_wig.jpg"],
    start=(STILLQ + "Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; do not copy its pose or background. "
           "Camera: his phone propped by hand at TABLE HEIGHT, very close, rolled about 15 degrees to the left (a dutch angle), looking at him three-quarter to the viewer's left: his face fills about 62 percent of the frame width with its centre at 55 percent, the tall silver-grey wig filling the top third of the frame and cropped by the top edge, sharp; at the lower edge the white tablecloth and the corner of a gold plate; behind him, soft and blurred, the candlelit gilded hall with a few courtiers' heads, no chandelier. "
           "Pose and emotion: he gives a smug sideways look at the lens under heavy lids, the chin lifted, one eyebrow raised, the lips closed in a faint proud smile." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same camera position, the same table height, the same roll, the same framing and crop, the same head size and head position (the face centre at 55 percent of the frame width), the same wig, the coat and the hall. "
         "Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); the wig keeps its cool silver-grey and white. "
         "Change ONLY the expression and the head: he is letting out a long satisfied sigh, the eyes closed under heavy lids, the chin lifted higher and the head tipped back about 8 degrees, the lips parted a little, a deeply self-satisfied look; the head, the top of the wig and the face centre stay within 3 percent of the photo. " + ENDQ),
    clip=("{HEAD}{KING}, the candlelit gilded hall behind him, his hand-held phone at table height, very close, rolled. At the end, 10 s, the frame is exactly as @last_frame (a long satisfied sigh, the eyes closed, the chin lifted); the king and the room are in the same place in both frames. Realistic live action, real skin texture, no beauty filter. "
          "0-2.5 s: a smug sideways look at the lens, then to the viewer's left: \"And this is my channel.\" with a small proud nod; "
          "2.5-5 s: \"They call me the Sun King.\" he lifts his chin and rolls his head toward the right; at 3.5 s a courtier behind him leans to his neighbour; "
          "5-6.5 s: a silent beat of one and a half seconds: a slow blink under heavy lids, the lips pressed in a knowing smirk; the camera keeps moving; "
          "6.5-8.5 s: \"Yes... I'm that handsome.\" with a small shrug of his shoulders, deadpan; "
          "8.5-10 s: the satisfied sigh, the eyes closing, the head tipping back, settling into the pose of @last_frame. "
          "CAMERA SCORE in absolute amounts (his hand-held phone at table height; the king and the room stay in place while the frame moves; his face is at 62 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 17 percent on each side): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a slow drift to the right by 8 percent and the roll easing by 3 degrees; 2-4 s a push-in of 5 percent and a sway to the left by 8 percent; 4-6 s the roll swings back by 5 degrees with a small sag; at about 5 s (the allowed window is 3 to 7 s) the focus hunts for half a second and snaps back sharp; 6-8 s a drift to the right by 9 percent; at about 7.5 s (the allowed window is 5.5 to 9 s) his own pink thumb slips into the lower left corner covering the lower left 20 percent of the frame width (never more than 25 percent) for 0.7 s and never his face; 8-10 s a small push-back and settle to the framing of @last_frame. "
          "POSE SCORE as verbs: glance, nod, lift, roll, blink, smirk, shrug, sigh, tip back; the head moves about a half of its own width (about 18 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; never a hold longer than 2 seconds. "
          "THE ROOM IS ALIVE: candle flames flicker; at 1 s a servant in livery far behind crosses from left to right; at 3.5 s the courtier behind him leans to his neighbour; at 6 s a lady's fan flutters at the back right. "
          "{TAIL}")
)

P["t1nc"] = dict(
    title="Take 1 NEW piece 1c: Some of you write that I eat too much ... before your eyes (setup S2b, three-quarter right, arm's length)", sec=14,
    lines='LOUIS: "[a satisfied sigh] Some of you write that I eat too much. I read it. [sniffs] Of course, that\'s not true. Every day I feast in front of the court. Today... before your eyes."',
    refs=["R1_king_card_A3_white_wig.jpg", "R10_hall_clean.jpg"],
    start=(STILLQ + "Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; do not copy its pose or background. " + HALL_NOTE +
           "Camera: his own hand-held phone at arm's length a little ABOVE his eye level and to his left, medium-close, rolled about 6 degrees to the right: his face fills about 50 percent of the frame width with its centre at 46 percent, turned three-quarter toward the viewer's right, sharp; a white napkin tucked into the lace cravat, at the lower edge a gold plate with a few grapes and the white tablecloth; behind him on the right the candlelit gilded hall: the long table with the court seated and standing courtiers in plain wigs, a lady with an open fan at the back, no chandelier. "
           "Pose and emotion: he is reading the comments on an imaginary screen below the lens with a wounded look: heavy lids, the lips pursed, the brows pulled together a little, the head tilted to the viewer's left." + STILLTAIL),
    end=("Edit the photo: keep EXACTLY the same camera position, the same angle, the same roll, the same framing and crop, the same head size and head position (the face centre at 46 percent of the frame width), the same wig, the coat, the napkin and the hall. "
         "Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); the wig keeps its cool silver-grey and white. "
         "Change ONLY the expression and the head: he is now looking straight into the lens with an expansive grand look, the chin lifted, one eyebrow raised, the lips closed in a smug faint smile as if saying 'before your eyes', the head turned a few degrees toward the lens; the head, the top of the wig and the face centre stay within 3 percent of the photo. " + ENDQ),
    clip=("{HEAD}{KING}, the candlelit gilded hall behind him, his own hand-held phone at arm's length a little above his eye level. At the end, 14 s, the frame is exactly as @last_frame (a grand smug look into the lens); the king and the room are in the same place in both frames. Realistic live action, real skin texture, no beauty filter. "
          "0-1.5 s: a satisfied sigh, the heavy lids lowering; "
          "1.5-4 s: he turns to the screen with a wounded look: \"Some of you write that I eat too much.\" with a tilt of the head; at 3 s a courtier at the right leans to his neighbour; "
          "4-6 s: \"I read it.\" a slow blink; then he sniffs, haughty; "
          "6-8 s: the silent beat of one and a half seconds: he lets it hang, then waves a hand dismissively without looking; the camera keeps moving; "
          "8-10.5 s: \"Of course, that's not true.\" the chin rising, a dry smile; "
          "10.5-13 s: \"Every day I feast in front of the court.\" the head sweeping slowly to look at the hall behind him and back; at 12 s the lady with the fan fans herself; "
          "13-14 s: \"Today... before your eyes.\" the eyes on the lens, settling into the pose of @last_frame. "
          "CAMERA SCORE in absolute amounts (his own hand-held phone at arm's length; the king and the room stay in place while the frame moves; his face is at 50 percent of the width, so every move keeps his face and wig inside the frame, the free margin is about 24 percent on each side): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a slow drift to the right by 8 percent and a push-in of 5 percent; 2-4 s a sway to the left by 9 percent with the roll easing by 3 degrees; 4-6 s a dip and a lift by 5 percent; at about 5 s (the allowed window is 3 to 7 s) the focus hunts for half a second; 6-8 s a drift to the right by 8 percent; 8-10 s a push-in of 6 percent and a sway left; at about 9 s (the allowed window is 7 to 11 s) his own pink thumb slips into the lower right corner covering the lower right 20 percent of the frame width (never more than 25 percent) for 0.7 s and never his face; 10-12 s the sweep of the head with the frame following by 10 percent to the right and back; 12-14 s a small push-back and settle to the framing of @last_frame. "
          "POSE SCORE as verbs: sigh, read, tilt, blink, sniff, wave, lift, sweep, smile; the head moves about half of its own width (about 18 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; never a hold longer than 2 seconds. "
          "THE ROOM IS ALIVE: candle flames flicker; at 1 s a servant in livery far behind carries a dish from right to left; at 3 s the courtier at the right leans to his neighbour; at 7 s a lady at the back left lowers her fan; at 12 s the lady with the fan fans herself. "
          "{TAIL}")
)

# ================================================================ writers
IMG_FOOT = '''
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [%s]}
open(H0 + "%s_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/%s_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\\?[^"]*', r'\\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
'''
HEAD = '''import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
'''
VID_FOOT = '''
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "%s_start_4k.jpg", RAW + "%s_end_4k.jpg"],
        "duration": %d, "resolution": "720p"}
open(H0 + "take_%s_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_%s.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_%s.status.json", "w").write(re.sub(r'(https://[^"?]+)\\?[^"]*', r'\\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_%s.mp4"); print("saved")
'''
def q(s):
    import json as _j
    parts = re.split(r"(?<=[.;:]) ", s)
    return "(" + "\n".join(_j.dumps(x + " ") for x in parts) + "\n)"

for k, p in P.items():
    price_clip = round(0.145 * p["sec"], 2)
    reflist = ", ".join('RAW + "%s"' % r for r in p["refs"])
    doc0 = ('"""%s: START still (prepared 06.11, NOT run until the owner\'s yes after seeing the refs and the Russian prompt). Script 7.3 lines: %s '
            'GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: %s. One call, about $0.12. Run: python3 gen_%s_start.py go"""\n') % (p["title"], p["lines"].replace('"""', "'"), ", ".join(p["refs"]), k)
    open(H0 + "gen_%s_start.py" % k, "w").write(doc0 + HEAD + "prompt = " + q(p["start"]) + "\n" + (IMG_FOOT % (reflist, k + "_start", k + "_start")))
    doc1 = ('"""%s: END still, an EDIT of the start still (same camera, different pose; prepared 06.11, NOT run until the owner\'s yes). One ref = refs/%s_start_4k.jpg (the 4K original). One call, about $0.12. Run: python3 gen_%s_end.py go"""\n') % (p["title"], k, k)
    open(H0 + "gen_%s_end.py" % k, "w").write(doc1 + HEAD + "prompt = " + q(p["end"]) + "\n" + (IMG_FOOT % ('RAW + "%s_start_4k.jpg"' % k, k + "_end", k + "_end")))
    clip = p["clip"].replace("{HEAD}", CLIPHEAD).replace("{KING}", KING).replace("{MARCEL}", MARCEL).replace("{TAIL}", CLIPTAIL)
    doc2 = ('"""%s: CLIP (prepared 06.11, NOT run until the owner\'s yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p %d s = $%.2f (0.145 x %d). first = %s_start_4k, last = %s_end_4k. Lines (script 7.3): %s Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes."""\n') % (p["title"], p["sec"], price_clip, p["sec"], k, k, p["lines"].replace('"""', "'"))
    open(H0 + "gen_take_%s.py" % k, "w").write(doc2 + HEAD + "prompt = " + q(clip) + "\n" + (VID_FOOT % (k, k, p["sec"], k, k, k, k)))
    print(k, "start/end $0.24 + clip $%.2f = $%.2f" % (price_clip, 0.24 + price_clip), "| prompt chars", len(clip))
