"""Take 5 piece 5c CLIP v2 on Seedance 2.5 LITE i2v (07.11): first frame ONLY (refs/t5c_start_4k.jpg), 720p, 12 s, 9:16, $0.15/s = $1.80, audio off. Rework of v1 (owner 07.11: quality poor, tear looks AI, realism): no tear wipe, eyes open from 0.8 s and on the glance to the lady, natural laugh 9.2-10.4 s with a plain breath after, laugh shake 2 %, thumb 8.3-8.9 s, wig margin 12 %. One call, no retries without a new yes. Run: python3 gen_take_t5c_seedance_v2.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = (
    "The first frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. "
    "Realistic live action, real skin texture, sharp focus on the face except 4.0 to 4.5 s. "
    "The same king in every frame: the same face, age about 45, heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark below the mouth exactly as in the first frame, light rouge, the tall powdered wig in silver-grey and white, the scarlet velvet coat with gold suns, lace cravat; "
    "he leans back in the carved gilded armchair, the candlelit gilded hall around him lit by wall sconces. "
    "The picture is a hand-held shot filmed by Marcel at arm's length from in front of and high above the king, looking down at him. "
    "0-2 s: he says a long happy \"Ohh...\" "
    "his eyes stay closed until 0.8 s, then open slowly onto the lens with heavy lids and stay open, the chest rises and falls, the lips are parted, both hands rest on his belly; at 1.5 s a servant far at the right crosses. "
    "2-4.5 s: he says \"I wasn't born to work.\" "
    "his face is flat, then a sly smile, the brows rise on \"work\" and his eyes look INTO THE LENS, his right hand pats the belly twice at 3.5 s, the head tilts 8 degrees, then a silent pause of 0.6 s from 3.9 to 4.5 s, the lips closed in a sly smile, the brows still up; at 3 s a courtier's wig at the right centre turns toward him. "
    "4.5-8 s: he says \"I was born for happiness, love, pleasure... and a good rest.\" "
    "on \"happiness\" his eyes look up to the ceiling, dreamy and open, on \"love\" his eyes stay open and slide right to the lady with the fan for 0.6 s, one hand lifts and rolls in the air for 0.8 s and goes back down, on \"pleasure\" his eyes return to the lens with one brow up, then a silent beat of 0.6 s, his lids half lowered and a tiny smile, before \"and a good rest\"; "
    "at 5.5 s the lady with the fan at the right turns her face to him; at 7 s a servant crosses behind. "
    "8-9 s: silent, his face is flat, a half blink, his eyes on the lens, the lips pressed together to hold it back, the hands still; two courtiers whisper behind him at the right centre. "
    "9-11 s: a natural laugh from 9.2 to 10.4 s, his eyes narrowed but visible, from 10.4 to 11 s the laugh fades into a plain breath, the head drops forward then rears back, the mouth open, the eyes squeezed into open slits (shut for no longer than 0.5 s), the shoulders shake, one hand pats the belly; "
    "a courtier at the right centre bows a little and a lady laughs politely at 10 s. "
    "11-12 s: the recovery, the chin up, the eyes OPEN, a plain breath out, a glance into the lens for 0.6 s, a small natural smile, the last frame with open eyes. "
    "CAMERA SCORE in absolute amounts (hand-held at arm's length, high; the king and the room stay in place while the frame moves; the whole wig and face stay inside the frame at every moment, the wig puff never closer than 6 percent to the top edge, the long side curls never cut by the edge and the camera stays far enough back that the wig keeps at least 12 percent clear on each side, the camera shakes sideways less than it moves vertically): "
    "0-2 s: a drift left by 6 percent while the picture rolls to about 14 degrees clockwise and holds it, the wall verticals leaning to the right; "
    "2-4.5 s: a slow push-in of 4 percent toward the face; "
    "4.0 to 4.5 s the focus hunt, the whole picture soft for 0.5 s, then sharp; "
    "4.5-8 s: a drift right by 7 percent, a tilt up of 4 percent following the gaze and back at 7 s; "
    "at 8.3 s (allowed window 4.5 to 10 s) the tip of Marcel's thumb enters at the bottom right edge, a pink fingertip 12 percent of the width, and leaves at 8.9 s, far from the face and from the hands; "
    "8-9 s: a slow sway of 3 percent; "
    "9-11 s: the camera shakes only a little with the laugh, 2 percent, the face stays sharp with no motion blur; "
    "11-12 s: the frame settles. "
    "His lips form every spoken word clearly (the voice is added later); in the silent beats the mouth is closed or smiling. "
    "POSE SCORE as verbs: sigh, open the eyes, smile slyly, look into the lens, pat, tilt, look up, slide the gaze, roll the hand, hold back, laugh, breathe out, glance; the acting is natural and plain, as a real person films himself; "
    "no expression lasts longer than 2 seconds. "
    "Acting limits: ordinary blinks aside the eyes are open at every moment except 0 to 0.8 s and the laugh slits, the face stays natural, five natural fingers on each hand. "
    "The camera moves only as small hand shakes and re-aims by hand, no whip pans; the frame follows the hand. "
    "Sound: only the low murmur of a large hall, fabric, candle flicker, breath; no music at all. "
    "Clean picture with no text or captions, no modern objects, only things of the 1680s, one king in the frame. "
)

body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "t5c_start_4k.jpg"],
        "duration": 12, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}
open(H0 + "take_t5c_seedance_v2_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t5c_seedance_v2.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t5c_seedance_v2.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t5c_seedance_v2.mp4"); print("saved")
