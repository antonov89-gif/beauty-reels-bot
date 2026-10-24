import sys
sys.path.insert(0, "/home/user/beauty-reels-bot/map_shorts/open_imagery")
import open_imagery as oi
from concurrent.futures import ProcessPoolExecutor
LON, LAT = 88.76196, 26.14974
JOBS = {"dh_reg": (0.25, 2000, 2000), "dh_loc": (0.0045, 2000, 2000)}
def run(k):
    d, w, h = JOBS[k]
    return k, oi.build(LON, LAT, d, w, h, f"sat/{k}.jpg")
if __name__ == "__main__":
    with ProcessPoolExecutor(2) as ex:
        for r in ex.map(run, JOBS): print(r, flush=True)
