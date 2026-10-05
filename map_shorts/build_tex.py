import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
LON0,LON1,LAT0,LAT1=-25,65,8,70
PPD=240
def crop(f, lon_off):
    im=Image.open(f)
    x0=int((max(LON0,lon_off)-lon_off)*PPD); x1=int((min(LON1,lon_off+90)-lon_off)*PPD)
    y0=int((90-LAT1)*PPD); y1=int((90-LAT0)*PPD)
    return im.crop((x0,y0,x1,y1))
a=crop('assets/B1.jpg',-90); b=crop('assets/C1.jpg',0)
eq=Image.new('RGB',(a.width+b.width,a.height)); eq.paste(a,(0,0)); eq.paste(b,(a.width,0))
eq=eq.resize((eq.width//2,eq.height//2),Image.LANCZOS)  # 120 px/deg
E=np.asarray(eq).astype(np.float32)/255
# style: saturate land, deepen sea
mx=E.max(2,keepdims=True); mn=E.min(2,keepdims=True)
gray=E.mean(2,keepdims=True)
E=np.clip(gray+(E-gray)*1.35,0,1)
sea=(E[...,2:3]>E[...,0:1]+0.04)&(E.mean(2,keepdims=True)<0.35)
E=np.where(sea,E*np.array([0.5,0.7,1.0]),E*np.array([1.06,1.0,0.9]))
E=np.clip(E**0.92,0,1)
# reproject to Mercator rows
H,W=E.shape[:2]
def my(lat): return np.log(np.tan(np.pi/4+np.radians(lat)/2))
m0,m1=my(LAT0),my(LAT1)
HM=int(round((m1-m0)/np.radians(1)*120))
rows=np.linspace(m1,m0,HM)
lat=np.degrees(2*np.arctan(np.exp(rows))-np.pi/2)
src=((LAT1-lat)/(LAT1-LAT0)*(H-1)).astype(np.int32)
M=(E[src]*255).astype(np.uint8)
np.save('tex_hi.npy',M)
Image.fromarray(M).resize((W//4,HM//4),Image.LANCZOS).save('tex_lo.png')
np.save('tex_lo.npy',np.asarray(Image.open('tex_lo.png')))
print(M.shape, (LON0,LON1,LAT0,LAT1), m0, m1)
