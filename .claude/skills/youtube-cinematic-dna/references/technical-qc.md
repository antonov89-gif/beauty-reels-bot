# Cinematic Technical QC — only load for shot generation, comparison or repair

## Camera
- Define scene geography and axis of action. Use 180° / eyeline / screen direction where they improve orientation; motivated crossings and jump cuts can be intentional.
- Character blocking drives camera choice. Record physical rig impression (locked, handheld, dolly, gimbal, crane, drone, vehicle) and camera start/path/end. Avoid floating, unmotivated orbit, instant acceleration and endlessly identical push-ins.
- Distinguish camera position from focal length. Lens family is an estimate unless verified. Preserve credible parallax, lens perspective, focus behavior, horizon and camera inertia.
- Motion blur should agree with movement. A 180° shutter near 24fps is a common baseline, not an instruction for every genre; do not invent camera metadata.

## Animation and physics
- Check anticipation, mass, center of gravity, acceleration/deceleration, object contact, secondary motion and aftermath; do not enforce generic anticipation on every spontaneous action.
- Human: feet grip ground, weight transfers, face and eye reactions have motivation, hands interact with props convincingly, clothing/hair follow momentum.
- Vehicle: tires spin coherently, suspension and body roll respond to road/steering, reflections change with viewpoint, damage and model remain consistent.
- Scene: environmental wind/rain/particles agree with lighting and motion; background people and geometry are temporally stable.

## Lighting, image and compositing
- Light is motivated by practical sources or an intentional filmmaking setup; check direction, shadow softness, specular response, reflected light, exposure, skin/material texture and continuity.
- Preserve intentional highlights/shadows without indiscriminate HDR, plastic skin, over-sharpening, excessive teal-orange/neon, bogus text or uniform background blur.
- Foreground/midground/background layers should have purpose; no mandatory artificial foreground objects. FX must agree with perspective, grain, focus, contact shadow, motion blur and exposure.

## Sound and performance
- Check real ambience/room tone when appropriate, differentiated near/far sound, room/reverb continuity, footsteps and contact Foley sync; avoid whoosh/impact overuse.
- Voice: intent/subtext, breaths, conversational pauses, pitch variability, pronunciation, stable character timbre, lip sync with face performance and physical state.
- Edit to story, reaction, action and information, not fixed cut intervals. Use hard cuts by default but not as a universal rule.

## Diagnostic gates
HARD FAIL (fix/regenerate): conspicuous identity drift, extra limb, melting face, mismatched vehicle, obvious warped architecture, physically impossible central action, broken action continuity, gross lip-sync/voice mismatch, intelligibility failure.
SOFT ISSUE (edit/grade/sound): slight camera over-smoothing, repeated angle, minor pacing flatness, overprocessed highlights, uniform music, thin ambience, low priority background flaw.
Do not treat numerical quality scores as objective measurement. If using a /10 rating, define criteria, confidence, and qualitative reasons. Better to return defect + severity + exact fix than a single cosmetic score.

## Integrity
Do not represent fabricated footage as real news or documentary evidence. Cinematic realism and creative fiction are fine; provenance statements should be truthful wherever material.

## Evidence-linked pass standard (V5.1 addition)
- A well-phrased prompt is not proof of good video. Only inspectable audio/video artifacts can pass production QC.
- Hard failures block approval until the repaired artifact is actually re-viewed. A numerical rating without defect-specific evidence is not an acceptance test.
- Review at shot level **and** at sequence level. Adjacent shots can introduce axis, action, environmental or acoustic continuity defects that an isolated good-looking shot conceals.
- The desired perception is professionally directed fiction and natural performance, not deception about actual events. For factual footage label synthetic reconstructions appropriately.
