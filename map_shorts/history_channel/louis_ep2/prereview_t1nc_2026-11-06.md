# Prereview piece t1nc (Take 1 piece 1c, setup S2b), 06.11.2026
Reviewed: gen_t1nc_start.py, gen_t1nc_end.py, gen_take_t1nc.py. No --reviewer-pass recorded. Preflight run on the start script only: mechanical PASS (R1 768x1376 best original, sharp 940 detail 6.59 blocks 0.99; R10 1686x1920 sharp 104.6 detail 1.52 blocks 1.29 vs limit 1.30, marginal). Both reference images opened at full size: clean, no seam, no text.

## VERDICT per script
- START still: FAIL (angle is not new: near duplicate of S5 and of the S3 description).
- END still: FAIL (minor: no "heavy lids, no wide eyes" clause; the "expansive grand look" invites wide eyes).
- CLIP: FAIL (too many words for 14 s, about 128 wpm incl. pauses; no silent beat after the final gag).

## Angle check S2b vs earlier setups
- vs S1 (extreme low selfie, 80% face, ceiling): different. PASS.
- vs S2 (table height, dutch 15 deg left, wig filling top, three-quarter LEFT): different height and mirrored. OK.
- vs S3 (map: "arm's length, a little higher and wider than S1, hall behind"): S2b says "arm's length a little ABOVE eye level": same description. WEAK.
- vs S5 (T2c_start_4k.jpg, opened): three-quarter face toward the viewer's RIGHT, near eye level, close medium, gold plate of grapes at the lower edge, candlelit hall behind on the right. S2b = the same composition with a 6 deg roll, a slightly higher camera and a napkin. FAIL: the viewer would see the same shot twice (and the grape plate pre-empts the Take 2 grape gag).

## Checklist, START still
1 Angle new, hand-held: FAIL (see above; hand-held itself is written, "his own hand-held phone").
2 Emotion (a still has one beat): PASS, wounded read, heavy lids, pursed lips, no wide eyes.
3 Laugh/human moment: N.A. (script piece has none; the sniff/wave is in the clip).
4 Pauses/lines: N.A. for a still (lines quoted in the docstring = script 7.3, match).
5 Living room: PASS, long table, standing courtiers, lady with open fan, no chandelier; named in the still.
6 Phone mistake: N.A. for a still (in the clip).
7 End pose differs: N.A. for the start still.
8 Face refs: PASS, A3 + angle in words + R10 hall-only, "do not copy pose/glasses" written. Note: bible line 90 says napkin removed from the costume; here a napkin is tucked in the cravat: deliberate, but it is in no other piece (continuity risk, owner to confirm).
9 Quality: PASS (A3 768 = best original, named; R10 native crop; output 4K).
10 Kling tags: N.A.
11 Channel rules: PASS (no handsome line, no music, one king, no text). AI disclosure: planned in the description, not in this script.
12: N.A.

## Checklist, END still
1 Angle: PASS in intent (same camera as start, edit) but inherits the S5 problem if the start is not changed.
2 Emotion: FAIL minor: "expansive grand look, one eyebrow raised" without "heavy lids kept, no wide eyes".
3 N.A.  4 N.A.
5 Room: PASS (kept by "same hall").
6 N.A.
7 End pose differs, same camera, face centre within 3%: PASS (start: eyes down to a screen, head tilted; end: chin up, look into the lens, smug smile).
8 Face refs: PASS (single ref = the 4K start still, an original, not a video frame; the face lock is stated).
9 Quality: PASS conditional (check the start still at full size first; quality paragraph present).
10 N.A.
11 PASS (add "no glass or crystal glass" for safety, the hall ref has glasses).
12 N.A.

## Checklist, CLIP (Kling 4.0 i2v 720p, 14 s, $2.03)
1 Angle new, hand-held: FAIL via the start still (S5 duplicate); hand-held/never static: PASS.
2 Emotion per beat: PASS: wounded -> haughty sniff -> dry smile -> grand smug; heavy lids stated. Minor: the start pin is already "wounded" but 0-1.5 s says "satisfied sigh".
3 Laugh/human moment: N.A. (no laugh in the piece; sniff and dismissive wave are the human moments).
4 Pauses, silent beat, exact lines: lines EXACT script 7.3: PASS. Silent beat 6-8 s exists but sits after "I read it", NOT after the gag "Today... before your eyes". FAIL.
   Timing: 30 words in 14 s with a sigh, a sniff and a 1.5 s silence = about 128 wpm (gate 60-90; 30 words need about 20 s at 90 wpm). Beats too short: 9 words in 2.5 s, 4 words with a pause in 1 s.
