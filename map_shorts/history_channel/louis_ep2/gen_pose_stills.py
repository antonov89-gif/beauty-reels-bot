"""Pose stills for the T2a test (owner 05.11 "Да давай"): two EDITS of the A3 edit keyframe, same camera/background/head size, only the pose and expression change. GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, image_urls = [T1_keyframe_edit_768.jpg]. 2 calls x about $0.12 = $0.24, no retries."""
import json, re, sys, threading
sys.path.insert(0, "/home/claude/v51")
import apipod
RAW = "https://raw.githubusercontent.com/antonov89-gif/beauty-reels-bot/claude/funny-bardeen-uj4fiv/map_shorts/history_channel/louis_ep2/pilot_frames/"
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_ep2/pilot_frames/"
BASE = ("Edit the photo: keep EXACTLY the same camera position, the same framing, the same head size and the same head position in the frame, the same hall and background (the long dining table, the candelabra, the ladies on stools, the standing courtiers, the windows, the painted ceiling) and the same lighting. "
        "Keep the man's face, age, skin, eyes, moustache, beauty mark, tall white-grey wig and scarlet velvet coat with gold suns and lace EXACTLY as they are (do not redraw his face). Change ONLY his pose and expression as described. Real phone-selfie photo, fine film grain, real skin texture. "
        "No text, no logos, no modern objects, no extra fingers, no blond or cream wig, no clown makeup. ")
POSES = {
 "P1_frown": BASE + "New pose and expression: the hand with the rings is lowered out of the frame (not touching the wig), his head turned slightly to his left, his eyes looking sideways toward the courtiers behind the table, brows pulled together in a haughty annoyed frown, lips pressed.",
 "P2_pleased": BASE + "New pose and expression: his head tilted a little to his right, a pleased smug closed-mouth smile with heavy eyelids, the ringed hand stretched out toward the table at the lower right of the frame as if presenting the food.",
}
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
def run(k):
    body = {"model": "gpt-image-2.5-sunburst-lite", "prompt": POSES[k], "aspect_ratio": "9:16", "resolution": "4K", "quality": "high", "image_urls": [RAW + "T1_keyframe_edit_768.jpg"]}
    r = apipod.submit("images", body); tid = (r.get("data") or {}).get("task_id")
    if not tid: print(k, "NOT SUBMITTED", json.dumps(r)[:300]); return
    out = H0 + f"anchors/POSE_{k}_4k.jpg"; open(out + ".task_id", "w").write(tid)
    res = apipod.wait("images", tid, timeout=900, every=5)
    open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    d = res.get("data") or {}; u = find(d)
    if u: apipod.download(u, out)
    print(k, d.get("status"), "cost", (d.get("usage") or {}).get("cost"), "saved" if u else "NO URL")
import sys as _s
for k in (_s.argv[1:] or list(POSES)):
    run(k)   # one after the other (retry of the 05.11 SUBMISSION_UNCERTAIN failures, owner 'Да')
