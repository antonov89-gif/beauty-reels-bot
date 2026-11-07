"""Take 5 piece 5b CLIP on Seedance 2.5 LITE i2v (07.11): image_urls[0] = first frame ONLY (owner rule 07.11: no end still when the next piece is a cut), 720p, 5 s, 9:16, $0.15/s = $0.75, audio off. Built from briefs/brief_t5_t7.md BRIEF 5b (no words: chewing, a hum, the murmur of the crowd; tilt-up re-aim 1.8-2.6 s with a 0.4 s blur during the tilt only; ONE look into the lens 3.2-3.8 s; eyes shut 0.5 s at 4.2 s; thumb 12 % at 4.4 s for 0.5 s). One call, no retries without a new yes. Run: python3 gen_take_t5b_seedance.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = (
    "The first frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. "
    "Realistic live action, real skin texture, sharp focus on the face except 1.9 to 2.3 s during the tilt. "
    "The same king in every frame: the same face, age about 45, heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark below the mouth exactly as in the first frame, light rouge, the tall powdered wig in cool silver-grey and white, the scarlet velvet coat with gold suns, lace cravat, napkin at the cravat; "
    "the candlelit gilded hall behind him lit by wall sconces. "
    "The picture is a hand-held shot filmed by Marcel from a little above the laden table, tilted down, the king sits at the far end of the table, his face about 19 percent of the frame width. "
    "The room is quiet apart from the murmur of the crowd, cutlery and the king's contented hum. "
    "0-1.8 s: "
    "he chews slowly with relish, the jaw moves, one cheek is lightly full, eyes open under heavy lids resting on the roast in front of him, a happy closed-mouth hum; "
    "his hands stay behind the dishes; at 1 s a servant's gloved hand enters from the right edge and sets a dish down. "
    "1.8-3.2 s: "
    "he swallows, his eyes are open, a pleased brow lift, his right hand (the viewer's left) rises from behind the dishes with a bite of roast to his mouth; "
    "at 2.5 s a courtier at the right centre shifts his weight and the lady behind him raises her fan higher. "
    "3.2-4.2 s: "
    "he notices the camera and looks INTO THE LENS from 3.2 to 3.8 s while chewing, a smug lift of the chin, then his eyes return to the dishes at 3.8 s, the mouth keeps chewing; two courtiers whisper behind him at the right centre. "
    "4.2-5 s: "
    "he shuts his eyes from 4.2 to 4.6 s in relish, they are open again by 4.7 s, and he glances down at the plate for the next bite from 4.7 to 5 s. Everything on the table stays exactly where it is, only the food the king lifts and the dish the servant sets down move; the tall silver candlestick and the gold fruit bowl at the left stay still; the king's hands touch only food. "
    "CAMERA SCORE in absolute amounts (hand-held; the king and the room stay in place while the frame moves; the whole wig and face stay inside the frame at every moment and the wig top stays at least 2 percent inside the top edge): "
    "0-1.8 s: a drift left by 6 percent over the pheasant and the ham, the roll held at about 7 degrees to the right; "
    "1.8-2.6 s: a re-aim, the frame tilts up by about 25 percent of its height toward the king in 0.8 s, the picture softens for 0.4 s during the tilt only, then the king is sharp again; "
    "2.6-3.2 s: a slow settle, a drift right by 2 percent; "
    "3.2-4.2 s: a slow push-in of 4 percent; "
    "at 4.4 s (allowed window 3.5 to 4.8 s) the tip of Marcel's thumb enters at the bottom right edge, 12 percent of the width, a pink fingertip enters at 4.4 s and leaves at 4.9 s, far from the face; "
    "4.2-5 s: a sway back of 3 percent and a settle. "
    "POSE SCORE as verbs: chew, hum, swallow, lift the brow, raise the bite, look into the lens, lift the chin, shut the eyes briefly, open, look down; "
    "no expression lasts longer than 2 seconds. "
    "Acting limits: the eyes are open except 4.2 to 4.6 s, the face stays natural, five natural fingers on the hand. "
    "The camera moves only as small hand shakes, re-aims and one slow hand-held push-in, no whip pans; the frame follows the hand. "
    "Sound: only the low murmur of a large hall, cutlery, candle flicker, a contented hum; no music at all. "
    "Clean picture with no text or captions, no modern objects, only things of the 1680s, one king in the frame. "
)

body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "t5b_start_4k.jpg"],
        "duration": 5, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}
open(H0 + "take_t5b_seedance_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t5b_seedance.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t5b_seedance.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t5b_seedance.mp4"); print("saved")
