"""Take 7 piece 7b-WALK START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, measured charge about $0.10 (preflight table pre-deduct $0.50). Owner 07.11: the king has walked through the hall and stops in its middle, looks into the camera and says "Всё, пока, я занят" (EN "That's all. Bye. I'm busy."), then points at the lens, then the lazy wave and the hard cut. The still is a self-filmed vlog frame: he has just stopped, courtiers bow on both sides. Refs in order: K4_master_neutral_O8.png (face, wig, costume) and K4_angle_low_O12.png (only the camera height and the foreshortening from below, so that 7b differs from 7a-walk and S13; the hall is described in words, R10 carries seated ladies, glasses and a chandelier). Lessons of the 7a-walk still: the model overshoots the wig width and drifts the gaze, so the geometry is hard (curls end at 20 % and 80 % of the width) and the pupils are centred on the lens. Result: pilot_frames/anchors/t7bw_start_sunburst_4k.jpg. Run: python3 gen_t7bw_start_sunburst.py go
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
"Reference 2 shows the same man from below: take only the camera height and the way the face is foreshortened from below (the underside of the chin, the nostrils) from it, the face and the wig from reference 1. "
"Camera: "
"the look of a frame from a hand-held vlog that he films of himself, at arm's-length distance, a spontaneous, slightly crooked, close frame, off-centre to the right, with natural grain and candle flicker on the skin, from low, the camera at chest height tilted up about 12 degrees so that the underside of his chin and the tall wig are seen, a wide-angle lens with visible perspective, the picture rotated about 5 degrees counter-clockwise: "
"his face fills about 29 percent of the frame width with its centre at 54 percent of the frame width, the top of the wig 10 percent of the frame height below the top edge with a visible band of empty gilded wall above it, the whole wig with its long side curls about 58 percent of the width, the left curls ending at about 21 percent of the width and the right curls at about 79 percent of the width, so that a clear band of wall and bowing courtiers shows at each side of the curls, his head tilted about 6 degrees and turned a little toward the viewer's left with both eyes and the beauty mark on the viewer's right clearly visible. "
"Pose and emotion: "
"he has just stopped in the middle of the great hall, his shoulders relaxed, a brisk businesslike look, both eyes open, the irises visible under the heavy upper lids, the pupils centred straight on the camera, one brow slightly raised, the lips just parted as if starting to say goodbye, a faint smug smirk; "
"the cuff of his scarlet sleeve and the back of one relaxed hand enter at the lower right edge, the fingers relaxed and open, cut off by the frame edge. "
"Behind him, blurred: "
"the long candlelit gilded hall lit by wall sconces with the ceiling out of frame, the standing courtiers in plain wigs on both sides bowing deeply in a double row that leaves a path behind him, at the back right a standing lady with an open fan bowing her head, a servant in livery far behind. "
"One king only, natural light rouge. A clean picture with no text, only gold, velvet, lace and candles of the 1680s, no modern objects. "
)

body = {"model": "gpt-image-2.5-sunburst", "prompt": prompt, "aspect_ratio": "9:16", "resolution": "4K", "quality": "high",
        "image_urls": [RAW + "K4_master_neutral_O8.png", RAW + "K4_angle_low_O12.png"]}
open(H0 + "t7bw_start_sunburst_prompt.txt", "w").write(prompt)
if len(sys.argv) > 1 and sys.argv[1] == "go":
    r = apipod.submit("images", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted")
    out = H0 + "pilot_frames/anchors/t7bw_start_sunburst_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=500, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    def find(x):
        if isinstance(x, str) and x.startswith("http"): return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u: return u
    d = res.get("data") or {}; u = find(d); print("status", d.get("status"), "usage", d.get("usage"), d.get("error_code"))
    if u: apipod.download(u, out); print("saved")
