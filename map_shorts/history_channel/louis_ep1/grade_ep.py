"""Picture grade for the history channel (compare_reference_ep1_v2.md item 2): the reference is darker, more textured and less golden.
gamma 0.86 (about -0.35 EV in the mids), contrast +6 %, saturation -20 %, yellows -25 %, texture sharpen, fine temporal grain (stronger in luma).
Measured on C02: brightness 116 -> 100 (reference 86), texture (Laplacian) 887 -> 1334 (reference 2360), grain 2.38 -> 2.69 (reference 2.81).
24 fps kept: 30-fps motion interpolation was tested on C06 and doubles objects on fast moves (rejected).
Usage: python3 grade_ep.py -> frames/<clip>_v5.mp4 and frames/EP1_C01-C08_v5.mp4 from frames/<clip>_snd.mp4"""
import subprocess
GRADE = "eq=gamma=0.86:contrast=1.06:saturation=0.80,huesaturation=colors=y:saturation=-0.25,unsharp=5:5:0.85:5:5:0,noise=c0s=9:c0f=t+u:c1s=3:c1f=t+u:c2s=3:c2f=t+u"
CLIPS = ["C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08"]
for c in CLIPS:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f"frames/{c}_snd.mp4", "-vf", GRADE, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "copy", f"frames/{c}_v5.mp4"], check=True)
ins = sum([["-i", f"frames/{c}_v5.mp4"] for c in CLIPS], [])
fc = "".join(f"[{i}:v]setsar=1[v{i}];" for i in range(len(CLIPS))) + "".join(f"[v{i}][{i}:a]" for i in range(len(CLIPS))) + f"concat=n={len(CLIPS)}:v=1:a=1[v][a]"
subprocess.run(["ffmpeg", "-y", "-v", "error"] + ins + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "320k", "frames/EP1_C01-C08_v5.mp4"], check=True)
