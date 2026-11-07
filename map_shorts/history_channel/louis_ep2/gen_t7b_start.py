"""Take 7 piece 7b he stands, the crowd bows, bye, subscribe (setup S14, low swing up): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS (OWNER): "[stands up, the crowd bows] That's all. Bye. I'm busy. [beat, points at the lens] ...And you: subscribe to my stunning channel. And like. [pause, a lazy wave of the hand, he looks away, bored] Or... whatever." Hard cut on "Or... whatever." to the end card. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: K4_master_neutral_O8.png, K4_angle_low_O12.png, R10_hall_clean.jpg. One call, about $0.12. Run: python3 gen_t7b_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 (the king's master portrait) is his face and costume: "
"exactly the same man of about 45, same heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; "
"do not copy its neutral pose or backdrop. "
"Reference 2 shows the same man from below, chin raised: "
"take the camera angle and the head pose from it, the face and the wig from reference 1. "
"Reference 3 shows only the hall: "
"ignore its angle, and do NOT copy its crystal glasses or the people at its table; "
"Camera: "
"his own phone in his outstretched hand held LOW, near the level of the table, looking UP at him as he rises from the gilded armchair: "
"a low angle of about 30 degrees from below, wide lens, rolled about 8 degrees to the left; "
"his face fills about 36 percent of the frame width with its centre at 50 percent, the whole tall wig and side curls inside the frame with at least 6 percent free on each side, the head in the upper middle of the frame, sharp, his chin raised; "
"behind and above him the gilded ceiling edge and the candlelit hall; "
"no chandelier. "
"Pose and emotion: "
"he is half risen, his free hand pressing on the white tablecloth at the lower edge (five natural fingers), the look haughty and bored under heavy lids, the lips closed in a faint smirk; "
"behind him at both sides the courtiers in plain wigs and the ladies in wide gowns are just starting to bow, their heads dipping at different depths. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "K4_angle_low_O12.png", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t7b_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t7b_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
