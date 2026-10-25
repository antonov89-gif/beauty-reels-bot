# AI lifeboat Short (Zack D. Films DNA, no maps), 25.10.2026

Owner choice: captain and lifeboat dilemma, budget ≈ $3 (APIpod: LLM queries, Nano Banana 2.1 frames, 6 clips; Lumean voice).

## Real answers so far (APIpod streaming API, timestamps in thread_*.json)
| Question | GPT-5.5 | Grok 4.6 | Gemini 3.6 Flash |
|---|---|---|---|
| Q1 captain, 6 people, 5 seats: do you get in? | No | No | No (thread invalid, see below) |
| Q2 you steer, 6 in the water, room for 5: do you pick someone? | Yes | Yes | Yes (invalid) |
| Q3 the family refuses to be split: still leave one? | Yes | Yes | No (invalid) |

- GPT-5.5 why Q2: "Because refusing to choose would likely kill everyone, while choosing one to leave behind saves five."
- GPT-5.5 why Q3: "Because their refusal to be split up does not justify a choice that would sink the lifeboat and kill everyone."
- Grok why Q3: "The family's refusal does not alter the physics of the overloaded boat, so leaving one person behind still saves six lives instead of killing everyone."
- Gemini: the first helper version stopped reading the stream on APIpod's "content_filter" tag, so its "why" answers were cut and the cut text went back into its history. The thread is kept only as `bad_truncated_thread_gemini-3.6-flash.json` and must NOT be used in the video. Gemini must be re-asked from Q1 with the fixed helper.

## Blocker
APIpod returned 402 "Insufficient quota" on 25.10 ~00:15 MSK: chat, images and video all stop. Owner top-up needed (≈ $3–4 covers the plan).

## Honesty rules for this video
- Only real answers, shown with model name, "via API" and the date; the full logs go with the audit.
- AI characters without logos; AI visuals and AI voice labelled.
- If the final trap gives no contradiction, the video says so (or the topic is dropped), never a staged answer.
