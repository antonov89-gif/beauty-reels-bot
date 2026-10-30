"""C15 on Seedance 2.5 LITE r2v, voice trial v4 (owner 30.10: "Сначала сделаем на модели для всех серии потом посмотрим"): the model voices the king from our v3 voice as reference audio and keeps its own speech and sounds (C09 r2v route, which the owner preferred). C10 passed (owner "Норм" to the voice of C09 and C10 together).
Inputs: reference image 1 = frames/C15_v7.jpg (the gilded mirror covers the lower right, banquet table behind), image 2 = the king's face master; reference audio 1 = voice/tts_ep1/C15_ref6s.wav (make_ref_audio.py C15 0.3 6, built AFTER the Lumean order). 720p, 6 s, $0.15/s = $0.90. Needs the owner's yes. Usage: python3 seedance25lite_c15_r2v.py show | go"""
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
          'Reference image 1 is the scene and the opening frame: the same vain French king in the tall grey-white powdered wig, white powdered face with pink rouge, thin upturned moustache, a scarlet velvet coat with gold suns and a white lace jabot, holds a gilded hand mirror that covers the lower right of the frame; behind him a long banquet table with marzipan towers and candles. His face is exactly reference image 2. '
          'DIALOGUE: the king speaks the line of reference audio 1, in his voice from that audio, with the same words and rhythm: "Now, if you\'ll excuse me... ... the soup is getting cold." then a cold, haughty laugh; lips clearly moving with every word, mouth closed in the pauses. '
          'ACTION: 0-2.5 s he lifts his chin, polite and lofty, the phone sways; 2.5-4.5 s he turns towards the banquet table and says the last words with a gleeful hungry look; 4.5-6 s a cold haughty laugh, chin up, and the gilded mirror swings across the lens as he walks to the table. '
          'Same face, wig, makeup and costume throughout. Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. '
          "Sound: recorded by the phone's own microphone: his voice close, cutlery and murmurs from the banquet, candles, the swish of velvet. No music.")
body = {"model": "seedance-2.5-lite-r2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C15_v7.jpg", "image/jpeg"), host(FM + "face_front_talking.jpg", "image/jpeg")],
        "audio_urls": [host(H0 + "voice/tts_ep1/C15_ref6s.wav", "audio/wav")],
        "duration": 6, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c15r2v"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
