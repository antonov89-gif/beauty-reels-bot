"""Take 5 piece 5b Marcel films the laden table and the king eating (no words): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: [Marcel films the laden table and the king eating, about 4 s, no words: chewing, a happy hum, the murmur of the crowd] GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: K4_master_neutral_O8.png, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t5b_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 (the king's master portrait) is his face and costume: "
"exactly the same man, heavy-lidded eyes, thin dark waxed moustache with curled tips, the beauty mark on the viewer's right of the mouth, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns; "
"do not copy its pose. "
"Reference 2 shows only the hall: "
"ignore its angle, and do NOT copy its crystal glasses or the people at its table; "
"Camera (filmed by Marcel): "
"hand-held, held a little ABOVE the dishes and tilted down about 25 degrees, a medium-close look at the laden table: "
"in sharp focus in the foreground a gold platter of roast pheasant, a ham, a pyramid of pastries, a bowl of fruit and a gold dish of peas, all heaped, plates and gold dishes only; "
"the king sits at the far end of the table along its length at the top of the frame, only slightly soft but clearly readable (his face about 19 percent of the frame width, the whole wig inside the frame, centre at 45 percent), heavy lids half-lowered, chewing with relish, his hands hidden behind the dishes; "
"rolled about 7 degrees to the right. "
"Behind him the candlelit hall, standing courtiers in plain wigs, at the back right a lady with a fan, no chandelier. "
"The phone that films is never visible in the frame. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t5b_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t5b_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
