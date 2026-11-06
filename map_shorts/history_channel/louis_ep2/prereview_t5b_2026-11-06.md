# Pre-generation review: piece t5b (Take 5, Marcel films the laden table, the king eats, no words), 06.11.2026
Scripts: gen_t5b_start.py, gen_t5b_end.py, gen_take_t5b.py. Preflight run only on the start script: mechanical PASS (A3 768x1376 = best original, named; R10 1686x1920; quality OK; reviewer/owner yes missing = expected). --reviewer-pass NOT recorded.

## VERDICTS
- START still: FAIL (3 small fixes)
- END still: FAIL (4 fixes)
- CLIP (Kling): FAIL (item 12 + a self-contradiction, 6 fixes)

## Item 7 judgement (deliberate camera change, tilt up + push-in)
Acceptable in principle for a no-words insert: a tilt up and push-in onto the eater is a real hand-held move, the hall, dishes, wig and coat stay identical, only the scale and the pose change. REFERENCE_RULES H2 warns that a last frame of another composition can make Kling jump or ghost, so it is acceptable ONLY with the following: (a) cut the scale jump (king face 14 % -> 46 % wide = 3.3x) to about 2x (start 18-20 %, end about 38 %); (b) give the end edit the A3 card as a second ref (the only identity source otherwise is a tiny soft face); (c) remove the contradictory "9 % push-in" numbers from the clip camera score; (d) the clip must say the camera move is large (tilt about 20 deg + clear push-in) not 8-10 %. Residual risk: moderate (one ghost/morph wastes $0.72); no further keyframe of another composition.

## CHECKLIST: START still (gen_t5b_start.py)
| # | item | result | evidence |
|--|--|--|--|
| 1 | angle new, hand-held | PASS (note) | above the dishes, tilted down 25 deg, roll 7 deg, king far at top; differs from S9 (across table) by axis and distance. Add "from the end of the table, along its length" so it is not read as S9; setup map has no row for 5b: add one |
| 2 | emotion per beat | FAIL | only "chewing, napkin"; no heavy lids / expression written for the king (only via the card) |
| 3 | laugh/human moment | N.A. | script 5b has none (the laugh is the next beat) |
| 4 | lines exactly script 7.3 | PASS | "no words ... about 4 s" (docstring quotes it); silent insert |
| 5 | living room | PASS | standing courtiers, lady with fan; motion is a clip matter |
| 6 | phone mistake | N.A. | still; the clip carries it |
| 7 | end differs, same composition | N.A. (start) | see judgement above |
| 8 | face refs | FAIL (minor) | A3 + R10 hall are right, but the king is 14 % wide AND "softly out of focus": identity weak and the quality gate (sharp >= 150) likely to fail on the generated still. Say "only slightly soft, face readable, mild depth of field", face 18-20 % wide |
| 9 | quality | PASS | A3 768x1376 best original (named, sharp 940, detail 6.6); R10 1686x1920 (sharp 104.6, detail 1.52, blocks 1.29: at the room limit 1.30); not video frames |
| 10 | Kling tags | N.A. | image script |
| 11 | channel rules | PASS | Louis, no text, one king, no glass; "handsome" absent; no music |
| 12 | motion score | N.A. | still |
Notes: R10 has crystal glasses and seated ladies at its lower table; the prompt forbids copying them (worked for T4a/T4b); check at full size after generation. State "his hands hidden behind the dishes" to avoid far, small hand artefacts.

## CHECKLIST: END still (gen_t5b_end.py)
| # | item | result | evidence |
|--|--|--|--|
| 1 | angle | PASS | same hall, tilt up 20 deg and moved in = new framing of the same setup, hand-held look |
| 2 | emotion | PASS | closed eyes under heavy lids in bliss, cheeks full, chewing; no wide eyes, no grin |
| 3 | laugh | N.A. | |
| 4 | lines | N.A. | no words |
| 5 | living room | FAIL (minor) | the people behind are not mentioned: add "the same courtiers and the lady with the fan behind him" |
| 6 | phone mistake | N.A. | |
| 7 | end differs / composition | PASS with conditions | pose differs (eyes closed, spoon, full cheeks); composition changes on purpose: see judgement; roll not stated: add "rolled about 4 deg" |
| 8 | face refs | FAIL | single ref = the start still with a tiny soft face. Add R1_king_card_A3_white_wig.jpg as a second image ("Reference 2 is the face card: exactly this man, do not copy its pose") |
| 9 | quality | PASS | source = the 4K start original; QUALITY sentence present (the T3d wording that worked) |
| 10 | Kling tags | N.A. | |
| 11 | channel rules | PASS | one king, no text, wig cool silver-grey |
| 12 | motion | N.A. | |
Other fix: "keep EXACTLY the same ... dishes and food positions" contradicts the camera moving in and up. Write "the same hall, same dishes, same arrangement of the food, same people, seen from the new camera position". Hand with a golden spoon is not in the start still: fine (Kling brings it in), keep "five natural fingers".

