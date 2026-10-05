import sys, time
from PIL import Image
import engine as E
fr = [int(x) for x in sys.argv[1].split(',')]
ims = []; t0 = time.time()
for f in fr:
    ims.append(E.frame(f).resize((270, 480)))
print('s/frame', round((time.time() - t0) / len(fr), 2))
cols = 6; rows = (len(ims) + cols - 1) // cols
g = Image.new('RGB', (270 * cols, 480 * rows))
for i, im in enumerate(ims):
    g.paste(im, ((i % cols) * 270, (i // cols) * 480))
g.save(sys.argv[2])
