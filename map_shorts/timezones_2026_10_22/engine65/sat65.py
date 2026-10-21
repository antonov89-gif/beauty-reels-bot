"""Esri World Imagery exports (EPSG:4326) for the time zones Short (engine65). WLD copied from sat64.
SP[key] = (lon, lat, d): centre and half-height in degrees of latitude. Fetched with the real curl CLI."""
import math
import os
import subprocess
import time

SP = {"WLD": (0.0, 0.0, 90.0), "FRA": (2.5, 46.5, 9.5), "MON": (7.42, 43.74, 0.8)}
SZ = {"WLD": (4096, 2048)}
W_IMG, H_IMG = 2304, 4096


def size(key):
    return SZ.get(key, (W_IMG, H_IMG))


def fetch(key, tries=5):
    lon, lat, d = SP[key]
    w, h = size(key)
    out = f"sat65/{key}.jpg"
    if os.path.exists(out):
        return key
    dlon = d * (w / h) / math.cos(math.radians(lat))
    u = ("https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"
         f"?bbox={lon - dlon},{lat - d},{lon + dlon},{lat + d}&bboxSR=4326&imageSR=4326&size={w},{h}&format=jpg&f=image")
    for a in range(tries):
        r = subprocess.run(["curl", "-sSf", "--max-time", "120", "-o", out, u])
        if r.returncode == 0 and os.path.getsize(out) > 20000:
            return key
        print("retry", key, a)
        time.sleep(4)
    raise SystemExit("fail " + key)


if __name__ == "__main__":
    for k in SP:
        print(fetch(k))
