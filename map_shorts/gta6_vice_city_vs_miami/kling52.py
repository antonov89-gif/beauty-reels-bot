import apipod, json, sys, concurrent.futures as cf
exec(open("gen52.py").read().split("os.makedirs")[0])
st = json.load(open("ai/state.json"))
def go(k):
    body = {"model": "kling-3.0-i2v", "prompt": "Animate this exact frame, keep composition, style and every object. " + A[k] + SUFFIX,
            "image_urls": [st[k]["img"]], "duration": 5, "resolution": "1080p", "aspect_ratio": "16:9", "generate_audio": True}
    r = apipod.submit("videos", body)
    if "data" not in r: return k, "submit " + str(r)[:300]
    w = apipod.wait("videos", r["data"]["task_id"], timeout=1800, every=10); d = w.get("data") or {}
    if d.get("status") != "completed": return k, "fail " + str(w)[:300]
    u = d["result"][0]; u = u if isinstance(u, str) else u.get("url")
    apipod.download(u, f"ai/{k}_kling.mp4"); return k, "ok"
with cf.ThreadPoolExecutor(4) as ex:
    for k, m in ex.map(go, sys.argv[1:]): print(k, m)
