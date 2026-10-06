"""Download the chosen CC BY / public-domain photos (Openverse metadata, images.weserv.nl proxy) -> img/, credits.json"""
import json
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "curl/8.5.0"}


def get(u, t=90):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t)


PICK = {  # key: (openverse query, title substring)
    "lambo": ("Lamborghini Aventador", "Orange Lamborghini Aventador LP700"),
    "jet": ("Gulfstream G650", "EGLF - Gulfstream G650"),
    "yacht": ("superyacht", "Kismet superyacht"),
    "ship": ("Icon of the Seas", "Thrill Island Icon of the Seas"),
    "sphere": ("Sphere Las Vegas", "Sphere - Las Vegas (53685825749)"),
    "carrier": ("USS Gerald R. Ford", "USS Gerald R. Ford in Oslo closeup 3"),
    "money": ("banknotes dollars", "Money Cash"),
}
import os
credits = json.load(open("credits.json")) if os.path.exists("credits.json") else {}
for key, (q, sub) in PICK.items():
    if os.path.exists(f"img/{key}.jpg"):
        continue
    u = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": q, "page_size": 20, "license": "cc0,pdm,by", "source": "wikimedia"})
    res = json.load(get(u))["results"]
    cands = [r for r in res if sub in (r.get("title") or "")] + [r for r in res if (r.get("width") or 0) >= 1800]
    data = None
    for r in cands:
        for w in (2600, 2000):
            try:
                data = get("https://images.weserv.nl/?" + urllib.parse.urlencode(
                    {"url": r["url"].split("?")[0].replace("https://", ""), "w": w, "output": "jpg"})).read()
                break
            except Exception as e:
                print("retry", key, e)
                time.sleep(2)
        if data:
            break
    open(f"img/{key}.jpg", "wb").write(data)
    json.dump(credits, open("credits.json", "w"), indent=1)
    credits[key] = {k: r.get(k) for k in ("title", "creator", "license", "license_version", "foreign_landing_url")}
    print(key, r["license"], r.get("creator"), len(data))
    time.sleep(0.5)
lu = ("upload.wikimedia.org/wikipedia/commons/b/b6/"
      "Leonardo_da_Vinci%2C_Salvator_Mundi%2C_c.1500%2C_oil_on_walnut%2C_45.4_%C3%97_65.6_cm.jpg")
data = get("https://images.weserv.nl/?url=" + lu + "&w=2600&output=jpg").read()
open("img/painting.jpg", "wb").write(data)
credits["painting"] = {"title": "Salvator Mundi (c. 1500), Leonardo da Vinci", "creator": "Leonardo da Vinci",
                       "license": "public domain",
                       "foreign_landing_url": "https://commons.wikimedia.org/wiki/File:Leonardo_da_Vinci,_Salvator_Mundi,"
                                              "_c.1500,_oil_on_walnut,_45.4_%C3%97_65.6_cm.jpg"}
print("painting", len(data))
json.dump(credits, open("credits.json", "w"), indent=1)
