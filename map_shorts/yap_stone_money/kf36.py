"""Yap Short: 2 skit keyframes (nano-banana-2.1, $0.04 each). URLs saved as soon as each finishes."""
import apipod, json, os, sys, concurrent.futures as cf
exec(open("/home/claude/v34/kf_test2.py").read().split("P = (")[0].replace("import apipod", ""))
J = {
 "K1": ("Scene: centuries ago, at the foot of tall green-topped limestone rock islands in a turquoise lagoon (Palau). Three Micronesian sailors in simple woven wraps "
        "push a huge round grey-white stone disk with a big hole in its centre (about two metres wide) onto a bamboo raft tied behind an outrigger sailing canoe. "
        "The men strain and look worried at the size of the stone. Bright daylight, calm sea, open ocean on the horizon. Vertical 9:16, free space at the top."),
 "K2": ("Scene: today, a small simple general store on a tropical Pacific island (Yap), open door with a view of the turquoise sea and palm trees. "
        "A cheerful local man in a T-shirt stands at the wooden counter and confidently points out of the door towards the sea, while the young female cashier "
        "behind the counter raises an eyebrow and nods slowly. Outside, a giant round stone money disk with a hole in the centre leans against a palm tree. "
        "Funny comedic moment, expressive faces. Vertical 9:16, free space at the top."),
}
U = json.load(open("kf/urls.json")) if os.path.exists("kf/urls.json") else {}
def go(k):
    r = apipod.submit("images", {"model": "nano-banana-2.1", "prompt": STYLE + J[k], "aspect_ratio": "9:16", "quality": "2K"})
    if "data" not in r: return k, "submit " + str(r)[:300]
    w = apipod.wait("images", r["data"]["task_id"]); d = w.get("data") or {}
    if d.get("status") != "completed": return k, "fail " + str(w)[:300]
    u = d["result"][0]; apipod.download(u, f"kf/{k}.jpg"); U[k] = u
    json.dump(U, open("kf/urls.json", "w"), indent=1)
    return k, "ok", d.get("usage")
todo = [k for k in (sys.argv[1:] or J) if k not in U or len(sys.argv) > 1]
with cf.ThreadPoolExecutor(2) as ex:
    for r in ex.map(go, todo): print(r, flush=True)
