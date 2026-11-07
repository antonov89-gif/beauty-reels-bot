# Pre-generation review: Take 4b v3 (pieces A and B), 07.11.2026

## VERDICT
- gen_t4bA_start.py: FAIL (content fixes needed; mechanical preflight PASS; reviewer-pass NOT recorded).
- gen_t4bA_end.py: FAIL (fixes below; missing-ref preflight FAIL is expected, text reviewed in full).
- gen_take_t4bA.py: FAIL (fixes below).
- gen_t4bB_end.py: PASS with 2 small fixes recommended (apply before showing).
- gen_take_t4bB.py: FAIL (fixes below).

## Refs of the START still (opened at full size)
1. K4_master_neutral_O8.png 941x1672 (best original, sharp 992, detail 6.0, blocks 1.03): sharp frontal, heavy lids, mark on the viewer's right. OK.
2. R8_marcel_full.jpg 1536x2752 (sharp 610): full figure, tricorn, daylight hall, wide-eyed mouth-open expression, loose white scarf; prompt rightly says face, wig, coat only. OK.
3. R10_hall_clean.jpg 1686x1920 (sharp 104.6, detail 1.52, blocks 1.29, room limits OK): NOT clean: crystal glasses, chandelier, real faces, a looking-up angle; prompt names the glasses/chandelier/people. OK with the stated ignore.
Order in image_urls = Reference 1/2/3 in the prompt: PASS.

