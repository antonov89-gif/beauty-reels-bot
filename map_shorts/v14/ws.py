import json, os, sys, time, urllib.request
KEY = open("/home/claude/v14/.wavespeed_key").read().strip()
BASE = "https://api.wavespeed.ai/api/v3"
def call(path, body=None, method=None):
    req = urllib.request.Request(BASE + path, method=method or ("POST" if body is not None else "GET"),
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e:
        return {"code": e.code, "error": e.read().decode()[:500]}
def run(model, body, out=None, timeout=600):
    r = call("/" + model, body)
    if r.get("code") != 200: return r
    pid = r["data"]["id"]; t0 = time.time()
    while time.time() - t0 < timeout:
        s = call(f"/predictions/{pid}/result")
        st = s["data"]["status"]
        if st == "completed":
            urls = s["data"]["outputs"]
            if out:
                for i, u in enumerate(urls):
                    p = out if len(urls) == 1 else out.replace(".", f"_{i}.")
                    urllib.request.urlretrieve(u, p)
            return s["data"]
        if st == "failed": return s
        time.sleep(3)
    return {"error": "timeout", "id": pid}
def balance(): return call("/balance")["data"]["balance"]
if __name__ == "__main__":
    print(balance())
