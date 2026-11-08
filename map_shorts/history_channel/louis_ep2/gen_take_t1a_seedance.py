"""Take 1 piece 1a CLIP on Seedance 2.5 LITE i2v (08.11): image_urls[0] = the owner's own start frame (refs/t1w_start_4k.jpg), image_urls[1] = the accepted middle still (last frame of 1a = first frame of 1b, the shot continues), 720p, 12 s, 9:16, $0.15/s = $1.80, audio off. Line (script, 19 words, about 95 wpm): "Is it... is it on? Ah. There I am. [clears throat] Bonjour. I am Louis, King of France. Welcome to Versailles." The king walks the hall filming himself, the phone too close, pulls it back, sees himself and is pleased, greets. Brief: briefs/brief_t1_walk.md PIECE 1a (beats and pins). Known risks: Seedance does not make a person walk from a still (written as hall slide and step bob), eyes may close long in delight (eyes open written per beat), a gesture hand and a camera hand may make three arms (camera arm stays out of frame after the pull-back; one free hand only), the accepted end still has glass and goblet at the right of the table (not to be animated). One call, no retries without a new yes. Run: python3 gen_take_t1a_seedance.py go
BRIEF: briefs/brief_t1_walk.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/"
prompt = (
    "The first frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it; the last frame is the exact end frame and the clip arrives at it by 12 s. "
    "Realistic live action in the look of a hand-held vlog that he films of himself while walking, real skin texture, sharp focus on the face except 2.2 to 2.6 s. "
    "The same king in every frame: the same face, age about 45, heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark below the mouth on the viewer's right always visible, light rouge, the tall powdered wig in silver-grey and white, the scarlet velvet coat with gold suns, lace cravat; "
    "he walks slowly along the long candlelit panelled hall, the hall slides past behind him, a long banquet table with seated people far ahead on the right comes closer, wall sconces, a row of wig stands on the left with courtiers. "
    "0-1.0 s: he says \"Is it...\" "
    "the camera is held too close, his face fills about 55 percent of the frame width, low, mouth open and searching, lids heavy, brows pulled together; his left hand with the rings, holding the camera, is at the top of the frame and leaves it by 2.5 s. "
    "1.0-2.5 s: he says \"...is it on?\" "
    "he grimaces, the nose wrinkles at 1.2 s, a squint at 1.8 s, his eyes shut for at most 0.5 s at 2.0 s and then open on the lens; the head shakes 6 degrees; a servant far ahead carries a dish along the table at 1.5 s. "
    "2.5-4.5 s: his mouth is closed during the swing from 2.5 to 3.2 s (the silent beat), he says \"Ah.\" softly at 3.3 to 3.6 s, then the mouth closes again with a smirk until 4.5 s; "
    "the camera is pulled away from his face, his face shrinks from 55 to about 38 percent of the frame width in 1.5 s, the frame swings down from the ceiling to a head-and-shoulders shot, a blur of 0.3 s only at the start of the swing, the camera arm leaves the picture; his eyes snap onto the lens, the brows rise for 0.3 s, then the lids lower and one corner of the mouth lifts in smug pleasure; his right hand smooths the lace at 3.8 s. "
    "4.5-6.0 s: he says \"There I am.\" "
    "one short glance down and to the right at himself for 0.5 s and back to the lens, lids heavy, a smirk; his right hand touches a curl of the wig at 5.2 s; a man at the table lifts a spoon at 5.0 s, a lady whispers behind a fan. "
    "6.0-7.5 s: he clears his throat and says \"Bonjour.\" "
    "the lips press, one small cough at 6.1 s with a slight head dip, the chin lifts 5 degrees, a lazy half smile, his right hand opens the palm toward the lens for 0.5 s at 6.8 s; a courtier at the left wall shifts his weight at 6.5 s; the servant sets the dish down at 7.0 s. "
    "7.5-9.5 s: he says \"I am Louis, King of France.\" "
    "eyes into the lens the whole line, a blink of 0.2 s at 8.7 s, the head tilts 6 degrees toward the viewer's left with the beauty mark still visible; his right hand drops and brushes the lace; a lady in blue lifts her fan at 8.0 s. "
    "9.5-12.0 s: he says \"Welcome to Versailles.\" "
    "at 9.8 s his gaze leaves the lens to the hall, down and to the left, for 0.6 s and the head turns 12 degrees, both eyes and the beauty mark stay visible, back to the lens at 10.8 s on \"Versailles\" with a proud lift of the chin; his right hand makes one small half circle toward the hall at 10.0 s, returns to the chest at 10.6 s and drops out of the picture by 11.3 s; a lady laughs behind her fan at 11.0 s; at 12 s he is as in the last frame: face about 34 percent of the width, head turned toward the viewer's left, lips closed in a small proud smile, eyes open on the lens, both arms out of the picture. "
    "CAMERA SCORE in absolute amounts, written in what the viewer sees (hand-held while walking, eye level; from 2.5 s on the whole wig and the long curls stay inside the picture with a margin of at least 5 percent of the frame height at the top, and never touch a side edge): "
    "0-2.5 s: a step bob of 4 to 6 percent up and down at two steps per second, a roll of 3 to 5 degrees; "
    "2.5-4.5 s: the swing down of 25 percent of the frame height; "
    "4.5-6.0 s: a bob of 4 percent, a roll of 2 degrees; "
    "6.0-7.5 s: a push-in of 4 percent on top of the step bob of 3 to 4 percent at two steps per second, a roll of 2 degrees to the left; "
    "7.5-8.5 s: a step catches, the frame drops 6 percent and returns; "
    "8.5-12.0 s: the step bob of 3 to 4 percent continues, the hall keeps sliding past, a slow drift of 6 percent to reveal more of the table, a roll of 2 degrees to the right, a push-in of 5 percent in the last second. "
    "HAND-HELD MISTAKES: a focus hunt at 2.0 to 2.4 s, the picture softens for 0.4 s and snaps sharp. "
    "Re-aims are slow, within one second, soft and by hand, never a whip pan, never a smooth gimbal glide. "
    "His lips form every spoken word clearly (the voice is added later); in the silent beats the mouth is closed. Silent beats with a closed mouth: 2.5-3.2 s, 3.7-4.5 s, 6.0-6.1 s before the cough, 9.5 s after \"France\". "
    "POSE SCORE as verbs: walk, grimace, wince, pull back, smirk, glance, touch the wig, clear the throat, greet, tilt the head, look at the hall, lift the chin; the acting is natural and plain, as a real person films himself; no expression lasts longer than 2 seconds. "
    "Acting limits: ordinary blinks aside the eyes are open at every moment, the face stays natural, five natural fingers on each hand, two arms in total and after 2.5 s only one hand visible at a time. "
    "Sound: only the low murmur of a large hall, footsteps, fabric, candle flicker, breath, room tone, no music. "
    "Nobody at the table lifts, holds or drinks from a glass or a cup; the objects on the table stay where they are; nobody looks into the lens. "
    "A clean picture of the 1680s with no text and no modern objects, one king in the frame. "
)

body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "refs/t1w_start_4k.jpg", RAW + "pilot_frames/anchors/t1wm_mid_sunburst_4k.jpg"],
        "duration": 12, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}
open(H0 + "take_t1a_seedance_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t1a_seedance.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=500, every=10)
    open(H0 + "pilot_frames/TAKE_t1a_seedance.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t1a_seedance.mp4"); print("saved")
