# Authenticity audit, Lofoten v7b (22.10.2026)

Scope: is every statement, image, sound and label in the video true, correctly sourced and honestly disclosed? Checked with frame review, ffmpeg measurements, source pages and web search. Marks: VERIFIED / PARTLY / NOT VERIFIED / FIXED.

## 1. Claims
| Claim | Result |
|---|---|
| "Above the Arctic Circle": Reine 67.93 N, Arctic Circle 66.56 N | VERIFIED by coordinates (about 150 km north of the Circle) |
| "Yet the sea doesn't freeze": Lofoten waters are warmed by the Gulf Stream / North Atlantic Current and stay open | PARTLY: travel and news sources agree, a 1902 Alpine Journal article says the sea is open all year; NO measured sea-ice statistic found. The description says "usually ice-free", the on-screen hook says it flatly. Safer hook if needed: "Yet the sea rarely freezes". |
| Description: "warmed by the North Atlantic Current" | VERIFIED (general), see above |

## 2. Footage (real shots)
| Shot | Source | Result |
|---|---|---|
| Ascend over the ridge | Pexels 39810267 "Aerial sunset hike on Reinebringen ridge" (Clément Proust) | VERIFIED: Reine harbour, bridges and islets visible and match the Esri imagery layout |
| Fjord drift | Pexels 39835660 "Scenic aerial view of Reinebringen fjord" | VERIFIED (title + visible Reine) |
| Close-up cabins | Pexels 39835662 "Aerial view of Reine, Lofoten Islands" | VERIFIED |
| Sweep over islets | Pexels 34425904 "Breathtaking aerial view of Lofoten Islands" (Loic Van Montagu) | PARTLY: title says Lofoten, not Reine; the frames show Reine's fjord and islets (matches the other Reine clips). Described as "Reine and Lofoten". |
| Identifiable people (Pexels prohibited use) | frame scan of all used segments | VERIFIED: none visible in the used segments (hikers appear only at 0-2 s of the ridge clip, not used) |
| Credits | photographers and links in the description | VERIFIED against the vidIQ/Pexels metadata |
| Pexels licence | free commercial use, attribution not required, identifiable people/logos restricted | VERIFIED via search of the Pexels terms; text of the licence page itself was not fetched (403 on pexels.com from this network, not bypassed) |

## 3. AI shots (2 of 7)
| Item | Result |
|---|---|
| Sea-level shot: Nano Banana 2.1 keyframe from a real Reine drone frame, then Veo 3.1 Lite | The cabins are AI-invented, NOT a photograph of the real Reine buildings. FIXED: on-screen label "AI-GENERATED SHOT", description line, YouTube isAiGeneratedContent = true, TikTok isAigc = true. |
| Top-down finale: Veo 3.1 Lite from an Esri satellite crop | Layout (roads, harbour, roofs) stays consistent with the satellite image in the frames reviewed, but individual buildings are generated and the model added propeller artefacts (cropped). FIXED: on-screen label plus Esri credit on screen. |
| Edge-similarity metric vs the start frame | 0.79 at 0.25 s, 0.27 after 2 s (the camera descends and turns, so a low value is expected): NOT a proof of fidelity. Fidelity judged by eye only. |

## 4. Sound
| Item | Result |
|---|---|
| Music: Mixkit "Epical Drums 04" (Grigoriy Nuzhny), Mixkit Stock Music Free License | PARTLY VERIFIED: Mixkit's info page (via search) says the free licence covers commercial projects such as YouTube videos, attribution not required, no use in broadcast/CD/games. The licence text itself loads in a script modal and was not read; Content ID handling is NOT confirmed. Risk: an automatic Content ID claim; if it happens, contact Mixkit. |
| Voice | none |
| Sound effects | none |

## 5. Imagery and data
| Item | Result |
|---|---|
| Esri World Imagery (dive and credit on screen) | Attribution shown on screen and in the description. NOT VERIFIED: whether Esri's terms allow this use (images pulled via the public export service) in a monetised video; same practice as the rest of the channel. Recommendation: have the user check Esri's "Master Agreement / Terms of Use" for the World Imagery basemap or keep Esri frames short. |
| Terrain: AWS Terrain Tiles (Mapzen terrarium) | attribution added to the description |
| Globe: NASA Blue Marble + Natural Earth | public domain |

## 6. Platform policy
YouTube "inauthentic content" (renamed from "repetitious content" 15.07.2025; reused-content rules unchanged): compilations stay eligible when the creator adds value; a mass-produced or only superficially altered video is the risk. Our video adds an original globe/satellite dive, a researched hook, edit and music choice, but most shots are other people's stock footage: assessment MODERATE risk for monetisation, LOW for removal. Mitigations: keep the globe/satellite dive (our own), add a voice-over or on-screen facts in some videos, do not publish many near-identical stock montages. Source: secondary news summaries, not YouTube's own policy page (not fetched).

## 7. Open items for the user
1. Decide the hook wording ("doesn't freeze" vs "rarely freezes").
2. Esri terms check (once, for the whole channel).
3. The AI flags must be switched ON at scheduling (Metricool: isAiGeneratedContent, isAigc).
