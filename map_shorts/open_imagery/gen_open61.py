import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from sat61 import SP
HI = {"PRC": "naip", "PRR": "naip", "OYA": "ign", "KOU": "ign", "VEL": "pnoa", "VEC": "pnoa", "LLI": "pnoa,ign", "LLR": "ign,pnoa", "ANG": "naip", "ANR": "naip"}
env = dict(os.environ, GDAL_HTTP_CAINFO="/root/.ccr/ca-bundle.crt")
def run(k):
    out = f"satO/{k}.jpg"
    if os.path.exists(out) and True:
        return k
    lon, lat, d = SP[k]
    args = [str(lon), str(lat), str(d), "1620", "2880", out]
    if k in HI:
        r = subprocess.run(["python3", "/home/claude/v62/hires.py"] + args + [HI[k]], env=env, capture_output=True, text=True)
    else:
        r = subprocess.run(["python3", "/home/claude/v62/open_imagery.py"] + args, env=env, capture_output=True, text=True)
    open(f"satO/{k}.log", "w").write(r.stdout + r.stderr)
    return k
keys = sys.argv[1:] or list(SP)
with ThreadPoolExecutor(3) as ex:
    print(list(ex.map(run, keys)))
