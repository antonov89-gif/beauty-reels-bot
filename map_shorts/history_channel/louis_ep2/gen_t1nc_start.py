"""Take 1 NEW piece 1c: Some of you write that I eat too much ... before your eyes (setup S2b, chest height from his left, diagonal along the table): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS: "[a satisfied sigh] Some of you write that I eat too much. I read it. [sniffs] Of course, that's not true. Every day I feast in front of the court. Today... before your eyes." GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: K4_master_neutral_O8.png, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t1nc_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 (the king's master portrait) is his face and costume: "
"exactly the same man of about 45, same heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light), the scarlet velvet coat with gold suns, lace cravat; "
"do not copy its neutral pose or backdrop. "
"Reference 2 shows only the hall: "
"ignore its angle, and do NOT copy its crystal glasses or the people at its table; "
"Camera: "
"a hand-held angle at CHEST HEIGHT, close to the tablecloth, FROM HIS LEFT SIDE looking diagonally ALONG the long table toward him (not across it, not from above): "
"he sits in the LEFT third of the frame, his face about 35 percent of the frame width with the whole tall wig about 70 percent inside the frame, turned toward the viewer's right to look back at the lens over his shoulder; "
"rolled about 10 degrees to the left; "
"on the right two thirds the long table stretching away with candles and plain gold dishes (no fruit, no grapes), the court seated and standing courtiers in plain wigs, a lady with an open fan and a servant in livery on the right. "
"Pose and emotion: "
"he is reading the comments with a wounded look: "
"heavy lids, the lips pursed, the brows pulled together a little, the head tilted slightly. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "R10_hall_clean.jpg"]}
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
