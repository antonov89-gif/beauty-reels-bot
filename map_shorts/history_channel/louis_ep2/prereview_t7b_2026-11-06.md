# Pre-generation review, piece t7b (Take 7 piece 7b, he stands, the crowd bows, "subscribe"; S14 low swing up), 06.11.2026
Scripts: gen_t7b_start.py, gen_t7b_end.py, gen_take_t7b.py. Preflight run on the start script only: mechanical PASS (R1 768x1376 best original, sharp 940 / detail 6.59 / blocks 0.99; R10 1686x1920, sharp 104.6 / detail 1.52 / blocks 1.29 vs hall limit 1.30: passes by 0.01). End/clip: missing-file FAIL expected (stills not generated). --reviewer-pass NOT recorded.

## VERDICTS
- START still (gen_t7b_start.py): FAIL (1 real fix: face size vs wig, 1 small)
- END still (gen_t7b_end.py): FAIL (2 fixes)
- CLIP (gen_take_t7b.py): FAIL (3 fixes)

## Why the wig is the core problem
A3: face width about 255 px of a 510 px wig (long curls to about 530), i.e. the wig is about 2.0x the face width. A face at 44 % of the frame width = wig about 88-95 % of the width. The clip prompt says "free margin about 28 % on each side" - that is the margin of the FACE, not of the wig; with drifts of 8-10 %, a roll and push-ins of 5-6 % the wig leaves the frame. T4b (face 37 %) was the working size; its lesson says the wig must stay inside at every moment.

