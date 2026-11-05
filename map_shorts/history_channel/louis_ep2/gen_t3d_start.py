"""T3d START still (= piece 3c "Fork or fingers?", setup S8b, prepared 05.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3: "[chewing, points the leg at the lens] Fork or fingers? Tell me in the comments. [swallows] Wrong answers go to the Bastille." GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs: 1 = card A3, 2 = R10 hall clean (ignore its angle). One call, about $0.12. Run: python3 gen_t3d_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone photo in dim candlelight, slightly underexposed, wide lens, real photograph, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, beauty mark on the viewer's right of the mouth as in reference 1, light rouge, the tall powdered wig in cool silver-grey and white like the pale grey in reference 1, NOT beige, NOT cream, NOT golden, the candlelight must not tint it, the scarlet velvet coat with gold suns, lace cravat and rings. Reference 2 shows only the hall: ignore its camera angle and tilt. Do not copy the background or the pose of reference 1. "
"Camera: hand-held phone dead level with his mouth (not below the table, not from above), rolled about 15 degrees to the LEFT, very close, wide lens. The king's face fills the left half of the frame, three-quarter, the nose toward the frame left, the top of the tall wig cropped by the top edge, in focus, looking straight into the lens. From the lower right a big greasy roast pheasant leg crosses the frame diagonally, 30 to 45 degrees off the lens axis, its meaty end with one clean semicircular bite taken out (pale meat visible, a shiny grease edge) pointing at the lens, slightly soft; the fist grips the bone end (four fingers curled, the thumb on top, exactly five fingers, rings as in reference 1, a lace cuff). The leg stays below his mouth and does not cover his eyes or lips. At the lower edge, partly visible, the picked carcass on a silver platter; nothing else on the table. "
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
