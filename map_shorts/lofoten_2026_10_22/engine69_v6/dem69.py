"""Terrain for the Lofoten dive (engine69): AWS Terrain Tiles (Terrarium, free) -> elevation on each satellite key's grid -> hillshade.
python3 dem69.py  writes dem/<KEY>.npy (float32 elevation, metres) for the keys used in the dive."""
import io
import math
import os
import subprocess

import numpy as np
from PIL import Image

from sat65 import SP, size

URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"


def tile_xy(lon, lat, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def tile(z, x, y):
    p = f"dem/t_{z}_{x}_{y}.png"
    if not os.path.exists(p):
        subprocess.run(["curl", "-sSf", "--max-time", "60", "-o", p, URL.format(z=z, x=x, y=y)], check=True)
    a = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
    return a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768


def elevation(key, z, out_h=1024):
    lon0, lat0, d = SP[key]
    w, h = size(key)
    dl = d * (w / h) / math.cos(math.radians(lat0))
    l0, l1, b0, b1 = lon0 - dl, lon0 + dl, lat0 - d, lat0 + d
    x0, y1 = tile_xy(l0, b0, z)
    x1, y0 = tile_xy(l1, b1, z)
    tx = range(int(x0), int(x1) + 1)
    ty = range(int(y0), int(y1) + 1)
    mosaic = np.vstack([np.hstack([tile(z, x, y) for x in tx]) for y in ty])
    out_w = int(out_h * w / h)
    lons = np.linspace(l0, l1, out_w)
    lats = np.linspace(b1, b0, out_h)
    X = np.array([tile_xy(lo, 0, z)[0] for lo in lons]) - tx[0]
    Y = np.array([tile_xy(0, la, z)[1] for la in lats]) - ty[0]
    import cv2
    mx, my = np.meshgrid(X * 256, Y * 256)
    return cv2.remap(mosaic.astype(np.float32), mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR)


if __name__ == "__main__":
    os.makedirs("dem", exist_ok=True)
    for key, z in (("NOR", 7), ("LOF", 10), ("LO2", 11), ("MID", 12), ("RE2", 13), ("REI", 13)):
        e = elevation(key, z)
        np.save(f"dem/{key}.npy", e.astype(np.float32))
        print(key, z, e.shape, round(float(e.min())), round(float(e.max())))
