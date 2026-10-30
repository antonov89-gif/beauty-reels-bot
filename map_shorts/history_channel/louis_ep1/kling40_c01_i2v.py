"""C01 v3 TEST on Kling 4.0 i2v (owner 30.10: "C01 v3, давай это будет тест, посчитай клинг 4.0 и сиденс 2.0"), voice trial v4 (owner 30.10: "Сначала сделаем на модели для всех серии потом посмотрим"): the model voices the king from our v3 voice as reference audio and keeps its own speech and sounds (C09 r2v route, which the owner preferred). C10 passed (owner "Норм" to the voice of C09 and C10 together).
Inputs: @first_frame = frames/C01_ceiling2.jpg (EXACT first frame: the painted ceiling, his wig edge at the bottom), @keyframe_1 = frames/C01_part2_first_v4.jpg (him in bed after the phone turns), 13 s, 1080p: $0.2175/s = $2.83 (charged 0.6525 for 3 s on 29.10; 720p is $0.145/s = $1.89). Kling speaks with ITS OWN voice and its own timing from the quoted line (no audio input in i2v; the r2v 'voices' field rejected our voice 3 times on 29.10), so this tests picture, camera and lips, not our voice. Needs the owner's yes. Usage: python3 kling40_c01_i2v.py show | go"""
import json, re, subprocess, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}


def host(path, ctype):  # public URL via the media presign of our publishing account
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
FM = H0 + "louis_card/face_master_v3/"
prompt = (CAMERA_BASE +
          '@first_frame: the phone is pointed up at a painted, gilded baroque ceiling with the edge of a gold bed canopy; at the very bottom edge of the frame the top of his small curled dark wig is just visible. @keyframe_1: the same vain French king, white powdered face with a little rouge, thin upturned moustache, a small curled dark wig, a gold embroidered silk dressing gown over a white lace shirt, sitting in his gilded bed in the state bedchamber, filming himself. '
          'He speaks with a French accent, haughty and amused, with real pauses: "Oops, the ceiling." (startled, annoyed, while the camera still looks at the ceiling) ... "There." (satisfied) ... "Bonjour. I am Louis, King of France." (grand and formal) ... "They call me the Sun King." (proud, drawling) ... "Yes... I\'m that handsome." (delighted, self-admiring). Lips clearly moving with every word, mouth closed in the pauses. '
          'ACTION: 0-2.5 s the camera looks up at the painted ceiling, shaky, his voice off screen; 2.5-4 s he tilts the phone down onto himself in one clumsy hand move, the ceiling slides out of the top of the frame and his face appears in bed; 4-9 s he looks into the lens and introduces himself, formal and proud, a ringed hand lifts a little on "Sun King"; 9-13 s a smug pause, then the delighted line and a small self-satisfied smirk. '
          'Same face, wig, makeup and costume throughout. Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. '
          "Sound: recorded by the phone's own microphone: his voice close, rustle of silk and bed linen, the knock of the phone, a quiet palace room with faint murmurs. No music.")
body = {"model": "kling-4.0-i2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C01_ceiling2.jpg", "image/jpeg")],
        "keyframe_urls": [host(H0 + "louis_ep1/frames/C01_part2_first_v4.jpg", "image/jpeg")],
        "duration": 13, "resolution": "1080p"}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "kling40_c01i2v"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
