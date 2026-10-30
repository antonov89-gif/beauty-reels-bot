# Lines vs the reference: meaning and delivery (30.10.2026, owner: "Сравни с референсом реплики смысл и подача")
Reference = "Elizabeth I - vlog 1" (LjfGP7wpjVs; lines read from the burned-in captions on frames, map_shorts/ref_tudor_vlog_2026_10_28/frames_vlog1_LjfGP7wpjVs.md) and "Tower of London" (lBkoOcM-r5k; Nexlev transcript, one_link_studio_lBkoOcM-r5k.md). Ours = voice/lines_ep1_emotion.json, episode 1 (C01-C15, no C11). Pace numbers from compare_reference_ep1_v2.md (measured).

## Meaning
| What the reference does | Reference example (verified) | Ours | Gap |
|--|--|--|--|
| Premise: says WHY she films | "My advisors say a queen must be seen by her people. So here I am being seen." | C01: "Welcome to Versailles. Yes, I'm that handsome. Try not to faint." (no reason to film) | MISSING |
| Confession + real fact + a turn | "When I was 29 I caught the small pox... It left these." -> "my ladies paint me white. White lead and vinegar." ; "I was here as a prisoner... I was 20... This time, I have the keys." | Only C04: "My hair started falling out at seventeen. I took it personally." Others are boasts. | 1 of 14 lines (theirs: the spine of every take) |
| Surprising anecdote told straight | "a bishop pulled out his own tooth to show me it was brave. My remedy: a golden toothpick." | Facts exist (C02 lever, C03 doctor/surgeon, C10 red heels, C12 357 mirrors, C14 dinner in public) but each is bent into a vanity joke | Facts are props, not stories |
| Reaction to an accident, laughs at herself | tray of almonds spills: "Saints preserve me", she laughs to tears | C09 "and there goes the hat" (reaction, good); C13 "Don't stand behind me..." | OK in 2 clips; no moment where he laughs AT HIMSELF |
| Self-correction, live feel | "Why am I upside down? Good. Right. Good." | C01 "Oops, the ceiling. There." | OK (own version) |
| Period colour in words | "Good morrow", "my sweet peasants", "Saints preserve me" | none | MISSING (bible allows a few: "Magnifique", "mon Dieu", "my friends") |
| Outro = next-episode tease + a self-aware joke | "Next time I will show you my routine and how I cover the scars. So keep an eye on my... oh yes, profile." | C14 "Tonight I dine in public..." (tease) + "Subscribe to my stunning channel." + C15 "Hit like. Ring the bell..." | Tease OK, CTA is two clips long |
| Joke density | most lines are plain information, deadpan; the humour comes from the situation | 9 of 14 lines end on a "statement + smug tag" pair ("To myself, mostly", "I'm just early", "of course", "Naturally", "I took it personally", "and I'm in every single one") | Too many tags; the series bible itself bans stock punchline pairs |
| Tone range | vain but also vulnerable, curious, giggling | one note: smug/arrogant in every line | No soft moment |

## Delivery
| Measure | Reference | Ours |
|--|--|--|
| Pace | 83-99 wpm; 2.5-3.1 words per speaking second | lines 10-21 words per 8-9 s clip (204 words / 14 clips); C02-C05 old takes 120-156 wpm; r2v takes: C09 about 130, C10 about 135 wpm |
| Pauses | 7-9 pauses > 0.5 s per 25-30 s take | 1-3 per clip; the r2v model adds its own (C10: 1.5 s before the last sentence) |
| Thought length | one topic per 24-30 s take, told in several sentences | one topic AND one joke per 8 s |
| Sentence shape | spoken, unfinished, "well", "so", "and yes" | written, every sentence complete and polished |

## What to change (principles only, no reference phrases copied)
1. C01: add a reason to film, in our words (for example "The whole court watches me all day. So, now you can too.").
2. Turn 2-3 boasts into confession + fact + turn like C04 (candidates: C06 powder, C08 nobody may speak first, C12 mirrors).
3. Keep at most one smug tag every two clips; the rest plain, deadpan, with a 0.6-1 s pause.
4. One human moment: he laughs at himself once (C09 hat, or C13).
5. One or two French words in the episode ("Magnifique", "mon Dieu").
6. Merge the outro into one clip: the tease of episode 2 + one CTA joke.
7. Max about 14 words per 8 s and spoken shape ("so", "well", unfinished sentences).
Cost of changing: C09 and C10 are already generated (keep). C01-C08 are to be redone anyway, C12-C15 are not generated yet: new lines only need new reference audio = Lumean TTS orders (about 0.23 RUB each, own yes).
