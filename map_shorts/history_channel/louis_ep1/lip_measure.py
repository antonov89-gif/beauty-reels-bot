"""Mouth opening per frame of a clip (MediaPipe face mesh, pip mediapipe==0.10.14): inner-lip gap / face height, None where no face is found (head turned away). Usage: python3 lip_measure.py clip.mp4 out.json -> [[t, opening, width], ...]. Used to place our voice on the real lip movement instead of on the model's own audio (its first word can start 0.4 s after the mouth opens)."""
import cv2, numpy as np, mediapipe as mp, sys, json
src=sys.argv[1]; out=sys.argv[2]
fm=mp.solutions.face_mesh.FaceMesh(static_image_mode=False,max_num_faces=1,refine_landmarks=False,min_detection_confidence=0.3,min_tracking_confidence=0.3)
cap=cv2.VideoCapture(src); fps=cap.get(cv2.CAP_PROP_FPS); res=[]; i=0
while True:
    ok,f=cap.read()
    if not ok: break
    r=fm.process(cv2.cvtColor(f,cv2.COLOR_BGR2RGB))
    if r.multi_face_landmarks:
        L=r.multi_face_landmarks[0].landmark
        lip=abs(L[14].y-L[13].y); face=abs(L[152].y-L[10].y)+1e-6; w=abs(L[291].x-L[61].x)+1e-6
        res.append((i/fps,float(lip/face),float(w/face)))
    else: res.append((i/fps,None,None))
    i+=1
json.dump(res,open(out,'w'))
print(len(res),"frames",sum(1 for r in res if r[1] is not None),"with face")
