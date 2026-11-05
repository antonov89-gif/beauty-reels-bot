"""T3b food-burst still f1 (whole roast pheasant carried in); setup S7 burst, no face, prepared 05.11, NOT run until the owner's yes after seeing the reference and the Russian prompt. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, one reference = R10 hall clean (room colour only). One call, about $0.12. Run: python3 gen_t3b_f1.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone photo in dim candlelight, slightly underexposed, wide lens, real photograph, fine film grain, natural messy real food, not a commercial food shot, no filter. "
"Reference 1 shows only the hall: use its warm candlelit gilded colour and blurred gold background; do not copy its composition and show no people's faces. "
"Camera: a low hand-held angle from table height looking slightly up, as if the phone is held in one hand and tilted, a slight roll of about 10 degrees. Subject: a whole roast pheasant dressed with its long tail feathers on a big silver platter, carried in by a servant whose white-gloved hands and cuffs are visible at the frame edges, golden glistening skin, steam rising, the gilded candlelit hall of reference 1 softly blurred behind, a blurred chandelier. "
"No faces, no people's faces visible, no text, no logos, no modern objects, no extra fingers, no plastic look.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R10_hall_clean.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t3b_f1_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T3b_F1_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
