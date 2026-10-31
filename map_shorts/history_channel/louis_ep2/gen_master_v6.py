"""Ep.2 set master v6: EDIT OF v4, face only: eye colour + powder (owner 31.10 option 2, $0.12). v4: HAUGHTY face from the owner's C08 frame (owner 31.10 'Лицо не надменное, плохое качество'; yes to $0.12). Earlier: v3 FACE FIX (owner 31.10 'Это ужас, переделай и проверь': v1/v2 faces were older, heavier, one eye droopy). Refs: face master first (owner 31.10: bigger wig, same face). Nano Banana Pro 4K 9:16 (about $0.12). PAID: runs after the owner's 'Сделай'.
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
prompt = ("Edit the FIRST reference image. Keep EVERYTHING exactly the same: the composition, the pose, the wig, the coat, the table, the crowd, the light, the haughty heavy-lidded expression, the moustache, the beauty spot, the wrinkles and pores. "
          "Change ONLY two things on the face. (1) The colour of both irises: muted grey-green (hazel-grey with a green tint, like the eyes in the SECOND reference image), not brown and not blue; keep the eyelids and the gaze unchanged. "
          "(2) The face powder: make the whole face, forehead, nose, cheeks and chin covered by a THICK matte white-grey court powder, pale and chalky like the SECOND reference image, clearly paler and less pink than now, with only a faint pink on the cheekbones; the neck and hands stay as they are. "
          "Photorealistic, same grain and sharpness, no smoothing, no text.")
refs = [host_file("louis_ep2/frames/master_table_v4_1440.jpg"), host_file("louis_ep2/frames/owner_C08_panel.jpg")]
r = apipod.submit("images", {"model": "nano-banana-pro", "prompt": prompt, "aspect_ratio": "9:16", "quality": "4K", "image_urls": refs})
if "data" not in r: print("SUBMIT FAILED", r); sys.exit(1)
tid = r["data"]["task_id"]; out = "louis_ep2/frames/master_table_v6_4k.jpg"; open(out + ".task_id", "w").write(tid)
res = apipod.wait("images", tid, timeout=600, every=5)
open(out + ".status.json", "w").write(re.sub(r'(https://[^"?]+)\?[^"]*', r'\1?[signed query removed]', json.dumps(res, indent=1)))
u = find(res.get("data") or {})
if u: apipod.download(u, out)
print("cost", (res.get("data") or {}).get("usage", {}).get("cost"), "saved" if u else "NO URL")
