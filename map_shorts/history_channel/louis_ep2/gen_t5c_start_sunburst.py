"""Take 5 piece 5c START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Setup S12 (from above, leaning back, eyes closed in a long happy sigh, hands on the belly). Refs in order: K4_master_neutral_O8.png, K4_angle_high_O13.png. Result: pilot_frames/anchors/t5c_start_sunburst_4k.jpg. Run: python3 gen_t5c_start_sunburst.py go
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
"Reference 2 shows the same man from above: "
"take ONLY the camera height and the way the face is foreshortened from above (large forehead, short chin) from it, the face and the wig from reference 1; the head pose and the eyes are NOT taken from reference 2: his head rests straight back against the chair, centred and facing the camera, the chin up, the eyes closed. "
"Camera: "
"a camera held at arm's length IN FRONT of him and HIGH above his face, looking DOWN at him from about 55 degrees above as he leans back in a gilded armchair (a clearly high angle), rolled about 14 degrees to the right; "
"his face fills about 35 percent of the frame width with its centre at 50 percent, the whole tall wig about 66 percent of the width with at least 15 percent free space on each side, the chin and the lace cravat in the lower middle, sharp. "
"Pose and emotion: "
"he has just leaned back into the carved gilded armchair, the head resting against its back, the eyes closed under heavy lids in a long happy sigh, the lips parted a little, a deeply contented face; "
"both hands rest on his belly over the scarlet coat, visible along the bottom edge of the frame, five natural fingers each, the fingers loosely overlapping. "
"Around the edges of the frame: "
"the carved gilded armchair and the candlelit gilded hall blurred, lit by wall sconces with the ceiling out of frame, and on the right and right-centre blurred figures far below: "
"a servant in livery, a courtier's powdered wig and shoulder, and a lady with a fan. "
"One king only, natural light rouge. The table and the armchair hold only plates, gold dishes, silver platters, napkins and candle holders. Clean picture with no text or lettering, no modern objects, only things of the 1680s. "
)

body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "K4_angle_high_O13.png"]}
open(H0 + "t5c_start_sunburst_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t5c_start_sunburst_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
