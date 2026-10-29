"""C01 part 2 v2: Wan 2.7 image-to-video DRIVEN BY OUR AUDIO (audio_url = the locked voice, C01 line), first frame = the last frame of part 1 v2.
Why: the Kling part 2 lips follow Kling's own faster speech; our drawled voice lags 0.4-0.9 s inside phrases. Wan 2.7 i2v accepts audio_url (spec).
Usage: python3 wan_part2.py go   (PAID, price NOT listed by the estimator; run only after the owner's yes; the status reports usage.cost)."""
import json, sys, urllib.request
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


prompt = ("Raw hand-held phone footage, ultra-wide lens, held by a page who stands still beside the bed: only tiny natural hand micro-shake, the camera does not move, no zoom. "
          "A vain French king in a short dark curled night wig and a gold silk dressing gown, propped on the pillows of his canopied state bed, speaks straight into the lens, his lips exactly in sync with the audio: "
          "irritated on 'Marcel, not the ceiling', taps his chest with one finger on 'Me', satisfied on 'Good', smug and drawling on 'Welcome to Versailles', chin up and delighted on 'Yes, I'm that handsome', "
          "one eyebrow up and sneering on 'Try not to faint', then a silent smirk. Keep his face, wig, moustache and gown exactly as in the first frame, natural blinking, real skin texture. No music.")
body = {"model": "wan2.7-i2v", "prompt": prompt, "image_urls": [host(H0 + "louis_ep1/frames/C01_part2_first.jpg", "image/jpeg")],
        "audio_url": host(H0 + "voice/tts_ep1/C01_drive_10s.mp3", "audio/mpeg"), "duration": 10, "resolution": "1080P", "watermark": False}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if sys.argv[1:] == ["go"]:
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/wan_part2.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10); open(H0 + "louis_ep1/frames/wan_part2.status.json", "w").write(json.dumps(res, indent=1))
    print(json.dumps(res)[:800])
    u = find(res.get("data") or {}); print("url", u)
    if u: apipod.download(u, H0 + "louis_ep1/frames/wan_part2.mp4")
