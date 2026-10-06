"""python3 fetchx.py key "query" "title substring" -> exact pick"""
import json, os, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "curl/8.5.0"}
def get(u, t=90): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t)
key, q, sub = sys.argv[1:4]
u = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "page_size": 20, "license": "cc0,pdm,by", "source": "wikimedia"})
r = next(r for r in json.load(get(u))["results"] if sub.lower() in (r.get("title") or "").lower())
src = r["url"].split("?")[0]
cands = [src]
if "/wikipedia/commons/" in src and "/thumb/" not in src:
    p = src.split("/wikipedia/commons/")[1]
    cands.append(src.replace("/wikipedia/commons/", "/wikipedia/commons/thumb/") + "/2560px-" + p.split("/")[-1])
data = None
for c in cands:
    for w in (2800, 2200):
        try:
            data = get("https://images.weserv.nl/?" + urllib.parse.urlencode({"url": c.replace("https://", ""), "w": w, "output": "jpg", "q": 92})).read()
            break
        except Exception as e:
            print("retry", e); time.sleep(1)
    if data:
        break
open(f"img/{key}.jpg", "wb").write(data)
cr = json.load(open("credits.json")); cr[key] = {k: r.get(k) for k in ("title", "creator", "license", "license_version", "foreign_landing_url")}
json.dump(cr, open("credits.json", "w"), indent=1)
print(key, r["license"], r["width"], r["height"], r["title"][:70])
