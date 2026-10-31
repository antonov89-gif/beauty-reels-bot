"""Ep.2 set master v2: ONLY the wig changes (owner 31.10: bigger wig, same face). Nano Banana Pro 4K 9:16 (about $0.12). PAID: runs after the owner's 'Сделай'.
Refs: master_table_4k.jpg (scene, face, coat: keep), tall_wig_ref.jpg (the wig). Output louis_ep2/frames/master_table_v2_4k.jpg (+ .task_id, .status.json)."""
import json, re, sys, urllib.request
sys.path.insert(0, "/home/claude/v51")
import apipod
FM = "/home/user/beauty-reels-bot/map_shorts/history_channel/louis_card/face_master_v3/"
K = open("/home/user/beauty-reels-bot/.zernio_key").read().strip(); H = {"Authorization": "Bearer " + K, "Content-Type": "application/json"}
FACE = "a man of about 35 with a pale complexion, light grey-hazel eyes, a long straight nose, a narrow face, a thin upturned waxed moustache, arched brows and a small dark beauty spot beside the mouth"
def host(path):
    n = path.split("/")[-1]
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": n, "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
    return d["publicUrl"]
def find(x):
    if isinstance(x, str) and x.startswith("http"): return x
    for v in (x.values() if isinstance(x, dict) else x if isinstance(x, list) else []):
        u = find(v)
        if u: return u
def host_file(path):
    n = path.split("/")[-1]
    d = json.load(urllib.request.urlopen(urllib.request.Request("https://zernio.com/api/v1/media/presign", data=json.dumps({"filename": n, "contentType": "image/jpeg"}).encode(), headers=H, method="POST"), timeout=60))
    urllib.request.urlopen(urllib.request.Request(d["uploadUrl"], data=open(path, "rb").read(), method="PUT", headers={"Content-Type": "image/jpeg"}), timeout=120)
    return d["publicUrl"]
prompt = ("Edit the FIRST reference image: keep EVERYTHING exactly the same (the same man, face, expression, skin, moustache, makeup and rouge, the scarlet coat with gold suns, the lace cravat, the pose, the camera angle, the table, candles, crowd, ladies, ceiling, windows and light). "
          "Change ONLY the wig: replace it with the tall powdered grey-white wig from the SECOND reference image: a towering swept-up front about as tall as his face above the forehead, deep S-shaped waves, rolled curls above the ears, and long wavy curls falling over both shoulders down to the chest. "
          "Do not change the face or the age. Photorealistic, same grain and lighting. No text.")
refs = [host_file("louis_ep2/frames/master_table_1440.jpg"), host_file(FM + "tall_wig_ref.jpg")]
r = apipod.submit("images", {"model": "nano-banana-pro", "prompt": prompt, "aspect_ratio": "9:16", "quality": "4K", "image_urls": refs})
if "data" not in r: print("SUBMIT FAILED", r); sys.exit(1)
tid = r["data"]["task_id"]; out = "louis_ep2/frames/master_table_v2_4k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=600, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
u = find(res.get("data") or {})
if u: apipod.download(u, out)
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")
