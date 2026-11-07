"""Builds the Seedance 2.5 STANDARD (non-Lite) variant of a clip script from its Lite variant (owner 07.11: 'модель выбери сидкнс 2.5 стандарт').
Usage: python3 build_seedance_std.py t4bB
Model seedance-2.5-i2v (APIpod spec seedance--2-5-image-to-video): image_urls[0] first frame, [1] last-frame constraint, 480p/720p, 4-30 s, NO aspect_ratio parameter (the output follows the first image), 720p = $0.2205 per second (MODEL_NOTES.md, measured earlier; the estimator ignores duration and resolution)."""
import os, re, sys
H = os.path.dirname(os.path.abspath(__file__)) + "/"
key = sys.argv[1]
src = open(H + "gen_take_%s_seedance.py" % key).read()
s = src.replace('"model": "seedance-2.5-lite-i2v"', '"model": "seedance-2.5-i2v"')
s = s.replace(', "aspect_ratio": "9:16"', "")
s = s.replace("_seedance_prompt.txt", "_seedance_std_prompt.txt").replace("_seedance.task_id", "_seedance_std.task_id").replace("_seedance.status.json", "_seedance_std.status.json").replace("_seedance.mp4", "_seedance_std.mp4")
sec = int(re.search(r'"duration":\s*(\d+)', s).group(1))
brief = re.search(r"BRIEF:\s*(\S+)", src).group(1)
i = s.index('"""', 3)
doc = ('"""Take %s CLIP on Seedance 2.5 STANDARD i2v (owner 07.11: seedance 2.5 standard): image_urls[0] first frame, [1] last-frame constraint, 720p, %d s, $0.2205/s = $%.2f, audio off, no aspect_ratio parameter (the output follows the first image). '
       'Same prompt as the Lite script. One call, no retries without a new yes. Run: python3 gen_take_%s_seedance_std.py go\nBRIEF: %s\n"""') % (key, sec, 0.2205 * sec, key, brief)
open(H + "gen_take_%s_seedance_std.py" % key, "w").write(doc + s[i + 3:])
print("built", sec, "s", "$%.2f" % (0.2205 * sec))
