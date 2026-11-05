"""Take 3, piece 3b-C (fork gag, setup S8a). Kling 4.0 i2v 720p 8 s = $1.16 (0.145 x 8). first = T3c start still, last = T3c end still (owner quality exception for the end still). Lines: "What is that? A fork? [pushes it away with two fingers, disgusted]". Runs only with the argument go. One call, no retries without a new yes."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("@first_frame is the exact starting frame: keep it unchanged at 0:00, then animate from it. The same king in every frame, always the face and look of @first_frame: the same face, the same age, the tall white-grey powdered wig of the same colour, thin dark waxed moustache with curled tips, beauty mark, light rouge, scarlet velvet coat with gold suns, lace cravat and rings; the same candlelit gilded hall, the same close hand-held position front-left across the table, the roast pheasant on the silver platter in the lower part of the frame. At the end, 8 s, the frame is exactly as @last_frame (his head turned a few degrees toward the fork, upper lip curled in disgust, one eyebrow raised, half-closed heavy lids, the leg still in his ringed hand, his other hand raised with two fingers pushing the silver two-tined fork that Marcel holds from the lower left in a sky-blue braided sleeve); the room and the king are in the same place in @last_frame as in @first_frame, only the pose, the fork and the expression differ. Realistic live action, real skin texture, no beauty filter. "
"0-1.5 s: he tugs the half-attached leg with the ringed hand on the viewer's right (the skin stretches, steam rises), his other hand on the viewer's left rests flat on the carcass, he looks down at it under heavy bored lids; the lady at the left whispers to her neighbour behind her fan. "
"1.5-3 s: the sky-blue sleeve at the lower left moves deeper into the frame and Marcel's hand comes out of it holding the silver two-tined fork toward him; he notices it, stops pulling and his eyes drop to the fork; the lady in blue on the right raises her fan. "
"3-4.5 s: flatly and drily he says: \"What is that?\" with a slow blink and his chin lifting slightly as he speaks; a courtier behind him turns his head. "
"4.5-5.5 s: his eyebrow climbs and he says, rising: \"A fork?\" "
"5.5-6.5 s: his hand on the viewer's left lifts off the carcass with the index and middle fingers extended and pushes the fork aside; Marcel's hand keeps holding the fork and the fork stays at the lower left of the frame; the ringed hand never lets go of the leg; his upper lip curls in disgust and his head turns a few degrees toward the fork; the servant with the dish drifts to the right edge and stays half out of the frame until the end. "
"6.5-8 s: a silent beat, he does not speak: a cold disgusted stare at the fork under half-closed lids, the leg still in his ringed hand, mouth closed, no smile; the lady in blue lowers her fan and looks at the fork, a courtier on the left shifts his weight. "
"CAMERA SCORE (filmed by Marcel on a phone in one hand, close, front-left across the table; the frame drifts and re-centres by a few percent, the king and the room stay in place): 0-2 s a slow drift to the right with a small roll to the left; 2-3 s a quick re-aim to the left toward the fork and a focus hunt at 2.4 s: the focus slides from his face to the fork and back within half a second (phone mistake); 3-5 s a slow push-in on his face while he speaks; 5-6.5 s a small jerk of the phone as the fork is pushed, and at 5.8 s the sleeve slides a little deeper into the frame (phone mistake), then a small push-back; 6.5-8 s a slow sway to the left that settles back to the framing of @last_frame, and at about 7 s the lens edge catches the sleeve and the frame dips for a moment. "
"THE ROOM IS ALIVE: steam rises from the pheasant all the time, the candle flames flicker, the ladies behind keep whispering behind their fans, the standing courtiers shift their weight. The background people keep their faces, only small natural movements. "
"Acting limits: heavy eyelids stay, no wide-open eyes, no broad grin, no lean toward the lens, the face stays natural and undistorted, exactly five fingers on each hand, the fork has exactly two tines. "
"No whip pans and no zoom lens: the only quick moves are the re-aim at 2-3 s and the jerk at 5-6.5 s described above, all by hand; no gimbal, no dolly or flying camera. "
"Sound: only diegetic, low murmur of a large hall, fabric, a silver fork touching the platter, candle flicker; no music at all. No text or captions, no modern objects, only one king in the frame (no second face, no double).")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [RAW + "T3c_start_4k.jpg", RAW + "T3c_end_4k.jpg"],
        "duration": 8, "resolution": "720p"}
open(H0 + "take3_T3c_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE3_T3c.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE3_T3c.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE3_T3c.mp4"); print("saved")
