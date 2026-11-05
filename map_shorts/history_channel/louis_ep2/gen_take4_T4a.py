"""Take 4, piece 4a "The drink" (setup S9). Kling 4.0 i2v 720p 12 s = $1.74 (0.145 x 12): 17 spoken words at 0.55 s each = 9.4 s plus the finger, the cup passing and the wait. first = T4a start still, last = T4a end v2 still (owner quality exception for detail 1.89). Lines (script 7.3): "No glass on my table. Thirsty? I just... [lifts one finger without looking] / CUPBEARER (off screen): A drink for the King! / [the cup goes from hand to hand behind him; he waits, drumming his fingers] ...and I wait." Motion score per PROMPT_CAMERA_LESSONS.md (absolute camera amounts, head travel, verbs, named people with seconds). Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("@first_frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), thin dark waxed moustache with curled tips, beauty mark on the viewer's right of the mouth, light rouge, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded hall seen from across the long dining table from slightly above, the king in the right third of the frame, the table edge running diagonally with the candelabra receding to the left, the cloth in front of him bare around his plate (no glass, goblet or cup on the table at any time). At the end, 12 s, the frame is exactly as @last_frame (his eyes up and aside toward the chandelier, bored under heavy lids, mouth closed, the left eyebrow slightly raised, the ringed hand on the cloth drumming with the index finger lifted a little, the cupbearer gone from the left, two white-gloved hands passing a gold goblet at the right edge behind the chair); the room and the king are in the same place in @last_frame as in @first_frame, only the pose, the gaze and the goblet differ. Realistic live action, real skin texture, no beauty filter. "
"0-1 s: he looks into the lens with a bored haughty stare, the ringed hand flat on the cloth. "
"1-3.5 s: he says flatly: \"No glass on my table.\" with his head tilting to the left and one eyebrow climbing; on the left the lady in the gold gown whispers to her neighbour behind her fan. "
"3.5-4.8 s: his chin lifts and his eyes wander over the hall while he says: \"Thirsty?\" and, after a short pause, \"I just...\" "
"4.8-5.5 s: without looking at it, he raises the index finger of the ringed hand to chest height beside the cravat (below his chin, not covering his face), his eyes already turned away up and to the left toward the chandelier. "
"5.5-8 s: from off screen a cupbearer's voice shouts \"A drink for the King!\" (the king does not react and does not look); at 6 s a courtier in a dark coat at the right edge turns his head toward the shout; his raised hand sinks back to the cloth. "
"8-10.5 s: he waits, drumming the fingers of the ringed hand on the cloth (the index lifts and falls), his head tilting to the right; at the right edge behind the chair, between two standing courtiers, two white-gloved hands pass a gold goblet from one to the other in soft focus, and at 9 s a courtier on the left shifts his weight. "
"10.5-12 s: flatly and quietly he says: \"...and I wait.\" with his chin up and his eyes up toward the chandelier, then a silent held beat in the pose of @last_frame. "
"CAMERA SCORE in absolute amounts (the page Marcel films from across the table on a phone in one hand; the king and the room stay in place, the frame moves): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a drift to the right while the roll of about 8 degrees to the right eases to 5 degrees; 2-4 s a push-in on the king by about 6 percent; 4-5 s the phone jerks to the left and comes back; at 6.5 s the page's own pink thumb covers the left 15 percent of the frame for about 0.6 s (phone mistake); 5-8 s a slow tilt down by about 3 degrees and back; 8-10 s a slow sway to the left; 10-12 s the frame settles back to the framing of @last_frame with its roll of about 8 degrees to the right. "
"POSE SCORE as verbs: stare, tilt left, brow up, chin up, wander, finger up, eyes away, sink, drum, tilt right, chin up; his head crosses at least half of its own width every 2 seconds. "
"THE ROOM IS ALIVE: candle flames flicker, ladies whisper behind their fans, standing courtiers shift their weight; the background people keep their faces, only small natural movements. "
"Acting limits: heavy eyelids stay, no wide-open eyes, no broad grin, the face stays turned toward the frame centre and natural, exactly five fingers on the hand with the same four rings, the face never covered by the hand. "
"No whip pans and no zoom lens: the only quick move is the jerk at 4-5 s, all by hand; no gimbal, no dolly or flying camera. "
"Sound: only diegetic, low murmur of a large hall, a distant footstep, fabric, candle flicker; no music at all. No text or captions, no modern objects, only one king in the frame (no second face, no double).")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T4a_start_4k.jpg", RAW + "T4a_end_v2_4k.jpg"],
        "duration": 12, "resolution": "720p"}
open(H0 + "take4_T4a_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE4_T4a.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE4_T4a.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE4_T4a.mp4"); print("saved")
