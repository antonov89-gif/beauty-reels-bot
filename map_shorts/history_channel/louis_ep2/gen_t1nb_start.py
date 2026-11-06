"""Take 1 NEW piece 1b: And this is my channel / Sun King / handsome (setup S2, table height, rolled): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS: "And this is my channel. They call me the Sun King. Yes... I'm that handsome. [a satisfied sigh]" GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: R1_king_card_A3_white_wig.jpg. One call, about $0.12. Run: python3 gen_t1nb_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's face and costume: "
"exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; "
"do not copy its pose or background. "
"Camera: "
"his phone propped by hand at TABLE HEIGHT, very close, rolled about 15 degrees to the left (a dutch angle), looking at him three-quarter to the viewer's left: "
"his face fills about 62 percent of the frame width with its centre at 55 percent, the tall silver-grey wig filling the top third of the frame and cropped by the top edge, sharp; "
"at the lower edge the white tablecloth and the corner of a gold plate; "
"behind him, soft and blurred, the candlelit gilded hall with a few courtiers' heads, no chandelier. "
"Pose and emotion: "
"he gives a smug sideways look at the lens under heavy lids, the chin lifted, one eyebrow raised, the lips closed in a faint proud smile. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg"]}
open(H0 + "t1nb_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t1nb_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
