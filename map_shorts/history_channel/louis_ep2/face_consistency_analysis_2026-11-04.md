# How not to lose the king's face: analysis of the T1 chain (04.11.2026, owner: "обдумай, проанализируй")
Method: SFace (OpenCV) face-embedding cosine similarity of frames sampled at 2 fps against the character card A3; script face_gate.py. SFace's same-person threshold is 0.363; our costumed king vs A3 is lower than a normal photo (A3 vs the owner's best frame = 0.595), so the practical gate is mean >= 0.60 and min >= 0.45. The numbers are a second opinion next to the eyes, not a replacement.

## Measured (mean similarity to A3, frames after the fumble)
| Clip | Setup | Mean | 1st half | 2nd half | Min |
|--|--|--|--|--|--|
| T1 v1 | first frame only, no tag | 0.35 | 0.35 | 0.35 | 0.27 |
| T1 v2 | + @first_frame tag | 0.33 | 0.35 | 0.31 | 0.25 |
| T1 v3 | + @keyframe_1 (generated still) | 0.81 | 0.78 | 0.83 | 0.72 |
| T1 v4 | + @keyframe_1 (edit of A3) | 0.76 | 0.76 | 0.77 | 0.69 |
| T1 v5 | + @keyframe_1 (owner's still) | 0.70 | 0.68 | 0.71 | 0.57 |
| T1b | chain from v5 last frame, no keyframe | 0.63 | 0.66 | 0.61 | 0.55 |
| T1c | chain from T1b last frame, no keyframe | 0.57 | 0.60 | 0.53 | 0.48 |
| T1d | chain from T1c last frame, no keyframe, lean-in | 0.55 | 0.56 | 0.53 | 0.47 |
| T3b | a separate still as first frame | 0.59 | 0.52 | 0.66 | 0.11 |

## What it says
1. WITHOUT an anchor the face is lost: v1 and v2 (first frame only) score 0.33-0.35, at the "different person" threshold. This is exactly what the owner saw ("лица не совпадают").
2. WITH an anchor in `keyframe_urls` the same clip scores 0.70-0.81. One extra image fixes most of it. The tag alone (v2) did nothing for identity.
3. A chain WITHOUT anchors decays: 0.70 (T1 v5) -> 0.63 -> 0.57 -> 0.55, about -0.05 to -0.08 per clip, because each last frame is a model output with its own small error and the next clip starts from it. Over 25 clips it would be a different man. T1b-T1d each looked "fine" on the join (RMSE 0.03) while the face slipped; a join check alone cannot catch this.
4. Drift is also driven by the acting: the worst seconds are the lean toward the lens (face width share rises from 0.3 to 0.6) and wide-eyed grins. Strong frowns drop the score too. Calm, haughty, medium-size face keeps it.
5. The anchor's own quality matters: the clip follows the anchor, not A3. The anchor chosen for the chain (owner's best frame) is only 0.595 close to A3, so the chain's ceiling is about 0.6-0.7. For a closer face, derive the anchors by EDITING the A3 frame (the A3 edit kept the face), not by generating a new still.

## Method for the rest of ep.2 (recommended)
A. Anchor set: from the owner's best frame (face accepted by the owner) make 5-6 in-scene stills by EDITING it, never regenerating: speaking (mouth open), haughty at the lens, laugh, frown/annoyed, eyes aside, chewing. Each one is gated with face_gate-style similarity to A3 and to the best frame (>= 0.70) and looked at by the eye before use (about $0.12 each).
B. Every clip is pinned at BOTH ends and in the middle: @first_frame = previous clip's last frame (when the previous ended on an anchor pose, drift does not accumulate), @last_frame = the anchor variant that matches the end beat, @keyframe_1 = an anchor in the middle. Slots: image_urls max 2, keyframe_urls up to 8.
C. Every clip ENDS on an anchor pose (so the chain is re-pinned every 6-8 s); the acting between is free but within the range: no lean-in, no wide eyes, no grin; heavy lids.
D. Gate before showing: face_gate.py on every clip (mean >= 0.60, min >= 0.45) plus eye check at 3 points; reject below, do not chain from a rejected clip.
E. Re-do from the point where the chain fell below the gate: T1c (0.57) and T1d (0.55). T1 v5 (0.70) and T1b (0.63) pass.
F. Fallback to test once if A-D fail: Kling 4.0 r2v with kling_elements (2-4 face images = face lock per its spec, model_choice.md), about $1.14 per 8 s; it does not pin the first frame, so it is a test, not the plan.
Cost impact: anchors about $0.6-0.7 once; retakes of T1c and T1d about $2.0-2.3; the rest of the episode at about $1.16 per 8 s without the 30 % retake reserve being used up by face failures.
