"""Take 5 piece 5a salad, ham, pastry, fruit, peas (setup S11): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 12 s = $1.74 (0.145 x 12). first = t5a_start_4k, last = t5a_end_4k. Lines (script 7.3): LOUIS: "Then salad, ham, pastry, fruit. [gives up counting] In under an hour. [holds a pea to the lens, softly] And peas. The court talks of nothing else. [eats it, delighted]" Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same king in every frame, always the face and look of the reference: "
"the same face, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden, the candlelight must not tint it), the scarlet velvet coat with a gold sun, lace cravat, the candlelit gilded hall behind him, filmed by Marcel with a hand-held phone held very low at the near corner of the long table looking along it; "
"the foreground food (ham, pastries, fruit, a tureen of peas) soft at the edges. "
"At the end, 12 s, the frame is exactly as @last_frame (he holds a green pea to the lens, a soft delighted half-smile); "
"the king and the room are in the same place in both frames. "
"Realistic live action, real skin texture, no beauty filter. "
"0-2.5 s: "
"he counts the dishes on his raised fingers with small nods, then shrugs and lets the hand fall: "
"\"Then salad, ham, pastry, fruit.\" at 2.5 s he gives up counting with a tolerant sigh; "
"at 1 s a servant in livery at the right back bends to move a dish. "
"2.5-5 s: "
"\"In under an hour.\" he lifts his chin proudly, then glances down along the table at the food; "
"at 4 s the lady with the fan at the left back leans to whisper to her neighbour. "
"5-7 s: "
"a silent beat of two seconds: "
"he reaches toward the tureen with two fingers and picks up one pea, looking at it tenderly; "
"the camera keeps moving. "
"7-9.5 s: "
"he lifts the pea toward the lens, softly: "
"\"And peas.\" then leans a little toward the lens with raised brows: "
"\"The court talks of nothing else.\" 9.5-12 s: "
"he eats the pea, closes his eyes and hums with delight, the head tipping back a little, then settles into the pose of @last_frame with the pea back between his fingers; "
"at 10 s a courtier behind him nods approvingly. "
"CAMERA SCORE in absolute amounts (Marcel's phone, low and hand-held; "
"the king and the room stay in place while the frame moves; "
"the king's face is at 42 percent of the width so every move keeps his face and wig inside the frame, the free margin is about 25 percent on each side): "
"every 2 seconds the frame shifts by 8 to 10 percent of its width: "
"0-2 s a slow creep along the table toward the king, a push-in of 6 percent and the roll easing by 3 degrees; "
"2-4 s a drift to the right by 9 percent over the food; "
"4-6 s a dip lower by 5 percent and a sag, then a lift; "
"6-8 s a push-in of 8 percent toward the pea as it rises; "
"at about 7 s (the allowed window is 5 to 9 s) the focus hunts: "
"the picture goes soft for half a second and snaps back sharp; "
"8-10 s a sway to the left by 8 percent; "
"at about 10.5 s (the allowed window is 8.5 to 11.5 s) Marcel's sleeve of blue brushes the left edge of the lens for 0.6 s; "
"10-12 s the frame settles back to the framing of @last_frame. "
"POSE SCORE as verbs: "
"count, nod, shrug, lift, glance, reach, pick, lift, lean, eat, hum; "
"the head moves about half of its own width (about 20 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; "
"never a hold longer than 2 seconds. "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 1 s the servant at the right back bends to a dish; "
"at 4 s the lady with the fan whispers to her neighbour; "
"at 8 s a courtier behind the king's left shoulder shifts his weight; "
"at 10 s a courtier nods. "
"Acting limits: "
"heavy eyelids stay except in the laugh beats, no wide-open eyes for the king, the face stays natural, hands have five natural fingers. "
"No whip pans and no zoom lens, all moves by hand; "
"no gimbal, no dolly or flying camera. "
"Sound: "
"only diegetic, low murmur of a large hall, fabric, cutlery, candle flicker, his voice and breath; "
"no music at all. "
"No text or captions, no modern objects, no clear glass or crystal glass anywhere, only one king in the frame (no second king, no double). "
)

body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "t5a_start_4k.jpg", RAW + "t5a_end_4k.jpg"],
        "duration": 12, "resolution": "720p"}
open(H0 + "take_t5a_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t5a.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t5a.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t5a.mp4"); print("saved")
