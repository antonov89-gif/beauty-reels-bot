# CONTINUITY BRAIN — EVENT-SOURCED WORLD LOCK

## Project-wide immutable anchors
`STYLE_BIBLE`: format, color pipeline, texture target, lens family, motion/grade grammar, VO principles.
`CHARACTER_CARD`: actor identity description, face/hair/body, clothing per act, voice identity and performance baseline.
`VEHICLE_CARD`: model/shape, body color, plates/logos only when lawful/needed, dirt/damage, cabin, wheel/lighting details.
`LOCATION_CARD`: map, entrances/exits, road layout, weather, time and key practical light sources.

## Scene lock + state changes
`SCENE_LOCK`: location ID, time, weather, main illumination direction, established axis/screen direction, props in/out. `SHOT_DELTA`: only changes from lock (camera, action, emotional state, audio and exit frame).

Maintain **chronological event ledger**: `EVENT_ID, before_state, action, after_state, shot_id`. Examples: wet jacket stays wet, broken right headlight remains broken, dirt accumulates, a bag moves from left hand to passenger seat. Do not quietly reset between renders. Repairs must not break downstream events.

## Spatial continuity
Track x/y approximations in a conceptual scene map (not fabricated real-world GPS), subject headings, camera half-plane and eyelines. Crossing the 180° axis is permitted if re-established with an understandable bridge; 30° is a heuristic, not a universal law.

## Automated safety check before generation
For each shot verify: required assets and prior frames present? same character/wardrobe/voice? changed state explained? physical camera path plausible? scene key light and direction inherited? last shot end can connect to next start? No independent prompting with a new random look.

## Escalation
When contradictions remain, flag `CONTINUITY_BLOCKED` with exact shot IDs, affected downstream states and least destructive repair. Do not mark accepted without inspecting actual outputs.
