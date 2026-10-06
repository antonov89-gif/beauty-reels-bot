import os
from rembg import remove, new_session
from PIL import Image
s = new_session("u2net")
for f in sorted(os.listdir("img")):
    k = f[:-4]
    if os.path.exists(f"masks/{k}.png"):
        continue
    im = Image.open(f"img/{f}").convert("RGB")
    remove(im, session=s, only_mask=True).save(f"masks/{k}.png")
    print(k, flush=True)
