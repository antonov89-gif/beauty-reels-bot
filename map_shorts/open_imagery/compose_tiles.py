"""Compose tiles/esri/{z}/{x}_{y}.jpg (cache name the engine reads) from open imagery: BM z8 base < 1-deg cells (100 m) < 0.5-deg cells (25 m)."""
import json, math, os, sys
import cv2
import numpy as np
from PIL import Image
import tiles as T

CELLS = {}


def cell_img(kind, cx, cy):
    k = (kind, cx, cy)
    if k not in CELLS:
        p = f"cells/{kind}_{cx}_{cy}.png"
        CELLS[k] = np.asarray(Image.open(p).convert("RGB")) if os.path.exists(p) else None
    return CELLS[k]


def lonlat_grid(z, x, y):
    n = 2 ** z
    px = (x + (np.arange(256) + 0.5) / 256) / n
    py = (y + (np.arange(256) + 0.5) / 256) / n
    lon = px * 360 - 180
    lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * py))))
    return np.meshgrid(lon, lat)


def bm_sample(lon, lat):
    z = 8
    n = 2 ** z
    gx = (lon + 180) / 360 * n * 256
    gy = (1 - np.arcsinh(np.tan(np.radians(lat))) / np.pi) / 2 * n * 256
    x0, x1 = int(gx.min() // 256), int(gx.max() // 256)
    y0, y1 = int(gy.min() // 256), int(gy.max() // 256)
    A = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256, 3), np.uint8)
    for i, tx in enumerate(range(x0, x1 + 1)):
        for j, ty in enumerate(range(y0, y1 + 1)):
            A[j * 256:(j + 1) * 256, i * 256:(i + 1) * 256] = T.tile("bm", z, tx % n, ty)
    return cv2.remap(A, (gx - x0 * 256 - 0.5).astype(np.float32), (gy - y0 * 256 - 0.5).astype(np.float32), cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def overlay(out, lon, lat, kind, step):
    cxs = np.floor(lon / step).astype(int)
    cys = np.floor(lat / step).astype(int)
    for cx in np.unique(cxs):
        for cy in np.unique(cys):
            im = cell_img(kind, int(round(cx * step * (2 if kind == "f" else 1))), int(round(cy * step * (2 if kind == "f" else 1))))
            if im is None:
                continue
            m = (cxs == cx) & (cys == cy)
            h, w = im.shape[:2]
            l0, b0 = cx * step, cy * step
            fx = ((lon - l0) / step * w - 0.5).astype(np.float32)
            fy = ((l0 * 0 + b0 + step - lat) / step * h - 0.5).astype(np.float32)
            smp = cv2.remap(im, fx, fy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            out[m] = smp[m]


def make(z, x, y):
    p = f"tiles/esri/{z}/{x}_{y}.jpg"
    if os.path.exists(p):
        return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    lon, lat = lonlat_grid(z, x, y)
    out = bm_sample(lon, lat)
    overlay(out, lon, lat, "c", 1.0)
    if z >= 11:
        overlay(out, lon, lat, "f", 0.5)
    Image.fromarray(out).save(p, quality=93)


if __name__ == "__main__":
    keys = json.load(open("esri_keys.json"))
    for i, (_, z, x, y) in enumerate(keys):
        make(z, x, y)
        if i % 200 == 0:
            print(i, len(keys), flush=True)
