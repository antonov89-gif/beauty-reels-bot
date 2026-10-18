"""Esri World Imagery exports (EPSG:4326) for the Turkey Short (engine63). Portrait 2304x4096 (Esri max) unless SZ overrides.
SP[key] = (lon, lat, d): centre and half-height in degrees of latitude. Fetched with the real curl CLI."""
import concurrent.futures as cf
import math
import os
import time
import subprocess

SP = {
    "WID": (35.0, 38.5, 24.0), "TUR": (35.5, 39.0, 13.5), "MAR": (29.0, 40.95, 1.3),
    "IST": (29.04, 41.06, 0.22), "BOS": (29.062, 41.084, 0.035), "ARA": (44.30, 39.70, 0.45),
    "OTT": (24.0, 34.0, 18.0),
    "EUR": (10.0, 48.0, 14.0), "BIG": (22.0, 44.0, 30.0),
}
SZ = {"OTT": (4096, 2304)}
W_IMG, H_IMG = 2304, 4096


def size(key):
    return SZ.get(key, (W_IMG, H_IMG))


def fetch(key, tries=5):
    lon, lat, d = SP[key]
    w, h = size(key)
    out = f"sat63/{key}.jpg"
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
    os.makedirs("sat63", exist_ok=True)
    with cf.ThreadPoolExecutor(4) as ex:
        print(list(ex.map(fetch, SP)))
    from PIL import Image, ImageDraw
    keys = list(SP)
    cols = 8
    sheet = Image.new("RGB", (cols * 225, ((len(keys) + cols - 1) // cols) * 400))
    for i, k in enumerate(keys):
        im = Image.open(f"sat63/{k}.jpg").resize((225, 400))  # landscape keys are squeezed in the sheet
        ImageDraw.Draw(im).text((6, 4), k, fill=(255, 255, 0))
        sheet.paste(im, ((i % cols) * 225, (i // cols) * 400))
    sheet.save("sat63/check.jpg", quality=85)