## CHECKLIST: CLIP (gen_take_t5b.py, Kling 4.0 i2v, 720p, 5 s)
| # | item | result | evidence |
|--|--|--|--|
| 1 | angle | PASS | hand-held written, not static; new vs S9 (note as above); "lingers" in 0-1.5 s reads as static: replace with "drifts" |
| 2 | emotion per beat | PASS (note) | chew relish -> eyes closed in bliss -> nod; make clear that closed-in-bliss eyes still sit under heavy lids (the acting limits line says heavy lids stay except in laugh beats) |
| 3 | laugh | N.A. | |
| 4 | lines | PASS | "No spoken words: only chewing, a happy hum and the murmur"; matches 7.3; but the Sound line says "his voice and breath": write "his hum and breath" so Kling does not speak |
| 5 | living room | FAIL (minor) | servant "places one more dish" at 1 s adds a dish that is absent in @last_frame; lady with the fan sits at the back LEFT (lessons: the left side stays quiet, name people on the right/centre) |
| 6 | phone mistake | FAIL (minor) | focus hunt "about 2 s" and the sleeve at "about 4 s" have no shape cap and the sleeve overlaps the 4-5 s settle onto the last pin: write "at 1.8 s the picture blurs for 0.5 s and snaps sharp" and "at 3.0 s Marcel's sky-blue sleeve covers the lower left 15 % (never above 20 %) for 0.5 s, gone by 3.6 s, never near the king" |
| 7 | end pose / pins | PASS with conditions | see judgement; end pose differs |
| 8 | face refs | PASS | pins carry the face; clip prompt gives the full descriptor; A3 not a Kling input (fine, same as earlier clips) |
| 9 | quality | PASS | both pins 4K originals (not generated yet, check at full size and preflight when they exist) |
| 10 | Kling tags | PASS | @first_frame / @last_frame = image_urls [start, end]; 5 s fits a no-words insert (script "about 4 s"); price 0.145 x 5 = $0.725 |
| 11 | channel rules | PASS | no music, no text, one king, no glass |
| 12 | motion score | FAIL | (a) camera numbers contradict the pins: "9 % push-in, 8-10 % per 2 s" vs the king growing 14 % -> 46 % and a 20 deg tilt; (b) beat windows (0-1.5/1.5-3.5/3.5-5) differ from camera windows (0-2/2-4/4-5); (c) pose score is a verb list without times; (d) head "a third of its width" (lessons: half width); (e) the room events: one on the left, one adds an object; (f) phone mistakes lack shapes. Good: per-beat camera with times that returns for the last pin, no "framing stays the same", mistakes at stated seconds not on the pins |

## WHAT TO FIX
Start: (1) add "from the end of the table, looking along it"; (2) face 18-20 % of the width, only slightly soft, readable, heavy lids, cheeks slightly full, hands hidden behind dishes; (3) add a setup row 5b to setup_map.
End: (1) add R1 card A3 as a second image_url and a sentence for it; (2) face about 38 % of the width (not 46 %), centre 50 %; (3) replace "same positions" by "same arrangement seen from the new camera position", add the people behind and "rolled about 4 deg"; (4) keep the QUALITY sentence.
Clip: (1) rewrite the camera score to match the pins in the SAME windows as the beats: 0-2 s slow drift left with roll 3 deg right, dishes sharp; 2-4 s a clear tilt up about 20 deg and a push-in (the king grows to about twice his size), focus pulls to the king at 2.3 s; 4-5 s a small sway and settle on @last_frame; the wig and the face stay inside the frame at every moment; (2) pose per window with verbs: 0-2 s chew, cheek bulge, a glance down at the dish; 2-4 s head turns toward the lens about half its width, swallow, hum with eyes closing; 4-5 s a small satisfied nod, spoon hand rises into the frame; (3) room: at 1 s a servant at the RIGHT edge passes behind the dishes with a covered dish and walks out of frame (no dish is left on the table); at 3 s a courtier behind the king, on the right, turns his head to watch him; at 4 s the lady with the fan (move her to the centre-right in the start still) fans herself faster; candle flicker all the time; (4) phone mistakes with the shapes above; (5) sound: "his hum and breath", not "voice"; (6) "lingers" -> "drifts".

