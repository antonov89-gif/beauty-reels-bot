# Pre-generation review: piece t5c (Take 5c "Ohh, I wasn't born to work", setup S12), 06.11.2026
Reviewer pass NOT recorded (by instruction). Preflight on gen_t5c_start.py: mechanical PASS (R1 card A3 768x1376 = best existing original, sharp 940, detail 6.59, blocks 0.99); reviewer/owner yes MISSING (expected). End and clip scripts: refs not generated yet (expected missing-file FAIL, not run).

## VERDICT
- gen_t5c_start.py: FAIL (fixable, 5 fixes)
- gen_t5c_end.py: PASS (depends on a fixed start; one soft note)
- gen_take_t5c.py: FAIL (fixable, 8 fixes)
A3 opened at full size: sharp, no seam, no text, the right face (silver wig, beauty mark on the viewer's right of the mouth); it carries a pose (hand at the wig, front view), prompt correctly says "do not copy pose/background".

## Checklist
| # | Item | Start still | End still | Clip |
|--|--|--|--|--|
| 1 Angle new, hand-held | PASS (with risk): 55 deg from above, roll 8 right, armchair, leaned back; S10a was 35 deg from above, roll 12 left, face 60 %, so it is the same family. Push it further apart (60-65 deg, roll 12-15 right). FIX: "held slightly BEHIND his head" cannot show his face (see fixes) | PASS: same camera by design | FAIL: same "behind and above his head" wording; hand-held score present |
| 2 Emotion per beat | PASS: start = eyes closed, long happy sigh, heavy lids | PASS: laugh beat, eyes shut, teeth (allowed, laugh beat) | PASS: sigh / lazy dreamy under heavy lids / soft smile / sinks / joyful laugh; no wide eyes |
| 3 Laugh moment | N.A. | PASS: big laugh with upper teeth | PASS: laugh 10.5-12 s (only 1.5 s, see fix) |
| 4 Pauses, silent beat, EXACT lines | N.A. | N.A. | PASS: the four fragments equal script 7.3 ("Ohh..." / "I wasn't born to work." / "I was born for happiness, love, pleasure..." / "...and a good rest." + laugh); silent beat 1 s after "pleasure" at 8 s. Note: no silence after the laugh, the edit must hold the tail |
| 5 Living room | FAIL: "nobody close", no people in frame, but the clip needs a servant, a courtier edge and a fan lady; the pin must contain them | PASS (inherits) | PASS with risk: 3 named people with seconds (servant 3 s, courtier 5 s, fan lady 9 s); but the lady is LEFT (lessons: left side stays quiet) and none exist in the start frame |
| 6 Phone mistake | N.A. | N.A. | PASS: thumb at ~8 s (window 6-10), not in the pins. Missing a numbered focus hunt; cap says 25 % (lessons: 20 %) |
| 7 End pose differs, same composition | PASS: composition set for the pin | PASS: same camera/crop/head position (3 %); changes = open laugh + hand on chest. Soft note: the head is already resting back at start, so "tipped back a few degrees" is almost the same, rely on the mouth and the hand | PASS: first/last = S12 pair |
| 8 Face refs | PASS: card A3 only, angle in words (setup map listed A3 + K_front; words replace K_front, fine); no hall crop needed | PASS: the 4K start still as the only ref | N.A. (pins) |
| 9 Quality | PASS: A3 is the named best original; 4K output | PASS: edits the 4K original, not a copy; measure after generation (subject limits 150/2.0/1.20) | PASS: both pins 4K; measure after |
| 10 Kling tags/duration | N.A. | N.A. | PASS: @first_frame/@last_frame = image_urls [start, end]; 17 words, 12 s fine; 720p 12 s = 12 x 0.145 = $1.74 |
| 11 Channel rules | PASS: no text/logos/glass/music; one king; no "handsome" | PASS | PASS: no music, no text, one king, no handsome line; AI disclosure N.A. in the prompt (planned in the publication package) |
| 12 Motion score (video) | N.A. | N.A. | FAIL: per-beat camera/pose/room/mistake written with numbers (good), but: (a) margin maths wrong: face 52 % of width with a wig about twice the face width (card: face 33 %, wig 65 %) means the wig already touches both edges, so "free margin 22 % each side" and "wig stays inside while the frame moves 8-10 %" cannot hold; (b) "head moves half its width = 18 %" but half of 52 % = 26 %; (c) between 2.5 s and 10.5 s the hands have no verb (only eyes/head), so the body is near still; (d) 6-8 s has only a drift and eyes up; (e) thumb cap 25 % > 20 %; (f) no focus-hunt event; (g) lady on the left |

## What to fix
START (gen_t5c_start.py)
1. Camera: replace "HIGH and slightly behind and above his head" with "held high IN FRONT of him and above, arm stretched up, looking down at his face from about 60 degrees" (a camera behind the head cannot see the face). Roll 12-15 degrees to the right, to separate from S10a.
2. Framing: face about 40 percent of the frame width (wig about 75 percent, whole wig inside the frame with about 10-12 percent margin each side, a little air above it), face centre at 50 percent. Not 52 percent with the wig at the top edge.
3. Replace "nobody close" by named blurred people at the edges: a courtier's wig and shoulder at the right edge, a servant in livery lower right far below, a lady with a fan at the right-centre background (not left). No glass, no chandelier stays.
4. Output path: the script saves to pilot_frames/anchors/t5c_start_4k.jpg, but end and clip fetch refs/t5c_start_4k.jpg on the branch: copy to refs/ and push before the end call.
5. Show A3 + prompt to the owner after the fix (preflight reviewer/owner yes still missing).

END (gen_t5c_end.py): no blocking fix. Optional: add "no glass anywhere" to the no-list; ask for the head to roll slightly to one side as well as back, so the pose differs more than the mouth. Re-check pin geometry after the start is regenerated.

CLIP (gen_take_t5c.py)
1. Camera sentence: "in front of and above" (as start), not "behind".
2. Margin: after fix 2 write "his face is at 40 percent of the width and the wig about 75 percent, so the free margin is about 12 percent each side; every move keeps the whole wig and face inside the frame", keep shifts at 8 percent only if the wig margin is 12 percent (else 6).
3. Head travel: "half its own width (about 20 percent of the frame width)" to match face 40 percent.
4. Add hand verbs: 0-2.5 s fingers drum; 3-4 s the left hand lifts and smooths the lace cravat; 5.5 s the hand returns to the belly; 7 s the right hand opens palm up like a lazy gesture; 9 s both hands settle; 10.5 s one hand rises to the chest. Add a shoulder or chin verb for 6-8 s.
5. Thumb: cap 20 percent, place the slot at about 7.5 s inside 6-10 s, lower left, 0.6 s, never the face.
6. Add a focus hunt as an event: "at 3.5 s the whole picture blurs for 0.5 s then snaps sharp"; not counted until seen on frames.
7. Room: servant at 3 s right to left (lower right), courtier shoulder at 5 s right edge, the fan lady at 9 s on the right-centre (these must exist in the start pin, fix 3 of start).
8. Laugh: start it at 10 s (the line "and a good rest" ends by 9.8 s) so the laugh has 2 s; the edit holds the last frame as the silent beat. Targets to check after: head >= 0.18 fw/s, still body <= 15 %, frozen background <= 10 %.

## Для владельца
Референсы по порядку:
Заготовка 1 (старт-кадр, GPT Image 2.5 Sunburst Lite, 4K, 9:16, около $0.12): один референс R1 = карточка короля A3 (R1_king_card_A3_white_wig.jpg), 768x1376, лучший существующий оригинал, резкая, без швов и текста. Роль: лицо и костюм (не поза и не фон).
Заготовка 2 (финальный кадр, правка старт-кадра, около $0.12): один референс = 4K старт-кадр t5c_start_4k.jpg (его ещё нет, сначала нужна заготовка 1). Роль: тот же ракурс, меняются только лицо-эмоция и руки.
Заготовка 3 (клип): @first_frame = t5c_start_4k.jpg, @last_frame = t5c_end_4k.jpg (оба 4K, пока не созданы).

ПРОМПТ 1, старт-кадр (перевод, текущая версия; правки из списка выше внесёт автор):
Вертикальная 9:16 настоящая фотография при тусклом свете свечей, слегка недоэкспонированная, мелкое плёночное зерно, живая кожа, без бьюти-фильтра. Референс 1 это лицо и костюм короля: тот же человек, тот же возраст, тяжёлые веки, тонкие тёмные навощённые усы с загнутыми кончиками, маленькая тёмная родинка справа от рта (справа с точки зрения зрителя), лёгкие румяна, высокий напудренный парик холодного серебристо-серого и белого цвета (НЕ бежевый, НЕ кремовый, НЕ золотистый), алый бархатный камзол с золотыми солнцами, кружевное жабо; не копировать его позу и фон.
Камера: собственный телефон короля на вытянутой руке, поднят ВЫСОКО, чуть позади и над головой, смотрит ВНИЗ на лицо под углом около 55 градусов, пока он откинулся в позолоченном кресле (высокий ракурс, никогда не на уровне глаз), наклон около 8 градусов вправо; лицо занимает около 52 % ширины кадра, центр на 50 %, верх парика у верхнего края, подбородок и кружевное жабо в нижней середине, резко.
Поза и эмоция: он только что откинулся в резное позолоченное кресло, голова на спинке, глаза закрыты под тяжёлыми веками в долгом счастливом вздохе, губы чуть приоткрыты, глубоко довольное лицо; обе руки лежат на животе поверх алого камзола, по пять естественных пальцев, у нижнего края.
По краям кадра: верх резного позолоченного кресла и размытый зал при свечах, без люстры, без стекла на столе, рядом никого.
Без текста, логотипов, современных предметов, без стекла и хрусталя, без лишних пальцев, без клоунского грима, только один король.
Правки (рекомендованы рецензентом): камера ВПЕРЕДИ и выше (не позади), лицо около 40 % ширины, парик целиком в кадре, на краях размытые люди (придворный справа, слуга справа внизу, дама с веером справа-центр), наклон 12-15 градусов вправо.

ПРОМПТ 2, финальный кадр (перевод): Отредактируй фото: сохрани ТОЧНО ту же позицию камеры, тот же высокий угол, тот же наклон, тот же кадр и обрезку, тот же размер и положение головы (центр лица на 50 % ширины), тот же парик, камзол, кресло и зал. Лицо, возраст, кожа, усы, родинка справа от рта и румяна ТОЧНО те же (не перерисовывать личность); парик остаётся холодным серебристо-серым и белым. Меняются ТОЛЬКО выражение и руки: он радостно смеётся над своей шуткой, голова запрокинута на несколько градусов в кресло, глаза крепко зажмурены, одна бровь поднята, морщинки смеха, рот широко открыт в большом счастливом смехе, видны верхние зубы, естественно и чуть неровно; руки поднялись: одна лежит ладонью на груди на кружевном жабо, другая всё ещё на животе; голова, верх парика и центр лица в пределах 3 % от фото. КАЧЕСТВО: сохранить полное разрешение, резкость и детали оригинала: лицо, волоски усов, кудри парика, кружево и золотая вышивка так же чётки, без сглаживания, размытия, мыльной или пятнистой кожи, без пересвета и ореолов. Настоящая съёмка на телефон, плёночное зерно, живая кожа. Без текста, логотипов, современных предметов, лишних пальцев, только один король.

ПРОМПТ 3, клип (перевод по долям; правки рецензента отмечены в конце):
@first_frame это точный стартовый кадр: первые 0,3 с оставить как есть, потом оживлять. Всё тот же король в каждом кадре, всегда лицо и вид референса: то же лицо, возраст, тяжёлые веки, тонкие тёмные усы с загнутыми кончиками, родинка справа от рта, румяна, высокий парик холодного серебристо-серого и белого (не бежевый, не кремовый, не золотой, свечи не должны его подкрашивать), алый бархатный камзол с золотым солнцем, кружевное жабо, в резном позолоченном кресле в зале при свечах, собственный телефон держит высоко над головой и чуть позади, смотрит вниз на своё лицо. В конце, на 12 с, кадр точно как @last_frame (он радостно смеётся, одна рука на груди); король и комната в обоих кадрах на одних местах. Реалистичная съёмка, живая кожа, без бьюти-фильтра.
0-2,5 с: глаза закрыты, он выдыхает долгий счастливый вздох, грудь поднимается и опускается, пальцы тихо барабанят по животу: «Ohh...»
2,5-6 с: открывает глаза под тяжёлыми веками, лениво смотрит вверх в объектив и мечтательно говорит: «I wasn't born to work.» с маленьким медленным покачиванием головы; на 4 с поворачивает голову влево посмотреть на двор и обратно.
6-9 с: «I was born for happiness, love, pleasure...» глаза уходят вверх и в сторону, как при воспоминании, мягкая улыбка; тишина в одну секунду после «pleasure» на 8 с с ленивым морганием.
9-10,5 с: «...and a good rest.» снова закрывает глаза и глубже оседает в кресле.
10,5-12 с: радостный смех над своей фразой: голова запрокидывается, плечи трясутся, одна рука поднимается к груди, поза как в @last_frame.
КАМЕРА в абсолютных величинах (телефон в его руке высоко; король и комната на месте, двигается кадр; лицо 52 % ширины, ход камеры не должен выводить лицо и парик из кадра, свободное поле около 22 % с каждой стороны): каждые 2 с кадр сдвигается на 8-10 % ширины: 0-2 с плавный дрейф вправо на 8 % и наезд на 5 %; 2-4 с качание влево на 8 %, наклон ослабевает на 3 градуса; 4-6 с опускание к подбородку на 5 % и подъём; 6-8 с дрейф вправо на 9 %; около 8 с (допустимое окно 6-10 с) его розовый большой палец заезжает в левый нижний угол, закрывая 20 % ширины слева внизу (не более 25 %) на 0,7 с, никогда не лицо (ошибка телефона); 8-10 с небольшой отъезд на 5 %; 10-12 с тряска от смеха на 8 %, затем успокоение до кадра @last_frame.
ПОЗА глаголами: вздох, барабанит, открыл, повернул, дрейф, моргнул, осел, смеётся; голова смещается примерно на пол своей ширины (около 18 % ширины кадра) в каждом 2-секундном окне, попеременно влево и вправо, в конце около центра; никакой паузы дольше 2,5 с (тишина на 8 с, камера продолжает двигаться).
КОМНАТА ЖИВАЯ: свечи мерцают; на краю кадра на 3 с слуга в ливрее пересекает справа налево далеко внизу; на 5 с у правого края сдвигаются край пудрового парика и плечо придворного; на 9 с дама с веером, маленькая, внизу слева, веет быстрее.
Ограничения игры: тяжёлые веки остаются, кроме смеха; широко открытых глаз нет; лицо естественное; у рук по пять пальцев. Без резких панорам и зума, всё руками; без гимбала, дрона и тележки. Звук: только естественный фон большого зала (гул, ткань, приборы, свечи), его голос и дыхание, без музыки. Без текста и титров, без современных предметов, без прозрачного стекла и хрусталя, в кадре один король.
Правки рецензента: камера впереди, а не позади; лицо 40 %, парик 75 %, поле около 12 %; голова на 20 % кадра в окне; руки по глаголам (пальцы барабанят, рука поправляет жабо на 3-4 с, возвращается на 5,5 с, ладонь вверх на 7 с, руки укладываются на 9 с, рука к груди на 10,5 с); палец не более 20 % на 7,5 с; расфокус всей картинки на 3,5 с на 0,5 с; дама с веером справа-центр и все трое людей уже в старт-кадре; смех с 10 с, хвост кадра остаётся тишиной на монтаже.

Настройки: старт-кадр GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, около $0.12; финальный кадр то же, около $0.12; клип Kling 4.0 i2v, 720p, 12 с, $1.74 (0,145 x 12). Итого около $1.98. Одна генерация = один отдельный ответ «да» после показа этих референсов и перевода.
