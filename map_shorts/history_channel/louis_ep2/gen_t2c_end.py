"""T2c END still (prepared 05.11, NOT run until the owner's yes after seeing the ref and the Russian prompt). An EDIT of the T2c start still: same camera, same framing, only the pose/expression and small room changes (proven route: P2 pose still for T2a v2). Owner 05.11 chose "В": the start still is kept as it is (camera from the king's right, beige wig; the wig is graded in the edit), so the end still keeps it EXACTLY too, or the Kling pins will not match. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, one ref = refs/T2c_start_4k.jpg (the 4K original itself, 2161x3840, not re-encoded: the 1440 copy measured detail 1.97 < 2.0). One call, about $0.12."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Edit the photo: keep EXACTLY the same camera position, the same framing, the same head size and head position in the frame, the same hand-held tilt, the same hall and background, the same gold dish of grapes at the lower edge and the same blurred sky-blue sleeve at the lower left corner. "
"Keep the man's face, age, skin, eyes, moustache, beauty mark, rouge, the wig (same shape and the same colour as in the photo, do not change it) and the scarlet velvet coat with gold suns, lace and rings EXACTLY as they are (do not redraw his face). "
"Change ONLY this: he has just put the grape into his mouth and is chewing with his lips closed, one cheek slightly full; his ringed hand has come down and rests on the edge of the table beside the dish, the fingers relaxed (five fingers); his eyes have turned sideways straight into the phone lens, heavy lids, one eyebrow slightly raised, a smug satisfied look, no smile, no open mouth. "
"In the background the people have moved a little: the lady nearest the king now holds her fan up beside her face, whispering to her neighbour, and the servant with the dish has walked further to the right edge of the frame. "
"Real phone photo, fine film grain, real skin texture, no beauty filter. No text, no logos, no modern objects, no extra fingers, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "T2c_start_4k.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t2c_end_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T2c_end_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
