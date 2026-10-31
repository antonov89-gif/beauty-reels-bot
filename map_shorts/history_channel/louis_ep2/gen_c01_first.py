"""Ep.2 C01 FIRST FRAME like the Vlog 2 first frame (owner 31.10 'Первый кадр должен так', yes to Nano Banana Pro 2K $0.09). Earlier: v3 FACE FIX (owner 31.10 'Это ужас, переделай и проверь': v1/v2 faces were older, heavier, one eye droopy). Refs: face master first (owner 31.10: bigger wig, same face). Nano Banana Pro 4K 9:16 (about $0.12). PAID: runs after the owner's 'Сделай'.
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
prompt = ("Vertical 9:16 phone selfie photo, the first frame of a video: the phone is held FAR TOO CLOSE to his face by a clumsy hand, ultra-wide front-camera distortion, soft focus, photorealistic, a real photograph with fine film grain, matte skin with visible pores and fine lines, no smoothing, no beauty filter. No text, no interface, no buttons, no modern objects. "
          "Composition like the SECOND reference image (only its framing: extreme close-up, the face tilted about 20 degrees and off-centre to the right, the nose and lips filling the frame, one eye at the lower right edge, the top half of the picture covered by a dark out-of-focus mass); ignore the phone interface and icons in that image. "
          "The man is the king from the FIRST reference image: the same face, the same light grey eyes, the same upturned waxed moustache, the same beauty spot beside the mouth, the same HAUGHTY look (heavy eyelids), now with his mouth slightly open mid-word. "
          "The dark mass covering the upper half is HIS OWN scarlet velvet sleeve with gold embroidery and his fist, out of focus and very close to the lens, as if he is still fumbling with the phone. A little of the tall grey-white wig curls is visible at the left edge. "
          "At the bottom a white lace cravat. Behind him a blurred gilded room with warm candle glints. Warm candlelight, shallow depth of field.")
refs = [host_file("louis_ep2/frames/master_table_v4_1440.jpg"), host_file("louis_ep2/frames/owner_vlog2_first_crop.jpg")]
r = apipod.submit("images", {"model": "nano-banana-pro", "prompt": prompt, "aspect_ratio": "9:16", "quality": "2K", "image_urls": refs})
if "data" not in r: print("SUBMIT FAILED", r); sys.exit(1)
tid = r["data"]["task_id"]; out = "louis_ep2/frames/C01_first_2k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=600, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
u = find(res.get("data") or {})
if u: apipod.download(u, out)
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")
