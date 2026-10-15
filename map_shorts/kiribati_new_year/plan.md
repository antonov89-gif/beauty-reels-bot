# Short (≈35 s, 9:16): "This Country Deleted New Year's Eve" (sequel to the viral Samoa Short)

Format: 1080x1920, English VO, 6 scenes, real animation (Grok Imagine from 1K keyframes), 78 words.
Why this topic: the Samoa Short ("This Country Deleted A Whole Day") took off. Same formula, same date line, bigger emotion: an absurd true claim -> historical cause -> business reason -> concrete dates -> human-scale comedy -> callback line "Business first". Analysis: map_shorts/analysis/ref_own_samoa_viral.md.

## What is new vs Samoa (to be more gripping)
- The deleted day is a holiday (New Year's Eve), not a random Friday: the loss is emotional and instantly understood.
- The country is split in two halves living in two different days: a built-in visual (two clocks, two calendars).
- A reward in the middle of the Short: the same move made the country first on Earth to greet each new year (UTC+14).
- Callback to the Samoa ending ("Business first") rewards returning viewers.

## 3 hooks
1. (chosen) "In 1994, half of this country deleted New Year's Eve."
2. "This country was living in two different days at the same time."
3. "Half of this country never had a December 31st in 1994."

## Voice-over (78 words; Kokoro test 35.2 s with lead + tail; Lumean about the same)
1. In 1994, half of this country deleted New Year's Eve.
2. Kiribati was split by the date line, so its east was almost a day behind.
3. The two halves could do business only four days a week.
4. So it moved the line around the whole country. Friday, December thirtieth, was followed by Sunday, January first.
5. Now its islands greet every new year before any other country.
6. And the east? No New Year's Eve party in 1994. Sorry. Business first.

## Scene table
| # | VO | Visual (keyframe) | Motion (Grok, 6 s) | On-screen text (word-timed, numbers pop instantly) |
|---|---|---|---|---|
| 1 | 1 | Beach party at dusk: long table with food, party hats, balloons, a big clock showing one minute to midnight, a family ready to cheer; the camera is at table level | the clock hand ticks to midnight, the family starts to cheer, then a big blank calendar page drops from above and wipes the scene | "1994", "NEW YEAR'S EVE" then a red strike through it at "deleted" |
| 2 | 2 | Navy starfield diagram of the central Pacific: small green island groups, a glowing yellow line cutting through the middle of the island country, west islands bright, east islands dim | slow orbit, two clocks pop on either side of the line | "KIRIBATI", "EAST = ALMOST 1 DAY BEHIND" |
| 3 | 3 | Two officials in two offices split by a vertical glowing line: left in sunlight with a desk calendar, right with the same desk calendar showing a different page; both hold phones and look puzzled | the left official says hello, the right one shakes his head, both look at calendars | "BUSINESS: 4 DAYS A WEEK" with a 7-day strip where 3 days are crossed out |
| 4 | 4 | Navy diagram again: the glowing line slowly bends east around all islands; a big blank calendar page flutters and flies off the eastern islands | line sweeps right, the page tears away | "LINE MOVED ~1,000 KM", "FRI 30 DEC" then "SUN 1 JAN" (strike on SAT 31 DEC) |
| 5 | 5 | Sunrise on a Pacific beach (Kiritimati style): a crowd with sunglasses and party hats cheers, a small firework bursts over the sea at dawn | slow push-in, the sun rises, the firework pops | "FIRST ON EARTH", "UTC+14" |
| 6 | 6 | Comic payoff: a family in party hats sit at the beach party table around an untouched cake, a hole where a calendar page was torn off hangs on a post, a man shrugs with raised palms | slow push-in, the girl's face falls, candles flicker, the man shrugs | "NO NEW YEAR'S EVE", "BUSINESS FIRST" |

## STYLE LOCK (all keyframes)
Same look as the Samoa and Pangaea Shorts: low-budget Daz Studio / Blender explainer CG with game-cutscene humans (smooth slightly plastic skin, realistic proportions and head size, normal eyes, simple hair, expressive faces), simple matte clothing textures, simplified readable environments, flat saturated blue sky or dusk, soft even lighting. Space/diagram shots (scenes 2 and 4): navy starfield, thin glowing lines, no labels. Free space above for captions. NOT Pixar, NOT cartoon, NOT photograph. No text, no letters, no numbers, no logos. Vertical 9:16.

## Keyframe prompts (Nano Banana 2.1, 9:16, **1K at $0.02 each**; each starts with the STYLE LOCK)
- K1: "A beach party at dusk in the tropics: a long table with food and drinks, balloons and party hats, an oversized clock with no numbers showing almost twelve o'clock on a wooden post, a Pacific islander family of five in party hats about to cheer, palm trees, string lights, calm sea behind. Table-level camera."
- K2: "Navy starfield with a soft glowing Earth horizon at the bottom: a top-down map-style view of the central Pacific with small green island groups scattered in a long chain; a thin glowing yellow line cuts vertically through the middle of the chain; the islands to the left of the line are bright, the islands to the right are dim. No labels."
- K3: "Split composition by a vertical glowing yellow line in the centre: on the left a Pacific islander official in a short-sleeve shirt in a sunlit office holding a phone with a paper desk calendar; on the right an identical office in softer evening light with another official holding a phone and a paper desk calendar showing a different page; both look puzzled. No readable text."
- K4: "Navy starfield diagram of the central Pacific island chain with a thin glowing yellow line bending eastward around all the islands, a big blank white calendar page fluttering and tearing away above the eastern islands. No labels."
- K5: "Sunrise over a calm Pacific beach: a cheering crowd of islanders and tourists in sunglasses and party hats, a small firework bursting over the sea at dawn, a low coconut palm island on the horizon, warm orange and pink sky."
- K6: "A beach party table with an untouched birthday-style cake, a family of four in party hats around it looking disappointed, on a wooden post behind them an empty hook with a torn calendar page, a man in a flowered shirt shrugging with raised palms, dusk light, string lights."

## Animation prompts (Grok Imagine 1.5 Fast, 6 s, image_urls = keyframe, $0.108 each)
- A1: "The oversized clock hand ticks to midnight, the family starts to cheer and raise their arms, then a big blank calendar page drops from above and covers the scene, smooth camera."
- A2: "Slow orbit around the island chain, the glowing line pulses, two small clocks pop up on either side of the line."
- A3: "The left official says hello into the phone and waves, the right official shakes his head and checks his calendar, both look at their calendars; the glowing line pulses."
- A4: "The glowing line slowly bends eastward around all the islands, the blank calendar page flutters and tears away to the right."
- A5: "Slow push-in, the sun rises slightly, the crowd cheers and raises hands, a small firework bursts over the sea."
- A6: "Slow push-in, the girl's smile falls into a pout, the candle flames flicker, the man shrugs with raised palms."
Avoid in prompts (filter): "explosion", alcohol close-ups, "alcohol" (say "drinks"), blood, violence.

## Negative prompt / continuity
Negative: text, letters, numbers, logos, flags with readable emblems, watermark, extra fingers, distorted faces, cartoon eyes, Pixar look, photograph, blurry.
Continuity: the islander family wears party hats (red and yellow) in K1, K5, K6; the calendar page is always blank white; the glowing line is always yellow; the clock in K1 has no numerals.
Overlays/captions: Poppins ExtraBold 3-word captions at ~78 % height, number slams with red glow as in the Madagascar and Suez Shorts; numbers and dates appear instantly (no count-up).

## Fact check (Wikipedia "Time in Kiribati", "Kiribati", "International Date Line", read 2026-10-15)
- Independence 12 July 1979; Kiribati gained the Phoenix and Line Islands from the US; the country straddled the date line.
- Before 1995: the Gilbert Islands UTC+12:00, the Phoenix (UTC-11:00) and Line Islands (UTC-10:00) east of the line; "the Gilberts were nearly a full day ahead" -> "almost a day behind" in the VO.
- Routine business by radio or phone possible only on days that were weekdays on both sides: "only four days of the week".
- The government changed the date for its eastern half on 31 December 1994 (Phoenix and Line Islands moved to UTC+13:00 and UTC+14:00); "Friday, 30 December 1994, was followed by Sunday, 1 January 1995" -> the eastern half has no Saturday 31 December 1994 (its New Year's Eve).
- The line moved about 1,000 km east around the country; the Line Islands, including Kiritimati, "started the year 2000 on its territory before any other country on Earth" (the article marks the tourism claim as needing a citation) -> VO "greet every new year before any other country" and the description says "UTC+14".
- Tone/wording: "half of this country" = the eastern half (Phoenix and Line Islands, a small share of the population; most people live in the Gilberts). The VO says "half of the country", the description clarifies "its eastern islands".
- Not checked: whether the eastern islanders held a New Year's Eve party earlier/later; the VO says "No New Year's Eve party in 1994" as a joke about the missing date, not a fact about events. Keep that framing in the description ("the date never happened there").

## Title, description, tags (draft; goes into publication.md after the render)
Titles: 1) "This Country Deleted New Year's Eve 🎆"  2) "Half of This Country Never Had December 31st 😳"  3) "This Country Lived in Two Days at Once 🌏"
Description: Kiribati straddled the International Date Line, so its eastern islands were almost a full day behind the west, and the two halves could do routine business only four days a week. In 1994 the country moved the date line around all its islands: the eastern half went from Friday, 30 December 1994 straight to Sunday, 1 January 1995, so Saturday, 31 December (New Year's Eve) never happened there. Its islands are now the first in the world to greet each new year (UTC+14). Sources: Wikipedia "Time in Kiribati", "Kiribati", "International Date Line". All scenes are AI-generated illustrations. AI voice.
Tags: kiribati, date line, international date line, new year, time zones, utc+14, geography, facts, deleted day, samoa, shorts.

## Cover plan (after the render, free from keyframes or $0.04 at 2K; same mechanics as the Gold cube / Suez covers)
Big contrast: a party table under an empty calendar hook with a huge red strike through "31", title "NO NEW YEAR'S EVE?" (Titan One, yellow + white), small "AI CONCEPT" tag, a map strip of the Pacific with the date line on top.

## Cost (spent 2026-10-15: 6 keyframes at 1K = $0.12 + 6 Grok clips $0.648; voice and cover still to do)
6 keyframes at 1K = $0.12 + 6 Grok clips = $0.648 + Lumean voice ~0.25 RUB + cover free = about $0.77.

## Checks before delivery (standard QC)
1080x1920 30 fps, -14 LUFS, caption sync, frame sheet over the whole timeline, dates/numbers match the VO (1994, Friday 30 December, Sunday 1 January, four days, UTC+14, ~1,000 km), no readable text in AI frames, no flags with emblems, chat copy under 30 MiB, no secrets in the repo.

## Clip QC notes (2026-10-15)
- K1 clock ticks to midnight, the family cheers, a blank page drops and covers the frame (good transition into scene 2).
- K3: only the left official moves (he waves); the right one is almost static. Use a light zoom to hide it.
- K6: the first 2 s are wide; from ~3.5 s it is a close-up of the girl and the cake (she may look like she blows the candles). Use the 2-5 s range at the engine level.
- K2, K4, K5: clean, strongest clips (the line lights up, the page flies away, sunrise + firework).
