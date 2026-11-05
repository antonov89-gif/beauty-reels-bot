"""T4a END still (Take 4 the drink, piece 4a, prepared 05.11, NOT run until the owner's yes after seeing the ref and the Russian prompt). An EDIT of the T4a start still: same camera/composition/head box, only the pose, the gaze and the room change. Script 7.3: "[lifts one finger without looking] / CUPBEARER: A drink for the King! / [the cup goes from hand to hand behind him; he waits, drumming his fingers] ...and I wait." GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, one ref = refs/T4a_start_4k.jpg (the 4K original). One call, about $0.12. Run: python3 gen_t4a_end.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Edit the photo: keep EXACTLY the same camera position, the same high-ish angle across the table, the same roll, the same framing, the same head size and head position in the frame (the king in the right third, his head the same size), the same table edge running diagonally with the same candelabra and flowers, and the same plates, napkins and bread rolls; the cloth in front of the king stays bare around his plate with no glass or cup on it. His face stays turned toward the frame centre (the nose toward the frame left) with the beauty mark on the viewer's right of the mouth. "
"Keep the man's face, age, skin, eyes, moustache, rouge, the wig (same shape and the same cool silver-grey and white colour as in the photo, NOT beige, NOT cream, NOT golden, the candlelight must not tint it) and the scarlet velvet coat with gold suns, lace and rings EXACTLY as they are (do not redraw his face). "
"Change ONLY this: his eyes no longer look into the lens: they look away and up to the right of the frame, toward the ceiling and the doorway, bored, under heavy lids, mouth closed, one eyebrow slightly raised, as if he is waiting and not looking; the hand with four rings, which lay on the cloth, is now raised to about the height of his shoulder with only the index finger lifted and the other fingers curled, the thumb tucked (exactly five fingers, the same rings), without looking at it. "
"In the background the cupbearer from the left has walked to the middle of the hall, small, a second servant in livery beside him, and behind the king's right shoulder, at the edge of the frame, a white-gloved servant's hand passes a gold goblet to another white-gloved hand, blurred; the courtiers have shifted a little, one lady's fan has moved, one courtier has turned his head toward the goblet. "
"QUALITY: keep the full resolution, sharpness and fine detail of the original photo: the face, the moustache hairs, the wig curls, the lace and the gold embroidery must stay exactly as crisp and detailed as in the photo; no smoothing, no blur, no softening, no painted or mottled texture on the skin; natural detail, no over-sharpening, no halos, no exaggerated pores. "
"Real phone photo, fine film grain, real skin texture, no beauty filter. No text, no logos, no modern objects, no extra fingers, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "T4a_start_4k.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t4a_end_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T4a_end_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
