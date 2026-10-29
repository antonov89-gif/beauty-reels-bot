"""Test clip C01 on kling-4.0-r2v (APIpod): character element from our frames + the locked voice as a reference (`voices`).
Usage: python3 kling_test.py estimate   (free price estimate, nothing is generated)
       python3 kling_test.py go         (PAID: one 8-s clip at 720p; run only after the owner's explicit yes)
Hosting of the reference files on Zernio media as in the other scripts. Task id and status are saved before waiting."""
import json
import sys
import urllib.request

sys.path.insert(0, "/home/claude/v51")
import apipod

H0 = "/home/user/beauty-reels-bot/map_shorts/history_channel/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip()
H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}


def host(path, ctype):
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": path.split("/")[-1], "contentType": ctype}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": ctype}), timeout=120)
    return d["publicUrl"]


mode = sys.argv[1] if len(sys.argv) > 1 else "estimate"
imgs = [host(H0 + "louis_card/A3_white_wig.jpg", "image/jpeg"), host(H0 + "louis_card/D2_morning.jpg", "image/jpeg"), host(H0 + "louis_ep1/frames/C01.jpg", "image/jpeg")]
voice = host(H0 + "voice/heir_sample.mp3", "audio/mpeg")
prompt = ("Raw documentary phone-vlog look, handheld ultra-wide front camera. @king (a vain 17th-century French king in a gold silk dressing gown and a short dark curled night wig, propped in a canopied state bed) "
          "starts on the painted ceiling, the phone tilts down to his face, a feather plume brushes the lens. He looks into the lens with a smug smirk and says in @king_voice, in a haughty, drawling, arrogant tone: "
          "\"Marcel, down! Bow. Lower. Good. Welcome to Versailles. Yes, I am that handsome. Try not to faint.\" Natural lip sync, room tone and candle flicker, no music.")
body = {"model": "kling-4.0-r2v", "prompt": prompt, "image_urls": [imgs[2]],
        "kling_elements": [{"name": "king", "element_input_urls": imgs, "tag": "character", "description": "vain French king, smug smirk, rouged cheeks, beauty patch, thin curled moustache"}],
        "voices": [{"name": "king_voice", "audio_url": voice}], "duration": 8, "resolution": "720p", "aspect_ratio": "9:16"}
print(json.dumps({k: (v if k != "prompt" else v[:80] + "...") for k, v in body.items()}, indent=1)[:1500])
if mode == "estimate":
    e = apipod._req("POST", "/v1/pricing/estimate", {"model_id": body["model"], "duration": body["duration"], "resolution": body["resolution"]})
    print("estimate", json.dumps(e)[:300], "(the estimator returned $0.714 for the 5-s default = 5 x $0.1428; 8 s = about $1.14)")
else:
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open("frames/kling_test_C01.mp4.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1500, every=10); open("frames/kling_test_C01.mp4.status.json", "w").write(json.dumps(res, indent=1)); print(json.dumps(res)[:600])

    def find(x):
        if isinstance(x, str) and x.startswith("http"):
            return x
        for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
            u = find(v)
            if u:
                return u
    u = find(res.get("data") or {}); print("url", u); apipod.download(u, "frames/kling_test_C01.mp4")
