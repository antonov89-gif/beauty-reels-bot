"""Take 7 piece 7a I was wondering what else to show you (setup S16, three-quarter right): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS (OWNER): "[leans back, thinks, looks around the hall] So... I was wondering what else to show you here. [pause, a short laugh] Ha. Probably... nothing." GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: K4_master_neutral_O8.png, K4_angle_34right_O11.png, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t7a_start.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 (the king's master portrait) is his face and costume: "
"exactly the same man of about 45, same heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; "
"do not copy its neutral pose or backdrop. "
"Reference 2 shows the same man turned to the right side of the image, the beauty mark stays on the right of the image: "
"take the camera angle and the head pose from it, the face and the wig from reference 1. "
"Reference 3 shows only the hall: "
"ignore its angle, and do NOT copy its crystal glasses or the people at its table; "
"Camera: "
"hand-held, held at arm's length a little BELOW his eye level, wide lens, so that the hall can be seen: "
"the camera is in front of him and a little to his right, his head with the wig fills about 60 percent of the frame width (his face about 30 percent) with its centre at 40 percent (a little left of centre), the head turned about 30 degrees toward the viewer's right with the beauty mark still visible; "
"to the right of him a wide view of the candlelit gilded hall with standing courtiers in plain wigs and a few ladies in wide gowns at the side, at the back right a lady with an open fan, a servant in livery far behind, a strip of the gilded ceiling at the top edge; "
"no chandelier; "
"rolled about 5 degrees to the right. "
"Pose and emotion: "
"he has leaned back in the armchair, his chin raised, thoughtful, his heavy-lidded eyes looking up and away to the right at the hall as if searching for an idea, the lips closed and pursed a little; "
"one hand resting on the chair arm at the lower edge. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "K4_angle_34right_O11.png", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t7a_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t7a_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
