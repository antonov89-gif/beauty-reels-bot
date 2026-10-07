"""Web-Mercator tile camera centred anywhere (wraps the antimeridian).
bm = NASA GIBS Blue Marble shaded relief (z<=8), esri = Esri World Imagery (close-ups)."""
import math, os, io, urllib.request, concurrent.futures as cf
import numpy as np
from PIL import Image
W, H = 1080, 1920
URL = {"bm": "https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_ShadedRelief_Bathymetry/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpeg",
       "esri": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"}
_MEM = {}
def my(lat):
    lat = max(-85.0, min(85.0, lat))
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
def path(src, z, x, y): return f"tiles/{src}/{z}/{x}_{y}.jpg"
def fetch(src, z, x, y):
    p = path(src, z, x, y)
    if os.path.exists(p): return p
    if os.path.exists(p + ".missing"): return None
    os.makedirs(os.path.dirname(p), exist_ok=True)
    for _ in range(4):
        try:
            data = urllib.request.urlopen(urllib.request.Request(URL[src].format(z=z, x=x, y=y), headers={"User-Agent": "curl/8.5.0"}), timeout=60).read()
            im = Image.open(io.BytesIO(data)).convert("RGB")
            a = np.asarray(im)
            if a.std() < 2.5: raise ValueError("placeholder")
            im.save(p, quality=93); return p
        except Exception:
            pass
    open(p + ".missing", "w").close(); return None
def tile(src, z, x, y):
    k = (src, z, x, y)
    if k not in _MEM:
        if len(_MEM) > 3000: _MEM.clear()
        p = fetch(src, z, x, y)
        if p: _MEM[k] = np.asarray(Image.open(p).convert("RGB"))
        elif z <= 1: _MEM[k] = np.full((256, 256, 3), (12, 30, 70), np.uint8)
        else:
            par = tile(src, z - 1, x // 2, y // 2)
            q = par[(y % 2) * 128:(y % 2) * 128 + 128, (x % 2) * 128:(x % 2) * 128 + 128]
            _MEM[k] = np.asarray(Image.fromarray(q).resize((256, 256), Image.BICUBIC))
    return _MEM[k]
class Cam:
    """lon may be any real (unwrapped); span = degrees across the frame width."""
    def __init__(self, lon, lat, span, src=None, zmax=None):
        self.lon, self.span = lon, span
        self.ppd = W / span
        self.Y = my(lat)
        need = self.ppd * 360 / 256
        z = max(1, math.ceil(math.log2(max(need, 1)) + 0.15))
        self.src = src or ("bm" if z <= 8 else "esri")
        self.z = min(z, 8 if self.src == "bm" else (zmax or 15))
    def xy(self, lon, lat):
        lon = lon + 360 * round((self.lon - lon) / 360)
        return ((lon - self.lon) * self.ppd + W / 2, (self.Y - my(lat)) * self.ppd + H / 2)
    def tiles_needed(self):
        z, n = self.z, 2 ** self.z
        tpd = 256 * n / 360  # tile px per degree
        x0 = (self.lon - self.span / 2 + 180) * tpd; x1 = (self.lon + self.span / 2 + 180) * tpd
        hh = H / 2 / self.ppd
        Ymax = math.degrees(math.pi)
        y0 = (Ymax - (self.Y + hh)) * tpd; y1 = (Ymax - (self.Y - hh)) * tpd
        return z, tpd, x0, x1, y0, y1, range(math.floor(x0 / 256), math.floor(x1 / 256) + 1), range(math.floor(y0 / 256), math.floor(y1 / 256) + 1)
    def keys(self):
        z, tpd, x0, x1, y0, y1, xs, ys = self.tiles_needed(); n = 2 ** z
        return [(self.src, z, tx % n, ty) for tx in xs for ty in ys if 0 <= ty < n]
    def render(self):
        z, tpd, x0, x1, y0, y1, xs, ys = self.tiles_needed(); n = 2 ** z
        tx0, ty0 = xs.start, ys.start
        A = np.zeros((len(ys) * 256, len(xs) * 256, 3), np.uint8); A[:] = (12, 30, 70)
        for i, tx in enumerate(xs):
            for j, ty in enumerate(ys):
                if 0 <= ty < n: A[j * 256:(j + 1) * 256, i * 256:(i + 1) * 256] = tile(self.src, z, tx % n, ty)
        im = Image.fromarray(A)
        return im.resize((W, H), Image.BICUBIC, box=(x0 - tx0 * 256, y0 - ty0 * 256, x1 - tx0 * 256, y1 - ty0 * 256))
def prefetch(keys, workers=16):
    keys = sorted(set(keys))
    todo = [k for k in keys if not os.path.exists(path(*k))]
    with cf.ThreadPoolExecutor(workers) as ex: list(ex.map(lambda k: fetch(*k), todo))
    return len(keys), len(todo)
