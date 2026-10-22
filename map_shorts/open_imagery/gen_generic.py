"""Open imagery for every key of a satNN module: python3 gen_generic.py sat63 satO63 [KEY...]   (run in /home/claude/v62)"""
import importlib, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
mod = importlib.import_module(sys.argv[1])
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
HI = {}
env = dict(os.environ, GDAL_HTTP_CAINFO="/root/.ccr/ca-bundle.crt", GDAL_HTTP_TIMEOUT="60", GDAL_HTTP_MAX_RETRY="3")
def run(k):
    p = f"{out}/{k}.jpg"
    if os.path.exists(p):
        return k
    lon, lat, d = mod.SP[k]
    w, h = mod.size(k) if hasattr(mod, "size") else (mod.W_IMG, mod.H_IMG)
    r = subprocess.run(["python3", "/home/claude/v62/open_imagery.py", str(lon), str(lat), str(d), str(w), str(h), p], env=env, capture_output=True, text=True)
    open(f"{out}/{k}.log", "w").write(r.stdout + r.stderr)
    return k
keys = sys.argv[3:] or list(mod.SP)
with ThreadPoolExecutor(3) as ex:
    print(list(ex.map(run, keys)))
