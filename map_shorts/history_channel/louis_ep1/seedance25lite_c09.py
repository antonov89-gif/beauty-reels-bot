"""C09 on Seedance 2.5 LITE i2v (720p, 8 s, $0.15/s = $1.20 by the APIpod pricing page): the hat-drop set piece, the peak of the episode (like the reference's dropped tray). First frame = frames/C09_first.jpg (hard cut after the dressing burst, so approximate first frame is fine). Line (13 words, one real pause): "Lower. Lower... [beat] and there goes the hat. [pause] Eyes on me, not on the hat." A courtier cries "Pardon, Sire!" (replaced by the chosen page voice in the edit). Needs the owner's yes. Usage: python3 seedance25lite_c09.py show | go"""
import json, re, subprocess, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}


def host(path, ctype):
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": path.split("/")[-1], "contentType": ctype}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": ctype}), timeout=120)
    return d["publicUrl"]


def find(x):
    if isinstance(x, str) and x.startswith("http"):
        return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u:
            return u


CAMERA_BASE = ("Filmed by himself on a phone held in one hand at arm's length, and he is clumsy with it: constant natural hand-held sway and small roll, the framing keeps drifting, his face slides off-centre and he re-centres it with small jerks, at moments the phone comes too close, the horizon tilts and is corrected. "
               "Never a smooth gimbal move, never a zoom, never a dolly or flying camera: every move comes from his arm and body, the phone always within arm's reach. ")
prompt = (CAMERA_BASE +
          "Continue from this exact frame: the same vain French king in the tall grey-white powdered wig, white powdered face with pink rouge, gold embroidered silk dressing gown and white lace jabot, in the gilded state bedchamber; the first frame is badly framed on purpose: half of his face is cut off by the left edge of the frame and he does not notice. Behind him a row of courtiers in simple plain wigs bows deeply, and a plumed hat lies on the parquet floor. "
          "0-2 s: he keeps talking to the courtiers, scornful, the phone sways in his hand, the framing does not improve: \"Lower. Lower...\" "
          "2-5 s: a short silent beat, then one plumed hat tumbles off a bowing courtier's head and rolls across the floor; he glances back over his shoulder, the phone swings with his turn so the bowing row and the rolling hat are fully visible for a moment; a courtier cries \"Pardon, Sire!\" and hurries after the hat; he says dryly: \"and there goes the hat.\" "
          "5-8 s: a real pause of about one second, then he turns back and yanks the phone to the centre, too close, with a wobble, his face large and haughty, looks down his nose at the lens and says: \"Eyes on me, not on the hat.\" "
          "Lips clearly moving with every word. Same face, wig, makeup and costume as the first frame. "
          "Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. "
          "Sound: recorded by the phone's own microphone: his voice close, rustle of coats and the knock of the phone, a plumed hat dropping on parquet and rolling, quick footsteps, a quiet palace room with faint murmurs. No music.")
body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C09_first.jpg", "image/jpeg")],
        "duration": 8, "resolution": "720p", "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c09"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
