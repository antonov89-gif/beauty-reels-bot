"""Take 4b v3 piece B: the king laughs, 'Nobody saw anything... And nobody will see you again... Joking' (setup S9b, from the side): CLIP (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Kling 4.0 i2v 720p 10 s = $1.45 (0.145 x 10). first = t4bB_start_4k, last = t4bB_end_4k. Lines (script 7.3): LOUIS: "Nobody saw anything." [turns to Marcel; quiet, flat] "And nobody will see you again." [Marcel freezes; pause] "Joking."  (the king first stares, then laughs for real) Motion score per PROMPT_CAMERA_LESSONS.md. Runs only with the argument go. One call, no retries without a new yes.
BRIEF: briefs/brief_t4b_B.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("@first_frame is the exact starting frame: "
"for the first 0.3 s keep it as it is, then animate from it. "
"the same two people as in the frames: "
"the king (the same man of about 45 as @first_frame: "
"heavy-lidded grey-green eyes, thin dark waxed moustache with curled tips, a small dark beauty mark on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white, the scarlet velvet coat with gold suns) and Marcel (a young servant with freckles and thick dark brows, a plain white wig, a pale blue livery coat with silver braid), filmed by a hand-held camera at table height from the side of the long table, medium-wide, both heads with their wigs fully in the frame (the king in the left part, Marcel in the right part), in the candlelit gilded hall; "
"on the white tablecloth a fallen gold goblet and a pool of red wine. "
"At the end, 10 s, the frame is as @last_frame (the king turned to Marcel with a flat look, Marcel frozen). "
"Realistic live action, real skin texture, no beauty filter. "
"0-1.2 s: "
"a silent beat: "
"the king stares at Marcel, blank, heavy lids; "
"Marcel does not breathe; "
"1.2-3.2 s: "
"the king's face cracks and he laughs for real, his head tipping back slightly and turning away, the eyelids staying heavy, his shoulders shaking, the upper teeth just showing; "
"Marcel flinches and looks from the king to the camera and back; "
"at 2.5 s a courtier behind the king laughs behind his hand; "
"3.2-4.9 s: "
"still laughing, the king looks at the wine and says: "
"\"Nobody saw anything.\" with a flat wave of his hand over the pool; "
"4.9-8.0 s: "
"the laugh stops, the king turns his head back to Marcel, heavy lids, flat and quiet: "
"\"And nobody will see you again.\" Marcel freezes; "
"8.0-8.8 s: "
"a pause: "
"both hold, only a candle flickers; "
"8.8-9.4 s: "
"the king, lightly: "
"\"Joking.\" with a faint smile; "
"9.4-10 s: "
"silent tail, Marcel exhales, settling to @last_frame. "
"CAMERA SCORE in absolute amounts (hand-held; "
"the people and the room stay in place while the frame moves; "
"the king's head with the wig is at 52 percent of the width on the left, Marcel's at 35 percent on the right, so every move is small and keeps both wigs inside the frame, the free margin is about 4 to 6 percent on each side): "
"every 2 seconds the frame shifts by 3 to 4 percent of its width and rolls by 2 to 3 degrees: "
"0-2 s a slow drift to the left by 3 percent and a push-in of 3 percent; "
"2-4 s the shake of the laughter by 4 percent; "
"at about 4.2 s the whole picture blurs for 0.5 s, then snaps sharp; "
"4-6 s a sway to the right by 3 percent; "
"at about 6.5 s (the allowed window is 4.5 to 8.5 s) a thumb slips into the lower left corner covering the lower left 15 percent of the frame width (never more than 20 percent) for 0.6 s and never a face; "
"6-8 s a push-in of 4 percent toward Marcel; "
"8-10 s a push-back of 4 percent and settle to the framing of @last_frame. "
"POSE SCORE as verbs with times: "
"0-1.2 s stare, hold; "
"1.2-3.2 s crack, laugh, tip back slightly, flinch; "
"3.2-4.9 s wave, laugh; "
"4.9-8.0 s turn, lift the brow, speak flat; "
"8.0-8.8 s hold; "
"8.8-10 s smile, exhale; "
"the heads move by turns and nods of 3 to 5 percent of the frame width in each 2-second window; "
"never a hold longer than 2 seconds except the pause at 8.0-8.8 s (camera and room keep moving). "
"THE ROOM IS ALIVE: "
"candle flames flicker; "
"at 2.5 s a courtier behind the king laughs behind his hand; "
"at 5 s the lady with the fan at the right back leans to her neighbour; "
"at 7 s a servant in livery far behind crosses from right to centre; "
"at 9 s two courtiers behind Marcel stop whispering and look at him. "
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
        "image_urls": [RAW + "t4bA_end_4k.jpg", RAW + "t4bB_end_4k.jpg"],
        "duration": 10, "resolution": "720p"}
open(H0 + "take_t4bB_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t4bB.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t4bB.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t4bB.mp4"); print("saved")
