"""Take 1 NEW piece 1c: Some of you write that I eat too much ... before your eyes (setup S2b, three-quarter right, arm's length): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS: "[a satisfied sigh] Some of you write that I eat too much. I read it. [sniffs] Of course, that's not true. Every day I feast in front of the court. Today... before your eyes." GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: R1_king_card_A3_white_wig.jpg, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t1nc_start.py go"""
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
"his own hand-held phone at arm's length a little ABOVE his eye level and to his left, medium-close, rolled about 6 degrees to the right: "
"his face fills about 50 percent of the frame width with its centre at 46 percent, turned three-quarter toward the viewer's right, sharp; "
"a white napkin tucked into the lace cravat, at the lower edge a gold plate with a few grapes and the white tablecloth; "
"behind him on the right the candlelit gilded hall: "
"the long table with the court seated and standing courtiers in plain wigs, a lady with an open fan at the back, no chandelier. "
"Pose and emotion: "
"he is reading the comments on an imaginary screen below the lens with a wounded look: "
"heavy lids, the lips pursed, the brows pulled together a little, the head tilted to the viewer's left. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t1nc_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t1nc_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
