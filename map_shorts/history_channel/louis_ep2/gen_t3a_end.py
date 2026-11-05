"""T3a END still (prepared 05.11, NOT run until the owner's yes after seeing the ref and the Russian prompt). An EDIT of the T3a start still: same camera, same framing, only his pose/expression and the servant change (proven route: P2 pose still, T2c end still). GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, one ref = refs/T3a_start_4k.jpg (the 4K original, not re-encoded). Piece 3a: "Four rounds. First, soup. [slurps] My sister-in-law says I eat four bowls. [a servant puts down one more] ...She can't count." One call, about $0.12."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Edit the photo: keep EXACTLY the same camera position, the same very low angle looking up from the table, the same framing, the same head size and head position in the frame, the same tilt and roll, the same hall and background, the same big silver soup bowl in the foreground and the same blurred pink thumb at the lower left corner. "
"Keep the man's face, age, skin, eyes, moustache, beauty mark, rouge, the wig (same shape and the same colour as in the photo, do not change it) and the scarlet velvet coat with gold suns, lace and rings EXACTLY as they are (do not redraw his face). "
"Change ONLY this: he has just slurped the soup, the spoon is lowered into the bowl in his ringed hand (five fingers), his lips are slightly wet and shiny, his mouth closed, and his eyes look flatly and deadpan straight into the phone lens under heavy lids, no smile, one eyebrow slightly raised, as if he has just said something dry about his sister-in-law. "
"The servant's gloved hand at the right edge has now put a second silver bowl down on the table next to the first one, and the hand is drawing back, blurred. In the background the lady behind has her fan raised beside her face and the courtiers have shifted a little. "
"QUALITY: keep the full resolution, sharpness and fine detail of the original photo: the face, the moustache hairs, the wig curls, the lace and the gold embroidery must stay exactly as crisp and detailed as in the photo; no smoothing, no blur, no softening, no painted or mottled texture on the skin; natural detail, no over-sharpening, no halos, no exaggerated pores. "
"Real phone photo, fine film grain, real skin texture, no beauty filter. No text, no logos, no modern objects, no extra fingers, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "T3a_start_4k.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t3a_end_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T3a_end_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
