"""T3b food-burst still f5 (gravy poured over meat); setup S7 burst, no face, prepared 05.11, NOT run until the owner's yes after seeing the reference and the Russian prompt. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, one reference = R10 hall clean (room colour only). One call, about $0.12. Run: python3 gen_t3b_f5.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone photo in dim candlelight, slightly underexposed, wide lens, real photograph, fine film grain, natural messy real food, not a commercial food shot, no filter. "
"Reference 1 shows only the hall: use its warm candlelit gilded colour and blurred gold background; do not copy its composition and show no people's faces. "
"Camera: a hand-held close shot from a low angle, a pink blurred thumb of the person holding the phone covering the lower left corner of the lens (a phone mistake), a slight tilt. Subject: a silver sauce boat in a white-gloved hand pouring thick brown gravy over slices of roast meat on a silver platter, a long glistening drip falling, steam, candle glints, the blurred gilded hall behind. "
"No faces, no people's faces visible, no text, no logos, no modern objects, no extra fingers, no plastic look.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R10_hall_clean.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t3b_f5_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T3b_F5_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
