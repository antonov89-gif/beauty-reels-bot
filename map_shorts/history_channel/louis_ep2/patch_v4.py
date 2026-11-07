# v4 (07.11): the filming device must never be drawn. Image models draw a named object even when it is negated, so the still prompts do not name the phone at all.
R = [("The phone that films is never visible in the frame. ", ""),
     ("his own phone held far too close and LOW, a low selfie from under his chin", "a selfie shot with the arm extended, held far too close and LOW, from under his chin"),
     ("only the blurred tip of his pink thumb is visible at the very lower right corner, and NO phone, no phone case and no screen is visible anywhere in the frame (the phone is the camera);", "the very lower right corner shows only the soft blurred tip of a pink thumb, the rest of that corner is blurred hall;"),
     ("he is squinting into the lens as if reading its screen, with a puzzled frown", "he is squinting into the lens as if checking something, with a puzzled frown"),
     ("his phone held in his hand at TABLE HEIGHT", "a hand-held selfie angle at TABLE HEIGHT"),
     ("his own hand-held phone held at CHEST HEIGHT", "a hand-held angle at CHEST HEIGHT"),
     ("the king's own phone seen from where the king sits", "the view from where the king sits"),
     ("the king's own arm's-length phone held IN FRONT of him and HIGH", "an arm's-length selfie angle IN FRONT of him and HIGH"),
     ("his own phone in his outstretched hand held LOW", "a selfie angle with his arm outstretched, LOW"),
     ("Real phone footage,", "Real handheld footage,"),
     ("the phone has been pulled back a little", "the camera has been pulled back a little"),
     ("he has seen himself on the screen and is pleased", "he has seen himself and is pleased"),
     ("Reference 1 (the king's master portrait)", "Reference 1 (the king's master portrait)")]
for k, p in P.items():
    for f in ("start", "end"):
        t = p[f]
        for a, b in R:
            t = t.replace(a, b)
        p[f] = t
# 07.11 third attempt of t1na start (inspector: soft 88/1.47, loose net strands, blurred thumb patch)
P["t1na"]["start"] = P["t1na"]["start"].replace("the very lower right corner shows only the soft blurred tip of a pink thumb, the rest of that corner is blurred hall;", "the lower right corner shows only the blurred hall;")
assert "shows only the blurred hall;" in P["t1na"]["start"]
P["t1na"]["start"] = P["t1na"]["start"].replace("the face is still sharp and readable;", "the face is still sharp and readable, tack-sharp 4K, fine lace and wig curl detail, a clean wig outline with no loose net strands, no soft focus;")
assert "tack-sharp 4K" in P["t1na"]["start"]
