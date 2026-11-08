"""Take 1 piece 1b END still (08.11): the king is SEATED at the long table, last frame of 1b and the match for the first frame of TAKE1_piece3_alive.mp4. gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Refs: K4_master_neutral_O8.png (face, wig, costume) and t1wm_mid_sunburst_4k.jpg (light, grade, hall, only; the owner accepted it as is 08.11). The piece 3 first frame is only 720x1280 (a video frame), so it is NOT a reference: its pose is written in words. Per briefs/brief_t1_walk.md PINS 1b END: seated low angle, face about 40 % of the width centre-left (brief says 45 %, lowered so that the wig stays inside), head tilted about 10 degrees toward the viewer's left, closed smug smirk, heavy lids with the eyes OPEN on the lens, the ringed right hand at the chin with the lace cuff (one hand only, the camera arm is outside the frame), seated ladies behind right, standing men in black behind left, a gold candlestick at the right edge, plates and candles on the cloth, NO glass, NO cup. Result: pilot_frames/anchors/t1we_seated_sunburst_4k.jpg. Run: python3 gen_t1we_seated_sunburst.py go
BRIEF: briefs/brief_t1_walk.md
"""
import json, re, sys
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/"
prompt = ("Vertical 9:16 real photograph in dim candlelight, slightly underexposed, fine film grain, real unretouched natural skin texture. "
"Reference 1 (the king's master portrait) is his face and costume: "
"exactly the same man of about 45, same heavy-lidded light grey-hazel eyes, thin dark waxed moustache with curled tips, a small dark beauty mark clearly visible on the viewer's right of the mouth, light rouge, the tall powdered wig in silver-grey and white, the scarlet velvet coat with gold suns, lace cravat; "
"take only the face, wig and costume from it. "
"Reference 2 is a frame of the same vlog; take from it only the light, the dark muted colour grade, the cool grey-silver tone of the wig and the look of the hall. Compose the new picture freshly. "
"Camera: "
"the look of a frame from a hand-held vlog that he films of himself while seated at a table, at arm's length, a spontaneous, slightly crooked, close frame from a low seated angle, off-centre to the left, with natural grain and candle flicker on the skin, a wide-angle lens with visible perspective on the nose and forehead, the picture rotated about 3 degrees counter-clockwise: "
"his face fills about 40 percent of the frame width with its centre at 44 percent of the frame width, the top of the wig 9 percent of the frame height below the top edge, the whole wig with its long side curls inside the frame, his head tilted about 10 degrees toward the viewer's left with both eyes and the beauty mark on the viewer's right clearly visible. "
"Pose and emotion: "
"he has just sat down at the long table and is about to speak, the lips closed in a smug satisfied smirk, the heavy upper lids lowered but both eyes open, the irises visible, looking straight into the lens, one brow slightly raised; "
"his one ringed hand (a single hand with four gold rings) rests at his chin with the lace cuff of the scarlet sleeve, five natural fingers, and no other hand is visible anywhere in the frame; the lower-left corner shows only a scarlet sleeve without a hand. "
"Behind him, blurred: "
"the long candlelit panelled hall in the dark muted grade of reference 2; at the table behind his right shoulder two ladies in gold and blue silk gowns seated together, one covering a smile with an open fan; behind his left shoulder standing men in black coats along the panelled wall; at the right edge a tall gold candlestick with a lit candle; on the white tablecloth only plates of food and candles. "
"One king only, natural light rouge. A clean picture with no text, only gold, velvet, lace and candles of the 1680s, no modern objects. "
)

body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "refs/K4_master_neutral_O8.png", RAW + "pilot_frames/anchors/t1wm_mid_sunburst_4k.jpg"]}
open(H0 + "t1we_seated_sunburst_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t1we_seated_sunburst_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=500, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
