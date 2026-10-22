"""High-resolution open orthophoto overlays on top of the open base (GIBS + Sentinel-2):
naip = USGS NAIP (US public domain), ign = IGN France Geoplateforme (Licence Ouverte Etalab), pnoa = IGN Spain PNOA (CC BY 4.0).
CLI: python3 hires.py lon lat d w h out src[,src...]"""
import io, math, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import open_imagery as O

URL = {
    "naip": "https://imagery.nationalmap.gov/arcgis/rest/services/USGSNAIPImagery/ImageServer/exportImage?bbox={l0},{b0},{l1},{b1}&bboxSR=4326&imageSR=4326&size={w},{h}&format=png&f=image",
    "ign": "https://data.geopf.fr/wms-r/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=ORTHOIMAGERY.ORTHOPHOTOS&STYLES=&CRS=EPSG:4326&BBOX={b0},{l0},{b1},{l1}&WIDTH={w}&HEIGHT={h}&FORMAT=image/png",
    "pnoa": "https://www.ign.es/wms-inspire/pnoa-ma?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=OI.OrthoimageCoverage&STYLES=&CRS=EPSG:4326&BBOX={b0},{l0},{b1},{l1}&WIDTH={w}&HEIGHT={h}&FORMAT=image/png&TRANSPARENT=TRUE",
}


def fetch(src, b, w, h, band=1000):
    if src == "naip":
        band = h                                            # ImageServer keeps the aspect ratio of the bbox: one request
    l0, b0, l1, b1 = b
    out = np.zeros((h, w, 4), np.uint8)
    for y0 in range(0, h, band):
        hh = min(band, h - y0)
        t = b1 - (b1 - b0) * y0 / h
        bt = b1 - (b1 - b0) * (y0 + hh) / h
        u = URL[src].format(l0=l0, b0=bt, l1=l1, b1=t, w=w, h=hh)
        tmp = tempfile.mktemp(suffix=".png")
        for _ in range(4):
            r = subprocess.run(["curl", "-sSf", "--max-time", "180", "-o", tmp, u])
            if r.returncode == 0 and os.path.getsize(tmp) > 500:
                break
        else:
            continue
        im = Image.open(tmp).convert("RGBA")
        os.remove(tmp)
        a = np.asarray(im)
        rgb = a[..., :3].astype(int).sum(2)
        valid = (a[..., 3] > 200) & (rgb > 9) & (rgb < 760)
        a = a.copy()
        a[..., 3] = np.where(valid, 255, 0)
        out[y0:y0 + hh] = a
    return out


def build(lon, lat, d, w, h, out, srcs):
    from scipy.ndimage import gaussian_filter
    info = O.build(lon, lat, d, w, h, out)
    base = np.asarray(Image.open(out).convert("RGB")).astype(np.float32)
    b = O.bbox_of(lon, lat, d, w, h)
    used = []
    for s in srcs:
        a = fetch(s, b, w, h)
        m = a[..., 3] > 0
        if m.mean() < 0.005:
            continue
        hi = a[..., :3].astype(np.float32)
        mf = m.astype(np.float32)
        den = gaussian_filter(mf, 60) + 1e-4                                  # large-scale tone of the orthophoto -> tone of the open base
        ratio = np.stack([(gaussian_filter(base[..., c] * mf, 60) / den + 1) / (gaussian_filter(hi[..., c] * mf, 60) / den + 1) for c in range(3)], -1)
        a = a.copy()
        a[..., :3] = np.clip(hi * np.clip(ratio, 0.6, 1.6), 0, 255).astype(np.uint8)
        al = gaussian_filter(m.astype(np.float32), 2.0)[..., None]
        al = np.where(m[..., None], np.maximum(al, 0.0) ** 0.5, al * 0)
        base = base * (1 - al) + a[..., :3].astype(np.float32) * al
        used.append((s, round(float(m.mean()), 3)))
    Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).save(out, quality=94)
    info["hires"] = used
    return info


if __name__ == "__main__":
    lon, lat, d, w, h = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    print(build(lon, lat, d, w, h, sys.argv[6], sys.argv[7].split(",") if len(sys.argv) > 7 else []))
