"""Image quality metrics for references (owner 05.11: "следить не только за размером 2K/4K, но и за самим качеством"). Needs opencv + numpy (python3 -m venv /tmp/fv && /tmp/fv/bin/pip install opencv-python-headless numpy).
All measured at 1024 px on the short side: sharp = variance of the Laplacian (fine detail), detail = mean difference to a half-resolution copy (low = soft or upscaled: the picture holds less detail than its pixel size), blocks = 8 px JPEG grid ratio (>1.2 = compression blocks).
Usage: python quality_metrics.py <image> [...]  -> prints JSON lines."""
import cv2, numpy as np, sys, os
def q(p):
    img=cv2.imread(p); h,w=img.shape[:2]; s=1024/min(h,w)
    g=cv2.cvtColor(cv2.resize(img,(round(w*s),round(h*s)),interpolation=cv2.INTER_AREA if s<1 else cv2.INTER_CUBIC),cv2.COLOR_BGR2GRAY).astype(np.float32)
    lap=cv2.Laplacian(g,cv2.CV_32F).var()
    d=cv2.resize(cv2.resize(g,None,fx=0.5,fy=0.5,interpolation=cv2.INTER_AREA),(g.shape[1],g.shape[0]),interpolation=cv2.INTER_CUBIC)
    hf=np.abs(g-d).mean()
    gx=np.abs(np.diff(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(np.float32),axis=1))
    blk=gx[:,7::8].mean()/np.delete(gx,np.s_[7::8],axis=1).mean()
    return w,h,lap,hf,blk
import json
for p in sys.argv[1:]:
    w,h,l,hf,b=q(p); print(json.dumps({"path":p,"w":w,"h":h,"sharp":round(float(l),1),"detail":round(float(hf),2),"blocks":round(float(b),2)}))
