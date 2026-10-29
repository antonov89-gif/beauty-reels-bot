# Channel registry and style bibles (27.10.2026)
Rule (CLAUDE.md): references are routed by niche; styles are never mixed; say the channel before production.

## 1. Mr. Buck: GEOGRAPHY (the only channel connected to our publishing)
- Accounts: YouTube mr.buck000 (Zernio account 6add13efdae3320d1b3875af; vidIQ channel UCFphFU69Tgz3LyHoZzODdWw), TikTok mr.buck222 (Zernio 6add1421fe3164c3e42a7f80).
- Niche: maps, borders, countries, routes, size and population comparisons, geography stories where a map is the hero (e.g. Iraq's 58 km door).
- Visual identity (keep it recognisable):
  - accurate Esri-free base (NASA Blue Marble, Copernicus Sentinel-2, Natural Earth), restyled as a tilted premium 3D map (Nano Banana edit) and animated (Veo);
  - our graphics on top: top banner with the claim, rotated red stamps, chips with numbers, captions of 2–4 words with the active word yellow;
  - own synth beat + SFX on every event; no human mascots of real nations; no third-party logos;
  - frame 0 = the map already moving + a 3–5 word claim.
- Story formula: giant vs tiny number -> villain -> "Wait, but…" -> hidden stake -> mechanism -> punch -> binary question. See `views_playbook_2026_10_27.md`.
- Gates: `prompts/premium_gate.py` + authenticity audit; AI flags ON; sources in the description.

## 2. Stories channel (other channel; NOT Mr. Buck; account not connected yet)
- Niche: true human stories told in 3D (the Zack D. Films family: Sullivan lightning, liver regrowth, the lost-boy ideas).
- Visual identity (its own, never used on Mr. Buck): game-engine 3D characters (STYLE v2 in `prompts/style_zackd_3d_render.md`), a continuous always-moving camera, motion transitions instead of cuts, memory-bubble insets with a glowing torn outline, a cold/warm colour code, one costume per character, white 1–3 word captions at ~78 % height, cultural accuracy of the set.
- Production: youtube-cinematic-dna V5.1 (frames -> pilot -> batch), AI disclosed.
- Publishing: needs the channel's own accounts connected to Zernio; until then files are delivered to the owner only.
- **Fiction allowed (owner, 27.10):** original invented stories are fine on this channel. Fiction audit instead of the facts audit: (1) the description says "a fictional story"; nothing is claimed as true, as news or as a real case; (2) no real person's name, likeness or brand; a real disaster is not retold with invented details as if real; (3) AI disclosed + flags ON; (4) no gore, no violence against children, not made for kids; (5) originality: not a copy of a reference's characters, scenes or wording (PHASE 96); (6) the premium_gate.py report. Real events may only be used with checked facts and "inspired by".

## 2b. History POV channel (other channel; NOT Mr. Buck; account not connected yet; brand DRAFT)
- Project: map_shorts/history_channel/project.json (channel-style-dna). First series: Louis XIV vlog (character card v2, white-grey wig main, documentary-vlog look, camera grammar from the Elizabeth reference).
- **Voice rule (owner, 28.10.2026): ONE voice on all videos of this channel; nasty (smarmy), arrogant, haughty.** So the voice is TTS (one fixed ElevenLabs v3 voice_id + settings, LOCKED 29.10 in map_shorts/history_channel/voice/voice_lock.json: ElevenLabs v3 'The Young Heir'), not the generator's native speech (it drifts between clips). The clips' own speech is muted; ambience and foley stay.
- Facts allowed for real monarchs (owner exception, 28.10): dead 150+ years, two sources, comedy framed, AI disclosed.

## 3. Routing log
| Date | Reference | Niche | Routed to |
|--|--|--|--|
| 27.10 | jPCF80Bte8s Congo's 23-mile coast | geography | Mr. Buck (made: Iraq) |
| 28.10 | @tudor.with.elizabeth (Queen Elizabeth I vlogs, 1.55M top) | history character POV vlog | Another channel (proposed: history POV vlogs); NOT Mr. Buck; plan in ref_tudor_vlog_2026_10_28 |
| 28.10 | @ChloeVSHistory (time-traveller POV, 418k subs, monetized) | history time-travel POV vlog (AI) | Another channel (same history POV channel as the Tudor reference); NOT Mr. Buck; plan in ref_chloe_2026_10_28 |
| 27.10 | uIC4AZP3wx4 crafter duck, wooden orthopedic shoes (real footage, 660M views) | DIY craft process, no voice | Another channel (owner, 27.10); parked, not Mr. Buck, no questions needed (see dna_uIC4AZP3wx4.md) |
| 27.10 | oMkomhg6s9o Zack D., Saroo / Google Earth | a human story (the map is only a prop) | Stories channel; its style is NOT taken by Mr. Buck |
| 26.10 | c3aRLh3SoAs, JUni9wxjZcU (Zack D. style) | story / science | Stories channel (Sullivan, liver) |
