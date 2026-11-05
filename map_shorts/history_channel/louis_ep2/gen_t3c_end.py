"""T3b-C END still (prepared 05.11, NOT run until the owner's yes after seeing the ref and the Russian prompt). An EDIT of the T3b-C start still: same camera/framing/head, only the pose, the fork and the expression change. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, one ref = refs/T3c_start_4k.jpg (the 4K original). Piece: "What is that? A fork? [pushes it away with two fingers, disgusted]". One call, about $0.12. Run: python3 gen_t3c_end.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Edit the photo: keep EXACTLY the same camera position, the same framing, the same head size and head position in the frame, the same rolled hand-held tilt, the same hall and background, the same silver platter with the roast pheasant at the lower part of the frame and the same sky-blue sleeve with braid at the lower left corner. "
"Keep the man's face, age, skin, eyes, moustache, beauty mark, rouge, the wig (same shape and the same colour as in the photo, do not change it) and the scarlet velvet coat with gold suns, lace and rings EXACTLY as they are (do not redraw his face). "
"Change ONLY this: the torn-off pheasant leg is now held lifted in his hand on the viewer's left, away from the platter; a silver two-pronged fork on a short handle, held by a hand in the sky-blue sleeve, comes in from the lower left corner toward him, its big blurred head close to the lens; two ringed fingers of his hand on the viewer's right push the fork away by its tines, the other fingers curled back (rings on the visible fingers, no extra fingers). "
"His head is turned a little toward the fork, his upper lip curled in disgust, one eyebrow raised, heavy bored haughty lids, his eyes on the fork, mouth closed, no smile. "
"In the background the people have moved a little: the lady behind leans toward her neighbour and whispers behind her fan, a courtier turns his head, the servant with the dish has walked on to the right edge. "
"QUALITY: keep the full resolution, sharpness and fine detail of the original photo: the face, the moustache hairs, the wig curls, the lace and the gold embroidery must stay exactly as crisp and detailed as in the photo; no smoothing, no blur, no softening, no painted or mottled texture on the skin; natural detail, no over-sharpening, no halos, no exaggerated pores. "
"Real phone photo, fine film grain, real skin texture, no beauty filter. No text, no logos, no modern objects, no extra fingers, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "T3c_start_4k.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t3c_end_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T3c_end_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