## Для владельца
Три шага, каждый по отдельному "да" (старт-кадр -> финальный кадр -> клип). Ниже промпты после исправлений выше (в репозитории сейчас еще старые версии, исправляются перед отправкой).

### Референсы по порядку подачи
Старт-кадр (GPT Image 2.5 Sunburst Lite, 4K, 9:16, около $0.12):
1. R1_king_card_A3_white_wig.jpg, 768x1376, карточка лица короля (лучший оригинал, чёткий: резкость 940), роль: лицо, парик, костюм; позу не копировать.
2. R10_hall_clean.jpg, 1686x1920, только зал (роль: свет, интерьер); бокалы и людей за столом не копировать.
Финальный кадр (правка старт-кадра, около $0.12):
1. t5b_start_4k.jpg, ~2161x3840 (ещё не создан), родной 4K-оригинал старт-кадра.
2. R1_king_card_A3_white_wig.jpg, 768x1376, карточка лица (добавить, сейчас её там нет).
Клип (Kling 4.0 i2v, 720p, 5 с, около $0.725):
1. @first_frame = t5b_start_4k.jpg (~2161x3840, ещё не создан).
2. @last_frame = t5b_end_4k.jpg (~2161x3840, ещё не создан).

### Чек-лист по пунктам для этой вставки
1 Ракурс: Марсель снимает с телефона из руки, чуть выше блюд, вдоль стола, камера наклонена вниз; новый, не S9; не статичный. 2 Эмоция: начало жуёт с тяжёлыми веками, середина блаженство с закрытыми глазами, конец довольный кивок. 3 Смех: нет, тут его нет. 4 Слов нет, только жевание, довольное мычание, гул толпы; тишины после гэга как отдельной нет, это вставка. 5 Зал живой: слуга справа, придворный за королём, дама с веером. 6 Ошибки телефона: расфокус 1.8 с и рукав Марселя 3.0 с. 7 Поза в конце другая; камера намеренно меняется (наклон вверх + наезд), риск описан выше. 8 Лицо: карточка A3 + описание.

### 1. Старт-кадр (полный промпт по-русски)
Вертикальное 9:16 настоящее фото при тусклом свете свечей, слегка недоэкспонировано, мелкая плёночная зернистость, живая кожа, без бьюти-фильтра.
Референс 1 это лицо и костюм короля: тот же самый человек, тяжёлые веки, тонкие тёмные навощённые усы с загнутыми кончиками, родинка справа от рта (справа с точки зрения зрителя), высокий напудренный парик холодного серебристо-серого и белого цвета (НЕ бежевый, НЕ кремовый, НЕ золотистый), алый бархатный камзол с золотыми солнцами; позу не копировать.
Референс 2 показывает только зал: его ракурс игнорировать, бокалы и людей за его столом НЕ копировать.
Камера (снимает Марсель): с руки, чуть выше блюд, вдоль стола с его торца, наклон вниз около 25 градусов, средний крупный план заставленного стола: в чёткости на переднем плане золотое блюдо с жареным фазаном, окорок, пирамида пирожных, чаша с фруктами и золотое блюдо с горошком, всё горой, только тарелки и золотые блюда; король сидит далеко за ними вверху кадра, маленький и лишь слегка мягкий по фокусу, лицо читаемо (около 18-20 процентов ширины кадра, центр на 45 процентах), жуёт, щёки слегка полные, тяжёлые веки, салфетка в кружевном галстуке, руки скрыты за блюдами; кадр завален на 7 градусов вправо. Позади свечной зал, стоящие придворные в простых париках, справа ближе к центру дама с веером, люстры нет. Без текста, логотипов, современных предметов, без стекла и хрусталя, без лишних пальцев, без клоунского грима, только один король.

