"""Self-check of a rendered loop: frame count/fps/duration, loop seam (last->first frame vs normal frame steps), largest frame jump,
loudness (EBU R128 integrated + true peak), audio seam (sample jump at the wrap) and music bed presence. Prints one JSON line.
Usage: python3 qc_loop.py <final.mp4>"""
import json
import re
import subprocess
import sys

import numpy as np

v = sys.argv[1]
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_streams", "-show_format", v], capture_output=True, text=True).stdout)
vs = next(s for s in pr["streams"] if s["codec_type"] == "video")
w, h = 270, 480
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)
steps = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
seam = float(np.abs(fr[0] - fr[-1]).mean())
near = float(np.median(np.concatenate([steps[:5], steps[-5:]])))

pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-f", "f32le", "-ac", "1", "-ar", "44100", "-"], capture_output=True).stdout
a = np.frombuffer(pcm, np.float32)
typ = float(np.median(np.abs(np.diff(a))))
wrap = float(abs(a[0] - a[-1]))
eb = subprocess.run(["ffmpeg", "-hide_banner", "-i", v, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", eb)[-1])
TP = float(re.findall(r"Peak:\s+(-?[0-9.]+) dBFS", eb)[-1])
rms_s = [float(20 * np.log10(np.sqrt(np.mean(a[i:i + 44100] ** 2)) + 1e-9)) for i in range(0, len(a) - 44100 + 1, 44100)]

out = dict(file=v.split("/")[-1], frames=len(fr), fps=vs["r_frame_rate"], dur=round(float(pr["format"]["duration"]), 3), size=f'{vs["width"]}x{vs["height"]}',
           seam_diff=round(seam, 2), step_near_seam=round(near, 2), seam_ok=seam <= max(2.5 * near, 1.5),
           max_step=round(float(steps.max()), 2), max_step_at_s=round(float(np.argmax(steps) + 1) / 30, 2), median_step=round(float(np.median(steps)), 2),
           lufs=I, true_peak=TP, loud_ok=(-15.5 <= I <= -12.5 and TP <= -1.0),
           audio_wrap_jump=round(wrap, 4), audio_typ_step=round(typ, 4), audio_seam_ok=wrap <= max(10 * typ, 0.02),
           rms_per_s_db=[round(x, 1) for x in rms_s])
print(json.dumps(out))
