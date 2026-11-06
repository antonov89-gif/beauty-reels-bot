# Pre-generation review, Take 5 piece 5a (salad, ham, pastry, fruit, peas), setup S11, 06.11.2026
Reviewer pass NOT recorded (as asked). Preflight run only on gen_t5a_start.py: mechanical PASS (A3 768x1376 = best original, sharp 940 / detail 6.59 / blocks 0.99; R10_hall_clean 1686x1920, sharp 104.6 / detail 1.52 / blocks 1.29 within room limits). End/clip scripts: missing-file FAIL expected, ignored. Both reference images opened at full size: A3 clean (no seam, no text, sharp); R10 clean and sharp, but it contains a chandelier, crystal glasses and seated/standing people (same ref and wording already worked for T4a/T4b; the prompt tells the model not to copy them).

## VERDICTS
- gen_t5a_start.py: FAIL (fixable, 2 edits)
- gen_t5a_end.py: FAIL (end pose contradicts the script beat; fixable)
- gen_take_t5a.py: FAIL (item 4 timing, item 12 keep-in-frame numbers wrong, mistake caps, pea logic)

## Checklist
| # | Start still | End still | Clip |
|--|--|--|--|
| 1 Angle | PASS: low, end of the long table, lens 25 cm above the cloth, roll 10 deg left; differs from S9 (across, above, roll right) and S10a (selfie from above). Hand-held N.A. for a still ("filmed by Marcel") | PASS: same camera | PASS: Marcel's phone low at the near corner, hand-held, new setup |
| 2 Emotion | PASS: start = tolerant amused, heavy lids, faint smirk | FAIL: asked "soft delighted half-smile, eyes on pea then lens" but the script's end beat is "eats it, delighted" (see 7) | PASS: per beat written (tolerant sigh, proud, tender, soft, delighted hum); heavy lids kept, no grin; raised brows at 7-9.5 s acceptable |
| 3 Human moment | N.A. (no laugh in script 5a) | N.A. | PASS: the delighted hum after the pea is the human moment |
| 4 Lines / pauses | N.A. | N.A. | FAIL: lines are EXACTLY script 7.3 (PASS), but timing: "And peas." + lean + "The court talks of nothing else." (8 words) are crammed into 7-9.5 s and the header "9.5-12 s" sits on the same line, so he eats while still talking; the silent beat is before the gag, the silent beat AFTER the gag (eating) is only ~2 s if the line is late. Move the lines earlier (see fixes) |
| 5 Living room | PASS: lady with fan back left, servant far right, standing courtiers in plain wigs, no chandelier | N.A. (same hall) | WARN: named people with seconds (servant 1 s, lady 4 s, courtier shift 8 s, courtier nod 10 s) but the lady is on the LEFT, which PROMPT_CAMERA_LESSONS says the model leaves static; 10 s nod has no side. Put 3 events on right/centre |
| 6 Phone mistake | N.A. | N.A. | WARN: focus hunt 7 s and sleeve 10.5 s at stated seconds, different from pins (PASS); but no cap on the sleeve ("never above 20 %, never reaches the face") and the sleeve text says "sleeve of blue" (should be Marcel's sky-blue braided sleeve as in T3c); focus hunt should read "the whole picture blurs for 0.5 s" |
| 7 End pose / pins | N.A. | FAIL: start = counting fingers, end = pea held to the lens (different pose, same camera: PASS), BUT the clip makes him EAT the pea at 9.5-12 s and then "pea back between his fingers": a pea appears from nowhere, and the last frame is the pre-eating state while the script ends on eating. Also "head within 3 %" conflicts with the head tipping back in the delight | FAIL (same reason): last pin contradicts the last beat |
| 8 Face refs | PASS: A3 + R10 hall in words; angle in words; R10 carries no king pose. WARN: R10 has glasses/people/chandelier, prompt forbids copying | PASS: only the 4K start still (original) | PASS: start and end stills as first/last |
| 9 Quality | PASS: A3 = best original (named), R10 1686x1920 | N.A. until the start still exists (4K original, not a copy) | N.A. until stills exist. PROCESS FAIL to fix: start script saves to pilot_frames/anchors/t5a_start_4k.jpg but end/clip URLs read refs/t5a_start_4k.jpg: copy to refs/ (and push to the branch) after inspection, same for the end still |
| 10 Kling tags | N.A. | N.A. | PASS: @first_frame and @last_frame match image_urls [start, end]; no @keyframe; 12 s, 720p = $1.74 (0.145 x 12); 17 words in 12 s is about 85 wpm with pauses, fits once timing is fixed |
| 11 Channel rules | PASS: no text, one king, no glass | PASS | PASS: no music, no text, one king, no "handsome" line; AI disclosure N.A. here (planned in publication) |
| 12 Motion score | N.A. | N.A. | FAIL: per-window camera score with times PASS, pose verbs PASS, room names PASS, no "framing stays the same" PASS, mistakes at seconds PASS; BUT the keep-in-frame clause is arithmetically wrong: the clip says "face 42 % of the width, free margin about 25 % each side". With the face centre at 60 % and face width 42 %, the face spans 39-81 % (right margin 19 %), and the wig is about twice the face width (A3: wig about 2x face width; T4b: face 37 % = head 85 %), so the wig already fills about 85 % and its right edge is cut. A sway left 8 % or a push-in 6-8 % will cut the wig and the face edge. Same cause in the start still |

## What to fix
START still (gen_t5a_start.py)
1. Face size: replace "face fills about 42 percent of the frame width with its centre at 60 percent" with "the king is small and far at the end of the table: his face about 28 percent of the frame width, the whole wig about 60 percent, centre of the head at 58 percent of the width, a free margin of at least 15 percent on each side and above the wig" (T4a head 22 % of width read fine; need >= 130 px head width at 720x1280, 28 % = 200 px). Foreground food stays larger and soft.
2. Pea logic: add "a small silver dish of green peas on the cloth just in front of his lower hand" (keep the tureen soft in the foreground if wanted), so the reach in the clip is short and the pea comes from his own dish.
End still (gen_t5a_end.py)
3. Change the end pose to the state AFTER eating: eyes closed or lowered under heavy lids, head tipped back about 5 degrees (allow 5 %, not 3 %), a soft happy closed-lip smile with a faint chew, the raised hand lowered with two fingertips resting at the peas dish; no pea in the fingers. Update the same face size, centre numbers and "head within 5 percent". Keep the quality paragraph.
Clip (gen_take_t5a.py)
4. Timing: 0-2.5 "Then salad, ham, pastry, fruit." + gives up; 2.5-4.5 "In under an hour." chin up; 4.5-6.2 silent reach and pick one pea; 6.2-7.3 lift pea, "And peas."; 7.5-9.5 lean, "The court talks of nothing else." (end the line by 9.5); 9.5-12 silent eating, closed eyes, hum, settle to the end pin (hand back at the dish, no new pea). Remove "with the pea back between his fingers"; change the "At the end... holds a pea" sentence to match the new last pin.
5. Recompute the keep-in-frame clause with the new numbers (face 28 %, wig 60 %, margins at least 15 % each side): moves of 8-10 % per 2 s stay, but state "the whole wig stays inside the frame at every moment"; reduce "head moves about 20 percent of the frame width" to "about half of the face width (about 14 percent of the frame width)".
6. Phone mistakes: "at 10.5 s Marcel's sky-blue braided sleeve covers the left 15 percent of the frame (never above 20 percent) for 0.6 s and never reaches the face"; "at 7 s the whole picture blurs for 0.5 s then snaps sharp".
7. Room: lady with the fan and the courtier moved to the right/centre behind the king (for example: 1 s servant right back bends; 4 s lady behind his right shoulder whispers; 8 s courtier right of the king shifts weight; 10 s a courtier at the right back nods).
8. After the stills are inspected: copy to refs/, push the branch, then run the clip (separate yes for each call; stills $0.12 each, clip $1.74).

## Для владельца:
Порядок референсов и роли

Кадр 1, старт (gen_t5a_start.py, GPT Image 2.5 Sunburst Lite, 4K, 9:16, около $0,12):
1. R1_king_card_A3_white_wig.jpg, 768x1376 (лучший существующий оригинал), роль: лицо и костюм короля. Чёткий, без швов и текста.
2. R10_hall_clean.jpg, 1686x1920, роль: только зал (позы и бокалы копировать нельзя). Чёткий; на нём есть люди, хрустальные бокалы и люстра, в промте запрещено их копировать.

Кадр 2, финиш (gen_t5a_end.py, правка старта, около $0,12):
1. t5a_start_4k.jpg (ещё не создан, будет около 2161x3840), роль: единственный референс, оригинал 4K.

Клип (gen_take_t5a.py, Kling 4.0 i2v, 720p, 12 с, $1,74 = 0,145 x 12):
1. @first_frame = t5a_start_4k.jpg (будет создан)
2. @last_frame = t5a_end_4k.jpg (будет создан)

ПОЛНЫЙ ПЕРЕВОД ПРОМТА 1 (стартовый кадр), текущая версия
Вертикальная реальная фотография 9:16 при тусклом свете свечей, чуть недоэкспонированная, мелкое плёночное зерно, настоящая текстура кожи, без бьюти-фильтра.
Референс 1: лицо и костюм короля: тот же самый человек, тот же возраст, тяжёлые веки, тонкие тёмные навощённые усы с загнутыми кончиками, маленькая тёмная родинка хорошо видна справа от рта (со стороны зрителя), лёгкие румяна, высокий напудренный парик холодного серебристо-серого и белого цвета, как бледно-серый на референсе 1, НЕ бежевый, НЕ кремовый, НЕ золотой, свечи не должны его подкрашивать, алый бархатный камзол с золотыми солнцами, кружевной галстук; позу и фон не копировать.
Референс 2 показывает только зал: его ракурс игнорировать, НЕ копировать его хрустальные бокалы и людей за столом.
Камера (снимает Марсель): НИЗКО, из ближнего угла в КОНЦЕ длинного стола, объектив всего в 25 см над скатертью, смотрит вдоль стола на короля, сидящего в дальнем конце; НЕ через стол и НЕ сверху, наклон (крен) около 10 градусов влево.
На переднем плане, мягко и не в фокусе, у нижнего и правого края: серебряное блюдо с глазированной ветчиной, пирамида маленьких пирожных, блюдо с фруктами и супница с зелёным горошком (вся еда на столе, только тарелки и золотая посуда).
Король сидит в дальнем конце, его лицо занимает около 42 процентов ширины кадра с центром на 60 процентах ширины, резкое, повёрнуто на три четверти к объективу, салфетка заткнута за кружевной галстук.
Поза и эмоция: он считает блюда на пальцах и как раз сдаётся, с терпимым, снисходительным видом, веки тяжёлые, полуопущены, губы сомкнуты в лёгкой ухмылке, одна рука поднята, показывает несколько пальцев; другая рука лежит на скатерти.
Позади: залитый свечами золочёный зал, стоящие придворные в простых париках, сзади слева дама с раскрытым веером, далеко справа слуга в ливрее; без люстры.
Без текста, логотипов, современных предметов, без стекла и хрусталя где-либо, без лишних пальцев, без клоунского грима, только один король.
Правки ревьюера к этому промту: лицо около 28 процентов ширины, весь парик около 60 процентов, центр головы на 58 процентах, поля не менее 15 процентов; добавить маленькую серебряную мисочку с горошком на скатерти перед его нижней рукой.

ПОЛНЫЙ ПЕРЕВОД ПРОМТА 2 (финишный кадр), текущая версия
Отредактируй фото: сохрани ТОЧНО ту же позицию камеры, тот же низкий ракурс вдоль стола, тот же крен, тот же кадр и обрезку, ту же еду на переднем плане, тот же размер и положение головы (центр лица на 60 процентах ширины), тот же парик, тот же камзол и салфетку, тот же зал позади.
Лицо, возраст, кожу, усы, родинку справа от рта (со стороны зрителя) и румяна сохрани ТОЧНО (личность не перерисовывать); парик остаётся холодным серебристо-серым и белым.
Измени ТОЛЬКО позу и выражение: теперь он держит одну зелёную горошину большим и указательным пальцами к объективу (рука на высоте подбородка, горошина хорошо видна), другая рука опущена за кадр; голова наклонена вперёд примерно на 6 градусов, подбородок вниз, глаза смотрят на горошину, потом в объектив под тяжёлыми веками, мягкая восторженная полуулыбка со сомкнутыми губами; голова, верх парика и центр лица остаются в пределах 3 процентов от фото.
КАЧЕСТВО: сохрани полное разрешение, резкость и мелкие детали оригинала: лицо, волоски усов, завитки парика, кружево и золотое шитьё должны остаться такими же чёткими; без сглаживания, размытия, смягчения, без рисованной или пятнистой текстуры кожи; естественная детализация, без пересвета резкостью и ореолов.
Настоящая съёмка на телефон, мелкое плёночное зерно, настоящая кожа, без бьюти-фильтра. Без текста, логотипов, современных предметов, лишних пальцев, только один король.
Правка ревьюера: финиш должен быть позой ПОСЛЕ того, как он съел горошину (глаза закрыты или опущены, голова запрокинута примерно на 5 градусов, мягкая счастливая улыбка с закрытыми губами и лёгкое жевание, рука опущена к мисочке с горошком, горошины в пальцах нет), допуск смещения головы 5 процентов, размеры лица как в новом старте.

ПОЛНЫЙ ПЕРЕВОД ПРОМТА 3 (клип), по долям, текущая версия
Общее: @first_frame - точный стартовый кадр: первые 0,3 с оставить как есть, затем оживить. Тот же король в каждом кадре, всегда лицо и вид с референса (тот же возраст, тяжёлые веки, тонкие навощённые усы, родинка справа от рта, румяна, высокий парик холодного серебристо-серого цвета, НЕ бежевый, НЕ кремовый, НЕ золотой; алый камзол с золотым солнцем, кружевной галстук), освещённый свечами золочёный зал за ним; снимает Марсель телефоном в руке, очень низко, в ближнем углу длинного стола, вдоль него; еда на переднем плане (ветчина, пирожные, фрукты, супница с горошком) мягкая по краям. К концу, на 12 с, кадр точно как @last_frame (он держит горошину перед объективом, мягкая восторженная полуулыбка); король и зал в обоих кадрах на тех же местах. Реалистичная живая съёмка, настоящая кожа, без бьюти-фильтра.
0-2,5 с: считает блюда на поднятых пальцах, слегка кивая, потом пожимает плечами и опускает руку: "Then salad, ham, pastry, fruit." На 2,5 с сдаётся со снисходительным вздохом; на 1 с слуга в ливрее справа сзади наклоняется переставить блюдо.
2,5-5 с: "In under an hour." он гордо поднимает подбородок, потом смотрит вниз вдоль стола на еду; на 4 с дама с веером слева сзади наклоняется шепнуть соседке.
5-7 с: тишина две секунды: он тянется к супнице двумя пальцами и берёт одну горошину, нежно её разглядывая; камера продолжает двигаться.
7-9,5 с: поднимает горошину к объективу, тихо: "And peas." потом чуть наклоняется к объективу с поднятыми бровями: "The court talks of nothing else." 9,5-12 с: съедает горошину, закрывает глаза и мычит от удовольствия, голова чуть запрокидывается, затем возвращается в позу @last_frame с горошиной снова между пальцами; на 10 с придворный сзади одобрительно кивает.
СЦЕНАРИЙ КАМЕРЫ в абсолютных величинах (телефон Марселя, низко, в руке; король и зал остаются на месте, двигается кадр; лицо короля 42 процента ширины, поэтому каждое движение держит лицо и парик в кадре, свободное поле около 25 процентов с каждой стороны): каждые 2 секунды кадр смещается на 8-10 процентов ширины: 0-2 с медленное подползание вдоль стола к королю, наезд 6 процентов, крен уменьшается на 3 градуса; 2-4 с дрейф вправо на 9 процентов над едой; 4-6 с проседание вниз на 5 процентов и провисание, потом подъём; 6-8 с наезд на 8 процентов к горошине, пока она поднимается; около 7 с (допустимое окно 5-9 с) фокус плывёт: картинка мягчеет на полсекунды и резко возвращается; 8-10 с качание влево на 8 процентов; около 10,5 с (окно 8,5-11,5 с) синий рукав Марселя задевает левый край объектива на 0,6 с; 10-12 с кадр успокаивается к кадру @last_frame.
СЦЕНАРИЙ ПОЗЫ глаголами: считает, кивает, пожимает плечами, поднимает, смотрит, тянется, берёт, поднимает, наклоняется, ест, мычит; голова смещается примерно на половину своей ширины (около 20 процентов ширины кадра) в каждом двухсекундном окне, чередуя лево и право и заканчивая около центра; ни одной паузы без движения дольше 2 секунд.
ЗАЛ ЖИВОЙ: пламя свечей мерцает; на 1 с слуга справа сзади наклоняется к блюду; на 4 с дама с веером шепчет соседке; на 8 с придворный за левым плечом короля переносит вес; на 10 с придворный кивает.
Ограничения игры: тяжёлые веки остаются, кроме смеховых моментов, никаких широко раскрытых глаз, лицо естественное, у рук по пять пальцев. Без резких панорам и без зума, все движения рукой; без гимбала, без тележки и летающей камеры.
Звук: только естественный: тихий гул большого зала, ткань, приборы, мерцание свечей, его голос и дыхание; никакой музыки. Без текста и субтитров, без современных предметов, без прозрачного стекла и хрусталя, только один король в кадре (без второго короля и двойника).
Правки ревьюера к клипу: реплики и тишина сдвинуты (And peas на 6,2-7,3 с, The court talks of nothing else на 7,5-9,5 с, молчаливое поедание 9,5-12 с, без новой горошины в конце); расчёт полей пересчитан под лицо 28 процентов и парик 60 процентов, парик целиком в кадре всегда; движение головы около 14 процентов ширины кадра; рукав Марселя голубой с тесьмой закрывает левые 15 процентов (не более 20) на 0,6 с и не доходит до лица; на 7 с вся картинка размывается на 0,5 с; дама и придворные для событий в зале справа/по центру.

Настройки: старт и финиш: GPT Image 2.5 Sunburst Lite, 4K, 9:16, около $0,12 каждый (отдельное "да" на каждый вызов). Клип: Kling 4.0 i2v, 720p, 12 с, $1,74 (0,145 x 12), первый и последний кадр.
