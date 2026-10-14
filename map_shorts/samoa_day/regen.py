import apipod, json, time, concurrent.futures as cf
exec(open("kf_all.py").read().split("def run")[0])
U = json.load(open("kf/urls.json"))
def gen(k):
    p, ref = K[k]
    body = {"model": "nano-banana-2.1", "prompt": STYLE + p, "aspect_ratio": "9:16", "quality": "2K"}
    if ref: body["image_urls"] = [U["S5"]]
    r = apipod.submit("images", body)
    if "data" not in r: return k, None, str(r)[:200]
    w = apipod.wait("images", r["data"]["task_id"]); d = w.get("data", {})
    if d.get("status") != "completed": return k, None, str(d)[:200]
    apipod.download(d["result"][0], f"kf_v2/{k}.jpg"); return k, d.get("usage"), d["result"][0]
with cf.ThreadPoolExecutor(4) as ex:
    for k, c, u in ex.map(gen, ["S2", "S3", "S4", "S6"]):
        print(k, c, u, flush=True)
        if c: U[k] = u; json.dump(U, open("kf/urls.json", "w"), indent=1)
