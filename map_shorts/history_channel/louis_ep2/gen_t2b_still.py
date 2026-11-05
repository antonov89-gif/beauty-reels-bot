"""T2b start still (owner 05.11 "1"): Marcel's low phone view. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, refs: 1 = the A3 edit (the hall, the king's look), 2 = Marcel full-length (his shoes, stockings, sleeve). One call, about $0.12, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 hand-held phone photo, ultra-wide front camera look, slightly underexposed, a real photograph with fine film grain, photorealistic, no retouching. "
"The FIRST reference image shows the hall and the king: use it for the SAME gilded candlelit dining hall at night and for how the king looks. The SECOND reference image shows Marcel the page: use it only for his white stockings, black buckled shoes and sky-blue coat sleeve with silver braid. "
"The picture is what a nervous young page sees on his phone while filming with the phone held low and pitched DOWN toward the floor: the bottom third of the frame is the polished parquet floor and Marcel's own white-stockinged legs and black buckled shoes, slightly out of focus, the edge of his sky-blue sleeve with silver braid and a thumb at the lower right corner of the frame; the middle of the frame is the very long dining table with a white cloth, gold plates and candelabra with lit candles seen from a low angle, a few ladies seated on folding stools along the near side of the table with their silk skirts and shoes, standing courtiers in plain wigs behind them; far away at the head of the table, small in the frame, sits the king in his scarlet velvet coat with gold suns and the tall white-grey powdered wig (a small distant figure, face tiny); the top of the frame shows the gilded hall and chandeliers cut by the frame edge. The horizon is slightly tilted. "
"No text, no captions, no logos, no modern objects, no extra fingers, no blond or cream wig, no clown makeup, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "pilot_frames/T1_keyframe_edit_768.jpg", RAW + "refs/R8_marcel_full_768.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/pilot_frames/"
open(H0 + "../t2b_still_prompt.txt", "w").write(prompt)
r = apipod.submit("images", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted")
out = H0 + "anchors/T2b_start_marcel_4k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=900, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
if u: apipod.download(u, out); print("saved")
