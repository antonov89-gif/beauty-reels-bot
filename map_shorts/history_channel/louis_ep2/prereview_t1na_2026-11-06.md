# Pre-generation review, piece t1na (Take 1 piece 1a, setup S1 extreme low selfie), 06.11.2026
Scripts: gen_t1na_start.py, gen_t1na_end.py, gen_take_t1na.py. Reviewer pass NOT recorded. Preflight run on the start script only: mechanical PASS (R1_king_card_A3_white_wig.jpg 768x1376 = best existing original, sharp 940 / detail 6.59 / blocks 0.99; reviewer and owner yes MISSING as expected). End/clip refs t1na_start_4k.jpg / t1na_end_4k.jpg do not exist yet (expected).

## VERDICTS
- START still (gen_t1na_start.py): PASS (with 3 recommended edits below)
- END still (gen_t1na_end.py): FAIL
- CLIP (gen_take_t1na.py): FAIL

## Face gate risk of the start still (80 percent of width, foreshortened, about 50 degrees from under the chin)
Acceptable, with conditions. Pro: a huge face gives many pixels for identity; the card A3 is sharp (940) and the same prompt recipe gave SFace 0.79-0.87 on earlier stills. Con: the setup map itself says low and profile angles score lower on SFace and the eye check is decisive; from 50 degrees the underside of the chin, nostrils and the moustache dominate, the beauty mark (viewer's right of the mouth) can be hidden by the lip/moustache underside, and the model may drift to another man (the card is a frontal, level shot, so the angle is a big departure). Conditions: (1) soften to about 40 degrees (still extreme low, less distortion); (2) the eye check on the beauty mark, curled moustache tips, heavy lids and silver-grey wig decides, SFace median >= 0.65 / p10 >= 0.45 is the hard gate as usual, NOT lowered silently (if it lands at 0.55-0.65 with a clean eye check, the owner decides an explicit exception, as for T2c); (3) at most 2 attempts by the rule (about $0.24 worst case); (4) the end still and the clip are only ordered after the start passes.

## Checklist: START still
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle new, hand-held | PASS | S1 per setup map (extreme low selfie, thumb, ceiling), not used by any earlier still (S0, S5, S8b, S9, S10a are other angles); roll 12 degrees, phone held too close = hand-held |
| 2 | Emotion | PASS | puzzled frown, squint, heavy lids half-lowered, one brow up, lips parted; no wide eyes, no grin |
| 3 | Laugh moment | N.A. | piece has no laugh |
| 4 | Pauses / exact lines | PASS | docstring lines are exactly script 7.3 for this piece; still has no timing |
| 5 | Living room | N.A. (still) | ceiling-only frame; people come in the clip. See clip FAIL: the pins carry no people at all |
| 6 | Phone mistake | PASS | pink thumb and phone-case edge at lower right, the face too close |
| 7 | End pose differs / same composition | N.A. | start still; see the end still |
| 8 | Face refs | PASS | card A3 only (identity), angle in words, "do not copy its pose or background"; no hall ref needed (ceiling in words); the card carries a hand-at-wig pose, so keep the do-not-copy sentence |
| 9 | Quality | PASS | one ref, 768x1376 named best original, preflight quality OK; output 4K |
| 10 | Kling tags | N.A. | image call |
| 11 | Channel rules | PASS | Louis XIV, one king, no text, no glass, no "handsome" line, no music |
| 12 | Motion score | N.A. | not a video prompt |
Recommended edits (not blocking): (a) "50 degrees" -> "about 40 degrees"; (b) fix the contradiction "tall wig cropped by the top edge" vs "ceiling behind and above him": say "the wig fills the top centre, the painted ceiling and gold cornice visible only at the left and right of the wig and in the upper corners"; (c) add "at the lower left and right corners, beside his shoulders, the blurred edge of the hall (a grey wig, a fan) so the clip has people to animate" (the room has people at the corners, none overlapping the face).

## Checklist: END still
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle | PASS | same setup as start by design (same camera) |
| 2 | Emotion end | PASS | pleased, heavy lids, eyes on the lens, closed smug faint smile, chin lifted |
| 3 | Laugh | N.A. | |
| 4 | Lines | N.A. | still |
| 5 | Living room | FAIL | no person anywhere in the pin; the clip's room events have nothing to match |
| 6 | Phone mistake | N.A. | |
| 7 | End differs, same composition | FAIL | pose differs (frown -> smug) but the composition does not: face 80 -> 56 percent of width, thumb removed, ceiling/cornice enlarged (invented area). The prompt itself contradicts: "keep EXACTLY the same angle, the same ceiling and cornice behind" vs "change the distance, more ceiling visible". An image edit asked to rescale a face by 30 percent redraws the face and the ceiling: identity drift and a ceiling morph in the clip |
| 8 | Face refs | PASS | edit from the 4K start original; no A3 needed for an edit (as T3d end, -23 percent loss) |
| 9 | Quality | PASS (conditional) | source = the 4K original, not a video frame; the quality sentence is present; measure after generation (sharp >= 150, detail >= 2.0, head area -30 percent max) |
| 10 | Kling tags | N.A. | |
| 11 | Channel rules | PASS | |
| 12 | Motion | N.A. | |
Fix: keep the same composition. Either (preferred) change the distance only slightly: face about 68-70 percent, same centre, same ceiling position, thumb gone, a strip of coat and lace at the lower edge, and delete "more ceiling visible"; the pull-back is then carried by the video model, not the still; or the owner accepts the 56 percent end as an explicit exception. Also add the corner people (a blurred grey wig edge at the lower right, a fan at the lower left) here AND in the start still so both pins contain them.

## Checklist: CLIP
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle | PASS | S1 low selfie, hand-held |
| 2 | Emotion per beat | PASS | start squint/frown, middle brighten + smooth moustache, end chin up eyes on lens; lids heavy, no wide eyes ("no wide-open eyes for the king") |
| 3 | Laugh | N.A. | none in this piece |
| 4 | Pauses / lines | PASS (note) | lines exact script 7.3 for the piece; silent beat 4.5-6 s (1.5 s). "Hm-hm" renders the [clears throat] tag: fine, the voice is replaced by v3 TTS. Words 19 in 12 s, 8-12 s has 9 words in 4 s = 2.25 w/s (inside 2.5-3.1 band, slightly slow) |
| 5 | Living room | FAIL | only 2 events: a courtier's head "at the lower edge behind him from right to left at 5 s" is physically impossible (in an under-chin low selfie the lower edge is his chin, lace and coat) and a "tiny servant's shoulder at the left edge at 9 s" (left side stays quiet per lessons, tiny). Need 3 named people with seconds on right/centre, placed where a low-up camera sees people: the lower corners beside his shoulders |
| 6 | Phone mistake | PASS (note) | thumb fumble 0-2.5 s is the pin's own (not counted); focus hunt at about 3 s and tilt to the ceiling at about 7 s (window 5-9) are the real mistakes; but the focus hunt is not an event with a number (lessons: "the whole picture blurs for 0.5 s then snaps sharp") and the thumb has no cap |
| 7 | End differs / same composition | FAIL | pose differs; composition does not (80 -> 56 percent). The prompt says "the king and the room are in the same place in both frames" which is false for these pins |
| 8 | Face refs | PASS | pins carry the identity; the prompt has the full face descriptor and the wig colour clause |
| 9 | Quality | PASS (conditional) | both pins 4K originals, to be measured |
| 10 | Kling tags | PASS | @first_frame / @last_frame, image_urls = [start, end] as in T4a; 12 s fits about 19 words plus the 1.5 s silence; 720p x 12 s x 0.145 = $1.74 |
| 11 | Channel rules | PASS | Louis XIV, no music, no text, one king, no glass, no handsome line |
| 12 | Motion score | FAIL | camera score per 2 s with seconds and numbers: present. Problems: (a) 9 percent drifts and a half-head-width head travel (40 percent of the frame) on a face that is 80 percent wide, plus roll 4 degrees, will throw the face out; the clause "every move keeps the face and wig inside the frame" is false for the start pin whose wig is already cropped, and it contradicts "the phone tilts up to the painted ceiling at 7 s"; (b) pose score 8-12 s is one window with the verbs "chin rising, eyes on the lens, settling" = 4 s with no 2-s verb (hold longer than 2 s); (c) room score fails (item 5); (d) wording "the king and the room are in the same place in both frames" is a static-framing sentence; (e) focus hunt is not a numbered event |

## What to fix in the clip (concrete)
1. Camera in absolute terms scaled to the huge face: 0-4 s drifts 5-6 percent of width (face is 80 percent), 4-12 s 8-10 percent (face 56-70 percent); replace the keep-in-frame sentence with "the eyes, nose, mouth and moustache stay inside the frame at every moment (the edge may cut the wig and the cheek: the clumsy camera is the character)"; make the ceiling tilt "the phone tips up so that the ceiling fills the frame for 0.5 s, the face slides to the lower edge but the eyes stay in frame, then comes back".
2. Head score: 0-4 s a quarter of the face width per 2 s, 4-12 s half; verbs per 2 s in 8-12 s: 8-9 s brow lifts on "Louis", 9-10 s glance aside to a courtier and back on "King of France", 10-11 s small bow of the head on "Welcome", 11-12 s chin lifts, smug smile, eyes on the lens.
3. Room score, three named people on the right/centre at seconds: lady with a fan in the lower right corner turns to her neighbour at 3 s; a courtier in a plain grey wig crosses the lower right corner from right to left at 5 s; a servant in livery enters the lower left corner at 9 s and bows; candle flames flicker throughout. The same people must exist as blurred shapes in both pins.
4. Phone mistakes as events with caps: "the pink thumb slides out of the lower right corner by 2 s and never covers more than 20 percent of the frame"; "at 3.0 s the whole picture blurs for 0.5 s and snaps sharp"; "at about 7 s the phone tips to the ceiling for 0.5 s" (window 5-9 s); none counts as delivered until seen on frames.
5. Replace "the king and the room are in the same place in both frames" with "the room stays in place while the frame drifts, rolls and re-centres; the phone is pulled back between 2.5 and 4.5 s".
6. Composition of the pins: see the end still fix (about 68-70 percent, same centre).
7. Order: start still first (face gate), then the end still, then the clip. Copy both 4K stills to refs/ and push before the end/clip calls (the scripts save to pilot_frames/anchors/ but the RAW URLs point to refs/). Targets after the clip: head >= 0.18 fw/s, still body <= 15 percent, frozen background <= 10 percent; if raw fails, ACCEPTED FOR EDIT with virtual hand-held.

## Для владельца:
Порядок референсов и роль.

### 1. Стартовый кадр (gen_t1na_start.py): GPT Image 2.5 Sunburst Lite, 4K, 9:16, high, цена около $0,12
Референс 1: R1_king_card_A3_white_wig.jpg, 768x1376 (это лучший существующий оригинал карточки, чёткость 940, детали 6,59, блоки 0,99), роль: лицо и костюм короля (лицо, возраст, усы, родинка, серо-серебристый парик, алый камзол, кружевное жабо). Позу и фон карточки копировать нельзя.
Промпт по-русски:
- Вертикальная реальная фотография при тусклом свете свечей, слегка недоэкспонирована, мелкое плёночное зерно, настоящая текстура кожи, без бьюти-фильтра.
- Референс 1: тот же самый человек, тот же возраст, тяжёлые веки, тонкие тёмные навощённые усы с загнутыми кончиками, маленькая тёмная родинка справа от рта (справа от зрителя), лёгкие румяна, высокий напудренный парик холодного серебристо-серого и белого цвета (НЕ бежевый, НЕ кремовый, НЕ золотистый), алый бархатный камзол с золотыми солнцами, кружевное жабо. Позу и фон не копировать.
- Камера: его собственный телефон, поднесённый слишком близко и очень низко, экстремальное селфи снизу, из-под подбородка вверх примерно под 50 градусов (рекомендую 40), широкий объектив, наклон около 12 градусов влево.
- Лицо занимает около 80 процентов ширины кадра, ракурс снизу с перспективным сокращением, ближе всего к объективу подбородок и нижняя сторона усов, высокий парик обрезан верхним краем; сзади и выше расписной потолок золочёного дворцового зала с мягкими облаками и небом и золотой карниз, свечной свет.
- Его розовый большой палец и край чехла телефона видны в правом нижнем углу.
- Лицо при этом остаётся чётким и узнаваемым.
- Поза и эмоция: он щурится на экран телефона с озадаченной хмуростью, тяжёлые веки приспущены, одна бровь поднята, губы слегка приоткрыты, он бормочет «is it on».
- Без текста, логотипов, современных предметов, без стекла и хрусталя, без лишних пальцев, без клоунского грима, только один король.
Правки ревьюера (рекомендую применить): 40 градусов вместо 50; убрать противоречие «парик обрезан» и «потолок над ним»; добавить размытые края зала в нижних углах (серый парик, веер) для людей в ролике.

### 2. Конечный кадр (gen_t1na_end.py): GPT Image 2.5 Sunburst Lite, 4K, edit, цена около $0,12. Статус ревью: FAIL
Референс: t1na_start_4k.jpg (ещё не создан, 4K оригинал, 2161x3840, после проверки лица), роль: исходное фото для правки (тот же ракурс, другая поза).
Промпт по-русски:
- Отредактируй фото: сохрани ТОЧНО тот же ракурс селфи снизу из-под подбородка, тот же наклон, тот же потолок и карниз, тот же парик, камзол и жабо.
- Сохрани лицо, возраст, кожу, усы, родинку справа от рта и румяна ТОЧНО (личность не перерисовывать); парик остаётся холодным серебристо-серым и белым.
- Меняй ТОЛЬКО расстояние и выражение: телефон отведён назад, лицо теперь занимает около 56 процентов ширины кадра, центр на 50 процентах, больше расписного потолка и золотого карниза сверху.
- Большого пальца в правом нижнем углу больше нет (внизу полоса алого камзола и кружева).
- Он увидел себя на экране и доволен: тяжёлые веки, глаза теперь на объективе, губы сомкнуты в самодовольной лёгкой улыбке, подбородок слегка приподнят.
- КАЧЕСТВО: сохрани полное разрешение, резкость и детали оригинала: лицо, волоски усов, локоны парика, кружево и золотое шитьё остаются такими же чёткими; без сглаживания, размытия, размягчения, без «рисованной» или пятнистой кожи; естественная детализация, без пересвета резкостью и ореолов.
- Настоящая съёмка на телефон, мелкое зерно, текстура кожи, без бьюти-фильтра.
- Без текста, логотипов, современных предметов, лишних пальцев, только один король.
Что исправить: лицо 56 процентов и «больше потолка» меняют композицию и противоречат «тот же потолок»; поставить 68-70 процентов, тот же центр и тот же потолок, убрать «больше потолка»; добавить те же размытые люди в нижних углах, что и в старте.

### 3. Ролик (gen_take_t1na.py): Kling 4.0 i2v, 720p, 12 секунд, 0,145 x 12 = $1,74, звук модели заглушен. Статус ревью: FAIL
Референсы в порядке прикрепления: 1) @first_frame = t1na_start_4k.jpg (4K, пока не создан, роль: стартовый кадр); 2) @last_frame = t1na_end_4k.jpg (4K, пока не создан, роль: последний кадр). Размер 2161x3840 после генерации.
Промпт по-русски:
- @first_frame точный стартовый кадр: первые 0,3 с оставить как есть, потом оживлять.
- Один и тот же король в каждом кадре, всегда лицо и вид референса: то же лицо, возраст, тяжёлые веки, тонкие тёмные усы с кончиками, родинка справа от рта, румяна, высокий парик холодного серебристо-серого и белого (не бежевый, не кремовый, не золотистый, свечи не должны его окрашивать), алый бархатный камзол с золотым солнцем, кружевное жабо, снято на его собственный телефон в руке, слишком близко и снизу, потом отодвинуто; сзади и выше расписной потолок и золочёный карниз зала при свечах.
- В конце, на 12 с, кадр ровно как @last_frame (телефон отведён, он довольно смотрит в объектив); король и зал в обоих кадрах на том же месте (ревью: эту фразу заменить, она неверна для разных размеров лица).
- Реалистичная живая съёмка, текстура кожи, без бьюти-фильтра.
- 0-2,5 с: лицо огромное и низкое в объективе, он щурится на экран с хмуростью, приглушённо: «Is it... is it on?», большой палец в правом нижнем углу возится по экрану.
- 2,5-4,5 с: он отводит телефон и видит себя; картинка плывёт вверх-вниз, фокус ищет полсекунды; лицо проясняется: «Ah. There I am.»
- 4,5-6 с: тихая пауза полторы секунды: он любуется собой, поглаживая ус одним пальцем; камера продолжает двигаться.
- 6-8 с: он откашливается: «Hm-hm.», выпрямляется: «Bonjour.»
- 8-12 с: «I am Louis, King of France. Welcome to Versailles.» подбородок поднимается, глаза на объективе, он замирает в позе @last_frame.
- ОЦЕНКА КАМЕРЫ в абсолютных числах (его телефон в руке; король и зал на месте, кадр движется; лицо занимает 80 процентов ширины в начале и 56 в конце, поэтому каждое движение оставляет лицо и парик в кадре): каждые 2 с кадр смещается на 8-10 процентов ширины: 0-2 с дрожащий дрейф влево на 9 процентов, крен качается на 4 градуса; 2-4 с отвод примерно на 25 процентов размера лица и дрейф вправо на 9 процентов; около 3 с фокус ищет полсекунды; 4-6 с качание влево на 8 процентов и просадка; 6-8 с наезд на 5 процентов и рывок перецентровки; около 7 с (допустимо 5-9 с) телефон поднимается к расписному потолку на полсекунды и возвращается; 8-10 с дрейф вправо на 8 процентов; 10-12 с небольшая просадка и успокоение до кадра @last_frame.
- ОЦЕНКА ПОЗЫ глаголами: прищур, хмурость, отвод назад, прояснение, поглаживание уса, откашливание, выпрямление, подъём подбородка; голова смещается примерно на половину своей ширины в каждом двухсекундном окне, влево-вправо и заканчивает у центра; никогда не держится дольше 2 секунд.
- КОМНАТА ЖИВАЯ: пламя свечей мерцает, расписные облака на потолке ловят свет; у нижнего края на 5 с голова придворного в простом парике проходит позади него справа налево; на 9 с крошечное плечо слуги в ливрее у левого края.
- Рамки игры: тяжёлые веки остаются, кроме смеха; без широко раскрытых глаз; лицо естественное; у рук по пять пальцев.
- Без резких панорам и без зума: все движения рукой; без гимбала, без тележки и летающей камеры.
- Звук: только фоновый, тихий гул большого зала, ткань, приборы, мерцание свечей, его голос и дыхание; музыки нет.
- Без текста и титров, без современных предметов, без прозрачного стекла и хрусталя, только один король в кадре (без второго и двойника).
Что исправить в ролике: пункты 1-7 выше (цифры дрейфа для лица 80 процентов, глаголы для 8-12 с, три именованных человека справа/в нижних углах, события телефонных ошибок с числами и ограничениями, убрать фразу «на том же месте», позы пинов с одной композицией). Размер лица на старте и в конце должен совпадать по композиции.