## Checklist: START still
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle new, hand-held | PASS | S14: low, table level, about 30 deg from below, roll 8 deg left, standing/rising; differs from S6 soup (very low, bowls foreground), T7a (a little below eye level, arm's length, hall to the right), S1 selfie. Phone "in his outstretched hand" |
| 2 | Emotion | PASS | haughty, bored, heavy lids, closed lips, faint smirk; no wide eyes |
| 3 | Laugh / human moment | N.A. | Take 7 laugh is in 7a, not in 7b |
| 4 | Pauses / lines | N.A. | still (lines in header match script 7.3, see clip) |
| 5 | Living room | PASS | courtiers and ladies on both sides starting to bow, heads at different depths |
| 6 | Phone mistake | N.A. | still; mistakes belong to the clip |
| 7 | End pose differs / same composition | PASS (with end-still fix) | start = half risen, hand on cloth; the end must keep head box |
| 8 | Face refs | PASS with WARN | A3 + angle in words; R10 is a hall crop but it carries seated ladies, standing men and a chandelier and glasses (prompt bans glasses, chandelier, table people). R10 blocks 1.29 vs 1.30 limit. Acceptable, as used for T4a/T4b |
| 9 | Quality | PASS | R1 best original named; R10 native crop; both opened full size: no seam, no stray hair, no text, sharp; R10 slightly soft in the wigs of the crowd |
| 10 | Kling tags | N.A. | image model |
| 11 | Channel rules | PASS | no handsome line, no text, one king, no music |
| 12 | Motion score | N.A. | still |
| x | Face size vs wig | FAIL | "face fills about 44 percent" gives a wig about 90-95 % wide, no margin for the clip moves |

Start fixes:
1. Face about 36 percent of the frame width (face centre 50 %), "the whole wig and both side curls fully inside the frame with at least 6 percent free on each side; the wig top may touch the top edge but not be cut at the sides". 
2. State the vertical head position (for example "face centre at 42 percent of the frame height") so the end still can copy it.
3. (small) Add "the hand on the cloth is the free hand; the phone hand is outside the frame".

## Checklist: END still
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle | PASS | same camera/roll/crop as the start (edit of the 4K start) |
| 2 | Emotion | PASS | bored, heavy lids, chin up, looking away to the viewer's left |
| 3 | Laugh | N.A. | |
| 4 | Pauses/lines | N.A. | |
| 5 | Living room | PASS | all bowing deeply |
| 6 | Phone mistake | N.A. | |
| 7 | End pose differs, same composition | FAIL | contradiction: "head a little higher in the frame" vs "head, wig top and face centre within 4 percent". Also the start has a hand pressing the tablecloth; the end says "one hand raised to the right" but does not remove the hand on the cloth, risk of two hands/extra arm |
| 8 | Face refs | PASS | only the 4K start (edit), no other pose |
| 9 | Quality | PASS (to be measured) | one ref = 4K original of the start; QUALITY sentence present; measure head area -23 % rule after |
| 10 | Kling tags | N.A. | |
| 11 | Channel rules | PASS | |
| 12 | Motion | N.A. | |

End fixes:
1. Remove "the head a little higher in the frame"; write "the head and face centre at the same place as in the photo (within 4 percent); the change is the body: standing upright, the chin up, looking away to the viewer's left".
2. Add "the hand that pressed on the tablecloth is gone (down, out of frame); only the raised right-side hand is visible, five fingers, one hand only".

## Checklist: CLIP
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle | PASS | new S14, hand-held, "his own hand-held phone", no gimbal/dolly |
| 2 | Emotion per beat | PASS | sigh/bored (2.5-5.5), satisfaction (5.5-7.5), eyebrow lift (7.5-9.5), smug nod (9.5-12), bored look away (12-14); heavy lids kept, no wide eyes |
| 3 | Laugh / human moment | N.A. | Take 7 laugh is 7a; here the human moment is the bored wave |
| 4 | Pauses / exact lines | PASS with WARN | Lines match script 7.3 exactly: "That's all. Bye. I'm busy." / "...And you: subscribe to my stunning channel. And like." / "Or... whatever." (16 words, 14 s = 69 wpm, in the 60-90 gate). Silent beat 5.5-7.5 and 12-13 pause. WARN: the text says "silent beat of one and a half seconds" but the window is 2 s; and "whatever." is followed by "the frame settles": say the last word ends at about 13.7 s and the edit cuts there (hard cut to the end card). The clip does end on "Or... whatever." |
| 5 | Living room | PASS with WARN | named: lady left 1 s, both sides 3 s, courtier right 4 s, servant 6 s, child page right 11 s. WARN: lessons say the left side stays quiet; 3 of 5 events are right/centre (ok); keep it |
| 6 | Phone mistake | PASS with WARN | focus hunt about 6 s (window 4-8) and own thumb about 10 s (window 8-12), neither on the pins. WARN: thumb asked 20 % (cap 25 %); lessons: 15 % cap 20 %, T4a gave 35 % when 15 % was asked. Also write the hunt as an event: "the whole picture blurs for 0.5 s then snaps sharp" |
| 7 | End pose differs / same camera | PASS after end-still fix | start half risen, hand on cloth, looking at lens; end upright, wave, looks away |
| 8 | Face refs | N.A. | only the generated pins (clip has no card; identity words present) |
| 9 | Quality | N.A. until pins exist | pins = 4K originals |
| 10 | Kling tags | PASS with WARN | @first_frame / @last_frame, image_urls = [start, end]; 14 s at 0.145 x 14 = $2.03 fits the 16 words. WARN: all earlier clips were 8-12 s; confirm the provider accepts duration 14 before submitting |
| 11 | Channel rules | PASS | no "handsome", no music, no text, one king, no glass |
| 12 | Motion score | FAIL | per-beat absolute camera score with times: present and good. FAIL points: (a) "free margin 28 % each side" is the FACE margin, the wig (about 2x the face) has no margin at 44 % face, the keep-in-frame clause cannot hold; (b) push-ins 5 % (2-4 s) and 6 % (6-8 s) are never pulled back before 12-14, so the last frame can be larger than @last_frame, add "10-12 s push-back of 8 percent"; (c) the pose verbs are listed once, not per window (the beats carry them, ok), but the start pin is "half risen" while 0-2.5 s says "rises": say "rises the last half" |

Clip fixes:
1. Rewrite the margin sentence after fixing the start (face 36 %): "his face is at 36 percent of the width, the wig about 75 percent, so every move keeps the whole wig and both side curls inside the frame, free margin about 10 percent on each side; moves are 8 to 10 percent of the width, the king's head stays between 30 and 70 percent of the width".
2. Add a push-back (10-12 s, "a pull-back of 8 percent") so the framing returns to @last_frame; and fix 5.5-7.5 s "one and a half seconds" -> "two seconds"; state "the last word 'whatever.' ends at 13.7 s".
3. Thumb: "covers the lower right 15 percent (never above 20) for 0.6 s"; focus hunt as an event "the whole picture blurs for 0.5 s, then snaps sharp".
Also confirm duration 14 s is accepted.

## Для владельца:
### Референсы по порядку
Стартовый кадр (gen_t7b_start.py, GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, около 0,12 $):
1. R1_king_card_A3_white_wig.jpg: карточка лица и костюма A3, 768x1376 (лучший оригинал), роль: личность короля, поза и фон не копируются.
2. R10_hall_clean.jpg: только зал, 1686x1920 (родной кроп), роль: свечи, позолота, придворные; бокалы, люстра и людей за столом не копировать.
Конечный кадр (gen_t7b_end.py, правка, около 0,12 $): 1. t7b_start_4k.jpg (4K оригинал стартового кадра, ещё не создан).
Клип (gen_take_t7b.py, Kling 4.0 i2v, 720p, 14 с, 2,03 $): @first_frame = t7b_start_4k.jpg, @last_frame = t7b_end_4k.jpg (оба ещё не созданы).

### Стартовый кадр, промпт по-русски
Вертикальная реальная фотография при тусклом свечном свете, слегка недоэкспонирована, мелкое плёночное зерно, живая кожа, без бьюти-фильтра. Референс 1: лицо и костюм короля, тот же человек, тот же возраст, тяжёлые веки, тонкие тёмные навощённые усы с загнутыми кончиками, маленькая тёмная родинка справа от рта (справа для зрителя), лёгкие румяна, высокий напудренный парик холодного серебристо-серого и белого цвета (НЕ бежевый, НЕ кремовый, НЕ золотой), алый бархатный кафтан с золотыми солнцами, кружевное жабо; позу и фон не копировать. Референс 2: только зал, угол не копировать, хрустальные бокалы и людей за столом не копировать. Камера: его собственный телефон в вытянутой руке, держит НИЗКО, на уровне стола, снизу вверх, пока он встаёт из золочёного кресла; ракурс снизу около 30 градусов, широкий объектив, крен около 8 градусов влево; лицо занимает около 44 процентов ширины кадра (исправить: около 36, парик целиком в кадре), центр на 50 процентах, чёткое, подбородок поднят; позади и выше позолоченный край потолка и зал со свечами; без люстры. Поза и эмоция: он наполовину поднялся, одна рука давит на белую скатерть у нижнего края (пять пальцев), взгляд надменный, скучающий под тяжёлыми веками, губы закрыты, лёгкая ухмылка; позади по обе стороны придворные в простых париках и дамы в широких платьях только начинают кланяться, головы опускаются на разную глубину. Без текста, логотипов, современных предметов, стекла и хрусталя, лишних пальцев, клоунского грима; только один король.

### Конечный кадр, промпт по-русски
Отредактировать фото: оставить ТОЧНО ту же позицию камеры, тот же низкий ракурс, крен, кадрирование, размер и положение головы (центр лица на 50 процентах ширины), тот же парик, кафтан и зал. Лицо, возраст, кожу, усы, родинку справа от рта и румяна сохранить ТОЧНО; парик остаётся холодным серебристо-серым и белым. Менять ТОЛЬКО позу и толпу: он теперь стоит полностью выпрямившись, (исправить: голова на прежнем месте, не выше), смотрит в сторону влево для зрителя, скучающее выражение под тяжёлыми веками, подбородок поднят; одна рука поднята справа в кадре на уровне плеча в ленивом взмахе, пальцы расслаблены, пять пальцев (исправить: рука, что давила на скатерть, убрана); придворные и дамы позади теперь все глубоко кланяются, головы низко; голова, верх парика и центр лица остаются в пределах 4 процентов. КАЧЕСТВО: полное разрешение, резкость и мелкие детали оригинала; лицо, волоски усов, завитки парика, кружево и золотая вышивка так же чётки; без сглаживания, размытия, мягкости, рисованной или пятнистой кожи; без пересвета и ореолов. Как живая съёмка на телефон, зерно, без бьюти-фильтра. Без текста, логотипов, современных предметов, лишних пальцев; один король.

### Клип, промпт по-русски (14 с)
@first_frame точный стартовый кадр: первые 0,3 с оставить как есть, затем оживить. Один и тот же король во всех кадрах, лицо как на референсе (тяжёлые веки, усы, родинка справа от рта, румяна, парик холодный серебристо-серый, свеча его не окрашивает, алый кафтан с золотым солнцем, кружевное жабо), встаёт из золочёного кресла в зале со свечами, снимает собственный телефон в руке, низко, и поднимается вместе с ним; придворные и дамы позади кланяются. В конце, 14 с, кадр точно как @last_frame (стоит, ленивый взмах, смотрит в сторону, толпа в глубоком поклоне); король и зал на тех же местах в обоих кадрах. Реализм, живая кожа.
0-2,5 с: встаёт из кресла, камера поднимается с ним; позади придворные начинают кланяться, дама слева приседает.
2,5-5,5 с: «That's all. Bye. I'm busy.» (Это всё. Пока. Я занят.) с усталым вздохом, смотрит сверху вниз в объектив; на 4 с придворный справа кланяется ниже всех.
5,5-7,5 с: немая пауза (исправить: два секунды, а не полторы): он даёт толпе стоять в поклоне, обводит взглядом с удовлетворением; камера движется.
7,5-9,5 с: тычет пальцем в объектив, лёгкий подъём брови: «...And you:» (...А вы:).
9,5-12 с: «subscribe to my stunning channel. And like.» (подпишитесь на мой потрясающий канал. И лайк.), медленно кивает, самодовольно.
12-14 с: немая пауза, ленивый взмах рукой, отводит взгляд в сторону, скучающий: «Or... whatever.» (Или... неважно.), кадр оседает в позу @last_frame; жёсткая склейка на этой фразе на плашку.
КАМЕРА (в абсолютных величинах, телефон в руке; король и зал на месте, кадр двигается; лицо 44 процента ширины, каждое движение держит лицо и парик в кадре, поля около 28 процентов): каждые 2 с кадр смещается на 8-10 процентов ширины: 0-2 с подъём с его вставанием на 10 процентов, крен уменьшается на 4 градуса; 2-4 с дрейф вправо на 9 и наезд на 5; 4-6 с качание влево на 8; около 6 с (окно 4-8) фокус «охотится» полсекунды; 6-8 с наезд на 6, пока он показывает пальцем; 8-10 с дрейф вправо на 8; около 10 с (окно 8-12) его розовый палец заезжает в правый нижний угол, закрывая 20 процентов ширины (не более 25) на 0,7 с, лицо не закрывает; 10-12 с проседание и подъём; 12-14 с качание влево на 8 и возврат к кадру @last_frame. (Исправить: лицо 36 процентов, поля парика 10 процентов; добавить отъезд на 8 процентов в 10-12 с; палец 15 процентов, не более 20.)
ПОЗА: встал, вздох, взгляд, указал, кивок, взмах, отвёл взгляд; голова смещается примерно на пол своей ширины (около 20 процентов ширины кадра) в каждом двухсекундном окне, влево и вправо, заканчивая у центра; без удержания дольше 2 с.
КОМНАТА ЖИВАЯ: свечи мерцают; на 1 с дама слева приседает; на 3 с придворные с обеих сторон опускают головы; на 4 с придворный справа кланяется ниже всех; на 6 с слуга за толпой опускает поднос; на 11 с паж-ребёнок справа выглядывает, и чья-то рука прижимает его вниз.
Игра: тяжёлые веки остаются, широко открытых глаз нет, лицо естественное, у рук по пять пальцев. Без резких панорам и зума, всё руками; без гимбала, тележки и летающей камеры. Звук: только естественный, тихий гул большого зала, ткань, приборы, мерцание свечей, его голос и дыхание; музыки нет. Без текста и субтитров, современных предметов, прозрачного стекла и хрусталя, только один король.
Настройки: Kling 4.0 i2v, 720p, 14 с, 0,145 $/с = 2,03 $ (проверить, что провайдер принимает 14 с). Оба кадра пока не созданы: сначала стартовый (0,12 $), затем конечный (0,12 $), затем клип. Итого около 2,27 $.
