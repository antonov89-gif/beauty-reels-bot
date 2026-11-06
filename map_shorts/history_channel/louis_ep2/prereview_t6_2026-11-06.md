# Pre-generation review, Take 6 "the verdict" (setup S13), 06.11.2026
Reviewed: gen_t6_start.py, gen_t6_end.py, gen_take_t6.py. Preflight run only on the start script: mechanical PASS (R1 768x1376 best original, sharp 940 / detail 6.59 / blocks 0.99; R10 1686x1920, sharp 104.6 / detail 1.52 / blocks 1.29 vs room limit 1.30, thin margin). --reviewer-pass NOT recorded. Missing-file preflight FAIL for end and clip ignored as agreed.
Both refs opened at full size: R1 = card A3, clean, sharp, no text, no seam (it carries a pose, hand at the wig, prompt says do not copy it). R10 = hall crop with a chandelier at top right, two seated ladies seen from behind and crystal glasses on the table (the prompt tells the model to ignore glasses and people; worked on T4a/T4b).

## VERDICTS
- gen_t6_start.py: FAIL (one real fix, see F1)
- gen_t6_end.py: PASS (re-check after the start still exists; inherits F1 only if the start framing changes)
- gen_take_t6.py: FAIL (F1, F2, F3, F4)

## Checklist: START still
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle new, hand-held | PASS | S13 frontal eye level close, roll 4 deg left; not used by S1-S12 |
| 2 | Emotion | PASS | heavy lids, complacent smirk, lips closed (start beat) |
| 3 | Laugh | N.A. | laugh is in the end still |
| 4 | Pauses / exact lines | N.A. | docstring quotes script 7.3 Take 6 exactly |
| 5 | Living room | PASS | courtiers, lady with fan back left behind him, blurred |
| 6 | Phone mistake | N.A. | still; the slight roll only |
| 7 | End pose differs, same composition | FAIL | "face fills 56 percent of the width" AND "wig top slightly cropped": the wig is about 2x the face width (A3; on T4b a 37 percent face box = 85 percent with wig), so 56 percent face means a wig cut at both sides. The clip then requires the wig and face to stay inside the frame while it drifts 8-10 percent: impossible. |
| 8 | Face refs | PASS | A3 + angle in words; R10 as hall crop; no other pose carried (R10 has no king) |
| 9 | Quality | PASS | R1 768x1376 named best original (allowed); R10 1686x1920 |
| 10 | Kling tags | N.A. | image model |
| 11 | Channel rules | PASS | one king, no text, no glass, no "handsome" line |
| 12 | Motion score | N.A. | still |
Minor: "chicken bones" vs pheasant/partridge of Take 3 (say "small bird bones"); two napkins (crumpled white one on the plate and the lace one in the hand): make it one.

## Checklist: END still (edit of t6_start_4k.jpg)
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle | PASS | keeps the same camera, roll, crop by instruction |
| 2 | Emotion | PASS | end beat: haughty laugh, heavy lids, one brow up; no wide eyes |
| 3 | Laugh | PASS | open mouth, upper teeth just showing |
| 4 | Lines | N.A. | still |
| 5 | Room | PASS | "same hall" kept; plate pushed right |
| 6 | Phone mistake | N.A. | still |
| 7 | End differs, same composition | PASS | start eyes down, closed lips, chin low; end chin up, looks into the lens, laughs; head within 3 percent. WARN: tipped-back laugh moved the head about 5 percent on T4b end, expect the same; fine for the clip |
| 8 | Face refs | PASS | single ref = the 4K start original, identity sentence + quality sentence (T3d lesson) |
| 9 | Quality | PASS (pending) | ref is a generated 4K original; to be measured once it exists (sharp >= 150, detail >= 2.0) |
| 10 | Tags | N.A. | |
| 11 | Channel rules | PASS | one king, no text |
| 12 | Motion | N.A. | |

