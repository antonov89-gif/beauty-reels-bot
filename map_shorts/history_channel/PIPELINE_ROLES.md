# WHO DOES WHAT (owner 07.11: "промпт должны делать на основании референса, движения, камеры... Делай предупреждение, кто делает референсы и кто делает промпты")
WARNING: a generation prompt is NOT written from the producer's imagination. The order is fixed; skipping a step = the prompt is not shown and not sent.

| Step | Who | Output |
|--|--|--|
| 1. Reference brief (motion, camera, emotion, gesture, gaze, pauses of the matching beat of Vlog 1) | **reference-comparator, BRIEF MODE** (analyst of the reference; looks at the real frames of /tmp/ref1/ref.mov, never invents) | louis_ep2/briefs/brief_<piece>.md: per beat with seconds: camera move in % of width and direction, body/head motion, gesture, facial expression, gaze target, pause length, phone mistakes, room events; each line marked ON FRAMES or HYPOTHESIS |
| 2. Identity references (the face must not change) | **character-card-specialist** (card/refs, face rules) + the owner's portrait set (K4_*) | which refs, in which order, descriptor block, face size vs wig |
| 3. Prompt writing (still start, still end, clip) | **the prompt writer = the main session**, ONLY from the brief (step 1) and the identity recipe (step 2), the script lines and the setup map; every prompt cites its brief file and its numbers | gen_*.py + the English prompt |
| 4. Prompt review before generation | **pregen-reviewer** (item 13: conforms to the brief; item 12: motion score; item 2/3: emotion) | PASS/FAIL, Russian block for the owner |
| 5. The owner's "да" after she has seen the refs and the Russian prompt | the owner | recorded in the preflight |
| 6. Generation | the main session (APIpod) or the owner by hand | still / clip |
| 7. Inspection of the result (defects, identity, quality) | **clip-inspector** (still mode / clip mode) | ACCEPTED / BRAK |
| 8. Comparison with the reference (motion + emotions + gestures + verbal/non-verbal) | **reference-comparator** (compare mode) | table reference / ours |
| 9. Viewer's opinion (rough cuts) | **viewer** | score and ideas |
| Costs and models | **model-economist** | cheapest route that holds the gates |

Rules: (a) the producer never judges its own result, steps 7 and 8 are done by agents before the owner sees the image or clip; (b) the brief is written BEFORE the prompt; a prompt without a brief file is FAIL at step 4; (c) a flat or blank face where the script has a reaction or a gag is a defect; (d) emotions, gaze and gestures are written per beat with seconds, taken from the brief.
