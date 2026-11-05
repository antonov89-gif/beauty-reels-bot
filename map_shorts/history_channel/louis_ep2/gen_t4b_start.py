"""T4b-1 START still (Take 4 piece 4b-1 "wine and laugh", setup S10a, prepared 05.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3: "[wine splashes over the lens] ...Mon Dieu. [silence, then he laughs for real] Nobody saw anything." The KING films now: his own arm's-length selfie from ABOVE (high angle, slightly dutch), face about 60 percent of the frame, clean lens at the start (the wine smear comes in the end still). GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs: 1 = card A3, 2 = R10 hall clean (ignore its angle, glasses and people). One call, about $0.12. Run: python3 gen_t4b_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
prompt = ("Vertical 9:16 hand-held phone selfie in dim candlelight, slightly underexposed, wide lens, real photograph, fine film grain, real skin texture, no beauty filter. "
"Reference 1 is the king's face and costume: exactly the same man, same age, heavy-lidded eyes, thin dark waxed moustache with curled tips, beauty mark on the viewer's right of the mouth as in reference 1, light rouge, the tall powdered wig in cool silver-grey and white like the pale grey in reference 1, NOT beige, NOT cream, NOT golden, the candlelight must not tint it, the scarlet velvet coat with gold suns, lace cravat. Reference 2 shows only the hall: ignore its camera angle and tilt, and do NOT copy the crystal glasses or the people at its table. Do not copy the background or the pose of reference 1. "
"Camera: the king's own arm's-length selfie from ABOVE, a high angle of about 35 degrees looking down at him, slightly dutch (rolled about 12 degrees to the left), wide lens, very close: his face fills about 60 percent of the frame width, the top of the tall wig cropped by the top edge, his face sharp and clearly readable, looking up into the lens, the nose slightly toward the frame right. At the lower edge of the frame only his scarlet coat with a gold sun, the lace cravat and a strip of bare white tablecloth; no hands in the frame, no cup, glass or goblet anywhere. "
"Pose and emotion: he has been waiting, patient and smug, heavy lids, lips closed in a faint knowing smirk, one eyebrow slightly raised, an expectant look into the lens. "
"Behind him, slightly out of focus: the candlelit gilded hall of reference 2, standing courtiers in plain wigs and ladies with open fans, a chandelier at the top. "
"No text, no logos, no modern objects, no extra fingers, no clown makeup, only one king.")
body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "R1_king_card_A3_white_wig.jpg", RAW + "R10_hall_clean.jpg"]}
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
open(H0 + "t4b_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/T4b_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
