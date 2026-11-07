"""Take t4bA CLIP on Seedance 2.5 LITE i2v (owner 07.11: Seedance 2.5 Lite): image_urls[0] = first frame, [1] = last-frame constraint (APIpod spec seedance--2-5-lite-image-to-video), 720p only, 10 s, $0.15/s = $1.50, audio off (the model audio is always muted). Same prompt as gen_take_t4bA.py (Kling) with the tag wording changed. One call, no retries without a new yes. Run: python3 gen_take_t4bA_seedance.py go
BRIEF: briefs/brief_t4b_A_B.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = (
    "The first frame is the exact starting frame: "
    "for the first 0.3 s keep it as it is, then animate from it. "
    "the same two people as in the frames: "
    "the king (the same man of about 45 as in the first frame: "
    "heavy-lidded grey-green eyes, thin dark waxed moustache with curled tips, a small dark beauty mark on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white, the scarlet velvet coat with gold suns) and Marcel (a young servant with freckles and thick dark brows, a plain white wig, a pale blue livery coat with silver braid), filmed by a hand-held camera at table height from the side of the long table, medium-wide, both heads with their wigs fully in the frame (the king in the left part, Marcel in the right part), in the candlelit gilded hall. "
    "At the end, 10 s, the frame is as the last frame (the goblet lies on its side in a pool of red wine on the cloth, Marcel straightened up with open raised hands looking at the king, the king turned three-quarter toward Marcel holding back a laugh). "
    "Realistic live action, real skin texture, no beauty filter. "
    "0-2 s: "
    "Marcel carries the gold goblet on the small tray in both hands toward the king from the viewer's right, bent and tense; "
    "the king waits expectant and amused, his eyes on the goblet, one eyebrow up, lips pressed into a smirk, the fingers of his ringed hand drumming on the cloth, one slow blink at 1.2 s; "
    "at 1 s the courtier in the dark coat in the middle background shifts his weight; "
    "2-2.5 s: "
    "Marcel's foot catches, he lurches, the tray drops flat onto the white tablecloth at the right and the goblet falls and rolls to rest on its side with its mouth toward the king; "
    "the king's eyes snap from the goblet to the spill, his eyebrows shoot up, his eyes widen a little (the lids stay heavy), a short sharp breath in, his fingers stop drumming; "
    "2.5-3.5 s: "
    "the red wine pours over the cloth and stops at the edge of the king's cuff (a natural spill: "
    "it does not fly, it pours and spreads on the cloth); "
    "the king's eyes rise to Marcel's face, the corner of his mouth twitches; "
    "he lifts his hand off the cloth and puts it back on the same spot by 8 s; "
    "3.5-5.5 s: "
    "Marcel straightens up with both hands flying up open at the height of his chest, his eyes go straight into the camera; "
    "at about 4.5 s the king, caught and amused, looks into the lens for 0.7 s and then back at Marcel with one eyebrow up and a small grimace of disbelief; "
    "at 4 s the lady with the fan at the right back turns her head toward them; "
    "5.5-7 s: "
    "Marcel says very quietly, his lips moving: "
    "\"Sorry, Sire.\" and bows his head a little, looking up at the king; "
    "the king, while Marcel speaks, presses his lips together to keep from laughing, his nostrils flare, his shoulders give one slight tremble, his eyes bright; "
    "7-10 s: "
    "the king's smile breaks through at the corner of his mouth, his eyes shine, he keeps looking at Marcel, then at the lens, his head tilting about 10 degrees (his eyes open the whole time; "
    "they never close for longer than 0.5 s); "
    "Marcel keeps both hands raised open (trembling slightly) and looks at the king, then at the lens; "
    "the two wigged courtiers in the middle background whisper to each other at 8 s; "
    "the frame settles to the last frame. "
    "EMOTION SCORE (strength 0-3, never one expression longer than 2 s): "
    "king 0-2 s expectant amusement (1), 2-2.5 s shock (2), 2.5-3.5 s disbelief with a twitch (2), 3.5-5.5 s caught and amused, one look into the lens (2), 5.5-7 s holding back laughter (2-3), 7-10 s a smile breaking through (3); "
    "Marcel 0-2 s tense (1), 2-3.5 s horror (3), 3.5-7 s frozen in shock then apologetic (2-3), 7-10 s relieved and trembling (2). "
    "Every reaction starts 0.3 to 0.5 s after its event. "
    "CAMERA SCORE in absolute amounts (hand-held; "
    "the people and the room stay in place while the frame moves; "
    "both heads are near the edges of the safe area, so every move is small and keeps both wigs inside the frame): "
    "every 2 seconds the frame shifts by 3 to 5 percent of its width and rolls by 2 to 3 degrees: "
    "0-2 s a slow drift to the left by 3 percent with the roll easing 3 degrees; "
    "2-2.5 s a quick re-aim down toward the spill by 4 percent; "
    "2.5-4 s a sway back to the first framing; "
    "at about 4.2 s (after the goblet has fallen and the spill is seen) the whole picture blurs for 0.5 s, then snaps sharp; "
    "4-6 s a slow push-in of 4 percent toward the centre of the frame; "
    "at about 6 s (the allowed window is 4 to 8 s) a thumb slips into the lower left corner covering the lower left 15 percent of the frame width (never more than 20 percent) for 0.6 s and never a face; "
    "6-8 s a drift to the left by 3 percent and a small sag; "
    "8-10 s a drift back by 3 percent, a push-back of 4 percent and settle to the framing of the last frame. "
    "POSE SCORE as verbs with times: "
    "0-2 s carry, drum, blink, shift; "
    "2-3.5 s lurch, tip, fall, snap the eyes, pull back; "
    "3.5-5.5 s straighten, throw up the hands, stare into the lens, glance; "
    "5.5-7 s speak, bow, press the lips, tremble; "
    "7-10 s smile, tilt, glance, tremble; "
    "the heads move by turns and nods of 3 to 5 percent of the frame width in each 2-second window; "
    "never a hold longer than 2 seconds; "
    "Marcel's raised hands tremble. "
    "THE ROOM IS ALIVE: "
    "candle flames flicker; "
    "at 1 s the courtier in the dark coat in the middle background shifts; "
    "at 4 s the lady with the fan at the right back turns her head; "
    "at 6 s a servant in livery far behind crosses from right to centre; "
    "at 8 s the two wigged courtiers in the middle background whisper. "
    "Acting limits: "
    "heavy eyelids stay except in the laugh beats, no wide-open eyes for the king, the face stays natural, hands have five natural fingers. "
    "No whip pans and no zoom lens, all moves by hand; "
    "no gimbal, no dolly or flying camera. "
    "Sound: "
    "only diegetic, low murmur of a large hall, fabric, cutlery, candle flicker, his voice and breath; "
    "no music at all. "
    "No text or captions, no modern objects, no clear glass or crystal glass anywhere, only one king in the frame (no second king, no double). "
    " "
)
body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "t4bA_start_4k.jpg", RAW + "t4bA_end_4k.jpg"],
        "duration": 10, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}
open(H0 + "take_t4bA_seedance_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t4bA_seedance.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t4bA_seedance.status.json", "w").write(re.sub(r'(https://[^"?]+)\\?[^"]*', r'\\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t4bA_seedance.mp4"); print("saved")
