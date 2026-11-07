"""Builds the one-image TEST script of the Take 4b v3 piece A start still on gpt-image-2.5-sunburst (owner 07.11) from the Lite script of the same piece."""
import os
H = os.path.dirname(os.path.abspath(__file__)) + "/"
s = open(H + "gen_t4bA_start.py").read()
s = s.replace('"model": "gpt-image-2.5-sunburst-lite"', '"model": "gpt-image-2.5-sunburst"')
s = s.replace("t4bA_start_prompt.txt", "t4bA_start_sunburst_prompt.txt").replace("pilot_frames/anchors/t4bA_start_4k.jpg", "pilot_frames/anchors/t4bA_start_sunburst_4k.jpg")
i = s.index('"""', 3)
doc = '"""TEST on the non-Lite model gpt-image-2.5-sunburst (owner 07.11: gpt-image-2.5-sunburst): the same prompt and refs as the Lite script (v3, positive-only wording), 4K high 9:16; the estimator shows $0.50 pre-deduct (real charge NOT KNOWN, at most $0.50). Result: pilot_frames/anchors/t4bA_start_sunburst_4k.jpg. Run: python3 gen_t4bA_start_sunburst.py go\nBRIEF: briefs/brief_t4b_A_B.md\n"""'
open(H + "gen_t4bA_start_" + "sunburst.py", "w").write(doc + s[i + 3:])
print("built", 'gpt-image-2.5-sunburst"' in s)
