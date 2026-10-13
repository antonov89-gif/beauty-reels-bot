import os, subprocess, urllib.request, concurrent.futures as cf
from catalog import PX, MK
os.makedirs("raw", exist_ok=True); os.makedirs("clips", exist_ok=True)
def norm(src, key):
    out = f"clips/{key}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-t", "14", "-an", "-vf",
                    "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p",
                    "-c:v", "libx264", "-crf", "19", "-preset", "fast", out], check=True)
    os.remove(src)
def get(item):
    key, url = item
    if os.path.exists(f"clips/{key}.mp4"): return key, "cached"
    raw = f"raw/{key}.mp4"
    for _ in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0"})
            with urllib.request.urlopen(req, timeout=300) as r, open(raw, "wb") as f:
                while True:
                    b = r.read(1 << 20)
                    if not b: break
                    f.write(b)
            norm(raw, key); return key, "ok"
        except Exception as e:
            err = str(e)
    return key, "FAIL " + err
items = [(k, f"https://www.pexels.com/download/video/{i}/") for k, (i, _) in PX.items()] + \
        [(k, f"https://assets.mixkit.co/videos/{i}/{i}-720.mp4") for k, i in MK.items()]
with cf.ThreadPoolExecutor(6) as ex:
    for k, s in ex.map(get, items):
        if s != "ok": print(k, s, flush=True)
print("done", len(os.listdir("clips")))