## Checklist, START still (gen_t4bA_start.py)
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle new, hand-held | PASS | S9b side, table height, 40 deg off the table line, roll 6; S9 (across/above) and S10 (selfie) differ; S9b is NOT yet in setup_map_2026-11-05.md: add the row |
| 2 | Emotion per beat | PASS | king impatient smirk, heavy lids; Marcel tense (a still has one beat) |
| 3 | Laugh | N.A. | start still |
| 4 | Lines/pauses | N.A. | stills carry no lines; docstring lines = script 7.3 |
| 5 | Living room | PASS | courtiers, lady with fan back right, servant far behind |
| 6 | Phone mistake | N.A. | still |
| 7 | End pose differs from start, same composition | FAIL | the start king already faces Marcel ("turned toward Marcel") and the end still also has him turned to Marcel: no change of pose, and the clip says he turns to Marcel at 7-10 s. Fix: START king looks to the viewer's LEFT (out at the hall, bored, eyes drifting), head turned about 25-30 deg, both eyes and the mark visible; Marcel stays at the right |
| 8 | Face refs / identity | FAIL (fixable) | order and descriptor block OK (about 45, grey-green, mark on viewer's right, silver-grey wig); but (a) king face centre 28 % with head+wig 52 % wide leaves a 2 % left margin (wig touches the edge, and the clip adds 3-4 % moves); (b) king turned toward the viewer's RIGHT hides/foreshortens the mark (lesson 06.11 says turn toward the viewer's left); (c) faces 26 % / 22 % are under the 28 % rule: accepted by the owner brief (two faces in 9:16), risk stays, eye check decides. Fix: king face centre 30 %, Marcel 76 %, head+wig 50 % and 34 %: king spans 5-55, Marcel 59-93, margins 5-7 %. Drop the duplicated "Reference 1 is the king's master portrait: the king exactly as in reference 1" sentence |
| 9 | Quality | PASS | O8 best original named; preflight metrics OK |
| 10 | Kling tags | N.A. | still |
| 11a | No device words | PASS | words phone/screen/case/device absent; "hand-held" is the only camera word (acceptable, not a selfie; may be dropped); advisory: "no extra fingers" is a negated finger phrase, replace with "five natural fingers on each hand" only |
| 11 | Channel rules | PASS | Louis, no music, no text, one king, no "handsome" line |
| 12 | Motion score | N.A. | still |

## Fixes for the other scripts
gen_t4bA_end.py
- Pose of the king must differ from the start: after the start fix, "turned toward Marcel, blank" is a real change. OK once the start is fixed.
- Add the small gold tray (on the cloth or on the floor, not in Marcel's hands) because it was in the start still.
- Add "no tricorn hat" for Marcel (R8 attached as ref 3) and a short descriptor of the king (silver-grey and white wig, mark on the viewer's right) so the identity does not rest only on "keep the faces".
- Marcel's end: eyes into the lens is good (differs from start: eyes on the goblet).
- Ref order: photo, O8, R8 = Reference 1/2/3: PASS. The start 4K file must exist and pass the quality limits before this runs.

gen_take_t4bA.py
- Typo in the text: "...gold suns) and Marcel (...), and Marcel, filmed by..." duplicated "and Marcel"; remove.
- Conflict: "the heads move about half of their own width in each 2-second window" is impossible with heads 52 % and 35 % wide and 4-6 % margins (it would leave the frame). Replace with "the heads move by turns and nods, 3-5 % of the frame width per 2 s, never leaving the safe area".
- Marcel "does not move" at 7-10 s: give him micro verbs (swallows, eyes drop to the pool, weight shift) so there is no 3 s hold of the body; the silent beat may be still in the face only.
- Camera: horizontal returns are not written for 8-10 s (net drift left 3 %): add "drift right 3 % to land on @last_frame". After the start fix the king moves from looking left to turning to Marcel at 7-10 s: say "the king looks away to the left at 0-2 s, down at the wine at 2-5.5 s, then turns to Marcel at 7-10 s" (a king who already faces Marcel contradicts "turns").
- Add "nothing flies at the camera, no splash upward, the wine never reaches his face or wig" (already half there) and "the king's cuff stained a little".
- Lines: only "Sorry, Sire." at 5.5-7 s: matches script 7.3, order OK (Marcel first). 10 s timing OK (2 words; silent beat 7-10 s). Phone mistakes: blur 3 s (note the goblet fall is at the same moment; move to 4.2 s to be separate), thumb 5.5 s (window 3.5-7.5), caps stated: PASS. Room: 4 named people with seconds: PASS. No "framing stays": PASS. Tags @first_frame/@last_frame match image_urls [start, end]: PASS.

gen_t4bB_end.py (PASS, 2 small fixes)
- End B vs start B (= end A) differ only by chin, brow, faint smile, hands: add a stronger change that costs no motion: Marcel's eyes lowered to the pool/floor and head bowed a little (start: eyes into lens), king's chin lifted and the shoulders back. Say Marcel's eyes direction ("eyes wide" has no direction).
- Add "no tricorn hat" (R8 is ref 3). Order photo, O8, R8 = Reference 1/2/3: PASS.

gen_take_t4bB.py
- Same duplicated "and Marcel" typo and same "half of their own width" conflict as in A.
- Script logic gap: the king starts turned to Marcel (pin), laughs, and at 5.8 s "turns his head to Marcel" again: write that during the laugh (1.5-5.8 s) he tips back and turns his face away to the front/left (toward the lens side), then turns back at 5.8 s.
- "waving two fingers over the pool": finger glitch risk and "two fingers" is a finger object; use "a flat dismissive wave of the hand".
- Laugh drift risk (T4b 06.11: sharpness fell in the laugh): "head tips back only slightly, upper teeth showing, eyes narrowed but the lids stay heavy; face stays the same man".
- Lines exactly script 7.3 in order: PASS ("Nobody saw anything." 4-5.8, "And nobody will see you again." 5.8-8.5, pause 8.5-9.3, "Joking." 9.3-10; "Joking" has 0.7 s, tight but possible: start it at 9.2 s). The silent beat after the gag falls after the clip: leave about 1 s of tail on the final cut (note for the edit).
- Laugh beat: PASS (1.5-4 s). Phone mistake at 6.5 s, blur 3.5 s: PASS. Room: 4 named people: PASS. B first = A end same image, last frame = B end: PASS. Tags and image_urls match.

Spill reading as an accident: PASS in the clip text (goblet tips off the tray, pours, spreads, nothing flies, cuff only, king's face and wig clean). Setup map: add S9b.

## Для владельца: СТАРТОВЫЙ кадр piece A (текущая версия, ревью пройдено 07.11)
Референсы в порядке прикрепления:
1. K4_master_neutral_O8.png, 941x1672, мастер-портрет короля (лучший оригинал, резкость 992).
2. R8_marcel_full.jpg, 1536x2752, Марсель (только лицо, парик, голубой ливрейный камзол; без треуголки, позы и фона карточки).
3. R10_hall_clean.jpg, 1686x1920, только зал (бокалы, люстру и людей игнорировать).

Полный промпт по частям:
- Общее: вертикальное фото 9:16, тусклый свет свечей, слегка недоэкспонировано, мелкое плёночное зерно, реальная кожа, без бьюти-фильтра.
- Референс 1 это мастер-портрет короля: тот же мужчина около 45 лет, тяжёлые веки, серо-зелёные глаза, тонкие тёмные навощённые усы с загнутыми кончиками, маленькая тёмная родинка хорошо видна справа от рта (справа от зрителя), лёгкие румяна, высокий напудренный парик серебристо-серый с белым (в свете чуть теплее или холоднее), алый бархатный камзол с золотыми солнцами, кружевное жабо; не копировать нейтральную позу и фон.
- Референс 2 это Марсель: лицо, белый парик, бледно-голубой ливрейный камзол с серебряным шитьём и белое жабо (без треуголки, без позы в полный рост и фона карточки); молодой слуга с веснушками и густыми тёмными бровями.
- Референс 3 показывает только зал: игнорировать его ракурс, не копировать хрустальные бокалы, люстру и людей за столом (люди новые).
- Камера: с рук, на высоте стола, сбоку длинного стола, около 40 градусов от линии стола, средне-широкий план, крен около 6 градусов вправо. Король сидит в ЛЕВОЙ части кадра (голова с париком около 50 % ширины, лицо около 26 %, центр лица на 30 % ширины, резкий), голова повёрнута на 25-30 градусов к ЛЕВОЙ стороне зрителя, смотрит в сторону со скукой, оба глаза и родинка справа от рта видны. Марсель стоит ПРАВЕЕ (голова с белым париком около 34 % ширины, лицо около 22 %, центр лица на 76 % ширины, резкий), повёрнут на три четверти к левой стороне зрителя, к королю. Обе головы целиком в кадре с париками, свободные поля около 5 % с каждого края.
- Между ними и ниже: белая скатерть, золотая тарелка и свечи, чисто, без пятен.
- Поза и эмоция: король ждёт и скучающе смотрит в сторону, тяжёлые веки, лёгкая усмешка нетерпения, пальцы с перстнями барабанят по скатерти (пять естественных пальцев). Марсель слегка склонился над столом, напряжён, чуть потеет, смотрит на золотой кубок с красным вином на маленьком золотом подносе в обеих руках (по пять естественных пальцев на каждой), кубок металлический, не стеклянный.
- Позади, размыто: освещённый свечами позолоченный зал, стоящие придворные в простых париках, справа сзади дама с раскрытым веером, далеко сзади слуга в ливрее.
- Запреты: без текста, логотипов, современных предметов, без стекла и хрусталя, без клоунского грима, только один король.

Модель: GPT Image 2.5 Sunburst Lite, 4K, качество high, 9:16, один вызов, около $0.12. Запуск только после твоего "да" после показа.
