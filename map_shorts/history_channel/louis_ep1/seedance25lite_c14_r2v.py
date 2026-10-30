"""C14 on Seedance 2.5 LITE r2v, voice trial v4 (owner 30.10: "Сначала сделаем на модели для всех серии потом посмотрим"): the model voices the king from our v3 voice as reference audio and keeps its own speech and sounds (C09 r2v route, which the owner preferred). C10 passed (owner "Норм" to the voice of C09 and C10 together).
Inputs: reference image 1 = frames/C14_v7.jpg (the gallery doors, finger pointing at the lens), image 2 = the king's face master; reference audio 1 = voice/tts_ep1/C14_ref11s.wav (make_ref_audio.py C14 0.4 11, built AFTER the Lumean order). 720p, 11 s, $0.15/s = $1.65. Needs the owner's yes. Usage: python3 seedance25lite_c14_r2v.py show | go"""
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
          'Reference image 1 is the scene and the opening frame: the same vain French king in the tall grey-white powdered wig, white powdered face with pink rouge, thin upturned moustache, a scarlet velvet coat with gold suns and a white lace jabot, rings on his fingers, stands at the doors of the Hall of Mirrors with the gallery behind him and films himself, pointing at the lens. His face is exactly reference image 2. '
          'DIALOGUE: the king speaks the line of reference audio 1, in his voice from that audio, with the same words and rhythm: "Next time, I dine in public. ... You may watch... but don\'t stare. ... Well, a little. ... Subscribe, and come hungry." (mock-generous, then firm, then sly, then grand); lips clearly moving with every word, mouth closed in the pauses. '
          'ACTION: 0-3 s he adjusts a curl and glances at a page off to the side; 3-6 s he wags a ringed finger at the lens on "don\'t stare"; 6-9 s a sly half-smile, he leans in conspiratorially on "Well, a little"; 9-11 s he draws himself up and points a ringed finger at the lens on "Subscribe". '
          'Same face, wig, makeup and costume throughout. Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. '
          "Sound: recorded by the phone's own microphone: his voice close, the echo of the gallery, distant murmurs of the court, the swish of velvet. No music.")
body = {"model": "seedance-2.5-lite-r2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C14_v7.jpg", "image/jpeg"), host(FM + "face_front_talking.jpg", "image/jpeg")],
        "audio_urls": [host(H0 + "voice/tts_ep1/C14_ref11s.wav", "audio/wav")],
        "duration": 11, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c14r2v"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
