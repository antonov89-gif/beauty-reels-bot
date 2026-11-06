"""Take 4 piece 4b-2 Marcel through the wine (setup S10): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS (off screen): "And nobody will see you again." [Marcel freezes; pause] "Joking." MARCEL (quietly): "Sorry, Sire." GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: R8_marcel_full.jpg, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t4b2_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is Marcel (a full-figure card: "
"use only his face, wig and costume, not its pose or background): "
"Marcel exactly as in the reference (his face only; "
"the terrified look is described in words): "
"a young frightened servant with freckles, thick dark brows, a plain white wig and a plain blue livery coat, nothing of the king's red coat or tall silver wig. "
"Do not copy its pose or background. "
"Reference 2 shows only the hall: "
"ignore its angle, and do NOT copy its crystal glasses or the people at its table; "
"Camera: "
"the king's own phone seen from where the king sits, a little LOW looking up at the standing Marcel from about 15 degrees below his eye level, hand-held, rolled about 6 degrees to the right, close: "
"Marcel's face fills about 46 percent of the frame width, his face centre at about 54 percent of the frame width, blue livery coat and a strip of white lace at the lower edge, the top of the white wig cropped a little by the top edge. "
"A deep red wine film is on the LEFT THIRD of the lens (thick dark irregular curved edge between 25 and 33 percent of the frame width, thin and transparent inside with runs and drops, never touching Marcel's face), the right two thirds sharp. "
"Pose and emotion: "
"Marcel stands rigid and pale, lips pressed together, eyes on the lens, a bead of sweat at the temple, terrified but trying to look calm; "
"both arms down at his sides, not visible. "
"Behind him, blurred: "
"the candlelit gilded hall, standing courtiers in plain wigs, at the back right a lady with an open fan, at the left behind the wine film a servant in livery; "
"no chandelier. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, no king in the frame, no hat, no tricorn. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R8_marcel_full.jpg", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t4b2_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t4b2_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
