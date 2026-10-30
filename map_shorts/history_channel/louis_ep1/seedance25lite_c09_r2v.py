"""C09 on Seedance 2.5 LITE r2v WITH OUR VOICE AS INPUT (owner 30.10: "Можно ли сразу в генерацию засунуть нашу озвучку"): the king's lips are generated to our locked line instead of being fitted afterwards.
Inputs: reference image 1 = frames/C09_v9.jpg (the scene: empty floor, the hat in a bowing courtier's hand), image 2 = the king's face master, image 3 = Marcel's card; reference audio 1 = voice/tts_ep1/C09_ref8s.wav (take A at natural speed on an 8-s timeline, make_c09_ref_audio.py).
r2v treats the images as references, not as an exact first frame: fine here (hard cut after the dressing burst). Lip sync to a given audio is NOT documented by APIpod for this route: this is the test. 720p, 8 s, price = the Lite rate $0.15/s = $1.20 (APIpod estimate 30.10 $0.60 per 4 s, same as Lite i2v; the charge with audio input NOT VERIFIED). Needs the owner's yes. Usage: python3 seedance25lite_c09_r2v.py show | go"""
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
          "Reference image 1 is the scene and the opening frame: the same vain French king in the tall grey-white powdered wig, white powdered face with pink rouge, gold embroidered silk dressing gown and white lace jabot, in the gilded state bedchamber; the framing is bad on purpose: half of his face is cut off by the left edge of the frame and he does not notice. His face is exactly reference image 2. Behind him a row of courtiers in simple plain grey wigs bows deeply; in the middle of the row stands the slim young page in the sky-blue coat with silver braid, a small white wig and a black ribbon (his face is reference image 3), who watches in alarm; the courtier next to him bows the deepest and holds his black plumed hat loosely in his lowered hand. At the start NOTHING lies on the parquet floor. "
          "DIALOGUE: the king speaks exactly the words of reference audio 1, in its exact timing, with precise lip sync on every word, and says nothing else: \"Lower!\" at 0.25 s, \"Lower!\" at 1.15 s, \"And there goes the hat.\" at 2.95 s, \"Eyes on me, not on the hat.\" at 5.7 s; his mouth is closed in the pauses. "
          "ACTION: 0-1.8 s he scorns the bowing courtiers, the phone sways in his hand, the framing does not improve. 1.8-2.9 s the black plumed hat slips out of the deepest-bowing courtier's fingers, drops onto the parquet and rolls away across the floor (the drop clearly visible); the young page opens his mouth in alarm and hurries after the hat; the king glances back over his shoulder, the phone swings with his turn so the bowing row and the rolling hat are fully visible. 2.95-4.1 s he says his line dryly, looking back. 4.1-5.6 s a real pause: he turns back and yanks the phone to the centre, too close, with a wobble, his face large and haughty. 5.7-7.2 s he looks down his nose at the lens and says his last line. "
          "Same face, wig, makeup and costume throughout. "
          "Picture: natural window daylight, slightly underexposed like a real phone video, real skin texture with pores, no beauty filter, not golden everywhere. "
          "Sound: recorded by the phone's own microphone: rustle of coats and the knock of the phone, a plumed hat dropping on parquet and rolling, quick footsteps, a quiet palace room with faint murmurs. No music.")
body = {"model": "seedance-2.5-lite-r2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C09_v9.jpg", "image/jpeg"), host(FM + "face_front_talking.jpg", "image/jpeg"), host(H0 + "marcel_card/marcel_front.jpg", "image/jpeg")],
        "audio_urls": [host(H0 + "voice/tts_ep1/C09_ref8s.wav", "audio/wav")],
        "duration": 8, "resolution": "720p", "aspect_ratio": "9:16", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode == "go":
    tag = "seedance25lite_c09r2v"
    r = apipod.submit("videos", body); print(r)
    tid = (r.get("data") or {}).get("task_id")
    if not tid: sys.exit("not submitted: " + json.dumps(r)[:400])
    open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("status", (res.get("data") or {}).get("status"), "usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
