# GTA 6 ep.2 (about 90 s, 9:16): "Guess the REAL Vice City spot"

Mechanic: the voice gives only a visual clue ("Look at the hotels"), a 2-second GUESS timer runs over the game-style clip, then a GAME/REAL slider wipe reveals the real place on Esri satellite with a pin, name and one animated fact. Between spots a car icon drives the route on the real Miami map with a mileage counter; a round mini-radar HUD (own design) sits in the corner; score counter 1/6..6/6; ending "How many did you get?".

Frames and clips: made by the channel owner from prompts.md (H0, P1-P6 / A0-A6).
Voice: Lumean ElevenLabs "David", 150 words, 67.9 s, 0.4 RUB (Whisper check OK; "Kaseya" sounds like "ka-SAY-a").

## Route (real order, a loop)
Ocean Drive -> MacArthur Causeway -> Kaseya Center -> Metromover (downtown) -> Wynwood -> Venetian Causeway.

## Facts (checked 16 Oct 2026)
- Art Deco District: listed on the National Register 14 May 1979, about 800 buildings (Miami Design Preservation League; Greater Miami CVB).
- MacArthur Causeway: about 3.5 miles, opened 17 Feb 1920 (Wikipedia; Big Bus Tours).
- Kaseya Center: opened 31 Dec 1999, 19,600 seats for basketball, Miami Heat (Wikipedia; Stadium Journey).
- Metromover: opened April 1986 with a 25-cent fare; free since the 2002 transit tax (Miami Today; Jon Bell; Miami-Dade fares page). 4.4 miles, 21 stations.
- Wynwood Walls: created by Tony Goldman in 2009 in old warehouses (Wynwood Walls; Bisnow).
- Venetian Causeway: 12 bridges, 2 bascule (lifting) spans; about 2.5-2.8 miles; built 1925-1927 (FDOT; Wikipedia).
- Trailer links are reported by outlets (Dexerto, New Times, Sportskeeda, Kotaku), not confirmed by Rockstar: wording "look exactly like".

## Progress (16 Oct 2026)
- Clips received from the owner: A0 (hook), A1 Ocean Drive, A2 MacArthur, A3 arena, A4 Metromover, A6 Venetian. Missing: A5 (Wynwood).
- Used windows: A0 0-6 s (later the skyline turns into generic towers); A1/A2/A4/A6 first 3.8-4 s; A3 from 1.4 s with a crop (zoom 1.22, x 0.62, y 0.30) that hides the AI-made game HUD in the bottom-left corner and the "P3 ARENA" text on the LED wall; A4 after 5.5 s tilts into a black train underside (not used).
- Clips contain car shapes close to real sports cars (no logos visible); fine for concept art.
- Engine50: hook with 3-2-1, clue (GUESS ring 2.0 s), reveal with GAME/REAL wipe + Esri satellite + pin + counters, route interludes with mileage counter, final map with 6 pins. Total 86 s, voice re-placed on the gapped timeline, loudness -14.1 LUFS.

## QC fixes (16 Oct 2026, second pass)
- FACT FIX: the first render said "free to ride since 1986". Wrong: the fare (25 cents) was dropped in 2002. Voice re-recorded (0.41 RUB) with "since 2002"; on-screen "SINCE 2002".
- Wording: "protected since 1979" changed to "on the National Register since 1979" (voice) and "HISTORIC DISTRICT · 1979" (screen): 1979 is the National Register listing, local protection came later.
- In the new take TTS said "live for boats" instead of "lift"; line 12 is taken from the first take (spliced, timing rebuilt in timing.json, audio from lumean/combined.wav).
- Arena clip A3 slowed to 0.6x so the clue stays in the clean part (LED text "P3 ARENA" appears later in the clip).
- Timer shows "TIME!" at zero instead of a frozen "0.0". Interludes 3.2 s, end card 3.4 s: total 85.0 s.
- Voice sync measured by onset detection: every line within 0.08 s of its planned start.
