"""Search Mixkit free stock video (Mixkit Stock Video Free License): python3 mixkit.py search "q" | get id"""
import re, sys, json, os, urllib.request, urllib.parse
UA = {"User-Agent": "Mozilla/5.0"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode("utf8", "ignore")
def search(q, pages=1):
    out = []
    for p in range(1, pages + 1):
        u = "https://mixkit.co/free-stock-video/discover/" + urllib.parse.quote(q.replace(" ", "-")) + "/" + (f"?page={p}" if p > 1 else "")
        try: h = get(u)
        except Exception as e: print("err", e); break
        for m in re.finditer(r'videos/(\d+)/\d+-thumb-360-0\.jpg" class="item-grid-video-player__thumb" alt="([^"]*)"', h):
            out.append((int(m.group(1)), m.group(2)))
    return out
if __name__ == "__main__":
    if sys.argv[1] == "search":
        for q in sys.argv[2:]:
            r = search(q)
            print(f"## {q} ({len(r)})")
            for i, t in r[:30]: print(i, t)
    elif sys.argv[1] == "get":
        os.makedirs("raw", exist_ok=True)
        for i in sys.argv[2:]:
            for res in ("1080", "720"):
                u = f"https://assets.mixkit.co/videos/{i}/{i}-{res}.mp4"
                try:
                    urllib.request.urlretrieve(u, f"raw/{i}.mp4"); print(i, res); break
                except Exception as e: pass
