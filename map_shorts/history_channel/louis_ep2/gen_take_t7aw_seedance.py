"""Take 7 piece 7a-WALK CLIP on Seedance 2.5 LITE i2v (07.11): image_urls[0] = first frame ONLY (owner rule 07.11: no end still when the next piece is a cut), 720p, 10 s, 9:16, $0.15/s = $1.50, audio off. Owner 07.11: the king walks through the hall holding the camera, looks into it and speaks (script_v7_final.md Take 7 words, brief 'BRIEF 7a-walk'). EN voice: "So... I was wondering what else to show you here. [pause, a short laugh] Ha. Probably... nothing." The pin has the wig top only 3 % from the top edge and the left curls 5 % from the left edge: the camera moves are written in what the viewer sees (the king slides toward the RIGHT edge of the picture, the king sinks lower in the frame), never the king toward the left or up. Deliberate deviations from BRIEF 7a-walk: step bob 1 % (not 4-6 %) because of the margins, no re-aim at 3-4.5 s, the fingertip at 8.9-9.5 s (not on the punchline), the gaze sweep and the cough glance written once each. One call, no retries without a new yes. Run: python3 gen_take_t7aw_seedance.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = (
    "The first frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. "
    "Realistic live action in the look of a hand-held vlog that he films of himself while walking, real skin texture, sharp focus on the face except 4.8 to 5.3 s. "
    "The same king in every frame: the same face, age about 45, heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark below the mouth on the viewer's right exactly as in the first frame and always visible, light rouge, the tall powdered wig in silver-grey and white, the scarlet velvet coat with gold suns, lace cravat; "
    "he walks slowly along the long candlelit gilded hall lit by wall sconces, the king walks in step with the camera held at arm's length in front of him and the hall slides past behind him; the courtiers in plain wigs standing at both sides step aside and bow a little as he passes; a courtier at the back right in a scarlet coat bows, he is not the king; the cuff and the back of the hand at the lower right edge stay as in the first frame. "
    "0-1.8 s: he says \"So...\" "
    "he walks on with a thoughtful look, his eyes slide up and to the right toward the hall and come back to the lens, the lips pursed; at 1.0 s the lady with an open fan at the back right lifts her fan. "
    "1.8-4.8 s: he says \"I was wondering what else to show you here.\" "
    "his eyes sweep the hall slowly from right to left, not a jump, the brows pull together once as if searching, at 4.2 s one glance INTO THE LENS on \"you\" for 0.6 s; a servant crosses behind him from right to left at 3.0 s; at 4.8 s the picture softens for 0.5 s and snaps sharp. "
    "4.8-6.0 s: silent, "
    "his eyes go around the hall again, the brow climbs as if an idea comes, the lips press, then a sour half smile, he gives up the search, a small sigh with the shoulders dropping a little at 5.5 s; two courtiers on the right whisper at 5.0 s and the others shift their weight and wait. "
    "6.0-7.0 s: he says \"Ha.\" "
    "a short natural laugh of at most 0.8 s, one breath, the eyes narrowed but visible, the head tips 5 degrees further toward the viewer's right (clockwise, as in the first frame) and the chin lifts a little, the shoulders shake once; the lady with the fan giggles behind her fan at 6.5 s. "
    "7.0-9.6 s: he says \"Probably... nothing.\" "
    "the laugh switches off within 0.3 s, his face is flat, the lids heavy and open, a silence of 0.5 s between \"Probably\" and \"nothing\", his eyes INTO THE LENS on \"nothing\", one blink after the line; a courtier on the right shifts his weight at 7.6 s; at 8.5 s another courtier clears his throat and turns his head, the king's eyes flick toward him for 0.3 s and return to the lens at 8.8 s with the lids open. "
    "9.6-10 s: a flat stare into the lens, the head level, the lips closed, one brow rising for 0.2 s. "
    "CAMERA SCORE in absolute amounts, written in what the viewer sees (hand-held while walking at arm's length, eye level; the whole wig and the long curls stay inside the picture at every moment; the wig top never rises above its starting height; the wig top has only 3 percent of free wall and the long curls on the left only 5 percent, so the king and the hall only slide toward the right edge of the picture and the picture only rises so that the king sinks lower in the frame): "
    "0.3-4.8 s: the picture rises so the king sinks 3 percent in the frame and holds that level, the king and the hall slide toward the right edge of the picture by 6 percent, a step bob of 1 percent mostly as roll, the roll about 5 degrees clockwise; "
    "4.8-6.0 s: the king and the hall slide 3 percent more toward the right edge, the picture rises 2 percent more, the roll eases to 4 degrees; "
    "6.0-7.0 s: a downward jolt of 2 percent with the laugh, the blur never longer than 0.3 s; "
    "7.0-9.6 s: the king gets 2 percent smaller, never larger, as the camera takes a slow step back; "
    "at 8.9 s (allowed window 6 to 9.6 s) a pink fingertip enters at the bottom left edge, 12 percent of the width, and leaves at 9.5 s, far from the face; "
    "9.6-10 s: the frame settles at a roll of 5 degrees. "
    "His lips form every spoken word clearly (the voice is added later); in the silent beats the mouth is closed. "
    "POSE SCORE as verbs: walk, glance aside, sweep, look into the lens, search, sigh, laugh, tip the head, hold the stare, flick the eyes, blink, raise a brow; the acting is natural and plain, as a real person films himself; "
    "no expression lasts longer than 2 seconds. "
    "Acting limits: ordinary blinks aside the eyes are open at every moment except the laugh slits, the face stays natural, five natural fingers on each hand. "
    "The camera moves only as small hand shakes and small re-aims by hand; the frame follows the hand. "
    "Sound: only the low murmur of a large hall, footsteps, fabric, candle flicker, breath, room tone, no music. "
    "A clean picture with no text, only things of the 1680s, no modern objects, one king in the frame. "
)

body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "t7aw_start_4k.jpg"],
        "duration": 10, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}
open(H0 + "take_t7aw_seedance_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t7aw_seedance.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=500, every=10)
    open(H0 + "pilot_frames/TAKE_t7aw_seedance.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t7aw_seedance.mp4"); print("saved")