5 Living room: PASS: servant 1 s (right to left), courtier right 3 s, lady back-left lowers fan 7 s, lady with fan 12 s; candles. Minor: left side events (7 s) rarely animate; the back-left lady is not in the start still (the still has one lady at the back).
6 Phone mistakes: PASS: focus hunt about 5 s, pink thumb lower right about 9 s (cap 25%, 0.7 s); the pins carry none.
7 End pose differs, same camera, same composition: PASS.
8 Face refs: PASS (the two stills; no extra keyframe).
9 Quality: PASS conditional on the two 4K stills being checked.
10 Tags: @first_frame/@last_frame match image_urls [start, end]: PASS. Duration does not fit the words: FAIL (see 4). Price 14 x 0.145 = $2.03 correct.
11 PASS (no music, no text, one king, no handsome line; AI disclosure planned in description).
12 Motion score: camera per beat with times and absolute %: PASS; pose verbs and head half-width per 2 s, hold <= 2 s: PASS; room with named people and seconds: PASS; no "framing stays the same": PASS; phone mistakes at seconds: PASS. Wording fixes (lessons T4a/T4b): write the focus hunt as an event ("at 5.0 s the whole picture blurs for 0.5 s then snaps sharp") and the thumb as a shape with a cap already present.

## What to fix
1. START: new angle. S2b must not be three-quarter-right/eye-level/grapes. Concrete option: camera at chest height from the king's left, a diagonal look along the table, king in the LEFT third (face about 35% of the width, centre at 30%), roll about 10 deg left, the long table receding on the right, a bread basket or a roast bone instead of grapes at the lower right; or any angle not in {low selfie, table height dutch left, eye-level/slightly high three-quarter right, from above, across the table}. Add S2b to setup_map_2026-11-05.md. Re-run this review after the change.
2. END: add "heavy lids stay, no wide eyes, the look is cold and smug, not surprised" and "no glass or crystal glass anywhere".
3. CLIP: time. Either 16 s ($2.32; sigh 1.5, line 1 3.3, "I read it" + blink 1.2, sniff 1, silent beat 1.5, line 3 2, line 4 3.5, "Today... before your eyes" 2.5, plus a 1 s smug silent tail on the lens), or cut the sniff/wave. The last 1-1.5 s must be the silent beat after the gag with the camera still moving. Re-spread the beat times accordingly.
4. CLIP: focus hunt as a blur event with a number; make the back-left lady a person present in the start still or move that event to the right side.
5. Napkin: confirm with the owner (continuity with Take 2).

## Для владельца
Ссылки на референсы (в порядке подачи):
СТАРТОВЫЙ КАДР (GPT Image 2.5 Sunburst Lite, 4K, 9:16, high, примерно $0.12):
1. R1_king_card_A3_white_wig.jpg, 768x1376 (лучший оригинал), лицо и костюм короля.
2. R10_hall_clean.jpg, 1686x1920, только зал (без людей на переднем плане как позы; бокалы и люди за столом не копировать).
КОНЕЧНЫЙ КАДР (правка старта, примерно $0.12): 1. t1nc_start_4k.jpg, 4K оригинал (будет создан).
КЛИП (Kling 4.0 i2v, 720p, 14 с, $2.03; по замечанию ревью лучше 16 с, $2.32): @first_frame = t1nc_start_4k.jpg, @last_frame = t1nc_end_4k.jpg (оба 4K, будут созданы).

ПРОМПТ СТАРТА (по смыслу):
Вертикальное 9:16 реальное фото при свете свечей, чуть недоэкспонировано, плёнка, настоящая кожа, без бьюти-фильтра. Референс 1 даёт лицо и костюм: тот же человек, возраст, тяжёлые веки, тонкие тёмные навощённые усы с загнутыми кончиками, маленькая родинка справа от рта (справа от зрителя), лёгкие румяна, высокий напудренный парик холодного серебристо-серого и белого цвета (не бежевый, не кремовый, не золотой), алый бархатный кафтан с золотыми солнцами, кружевное жабо; позу и фон не копировать. Референс 2 даёт только зал: угол не брать, хрустальные бокалы и людей за столом не копировать.
Камера: его собственный телефон в руке на длине руки, чуть выше уровня глаз и слева от него, средне-крупный план, крен около 6 градусов вправо; лицо занимает около 50% ширины кадра, центр на 46%, голова в три четверти к правой стороне зрителя, резкое; белая салфетка за жабо, внизу золотая тарелка с виноградом и белая скатерть; позади справа зал со свечами: длинный стол, придворные сидят и стоят в простых париках, дама с раскрытым веером в глубине, без люстры.
Поза и эмоция: он читает комментарии на воображаемом экране под объективом с обиженным видом: тяжёлые веки, поджатые губы, брови чуть сведены, голова наклонена влево от зрителя. Без текста, логотипов, современных предметов, стекла и хрусталя, лишних пальцев, клоунского грима; только один король.
(Замечание ревью: ракурс повторяет S5, нужно заменить, см. правки.)

