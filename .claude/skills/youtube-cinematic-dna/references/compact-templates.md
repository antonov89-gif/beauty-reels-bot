# Compact handoff templates — evidence, provenance, deltas, iteration

## One-screen STATE capsule (<=350 words; versioned)
```
PROJECT_ID: YT-DNA-001   MODE: SMART
REFERENCE: url/file | media access L0-L4 | duration when verified
COVERAGE: AV ranges / sampled ranges / unseen ranges
EVIDENCE_INDEX: REF-E01.. | last audited range | source/as-of for metrics
TOP_DNA: DNA-01..07 with claim IDs and confidence
STYLE_BIBLE: SB-v1 (camera/light/color/motion/edit/audio in one compact blob)
SCENE_LOCKS: SC01-v1 ... | characters, objects, location, weather, lighting, voice
ORIGINAL_STORY: premise + story beat IDs
SHOT_PLAN: shot ID → intended beat/camera delta + DNA principle
ARTIFACTS: real generated ID/path ONLY, attempt and review status
QC_OPEN: issue IDs + priority + planned fixes
APPROVED: inspected approved shot IDs/sequence IDs
NEXT_ACTION: single highest-value concrete next action
BLOCKERS: inaccessible source, missing tool, failed attempts, etc.
```

## SOURCE + COVERAGE
```
SOURCE_ACCESS: L3 (actual decoded video+audio in inspected ranges)
INSPECTED_AV: 00:00–00:15 continuous, 01:15–01:30 continuous
SAMPLED_VIDEO: 00:15–01:15 1 fps
UNSEEN: 01:30–02:10
EXTERNAL_METRICS: vidIQ/public data as of YYYY-MM-DD (or NOT_CHECKED)
```

## Reference evidence + claim, minimal
```
REF-E08 | video+audio | 00:07.2–00:08.6 | 8fps inspected excerpt
OBS: subject begins movement, camera follows laterally, hard cut on sound.
CL-08 | OBSERVED | REF-E08 | medium confidence: lateral movement and cut.
CL-09 | ESTIMATED | REF-E08 | low confidence: likely ~35mm perspective.
DNA-03 | refs CL-08,CL-09 | delayed follow-cam with offscreen cue.
```

## SHOT MAP (reference)
|ID|Time|Beat|Frame|Blocking|Camera|Light|Audio/cut|Evidence|
|--|--|--|--|--|--|--|--|--|
|R-03|00:07.2–00:08.6|reveal|medium-wide|subject L→C|lateral follow|right practical|hard cut on sound|REF-E08|

## Global STYLE_BIBLE, only one version
```
SB-v1: 16:9; color [neutral shadow + warm practical]; lens impression wide/normal;
shot rhythm [wide→reaction→detail as motivated]; camera [grounded tracking,
no unmotivated orbit]; blocking [subject drives path]; light [physically
motivated]; voice [natural performance]; sound [space-specific ambience];
no visible temporal morphing. These are project choices unless evidence-tagged.
```

## SCENE LOCK (inherit STYLE_BIBLE)
```
SC-02-v1 | PLACE/TIME/WEATHER | people/outfits/props/vehicles | geography
LIGHT SOURCE/DIRECTION | acoustic space | character voice | intended emotion
```

## SHOT DELTA (inherits SB + SCENE)
```
SHOT: S02-04 | BEAT: new original story beat B-06 | DNA: DNA-03
DURATION: 3.5s target | BLOCKING: start→physical action→end
CAMERA: physical rig + starting position→trajectory/inertia→end composition
FRAME: size/height/lens impression/focus | MOTION: subject/FG/BG
AUDIO: dialogue/Foley/ambience/music cue | CUT: motivated handoff
METHOD: 3D / stock / I2V / T2V / live footage / compositing
START/END FRAME: controlled description | RISK + ACCEPTANCE GATE
```

## One-round QC delta
|Shot+attempt|Artifact|Inspected range|Evidence|Severity + fault|Cheapest viable action|Decision|
|--|--|--|--|--|--|--|
|S02-04 a1|real URI/path|00:02.0–00:03.1|OUT-E07|HIGH: wheel steering glitch|regenerate final segment|FIX_REQUIRED|

## Tool-result honesty markers
`NOT_OBSERVED` ≠ `PASSES`; `PROMPT_WRITTEN` ≠ `GENERATED`; `GENERATED` ≠ `INSPECTED`; `FIX_SUGGESTED` ≠ `FIX_APPLIED`; `INSPECTED` ≠ `APPROVED`; `SAMPLE_PASS` ≠ `FULL_FILM_PASS`.

## FULL output only on explicit demand
Deliver: source/coverage ledger, detailed shot map, expanded cinematography and sound, confidence and performance cross-check, style bible, original narrative, beat-to-DNA map, exact production spec, asset strategy, pilot attempts, fault ledger, approved assets and unresolved work. Label unperformed steps clearly.
