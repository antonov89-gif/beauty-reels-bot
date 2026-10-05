import sys, time
from PIL import Image
import engine12 as E
if sys.argv[1] == "shots":
    fr = [int(((s["t0"] + s["t1"]) / 2 + 0.6 * (s["t1"] - s["t0"]) / 2) * E.FPS) for s in E.SHOTS]
else:
    fr = [int(x) for x in sys.argv[1].split(",")]
ims = []; t0 = time.time()
for f in fr:
    ims.append(E.frame(min(E.NF - 1, f)).resize((216, 384)))
print("s/frame", round((time.time() - t0) / len(fr), 2))
cols = 9; rows = (len(ims) + cols - 1) // cols
g = Image.new("RGB", (216 * cols, 384 * rows), (0, 0, 0))
for i, im in enumerate(ims):
    g.paste(im, ((i % cols) * 216, (i // cols) * 384))
g.save(sys.argv[2])