## Checklist: CLIP (Kling 4.0 i2v 720p 12 s)
| # | Item | Result | Evidence |
|--|--|--|--|
| 1 | Angle new, hand-held | PASS | S13, own hand-held score. WARN: the header says "slowly pushing in" as a general state, see F4 |
| 2 | Emotion per beat | PASS | smirk -> flat contempt, half-closed eyes -> laugh; heavy lids stay except the laugh |
| 3 | Laugh | PASS | haughty laugh 10.5-12 s |
| 4 | Pauses, exact lines | FAIL | Lines are exactly script 7.3 (24 words). But pace: "So. Do I eat too much?" 6 words in 1.5 s = 4 w/s, and "Don't be afraid ... loser" 12 words in 2.5 s = 4.8 w/s (gate 2.5-3.1 w/s). 24 words need about 9 s of speech + 1.5 s silent beat + laugh = 14-15 s. Silent beat 3.5-5.5 s is present (PASS) |
| 5 | Living room | PASS (WARN) | lady turns at 3 s, servant R->L at 6 s, courtier bows at 9 s, candles. WARN: the lady is at the LEFT back, where Kling kept people still on T3a/T4a; move her to the centre/right, add a whisper pair |
| 6 | Phone mistake | PASS | focus hunt about 5 s (0.5 s), pink thumb about 9 s lower right 20 percent (cap 25; lessons say cap 20) |
| 7 | End vs start, pins | FAIL (via F1/F4) | same camera and composition asked, different pose; but push-ins add up (+6 +5 percent) with a single push-back at 10-12 s unspecified, and the wig-in-frame clause conflicts with a face at 56 percent / cropped wig |
| 8 | Face refs | PASS | pins carry the identity; face description in words |
| 9 | Quality | PASS (pending) | pins are 4K originals, to be measured |
| 10 | Tags, duration | FAIL (duration) | @first_frame/@last_frame match image_urls order [start, end]. Duration 12 s does not fit 24 words at about 90 wpm plus pauses (see item 4) |
| 11 | Channel rules | PASS | no music, no text, one king, no "handsome" line |
| 12 | Motion score | PASS (WARN) | camera score per 2 s with absolute amounts and keep-in-frame clause; pose verbs + head half-width per window; room with 3 named people and seconds; phone mistakes at stated seconds not on the pins. No forbidden "framing stays" wording ("the king and the room are in the same place in both frames" is about the pins only; keep it that way). 8-10 s sway has no amount: write one |

## What to fix
F1 (start, and the clip depends on it): replace "his face fills about 56 percent of the frame width ..., the wig top slightly cropped" with "his head INCLUDING the whole tall wig fills about 80 percent of the frame width (the face itself about 30 percent), the whole wig inside the frame with a thin margin above it, centre at 50 percent". Same in the clip: "his head with the wig is at about 80 percent of the width, free margin about 10 percent each side, so every move is 4-6 percent of the width"; the T4b lesson (8-10 percent) applies only when the margin is big. Keep the keep-in-frame clause.
F2 (clip, duration/pace): 15 s (about $2.18, check that Kling accepts 15) or cut the pace per window: 2-4.5 s "So. ... Do I eat too much?" (6 words), silent 4.5-6.5 s, 6.5-9 s "...No. I eat like a king." (6 words), 9-12.5 s "Don't be afraid of getting fat. Be afraid of being a loser." (12 words, 3.5 s is still 3.4 w/s: the voice is laid over by whole phrases in the edit, so lips only need to be plausible), laugh 12.5-15 s. Words stay exactly script 7.3.
F3 (clip, room): lady with the fan to the centre/right back; add two courtiers whispering on the right at 4 s; servant 6 s and courtier bow 9 s stay.
F4 (clip, push-in): remove "slowly pushing in" from the header or write the net: the pushes (+6 and +5 percent) are undone by an explicit push-back of 11 percent in 8-12 s so the last frame equals @last_frame; give the 8-10 s sway a number (6 percent right); thumb cap 20 percent.
Optional: start: "small bird bones", one napkin only.

---
# Для владельца (по-русски)

## Картинки по порядку подключения
### Стартовый кадр (gen_t6_start.py, GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, около $0,12)
1. R1_king_card_A3_white_wig.jpg: лицо и костюм короля (карточка A3), 768x1376 (лучший существующий оригинал), чёткая, без артефактов.
2. R10_hall_clean.jpg: только зал, 1686x1920, чёткая (в кадре есть бокалы и дамы со спины, промпт запрещает их копировать).

### Финальный кадр (gen_t6_end.py, редактирование, около $0,12)
1. t6_start_4k.jpg: оригинал стартового кадра в 4K (ещё не создан, около 2160x3840).

### Клип (gen_take_t6.py, Kling 4.0 i2v)
1. @first_frame = t6_start_4k.jpg
2. @last_frame = t6_end_4k.jpg (оба ещё не созданы)

