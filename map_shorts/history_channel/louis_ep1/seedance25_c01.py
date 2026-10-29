"""Seedance 2.5 DRAFT route (owner 29.10: "take Seedance 2.5, first a draft test"). Stage 1: 480p draft (low cost); stage 2: python3 seedance25_c01.py final <draft_task_id> renders the 1080p final from the approved draft.
C01 as ONE continuous 12-s generation (owner 29.10: no visible splice; he films himself; he speaks only after the phone points at him).
Seedance 2.0 r2v, our voice as audio_urls with a 2.7-s silent lead (drive audio = silence + voice/tts_ep1/C01.mp3 padded to 12 s).
Image refs: [0] ceiling frame (C01_ceiling2.jpg, wanted as the opening), [1] the C01 frame (landing/identity).
Usage: python3 seedance25_c01.py draft | final <draft_task_id>   (PAID; run only after the owner's yes; draft estimate about $1.18 for 12 s = 3 x the 4-s estimator $0.392, final 1080p price NOT VERIFIED).
Signed result URLs carry a provider credential: they are stripped before anything is saved."""
import json, re, subprocess, sys, urllib.request
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


drive = H0 + "voice/tts_ep1/C01_drive_12s.mp3"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-t", "2.7", "-i", "anullsrc=r=44100:cl=mono", "-i", H0 + "voice/tts_ep1/C01.mp3",
                "-filter_complex", "[1:a]aresample=44100,aformat=channel_layouts=mono[v];[0:a][v]concat=n=2:v=0:a=1,apad=whole_dur=12[a]", "-map", "[a]", "-c:a", "libmp3lame", "-b:a", "192k", drive], check=True)
prompt = ("One continuous hand-held phone selfie video, ultra-wide front camera, ONE take, no cut. A vain French king in a short dark curled night wig and a gold silk dressing gown, propped on the pillows of his canopied state bed, holds the phone himself (his arm is in the frame). "
          "The video OPENS exactly on reference image 1: the phone points straight up at the painted gilded ceiling, small natural hand shake, a white plume at the edge of the lens, nobody speaks for the first 1.5 seconds. "
          "Then his own hand turns the phone down onto himself in ONE continuous tilt: the camera only ROTATES, it does not fly or zoom toward the bed; motion blur, a hint of rolling-shutter wobble, the exposure drops from the bright ceiling to the warm bed, the focus hunts and locks on his face, a small overshoot and settle, until the framing matches reference image 2. "
          "ONLY after the phone is pointed at him, from about 2.7 seconds, he speaks straight into the lens, his lips exactly in sync with the reference audio: \"Oops, the ceiling. There. Welcome to Versailles. Yes, I'm that handsome. Try not to faint.\" "
          "Startled and annoyed on 'Oops, the ceiling', satisfied on 'There', smug and drawling on the welcome, chin up on 'handsome', one eyebrow up and sneering on 'faint', then a silent smirk. Real skin texture, natural blinking, photorealistic. No music.")
body = {"model": "seedance-2.5-draft", "prompt": prompt,
        "image_urls": [host(H0 + "louis_ep1/frames/C01_ceiling2.jpg", "image/jpeg"), host(H0 + "louis_ep1/frames/C01.jpg", "image/jpeg")],
        "audio_urls": [host(drive, "audio/mpeg")], "duration": 12, "aspect_ratio": "adaptive", "generate_audio": True}
mode = sys.argv[1] if len(sys.argv) > 1 else "show"
if mode == "final":
    body = {"model": "seedance-2.5-draft", "draft_task_id": sys.argv[2], "resolution": "1080p"}
print(json.dumps({k: (v if k != "prompt" else v[:70] + "...") for k, v in body.items()}, indent=1)[:900])
if mode in ("draft", "final"):
    tag = "seedance25_" + mode
    r = apipod.submit("videos", body); print(r)
    tid = r["data"]["task_id"]; open(H0 + "louis_ep1/frames/" + tag + ".task_id", "w").write(tid)
    res = apipod.wait("videos", tid, timeout=1800, every=10)
    open(H0 + "louis_ep1/frames/" + tag + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
    u = find(res.get("data") or {}); print("usage", (res.get("data") or {}).get("usage"))
    if u: apipod.download(u, H0 + "louis_ep1/frames/" + tag + ".mp4")
