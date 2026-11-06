"""T4b-1 END still (Take 4 wine and laugh, prepared 05.11, NOT run until the owner's yes after seeing the ref and the Russian prompt). An EDIT of the T4b start still: same camera/crop/head position; the wine film on the left third of the lens and the king's one real laugh. Script 7.3: "[wine splashes over the lens] ...Mon Dieu. [silence, then he laughs for real] Nobody saw anything." GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, one ref = refs/T4b_start_4k.jpg (the 4K original). One call, about $0.12. Run: python3 gen_t4b_end.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Edit the photo: keep EXACTLY the same camera position, the same high-ish selfie angle, the same roll, the same framing and crop, the same head size and head position (the face a little right of centre, its centre at 58 percent of the frame width), the same tall wig, the same blurred hall behind him with the lady with the fan at the left and the courtiers at the right, and the same scarlet coat with the gold sun and the lace cravat at the lower edge; no cup, glass or goblet anywhere, no hands in the frame. "
"Keep the man's face, age, skin, moustache with its curled tips, the beauty mark on the viewer's right of the mouth, rouge, the wig (same shape and the same cool silver-grey and white colour as in the photo, NOT beige, NOT cream, NOT golden, the candlelight must not tint it) and the coat EXACTLY as they are (do not redraw his identity). The red film does not tint the wig or the face outside its own area. "
"Change ONLY this: (1) a deep red wine film has been splashed over the LEFT THIRD of the lens: a translucent liquid film, dark and thick at its irregular curved edge, thin and transparent inside, with thick drops and runs sliding down, a soft blur inside it and candle highlights refracting in the drops; its edge lies between 25 and 35 percent of the frame width, curved and irregular like a real splash, running through the side curls of the wig and NEVER reaching the face (no drip and no blur to the right of 36 percent of the width at face height); the lady with the fan is seen through it as a red blur; there is no straight vertical line, no flat red overlay and no red on the skin; the right two thirds stay sharp. "
"(2) He is laughing for real: the head tipped back about 10 to 15 degrees with the chin lifted and no sideways turn; the head, the top of the wig, the face centre and the head size stay within 3 percent of the photo; the shoulders lift slightly but stay inside the same crop; the eyes squeezed nearly shut under heavy lids, one eyebrow up, laugh creases at the eyes and cheeks; a big real laugh with the mouth open, the upper teeth visible, natural and slightly uneven, the lower teeth mostly hidden by the lip and shadow, the tongue not shown; the moustache with its curled tips and the beauty mark on the viewer's right of the mouth stay visible and in place. "
"QUALITY: keep the full resolution, sharpness and fine detail of the original photo in the sharp area: the face, the moustache hairs, the wig curls, the lace and the gold embroidery must stay exactly as crisp and detailed as in the photo; no smoothing, no blur, no softening, no painted or mottled texture on the skin; natural detail, no over-sharpening, no halos, no exaggerated pores. The wine film is a lens effect; the sharp area is untouched. "
"Real phone selfie, fine film grain, real skin texture, no beauty filter. No text, no logos, no modern objects, no extra fingers, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "T4b_start_4k.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t4b_end_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T4b_end_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
