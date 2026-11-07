"""Take 5 piece 5c Ohh, I wasn't born to work (setup S12, from above): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS (OWNER): "[leans back, hands on the belly, a long happy sigh] Ohh... I wasn't born to work. I was born for happiness, love, pleasure... and a good rest. [a joyful laugh at his own line]" GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: K4_master_neutral_O8.png, K4_angle_high_O13.png. One call, about $0.12. Run: python3 gen_t5c_start.py go
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
"Reference 2 shows the same man from above, head tilted back: "
"take the camera angle and the head pose from it, the face and the wig from reference 1. "
"Camera: "
"an arm's-length selfie angle IN FRONT of him and HIGH above his face, looking DOWN at him from about 55 degrees above as he leans back in a gilded armchair (a high angle, never eye level), rolled about 14 degrees to the right; "
"his face fills about 40 percent of the frame width with its centre at 50 percent, the whole tall wig about 75 percent of the width and inside the frame, the chin and the lace cravat in the lower middle, sharp. "
"Pose and emotion: "
"he has just leaned back into the carved gilded armchair, the head resting against its back, the eyes closed under heavy lids in a long happy sigh, the lips parted a little, a deeply contented face; "
"both hands rest on his belly over the scarlet coat, five natural fingers each, at the lower edge. "
"Around the edges of the frame: "
"the carved gilded armchair and the candlelit gilded hall blurred, no chandelier, and on the right and right-centre blurred figures far below: "
"a servant in livery, a courtier's powdered wig and shoulder, and a lady with a fan. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "K4_angle_high_O13.png"]}
open(H0 + "t5c_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t5c_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
