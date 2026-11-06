"""Take 4 piece 4b-2 Marcel through the wine (setup S10): END still, an EDIT of the start still (same camera, different pose; prepared 06.11, NOT run until the owner's yes). One ref = refs/t4b2_start_4k.jpg (the 4K original). One call, about $0.12. Run: python3 gen_t4b2_end.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Edit the photo: "
"keep EXACTLY the same camera position, the same low angle, the same roll, the same framing and crop, the same head size and head position (face centre at 54 percent of the frame width), the same white wig, the same blue livery coat and lace, the same hall behind, and the same wine film on the left third of the lens (same edge, same drops). "
"Keep Marcel's face, freckles, thick brows, age and skin EXACTLY (do not redraw his identity). "
"Change ONLY his expression and head: "
"he has just heard 'Joking' and is relieved but shaken, saying quietly 'Sorry, Sire': "
"the head bowed forward about 8 degrees with the chin tucked, the eyes looking up into the lens under raised brows, a tiny trembling forced half-smile, the lips slightly parted in the middle of a word, the shoulders dropped a little; "
"the head, the top of the wig and the face centre stay within 3 percent of the photo. "
"QUALITY: "
"keep the full resolution, sharpness and fine detail of the original photo: "
"the face, the moustache hairs, the wig curls, the lace and the gold embroidery must stay exactly as crisp and detailed as in the photo; "
"no smoothing, no blur, no softening, no painted or mottled texture on the skin; "
"natural detail, no over-sharpening, no halos. "
"Real phone footage, fine film grain, real skin texture, no beauty filter. "
"No text, no logos, no modern objects, no extra fingers, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "t4b2_start_4k.jpg"]}
open(H0 + "t4b2_end_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t4b2_end_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
