"""Take 1 NEW piece 1a: Is it on / Ah there I am / Bonjour / Welcome to Versailles (setup S1, extreme low selfie): END still, an EDIT of the start still (same camera, different pose; prepared 06.11, NOT run until the owner's yes). One ref = refs/t1na_start_4k.jpg (the 4K original). One call, about $0.12. Run: python3 gen_t1na_end.py go
BRIEF: briefs/brief_t1na.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Reference 1 is the photo to edit; "
"reference 2 is identity only (the neutral frontal master): "
"use it only to keep the face, moustache, beauty mark on the viewer's right of the mouth and rouge, and never copy its pose, angle or framing. "
"Edit the photo (reference 1): "
"keep EXACTLY the same low selfie angle from under the chin, the same roll, the same ceiling and cornice behind, the same wig, coat and cravat. "
"Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY (do not redraw his identity); "
"the wig keeps its silver-grey and white (a light tint from the scene light is fine). "
"Change ONLY the distance and the expression: "
"the camera has been pulled back a little, so that his head with the wig now fills about 80 percent of the frame width (his face about 36 percent) with its centre at 50 percent, the same painted ceiling and gold cornice, the same blurred shapes in the lower corners; "
"the lower right corner stays as in the photo, blurred hall, fan and candles; "
"he has seen himself and is pleased: "
"heavy lids, the eyes now on the lens, the lips closed in a smug faint smile, the head turned about 5 degrees toward his left, the chin lifted, the gaze straight into the lens (the head moves 3 to 5 percent). "
"QUALITY: "
"keep the full resolution, sharpness and fine detail of the original photo: "
"the face, the moustache hairs, the wig curls, the lace and the gold embroidery must stay exactly as crisp and detailed as in the photo; "
"no smoothing, no blur, no softening, no painted or mottled texture on the skin; "
"natural detail, no over-sharpening, no halos. "
"Real handheld footage, fine film grain, real skin texture, no beauty filter. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "t1na_start_4k.jpg", RAW + "K4_master_neutral_O8.png"]}
open(H0 + "t1na_end_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t1na_end_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
