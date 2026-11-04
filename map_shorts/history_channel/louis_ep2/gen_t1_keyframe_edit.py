"""T1 keyframe by EDITING card A3 (owner 04.11 "делай"): GPT Image 2.5 Sunburst Lite, 4K, quality high, 9:16, only image_urls = A3. One call, about $0.12, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Edit the photo: keep the man, his face, his tall white-grey wig, his scarlet velvet coat with gold suns, lace cravat and cuffs, jewelled rings, his pose and his expression EXACTLY as they are (do not redraw or change his face, age, skin or moustache). "
"Change only the setting around him: he now sits at the head of a very long dining table with a white cloth, gold plates and candelabra with lit candles in a gilded antechamber of Versailles at night, warm candlelight only; behind the table a standing crowd of courtiers in plain simple wigs and dark period clothes, in the front row four or five ladies seated on folding stools; the table is visible beside him. "
"Same hand-held phone-selfie look, fine film grain, real skin texture. No text, no logos, no modern objects, no extra fingers, no blond or cream wig, no clown makeup.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg"]}
r = apipod.submit("images", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted")
out = "pilot_frames/T1_keyframe_edit_4k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=600, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
u = find(res.get("data") or {}); d = res.get("data") or {}
print("status", d.get("status"), "usage", d.get("usage"))
if u: apipod.download(u, out); print("saved")
