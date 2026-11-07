"""Take 1 NEW piece 1a: Is it on / Ah there I am / Bonjour / Welcome to Versailles (setup S1, extreme low selfie): START still (prepared 06.11, NOT run until the owner's yes after seeing the refs and the Russian prompt). Script 7.3 lines: LOUIS: "[phone too close, muffled] Is it... is it on? [pulls it back, sees himself, pleased] Ah. There I am. [clears throat] Bonjour. I am Louis, King of France. Welcome to Versailles." GPT Image 2.5 Sunburst Lite, 4K, high, 9:16. Refs in order: K4_master_neutral_O8.png, K4_angle_low_O12.png. One call, about $0.12. Run: python3 gen_t1na_start.py go"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real skin texture, no beauty filter. "
"Reference 1 (the king's master portrait) is his face and costume: "
"exactly the same man of about 45, same heavy-lidded eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in cool silver-grey and white (NOT beige, NOT cream, NOT golden), the scarlet velvet coat with gold suns, lace cravat; "
"do not copy its neutral pose or backdrop. "
"Reference 2 shows the same man from below, chin up: "
"take the camera angle and the head pose from it, the face and the wig from reference 1. "
"Camera: "
"a selfie shot with the arm extended, held far too close and LOW, from under his chin looking up at about 40 degrees, wide lens, rolled about 12 degrees to the left: "
"his head with the tall wig fills about 85 percent of the frame width (his face about 38 percent), foreshortened from below, the chin and the underside of the moustache nearest the lens, the whole wig with its side curls readable and its top close to but not past the top edge, behind and above him the painted ceiling of a gilded palace hall with soft cloud and sky paintings and a gold cornice, candlelit; "
"the lower right corner shows only the blurred hall; "
"the face is still sharp and readable, tack-sharp 4K, fine lace and wig curl detail, a clean wig outline with no loose net strands, no soft focus; "
"in the lower left and lower right corners blurred shapes of the hall: "
"at the left a grey powdered wig and a lace shoulder of a courtier, at the right an open fan and a servant's livery shoulder. "
"Pose and emotion: "
"he is squinting into the lens as if checking something, with a puzzled frown, heavy lids half-lowered, one eyebrow raised, the lips slightly parted as he mumbles 'is it on'. "
"No text, no logos, no modern objects, no glass or crystal glass anywhere, no extra fingers, no clown makeup, only one king. "
)

body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "K4_angle_low_O12.png"]}
open(H0 + "t1na_start_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t1na_start_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
