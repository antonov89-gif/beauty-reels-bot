import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
def my(lat): return np.degrees(np.log(np.tan(np.pi/4 + np.radians(lat)/2)))
B1 = Image.open('assets/B1_aug.jpg'); C1 = Image.open('assets/C1_aug.jpg')
def eq_crop(lon0, lon1, lat0, lat1):
    out = Image.new('RGB', (int((lon1-lon0)*240), int((lat1-lat0)*240)))
    for im, off in ((B1, -90), (C1, 0)):
        a, b = max(lon0, off), min(lon1, off+90)
        if a >= b: continue
        c = im.crop((int((a-off)*240), int((90-lat1)*240), int((b-off)*240), int((90-lat0)*240)))
        out.paste(c, (int((a-lon0)*240), 0))
    return out
def style(E):
    E = E.astype(np.float32)/255
    g = E.mean(2, keepdims=True)
    sea = (E[..., 2:3] > E[..., 0:1] + 0.03) & (g < 0.33)
    E = np.clip(g + (E-g)*1.25, 0, 1)
    E = np.where(sea, E*np.array([0.42, 0.62, 0.95]) + np.array([0.0, 0.02, 0.06]), E*np.array([1.05, 1.0, 0.9]))
    E = np.clip(E**0.95, 0, 1)
    return E
def merc(E, lat0, lat1, ppd):
    H = E.shape[0]
    rows = int(round((my(lat1)-my(lat0))*ppd))
    Y = np.linspace(my(lat1), my(lat0), rows)
    lat = np.degrees(2*np.arctan(np.exp(np.radians(Y))) - np.pi/2)
    src = np.clip(((lat1-lat)/(lat1-lat0)*(H-1)).astype(np.int64), 0, H-1)
    return (E[src]*255).astype(np.uint8)
def build(name, lon0, lon1, lat0, lat1, ppd, strip=2000):
    eq = eq_crop(lon0, lon1, lat0, lat1)
    if ppd != 240: eq = eq.resize((int((lon1-lon0)*ppd), int((lat1-lat0)*ppd)), Image.LANCZOS)
    E = np.asarray(eq)
    out = []
    for x0 in range(0, E.shape[1], strip):  # style in strips to limit memory
        out.append(merc(style(E[:, x0:x0+strip]), lat0, lat1, ppd))
    M = np.concatenate(out, 1)
    np.save(name, M); print(name, M.shape)
build('tex_hi.npy', -15, 50, 22, 62, 240)
build('tex_mid.npy', -25, 65, 8, 70, 120)
m = np.load('tex_mid.npy'); np.save('tex_lo.npy', np.asarray(Image.fromarray(m).resize((m.shape[1]//4, m.shape[0]//4), Image.LANCZOS)))
Image.fromarray(m).resize((m.shape[1]//10, m.shape[0]//10)).save('tex_prev.jpg')
