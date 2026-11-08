"""Take 1 NEW OPENER (owner 07.11): MIDDLE still = the LAST frame of piece 1a and the FIRST frame of piece 1b: the king has walked farther along the hall toward the long table where people sit and do things, he has pulled the camera back to arm's length, sees himself and is pleased ("Ah. There I am. Bonjour."). gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). One ref only: K4_master_neutral_O8.png (face, wig, costume); the hall is described in words (the old hall refs carry glasses and a chandelier). Per briefs/brief_t1_walk.md: end of 1a = face about 38 % in the brief (here 34 % because the wig is twice the face width and the margins must hold), head 12 degrees toward the viewer's left, the table 45 % of the width, no glasses; NO hand visible (the camera arm is out of the frame, the king's gesture hand appears only in the clips, lessons of 7b: count arms). Result: pilot_frames/anchors/t1wm_mid_sunburst_4k.jpg. Run: python3 gen_t1wm_mid_sunburst.py go
BRIEF: briefs/brief_t1_walk.md
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
"Reference 2 is a frame of the same vlog and gives only the light, the dark muted colour grade, the cool grey-silver tone of the wig and the look of the panelled hall with grey wig stands; the hand, the pose and the framing of reference 2 are not used. "
"Camera: "
"the look of a frame from a hand-held vlog that he films of himself while walking, at close range, about one metre, a spontaneous, slightly crooked, close frame, off-centre, with natural grain and candle flicker on the skin, at eye level, a wide-angle lens with visible perspective on the nose and forehead, the picture rotated about 4 degrees clockwise: "
"the camera pulled back so that his face fills about 31 percent of the frame width with its centre at 47 percent of the frame width, the whole wig about 56 percent of the width and never more than 60 percent, with at least 18 percent of free space at the left edge and 22 percent at the right edge, the long side curls hanging in front of his shoulders inside the frame, the top of the wig 8 percent of the frame height below the top edge, his head turned about 12 degrees toward the viewer's left and tilted about 5 degrees toward his left shoulder with both eyes and the beauty mark on the viewer's right clearly visible. "
"Pose and emotion: "
"he is caught mid-stride walking along the great hall, both eyes open, the irises visible under the heavy upper lids, looking straight into the lens with both eyes equally open, one brow slightly raised, the lips closed in a pleased smug half smile as if he has just seen himself and approves, his shoulders relaxed; both arms are down out of the frame, the frame shows only his head, wig, shoulders, scarlet coat and lace cravat. "
"Behind him, blurred: "
"the long candlelit hall with panelled walls in the dark muted grade of reference 2, lit by wall sconces with the ceiling out of frame; a long banquet table fills the right edge and runs behind his shoulder with people seated along it doing small natural things: a man in dark clothes eating, two ladies in gold and green gowns whispering to each other, a lady in a pale blue gown with an open fan, a servant in livery serving a dish; on the left a row of wooden wig stands with powdered wigs beside standing courtiers in plain wigs and a few ladies in silk gowns at the gilded wall. "
"One king only, natural light rouge. A clean picture with no text, only gold, velvet, lace and candles of the 1680s, no modern objects. "
)

body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "t1w_start_4k.jpg"]}
open(H0 + "t1wm_mid_sunburst_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t1wm_mid_sunburst_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=500, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
