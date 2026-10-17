"""Esri World Imagery exports (portrait 1620x2880, EPSG:4326) for the week-of-21.10 Shorts.
SP[key] = (lon, lat, d): centre and half-height in degrees of latitude."""
import concurrent.futures as cf
import math
import os
import time
import urllib.request

SP = {
    # pheasant
    "PYR": (-1.0, 43.6, 3.2), "BID": (-1.775, 43.350, 0.030), "PHE": (-1.7658, 43.3424, 0.0016),
    # baarle
    "BNL": (5.0, 51.6, 1.9), "BAA": (4.934, 51.442, 0.016), "BAC": (4.9305, 51.4405, 0.0035),
    # bolivia
    "SAM": (-64.0, -18.0, 16.0), "COA": (-69.4, -22.6, 3.6), "TIT": (-69.25, -15.95, 2.2),
    # egypt
    "EGY": (30.8, 26.8, 6.5), "DEL": (31.2, 30.6, 1.1), "NIL": (32.65, 25.70, 0.16), "CAP": (31.74, 30.02, 0.06),
    # chile
    "CHL": (-70.5, -36.5, 21.0), "EUR": (15.0, 52.0, 21.0), "ATA": (-69.4, -23.6, 1.3), "GLA": (-73.4, -49.6, 1.1),
    # canberra
    "AUS": (141.0, -28.0, 20.0), "SEA": (148.0, -35.5, 5.5), "CBR": (149.125, -35.300, 0.030),
    # diomede
    "BER": (-169.4, 65.6, 4.6), "DIO": (-169.0, 65.765, 0.12),
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
