# Audit of the stills we already have (06.11, owner: "мы раньше делали эти фото, подойдут или нет, проверь, поищи"), measured, no generation
Reason: the APIpod balance is exhausted (HTTP 500 insufficient quota on the 4b-1 retake): which existing stills could replace new paid ones for the remaining pieces (4b-2 Marcel, 5a, 5b, 5c, 6, 7)?
Measured (sharp / detail at 1024 short side; SFace to card A3 for the king, to the Marcel card R2 for Marcel; subject limits 150 / 2.0, face >= 0.70):
| still | size | sharp / detail | face | verdict |
|--|--|--|--|--|
| ANCHOR_E1 haughty | 2161x3840 | 148 / 2.03 | 0.69 | borderline, face just below the gate |
| ANCHOR_E2 smug | 2161x3840 | 182 / 2.26 | 0.81 | good |
| ANCHOR_E3 laugh | 2161x3840 | 166 / 1.76 | 0.67 | detail and face below the limits |
| ANCHOR_E6 annoyed | 2161x3840 | 174 / 2.15 | 0.72 | ok |
| ANCHOR_E7 blissful | 2161x3840 | 191 / 2.36 | 0.67 | face below the gate |
| ANCHOR_E8 startled | 2161x3840 | 276 / 2.33 | 0.80 | good |
| POSE_P2 pleased | 2161x3840 | 397 / 3.21 | 0.84 | good (already T2a's last pin) |
| T1_keyframe_edit | 2161x3840 | 820 / 4.80 | 0.89 | good (already Take 1's pin) |
| F04b_v1_owner (Marcel + wine) | 941x1672 | 31 / 1.14 | 0.74 | NO: soft, small |
| R4 Marcel terrified (card tile) | 1280x2294 | 116 / 1.64 | 0.88 | below the limits, would need an owner exception |
| R3 Marcel three-quarter (card tile) | 1280x2294 | 200 / 2.69 | 0.79 | quality ok, but the room behind is another room (not the dining hall) |
| T2b_start Marcel POV (shoes) | 2161x3840 | 179 / 2.12 | n.a. (feet) | already used in T2b |
Pairs as first/last pins of ONE clip: the E-series stills differ from each other by RMSE 0.19-0.27 (head boxes and background differ), a usable pin pair needs <= about 0.10 (all our accepted pairs 0.03-0.10 against their clips; P2/T1 pair 0.125 was the T2a case). So the E-series can NOT be paired as first+last pins. Single stills are usable as: (a) a first-frame-only clip (the face drifts after about 4 s without a last pin: earlier test), (b) free 2-3 s inserts/cutaways in the edit with virtual hand-held (sharpness of the head about halves under a strong punch-in: measured earlier), (c) the E-series are all the same S0 composition (frontal eye-level selfie in the same hall) = Take 1's look again: the owner's "never repeat one king frame" rule applies if used as separate setups.
Fits per remaining piece: 4b retake: has its own pins; 4b-2 Marcel: nothing fits as a start pin in the dining hall (R3 has the wrong room, R4 below the limits, F04b unusable); 5a/5b (across/along the table, Marcel films): nothing; 5c (from above, leaning back): nothing (the K_ sheet tiles are 512 px); 6 verdict (frontal close, S13): E2 or E8 can serve as an insert or a first-frame-only clip but repeat the S0 look; 7 outro (king standing): nothing (R8 is Marcel).
