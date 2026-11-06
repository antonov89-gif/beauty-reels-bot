# Pre-generation review: piece t7a (Take 7a "what else to show you / Probably nothing", setup S16), 06.11.2026
Scripts: gen_t7a_start.py, gen_t7a_end.py, gen_take_t7a.py. Reviewer pass NOT recorded (as asked).
Preflight on the start script: mechanical PASS (R1 768x1376 below 1024 but the best existing original, named; quality sharp 940 / detail 6.59 / blocks 0.99; R10_hall_clean 1686x1920, sharp 104.6 / detail 1.52 / blocks 1.29, room limits 1.30 = passes with ZERO margin). End and clip scripts: missing-file FAIL expected, not counted.
Both reference images opened at full size: R1 = sharp, no seam, no text, front selfie with the hand at the wig (a pose, must not be copied); R10 = clean hall crop but it contains a chandelier (top right), crystal glasses on the table and seated ladies seen from behind (the prompts already forbid chandelier/glasses).

## VERDICT: FAIL for all three scripts (fixable, 3-5 small edits each, no structural redesign)
- start: FAIL (geometry words contradict each other; face 40 % width cannot leave room for the hall; "do not copy its people" vs "ladies at the table")
- end: FAIL (no heavy-lid / no wide-eyes clause; the pose "has just said probably nothing, laughing" is in the wrong order vs the script)
- clip: FAIL (item 12 numbers do not fit the frame; head-score inconsistent; speech slot too short; no silent beat after the last line)

