"""WaveSpeed models through 302.ai (same prices). Key in /home/claude/.k302 (never commit)."""
import json, time, urllib.request
KEY = open("/home/claude/.k302").read().strip()
BASE = "https://api.302.ai/ws/api/v3"
def call(path, body=None):
    req = urllib.request.Request(BASE + path, method="POST" if body is not None else "GET",
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    try: return json.load(urllib.request.urlopen(req, timeout=180))
    except urllib.error.HTTPError as e: return {"code": e.code, "error": e.read().decode()[:400]}
def run(model, body, out=None, timeout=900):
    r = call("/" + model, body)
    if r.get("code") != 200: return r
    pid = r["data"]["id"]; t0 = time.time()
    while time.time() - t0 < timeout:
        s = call(f"/predictions/{pid}/result"); st = (s.get("data") or {}).get("status")
        if st == "completed":
            if out:
                u = s["data"]["outputs"][0]
                for hdr in ({"User-Agent": "Mozilla/5.0"}, {"User-Agent": "Mozilla/5.0", "Authorization": "Bearer " + KEY}):
                    try:
                        open(out, "wb").write(urllib.request.urlopen(urllib.request.Request(u, headers=hdr), timeout=300).read()); break
                    except Exception as e: s["data"]["dl_err"] = str(e)
            return s["data"]
        if st == "failed": return s
        time.sleep(4)
    return {"error": "timeout", "id": pid}
