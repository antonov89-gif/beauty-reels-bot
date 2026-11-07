"""Builds the Sunburst (non-Lite) variant of the Take 4b v3 piece B END still script (owner 07.11: 'делай сам'): same prompt and refs as the Lite script of the same piece, model gpt-image-2.5-sunburst (measured charge about $0.10 at 4K high), output pilot_frames/anchors/t4bB_end_sunburst_4k.jpg."""
import os, re
H = os.path.dirname(os.path.abspath(__file__)) + "/"
src = open(H + "gen_t4bB_" + "end.py").read()
s = src.replace('"model": "gpt-image-2.5-sunburst-lite"', '"model": "gpt-image-2.5-sunburst"')
s = s.replace("t4bB_end_prompt.txt", "t4bB_end_sunburst_prompt.txt").replace("pilot_frames/anchors/t4bB_end_4k.jpg", "pilot_frames/anchors/t4bB_end_sunburst_4k.jpg")
i = s.index('"""', 3)
brief = re.search(r"BRIEF:\s*(\S+)", src).group(1)
doc = ('"""Take 4b v3 piece B END still on gpt-image-2.5-sunburst (non-Lite; owner 07.11: делай сам): an EDIT of the end still of piece A (refs: t4bA_end_4k.jpg to edit, K4 master O8 for the king, R8 for Marcel), 4K high 9:16, about $0.10. '
       'Result: pilot_frames/anchors/t4bB_end_sunburst_4k.jpg. Run: python3 gen_t4bB_end_sunburst.py go\nBRIEF: ' + brief + '\n"""')
open(H + "gen_t4bB_end_" + "sunburst.py", "w").write(doc + s[i + 3:])
print("built", "gpt-image-2.5-sunburst\"" in s, brief)
