"""C01 part 2, Seedance 2.0 reference-to-video TEST at 720p (owner said yes 29.10, about $1.26 for 10 s): lips driven by OUR audio (audio_urls = the locked voice, C01 line).
Image refs: [0] the last frame of part 1 v2 (wanted as the opening frame), [1] the C01 storyboard frame (identity). The generated audio is muted in the edit; only the lip timing matters.
Usage: python3 seedance_part2.py go (PAID)."""
import json, re, sys, urllib.request
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


prompt = ("Vertical hand-held phone video, ultra-wide lens. The video opens EXACTLY on reference image 1 (same framing, same man, same bed, same room) and keeps that framing: "
          "the phone is held still by a page, only tiny natural hand micro-shake, no camera movement, no zoom, no cut. "
          "The man (a vain French king in a short dark curled night wig and a gold silk dressing gown, propped on pillows in a canopied state bed; face and costume as in reference images 1 and 2) "
          "speaks straight into the lens and his lips are perfectly synchronized, word for word, with the reference audio, which starts at 0.15 s: "
          "\"Marcel, not the ceiling. Me. Good. Welcome to Versailles. Yes, I'm that handsome. Try not to faint.\" "
          "Irritated on the first words, taps his chest with one finger on \"Me\", satisfied on \"Good\", smug and drawling on the welcome, chin up on \"handsome\", one eyebrow up on \"faint\", "
          "then a silent smirk to the end. Natural blinking, real skin texture, photorealistic. Use the reference audio as his voice; no music.")
body = {"model": "seedance-2.0-r2v", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C01_part2_first.jpg", "image/jpeg"), host(H0 + "louis_ep1/frames/C01.jpg", "image/jpeg")],
        "audio_urls": [host(H0 + "voice/tts_ep1/C01_drive_10s.mp3", "audio/mpeg")],
        "duration": 10, "resolution": "720p", "aspect_ratio": "adaptive", "generate_audio": True}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if sys.argv[1:] == ["go"]:
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/seedance_part2.task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10); open(H0 + "louis_ep1/frames/seedance_part2.status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))  # signed URLs carry a provider credential: never commit them
    print(json.dumps(res)[:800])
    u = find(res.get("data") or {}); print("url", u)
    if u: apipod.download(u, H0 + "louis_ep1/frames/seedance_part2.mp4")
