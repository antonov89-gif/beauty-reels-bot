import os, concurrent.futures as cf
from satfetch import fetch
from PIL import Image, ImageDraw
SP = {"FL": (-83.0, 27.6, 3.6), "MIA": (-80.20, 25.80, 0.16), "OB": (-80.1310, 25.7800, 0.008), "PORT": (-80.1650, 25.7770, 0.012),
      "MAC": (-80.1600, 25.7860, 0.014), "BRK": (-80.1920, 25.7640, 0.010), "CIRC": (-80.18925, 25.76985, 0.0012), "PCK": (-80.2405, 25.7275, 0.004),
      "OPA": (-80.2506, 25.9017, 0.003), "LH": (-80.2193, 25.7656, 0.003), "WYN": (-80.1993, 25.8011, 0.003), "KAS": (-80.1881, 25.7814, 0.003),
      "MET": (-80.1930, 25.7745, 0.004), "VEN": (-80.1600, 25.7915, 0.012), "KEYS": (-81.165, 24.705, 0.03), "EVG": (-80.70, 25.45, 0.5)}
def go(k):
    lon, lat, d = SP[k]
    if not os.path.exists(f"sat/{k}.jpg"): fetch(lon, lat, d, f"sat/{k}.jpg", 2560, 1440)
    return k
if __name__ == "__main__":
    with cf.ThreadPoolExecutor(4) as ex: print(list(ex.map(go, SP)))
    sh = Image.new("RGB", (480 * 4, 270 * 4))
    for i, k in enumerate(SP):
        im = Image.open(f"sat/{k}.jpg").resize((480, 270)); dr = ImageDraw.Draw(im)
        dr.line((240, 0, 240, 270), fill=(255, 0, 0)); dr.line((0, 135, 480, 135), fill=(255, 0, 0)); dr.text((6, 4), k, fill=(255, 255, 0))
        sh.paste(im, ((i % 4) * 480, (i // 4) * 270))
    sh.save("sat/check.jpg", quality=88)
