"""Take 4b v3 piece A: Marcel spills the wine, looks at the camera and at the king, 'Sorry, Sire' (setup S9b, from the side): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: MARCEL (quietly): "Sorry, Sire." [Marcel stumbles, the goblet tips, the wine runs over the tablecloth and a little over the king's cuff; he freezes, looks into the camera, then at the king; the king slowly turns his head to Marcel, blank.] GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: K4_master_neutral_O8.png, R8_marcel_full.jpg, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t4bA_start.py go
BRIEF: briefs/brief_t4b_A_B.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's master portrait: "
"the same man of about 45, heavy-lidded grey-green eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light), the scarlet velvet coat with gold suns, lace cravat; "
"do not copy its neutral pose or backdrop. "
"Reference 2 is Marcel: "
"his face, white wig, pale blue livery coat with silver braid and a white cravat only (no tricorn hat, not the full-figure pose or backdrop of that card): "
"a young servant with freckles and thick dark brows. "
"Reference 3 shows only the hall: "
"ignore its angle, and do NOT copy its crystal glasses, its chandelier or the people at its table (new people). "
"Camera: "
"hand-held at TABLE HEIGHT from the SIDE of the long table, about 40 degrees off the line of the table, a CLOSE medium shot, tight enough that the two heads with their wigs fill most of the frame width, rolled about 6 degrees to the right: "
"the king sits in the LEFT part of the frame (his head with the wig about 50 percent of the frame width, his face about 26 percent, face centre at 32 percent of the width, the whole wig inside the frame with about 5 percent free space at the left edge, sharp), his head turned only about 10 degrees toward the viewer's right, his eyes on the gold goblet that Marcel carries, both eyes and the beauty mark on the viewer's right of his mouth visible; "
"Marcel stands at the RIGHT of the frame (his head with the white wig about 34 percent of the width, his face about 22 percent, face centre at 76 percent of the width, sharp), turned three-quarter toward the viewer's left, toward the king; "
"both heads fully inside the frame with their wigs and about 5 percent free space at each edge. "
"Between and below them the clean white tablecloth with one gold plate and two candles; "
"the lower corners of the frame show only white tablecloth. "
"Pose and emotion: "
"the king sits expectant and amused: "
"eyelids heavy, one eyebrow raised, the lips pressed into a knowing smirk, his eyes fixed on the goblet, one ringed hand resting flat on the white cloth in front of him, sharp, five natural fingers, the fingers lifting one after another as he drums; "
"Marcel bends a little over the table, tense and sweating a little, his eyes on the gold goblet of red wine standing on a small gold tray in both his hands (five natural fingers on each hand), the goblet metal, never glass. "
"Everything is tack-sharp 4K: "
"skin pores, moustache hairs, wig curls, lace and the gold braid, no soft focus, both people in the sharp plane. "
"Behind them, softly blurred: "
"the candlelit gilded hall, standing courtiers in plain wigs, at the back right a lady with an open fan, a servant in livery far behind. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no clown makeup, only one king. "
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
