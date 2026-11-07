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
    "At the end, 10 s, the frame is as the last frame (the king cool and flat with a lifted chin, turned to Marcel; "
    "Marcel with lowered hands and wide eyes on the king). "
    "Realistic live action, real skin texture, no beauty filter. "
    "0-1.2 s: "
    "the king, in his closed-mouth smirk, looks at Marcel, one slow blink; "
    "the smirk tightens; "
    "Marcel's hands are raised open and tremble; "
    "1.2-3.2 s: "
    "the king's lips press together for a moment, his cheeks lift, his shoulders tremble at 2.0 s, then the laugh breaks out for real (short, about 1.5 s): "
    "his head tips back slightly and turns away, his shoulders shake, the upper teeth show, his eyes open again at the end of the laugh; "
    "Marcel flinches and looks from the king to the spill and back; "
    "at 2.5 s a courtier behind the king laughs behind his hand; "
    "at 3.0 s Marcel's hands drop partly; "
    "3.2-4.9 s: "
    "still laughing quietly, the king looks at the wine and says: "
    "\"Nobody saw anything.\" with a flat wave of his hand over the pool, his chin lifting; "
    "4.9-8.0 s: "
    "the smile switches off in 0.3 s, the king turns his head back to Marcel, his face flat and cold, quietly and flat, no gestures, only one blink: "
    "\"And nobody will see you again.\" Marcel freezes and clasps his hands in front of him at 5.8 s; "
    "8.0-8.8 s: "
    "a silence of 0.8 s, both hold, only a candle flickers, one eyebrow of the king lifts for 0.2 s; "
    "Marcel's hands stay clasped; "
    "8.8-9.4 s: "
    "the king, lightly: "
    "\"Joking.\" the corner of his mouth up, his eyes still flat, one eye narrowing; "
    "9.4-10 s: "
    "a silent tail: "
    "Marcel lowers his clasped hands with a shaky breath, his eyes still wide on the king, settling to the last frame. "
    "EMOTION SCORE (strength 0-3, never one expression longer than 2 s except the held pause): "
    "king 0-1.2 s smirk tightening (1), 1.2-3.2 s holding back then real laughter (2-3), 3.2-4.9 s smug (2), 4.9-8.0 s deadpan menace (2), 8.0-8.8 s silent (1), 8.8-10 s sly (2); "
    "Marcel 0-1.2 s shocked (2), 1.2-3.2 s flinching (2), 4.9-8.0 s frozen terror (3), 8.8-10 s shaky half-relief with the eyes still wide (2). "
    "Every reaction starts 0.3 to 0.5 s after its event. "
    "The king never looks into the lens. "
    "CAMERA SCORE in absolute amounts (hand-held; "
    "the people and the room stay in place while the frame moves; "
    "both wigs stay inside the frame): "
    "every 2 seconds the frame shifts by 3 to 5 percent of its width and rolls by 2 to 3 degrees: "
    "0-2 s a slow drift to the left by 3 percent and a push-in of 3 percent; "
    "2-3.2 s a tremor with the king's shaking; "
    "3.2-4 s the shake of the laughter by 5 percent; "
    "at about 4.2 s the whole picture blurs for 0.5 s, then snaps sharp; "
    "4.2-4.9 s a sway to the right by 3 percent; "
    "4.9-8.0 s a slow push-in of 3 to 4 percent toward Marcel without any shake; "
    "at about 8 s (the allowed window is 6 to 9 s) a fingertip slips into the lower left corner covering the lower left 15 percent of the frame width (never more than 20 percent) for 0.6 s and never a face; "
    "8.8-10 s a push-back of 4 percent and settle to the framing of the last frame. "
    "POSE SCORE as verbs with times: "
    "0-1.2 s look, blink, tighten; "
    "1.2-3.2 s press, lift, tremble, burst, tip back, recover; "
    "3.2-4.9 s wave, laugh, lift the chin; "
    "4.9-8.0 s turn, speak flat, blink; "
    "8.0-8.8 s hold, lift one brow; "
    "8.8-10 s speak, narrow, breathe; "
    "Marcel: "
    "tremble, flinch, drop the hands, clasp, hold, lower; "
    "never a hold longer than 2 seconds except the silence at 8.0-8.8 s (camera and room keep moving). "
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
    "only diegetic, low murmur of a large hall, fabric, cutlery, candle flicker, breath; "
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
