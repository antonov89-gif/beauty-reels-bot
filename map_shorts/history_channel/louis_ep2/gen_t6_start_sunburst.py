"""Take 6 (the verdict) START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Setup S13 (frontal, eye level, close; wiping the fingers, eyes down on the bones, complacent smirk). Refs in order: K4_master_neutral_O8.png, R10_hall_clean.jpg. Result: pilot_frames/anchors/t6_start_sunburst_4k.jpg. Run: python3 gen_t6_start_sunburst.py go
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
"Reference 2 gives only the gilded walls and the warm candlelight; the table, the people and the dishes are new. "
"Camera: "
"the look of a frame from a hand-held vlog that he films of himself at arm's-length distance, not a studio portrait: his face close, slightly off-centre to the left, his head tilted about 8 degrees, a wide-angle lens with visible perspective on the nose and forehead, spontaneous and a little imperfect, at eye level: "
"his face fills about 34 percent of the frame width with its centre at 47 percent of the frame width, the powdered wig puff about 50 percent of the frame width, the whole wig with its long side curls about 66 percent and never wider than 70 percent, so at least 14 percent of free gilded wall at each side, and the top of the wig sits 6 percent of the frame height below the top edge, sharp; "
"a slight roll of about 4 degrees to the left; "
"at the lower edge the lace cravat, and below it the rim of a gold plate with a few small clean bird bones, soft; the table is set only with gold plates and gold dishes, the lower left corner is empty gilded table surface; in the lower right corner the scarlet velvet sleeve of his arm enters from below, with a wide white lace cuff and the back of a relaxed hand, large and soft because it is close to the lens; the hand is cut off by the right frame edge, only the cuff, the wrist, the back of the hand and the knuckles show, about 12 percent of the frame width and 10 percent of the height; the hand rests open and relaxed and holds nothing, and it stays clear of the plate. "
"Pose and emotion: "
"his shoulders are relaxed and a little turned, his chin slightly lowered, both eyes open, the irises visible under the heavy upper lids, looking straight into the lens, one brow slightly raised, a complacent faint smirk, the lips closed. "
"Behind him, blurred: "
"the candlelit gilded hall lit by wall sconces with the ceiling out of frame, standing courtiers in plain wigs, at the back right a lady with an open fan and two courtiers whispering. "
"One king only, natural light rouge. Clean picture with no text or lettering, no modern objects, only gold plates, candles, velvet and lace of the 1680s. "
)

body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "R10_hall_clean.jpg"]}
open(H0 + "t6_start_sunburst_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t6_start_sunburst_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
