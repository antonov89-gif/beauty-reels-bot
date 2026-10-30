"""C09 on Seedance 2.5 LITE i2v (720p, 8 s, $0.15/s = $1.20 by the APIpod pricing page): the hat-drop set piece, the peak of the episode (like the reference's dropped tray). First frame = frames/C09_v9.jpg (v2, owner 30.10 "Шляпа уже лежит": in v8 the hat already lay on the floor, so nothing could fall on camera; now the floor is empty and the courtier next to Marcel holds his plumed hat in his lowered hand during the bow; the hat slips out of his fingers on camera) (earlier: C09_v8.jpg, Marcel from his card in the bowing row) (hard cut after the dressing burst, so approximate first frame is fine). Line (13 words, one real pause): "Lower. Lower... [beat] and there goes the hat. [pause] Eyes on me, not on the hat." A courtier cries "Pardon, Sire!" (replaced by the chosen page voice in the edit). Needs the owner's yes. Usage: python3 seedance25lite_c09.py show | go"""
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
          "Continue from this exact frame: the same vain French king in the tall grey-white powdered wig, white powdered face with pink rouge, gold embroidered silk dressing gown and white lace jabot, in the gilded state bedchamber; the first frame is badly framed on purpose: half of his face is cut off by the left edge of the frame and he does not notice. Behind him a row of courtiers in simple plain grey wigs bows deeply; in the middle of the row stands the slim young page in the sky-blue coat with silver braid, a small white wig and a black ribbon, who watches in alarm; the courtier next to him bows the deepest and holds his black plumed hat loosely in his lowered hand. At the start NOTHING lies on the parquet floor. "
          "0-2 s: he keeps talking to the courtiers, scornful, the phone sways in his hand, the framing does not improve: \"Lower. Lower...\" "
          "1.5-3 s: the black plumed hat slips out of the deepest-bowing courtier's fingers, drops onto the parquet and rolls away across the floor (the drop is clearly visible); he glances back over his shoulder, the phone swings with his turn so the bowing row and the rolling hat are fully visible for a moment; the young page in the sky-blue coat cries \"Pardon, Sire!\" and hurries after the hat, the other courtiers stay bowed; he says dryly: \"and there goes the hat.\" "
          "5-8 s: a real pause of about one second, then he turns back and yanks the phone to the centre, too close, with a wobble, his face large and haughty, looks down his nose at the lens and says: \"Eyes on me, not on the hat.\" "
          "Lips clearly moving with every word. Same face, wig, makeup and costume as the first frame. "
          "Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. "
          "Sound: recorded by the phone's own microphone: his voice close, rustle of coats and the knock of the phone, a plumed hat dropping on parquet and rolling, quick footsteps, a quiet palace room with faint murmurs. No music.")
body = {"model": "seedance-2.5-lite-i2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C09_v9.jpg", "image/jpeg")],
        "duration": 8, "resolution": "720p", "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c09v9"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
