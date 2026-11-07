"""Take 4 piece 4b-2 Marcel through the wine (setup S10): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 8 s = $1.16 (0.145 x 8). first = t4b2_start_4k, last = t4b2_end_4k. Lines (script 7.3): LOUIS (off screen): "And nobody will see you again." [Marcel freezes; pause] "Joking." MARCEL (quietly): "Sorry, Sire." Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes.
BRIEF: briefs/brief_t4b2.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"Marcel exactly as in the reference (his face only; "
"the terrified look is described in words): "
"a young frightened servant with freckles, thick dark brows, a plain white wig and a plain blue livery coat, nothing of the king's red coat or tall silver wig, in the same candlelit gilded hall, filmed on the king's own hand-held phone from a seated eye level, looking slightly up at Marcel, a red wine film on the left third of the lens that stays there all the time (it never grows past 35 percent of the width and never touches Marcel's face). "
"At the end, 8 s, the frame is exactly as @last_frame (Marcel bowed a little, relieved, mid-word 'Sorry, Sire'). "
"Realistic live action, real skin texture, no beauty filter. "
"The king is not in the frame: "
"his voice is off screen and the lens is his. "
"0-1 s: "
"Marcel stands rigid and pale, lips pressed, eyes on the lens, a bead of sweat at his temple; "
"at 0.5 s his eyes flick to the left toward the wine film and back; "
"behind him at the right back the lady with the fan stops fanning and turns her head toward him. "
"1-3.3 s: "
"the king's voice says off screen, flat and quiet: "
"\"And nobody will see you again.\" his chin dips, his eyes flick to the courtier and back, his shoulders lift on the breath, his eyes widen a little and his throat swallows at 2 s, his breathing quickens, his lips tremble once, the rest of him does not move; "
"at 2 s a courtier behind his right shoulder glances at him and away. "
"3.3-4.6 s: "
"the silent beat of 1.3 s: "
"Marcel freezes completely, only one eyelid twitches and the sweat bead runs down; "
"the candle flames flicker; "
"the camera keeps moving. "
"4.6-5.4 s: "
"the king's voice, light: "
"\"Joking.\" and a short exhale of a laugh; "
"Marcel's shoulders drop and the breath leaves him, the head bowing forward. "
"5.4-6.8 s: "
"Marcel says very quietly, his lips moving: "
"\"Sorry, Sire.\" while bowing his head forward about 8 degrees and looking up into the lens, a trembling half-smile. "
"6.8-8 s: "
"he straightens a little and glances away to the right at the courtier, then back at the lens, the frame settling to @last_frame. "
"CAMERA SCORE in absolute amounts (the king's own phone in one hand; "
"Marcel and the room stay in place while the frame moves; "
"Marcel's face is at 46 percent of the width and his wig a little wider, so every move keeps his face and wig inside the frame, the free margin is about 12 percent on each side): "
"every 2 seconds the frame shifts by 8 to 10 percent of its width: "
"0-2 s a slow drift to the right by 8 percent with the roll easing by 3 degrees and a push-in of 5 percent; "
"2-4 s a small push-in and a shake of the king's hand as he speaks, then a sag to the left by 8 percent; "
"at about 2.5 s the whole picture blurs for 0.5 s, then snaps sharp; "
"4-5 s the phone jerks up and comes back as he laughs; "
"5-7 s a slow sway to the right by 8 percent and a tilt down by 4 degrees; "
"at about 5.5 s (the allowed window is 3.5 to 7.5 s) the king's own pink thumb slips into the lower right corner covering the lower right 15 percent of the frame width (never more than 20 percent) for 0.7 s and never Marcel's face (phone mistake); "
"7-8 s a last small sway back to the framing of @last_frame. "
"POSE SCORE as verbs: "
"stiffen, flick, swallow, tremble, freeze, twitch, exhale, bow, glance; "
"Marcel's head moves about half of its own width (about 23 percent of the frame width) in each 2-second window, alternating left and right and ending near the centre; "
"never a stillness of the camera longer than 2 seconds. "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 1 s the lady with the fan at the right back turns her head; "
"at 2 s the courtier behind Marcel's right shoulder glances at him; "
"at 6 s a servant behind him on the right walks across from right to the centre; "
"at 4 s two courtiers at the right whisper to each other. "
"Acting limits: "
"the face stays natural, hands have five natural fingers. "
"No whip pans and no zoom lens, all moves by hand; "
"no gimbal, no dolly or flying camera. "
"Sound: "
"only diegetic, low murmur of a large hall, fabric, cutlery, candle flicker, his voice and breath; "
"no music at all. "
"No text or captions, no modern objects, no clear glass or crystal glass anywhere, no king in the frame, only Marcel. "
)

body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "t4b2_start_4k.jpg", RAW + "t4b2_end_4k.jpg"],
        "duration": 8, "resolution": "720p"}
open(H0 + "take_t4b2_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t4b2.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t4b2.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t4b2.mp4"); print("saved")
