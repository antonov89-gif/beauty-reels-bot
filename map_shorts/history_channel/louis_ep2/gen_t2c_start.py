"""T2c START still (prepared 05.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs: 1 = card A3 (face), 2 = K_right34 (angle), 3 = R9 hall only (room). One call, about $0.12."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone photo, wide lens, slightly underexposed, real photograph, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's face and costume: exactly the same man, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, beauty mark beside the mouth, light rouge, the tall white-grey powdered wig, the scarlet velvet coat with gold suns, lace cravat and rings. Reference 2 shows only the camera angle on his face (three-quarter side view). Reference 3 shows only the hall. Do not copy the background or the pose of references 1 and 2. "
"Camera: the page Marcel films him from the side, close, at the king's eye level, the phone held in a hand (slightly tilted), so we see the king in a three-quarter side view, his left cheek toward the camera, from the chest up; a blurred edge of a sky-blue sleeve with silver braid at the lower left corner of the frame (the page's own arm). "
"Pose and emotion: the king sits at the head of the long table; in front of him a gold dish with a bunch of dark grapes; he holds ONE grape between two ringed fingers near his mouth, looking at it with bored, haughty heavy lids, mouth closed, about to speak. "
"Behind him, slightly out of focus: the candlelit gilded hall of reference 3, ladies on folding stools with open fans whispering to each other, standing courtiers in plain wigs. "
"No text, no logos, no modern objects, no extra fingers, no blond or cream wig, no clown makeup, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg", RAW + "K_right34.jpg", RAW + "R9_hall_only.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t2c_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T2c_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
