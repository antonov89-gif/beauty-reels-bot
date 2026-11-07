"""Take 6 (the verdict) CLIP on Seedance 2.5 LITE i2v (07.11): image_urls[0] = first frame ONLY (owner rule 07.11: no end still when the next piece is a cut), 720p, 15 s, 9:16, $0.15/s = $2.25, audio off. Built from briefs/brief_t5_t7.md BRIEF 6 with the 07.11 changes: the start pin looks into the lens (self-filmed vlog look), so the glance down to the bones happens at 0.4-1.2 s; no leftward drift and no push-in (the pin has a 5-8 % left margin); realism rule (no theatrical gestures, no tears). LOUIS (OWNER): "[wipes his fingers, sits up, glances at the bones on his plate, pushes the plate a little away] So. Do I eat too much? ...No. I eat like a king. [chin up] Don't be afraid of getting fat. Be afraid of being a loser. [haughty laugh]" One call, no retries without a new yes. Run: python3 gen_take_t6_seedance.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = (
    "The first frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. "
    "Realistic live action in the look of a hand-held vlog that he films of himself, real skin texture, sharp focus on the face except 7.5 to 8.0 s. "
    "The same king in every frame: the same face, age about 45, heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark below the mouth exactly as in the first frame, light rouge, the tall powdered wig in silver-grey and white, the scarlet velvet coat with gold suns, lace cravat; "
    "the candlelit gilded hall behind him lit by wall sconces; the sleeve and the back of the hand at the lower right edge of the frame stay as in the first frame and hold nothing. "
    "0-2.5 s: he is wiping his fingers on a lace napkin with the hand below the frame, "
    "from 0 to 0.3 s his eyes are on the lens, from 0.4 to 1.2 s his eyes drop to the bones on the plate with a complacent smirk, at 1.5 s his eyes rise to the lens again, at 2 s the edge of the plate slides about 10 centimetres away; at 1 s the lady with the open fan at the back right turns toward him. "
    "2.5-5.5 s: he says \"So. Do I eat too much?\" "
    "his eyes are INTO THE LENS, the brows rise slightly on \"too much\", the head tilts 8 degrees to the right; two courtiers whisper behind him at the right centre at 3.5 s. "
    "5.5-8 s: a silent pause of 0.8 s and then \"...No.\" "
    "his face is flat and deadpan, the lids heavy and open, the eyes on the lens, one blink at 7.0 s; the whispering stops. "
    "8-10.5 s: he says \"I eat like a king.\" "
    "the chin goes up 10 degrees, he looks down his nose into the lens, one corner of the mouth rises; a courtier at the right centre bows a little at 9.5 s. "
    "10.5-13 s: he says softly \"Don't be afraid of getting fat. Be afraid of being a loser.\" "
    "after a pause of 0.7 s, a slow head shake of 6 degrees on \"fat\", the eyes narrow on \"loser\", one brow rises, a squint of one eye at 12.5 s; the fan flutters and a servant crosses behind him at 12 s. "
    "13-15 s: a short haughty laugh of at most 1.2 s, the chin up, the upper teeth just visible, one brow raised, the eyes half-lidded and OPEN on the lens, the laugh switches off within 0.3 s, then a smug flat smirk with a small sniff for the last 0.7 s and a glance to the left at the court. "
    "CAMERA SCORE in absolute amounts (hand-held at arm's length, eye level; the king and the room stay in place while the frame moves; the whole wig and face stay inside the frame at every moment; the long curls on the left have only 5 to 8 percent of free wall, so the frame never drifts left and never pushes in): "
    "0-2.5 s: a drift right by 3 percent, the roll held at about 4 degrees to the left; "
    "2.5-5.5 s: a drift right by 4 percent; "
    "5.5-8 s: a sway of 3 percent, the calm is the threat; the picture softens for 0.5 s at 7.5 s and snaps sharp; "
    "8-10.5 s: a quick dip down by 15 percent to the plate and back up within 1 s at 8.5 s, then a drift right by 3 percent; "
    "at 10 s (allowed window 8 to 13 s) the tip of Marcel's thumb enters at the bottom left edge, a pink fingertip 12 percent of the width, and leaves at 10.6 s, far from the face; "
    "10.5-13 s: a slow push-back of 3 percent and the roll easing to about 2 degrees to the right; "
    "13-15 s: the frame settles with a sway of 2 percent. "
    "His lips form every spoken word clearly (the voice is added later); in the silent beats the mouth is closed. "
    "POSE SCORE as verbs: wipe, glance down, look into the lens, tilt, wait, blink, lift the chin, shake the head, narrow the eyes, squint, laugh, sniff, glance aside; the acting is natural and plain, as a real person films himself; "
    "no expression lasts longer than 2 seconds. "
    "Acting limits: ordinary blinks aside the eyes are open at every moment, the face stays natural, five natural fingers on each hand. "
    "The camera moves only as small hand shakes and small re-aims by hand, no whip pans; the frame follows the hand. "
    "Sound: only the low murmur of a large hall, fabric, candle flicker, breath, room tone, no music. "
    "Clean picture with no text or captions, no modern objects, only things of the 1680s, one king in the frame. "
)

body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "t6_start_4k.jpg"],
        "duration": 15, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}
open(H0 + "take_t6_seedance_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t6_seedance.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t6_seedance.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t6_seedance.mp4"); print("saved")
