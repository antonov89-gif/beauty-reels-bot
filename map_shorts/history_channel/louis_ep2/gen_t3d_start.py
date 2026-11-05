"""T3d START still (= piece 3c "Fork or fingers?", setup S8b, prepared 05.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3: "[chewing, points the leg at the lens] Fork or fingers? Tell me in the comments. [swallows] Wrong answers go to the Bastille." GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs: 1 = card A3, 2 = R10 hall clean (ignore its angle). One call, about $0.12. Run: python3 gen_t3d_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone photo in dim candlelight, slightly underexposed, wide lens, real photograph, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, beauty mark beside the mouth, light rouge, the tall white-grey powdered wig, the same colour as reference 1, the scarlet velvet coat with gold suns, lace cravat and rings. Reference 2 shows only the hall: ignore its camera angle and tilt. Do not copy the background or the pose of reference 1. "
"Camera: a very low hand-held angle from the edge of the table, the phone just above the tablecloth tilted up about 25 degrees and rolled about 12 degrees to the right, wide lens, very close. In the foreground, large and slightly soft, the greasy roast pheasant leg with a bite taken out of it, held in his ringed hand and pointed straight at the lens, rings on three visible fingers and the thumb on top (exactly five fingers); his face is behind it in the upper middle, three-quarter, in focus, looking straight into the lens. "
"Pose and emotion: he is chewing, one cheek slightly full, lips shiny with grease, heavy bored haughty lids, a flat deadpan stare into the lens, one eyebrow slightly raised, no smile. "
"Behind him, slightly out of focus: the candlelit gilded hall of reference 2, ladies on folding stools whispering behind open fans, standing courtiers shifting their weight, a servant crossing with a dish. "
"Bare hands only, nothing in his hands but the leg. No text, no logos, no modern objects, no extra fingers, no clown makeup, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg", RAW + "R10_hall_clean.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t3d_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T3d_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
