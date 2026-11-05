"""T4a START still (Take 4 "The drink", piece 4a, setup S9, prepared 05.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3: "No glass on my table. Thirsty? I just... [lifts one finger without looking] / CUPBEARER (off screen): A drink for the King! / [the cup goes from hand to hand behind him; he waits, drumming his fingers] ...and I wait." New angle (not close/eye-level/side as S5/T2c): from across the table, wide medium, slightly above eye level, the king in the right third, the empty place setting in front of him, a cupbearer small and far behind. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs: 1 = card A3, 2 = R10 hall clean (ignore its angle). One call, about $0.12. Run: python3 gen_t4a_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone photo in dim candlelight, slightly underexposed, wide lens, real photograph, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, beauty mark on the viewer's right of the mouth as in reference 1, light rouge, the tall powdered wig in cool silver-grey and white like the pale grey in reference 1, NOT beige, NOT cream, NOT golden, the candlelight must not tint it, the scarlet velvet coat with gold suns, lace cravat and rings. Reference 2 shows only the hall: ignore its camera angle and tilt, and do NOT copy the crystal glasses or the people at its table. Do not copy the background or the pose of reference 1. "
"Camera: the page Marcel films from across the long dining table, standing, the phone held a little above the king's eye level (a high-ish angle of about 20 degrees looking down), a medium-wide shot, rolled about 8 degrees to the right, wide lens. The king sits at the head of the table in the right third of the frame and fills about 45 percent of the frame width, chest up with the table edge in front of him, his head at least 15 percent of the frame width, the face sharp and clearly readable, the top of the wig inside the frame; his face is turned toward the centre of the frame (the nose points to the frame left), the beauty mark stays visible on the viewer's right of the mouth as in reference 1, and his stare goes straight into the lens. The table edge runs diagonally from the lower right to the upper left, the candelabra on it recede to the left. "
"The table: the whole visible tablecloth carries only plates, folded napkins, bread rolls, low candelabra and one low bowl of flowers, and the cloth in front of the king is bare around his plate. "
"Pose and emotion: bored and haughty, heavy lids, mouth closed with the corners slightly down, one eyebrow slightly raised; his right hand with four rings lies relaxed on the cloth beside the plate, four fingers curled slightly and the thumb visible, the rings clearly formed; his other hand is below the table edge, out of view. "
"Behind him and around him, slightly out of focus: the candlelit gilded hall of reference 2, two rows of standing courtiers in plain wigs, ladies with open fans whispering, and far in the left background, small and blurred, at a side door of the hall, a cupbearer in livery with an empty gold tray in his hands, walking away. "
"No text, no logos, no modern objects, no extra fingers, no clown makeup, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg", RAW + "R10_hall_clean.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t4a_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T4a_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
