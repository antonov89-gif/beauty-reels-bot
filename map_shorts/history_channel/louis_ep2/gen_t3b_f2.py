"""T3b food-burst still f2 (two partridges on a silver-gilt plate); setup S7 burst, no face, prepared 05.11, NOT run until the owner's yes after seeing the Russian prompt. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, text only (NO reference image: the reviewer warned that the hall reference R10 carries real faces that can leak into the shots; the warm gilded colour is described in words and graded in the edit). One call, about $0.12. Run: python3 gen_t3b_f2.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
# TEXT_ONLY_NO_REFERENCE (food close-ups without faces; the hall reference would leak real faces)
prompt = ("Vertical 9:16 hand-held phone photo in dim ordinary candlelight, slightly underexposed, wide lens, a real photograph shot by a diner at a royal feast, fine film grain, uneven slightly greasy real food, messy table, crumbs and a smear on the cloth, no filter. "
"Camera: a close hand-held shot from above and slightly from the side, the phone very close and tilted, the edge of the filming person's finger partly in the top right corner, blurred, a focus miss on the near rim of the plate. Subject: two small roast partridges on a silver-gilt plate, slightly greasy, a drip of fat sliding down, a visible green sprig of herbs, a smear on the white tablecloth, steam, a silver knife; no hands in the frame; warm candlelight, the blurred gilded hall far behind. "
"No faces and no people's faces visible, no text, no logos, no modern objects, no forks, no extra fingers.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high"}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t3b_f2_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T3b_F2_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
