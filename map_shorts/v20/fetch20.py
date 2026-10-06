"""Auto-pick landscape CC0/PD/CC BY photos from Wikimedia (via Openverse) and download through images.weserv.nl.
python3 fetch20.py key "query" [skip_n]  -> img/<key>.jpg + credits.json entry"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "curl/8.5.0"}


def get(u, t=90):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t)


key, q = sys.argv[1], sys.argv[2]
skip = int(sys.argv[3]) if len(sys.argv) > 3 else 0
u = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
    {"q": q, "page_size": 20, "license": "cc0,pdm,by", "source": "wikimedia"})
res = json.load(get(u))["results"]
cands = [r for r in res if (r.get("width") or 0) >= 2000 and (r.get("height") or 1) and
         1.25 <= (r["width"] / r["height"]) <= 2.4 and not r["url"].lower().endswith((".svg", ".tif", ".tiff", ".pdf"))]
cands = cands[skip:]
os.makedirs("img", exist_ok=True)
cr = json.load(open("credits.json")) if os.path.exists("credits.json") else {}
for r in cands:
    try:
        data = get("https://images.weserv.nl/?" + urllib.parse.urlencode(
            {"url": r["url"].split("?")[0].replace("https://", ""), "w": 2800, "output": "jpg", "q": 92})).read()
    except Exception as e:
        print("retry", e)
        time.sleep(1.5)
        continue
    open(f"img/{key}.jpg", "wb").write(data)
    cr[key] = {k: r.get(k) for k in ("title", "creator", "license", "license_version", "foreign_landing_url")}
    json.dump(cr, open("credits.json", "w"), indent=1)
    print(key, r["license"], r["width"], r["height"], (r.get("title") or "")[:70])
    break
else:
    print("NONE", key)