### 2. Финальный кадр (правка, полный промпт по-русски)
Правка фото: оставить тот же зал, стол, блюда, их расстановку, парик и камзол, то есть то же самое, но увиденное с новой позиции камеры; изменить ТОЛЬКО камеру и короля: камера наклонилась ВВЕРХ на 20 градусов и подъехала, король теперь главный объект, в резкости, лицо около 38 процентов ширины кадра (центр на 50 процентах), еда мягкая у нижнего края, кадр завален около 4 градусов; те же придворные и дама с веером позади. Щёки полные едой, довольно жуёт с закрытым ртом, глаза закрыты под тяжёлыми веками в блаженстве, одна рука с золотой ложкой у нижнего края. Лицо, возраст, кожа, усы, родинка справа от рта и румяна точно как в оригинале и в карточке (референс 2 = карточка лица, позу не копировать), парик холодный серебристо-серый и белый. КАЧЕСТВО: сохранить полное разрешение, резкость и мелкие детали оригинала: лицо, волоски усов, завитки парика, кружево, золотую вышивку; без сглаживания, размытия, мягкости и рисованной или пятнистой кожи; естественная детализация, без пересвета резкости, без ореолов. Настоящая съёмка на телефон, зерно, живая кожа, без бьюти-фильтра. Без текста, логотипов, современных предметов, лишних пальцев, только один король.

### 3. Клип (полный промпт по-русски, по долям секунды)
@first_frame точный первый кадр: первые 0.3 с держать как есть, потом оживлять. Тот же король в каждом кадре, всегда лицо и вид референса: то же лицо, возраст, тяжёлые веки, тонкие тёмные усы с загнутыми кончиками, хорошо видная родинка справа от рта, лёгкие румяна, высокий напудренный парик холодного серебристо-серого и белого (не бежевый, свечи его не красят), алый бархатный камзол с золотым солнцем, кружевной галстук. Снимает Марсель на телефон с руки в свечном золочёном зале. К концу, 5 с, кадр точно как @last_frame (камера наклонилась вверх и подъехала к жующему королю в резкости). Реалистичная съёмка, живая кожа. Слов нет: только жевание, довольное мычание и гул толпы.
0-2 с: камера плавно дрейфует влево с лёгким креном 3 градуса вправо, блюда в резкости, король далеко жуёт, раздувает щёку, бросает взгляд на блюдо; на 1 с справа слуга в ливрее проходит за блюдами с накрытым блюдом и уходит из кадра (на столе ничего не добавляется); в 1.8 с картинка размывается на 0.5 с и снова чётко.
2-4 с: заметный наклон камеры вверх около 20 градусов и наезд (король вырастает примерно вдвое), фокус переходит на короля около 2.3 с; голова поворачивается к объективу примерно на пол своей ширины, король глотает, мычит, глаза закрываются от блаженства; в 3 с придворный справа за королём поворачивает голову посмотреть на него; в 3.0 с голубой рукав Марселя закрывает нижний левый угол объектива (15 процентов, не более 20) на 0.5 с и уходит к 3.6 с, не приближаясь к королю.
4-5 с: небольшое покачивание и остановка точно на композиции @last_frame; довольный небольшой кивок, рука с ложкой поднимается в кадр; в 4 с дама с веером справа обмахивается чаще. Свечи мерцают всё время. Король и стены остаются на месте, а кадр дрейфует, кренится и перецентровывается на несколько процентов, парик и лицо всё время внутри кадра.
Ограничения актёра: веки тяжёлые всегда (закрытые в блаженстве это тоже тяжёлые), никаких широко открытых глаз, лицо естественное, у рук по пять пальцев. Без резких панорам и зума, все движения рукой; без стабилизатора, тележки и летающей камеры. Звук: только естественный: тихий гул большого зала, ткань, приборы, мерцание свечей, мычание и дыхание; музыки нет. Без текста и субтитров, без современных предметов, без прозрачного стекла и хрусталя, только один король в кадре (без второго и без двойника).
Параметры: Kling 4.0 i2v, 720p, 5 с, около $0.725 (0.145 x 5). Новая версия промптов ещё не записана в файлы; после правок покажу заново.
