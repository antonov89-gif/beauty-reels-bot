"""T3a START still (S6, prepared 05.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Piece 3a: "Four rounds. First, soup. [slurps] My sister-in-law says I eat four bowls. [a servant puts down one more] ...She can't count." Setup S6 = very low from the table looking up, bowls in the foreground, push-in (reference shot 3). GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs: 1 = card A3 (face and costume, 768x1376 best original), 2 = R10 hall clean (room only, native 1686x1920). The angle is described in words (no 512 px tile). One call, about $0.12."""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone photo, wide lens, slightly underexposed, real photograph, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's face and costume: exactly the same man, the same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, beauty mark beside the mouth, light rouge, the tall white-grey powdered wig, the scarlet velvet coat with gold suns, lace cravat and rings. Reference 2 shows only the hall. Do not copy the background or the pose of reference 1. "
"Camera: a very low angle, the phone held at table height, almost on the tablecloth, looking UP at the king (a worm's-eye view, rolled about 15 degrees, a slightly tilted horizon): in the foreground a big silver soup bowl with steam and a silver spoon, partly blurred, filling the lower third of the frame; the king sits behind it, we see him from below, his chin, moustache, nostrils and the towering wig against the gilded ceiling and a chandelier, his face still clearly recognisable and in focus. "
"Pose and emotion: he is bending slightly toward the bowl with the spoon raised to his lips, his eyes looking down at the soup with heavy bored haughty lids, mouth closed, about to slurp; one ringed hand holds the spoon, five fingers. "
"Behind and beside him, slightly out of focus: the candlelit gilded hall of reference 2, ladies on folding stools whispering behind open fans, standing courtiers shifting their weight, a servant in livery with a covered silver dish waiting at the right edge. "
"A small phone mistake: a blurred fingertip of the page's hand at the lower right corner of the frame. "
"No text, no logos, no modern objects, no extra fingers, no blond or cream wig, no clown makeup, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg", RAW + "R10_hall_clean.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t3a_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T3a_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
