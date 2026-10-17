"""Esri World Imagery exports (portrait 1620x2880, EPSG:4326) for the week-of-25.10 Shorts.
SP[key] = (lon, lat, d): centre and half-height in degrees of latitude."""
import concurrent.futures as cf
import math
import os
import time
import urllib.request

SP = {
    # pointroberts
    "PRC": (-123.030, 48.990, 0.040), "PRR": (-122.97, 49.02, 0.34), "PRW": (-123.0, 49.1, 1.2),
    # guiana
    "GUI": (-53.0, 3.9, 6.2), "OYA": (-51.80, 3.89, 0.07), "KOU": (-52.77, 5.23, 0.06), "FRA": (2.0, 45.5, 7.5),
    # velez
    "VEL": (-4.3010, 35.1722, 0.0060), "VEC": (-4.30, 35.18, 0.03), "MED": (-5.0, 36.0, 3.2),
    # birtawil
    "BIR": (34.6, 22.0, 3.2), "NES": (32.0, 21.0, 11.0),
    # sa3
    "ZAF": (24.0, -29.0, 10.5), "LES": (28.25, -29.55, 2.0), "CPT": (18.45, -33.95, 0.25),
    # llivia
    "LLI": (1.9830, 42.4625, 0.011), "LLR": (2.0, 42.45, 0.12), "PYX": (1.9, 42.7, 1.6),
    # angle
    "ANG": (-95.05, 49.35, 0.20), "ANR": (-94.9, 49.0, 0.95), "USA": (-96.0, 46.0, 6.0),
}
W_IMG, H_IMG = 1620, 2880


def fetch(key, tries=5):
    lon, lat, d = SP[key]
    out = f"sat/{key}.jpg"
    if os.path.exists(out):
        return key
    dlon = d * (W_IMG / H_IMG) / math.cos(math.radians(lat))
    u = ("https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"
         f"?bbox={lon - dlon},{lat - d},{lon + dlon},{lat + d}&bboxSR=4326&imageSR=4326&size={W_IMG},{H_IMG}&format=jpg&f=image")
    for a in range(tries):
        try:
            data = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "curl/8.5.0"}), timeout=120).read()
            open(out, "wb").write(data)
            return key
        except Exception as e:
            print("retry", key, a, str(e)[:60])
            time.sleep(4)
    raise SystemExit("fail " + key)


if __name__ == "__main__":
    os.makedirs("sat", exist_ok=True)
    with cf.ThreadPoolExecutor(4) as ex:
        print(list(ex.map(fetch, SP)))
    from PIL import Image, ImageDraw
    keys = list(SP)
    cols = 8
    sheet = Image.new("RGB", (cols * 225, ((len(keys) + cols - 1) // cols) * 400))
    for i, k in enumerate(keys):
        im = Image.open(f"sat/{k}.jpg").resize((225, 400))
        ImageDraw.Draw(im).text((6, 4), k, fill=(255, 255, 0))
        sheet.paste(im, ((i % cols) * 225, (i // cols) * 400))
    sheet.save("sat/check.jpg", quality=85)
