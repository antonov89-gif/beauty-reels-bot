# Evidence Protocol — prove what was observed

## 1. Source gate (mandatory)
Record modality and scope *before* making forensic claims.

|Level|What the assistant has|Allowed conclusions|Not allowed|
|---|---|---|---|
|L0|User pasted a URL only; no fetched media|Ask context or describe accessible general framework|Pretend video was watched|
|L1|Page metadata, title, thumbnail, description, transcript|Packaging, topic, explicit spoken/text content, timing only if transcript actually timestamped|Camera trajectory, beat-sync, edit counts, video physics, acoustic space|
|L2|Accessible still frames or sampled video frames|Visible composition, color, some scene changes, hypothesized motion (only if temporal sequence exists)|Exact sub-second motion without adequate sampling; sound properties without audio|
|L3|Decoded video plus audio covering stated ranges|Per-shot timing, motion, sync and sound for *inspected ranges*|Claims about uninspected footage or nonobservable equipment settings|
|L4|L3 plus dated authorized analytics / creator data|Correlational performance analysis, official CTR/retention when actually provided|Causal proof of algorithmic views from correlations alone|

A transcript is not a substitute for hearing delivery; metadata is not a substitute for video; vidIQ is not a video player. Verify whether *audiovisual content* is truly accessible from the host or file, not just an accessible webpage.

## 2. Coverage register
Keep time ranges separately:
- `INSPECTED_AV`: video *and* audio actually viewed/listened to, whether continuous or sampled.
- `INSPECTED_VIDEO`: frames/playback viewed with no audio.
- `INSPECTED_AUDIO`: audio heard but video unavailable.
- `SAMPLED`: e.g. 1 fps survey — sufficient for composition, not necessarily fast transitions.
- `UNSEEN`: not verified. For long-form report estimated temporal coverage honestly.
- `METHOD`: player, frame extraction, waveform/audio excerpt, tool explicitly supporting video, etc.

For fast editing/action, inspect denser frame sequence where practical; do not infer high-frequency motions from sparse samples. Timing exactness cannot exceed sampling granularity. No need to extract thousands of frames blindly; choose uncertain high-impact intervals.

## 3. Evidence ledger
Minimal record:
```
EVIDENCE_ID: REF-E014
SOURCE: reference YouTube URL / provided video / inspected output
MODALITY: video+audio / frames / audio / transcript / metadata / analytics
TIME: 00:12.10–00:13.30 (or NOT_APPLICABLE)
METHOD: continuous playback / sampled frames 4fps / inspected clip / tool observation
OBSERVATION: shot switches wide→reaction close-up; off-screen siren continues
CONFIDENCE: HIGH / MEDIUM / LOW (strength of evidence, not enthusiasm)
```
Do not create fictional evidence IDs for evidence that has not been inspected. You may use a `PENDING-E###` placeholder only if explicitly marked pending.

## 4. Claim ledger
```
CLAIM_ID: CL-014
CLAIM: "cut is motivated by actor's reaction"
STATUS: OBSERVED / ESTIMATED / UNKNOWN
EVIDENCE_IDS: [REF-E014]
EXPLANATION: transition follows the actor's turn; motivation is interpretation
IMPLICATION: preserve reaction-led rather than timer-led cutting
```
Separate directly visible action (`OBSERVED`) from inferred camera rig, lens, software, AI tool, motivation or reasons a video went viral (`ESTIMATED`). Never call an estimated 35 mm or 24 fps a measured camera setting without metadata. If a claim has no source, label it `UNKNOWN` and do not drive costly generation decisions from it.

## 5. Production trace
```
PRINCIPLE_ID: DNA-04
CLAIM_IDS: [CL-014]
GENERAL_RULE: reaction-led cut when information changes
ORIGINAL_BEAT: hero hears noise off-screen; close-up reaction before reverse angle
RISK: copying original event/shot too literally; change setting, action, framing
```
Purpose: transfer filmmaking logic, not protected expression. A principle supported by weak evidence may still be used creatively, but label it a *creative choice*, not a reference fact.

## 6. Views/analytics integrity
Dated and attributed source records should preserve `source`, `as_of`, `public metric`, `channel context`, `scope`, and caveat. Do not manufacture retention graph, CTR, watch time, subscriber conversion, demographics, or reasons for distribution. Use observed public views/outliers to form testable hypotheses, not causality claims.

## 7. Tooling-aware sampling (optional)
For user-provided video files in a compliant local environment, `ffprobe` can reveal technical streams and `ffmpeg` can extract keyframe/sample images and audio ranges. Tools vary; do not imply either has been run unless it actually was. 1 fps is a coarse scouting sample, **not** a shot-boundary gold standard. High-action cuts may need dense inspection near each cut. Never download copyrighted content using unauthorized means; respect source licensing/access.

## Evidence gate checklist
- Is modality confirmed?
- Do inspected ranges support all cited timestamps?
- Are estimates distinctly marked?
- Are important production choices traceable to direct evidence or explicit creative invention?
- If not, do more inspection when possible, otherwise narrow the claim.
