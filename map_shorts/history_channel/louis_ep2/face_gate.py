"""Face-consistency gate for ep.2 clips (04.11): SFace cosine similarity of each sampled frame to the card A3 and to the chain anchor.
Setup (not committed, 38 MB): python3 -m venv /tmp/fv && /tmp/fv/bin/pip install opencv-python-headless numpy; download face_detection_yunet_2023mar.onnx and face_recognition_sface_2021dec.onnx
from https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models/... into /tmp/fvm/ as yunet.onnx and sface.onnx.
Usage: /tmp/fv/bin/python face_gate.py clip1.mp4 [clip2.mp4 ...]   (prints per-frame A3/anchor similarity at 2 fps, mean, first/second half, min; verdict)
Gate used: mean vs A3 >= 0.60 and min >= 0.45 (SFace same-person threshold is 0.363, but our costumed king vs the card A3 itself scores 0.60 with the anchor, so 0.60 is the practical floor)."""
import cv2, numpy as np, sys, glob, os, subprocess
H = os.path.dirname(os.path.abspath(__file__)) + "/"
det = cv2.FaceDetectorYN.create(os.environ.get("YUNET", "/tmp/fvm/yunet.onnx"), "", (320, 320), 0.6, 0.3, 5000)
rec = cv2.FaceRecognizerSF.create(os.environ.get("SFACE", "/tmp/fvm/sface.onnx"), "")
def emb(img):
    h, w = img.shape[:2]; det.setInputSize((w, h)); _, f = det.detect(img)
    if f is None: return None
    f = f[np.argmax(f[:, 2] * f[:, 3])]; return rec.feature(rec.alignCrop(img, f))
sim = lambda a, b: float(rec.match(a, b, cv2.FaceRecognizerSF_FR_COSINE))
A3 = emb(cv2.imread(H + "../louis_card/A3_white_wig.jpg")); ANCHOR = emb(cv2.imread(H + "pilot_frames/owner_best_last_frame.jpg"))
for c in sys.argv[1:]:
    d = "/tmp/facegate_" + os.path.basename(c).replace(".mp4", ""); os.makedirs(d, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", c, "-vf", "fps=2", d + "/f_%02d.jpg"], check=True)
    a3, an = [], []
    for fp in sorted(glob.glob(d + "/f_*.jpg")):
        e = emb(cv2.imread(fp))
        if e is not None: a3.append(sim(e, A3)); an.append(sim(e, ANCHOR))
    h = len(a3) // 2
    ok = np.mean(a3) >= 0.60 and min(a3) >= 0.45
    print(f"{os.path.basename(c)}: n={len(a3)} A3 mean {np.mean(a3):.2f} (1st half {np.mean(a3[:h]):.2f}, 2nd {np.mean(a3[h:]):.2f}, min {min(a3):.2f}); anchor mean {np.mean(an):.2f}; {'PASS' if ok else 'FAIL'}")
