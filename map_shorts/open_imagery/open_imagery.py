"""Esri-free imagery for the map Shorts. Same output contract as the old sat*.py fetchers: a JPEG of size (w, h) in EPSG:4326 around
(lon, lat) with half-height d degrees (the engines crop from these files).
Sources (all open): NASA GIBS Blue Marble (public domain) for the world / regions coarser than ~250 m per pixel;
Copernicus Sentinel-2 L2A true colour from the AWS open data (free, full and open: reproduction, adaptation, commercial use allowed;
notice 'Contains modified Copernicus Sentinel data <year>') for close views.
Attribution to use: 'NASA Blue Marble; Contains modified Copernicus Sentinel data 2025; Natural Earth'."""
import math
import os
import json
import subprocess
import urllib.request

import numpy as np
from PIL import Image

os.environ.setdefault("GDAL_HTTP_CAINFO", "/root/.ccr/ca-bundle.crt")
os.environ.setdefault("CURL_CA_BUNDLE", "/root/.ccr/ca-bundle.crt")
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif,.TIF")
GIBS = ("https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?SERVICE=WMS&REQUEST=GetMap&VERSION=1.1.1&LAYERS={layer}"
        "&SRS=EPSG:4326&BBOX={b}&WIDTH={w}&HEIGHT={h}&FORMAT=image/jpeg")
STAC = "https://earth-search.aws.element84.com/v1/search"


def bbox_of(lon, lat, d, w, h):
    dl = d * (w / h) / math.cos(math.radians(lat))
    return lon - dl, lat - d, lon + dl, lat + d


def gibs_image(b, w, h, layer="BlueMarble_NextGeneration"):
    """GIBS limits the request size; fetch in horizontal bands of <= 2048 rows and stack."""
    l0, b0, l1, b1 = b
    out = Image.new("RGB", (w, h))
    band = 1024
    tmp = f"/tmp/_gibs_{os.getpid()}.jpg"
    for y0 in range(0, h, band):
        hh = min(band, h - y0)
        t = b1 - (b1 - b0) * y0 / h
        bt = b1 - (b1 - b0) * (y0 + hh) / h
        u = GIBS.format(layer=layer, b=f"{l0},{bt},{l1},{t}", w=w, h=hh)
        for attempt in range(4):
            r = subprocess.run(["curl", "-sSf", "--max-time", "120", "-o", tmp, u])
            if r.returncode == 0 and os.path.getsize(tmp) > 2000:
                break
        else:
            raise SystemExit("GIBS failed " + u)
        out.paste(Image.open(tmp).convert("RGB").resize((w, hh)), (0, y0))
    return out


