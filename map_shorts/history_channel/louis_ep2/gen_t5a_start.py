"""Take 5 piece 5a salad, ham, pastry, fruit, peas (setup S11): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS: "Then salad, ham, pastry, fruit. [gives up counting] In under an hour. [holds a pea to the lens, softly] And peas. The court talks of nothing else. [eats it, delighted]" GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: K4_master_neutral_O8.png, K4_angle_low_O12.png, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t5a_start.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 (the king's master portrait) is his face and costume: "
"exactly the same man of about 45, same heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light), the scarlet velvet coat with gold suns, lace cravat; "
"do not copy its neutral pose or backdrop. "
"Reference 2 shows the same man from below, low camera: "
"take the camera angle and the head pose from it, the face and the wig from reference 1. "
"Reference 3 shows only the hall: "
"ignore its angle, and do NOT copy its crystal glasses or the people at its table; "
"Camera (filmed by Marcel): "
"LOW, from the near corner at the END of the long table, the lens only about 25 centimetres above the tablecloth, looking along the table toward the king who sits at its far end; "
"NOT across the table and NOT from above, rolled about 10 degrees to the left. "
"In the foreground, soft and out of focus at the lower edge and the right edge: "
"a silver platter with a glazed ham, a pyramid of small pastries, a dish of fruit and a bowl of strawberries (all food on the table, plates and gold dishes only). "
"The king sits at the far end, his face fills about 28 percent of the frame width (the tall wig about 60 percent, with at least 15 percent free space on each side) with its centre at 58 percent of the frame width, sharp, turned three-quarter toward the lens, napkin tucked into the lace cravat. "
"Pose and emotion: "
"he is counting the dishes on his fingers, just giving up, with a tolerant amused look, heavy lids half-lowered, lips closed in a faint smirk, one hand raised showing a few fingers; "
"the other hand rests on the cloth in front of a small silver dish of green peas on the cloth before him. "
"Behind him: "
"the candlelit gilded hall, standing courtiers in plain wigs, at the back right a lady with an open fan, a servant in livery far behind at the right; "
"no chandelier. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "K4_angle_low_O12.png", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t5a_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t5a_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
