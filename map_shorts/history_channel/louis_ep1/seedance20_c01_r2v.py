"""C01 v3 TEST on Seedance 2.0 r2v (owner 30.10: "C01 v3, давай это будет тест, посчитай клинг 4.0 и сиденс 2.0"), voice trial v4 (owner 30.10: "Сначала сделаем на модели для всех серии потом посмотрим"): the model voices the king from our v3 voice as reference audio and keeps its own speech and sounds (C09 r2v route, which the owner preferred). C10 passed (owner "Норм" to the voice of C09 and C10 together).
Inputs: reference image 1 = frames/C01_ceiling2.jpg (the painted gilded ceiling with the canopy edge, his head at the bottom edge: the opening), image 2 = frames/C01_part2_first_v4.jpg (him in bed, small curled wig, gold gown: the look after the phone is turned), image 3 = the king's face master; reference audio 1 = voice/tts_ep1/C01_ref13s.wav (make_ref_audio.py C01 0.3 13, built AFTER the Lumean order of the v3 line). Replaces the old C01 (draft route, about $11 spent, not used). 720p, 13 s, $0.126/s = $1.64 (charged $1.26 for 10 s on 29.10); 1080p would be $0.315/s = $4.10. Needs the owner's yes. Usage: python3 seedance20_c01_r2v.py show | go"""
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
          'Reference image 1 is the opening frame: the phone is pointed up at a painted, gilded baroque ceiling with the edge of a gold bed canopy; at the very bottom edge of the frame the top of his small curled wig is just visible. Reference image 2 is the look of the scene once the phone turns: the same vain French king, white powdered face with a little rouge, thin upturned moustache, a small curled dark wig, a gold embroidered silk dressing gown over a white lace shirt, sitting in his gilded bed in the state bedchamber, filming himself. His face is exactly reference image 3. '
          'DIALOGUE: the king speaks the line of reference audio 1, in his voice from that audio, with the same words and rhythm: "Oops, the ceiling. ... There. ... Bonjour. I am Louis, King of France. ... They call me the Sun King. ... Yes... I\'m that handsome." (startled and annoyed, then satisfied, then grand and formal, then proud, then delighted); lips clearly moving with every word, mouth closed in the pauses. '
          'ACTION: 0-2.5 s the camera looks up at the painted ceiling, shaky, his voice says the first words off screen; 2.5-4 s he tilts the phone down onto himself in one clumsy hand move, the ceiling slides out of the top of the frame and his face appears in bed, he settles the framing and says "There."; 4-9 s he looks into the lens and introduces himself, formal and proud, a ringed hand lifts a little on "Sun King"; 9-13 s a smug pause, then the delighted admiring line, a small self-satisfied smirk. '
          'Same face, wig, makeup and costume throughout. Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. '
          "Sound: recorded by the phone's own microphone: his voice close, rustle of silk and bed linen, the knock of the phone, a quiet palace room with faint murmurs. No music.")
body = {"model": "seedance-2.0-r2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C01_ceiling2.jpg", "image/jpeg"), host(H0 + "louis_ep1/frames/C01_part2_first_v4.jpg", "image/jpeg"), host(FM + "face_front_talking.jpg", "image/jpeg")],
        "audio_urls": [host(H0 + "voice/tts_ep1/C01_ref13s.wav", "audio/wav")],
        "duration": 13, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance20_c01r2v"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