ПРОМПТ КОНЦА (правка):
Отредактируй фото: сохрани ТОЧНО ту же позицию камеры, угол, крен, кадр, размер и положение головы (центр лица на 46% ширины), парик, кафтан, салфетку и зал. Лицо, возраст, кожу, усы, родинку и румяна не менять; парик остаётся серебристо-серым. Меняется ТОЛЬКО выражение и голова: он смотрит прямо в объектив с величественным взглядом, подбородок поднят, одна бровь приподнята, губы сомкнуты в самодовольной лёгкой улыбке, будто говорит «на ваших глазах», голова повёрнута на несколько градусов к объективу; голова, верх парика и центр лица остаются в пределах 3% кадра. Качество: полное разрешение, резкость и детали оригинала (лицо, волоски усов, локоны, кружево, золотая вышивка), без сглаживания, размытия, пятнистой текстуры; без пересвета. Реальная съёмка на телефон, зерно, без бьюти-фильтра. Без текста, логотипов, современных предметов, лишних пальцев; один король.

ПРОМПТ КЛИПА по долям (14 с):
Общее: @first_frame точный стартовый кадр, первые 0.3 с держать, потом оживлять. Тот же король в каждом кадре: лицо, возраст, тяжёлые веки, усы, родинка, румяна, серебристый парик (свечи его не окрашивают), алый кафтан с золотым солнцем, кружевное жабо, зал позади, телефон в его руке на длине руки чуть выше глаз. В конце, на 14 с, кадр точно как @last_frame (величественный самодовольный взгляд в объектив); король и зал на тех же местах в обоих кадрах. Реалистичная съёмка, настоящая кожа.
0-1.5 с: довольный вздох, тяжёлые веки опускаются.
1.5-4 с: он поворачивается к экрану с обиженным видом: «Some of you write that I eat too much.» (Кое-кто из вас пишет, что я слишком много ем.), наклон головы; на 3 с придворный справа наклоняется к соседу.
4-6 с: «I read it.» (Я это читал.), медленное моргание; затем он надменно шмыгает носом.
6-8 с: тихая пауза 1.5 с: он даёт ей повиснуть, затем небрежно машет рукой, не глядя; камера продолжает двигаться.
8-10.5 с: «Of course, that's not true.» (Конечно, это неправда.), подбородок вверх, сухая улыбка.
10.5-13 с: «Every day I feast in front of the court.» (Каждый день я пирую на глазах у двора.), голова медленно скользит к залу позади и обратно; на 12 с дама с веером обмахивается.
13-14 с: «Today... before your eyes.» (Сегодня... на ваших глазах.), взгляд в объектив, поза @last_frame.
Камера (в процентах ширины, лицо ~50% ширины, поля ~24% с каждой стороны, лицо и парик всегда в кадре): каждые 2 с кадр смещается на 8-10%: 0-2 с дрейф вправо 8% и наезд 5%; 2-4 с качание влево 9%, крен уходит на 3 градуса; 4-6 с провал и подъём 5%; около 5 с (допуск 3-7 с) фокус «ищет» полсекунды; 6-8 с дрейф вправо 8%; 8-10 с наезд 6% и качание влево; около 9 с (допуск 7-11 с) его розовый палец на 0.7 с закрывает нижние 20% ширины справа (не больше 25%), лицо не закрывает; 10-12 с поворот головы, кадр следует на 10% вправо и обратно; 12-14 с небольшой отъезд и успокоение до кадра @last_frame.
Поза глаголами: вздох, чтение, наклон, моргание, шмыганье, взмах, подъём, поворот, улыбка; голова смещается примерно на полширины лица (около 18% кадра) в каждом 2-секундном окне, влево-вправо, заканчивая около центра; удержание не дольше 2 с.
Комната живая: свечи мерцают; на 1 с слуга в ливрее далеко позади несёт блюдо справа налево; на 3 с придворный справа наклоняется к соседу; на 7 с дама сзади слева опускает веер; на 12 с дама с веером обмахивается.
Ограничения игры: тяжёлые веки, кроме смеха (его тут нет), широко раскрытых глаз нет, лицо естественное, у рук по пять пальцев. Без резких панорам и зума, всё рукой; без стабилизатора, тележки, дрона.
Звук: только живой (гул большого зала, ткань, приборы, свечи, его голос и дыхание); музыки нет. Без текста и субтитров, без современных предметов, без прозрачного стекла и хрусталя, один король.
Настройки: Kling 4.0 i2v, 720p, 14 с, $2.03 (ревью советует 16 с, $2.32, чтобы уложить 30 слов с паузами и тишиной после финальной шутки).
