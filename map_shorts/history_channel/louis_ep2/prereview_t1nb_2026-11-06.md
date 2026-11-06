# Pre-generation review: piece t1nb (Take 1 piece 1b, setup S2, 06.11.2026)
Scripts: gen_t1nb_start.py, gen_t1nb_end.py, gen_take_t1nb.py. Preflight run only on the start script: mechanical PASS (R1 card 768x1376 = best original, named; sharp 940, detail 6.59, blocks 0.99). Reviewer pass NOT recorded (as asked). Missing refs of end/clip are expected.

## VERDICTS
- START still (gen_t1nb_start.py): FAIL (2 fixes)
- END still (gen_t1nb_end.py): PASS with 2 WARN (fix recommended)
- CLIP (gen_take_t1nb.py): FAIL (2 fixes + 1 recommended)

## Checklist: START still
| # | item | result | evidence |
|--|--|--|--|
| 1 | angle | FAIL | S2 is new (table height, rolled 15 deg, 3/4 left), but the wording is "his phone PROPPED by hand": propped/static is banned (owner 05.11). Write "held in his hand". |
| 2 | emotion | PASS | smug sideways look, heavy lids, chin up, one brow, closed faint smile; no wide eyes, no grin |
| 3 | laugh | N.A. | script 7.3 has a satisfied sigh here, no laugh |
| 4 | lines/pauses | N.A. (lines PASS) | docstring lines = script 7.3 Take 1 "And this is my channel. They call me the Sun King. Yes... I'm that handsome. [a satisfied sigh]" exactly |
| 5 | living room | PASS (still) | "a few courtiers' heads" soft behind; motion belongs to the clip. WARN: the servant of the clip (1 s) is not in the still |
| 6 | phone mistake | N.A. | in the clip |
| 7 | pose/composition for pins | FAIL | "face fills about 62 percent of the frame width, centre at 55 percent" is contradictory: on the card the face is ~34 % of the width and the wig ~65 %; in T4b the face was 37 % with head+wig ~85 %. A face of 62 % makes the wig ~120 % of the width (cropped at the sides) while the clip says "keep the wig inside the frame". Centre at 55 % also leaves 24 % left and only 14 % right margin, not "17 % each side". Fix: "head with wig fills about 85 percent of the width, face about 37 percent, face centre at 52-55 percent, wig cropped only by the top edge, free margin >= 8 percent each side". |
| 8 | face refs | PASS | card A3 only + angle in words (3/4 to the viewer's left); "do not copy its pose or background"; no hall-only crop needed (hall described as blurred). Setup map listed K_left34 too: optional |
| 9 | quality | PASS | R1 768x1376 below 1024 but the best existing original (named); preflight quality OK; output 4K |
| 10 | kling tags | N.A. | still |
| 11 | channel rules | PASS | Louis, one king, no text/logos, no glass; "handsome" only in the docstring (script line) |
| 12 | motion score | N.A. | still |

## Checklist: END still
| # | item | result | evidence |
|--|--|--|--|
| 1 | angle | PASS | edit of the start: same camera/roll/crop (still has no motion; carries no "propped" word) |
| 2 | emotion | PASS | long satisfied sigh, eyes closed under heavy lids, lips a little parted; the clip's last beat |
| 3 | laugh | N.A. | |
| 4 | lines | N.A. | still |
| 5 | living room | PASS | "same hall" kept |
| 6 | phone mistake | N.A. | |
| 7 | end differs from start, same composition | WARN | pose differs (smug look -> eyes closed, chin higher, head back 8 deg), same crop. But "head, wig top and face centre within 3 percent" contradicts "tipped back 8 degrees, chin lifted higher" (T4b end moved ~5 %). Fix: tip back about 5 degrees and allow 4-5 percent, or tell the model to tilt only the chin and keep the wig top fixed. |
| 8 | face refs | PASS | one ref = the start 4K original; "do not redraw identity" |
| 9 | quality | WARN | the ref refs/t1nb_start_4k.jpg does not exist yet: the start script saves to pilot_frames/anchors/; the file must be copied to refs/ AND pushed to the branch before the RAW URL works; measure it first (subject limits 150 / 2.0 / 1.2); QUALITY sentence present |
| 10 | tags | N.A. | |
| 11 | channel rules | PASS | no text, one king; add "no glass or crystal glass" (the start has it, the end edit does not) |
| 12 | motion | N.A. | |

## Checklist: CLIP (Kling 4.0 i2v 720p 10 s)
| # | item | result | evidence |
|--|--|--|--|
| 1 | angle | PASS | "his hand-held phone at table height, very close, rolled", "No whip pans... all moves by hand; no gimbal"; S2 is new vs S1/S3/S5/S6/S8b/S9/S10a |
| 2 | emotion per beat | PASS | start: smug sideways look + proud nod; middle: chin lift, knowing smirk after a slow blink, deadpan shrug; end: sigh, eyes close. Limit "heavy eyelids stay... no wide-open eyes". Small WARN: add "except the closing of the sigh" so the model is not confused |
| 3 | laugh | N.A. | script 7.3 has none |
| 4 | pauses/silent beat/lines | PASS | silent beat 5-6.5 s (1.5 s) after "Sun King", sigh beat 8.5-10 s after the gag; lines exact script 7.3. Pace: 16 words / 10 s = 96 wpm incl. a 1.5 s pause and sigh: slightly above the 60-90 gate, acceptable for 15-19 words per clip rule; the TTS is laid over whole phrases |
| 5 | living room | PASS | servant crosses left->right at 1 s, courtier behind leans at 3.5 s, lady's fan at back right at 6 s, candles flicker. WARN: the left side tends to stay quiet (lesson T4a): start the servant from the centre/right; the servant must exist in the start still (still says "a few courtiers' heads" only): add "a servant in livery" to the START prompt |
| 6 | phone mistake | PASS (cap fix) | focus hunt ~5 s (window 3-7), own pink thumb at ~7.5 s (window 5.5-9); neither on a pin. Cap is 20 % (never 25 %): lessons say 15 % / never above 20 % (T4a asked 15, got 35). Lower to 15 % / 20 % and "never reaches the face"; focus hunt as "the whole picture blurs for 0.5 s then snaps sharp" |
| 7 | pins | FAIL (inherits start) | same camera, different pose, same composition: PASS in intent; but the framing numbers are wrong (see start item 7): "his face is at 62 percent of the width... free margin about 17 percent on each side" is false for a face centre at 55 % and impossible with a wig. With drifts of 8-10 % and head travel of 18 % the wig or the face will be cut. Fix with the new numbers: compute the margin from the real still (head+wig ~85 % -> margin ~7 %), then lower the drift to 6-8 % or keep the clause "face and wig stay inside the frame at every moment" and let the moves be the slightly smaller ones |
| 8 | face refs | PASS | the start still (from card A3) is the identity, the pins carry the face; face gate after the clip against A3 |
| 9 | quality | WARN | both pins are not generated yet; each must be measured (>= 150 / 2.0 / 1.2) and copied to refs/ and pushed before the call; end must be within -30 % head sharpness at 720p |
| 10 | tags/duration | PASS | @first_frame / @last_frame, image_urls = [start, end] in that order; 10 s for 16 words + beats; price 0.145 x 10 = $1.45 matches |
| 11 | channel rules | PASS | Louis XIV, "no music at all", "No text or captions", one king, no glass; AI disclosure planned at upload (description + platform flags, not on screen, owner 04.11). "handsome": only this opener line. NOTE: the existing Take 1 rough cut (TAKE1_rough_v2: pilot + piece 2b) ALSO contains "Yes... I'm that handsome." (gen_take1_piece2/2b, gen_t1b_kling40). When 1b enters the edit, the old piece that carries the line must be cut out, otherwise it is said twice |
| 12 | motion score | FAIL (numbers) / PASS (structure) | camera score per 2-s window with times and a return to the last pin: yes; pose verbs per window + head half-width alternating: yes; room score with times: yes (3 people, roles not names: accepted); no "framing stays the same" (wording is "the king and the room stay in place while the frame moves"); phone mistakes at seconds different from the pins: yes. FAIL only because the keep-in-frame margin numbers are wrong (item 7) |

## What to fix (concrete)
1. START: replace "his phone propped by hand" with "his phone held in his hand (hand-held)".
2. START: replace the "face 62 % of the width, centre 55 %" line with "head with the wig about 85 % of the width (face about 37 %), face centre at 52-55 %, free margin at least 8 % each side, wig cropped only by the top edge"; add "a servant in livery far behind" to the hall description.
3. CLIP: fix the margin sentence (no "62 percent / 17 percent each side"): "the head with the wig is about 85 % of the width, the free margin is about 7 % on each side, every move keeps the wig and the whole face inside the frame at every moment"; keep drifts at 6-8 %.
4. CLIP: thumb cap 15 % (never above 20 %) for 0.6 s; focus hunt as a numbered event; start the servant from the centre/right.
5. END (recommended): head tip 5 deg and tolerance 4-5 %; add "no glass or crystal glass".
6. Before the calls: copy t1nb_start_4k.jpg / t1nb_end_4k.jpg into refs/ and push to the branch (RAW URL), measure quality, then show again to the owner; the old Take 1 piece that already says "handsome" leaves the edit.

## Для владельца
Это предварительная проверка. Исправления выше нужно внести до показа и до "да".

### Референсы по порядку
Стартовый кадр (gen_t1nb_start.py, GPT Image 2.5 Sunburst Lite, 4K, 9:16, одна картинка за вызов):
1. R1_king_card_A3_white_wig.jpg, 768x1376: личность и костюм короля (карточка A3, лучший существующий оригинал; чёткость 940, детали 6.59, блоки 0.99). Позу и фон не копировать.
Финальный кадр (gen_t1nb_end.py):
1. t1nb_start_4k.jpg (4K, ещё не создан, будет оригиналом старта): правка того же кадра.
Клип (gen_take_t1nb.py, Kling 4.0 i2v):
1. @first_frame = t1nb_start_4k.jpg (4K, не создан)
2. @last_frame = t1nb_end_4k.jpg (4K, не создан)

### 1. Стартовый кадр: полный промпт по-русски
Вертикальное 9:16 настоящее фото при тусклых свечах, чуть недоэкспонировано, мелкое киношное зерно, живая кожа, без бьюти-фильтра. Референс 1 = лицо и костюм короля: тот же человек, тот же возраст, тяжёлые веки, тонкие тёмные навощённые усы с загнутыми кончиками, маленькая тёмная родинка справа от рта (справа от зрителя), лёгкие румяна, высокий напудренный парик холодного серебристо-серого и белого цвета (НЕ бежевый, НЕ кремовый, НЕ золотой), алый бархатный кафтан с золотыми солнцами, кружевное жабо. Позу и фон не копировать.
Камера: его телефон, "прислонённый рукой" на высоте стола (ИСПРАВИТЬ на "в руке"), очень близко, наклон около 15 градусов влево (голландский угол), смотрит на него в три четверти, слева от зрителя. Лицо занимает около 62 % ширины кадра с центром на 55 % (ИСПРАВИТЬ: голова с париком около 85 % ширины, лицо около 37 %, запас по краям не меньше 8 %); высокий серебристо-серый парик занимает верхнюю треть и обрезан верхней кромкой, резкий. Внизу белая скатерть и угол золотой тарелки. За ним мягко размытый зал при свечах, несколько голов придворных, без люстры.
Поза и эмоция: самодовольный взгляд искоса в объектив из-под тяжёлых век, подбородок поднят, одна бровь поднята, губы сомкнуты в лёгкой гордой улыбке.
Запреты: без текста, логотипов, современных предметов, без стекла и хрусталя, без лишних пальцев, без клоунского грима, только один король.
Настройки: GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, один вызов, около $0.12.

### 2. Финальный кадр: полный промпт по-русски
Отредактируй фото: оставь ТОЧНО ту же позицию камеры, высоту стола, наклон, кадрирование, размер и положение головы (центр лица на 55 % ширины), тот же парик, кафтан и зал. Лицо, возраст, кожу, усы, родинку справа от рта и румяна сохрани точно (личность не перерисовывать); парик остаётся холодным серебристо-серым и белым. Измени ТОЛЬКО выражение и голову: он выпускает долгий довольный вздох, глаза закрыты под тяжёлыми веками, подбородок выше, голова запрокинута примерно на 8 градусов (рекомендация: 5), губы чуть приоткрыты, глубоко самодовольный вид; голова, верх парика и центр лица остаются в пределах 3 % от фото (рекомендация: 4-5 %).
Качество: полное разрешение, резкость и мелкие детали оригинала: лицо, волоски усов, завитки парика, кружево и золотое шитьё так же чёткие; без сглаживания, размытия, "рисованной" кожи, без пересвета и ореолов. Настоящее видео с телефона, зерно, живая кожа, без бьюти-фильтра. Без текста, логотипов, современных предметов, лишних пальцев, только один король (рекомендация: добавить "без стекла и хрусталя").
Настройки: GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, около $0.12.

### 3. Клип: полный промпт по-русски (по долям)
Общее: @first_frame = точный стартовый кадр, первые 0,3 с оставить как есть, затем оживить. Тот же король в каждом кадре: то же лицо, возраст, тяжёлые веки, усы, родинка справа от рта, румяна, высокий серебристо-серый парик (не бежевый, не кремовый, не золотой, свечи не должны его красить), алый кафтан с золотым солнцем, кружевное жабо, зал при свечах, телефон в его руке на высоте стола, очень близко, с наклоном. В конце, на 10 с, кадр точно как @last_frame (долгий довольный вздох, глаза закрыты, подбородок поднят); король и зал на тех же местах в обоих кадрах. Реалистичная съёмка, живая кожа, без бьюти-фильтра.
0-2,5 с: самодовольный взгляд искоса в объектив, затем влево; "And this is my channel." с лёгким гордым кивком.
2,5-5 с: "They call me the Sun King." поднимает подбородок и перекатывает голову вправо; на 3,5 с придворный позади наклоняется к соседу.
5-6,5 с: тихая пауза 1,5 с: медленное моргание под тяжёлыми веками, губы сжаты в многозначительной ухмылке; камера продолжает двигаться.
6,5-8,5 с: "Yes... I'm that handsome." с лёгким пожатием плеч, с каменным лицом.
8,5-10 с: довольный вздох, глаза закрываются, голова запрокидывается, поза @last_frame.
Камера (в абсолютных величинах; телефон в его руке на высоте стола; король и зал на месте, двигается кадр; ИСПРАВИТЬ: лицо 62 % ширины и поля 17 % неверны, надо "голова с париком ~85 %, поля ~7 %, парик и лицо целиком в кадре в каждый момент"): каждые 2 с кадр сдвигается на 8-10 % ширины (рекомендация 6-8 %): 0-2 с плавный дрейф вправо на 8 %, наклон ослабевает на 3 градуса; 2-4 с наезд на 5 % и качание влево на 8 %; 4-6 с наклон возвращается на 5 градусов с небольшим провалом; около 5 с (допустимо 3-7 с) фокус плавает полсекунды и возвращается резким; 6-8 с дрейф вправо на 9 %; около 7,5 с (допустимо 5,5-9 с) его собственный розовый палец заезжает в нижний левый угол, закрывая нижние 20 % ширины (не больше 25 %; рекомендация 15 % / максимум 20 %) на 0,7 с, лицо никогда; 8-10 с лёгкий отъезд и возврат к кадру @last_frame.
Поза глаголами: взгляд, кивок, подъём, перекат, моргание, ухмылка, пожатие, вздох, запрокидывание; голова смещается примерно на половину своей ширины (около 18 % кадра) в каждом двухсекундном окне, влево и вправо, заканчивая около центра; ни одной паузы без движения дольше 2 с.
Комната живая: свечи мерцают; на 1 с слуга в ливрее далеко позади идёт слева направо (рекомендация: из центра/вправо); на 3,5 с придворный позади наклоняется к соседу; на 6 с у дамы сзади справа трепещет веер.
Ограничения игры: тяжёлые веки остаются (кроме закрытия глаз на вздохе), без широко открытых глаз, лицо естественное, у рук по пять пальцев. Без резких панорам и зума, всё движение рукой; без гимбала, дрона, тележки.
Звук: только естественный, тихий гул большого зала, ткань, приборы, мерцание свечей, его голос и дыхание; музыки нет. (Речь модели потом заменяется нашим голосом v3.)
Без текста и субтитров, без современных предметов, без стекла и хрусталя, только один король (без второго и двойника).
Настройки: Kling 4.0 i2v, 720p, 10 с, цена 0,145 x 10 = $1,45, один вызов, повтор только после нового "да".
Проверка слов: 16 слов за 10 с, паузы есть; слово "handsome" только в этом открытии (в старом куске Take 1 "piece 2b" оно тоже есть: при монтаже один из двух убрать).
