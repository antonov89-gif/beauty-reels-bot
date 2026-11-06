"""Take 6 the verdict (setup S13, frontal close, slow push-in): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS (OWNER): "[wipes his fingers, sits up, glances at the bones on his plate, pushes the plate a little away] So. Do I eat too much? ...No. I eat like a king. [chin up] Don't be afraid of getting fat. Be afraid of being a loser. [haughty laugh]" GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: R1_king_card_A3_white_wig.jpg, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t6_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's face and costume: "
"exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; "
"do not copy its pose or background. "
"Reference 2 shows only the hall: "
"ignore its angle, and do NOT copy its crystal glasses or the people at its table; "
"Camera: "
"hand-held at arm's length at EYE LEVEL, frontal, close: "
"his face fills about 30 percent of the frame width with its centre at 50 percent of the frame width, the whole tall wig about 70 percent of the width and fully inside the frame, sharp; "
"a slight roll of about 4 degrees to the left; "
"at the lower edge a gold plate with a few small clean bird bones, soft. "
"Pose and emotion: "
"he is wiping his fingers on a single lace napkin held in one hand just below the frame, his chin slightly lowered, his heavy-lidded eyes looking down at the bones on the plate with a complacent faint smirk, the lips closed. "
"Behind him, blurred: "
"the candlelit gilded hall, standing courtiers in plain wigs, at the back right a lady with a fan and two courtiers whispering, no chandelier. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t6_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t6_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
