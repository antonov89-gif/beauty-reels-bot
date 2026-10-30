"""C12 on Seedance 2.5 LITE r2v, voice trial v4 (owner 30.10: "Сначала сделаем на модели для всех серии потом посмотрим"): the model voices the king from our v3 voice as reference audio and keeps its own speech and sounds (C09 r2v route, which the owner preferred). C10 passed (owner "Норм" to the voice of C09 and C10 together).
Inputs: reference image 1 = frames/C12_v7a.jpg (Hall of Mirrors, scarlet velvet coat with gold suns, ringed hand on the chest, courtiers in SIMPLE wigs: owner 29.10 "звезда тут один"), image 2 = the king's face master; reference audio 1 = voice/tts_ep1/C12_ref9s.wav (make_ref_audio.py C12 0.4 9: the line at natural pace 0.4-7.5 s). 720p, 9 s, $0.15/s = $1.35. Needs the owner's yes. Usage: python3 seedance25lite_c12_r2v.py show | go"""
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
          "Reference image 1 is the scene and the opening frame: the same vain French king in the tall grey-white powdered wig, white powdered face with pink rouge, thin upturned moustache, a scarlet velvet coat embroidered with gold suns, white lace jabot and lace cuffs, rings on his fingers, films himself while WALKING down the Hall of Mirrors at Versailles: tall arched mirrors on one side, tall windows on the other, crystal chandeliers, gilded ceiling. His face is exactly reference image 2. Courtiers in simple plain wigs follow him at a respectful distance; he is the only one with the tall wig. "
          "DIALOGUE: the king speaks the line of reference audio 1, in his voice from that audio, with the same words and rhythm: \"Venice sold us mirrors. Now we have three hundred and fifty-seven of our own, and I'm in every single one.\" Lips clearly moving with every word, mouth closed in the pauses. "
          "ACTION: 0-3 s he walks towards the lens, grand and showy, the phone bobbing with each step; 3-6 s he sweeps his ringed hand at the row of mirrors without looking at them; 6-8.5 s he glances sideways at his own reflection in a mirror, delighted, and laughs softly, then looks back at the lens. "
          "Same face, wig, makeup and costume throughout. "
          "Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. "
          "Sound: recorded by the phone's own microphone: his voice close, footsteps and the swish of velvet on parquet, the echo of a long hall, courtiers' quiet steps and murmurs. No music.")
body = {"model": "seedance-2.5-lite-r2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C12_v7a.jpg", "image/jpeg"), host(FM + "face_front_talking.jpg", "image/jpeg")],
        "audio_urls": [host(H0 + "voice/tts_ep1/C12_ref9s.wav", "audio/wav")],
        "duration": 9, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c12r2v"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
