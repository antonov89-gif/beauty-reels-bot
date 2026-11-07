"""Take 5 piece 5b START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Setup S11b (Marcel films the laden table and the king eating, no words). Refs in order: K4_master_neutral_O8.png (face, wig, coat), K4_angle_high_O13.png (high camera angle and head pose), R10_hall_clean.jpg (hall only). Brief pin: START hands hidden behind the dishes, chewing, no lens look. Result: pilot_frames/anchors/t5b_start_sunburst_4k.jpg. Run: python3 gen_t5b_start_sunburst.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real unretouched natural skin texture. "
"Reference 1 (the king's master portrait) is his face and costume: "
"exactly the same man of about 45, same heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light), the scarlet velvet coat with gold suns, lace cravat; "
"take only the face, wig and costume from it. "
"Reference 2 shows the same man from above, high camera: "
"take the camera angle and the head pose from it, the face and the wig from reference 1. "
"Reference 3 gives only the mood of the hall: gilded walls, warm candlelight, standing courtiers in grey wigs; take no objects and no people from it, the table and the people are new. "
"Camera (filmed by Marcel): "
"hand-held, held a little above the dishes and tilted down about 25 degrees, a medium-close look at the laden table, rolled about 7 degrees to the right. "
"In sharp focus, the dishes and the king both in focus (a deep-focus wide look), the foreground heaped: a gold platter of roast pheasant, a glazed ham, a pyramid of small pastries, a bowl of fruit and a gold dish of green peas. "
"The king sits at the far end of the table along its length, at the top of the frame, sharp: his face fills about 20 percent of the frame width (the tall wig about 42 percent, with at least 15 percent free space on each side), its centre at 50 percent of the frame width, head turned a quarter toward the viewer's left, both eyes and the beauty mark clearly visible. "
"Pose and emotion: "
"he is chewing slowly with relish, one cheek lightly full, heavy lids half-lowered with his eyes on the dishes in front of him, lips closed in a small contented smile, napkin tucked into the lace cravat; his hands are hidden behind the dishes, only the dishes stand between the camera and his hands. "
"Behind him: "
"the candlelit gilded hall lit by wall sconces with the ceiling out of frame, standing courtiers in plain wigs, at the back right a lady with an open fan, a servant in livery far behind at the right. "
"One king only, natural light rouge. The table holds only plates, gold dishes, silver platters, napkins and candle holders. Clean picture with no text or lettering, no modern objects, only things of the 1680s. "
)

body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "K4_angle_high_O13.png", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t5b_start_sunburst_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t5b_start_sunburst_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
