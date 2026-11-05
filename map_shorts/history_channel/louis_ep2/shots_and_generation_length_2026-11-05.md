# Shot lengths, cuts and generation length: reference Vlog 1 vs our ep.2 (05.11.2026, owner: "посмотри какие сцены по длине, увидь склейки у референса, определи длину генерации по секундам")
Owner decisions 05.11: 720p stays; quality must stay constant (no loss from chaining last frames); one strictly identical face.

## Reference, measured on the owner's 1080x1920 30 fps file (first 30.78 s) with 30 fps frame differences, face embeddings, brightness and audio
- Hard cuts: ONE, at 23.61 s (frame difference 54.6, face similarity to the previous shot drops 0.90 -> 0.28, brightness 82 -> 91). Everything before it is a single shot of 23.6 s.
- Inside that shot, 5.0 s -> 23.4 s (18.4 s): NO seam. Face similarity to the 5 s face stays 0.86-0.94 on almost every sample (dips to 0.69-0.79 at 13.2-14.8 s are head turns on "England and Ireland and well", not seams); frame difference has no spike above median+6*MAD anywhere in 8-22.5 s (median 3.4); brightness is flat at 82-84; audio has no dead silence (nothing below -55 dBFS for 0.1 s) and the level steps are word onsets, not periodic.
- The first 4.5 s are one continuous camera move (extreme low angle with a thumb, tilt up to level), no cut: frame-difference spikes at 3.2, 3.4, 3.6, 3.9, 4.9, 5.2, 5.9 s are the hand motion.
- Earlier measurement of the whole video (owner's 360p copy, frames_vlog1_LjfGP7wpjVs.md): 14 shots, 13 hard cuts; three long continuous takes of 23.6 s, 28.8 s and 30.1 s (64 % of the runtime), one 5.9 s burst of 9 micro-cuts (food close-ups), three medium shots of 9.8 s, 12.7 s and 17.4 s; mean shot 9.2 s, median 1.9 s.
## Generation length of the reference (what can be known)
- The longest continuous take is 30.1 s, the others 28.8 s and 23.6 s, all with no visible seam. None of the periodic breaks that a chain of 5-8 s clips would leave (colour step, face reset, grain reset, audio gap at every 5/8/10 s) appears. STRONG INFERENCE: the takes were generated in one pass of about 24-30 s each (or chained so cleanly that no seam can be measured). The tool is NOT known and is not proven.
- Tools that can do a 30 s single generation: Kling 4.0 i2v (3-30 s, OpenAPI spec read 04.11) and Seedance 2.5 (4-30 s, model_choice.md). So the reference's takes fit one generation each.

## Ours (plan 7.1, 25 clips of 8-10 s, estimated at 110 wpm + beats)
| Take | Words | Estimated length | Reference comparison |
|--|--|--|--|
| 1 selfie, opener, myth | 59 | about 32 s | longer than the reference's 23.6 s |
| 2 room and rule | 52 | about 28 s | like its 28.8 s take |
| 3 food | 60 | about 33 s | longer than its 30.1 s take |
| 4 drink | 45 | about 25 s | like its 23.6 s take |
| 5 last rounds, belly | 36 | about 20 s + 4 s | between its medium and long shots |
| 6 verdict | 24 | about 13 s | like its 12.7 s shot |
| 7 teaser and outro | 51 | about 28 s | like its 28.8 s take |
| 8 cannot turn it off | 9 | about 5 s | |
All eight takes are 13-33 s with hard cuts only between takes (7 cuts in about 3 min, mean about 22 s). The reference mean is 9.2 s with one 9-cut burst and medium shots of 10-17 s. We are slower and more uniform; adding a food burst (Take 3 or 5), a Marcel reaction shot and 2-3 medium cutaways would bring the mean toward 10-12 s without more speech.
## The seam problem in our method
We generate 8-10 s clips and join them, so every 8-10 s is a seam where the face, the sharpness and the colour can step (measured: the chain lost about 0.05-0.08 face similarity and about 80 % sharpness over three links). The reference has no seams inside 24-30 s takes.

## Proposed method (needs the owner's yes before any spend)
1. Make each take ONE generation of 15-30 s instead of 3-4 clips of 8-10 s (Kling 4.0 i2v, 720p, $0.145/s: the price per second is the same, a 30 s take is $4.35).
2. Pin each take with every slot the API allows: for duration >= 9 s the spec caps the frames at 10 (first + last + 8 keyframes), i.e. one anchor every 3-4 s in a 30 s take. Anchors come from the card/emotion edits (the six in-scene anchors made 05.11), so the face is the same card face all the way and nothing is chained from a model last frame: no loss of quality or face by chaining.
3. Keep the acting inside the safe range (no lean-in, no wide eyes, no grin).
4. Gate each take: SFace median >= 0.65 and p10 >= 0.45 against A3, outliers checked by eye, plus the sharpness numbers against the first anchor still.
5. Pilot first: one 15 s piece (the first 15 s of Take 1) at $2.18 to see whether a long pinned take holds the face and the sharpness. If it does, the takes are 20-30 s.
Risks: a failed 30 s take costs $4.35 (against $1.16 for a failed 8 s clip); speech timing over 30 s; our voice is laid over the picture by whole phrases, so the model's mouth timing must be close; the anchors force the poses at their moments, so the acting between them is the model's.
