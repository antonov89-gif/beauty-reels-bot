"""Take 3, piece 3c "Fork or fingers?" (setup S8b, pins T3d). Kling 4.0 i2v 720p 10 s = $1.45 (0.145 x 10). first = T3d start still, last = T3d end still (both pass the quality limits, no exception). Lines: "Fork or fingers? Tell me in the comments. [swallows] Wrong answers go to the Bastille." Prompt carries the absolute motion score (PROMPT_CAMERA_LESSONS.md). Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("@first_frame is the exact starting frame: for the first 0.3 s keep it as it is, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), thin dark waxed moustache with curled tips, beauty mark, light rouge, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded hall, the phone level with his mouth, his face in the left half of the frame, the picked carcass on the silver platter at the lower edge. At the end, 10 s, the frame is exactly as @last_frame (he has swallowed, lips closed and glossy in a flat line, the leg lowered in his ringed fist pointing down toward the platter, a flat deadpan stare into the lens, one eyebrow slightly raised, a slight roll to the left); the room and the king are in the same place in @last_frame as in @first_frame, only the pose and the leg differ. Realistic live action, real skin texture, no beauty filter. "
"0-1.5 s: he is chewing, the cheek full, the leg held at the lens in the ringed fist, heavy bored lids, his stare into the lens; behind him on the right the lady in the gold gown with her fan whispers to her neighbour. "
"1.5-3.2 s: he stops chewing and jabs the leg toward the lens so that its bitten end grows larger in the frame, largest at about 2.3 s, then pulls it back below his chin by 3.2 s (the leg stays below his eyes and never covers his mouth for longer than half a second); his eyebrow climbs; he says flatly: \"Fork or fingers?\" "
"3.2-3.7 s: a half-second pause, a slow blink, the chin lifts a little. "
"3.7-5.7 s: with a small tilt of the head to his right he says drily: \"Tell me in the comments.\" while the leg waggles slightly in his fist; a courtier in a dark coat behind the ladies steps from the right edge toward the centre. "
"5.7-6.6 s: a visible swallow, the cheek empties, the fist sinks by about a hand's width and the bitten end of the leg swings down toward the platter; the servant with the dish, already at the right edge, walks behind the ladies toward the centre and out of the frame. "
"6.6-8.7 s: quietly, with the eyebrow up, he says: \"Wrong answers go to the Bastille.\" with a small nod forward at 7.4 s on the word Bastille and his eyes sliding to the left at 8.2 s and back into the lens by 8.7 s. "
"8.7-10 s: a silent beat, he does not speak: a flat deadpan stare into the lens, the leg lowered, mouth closed, no smile; the lady in the gold gown turns her head to look at him with her fan still raised, a courtier shifts his weight. "
"CAMERA SCORE in absolute amounts (filmed on a phone in one hand, close, level with his mouth; the king and the room stay in place, the frame moves): every 2 seconds the frame shifts by 8 to 10 percent of its width: 0-2 s a drift to the left with a roll of 3 to 5 degrees to the left building to about 8 degrees at 2 s; at 1.5 s a focus hunt: the focus slides from the leg to his face within half a second (phone mistake); 2-4 s a push-in on his face by about 6 percent; 4-5 s the phone jerks away to the right and comes back; 5-7 s a tilt up by about 4 degrees and a dip back, and at 6 s his own pink thumb slides in from the lower left corner for one second (phone mistake); 7-8.7 s a slow sway to the right; 8.7-10 s the frame settles back to the framing of @last_frame with its slight roll to the left and a last small dip at 9.2 s. "
"POSE SCORE: his head crosses the frame by at least a third of its own width every 2 seconds: leaning left while jabbing the leg, centre at the pause, a tilt to his right for the comments line, back to the centre for the swallow, a nod on the Bastille line and a glance to the left before the silent beat. "
"THE ROOM IS ALIVE: steam from the carcass, candle flames flicker, the ladies whisper behind their fans, the standing courtiers shift their weight; the background people keep their faces. "
"Acting limits: heavy eyelids stay, no wide-open eyes, no broad grin, no lean toward the lens beyond the jab, the face stays natural and undistorted, exactly five fingers on the hand, the leg stays visibly bitten. "
"No whip pans and no zoom lens: the only quick moves are the jerk at 4-5 s and the focus hunt, all by hand; no gimbal, no dolly or flying camera. "
"Sound: only diegetic, low murmur of a large hall, the leg squelching in the fist, fabric, candle flicker; no music at all. No text or captions, no modern objects, no fork, only one king in the frame (no second face, no double).")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T3d_start_4k.jpg", RAW + "T3d_end_4k.jpg"],
        "duration": 10, "resolution": "720p"}
open(H0 + "take3_T3d_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE3_T3d.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE3_T3d.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE3_T3d.mp4"); print("saved")