## Is S16 a really new angle? YES, with two provisos
| vs | S16 | difference |
|--|--|--|
| S9 (across the table, from above ~20 deg, king in right third 45 %, roll 8 right) | below eye level, arm's length, king left of centre (42 %), hall on the right | opposite vertical angle, opposite side of frame, not across a table: new |
| S10a (selfie from above, face ~58-60 %, dutch) | below, wide, face 40 % | opposite vertical angle and scale: new |
| S11 (low, over shoulder / along the table, filmed by Marcel, NOT made yet) | his own arm, he sits back, the hall behind him | both are "low": must stay distinguishable. S11 = along the table with food in front; S16 = near the face with the hall to one side. Keep the table out of S16 |
| S12 (from above, leaning back, A7; NOT made yet) | from below, leaning back | same body pose family (leaning back), opposite vertical angle; make the S12 still carry a different head turn |
| S13 (frontal, eye level, close, push-in; NOT made yet) | three-quarter, below, wide | new |
Closest sibling NOT in the list: S5 (side-on three-quarter, camera on the king's right, eye level, close medium, T2c). S16 differs from S5 by below-eye-level, wider lens with the hall visible, leaning back, but the head turn is the same family: keep the vertical angle and the wide hall as the visible difference, and do not use T2c as any reference.
Provisos: (1) S16 is not in setup_map_2026-11-05.md: add the row (Take 7a, S16, "arm's length, a little below eye level, three-quarter, wide hall to one side", A3 + R10). (2) S11 and S12 stills do not exist yet, so "new" is checked on the written prompts only; compare the real stills when they exist.

## Checklist: START script (gen_t7a_start.py)
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle new, hand-held, never static | FAIL (words) | New vs S9/S10a/S11/S12/S13 (above). But "camera held ... below his eye level and to his LEFT" + "turned three-quarter toward the viewer's RIGHT" are not one geometry (a camera at his left sees his face turned to the viewer's left); the model will pick one at random (the S5 flip in T2c). Also wig missing from the width sentence: A3 shows head with wig about 2x the face width, so "face fills 40 %, centre 42 %" means the wig spans about 0-85 % and the "wide view of the hall to the right" gets about 15 % of the frame |
| 2 | Emotion per beat, heavy lids, no wide eyes | PASS | start beat only: thoughtful, "heavy-lidded", lips pursed, no wide eyes |
| 3 | Laugh / human moment | N.A. (start) | the laugh is in the end still and the clip |
| 4 | Pauses, lines exact | N.A. (still) | no lines in a still |
| 5 | Living room | PASS | fan lady back right, servant far behind, standing courtiers, ladies; "do NOT copy ... the people at its table" and "ladies at the sides of the table" contradict: say "new people, not those of Reference 2" |
| 6 | Phone mistake | N.A. (still) | belongs to the clip |
| 7 | End pose differs, same composition | N.A. (start) | checked at the end script |
| 8 | Face references | PASS with note | A3 + R10 hall_clean (no angle tile by design, angle in words). R10 still has chandelier/glasses/seated ladies; prompt forbids them (worked on T4a/T4b). Beauty mark is on the viewer's right = the FAR cheek when the nose turns to the viewer's right: write "the mark stays clearly visible, not hidden by the nose" (already says "clearly visible", keep it and add the turn angle ~30 deg, not 45+) |
| 9 | Quality | PASS | sources are originals; R1 768 px is the best original (named), R10 1686x1920 native; R10 blocks 1.29 vs 1.30 = tight but allowed |
| 10 | Kling tags | N.A. | image prompt |
| 11 | Channel rules | PASS | Louis XIV, no text, one king, no "handsome" line; AI disclosure N.A. at piece level |
| 12 | Motion score | N.A. | still |

## Checklist: END script (gen_t7a_end.py)
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle | PASS | "EXACTLY the same camera, angle, roll, framing, crop, head size/position (centre 42 %)" |
| 2 | Emotion, heavy lids | FAIL | the end laugh may show teeth (laugh beat), but there is no "heavy lids stay half-lowered, no wide-open eyes" clause; "one eyebrow raised" + "eyes back on the lens" invites wide eyes |
| 3 | Laugh | PASS | short dry laugh, mouth slightly open, teeth just visible |
| 4 | Lines/pauses | N.A. (still); note | the pose says "he has just said 'probably nothing' and is giving a short dry laugh". In script 7.3 the laugh COMES BEFORE the line ("Ha. Probably... nothing."). Make the end pin the AFTERMATH: dry smirk, lips closed or just parted, eyes on the lens, one brow up |
| 5 | Living room | PASS | "the hall with the people" kept; people may shift: add "the courtiers and the fan lady may have moved a little (fan closed)" so the last pin matches the clip's 4 s fan event |
| 6 | Phone mistake | N.A. | still |
| 7 | End pose differs, same composition | PASS | start: chin up, eyes away right, lips pursed; end: eyes on lens, smirk, head tipped a few degrees to the viewer's left; head/wig/face centre within 3 % |
| 8 | Face refs | PASS | edit of the start still (the 4K original); same pattern as T3d/T4b end edits |
| 9 | Quality | PASS | quality sentence present; source = the 4K start still; NOTE the start script saves to pilot_frames/anchors/t7a_start_4k.jpg but this script reads RAW .../refs/t7a_start_4k.jpg: copy it to refs/ and push before the call (same for t7a_end_4k.jpg for the clip) |
| 10 | Kling | N.A. | image edit |
| 11 | Channel rules | PASS | no text, no modern objects, one king, no "handsome" |
| 12 | Motion score | N.A. | still |

## Checklist: CLIP script (gen_take_t7a.py), Kling 4.0 i2v 720p 10 s = $1.45
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle new, hand-held | PASS | "his own hand-held phone held below eye level", no gimbal/dolly, every move by hand |
| 2 | Emotion per beat | PASS | thoughtful (0-2.5) -> frown/tilt (2.5-5.5) -> mouth corners rise (5.5-7) -> laugh (7-8.5) -> shrug (8.5-10); "heavy eyelids stay except in the laugh beats, no wide-open eyes" present |
| 3 | Laugh | PASS | 7-8.5 s "Ha." with a shoulder shake |
| 4 | Pauses, lines exact | FAIL (partly) | lines are EXACTLY script 7.3 ("So... I was wondering what else to show you here." / "Ha." / "Probably... nothing."); 1.5 s silent beat 5.5-7 s before the laugh = the script's [pause]. But (a) 10 words in 2.5-5.5 s = 3.3 words/s, above the 2.5-3.1 gate: widen to 2.5-6.0 s; (b) there is no silent beat AFTER the last line (it ends on "nothing" at 10 s on the laugh pin): add 9.3-10 s silent settle, smirk, eyes on the lens, hall murmur only; (c) the last pin must be the smirk aftermath, not mid-laugh (see end script) |
| 5 | Living room | PASS | servant crosses at 1 s, courtier right edge turns at 3 s, fan lady closes the fan at 4 s, courtier shifts weight at 7 s, candles flicker. Note: the servant crosses from LEFT (the side that stayed quiet in T4a); make him cross right to left or keep him as a bonus event |
| 6 | Phone mistake | PASS | lens tilts to the ceiling ~5 s (window 3-7), pink thumb lower-left ~8.5 s, 20 % cap (never above 25 %), never the face; neither is on the pins |
| 7 | End differs, same composition | PASS | start: chin up, gaze away right; end: eyes on lens, dry laugh; "the king and the room are in the same place in both frames" (not a "framing stays" sentence) |
| 8 | Face refs | N.A. | the clip uses the two stills only; face from the start still (as T3d/T4a) |
| 9 | Quality | PENDING | depends on the new stills: gate each at full size (sharp >= 150, detail >= 2.0, blocks <= 1.2, head area loss <= 30 % at 720p) before the call |
| 10 | Kling tags | PASS | @first_frame and @last_frame named in the prompt; image_urls = [start, end], same order as other clips; no @keyframe_N used, none promised. Duration 10 s for 13 words = 78 wpm incl. pauses: fits |
| 11 | Channel rules | PASS | Louis XIV, no music, no text, one king, no "handsome". AI disclosure: not in a piece, N.A. |
| 12 | Motion score | FAIL (numbers) | Camera per window with seconds: present. Pose verbs: present. Room: 4 timed events. Phone mistakes: seconds + caps. No "framing stays the same". BUT: (a) the claim "face 40 % wide, free margin about 30 % on each side" is wrong: face spans 22-62 %, and the wig is about twice as wide as the face, so a 10 % horizontal swing can cut the wig (T4b/T4a lesson: keep-in-frame clause only works with correct numbers); fix by stating the head-with-wig width and capping horizontal swings at about 6 % OR using the vertical/push-pull moves for the other half; (b) "head moves about half its width (about 15 % of the frame width)": half of a 40 % face = 20 %; align the numbers; (c) the 4-6 s sag + the ceiling tilt + the 2.5-5.5 s speech overlap three moves: acceptable, but give the ceiling tilt one slot (5.0 +-1) and say the face returns to the frame at once |

## What to fix (concrete)
START
1. One geometry in words: "the phone is held in front of him, a little below his chin line and slightly to HIS RIGHT (we see more of his right cheek); his head is turned about 30 degrees toward the viewer's right, his gaze goes past the lens to the right; beauty mark on the viewer's right of the mouth stays clearly visible." Delete "to his left".
2. Replace "face fills about 40 percent of the frame width" by "head with the wig fills about 60 percent of the frame width, face centre at 40 percent; the right 35 percent of the frame shows the hall" (A3 wig is about twice the face width), and keep the same numbers in the end and clip texts.
3. Replace "do NOT copy ... the people at its table" by "new people, not the ones of Reference 2; no glasses, no chandelier".
4. Add S16 to setup_map_2026-11-05.md.
END
5. Add: "heavy lids stay half-lowered, eyes NOT wide, the eyebrow lifts only a little".
6. Make the pose the aftermath of the line: dry smirk, lips closed or just parted, eyes on the lens, head tipped a few degrees to the viewer's left, fan lady's fan closed.
7. Copy t7a_start_4k.jpg to refs/ and push before running (RAW path).
CLIP
8. Correct the margin sentence (see 12a), cap horizontal swings (10 % -> about 6 %) and align the head-travel number (half of the face = 20 % of the width, or say 15 % and call it "a third").
9. Speech slot: "So... I was wondering what else to show you here." 2.5-6.0 s; silent beat 6.0-7.0; "Ha." 7.0-8.0; "Probably... nothing." 8.0-9.3; 9.3-10 s silent settle (smirk, eyes on the lens, hall murmur).
10. Last pin text in the clip = the aftermath smirk (same as the fixed end still); thumb moved to about 7.5-8 s so it does not hide the laugh.
11. The servant crosses right to left (or add a second room event on the right: a lady behind the table leans to her neighbour at 6 s).

## Для владельца:
Референсы по порядку подачи.
Старт-кадр (gen_t7a_start.py, GPT Image 2.5 Sunburst Lite, 4K, 9:16, high, около 0,12 доллара):
1. R1_king_card_A3_white_wig.jpg: лицо и костюм короля (карточка A3), 768x1376, меньше 1024, но это лучший существующий оригинал; чёткость 940, детали 6,59. Поза с рукой у парика не копируется.
2. R10_hall_clean.jpg: только зал, 1686x1920 (чёткость 105, детали 1,52, блоки 1,29: на пределе, но проходит). Хрустальные бокалы, люстра и сидящие дамы из референса не копируются.
Конец (gen_t7a_end.py, правка старт-кадра, 4K, около 0,12 доллара): один референс, будущий t7a_start_4k.jpg (оригинал 4K, пока не создан).
Клип (gen_take_t7a.py, Kling 4.0 i2v, 720p, 10 секунд, 0,145 x 10 = 1,45 доллара): @first_frame = t7a_start_4k.jpg, @last_frame = t7a_end_4k.jpg (обоих пока нет).

Проверка по пунктам (то, что названо владельцу): 1 ракурс S16 новый (снизу, на вытянутой руке, зал сбоку; S9 был сверху через стол, S10a селфи сверху, S12 сверху, S13 фронтально; ближайший родственник S5 по повороту головы, но у него уровень глаз и без зала); 2 эмоции по долям: задумчив, хмурится, уголки губ, смех, пожатие плеч; тяжёлые веки; 3 смех на 7-8,5 с; 4 реплики точь-в-точь по сценарию 7.3, пауза 1,5 с перед смехом; 5 живой зал: слуга, придворный справа, дама с веером, придворный; 6 ошибки телефона: взгляд в потолок около 5 с, палец около 8,5 с; 7 конечная поза отличается при той же композиции; 8 лицо: карточка A3 плюс зал; 9 качество: оригиналы; 10 теги @first_frame/@last_frame совпадают; 11 правила канала соблюдены. Замечания (вердикт: ПЕРЕДЕЛАТЬ ПРОМПТЫ) перечислены выше в разделе "What to fix".

### 1) Промпт старт-кадра (по-русски, как он должен быть после исправлений; исходный смысл сохранён)
Вертикальная реальная фотография 9:16 при свечах, чуть недоэкспонированная, мелкое плёночное зерно, настоящая кожа, без бьюти-фильтра.
Референс 1 — лицо и костюм короля: тот же человек, тот же возраст, тяжёлые веки, тонкие тёмные навощённые усы с загнутыми кончиками, маленькая тёмная родинка справа от рта (справа от зрителя), лёгкие румяна, высокий напудренный парик холодного серебристо-серого и белого цвета (НЕ бежевый, НЕ кремовый, НЕ золотистый), алый бархатный камзол с золотыми солнцами, кружевное жабо; позу и фон не копировать.
Референс 2 — только зал: угол не копировать; хрустальные бокалы и людей за его столом не копировать.
Камера: ручная, на вытянутой руке, чуть НИЖЕ уровня его глаз, широкий объектив, чтобы виден был зал; (по замечанию ревьюера: голова с париком занимает около 60 процентов ширины кадра, центр лица на 40 процентах, справа около трети кадра занимает зал; камера перед ним и чуть справа от него, голова повёрнута на 30 градусов к правой стороне зрителя); справа от него широкий вид на освещённый свечами золочёный зал: стоящие придворные в простых париках, дамы в широких платьях по бокам стола, в глубине справа дама с раскрытым веером, далеко позади слуга в ливрее, полоска золочёного потолка у верхнего края; без люстры; наклон около 5 градусов вправо.
Поза и эмоция: он откинулся в кресле, подбородок поднят, задумчив, тяжёлые веки, взгляд вверх и в сторону, вправо, на зал, как будто ищет идею; губы сомкнуты и чуть поджаты; одна рука лежит на подлокотнике у нижнего края.
Без текста, логотипов, современных предметов, без стекла и хрусталя, без лишних пальцев, без клоунского грима, только один король.

### 2) Промпт конечного кадра (правка старт-кадра)
Отредактируй фото: та же позиция камеры, тот же ракурс, наклон, кадр и обрезка, тот же размер и положение головы (центр лица на 40-42 процентах ширины), тот же парик, камзол и зал с людьми. Лицо, возраст, кожа, усы, родинка справа от рта и румяна СТРОГО те же. Парик остаётся холодным серебристо-серым и белым.
Меняется ТОЛЬКО выражение: глаза снова на объективе, он только что сказал «наверное, ничего», сухая усмешка, рот закрыт или чуть приоткрыт, бровь слегка приподнята, голова наклонена на несколько градусов к левой стороне зрителя; тяжёлые веки остаются полуопущенными, глаза НЕ широкие; веер у дамы сзади закрыт. Голова, верх парика и центр лица в пределах 3 процентов от старта.
КАЧЕСТВО: полное разрешение, чёткость и мелкие детали оригинала; усы, локоны парика, кружево и золотая вышивка так же чёткие; без сглаживания, размытия, смягчения, «нарисованной» кожи, без пересвета и ореолов. Настоящее телефонное видео, зерно, без бьюти-фильтра. Без текста, логотипов, современных предметов, лишних пальцев, только один король.

### 3) Промпт клипа (10 секунд, по долям, с исправлениями)
@first_frame — точный первый кадр: первые 0,3 с как есть, затем оживает. Всё время один и тот же король, лицо и вид как в референсе: тот же возраст, тяжёлые веки, усы, родинка справа от рта, парик холодный серебристо-серый (не бежевый, не кремовый, не золотой, свечи его не красят), алый камзол с золотым солнцем, жабо; он откинулся в кресле в освещённом золочёном зале, снимает на свой телефон в руке чуть ниже уровня глаз, чтобы позади был виден зал. В конце, на 10 с, кадр в точности как @last_frame (сухая усмешка, глаза на объективе); король и зал в обоих кадрах на одном месте. Реалистичная живая съёмка, настоящая кожа.
0-2,5 с: откидывается, медленно обводит взглядом зал справа налево, задумчив, губы поджаты.
2,5-6,0 с: переводит глаза на объектив: «So... I was wondering what else to show you here.» («Так... интересно, что бы ещё вам тут показать.») с лёгким хмуром и наклоном головы вправо; на 4 с дама сзади справа закрывает веер.
6,0-7,0 с: тишина около секунды: снова смотрит по залу, уголки рта ползут вверх; камера продолжает двигаться.
7,0-8,0 с: короткий сухой смех «Ha.» («Ха.») с небольшим подёргиванием плеча.
8,0-9,3 с: «Probably... nothing.» («Наверное... ничего.») лёгким тоном, пожатие одним плечом.
9,3-10 с: тишина, усмешка, глаза на объективе, поза @last_frame, слышен только гул зала.
ПЛАН КАМЕРЫ в абсолютных величинах (его собственный телефон в руке; король и зал стоят на месте, двигается кадр; голова с париком занимает около 60 процентов ширины, поэтому каждое движение держит лицо и парик в кадре; горизонтальные смещения не более 6 процентов, остальное даёт наезд/отъезд и наклон): 0-2 с плавный сдвиг вправо на 6 процентов вслед за взглядом, крен ослабевает на 3 градуса; 2-4 с возврат влево на 6 процентов с наездом на 5 процентов; 4-6 с проседание вниз на 5 процентов и подъём; около 5 с (допустимо 4-6) телефон на полсекунды наклоняется к потолку и возвращается; 6-8 с дрейф вправо на 5 процентов; около 7,5-8 с его собственный розовый палец заходит в левый нижний угол и закрывает до 20 процентов ширины (не более 25) на 0,6 с, лицо не закрывает; 8-10 с небольшой наезд и успокоение до кадра @last_frame.
ПЛАН ПОЗЫ глаголами: откинуться, обвести взглядом, нахмуриться, наклонить голову, взглянуть, усмехнуться, засмеяться, пожать плечом; голова смещается примерно на треть-половину своей ширины в каждом двухсекундном окне, влево-вправо, заканчивая около центра; ни одной паузы в позе дольше 2 секунд.
ЗАЛ ЖИВОЙ: пламя свечей колеблется; на 1 с слуга в ливрее далеко позади проходит справа налево; на 3 с придворный у правого края стола поворачивается к соседу; на 4 с дама справа сзади закрывает веер; на 6 с дама за столом наклоняется к соседке; на 7 с придворный переносит вес.
Ограничения игры: тяжёлые веки остаются (кроме смеха), глаза не широко раскрыты, лицо естественное, у рук по пять пальцев. Без резких панорам и зума, всё движение рукой; без стабилизатора, тележки и дрона.
Звук: только естественный: тихий гул большого зала, ткань, приборы, свечи, его голос и дыхание; музыки нет совсем (звук модели всё равно заглушается, голос кладём наш, v3).
Без текста и титров, без современных предметов, без прозрачного стекла и хрусталя, один король в кадре (без двойника).

Настройки: старт и конец — GPT Image 2.5 Sunburst Lite, 4K, 9:16, high, по 0,12 доллара (итого 0,24); клип — Kling 4.0 i2v, 720p, 10 секунд, 1,45 доллара. Всё вместе около 1,69 доллара. Каждый вызов только после отдельного "да" после просмотра референсов и этого перевода.
