import sys
sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/open_imagery")
import open_imagery as oi
LON, LAT = 88.76196, 26.14974
from PIL import Image
# mid: GIBS 500 m over +-3 deg; mid2: Sentinel-2 mosaic +-0.04 deg
b = oi.bbox_of(LON, LAT, 3.0, 2000, 2000)
oi.gibs_image(b, 2000, 2000, layer="BlueMarble_ShadedRelief_Bathymetry").save("sat/dh_mid.jpg", quality=93)
print("mid ok", flush=True)
print(oi.build(LON, LAT, 0.04, 2000, 2000, "sat/dh_mid2.jpg"), flush=True)
