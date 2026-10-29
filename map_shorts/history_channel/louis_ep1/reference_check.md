# Ep.1 reference check (statuses: GENERATED != INSPECTED != APPROVED)

## C01 start frame, frames/C01_ceiling.jpg (29.10, $0.04)
Status: GENERATED, INSPECTED (by us), not APPROVED by the owner.
Check: painted gilded baroque ceiling, gold canopy top at the lower right, a black hat with a white plume at the lower left (our phone-mistake device, not the reference thumb), no people, no faces, no modern objects. Soft defect: a skylight at the top edge (the real state bedchamber has none); accepted because the camera leaves the ceiling in 1.3 s. Kling character refs switched to night-wig images only (D2_morning, C01, C02, C03).

## C01 clip, Kling 4.0 r2v, 12 s 1080p (owner said yes, about $2.55)
Attempt 1 (task 940f34aa): FAILED by the provider: "Not enough speech in the voice audio. Please use a 5-30 second clip with clear speech and no long pauses." (voice ref heir_fr_sample.mp3, 12.8 s with pauses).
Attempt 2 (task dda11367): FAILED with the same message, voice ref heir_fr_ref_speech.mp3 = 23.7 s of continuous speech (no pause >= 0.3 s at -40 dB, mp3 48 kHz mono, URL checked: 200, audio/mpeg).
No cost field in either failed status; APIpod has no balance endpoint, so "not charged" is NOT VERIFIED. Two corrective attempts used: method reassessment goes to the owner (no third attempt without a decision).
Attempt 3 (task 7bf475e6, owner chose "C": same 23.7 s reference as WAV 44.1 kHz 16-bit mono): FAILED, same message. Kling r2v does not accept our synthetic French-accent voice as a voice reference (3 of 3). Also found in the official spec (docs.apipod.ai, kling-4.0-r2v.yaml): r2v `image_urls` are REFERENCE images (@image_N), not a first frame, so the ceiling would not have been the opening frame anyway.
Method reassessment (to the owner): kling-4.0-i2v takes a real first frame, up to 8 keyframes and a last frame (3-30 s, about $0.145/s at 720p from the estimator; 1080p rate NOT VERIFIED). seedance-2.0-r2v takes `audio_urls` (needs an image) but no first frame; its lip-sync to a given audio is undocumented.
