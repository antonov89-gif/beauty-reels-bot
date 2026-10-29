# Premium / more professional voice options (searched 29.10.2026)
Owner: "remember voice 7 (The Young Heir); search for more expensive, more professional voice-over models".
Locked now: ElevenLabs v3 "The Young Heir" via Lumean (voice_lock.json). Cost of that today: 0.23 RUB per order (min 500 chars), about $0.006 per 1000 chars.

## Ranking and prices found (web, treat as secondary; Artificial Analysis arena checked 16.10.2026 per Forasoft)
| Option | What it is | Price | Fit for our king |
|--|--|--|--|
| **ElevenLabs Eleven v4 / v4 Turbo** | top two of the Artificial Analysis TTS arena (Elo 1330 / 1329), above Qwen-Audio-3.1, Cartesia Sonic-3.6, Gemini 3.8 Flash TTS | $0.08 per 1K chars (v4), $0.04 (Turbo) | Best candidate: same voice ids as our lock may work; strongest expressiveness for character voices |
| Respeecher (speech-to-speech) | converts a human actor's take into another voice while KEEPING timing and breath; licensed voice library | custom quote | The professional route to a natural performance: a human performs, we keep the locked voice; also gives real timing for lip-sync |
| Google Gemini TTS | style directed by natural-language prompts ("say it arrogantly, posh") | about $10-15 per 1M chars | Good A/B for direction; no account here |
| Cartesia Sonic 3.6 | latency-first, instant and professional clones | about $37 per 1M chars | Not a character-acting pick |
| Inworld TTS-2, OpenAI gpt-4o-mini-tts, Azure HD, Murf | mid-range, promptable styles | $15-30 per 1M chars | Weaker for a nasty aristocrat |
| Open source (Chatterbox, Orpheus) | emotion control, zero-shot clone from ~5 s of audio | GPU only | Possible later; needs a GPU |
| Human voice actor (Fiverr/Voices.com) | real performance | commercial licence extra; benchmarks $250-750 per finished minute (weak sources) | The only truly natural option; needs a written licence incl. AI processing |
Source caveat: vendor and blog benchmarks; no source tests a posh-British arrogant character. Only our own A/B on our lines counts.

## What we can reach from here
- Lumean: ElevenLabs template shows only `eleven_v3` (a v4 model id may or may not be accepted: unknown until one order is placed).
- Higgsfield catalog has `elevenlabs_v4`, `elevenlabs_v4_turbo`, Seed Audio 1.0, Qwen Audio 3.0 TTS, Text to Speech V2 (ElevenLabs, MiniMax, Seed Speech, Vibe Voice, Cozy Voice), `voice_change` (swap the voice in a clip, keeps timing). The account shows 0.1 credits: needs a top-up.
- vidIQ voiceover: premade ElevenLabs voices only, 14 credits per 1000 chars (949 credits left); no library voices like our lock.
- APIpod: no TTS documented.

## Proposal
1. A/B the same 6-line sample on the locked voice: Eleven v3 (done: heir.mp3) vs Eleven v4 (Lumean model id, 0.23 RUB, if accepted) vs Eleven v4 on Higgsfield (after a top-up).
2. For the most natural result: a human take (the owner or an actor) + speech-to-speech into The Young Heir (Higgsfield `voice_change`, or Respeecher): human timing and breath, locked timbre, lip-sync timing from the take.
