"""Open-imagery tile cache for the Hormuz video: builds tiles/esri/{z}/{x}_{y}.jpg (the engine's cache name) from
NASA GIBS Blue Marble + Copernicus Sentinel-2 L2A. Fine 0.5-deg cells (25 m/px) for z>=11, 1-deg cells (100 m/px) for z=10, GIBS BM for z<=9."""
import json, math, os, sys
import numpy as np
from PIL import Image
sys.path.insert(0, "/home/claude/v62")
import open_imagery as O
os.environ.setdefault("GDAL_HTTP_CAINFO", "/root/.ccr/ca-bundle.crt")
os.makedirs("cells", exist_ok=True)
WREF = json.load(open("water_ref.json")) if os.path.exists("water_ref.json") else None


def cell(args):
    kind, cx, cy = args
    step = 0.5 if kind == "f" else 1.0
    mpp = 25 if kind == "f" else 100
    out = f"cells/{kind}_{cx}_{cy}.png"
    if os.path.exists(out):
        return out
    l0, b0 = cx * step, cy * step
    b = (l0, b0, l0 + step, b0 + step)
    lat = b0 + step / 2
    w = int(step * 111320 * math.cos(math.radians(lat)) / mpp)
    h = int(step * 111320 / mpp)
    base = O.gibs_image(b, w, h, "BlueMarble_ShadedRelief_Bathymetry")
    s2, filled, used = O.s2_mosaic(b, w, h, lat, max_scenes=14, water_ref=WREF)
    arr = np.asarray(base).copy()
    if filled.mean() > 0.01:
        arr[filled] = np.asarray(s2)[filled]
    Image.fromarray(arr).save(out)
    O.fix_sea(out) if False else None
    return out + f" {filled.mean():.2f}"


if __name__ == "__main__":
    from multiprocessing import Pool
    keys = json.load(open("esri_keys.json"))

    def ll(z, x, y):
        n = 2 ** z
        return x / n * 360 - 180, math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    f, c = set(), set()
    for _, z, x, y in keys:
        lo0, la1 = ll(z, x, y); lo1, la0 = ll(z, x + 1, y + 1)
        if z >= 11:
            f |= {(math.floor(a * 2), math.floor(d * 2)) for a in (lo0, lo1) for d in (la0, la1)}
            f |= {(cx, cy) for cx in range(math.floor(lo0 * 2), math.floor(lo1 * 2) + 1) for cy in range(math.floor(la0 * 2), math.floor(la1 * 2) + 1)}
        elif z == 10:
            c |= {(cx, cy) for cx in range(math.floor(lo0), math.floor(lo1) + 1) for cy in range(math.floor(la0), math.floor(la1) + 1)}
    jobs = [("f",) + k for k in sorted(f)] + [("c",) + k for k in sorted(c)]
    print(len(jobs), "cells", flush=True)
    with Pool(6) as p:
        for r in p.imap_unordered(cell, jobs):
            print(r, flush=True)
