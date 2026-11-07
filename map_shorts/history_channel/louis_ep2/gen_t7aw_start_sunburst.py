"""Take 7 piece 7a-WALK START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Owner 07.11: the king WALKS through the hall, looks into the camera and speaks (no armchair); the still is a self-filmed vlog frame mid-stride. One ref only: K4_master_neutral_O8.png (face, wig, costume); the hall is described in words because R10 carries seated ladies, glasses and a chandelier (reviewer 07.11). Result: pilot_frames/anchors/t7aw_start_sunburst_4k.jpg. Run: python3 gen_t7aw_start_sunburst.py go
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
"Camera: "
"the look of a frame from a hand-held vlog that he films of himself while walking, at arm's-length distance, a spontaneous, slightly crooked, close frame, off-centre, with natural grain and candle flicker on the skin, at eye level, a wide-angle lens with visible perspective on the nose and forehead, the picture rotated about 5 degrees clockwise: "
"his face fills about 30 percent of the frame width with its centre at 48 percent of the frame width, the whole wig about 60 percent of the width and never more than 64 percent, with at least 18 percent of free gilded wall at each side and the top of the wig 8 percent of the frame height below the top edge, his head tilted about 6 degrees, the wall sconces of the hall receding in strong perspective behind him. "
"Pose and emotion: "
"he is caught in mid-stride walking toward the viewer along the great hall, his shoulders relaxed and a little swaying, both eyes open, the irises visible under the heavy upper lids, looking straight into the lens, one brow slightly raised, the lips just parted as if starting to speak, a conspiratorial faint smirk; "
"the cuff of his scarlet sleeve and the back of one relaxed hand enter at the lower right edge, the fingers relaxed and open, cut off by the frame edge. "
"Behind him, blurred: "
"the long candlelit gilded hall lit by wall sconces with the ceiling out of frame, standing courtiers in plain wigs stepping aside on both sides to leave him a path, some bowing a little, at the back right a standing lady with an open fan, a servant in livery far behind. "
"One king only, natural light rouge. Clean picture with no text or lettering, no modern objects, only gold, velvet, lace and candles of the 1680s. "
)

body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png"]}
open(H0 + "t7aw_start_sunburst_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t7aw_start_sunburst_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=500, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
