"""Test clip C01 on kling-4.0-r2v (APIpod): character element from our frames + the locked voice as a reference (`voices`).
Usage: python3 kling_test.py estimate   (free price estimate, nothing is generated)
       python3 kling_test.py go         (PAID: one 12-s clip at 1080p; run only after the owner's explicit yes)
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
# C01 = night wig and dressing gown: character refs only from night-wig images (no white wig here)
imgs = [host(H0 + "louis_card/D2_morning.jpg", "image/jpeg"), host(H0 + "louis_ep1/frames/C01.jpg", "image/jpeg"), host(H0 + "louis_ep1/frames/C02.jpg", "image/jpeg"), host(H0 + "louis_ep1/frames/C03.jpg", "image/jpeg")]
voice = host(H0 + "voice/heir_fr_sample.mp3", "audio/mpeg")
prompt = ("Raw documentary phone-vlog look, hand-held ultra-wide phone camera. @king (a vain 17th-century French king in a gold silk dressing gown and a short dark curled night wig, propped in a canopied state bed) "
          "Shot on a phone held by a page. 0-1.3 s: the phone points straight up at the painted gilded ceiling, small natural hand-held shake and slight roll, the tip of a hat plume drifts across the lower edge of the lens, nobody speaks. 1.3-2.5 s: one continuous downward tilt, no cut: motion blur, slight rolling-shutter wobble, exposure darkens from the bright ceiling to the warm bed, autofocus hunts then locks on his face, a small overshoot and settle; he is already glaring into the lens. Only from 2.5 s does he speak. 2.5-12 s: framed from slightly below in the bed, the hand-held shake calms to micro-movements. He looks into the lens with a smug smirk and says in @king_voice, in a haughty, drawling, arrogant tone: "
          "\"Marcel, not the ceiling. Me. Good. Welcome to Versailles. Yes, I'm that handsome. Try not to faint.\" Natural lip sync, room tone and candle flicker, no music.")
start = host(H0 + "louis_ep1/frames/C01_ceiling.jpg", "image/jpeg")  # first frame = the ceiling (owner 29.10); generate it first (2K still, about $0.04)
body = {"model": "kling-4.0-r2v", "prompt": prompt, "image_urls": [start],
        "kling_elements": [{"name": "king", "element_input_urls": imgs, "tag": "character", "description": "vain French king, smug smirk, rouged cheeks, beauty patch, thin curled moustache"}],
        "voices": [{"name": "king_voice", "audio_url": voice}], "duration": 12, "resolution": "1080p", "aspect_ratio": "9:16"}
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
