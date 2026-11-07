"""Take 4b v3 piece A: Marcel spills the wine, looks at the camera and at the king, 'Sorry, Sire' (setup S9b, from the side): END still, an EDIT of the start still (same camera, different pose; prepared 06.11, NOT run until the owner's yes). One ref = refs/t4bA_start_4k.jpg (the 4K original). One call, about $0.12. Run: python3 gen_t4bA_end.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Reference 1 is the photo to edit; "
"reference 2 is the king's identity only (his neutral master portrait: "
"the same man of about 45 with the moustache, beauty mark on the viewer's right of the mouth, silver-grey and white wig) and reference 3 is Marcel's identity only (freckles, thick dark brows, white wig, pale blue livery, no tricorn hat): "
"use them only to keep the faces, and never copy their poses, angles or framing. "
"Edit the photo (reference 1): "
"keep EXACTLY the same camera position from the side, the same table height, the same roll, the same framing and crop, the same positions and sizes of both heads (the king's face centre at 30 percent and Marcel's at 76 percent of the frame width), the same wigs, coats and the same hall behind. "
"Change ONLY the moment: "
"the gold goblet has fallen over on its side on the white tablecloth, empty, the small gold tray beside it, and a natural pool of dark red wine has spread over the cloth between them and ran to the table edge, a little of it on the edge of the king's cuff only (none on his face, wig or cravat); "
"Marcel stands frozen, bent a little, both hands raised open in front of his chest (five natural fingers each), his eyes wide, looking straight into the lens, his lips slightly parted as if about to speak; "
"the king has turned his head toward Marcel (the viewer's right), his chin level, heavy lids, a blank unreadable face, the lips closed; "
"Marcel's head is a little bowed. "
"The heads move at most 4 percent of the frame width. "
"QUALITY: "
"keep the full resolution, sharpness and fine detail of the original photo: "
"the face, the moustache hairs, the wig curls, the lace and the gold embroidery must stay exactly as crisp and detailed as in the photo; "
"no smoothing, no blur, no softening, no painted or mottled texture on the skin; "
"natural detail, no over-sharpening, no halos. "
"Real handheld footage, fine film grain, real skin texture, no beauty filter. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "t4bA_start_4k.jpg", RAW + "K4_master_neutral_O8.png", RAW + "R8_marcel_full.jpg"]}
open(H0 + "t4bA_end_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t4bA_end_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
