"""Take 7 piece 7a START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Setup S16 (in front and slightly right below eye level, wide, hall on the right; leaned back, chin raised, eyes up-right at the hall). Refs in order: K4_master_neutral_O8.png, K4_angle_34right_O11.png, R10_hall_clean.jpg. Result: pilot_frames/anchors/t7a_start_sunburst_4k.jpg. Run: python3 gen_t7a_start_sunburst.py go
BRIEF: briefs/brief_t5_t7.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/refs/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real unretouched natural skin texture. "
"Reference 1 (the king's master portrait) is his face and costume: "
"exactly the same man of about 45, same heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white (its colour reads a little warmer or cooler with the light), the scarlet velvet coat with gold suns, lace cravat; "
"take only the face, wig and costume from it. "
"Reference 2 shows the same man turned to the right side of the image, the beauty mark stays on the right of the image: "
"take the head turn from it, the face and the wig from reference 1. "
"Reference 3 gives only the gilded walls and the warm candlelight of the hall; the table, the people and the dishes are new. "
"Camera: "
"the look of a frame from a hand-held vlog that he films of himself at arm's-length distance, not a studio portrait, held a little BELOW his eye level, a wide-angle lens with visible perspective, spontaneous and a little imperfect, so that the hall can be seen: "
"the camera is in front of him and a little to his right, his head with the whole wig fills about 58 percent of the frame width with at least 14 percent free wall at the left (his face about 28 percent) with its centre at 42 percent, the top of the wig 8 percent of the frame height below the top edge, the head turned about 30 degrees toward the viewer's right and tilted about 6 degrees with the beauty mark still visible; "
"to the right of him a wide view of the candlelit gilded hall with standing courtiers in plain wigs and a few ladies in wide gowns at the side, at the back right a lady with an open fan, a servant in livery far behind, the gilded wall above; "
"the hall is lit by wall sconces; "
"rolled about 5 degrees to the right. "
"Pose and emotion: "
"he has leaned back in the armchair, his chin raised, thoughtful, his heavy-lidded eyes looking up and away to the right at the hall as if searching for an idea, the lips closed and pursed a little; "
"the cuff of his scarlet sleeve and the back of one relaxed hand rest on the chair arm at the lower right edge, cut off by the frame edge, holding nothing. "
"One king only, natural light rouge. Clean picture with no text or lettering, no modern objects, only gold, velvet, lace and candles of the 1680s. "
)

body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "K4_angle_34right_O11.png", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t7a_start_sunburst_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t7a_start_sunburst_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
