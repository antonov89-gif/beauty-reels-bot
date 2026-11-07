"""Repoints the BRIEF: marker of the t5a..t7b scripts to the combined brief briefs/brief_t5_t7.md (07.11), and builds the Sunburst (non-Lite) variant of the t5a start still (non-Lite measured sharper, about $0.10 at 4K high)."""
import os, re, glob
H = os.path.dirname(os.path.abspath(__file__)) + "/"
n = 0
for f in glob.glob(H + "gen_" + "*.py"):
    b = os.path.basename(f)
    if not re.match(r"gen_(take_)?t(5a|5b|5c|6|7a|7b)(_start|_end)?\.py$", b):
        continue
    s = open(f).read()
    t = re.sub(r"BRIEF:\s*briefs/brief_t[5-7][abc]?\.md", "BRIEF: briefs/brief_t5_t7.md", s)
    if t != s:
        open(f, "w").write(t); n += 1
print("repointed", n)
src = open(H + "gen_t5a_" + "start.py").read()
s = src.replace('"model": "gpt-image-2.5-sunburst-lite"', '"model": "gpt-image-2.5-sunburst"')
s = s.replace("t5a_start_prompt.txt", "t5a_start_sunburst_prompt.txt").replace("pilot_frames/anchors/t5a_start_4k.jpg", "pilot_frames/anchors/t5a_start_sunburst_4k.jpg")
i = s.index('"""', 3)
doc = ('"""Take 5 piece 5a START still on gpt-image-2.5-sunburst (non-Lite), 4K high 9:16, about $0.10. Same prompt and refs as the Lite script (K4 master O8, angle low O12, hall R10). '
       'Result: pilot_frames/anchors/t5a_start_sunburst_4k.jpg. Run: python3 gen_t5a_start_sunburst.py go\nBRIEF: briefs/brief_t5_t7.md\n"""')
open(H + "gen_t5a_start_" + "sunburst.py", "w").write(doc + s[i + 3:])
print("built", 'gpt-image-2.5-sunburst"' in s)
