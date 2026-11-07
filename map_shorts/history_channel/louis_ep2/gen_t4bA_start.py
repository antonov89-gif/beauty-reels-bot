"""Take 4b v3 piece A: Marcel spills the wine, looks at the camera and at the king, 'Sorry, Sire' (setup S9b, from the side): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: MARCEL (quietly): "Sorry, Sire." [Marcel stumbles, the goblet tips, the wine runs over the tablecloth and a little over the king's cuff; he freezes, looks into the camera, then at the king; the king slowly turns his head to Marcel, blank.] GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: K4_master_neutral_O8.png, R8_marcel_full.jpg, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t4bA_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's master portrait: "
"the king exactly as in reference 1 (his master portrait): "
"the same man of about 45, heavy-lidded grey-green eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light), the scarlet velvet coat with gold suns, lace cravat; "
"do not copy its neutral pose or backdrop. "
"Reference 2 is Marcel: "
"Marcel exactly as in reference 2 (face, white wig, pale blue livery coat with silver braid and a white cravat only; "
"no tricorn hat, not the full-figure pose or backdrop of that card): "
"a young servant with freckles and thick dark brows. "
"Reference 3 shows only the hall: "
"ignore its angle, and do NOT copy its crystal glasses, its chandelier or the people at its table (new people). "
"Camera: "
"hand-held at TABLE HEIGHT from the SIDE of the long table, about 40 degrees off the line of the table, a medium-wide shot, rolled about 6 degrees to the right: "
"the king sits in the LEFT part of the frame (his head with the wig about 52 percent of the frame width, his face about 26 percent, face centre at 28 percent of the width, sharp), turned three-quarter toward the viewer's right, toward Marcel; "
"Marcel stands at the RIGHT of the frame (his head with the white wig about 35 percent of the width, his face about 22 percent, face centre at 78 percent of the width, sharp), turned three-quarter toward the viewer's left, toward the king; "
"both heads fully inside the frame with their wigs. "
"Between and below them the white tablecloth with a gold plate and candles, clean, no stains. "
"Pose and emotion: "
"the king sits waiting, heavy lids, a faint smirk of impatience, his ringed fingers drumming on the cloth in front of him (five natural fingers); "
"Marcel bends a little over the table, tense and sweating a little, his eyes on the gold goblet of red wine standing on a small gold tray in both his hands (five natural fingers on each hand), the goblet metal, never glass. "
"Behind them, blurred: "
"the candlelit gilded hall, standing courtiers in plain wigs, at the back right a lady with an open fan, a servant in livery far behind. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "R8_marcel_full.jpg", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t4bA_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t4bA_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
