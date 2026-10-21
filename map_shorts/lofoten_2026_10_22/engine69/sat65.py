"""Esri World Imagery exports (EPSG:4326) for the time zones Short (engine65). WLD copied from sat64.
SP[key] = (lon, lat, d): centre and half-height in degrees of latitude. Fetched with the real curl CLI."""
import math
import os
import subprocess
import time

SP = {"WLD": (0.0, 0.0, 90.0), "FRA": (2.5, 46.5, 9.5), "MON": (7.42, 43.74, 0.8),
      "MAL": (73.2, 3.2, 4.5), "ATL": (73.5, 4.25, 0.45), "MLE": (73.515, 4.185, 0.035), "VEL": (73.529, 4.19, 0.03),
      "HUL": (73.54, 4.215, 0.03), "MAA": (73.49, 3.942, 0.03), "FUV": (73.425, -0.298, 0.04), "RAS": (72.995, 4.265, 0.04),
      "THU": (73.652, 4.375, 0.03), "UKU": (72.866, 4.859, 0.03), "GAN": (73.155, -0.693, 0.04),
      "NOR": (14.0, 67.0, 5.0), "LOF": (14.0, 68.1, 0.75), "REI": (13.09, 67.93, 0.06),
      "LO2": (13.4, 67.97, 0.5), "MID": (13.1, 67.93, 0.15), "RE2": (13.06, 67.945, 0.015)}
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
