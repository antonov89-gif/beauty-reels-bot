# v3 (07.11): new card set. Master O8 (new face line, age about 45, wig colour judged against the light), one angle tile as reference 2 where a matching one exists. Runs after patch_v2.
import re
ANGLE = {"t1na": ("K4_angle_low_O12.png", "from below, chin up"), "t5a": ("K4_angle_low_O12.png", "from below, low camera"),
         "t5c": ("K4_angle_high_O13.png", "from above, head tilted back"), "t7a": ("K4_angle_34right_O11.png", "turned to the right side of the image, the beauty mark stays on the right of the image"),
         "t7b": ("K4_angle_low_O12.png", "from below, chin raised")}
WIGOLD = "the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it)"
WIGOLD2 = "the tall powdered wig in cool silver-grey and white like the pale grey in reference 1, NOT beige, NOT cream, NOT golden, the candlelight must not tint it"
WIGNEW = "the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light)"
for k, p in P.items():
    if k in ("t4b2", "t4bA", "t4bB"):
        continue
    refs = ["K4_master_neutral_O8.png"]
    if k in ANGLE: refs.append(ANGLE[k][0])
    if "R10_hall_clean.jpg" in p["refs"]: refs.append("R10_hall_clean.jpg")
    p["refs"] = refs
    if "end_extra" in p: p["end_extra"] = ["K4_master_neutral_O8.png"]
    for f in ("start", "end", "clip"):
        t = p[f]
        t = t.replace(WIGOLD2, WIGNEW).replace(WIGOLD, WIGNEW)
        t = t.replace("Reference 1 is the king's face and costume: exactly the same man, same age,", "Reference 1 is the king's face and costume: exactly the same man of about 45, same")
        t = t.replace("same same", "same")
        t = re.sub(r"like the pale grey in reference 1, ", "", t)
        t = t.replace("Reference 1 is the king's face and costume", "Reference 1 (the king's master portrait) is his face and costume")
        t = t.replace("do not copy its pose or background", "do not copy its neutral pose or backdrop")
        t = t.replace("(the same cool silver-grey and white colour as in the photo, NOT beige, NOT cream, NOT golden, the candlelight must not tint it)", "(same silver-grey and white as in the photo)")
        t = t.replace("; the wig keeps its cool silver-grey and white", "; the wig keeps its silver-grey and white (a light tint from the scene light is fine)")
        p[f] = t
    if k in ANGLE:
        sent = " Reference 2 shows the same man " + ANGLE[k][1] + ": take the camera angle and the head pose from it, the face and the wig from reference 1. "
        p["start"] = p["start"].replace("do not copy its neutral pose or backdrop. ", "do not copy its neutral pose or backdrop." + sent, 1)
        if "Reference 2 shows only the hall" in p["start"]:
            p["start"] = p["start"].replace("Reference 2 shows only the hall", "Reference 3 shows only the hall")
    p["start"] = p["start"].replace("Reference 2 shows only the hall: ignore its angle", "Reference " + str(len(refs)) + " shows only the hall: ignore its angle") if "R10_hall_clean.jpg" in refs else p["start"]
