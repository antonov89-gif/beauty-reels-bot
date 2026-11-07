"""Take 5 piece 5b Marcel films the laden table and the king eating (no words): END still, an EDIT of the start still (same camera, different pose; prepared 06.11, NOT run until the owner's yes). One ref = refs/t5b_start_4k.jpg (the 4K original). One call, about $0.12. Run: python3 gen_t5b_end.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Edit the photo: "
"the same hall, the same table and dishes (the same arrangement of the food, now seen from the new camera position), the same wig and coat. "
"Change ONLY the camera and the king: "
"the camera has tilted UP about 20 degrees and moved in, rolled about 4 degrees to the left, so that now the king is the subject, sharp, his face filling about 38 percent of the frame width (the whole wig inside the frame, centre at 50 percent), the food now soft at the lower edge; "
"behind him the lady with the fan at the right, standing courtiers in plain wigs and a servant; "
"his cheeks full of food, chewing happily with a closed mouth, eyes closed under heavy lids in bliss, one hand holding a golden spoon near the lower edge. "
"Keep the man's face, age, skin, moustache, beauty mark on the viewer's right of the mouth and rouge EXACTLY as in reference 2 (the card; "
"reference 1 is the start photo) (do not redraw his identity); "
"the wig keeps its silver-grey and white (a light tint from the scene light is fine). "
"QUALITY: "
"keep the full resolution, sharpness and fine detail of the original photo: "
"the face, the moustache hairs, the wig curls, the lace and the gold embroidery must stay exactly as crisp and detailed as in the photo; "
"no smoothing, no blur, no softening, no painted or mottled texture on the skin; "
"natural detail, no over-sharpening, no halos. "
"Real phone footage, fine film grain, real skin texture, no beauty filter. "
"No text, no logos, no modern objects, no extra fingers, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "t5b_start_4k.jpg", RAW + "K4_master_neutral_O8.png"]}
open(H0 + "t5b_end_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t5b_end_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
