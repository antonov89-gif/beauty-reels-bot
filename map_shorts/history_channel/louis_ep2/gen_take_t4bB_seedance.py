"""Take t4bB CLIP on Seedance 2.5 LITE i2v (owner 07.11: Seedance 2.5 Lite): image_urls[0] = first frame, [1] = last-frame constraint (APIpod spec seedance--2-5-lite-image-to-video), 720p only, 10 s, $0.15/s = $1.50, audio off (the model audio is always muted). Same prompt as gen_take_t4bB.py (Kling) with the tag wording changed. One call, no retries without a new yes. Run: python3 gen_take_t4bB_seedance.py go
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
    "heavy-lidded grey-green eyes, thin dark waxed moustache with curled tips, a small dark beauty mark on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white, the scarlet velvet coat with gold suns) and Marcel (a young servant with freckles and thick dark brows, a plain white wig, a pale blue livery coat with silver braid), filmed by a hand-held camera at table height from the side of the long table, medium-wide, both heads with their wigs fully in the frame (the king in the left part, Marcel in the right part), in the candlelit gilded hall; "
    "on the white tablecloth a fallen gold goblet and a pool of red wine. "
    "At the end, 10 s, the frame is as the last frame (the king cool and flat with a lifted corner of the mouth, turned to Marcel; "
    "Marcel frozen). "
    "Realistic live action, real skin texture, no beauty filter. "
    "0-1.5 s: "
    "a silent look: "
    "the king looks at Marcel, one slow blink; "
    "Marcel does not breathe; "
    "1.5-3 s: "
    "the king holds back a laugh: "
    "his lips pressed tight, his cheeks lifting, his shoulders trembling at 2.2 s; "
    "Marcel looks from the king to the camera and back; "
    "at 2.5 s a courtier behind the king laughs behind his hand; "
    "3-4 s: "
    "the laugh breaks out for real, no longer than 1.5 s: "
    "his head tips back slightly and turns away, his shoulders shake, the upper teeth show, then he recovers with his eyes open; "
    "4-5.8 s: "
    "the king, chin up: "
    "\"Nobody saw anything.\" with a flat wave of his hand over the pool of wine, a look into the lens for 0.6 s on the word 'anything'; "
    "5.8-8.5 s: "
    "the smile switches off in 0.3 s, the king turns his head to Marcel, his face flat, cold, a quiet voice, no gestures, only a blink: "
    "\"And nobody will see you again.\" Marcel freezes; "
    "8.5-9.3 s: "
    "a silence of 0.8 s, both hold, only a candle flickers, one eyebrow of the king lifts for 0.2 s; "
    "9.3-10 s: "
    "the king, lightly: "
    "\"Joking.\" the corner of his mouth up, his eyes still flat, one eye narrowing; "
    "Marcel exhales, settling to the last frame. "
    "EMOTION SCORE (strength 0-3): "
    "king 0-1.5 s cool stare (1), 1.5-3 s holding back laughter (2-3), 3-4 s real laugh (3), 4-5.8 s smug (2), 5.8-8.5 s deadpan menace (2), 8.5-9.3 s silent (1), 9.3-10 s sly (2); "
    "Marcel 0-3 s dread (3), 3-5.8 s flinching (2), 5.8-8.5 s frozen terror (3), 9.3-10 s relief (2). "
    "Every reaction starts 0.3 to 0.5 s after its event. "
    "CAMERA SCORE in absolute amounts (hand-held; "
    "the people and the room stay in place while the frame moves; "
    "both wigs stay inside the frame): "
    "every 2 seconds the frame shifts by 3 to 5 percent of its width and rolls by 2 to 3 degrees: "
    "0-2 s a slow drift to the left by 3 percent and a push-in of 3 percent; "
    "2-3 s a tremor with the king's shaking; "
    "3-4 s the shake of the laughter by 5 percent; "
    "at about 4.2 s the whole picture blurs for 0.5 s, then snaps sharp; "
    "4-5.8 s a sway to the right by 3 percent; "
    "5.8-8.5 s a slow push-in of 3 to 4 percent toward Marcel without any shake; "
    "at about 8 s (the allowed window is 6 to 9 s) a thumb slips into the lower left corner covering the lower left 15 percent of the frame width (never more than 20 percent) for 0.6 s and never a face; "
    "8.5-10 s a push-back of 4 percent and settle to the framing of the last frame. "
    "POSE SCORE as verbs with times: "
    "0-1.5 s look, blink; "
    "1.5-3 s press, lift, tremble; "
    "3-4 s burst, tip back, recover; "
    "4-5.8 s wave, glance at the lens; "
    "5.8-8.5 s turn, speak flat, blink; "
    "8.5-9.3 s hold, lift one brow; "
    "9.3-10 s speak, narrow, exhale; "
    "never a hold longer than 2 seconds except the silence at 8.5-9.3 s (camera and room keep moving). "
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
    " "
)
body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt, "image_urls": [RAW + "t4bA_end_4k.jpg", RAW + "t4bB_end_4k.jpg"],
        "duration": 10, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": False}
open(H0 + "take_t4bB_seedance_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "pilot_frames/TAKE_t4bB_seedance.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=2400, every=10)
    open(H0 + "pilot_frames/TAKE_t4bB_seedance.status.json", "w").write(re.sub(r'(https://[^"?]+)\\?[^"]*', r'\\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; print("status", d.get("status"), "usage", d.get("usage"))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    u = find(d.get("result") or d)
    if u: apipod.download(u, H0 + "pilot_frames/TAKE_t4bB_seedance.mp4"); print("saved")