## Полный промпт, стартовый кадр (перевод)
Вертикальная реальная фотография 9:16 при тусклом свете свечей, слегка недоэкспонирована, мелкое плёночное зерно, настоящая текстура кожи, без бьюти-фильтра.
Референс 1: лицо и костюм короля: тот же самый мужчина, тот же возраст, тяжёлые веки, тонкие тёмные навощённые усы с загнутыми кончиками, маленькая тёмная родинка хорошо видна справа от рта (со стороны зрителя), лёгкий румянец, высокий напудренный парик холодного серебристо-серого и белого цвета (НЕ бежевый, НЕ кремовый, НЕ золотистый), алый бархатный камзол с золотыми солнцами, кружевное жабо; не копировать его позу и фон.
Референс 2 показывает только зал: игнорировать его ракурс, НЕ копировать хрустальные бокалы и людей за столом.
Камера: в руке на вытянутой руке на УРОВНЕ ГЛАЗ, анфас, крупно: лицо занимает около 56 процентов ширины кадра, центр на 50 процентах ширины, верх парика слегка обрезан, резко; лёгкий крен около 4 градусов влево; у нижнего края золотая тарелка с несколькими чистыми куриными косточками и скомканной белой салфеткой, мягко.
Поза и эмоция: он вытирает пальцы о кружевную салфетку, которую держит в одной руке чуть ниже кадра, подбородок слегка опущен, тяжёлые веки, взгляд вниз на косточки на тарелке, самодовольная еле заметная усмешка, губы сомкнуты.
Позади, размыто: освещённый свечами позолоченный зал, стоящие придворные в простых париках, сзади слева дама с веером, без люстры.
Без текста, логотипов, современных предметов, без стекла и хрусталя, без лишних пальцев, без клоунского грима, только один король.
(Правка ревьюера: "лицо 56 процентов + верх парика обрезан" противоречит клипу; нужно: голова вместе с париком около 80 процентов ширины, парик целиком в кадре, лицо около 30 процентов; кости "мелкие птичьи", салфетка одна.)

## Полный промпт, финальный кадр (перевод)
Отредактируй фото: сохрани ТОЧНО ту же позицию камеры, тот же ракурс на уровне глаз анфас, тот же крен, тот же кадр и обрезку, тот же размер и положение головы (центр лица на 50 процентах ширины), тот же парик, камзол и зал; золотая тарелка с костями чуть отодвинута вправо у нижнего края.
Лицо, возраст, кожу, усы, родинку справа от рта (со стороны зрителя) и румянец сохрани ТОЧНО (не перерисовывать личность); парик остаётся холодным серебристо-серым и белым.
Измени ТОЛЬКО позу и выражение: подбородок высоко поднят, голова запрокинута на несколько градусов, взгляд свысока вдоль носа в объектив под тяжёлыми веками, надменный короткий смех с чуть открытым ртом и едва видными верхними зубами, одна бровь поднята; голова, верх парика и центр лица остаются в пределах 3 процентов кадра.
КАЧЕСТВО: сохрани полное разрешение, резкость и мелкие детали оригинала: лицо, волоски усов, завитки парика, кружево и золотую вышивку так же чётко, как на фото; без сглаживания, размытия, мягкости, рисованной или пятнистой текстуры кожи; естественная детализация, без пересвета резкости и ореолов.
Настоящая съёмка на телефон, мелкое плёночное зерно, настоящая текстура кожи, без бьюти-фильтра. Без текста, логотипов, современных предметов, лишних пальцев, только один король.

