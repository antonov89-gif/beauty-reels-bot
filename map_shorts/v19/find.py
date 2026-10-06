import json, sys, urllib.parse, urllib.request
UA = {"User-Agent": "curl/8.5.0"}
q = sys.argv[1]
u = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "page_size": 20, "license": "cc0,pdm,by", "source": "wikimedia"})
d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
for i, r in enumerate(d["results"]):
    if (r.get("width") or 0) >= 1800:
        print(i, r["license"], r.get("width"), r.get("height"), (r.get("title") or "")[:60], "|", r["url"])
