"""Take 5 piece 5a CLIP v2 on Seedance 2.5 LITE i2v (owner 07.11: Переделать): first frame ONLY (refs/t5a_start_4k.jpg), 720p, 12 s, 9:16, $0.15/s = $1.80, audio off. Fixes against v1 (inspector + comparator): eyes stay open on the ceiling look, visible torso and left-hand motion, delight eyes closed only 9.0-9.8 s, operator thumb 8.5-9.1 s, lower camera. One call, no retries without a new yes. Run: python3 gen_take_t5a_seedance_v2.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = (
    "The first frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. "
    "Realistic live action, real skin texture, sharp focus on the face at all times except the one named focus hunt. "
    "The same king in every frame: the same face, age about 45, heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white, the scarlet velvet coat with gold suns, lace cravat; "
    "the candlelit gilded hall behind him lit by wall sconces; the food in the foreground stays soft at the edges. "
    "The picture is a hand-held shot filmed by Marcel, very low at the near corner of the long table looking along it; from 0.5 s the frame sinks about 8 centimetres toward the tablecloth by 2.5 s while it tilts up so the wig stays inside. "
    "0-2.5 s: he says \"Then salad, ham, pastry, fruit.\" "
    "his eyes follow his own raised fingers down and to the right, heavy lids, closed-lip smirk, he counts on a finger with each word (at 0.4, 1.0, 1.6 and 2.2 s), the head turns half a face width left and right, on \"fruit\" his eyes lift to the lens; "
    "his left hand (the viewer's left) rests on the cloth beside the napkin and at 3 s and again at 7 s it lifts and drums its fingers on the cloth; at 1.5 s the lady with the open fan at the back right lifts her fan. "
    "2.5-4.5 s: he says \"In under an hour.\" "
    "he gives up counting, his right counting hand drops to the cloth, his eyes stay OPEN and look up to the ceiling for 0.4 s, the lids do not close for longer than a blink, a short breath through the nose, brows up, then his eyes return to the lens with an amused surrender, both shoulders lift visibly by about 3 centimetres at 3.2 s and his torso rocks back a little; "
    "at 4 s a courtier at the right centre steps behind him from right to left; "
    "at 4.5 s the picture softens for 0.5 s and snaps sharp. "
    "4.5-6.5 s: silent, "
    "his eyes drop to the dish of peas, brow up, a sly half smile, the lips pucker, two fingers of his right hand pick up ONE pea and lift it toward the lens, his torso leans 3 centimetres toward the pea at 6 s; "
    "at 5.5 s the servant far right turns his head. "
    "6.5-9 s: he says softly \"And peas. The court talks of nothing else.\" "
    "his eyes touch the pea for 0.2 s at 6.5 s, then look INTO THE LENS from 6.7 to 7.7 s while the pea is held beside his cheek, then slide right to the court for 0.5 s and back, one brow rises on \"nothing else\", the pea hand wobbles about 2 cm, the head tilts 10 degrees to the right; "
    "at 7.5 s the two courtiers at the right centre whisper behind him; at 8.5 s the servant crosses behind with a dish. "
    "9-12 s: silent, "
    "at 9.0 s the pea goes into his mouth, from 9.0 to 9.8 s his eyes are closed in delight and the head tips back 5 degrees, at 9.8 s his eyes OPEN again and stay open, a closed-lip chew, one corner of the mouth up, a happy hum, his torso leans back at 9 s; "
    "at 10.5 s his eyes drift down and to the right to the next dish, at 11.3 s they glance into the lens; his right hand returns to the cloth beside the dish of peas and the fingers rub together; "
    "at 10 s a lady far right fans herself faster. "
    "CAMERA SCORE in absolute amounts (hand-held, low; the king and the room stay in place while the frame moves; the whole wig and face stay inside the frame at every moment): "
    "0-2 s: a drift left by 8 percent, the roll builds to about 10 degrees left by 1.5 s, a push-in of 5 percent at 1.5 s drifting toward the cloth, the wig top never closer than 2 percent to the top edge; "
    "2-4 s: the frame dips 4 percent with the shrug and returns within 0.6 s, the wig top never closer than 2 percent to the top edge; "
    "at 4.5 s the focus hunt for 0.5 s; "
    "4.5-6.5 s: a slow push-in of 6 percent drifting toward the pea hand and the cloth, the wig top never closer than 2 percent to the top edge; "
    "6.5-9 s: a drift right by 8 percent and the roll easing to about 4 degrees; "
    "at 8.5 s (allowed window 6.5 to 10.5 s) the tip of Marcel's thumb enters at the bottom right edge, 12 percent of the width, from 8.5 to 9.1 s only, then it leaves the frame and the bottom edge stays clear for the rest of the clip, far from the face and from the pea hand; "
    "9-12 s: a settling sway of 3 percent. "
    "His lips form every spoken word clearly (the voice is added later); in the silent beats the mouth is closed or chewing. "
    "POSE SCORE as verbs: count, shrug, look up, drum, lift, pick, lean, hold, look, tilt, eat, open, hum, glance; "
    "no expression lasts longer than 2 seconds. "
    "Acting limits: ordinary blinks aside the eyes are open at every moment except 9.0 to 9.8 s, the face stays natural, five natural fingers on each hand. "
    "All moves are small shakes and re-aims by hand: no whip pans, never a zoom, a gimbal or a dolly. "
    "Sound: only the low murmur of a large hall, fabric, cutlery, candle flicker, breath; no music at all. "
    "Clean picture with no text or captions, no modern objects, only things of the 1680s, one king in the frame. "
)

body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "t5a_start_4k.jpg"],
        "duration": 12, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}
open(H0 + "take_t5a_seedance_v2_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t5a_seedance_v2.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t5a_seedance_v2.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t5a_seedance_v2.mp4"); print("saved")
