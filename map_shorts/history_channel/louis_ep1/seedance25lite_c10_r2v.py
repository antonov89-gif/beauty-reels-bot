"""C10 on Seedance 2.5 LITE r2v, voice trial v4 (owner 30.10: "Сначала сделаем на модели для всех серии потом посмотрим"): the model voices the king from our v3 voice as reference audio and keeps its own speech and sounds (C09 r2v route, which the owner preferred). First clip after C09: also the test whether the model voice stays the same from clip to clip.
Inputs: reference image 1 = frames/C10_v7.jpg (seated in the gilded armchair, one leg raised to the lens: black shoe with a RED HEEL only, sole dark leather), image 2 = the king's face master; reference audio 1 = voice/tts_ep1/C10_ref8s.wav (make_ref_audio.py C10 0.5 8: the whole line at natural pace from 0.5 s). r2v images are references, not an exact first frame (C09 -> C10 is a hard cut). 720p, 8 s, $0.15/s = $1.20 (C09 r2v actual charge 30.10). Needs the owner's yes. Usage: python3 seedance25lite_c10_r2v.py show | go"""
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
          "Reference image 1 is the scene and the opening frame: the same vain French king in the tall grey-white powdered wig, white powdered face with pink rouge, thin upturned moustache, gold embroidered silk dressing gown and white lace jabot, sits in a gilded armchair in the state bedchamber and films himself; he has lifted one leg so his black buckled shoe is right in front of the lens: the HEEL is red, the sole is dark leather (only the heel is red). His face is exactly reference image 2. Courtiers in plain wigs stand in the background. "
          "DIALOGUE: the king speaks the line of reference audio 1, in his voice from that audio, with the same words and rhythm: \"Red heels. Nobles only, and only the ones I like. Mine are the tallest, of course.\" Lips clearly moving with every word, mouth closed in the pauses. "
          "ACTION: 0-2 s he wiggles the shoe at the lens, flirtatious and teasing, the phone sways; 2-5 s he lowers the leg a little and smirks at the lens, the red heel still in frame; 5-7.5 s he taps the tall heel with a ringed finger, proud, then looks back at the lens, smug. "
          "Same face, wig, makeup and costume throughout. "
          "Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. "
          "Sound: recorded by the phone's own microphone: his voice close, the creak of the armchair, rustle of silk, the knock of a heel, a quiet palace room with faint murmurs. No music.")
body = {"model": "seedance-2.5-lite-r2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C10_v7.jpg", "image/jpeg"), host(FM + "face_front_talking.jpg", "image/jpeg")],
        "audio_urls": [host(H0 + "voice/tts_ep1/C10_ref8s.wav", "audio/wav")],
        "duration": 8, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c10r2v"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
