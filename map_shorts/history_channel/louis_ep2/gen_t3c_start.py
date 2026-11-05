"""T3b-C START still (S8a fork gag, prepared 05.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Piece: "[tears a leg; Marcel's fork comes into the lens] What is that? A fork? [pushes it away with two fingers, disgusted]". GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs: 1 = card A3 (face and costume, 768x1376 best original), 2 = R10 hall clean (room only). Angle in words. One call, about $0.12. Run: python3 gen_t3c_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone photo in dim candlelight, slightly underexposed, wide lens, real photograph, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, beauty mark beside the mouth (on the side where his left cheek shows), light rouge, the tall white-grey powdered wig, the same colour as reference 1, the scarlet velvet coat with gold suns, lace cravat and rings. Reference 2 shows only the hall: ignore its camera angle and tilt. Do not copy the background or the pose of reference 1. "
"Camera: the page Marcel films from the table height, close, on the king's left front, slightly across the table, wide lens, rolled about 12 degrees; a thin blurred sliver of a sky-blue sleeve with silver braid at the very lower-left edge. The roast pheasant on a silver platter with rising steam and the hands fill the lower 40% of the frame; his face is in the upper middle, three-quarter, the nose toward the frame left, lit, natural and in focus. "
"Pose and emotion: with one ringed hand he pins the carcass flat on the platter, with the other he pulls the drumstick, which is still half attached with the skin stretching (rings on three visible fingers, thumb on top); grease on his fingers and a shine on his lips; he looks at the leg under heavy bored haughty lids, mouth closed, about to bite. "
"Behind him, slightly out of focus: the candlelit gilded hall of reference 2, ladies on folding stools whispering behind open fans, standing courtiers shifting their weight, a servant crossing with a dish. "
"Bare hands only, nothing on the platter but the pheasant. No text, no logos, no modern objects, no extra fingers, no clown makeup, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg", RAW + "R10_hall_clean.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t3c_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T3c_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