## Полный промпт, клип (перевод по битам)
@first_frame точный стартовый кадр: первые 0,3 с оставить как есть, затем анимировать. Тот же король в каждом кадре, всегда лицо и облик референса: то же лицо, возраст, тяжёлые веки, тонкие тёмные усы с загнутыми кончиками, родинка справа от рта (со стороны зрителя), лёгкий румянец, высокий парик холодного серебристо-серого и белого цвета (НЕ бежевый, НЕ кремовый, НЕ золотой, свечи не должны его окрашивать), алый бархатный камзол с золотым солнцем, кружевное жабо, освещённый свечами зал позади, его собственный телефон в руке на уровне глаз, анфас, крупно, медленно приближается. В конце, на 12 с, кадр точно как @last_frame (подбородок вверх, надменный смех, тарелка чуть отодвинута); король и зал в обоих кадрах на одном месте. Реалистичная живая съёмка, настоящая кожа, без бьюти-фильтра.
- 0-2 с: вытирает пальцы о кружевную салфетку, смотрит вниз на кости на тарелке с самодовольной усмешкой, затем выпрямляется.
- 2-3,5 с: двумя пальцами отодвигает тарелку и смотрит в объектив: "So." короткая пауза, затем "Do I eat too much?" с поднятой бровью; на 3 с дама с веером сзади слева поворачивает голову.
- 3,5-5,5 с: немая пауза полторы секунды: он даёт вопросу повиснуть, смотрит на двор, медленно моргает, затем обратно; камера продолжает двигаться.
- 5,5-8 с: "...No. I eat like a king." подбородок медленно поднимается.
- 8-10,5 с: "Don't be afraid of getting fat. Be afraid of being a loser." тихо и ровно, глаза полуприкрыты, лёгкий презрительный наклон головы влево; на 9 с придворный за правым плечом слегка склоняет голову.
- 10,5-12 с: надменный смех, подбородок вверх, оседает в позу @last_frame.
ПЛАН КАМЕРЫ в абсолютных величинах (его собственный телефон; король и зал на месте, двигается кадр; лицо 56 процентов ширины, поэтому каждое движение держит лицо и парик в кадре, свободное поле около 20 процентов с каждой стороны): каждые 2 с кадр сдвигается на 8-10 процентов ширины:
0-2 с медленный наезд на 6 процентов и дрейф влево на 8 процентов, крен уменьшается на 3 градуса;
2-4 с качание вправо на 9 процентов;
4-6 с проседание вниз на 5 процентов и подъём, крен качается в другую сторону на 4 градуса; около 5 с (допустимо 3-7 с) фокус ищет: картинка на полсекунды становится мягкой и снова резкой;
6-8 с дрейф влево на 8 процентов с наездом на 5 процентов;
около 9 с (допустимо 7-11 с) его собственный розовый палец заезжает в правый нижний угол, закрывая нижние 20 процентов ширины (не более 25) на 0,7 с, но никогда не лицо;
8-10 с качание вправо;
10-12 с небольшой отъезд и встряска от смеха на 8 процентов, оседание в кадр @last_frame.
ПЛАН ПОЗЫ глаголами: вытирает, смотрит, выпрямляется, отодвигает, поднимает, моргает, наклоняет, склоняется, смеётся; голова смещается примерно на половину своей ширины (около 20 процентов ширины кадра) в каждом 2-секундном окне, влево-вправо, заканчивая около центра; никакого удержания дольше 2 с.
КОМНАТА ЖИВАЯ: свечи мерцают; на 3 с дама с веером поворачивает голову; на 6 с слуга в ливрее далеко справа проходит справа налево; на 9 с придворный за правым плечом склоняет голову.
Ограничения игры: тяжёлые веки остаются, кроме моментов смеха, никаких широко раскрытых глаз, лицо естественное, у рук по пять пальцев. Без резких панорам и зума, всё движение рукой; без стабилизатора, дрона и тележки.
Звук: только естественный, низкий гул большого зала, ткань, приборы, мерцание свечей, его голос и дыхание; никакой музыки.
Без текста и субтитров, без современных предметов, без прозрачного стекла и хрусталя, только один король в кадре (без второго короля и двойника).
(Правки ревьюера для клипа: длительность 15 с вместо 12 или перераспределить слова (24 слова по 4-4,8 слова/с слишком быстро); поле вокруг парика пересчитать (голова с париком около 80 процентов ширины, движения 4-6 процентов); дама слева переносится в центр/право, добавить шепчущихся придворных справа; наезды (+6 и +5) компенсировать явным отъездом, иначе последний кадр не совпадёт; у качания 8-10 с указать величину; палец не более 20 процентов.)

## Настройки
- Старт: GPT Image 2.5 Sunburst Lite, 4K, high, 9:16, один вызов около $0,12.
- Финал: тот же, редактирование, около $0,12.
- Клип: Kling 4.0 i2v, 720p, сейчас 12 с = $1,74 (0,145 x 12); при 15 с около $2,18.
- Всего около $1,98 (12 с) или $2,42 (15 с). Каждый вызов только после отдельного "да" владельца.
