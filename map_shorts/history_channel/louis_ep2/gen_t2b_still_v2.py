"""T2b start still v2 (owner 05.11 "2": GPT Image 2.5, re-worded, refs hall-only + Marcel + card A3; no re-used king still). Earlier: T2b start still (owner 05.11 "1"): Marcel's low phone view. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, refs: 1 = the A3 edit (the hall, the king's look), 2 = Marcel full-length (his shoes, stockings, sleeve). One call, about $0.12, no retries."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 phone photo, wide lens, slightly underexposed, a real photograph with fine film grain, photorealistic. "
"Reference 1 shows the hall only: use it for the same gilded candlelit dining hall at night (windows, paintings, candelabra, people in plain wigs). Reference 2 shows the page Marcel: use it only for his white stockings, black buckled shoes and sky-blue sleeve with silver braid. Reference 3 shows the king: use it only for his costume and wig (a small far figure). Do not copy any pose or framing from the references. "
"Camera: a phone held low by a page, pointing down at a steep angle, the horizon tilted. Bottom third: the polished parquet floor and a pair of black buckled shoes with white stockings, slightly out of focus, a sky-blue cuff with silver braid at the lower edge. Middle: a very long dining table with a white cloth, gold plates and candelabra with lit candles seen from a low angle, ladies in silk gowns seated on folding stools along the near side, men in plain wigs standing behind them. Far away at the head of the table, small in the frame, the king in a scarlet coat with gold suns and a tall white-grey wig. Top: the gilded hall and chandeliers, cut by the frame edge. "
"No text, no captions, no logos, no modern objects, no extra fingers, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "refs/R9_hall_only.jpg", RAW + "refs/R8_marcel_full_768.jpg", RAW + "refs/R1_king_card_A3_white_wig.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/pilot_frames/"
open(H0 + "../t2b_still_v2_prompt.txt", "w").write(prompt)
r = apipod.submit("images", body); print(r)
tid = (r.get("data") or {}).get("task_id")
if not tid: sys.exit("not submitted")
out = H0 + "anchors/T2b_start_marcel_v2_4k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=900, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
if u: apipod.download(u, out); print("saved")
