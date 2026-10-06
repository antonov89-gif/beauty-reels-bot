"""Hillshade relief for the Aral region from public Terrarium elevation tiles (AWS open data). Output: shade.npy
aligned to the 'mid' texture grid (lon0=-25, lat1=70, 120 px/deg), cropped to lon 38..66, lat 28..56."""
import io, math, numpy as np, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
Z = 8
N = 2 ** Z
LON0, LON1, LAT0, LAT1 = 38.0, 66.0, 28.0, 56.0
def tx(lon): return (lon + 180) / 360 * N
def ty(lat):
    r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * N
x0, x1 = int(tx(LON0)), int(tx(LON1))
y0, y1 = int(ty(LAT1)), int(ty(LAT0))
def get(xy):
    x, y = xy
    for _ in range(3):
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
dem = dem[py0:py1, px0:px1]
print("dem", dem.shape, dem.min(), dem.max())
dem = np.maximum(dem, -28.0)  # flatten sea/bathymetry (Caspian surface ~ -28 m)
# metres per pixel at each row (web mercator): 156543.03/2^Z * cos(lat)
rows = np.arange(dem.shape[0]) + py0 + y0 * 256
lat = np.degrees(np.arctan(np.sinh(math.pi * (1 - 2 * rows / (N * 256)))))
mpp = (40075016.7 / (N * 256) * np.cos(np.radians(lat)))[:, None]
EXAG = 7.0
gy, gx = np.gradient(dem)
dzdx, dzdy = gx / mpp * EXAG, gy / mpp * EXAG
az, alt = math.radians(315), math.radians(42)
slope = np.arctan(np.hypot(dzdx, dzdy)); aspect = np.arctan2(dzdy, -dzdx)
shade = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
# resample to the mid texture grid (120 px/deg, mercator)
def my(l): return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(l) / 2)))
w = int(round((LON1 - LON0) * 120)); h = int(round((my(LAT1) - my(LAT0)) * 120))
sh = np.asarray(Image.fromarray(((shade + 1) * 127.5).astype(np.uint8)).resize((w, h), Image.LANCZOS)).astype(np.float32) / 127.5 - 1
Image.fromarray(np.clip(shade * 255, 0, 255).astype(np.uint8)).resize((w, h)).save("shade_prev.png")
np.save("shade.npy", sh.astype(np.float32))
np.save("dem_small.npy", np.asarray(Image.fromarray(dem).resize((w, h), Image.BILINEAR)).astype(np.float32))
print("shade", sh.shape, sh.mean())
