"""RETAKE v2 (owner "2" on 06.11 after the formal brak of the first take: big early flute, laugh too early, 40 percent still body): Take 4, piece 4b-1 "wine and laugh" (setup S10a, the king's own selfie from above). Kling 4.0 i2v 720p 10 s = $1.45 (0.145 x 10). first = T4b start still, last = T4b end still (both pass the quality limits, no exception). Lines (script 7.3): "...Mon Dieu. [silence, then he laughs for real] Nobody saw anything." The goblet and the splash happen inside the clip (the pins carry no cup). Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("@first_frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, and the red wine film never tints it: the wig stays silver-grey all over and the drip stays on the lens glass left of the side curls), thin dark waxed moustache with curled tips, the beauty mark on the viewer's right of the mouth, light rouge, scarlet velvet coat with a gold sun, lace cravat; the same candlelit gilded hall behind him, his own hand-held phone selfie from slightly above at arm's length, his face a little right of the frame centre, the left third of the frame holding the side curls of the wig and the blurred hall. At the end, 10 s, the frame is exactly as @last_frame (he is laughing for real, the head tipped back a little and about 5 percent of the frame height higher, eyes nearly shut, a thin wavy dark-red drip line and a red tint on the left 30 percent of the lens, the right two thirds sharp); the room and the king are in the same place in @last_frame as in @first_frame, only the expression, the head tip and the wine differ. At 0 s and at 10 s no goblet is in the frame. Realistic live action, real skin texture, no beauty filter. "
"0-1.5 s: he smirks into the lens, pleased, the wait over, heavy lids; behind him at the left back the lady with the fan whispers to her neighbour; at 1 s a courtier at the right edge turns his head toward the left. "
"1.5-2.2 s: from the LEFT edge of the frame a small white-gloved hand with a GOLD goblet (a metal cup on a stem, never a clear glass or a flute, no larger than a fifth of the frame width and never covering his face) swings in at 1.5 s and tips it; by 2.2 s the hand and the goblet are completely out of the frame and from 2.2 s to 10 s no hand, glass or goblet is anywhere in the frame; the splash comes from the goblet that is already out of the frame. "
"2-4 s: the wine hits the left third of the lens (the event, not a phone mistake): a single drop of wine hits the lens at 2 s and runs down for 1 s, the picture lurches, he flinches back a little and to the left, at 2.5 s the whole picture blurs for half a second and snaps sharp again, and a thin wavy dark-red drip line and a red tint stay on the left 30 percent of the lens (the film never grows past 35 percent of the width and never touches his face or the top of his wig). "
"3-4.2 s: he blinks slowly under heavy lids and says softly, his lips moving slightly: \"...Mon Dieu.\" and the phone drifts back toward the framing of @last_frame. "
"4.2-6.2 s: a long silent beat of two full seconds: he looks into the lens in disbelief, then his mouth starts to twitch; the lady with the fan turns toward him and a courtier at the right edge in a dark coat steps toward the centre. "
"6.2-8.2 s: the laugh builds: his shoulders start to shake, his eyes squeeze shut, and then his head tips back about 10 degrees and about 5 percent of the frame height up with a big real laugh, the upper teeth showing; at 6.5 s a servant far behind on the right walks across from right to left. "
"8.2-9.6 s: still laughing, with a breath of laughter he says: \"Nobody saw anything.\" and the frame settles to the framing of @last_frame. "
"9.6-10 s: he holds the laugh in the pose of @last_frame. "
"CAMERA SCORE in absolute amounts (his own hand-held phone in one outstretched hand; the king and the room stay in place, the frame moves; his face is at 58 percent of the frame width, so every move keeps the wig and the face inside the frame (the free margin is about 19 percent of the width on the left and 14 percent on the right)): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a slow drift to the right by 8 percent with the roll easing by 3 degrees and a push-in of 6 percent; at 2 s a lurch of 9 percent to the left with the splash; 2-4 s a shake that settles; 4-6 s a slow sway to the right by 8 percent; at about 6.5 s (the allowed window is 4.5 to 8.5 s) his own pink thumb slips into the lower right corner for 0.5 s, covering the lower right 20 percent of the frame width (never more than 25 percent) for 0.8 s and never his face (phone mistake); 6-8 s the frame shakes with his laughter by 6 percent; 8-10 s the frame settles back to the framing of @last_frame. "
"POSE SCORE as verbs: smirk, lean, flinch, blink, stare, twitch, shake, squeeze, tip back, breathe; the head moves about half of its own width (about 15 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre: 0-2 s leans slightly toward the lens, 2-4 s flinches back and left with the eyes dropping and the chin lifting, 4-6 s comes forward, glances left and the shoulders drop, 6-8 s shakes and tips back, 8-10 s settles; never a stillness longer than 3 seconds. "
"THE ROOM IS ALIVE: candle flames flicker; at 3 s the courtier at the right edge shifts his weight from one foot to the other; the background people keep their faces. "
"Acting limits: heavy eyelids stay except in the laugh, no wide-open eyes, the face stays natural, the laugh shows only the upper teeth; no hands are in the frame except the gloved hand at 1.5-2.2 s and his own thumb at about 6.5 s. "
"No whip pans and no zoom lens: the only quick moves are the lurch at 2 s and the shake of the laugh, all by hand; no gimbal, no dolly or flying camera. "
"Sound: only diegetic, low murmur of a large hall, a splash of liquid, fabric, candle flicker, his laughter; no music at all. No text or captions, no modern objects, only one king in the frame (no second face, no double).")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T4b_start_4k.jpg", RAW + "T4b_end_4k.jpg"],
        "duration": 10, "resolution": "720p"}
open(H0 + "take4_T4b_v2_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE4_T4b_v2.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE4_T4b_v2.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE4_T4b_v2.mp4"); print("saved")
