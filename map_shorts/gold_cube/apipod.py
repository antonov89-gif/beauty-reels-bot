"""APIPod helper. The key is read from the APIPOD_KEY environment variable only; it is never written to disk."""
import os, json, time, urllib.request, urllib.error
BASE = "https://api.apipod.ai"
def _req(method, path, body=None):
    key = os.environ["APIPOD_KEY"]
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json", "Accept": "application/json", "User-Agent": "curl/8.5.0"})
    try:
        return json.load(urllib.request.urlopen(r, timeout=120))
    except urllib.error.HTTPError as e:
        return {"http_error": e.code, "body": e.read().decode()[:600]}
def submit(kind, body):
    r = _req("POST", f"/v1/{kind}/generations", body)
    return r
def wait(kind, task_id, timeout=900, every=6):
    t0 = time.time()
    while time.time() - t0 < timeout:
        r = _req("GET", f"/v1/{kind}/status/{task_id}")
        d = r.get("data") or {}
        if d.get("status") in ("completed", "failed", "cancelled"): return r
        time.sleep(every)
    return {"timeout": True}
def download(url, out):
    for hdr in ({"User-Agent": "curl/8.5.0"},):
        open(out, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=300).read())