def s2_scenes(b, lat, years=(2023, 2024, 2025), cloud=35, limit=300):
    """Scenes in the local summer (snow-free, sun high), least cloudy first; best scene of every tile first."""
    months = (6, 7, 8, 9) if lat >= 0 else (12, 1, 2, 3)
    feats = []
    for y in years:
        d0, d1 = (f"{y}-06-01", f"{y}-09-30") if lat >= 0 else (f"{y}-12-01", f"{y + 1}-03-31")
        body = {"collections": ["sentinel-2-l2a"], "bbox": list(b), "datetime": f"{d0}T00:00:00Z/{d1}T23:59:59Z",
                "query": {"eo:cloud_cover": {"lt": cloud}}, "limit": limit // len(years)}
        r = urllib.request.Request(STAC, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        try:
            feats += json.load(urllib.request.urlopen(r, timeout=90))["features"]
        except Exception:
            pass
    feats.sort(key=lambda f: f["properties"]["eo:cloud_cover"])
    seen, first, rest = set(), [], []
    for f in feats:
        tile = f["properties"].get("grid:code") or f["id"].split("_")[1]
        (rest if tile in seen else first).append(f)
        seen.add(tile)
    return first + rest


def s2_mosaic(b, w, h, lat, max_scenes=40):
    """Cloud-masked mosaic with the Sentinel-2 scene classification (SCL): cloud, shadow, snow and no-data pixels are filled from other scenes."""
    import rasterio
    from rasterio.enums import Resampling
    from rasterio.transform import from_bounds
    from rasterio.vrt import WarpedVRT
    l0, b0, l1, b1 = b
    s2_mosaic.__dict__.pop("water_ref", None)
    dst = from_bounds(l0, b0, l1, b1, w, h)
    acc = np.zeros((h, w, 3), np.uint8)
    filled = np.zeros((h, w), bool)
    used = []
    for f in s2_scenes(b, lat):
        if filled.mean() > 0.995 or len(used) >= max_scenes:
            break
        try:
            with rasterio.open(f["assets"]["visual"]["href"]) as src, rasterio.open(f["assets"]["scl"]["href"]) as sc:
                with WarpedVRT(src, crs="EPSG:4326", transform=dst, width=w, height=h, resampling=Resampling.bilinear, nodata=0) as vrt:
                    a = vrt.read([1, 2, 3])
                with WarpedVRT(sc, crs="EPSG:4326", transform=dst, width=w, height=h, resampling=Resampling.nearest, nodata=0) as vs:
                    c = vs.read(1)
        except Exception:
            continue
        a = np.moveaxis(a, 0, -1)
        wat = c == 6
        if wat.sum() > 2000:                                              # water tone differs between scenes: match every scene's water to the first one's
            med = np.median(a[wat].astype(np.float32), axis=0)
            if "water_ref" not in s2_mosaic.__dict__:
                s2_mosaic.water_ref = med
            sh = (s2_mosaic.water_ref - med)
            a = a.astype(np.float32)
            a[wat] = np.clip(a[wat] + sh, 0, 255)
            a = a.astype(np.uint8)
        good = (a.sum(axis=2) > 12) & np.isin(c, (4, 5, 6, 7))             # vegetation, bare, water, unclassified
        m = good & ~filled
        if m.mean() > 0.002:
            acc[m] = a[m]
            filled |= m
            used.append((f["id"], round(float(m.mean()), 3)))
    return Image.fromarray(acc), filled, used


def build(lon, lat, d, w, h, out, quality=94):
    b = bbox_of(lon, lat, d, w, h)
    m_per_px = 2 * d * 111320 / h
    base = gibs_image(b, w, h, "BlueMarble_ShadedRelief_Bathymetry" if m_per_px > 60 else "BlueMarble_NextGeneration")
    info = {"m_per_px": round(m_per_px), "source": "gibs"}
    if m_per_px <= 260 and d <= 2.5:                                      # Sentinel-2 is sharper than Blue Marble here
        s2, filled, used = s2_mosaic(b, w, h, lat)
        if filled.mean() > 0.02:
            arr = np.asarray(base).copy()
            a2 = np.asarray(s2)
            arr[filled] = a2[filled]
            base = Image.fromarray(arr)
            info.update(source="gibs+sentinel2", s2_cover=round(float(filled.mean()), 3), scenes=used)
    base.save(out, quality=quality)
    if info["source"] == "gibs+sentinel2":
        fix_sea(out)
    return info

def fix_sea(path, sea=(14, 40, 62)):
    """Sentinel-2 open sea is near-black with tile seams: replace water (blue >= green, dark) by a smooth sea tone, keep shore detail."""
    from scipy.ndimage import gaussian_filter
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.3 * r + 0.59 * g + 0.11 * b
    wm = ((b >= g - 1) & (lum < 60)).astype(np.float32)
    wm = gaussian_filter(wm, 3)
    wm = np.clip((wm - 0.35) / 0.4, 0, 1)
    tone = np.array(sea, np.float32) + (lum[..., None] - 14) * 0.6 * 0                # flat tone
    out = a * (1 - wm[..., None]) + tone * wm[..., None]
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(path, quality=94)


if __name__ == "__main__":
    import sys
    lon, lat, d, w, h = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    print(build(lon, lat, d, w, h, sys.argv[6]))
