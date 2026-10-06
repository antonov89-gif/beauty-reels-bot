"""Hillshade for a region from public Terrarium elevation tiles; writes shade_mid.npy (120 ppd) and shade_hi.npy (240 ppd).
usage: python3 build_dem2.py LON0 LON1 LAT0 LAT1  (grid origin = region top-left, mercator)"""
import io, math, sys, numpy as np, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
LON0, LON1, LAT0, LAT1 = map(float, sys.argv[1:5])
Z = 8; N = 2 ** Z
def tx(lon): return (lon + 180) / 360 * N
def ty(lat):
    r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * N
x0, x1 = int(tx(LON0)), int(tx(LON1)); y0, y1 = int(ty(LAT1)), int(ty(LAT0))
def get(xy):
    x, y = xy
    for _ in range(4):
        try:
            d = urllib.request.urlopen(f"https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{x}/{y}.png", timeout=30).read()
            a = np.asarray(Image.open(io.BytesIO(d)).convert("RGB")).astype(np.float32)
            return xy, a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
        except Exception:
            pass
    raise RuntimeError(xy)
tiles = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]
with ThreadPoolExecutor(12) as ex:
    res = dict(ex.map(get, tiles))
dem = np.zeros(((y1 - y0 + 1) * 256, (x1 - x0 + 1) * 256), np.float32)
for (x, y), a in res.items():
    dem[(y - y0) * 256:(y - y0 + 1) * 256, (x - x0) * 256:(x - x0 + 1) * 256] = a
px0, px1 = int((tx(LON0) - x0) * 256), int((tx(LON1) - x0) * 256)
py0, py1 = int((ty(LAT1) - y0) * 256), int((ty(LAT0) - y0) * 256)
dem = np.maximum(dem[py0:py1, px0:px1], -28.0)
rows = np.arange(dem.shape[0]) + py0 + y0 * 256
lat = np.degrees(np.arctan(np.sinh(math.pi * (1 - 2 * rows / (N * 256)))))
mpp = (40075016.7 / (N * 256) * np.cos(np.radians(lat)))[:, None]
EXAG = 5.0
gy, gx = np.gradient(dem)
dzdx, dzdy = gx / mpp * EXAG, gy / mpp * EXAG
az, alt = math.radians(315), math.radians(42)
slope = np.arctan(np.hypot(dzdx, dzdy)); aspect = np.arctan2(dzdy, -dzdx)
shade = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
def my(l): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(l) / 2)))
for name, ppd in (("mid", 120), ("hi", 240)):
    w = int(round((LON1 - LON0) * ppd)); h = int(round((my(LAT1) - my(LAT0)) * ppd))
    sh = np.asarray(Image.fromarray(((shade + 1) * 127.5).astype(np.uint8)).resize((w, h), Image.LANCZOS))
    np.save(f"shade_{name}.npy", sh)
    print(name, sh.shape)
w = int(round((LON1 - LON0) * 120)); h = int(round((my(LAT1) - my(LAT0)) * 120))
el = np.asarray(Image.fromarray(np.maximum(dem, 0).astype(np.float32)).resize((w, h), Image.BILINEAR))
np.save("elev_mid.npy", el.astype(np.float32))
print("dem", dem.min(), dem.max(), "elev", el.shape)
