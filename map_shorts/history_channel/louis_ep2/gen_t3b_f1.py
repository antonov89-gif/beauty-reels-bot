"""T3b food-burst still f1 (whole roast pheasant carried in); setup S7 burst, no face, prepared 05.11, NOT run until the owner's yes after seeing the Russian prompt. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, text only (NO reference image: the reviewer warned that the hall reference R10 carries real faces that can leak into the shots; the warm gilded colour is described in words and graded in the edit). One call, about $0.12. Run: python3 gen_t3b_f1.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
# TEXT_ONLY_NO_REFERENCE (food close-ups without faces; the hall reference would leak real faces)
prompt = ("Vertical 9:16 hand-held phone photo in dim ordinary candlelight, slightly underexposed, wide lens, a real photograph shot by a diner at a royal feast, fine film grain, uneven slightly greasy real food, messy table, crumbs and a smear on the cloth, no filter. "
"Camera: a low hand-held angle from table height looking up, the phone tilted and rolled about 10 degrees, a smudge flare of a greasy lens across the top corner. Subject: a whole roast pheasant with its long tail feathers on a big silver platter, carried in by a servant seen only as white-gloved hands and cuffs at the frame edges (no head, no face in the frame); the skin is uneven and dark in places, fat has pooled on the platter, a torn-off bit of crust, steam rising; behind, softly blurred warm gold candlelit palace hall, a blurred chandelier. "
"No faces and no people's faces visible, no text, no logos, no modern objects, no forks, no extra fingers.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high"}
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
