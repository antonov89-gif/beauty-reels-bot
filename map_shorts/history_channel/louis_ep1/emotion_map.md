# Emotion map, ep.1 "My Morning" (owner 29.10: "use emotions, this is important")
Rule for the whole series: the king is never flat. Every line carries a named emotion in the VOICE (tags in voice/lines_ep1_emotion.json, pace, pauses, vowel stretching, small non-verbal sounds) AND in the FACE and body of the clip prompt. Emotional arc of the episode: irritated command -> smug welcome -> proud conspiracy -> swooning self-love -> mock-tragic wound -> prophetic joke -> bored regality -> petty outrage -> flirtation with his own ankle -> showman glee -> snapped irritation then swoon -> sly generosity -> gleeful exit to the feast.

| Clip | Voice emotion (tags, delivery) | Face and body (put into the Kling/Veo prompt) | Non-verbal beat |
|--|--|--|--|
| C01 | irritated and sharp "Marcel — down!", then regal command, drawling smug welcome, self-admiring "that handsome", sneering amusement on "faint" | eyes roll up to the ceiling, jaw tight, then chin lifts, slow smirk, one eyebrow up on "faint" | short exasperated exhale after "down" |
| C02 | conspiratorial pride, a soft laugh into "premiere" | leans in toward the lens as if sharing a secret, eyes sparkle, tiny head tilt | small satisfied "hm" |
| C03 | dry boredom for the doctor, mock puzzlement, then commanding and breathy, swooning on "Magnificent" | glances at the doctor and away, eyelids heavy, then eyes wide and shining at his own reflection, lips parted | a breath in before "Magnificent" |
| C04 | brisk, mock-tragic sigh, wounded pride, dry resolve | hand on the chest, lower lip pushes out, brow knits, then lifts chin | a sigh on "leaving" |
| C05 | smug, lofty, a soft sigh of delight | strokes the tall wig, closes his eyes for a moment, tastes the compliment, opens them to the lens | sigh of delight |
| C06 | theatrical savouring of each word, prophetic, mock-modest chuckle | holds the white wig up like a relic, eyes shine, a modest lowered gaze on "early" with a sly smile | chuckle |
| C07 | regal boredom, then delighted preening | slow blink, then a pleased little shimmy of the shoulders, admires his sleeve | delighted "mm" |
| C08 | contemptuous, then tender and adoring on "Me", snort of laughter | sweeps a withering look over the court, softens to a fond smile at himself in the lens | snort-laugh |
| C09 | sharp scandalised "Lower", outraged whisper "that is a hat", recovering haughtiness | eyes widen, nostrils flare, mouth tight, then smooths his face and lifts his nose | a sharp inhale |
| C10 | flirtatious, teasing; admiring sigh at his ankle | turns the foot like a jewel, eyebrow raised, lip bitten in admiration | admiring sigh |
| C12 | showman grandeur, gleeful, soft laugh on "Lucky mirrors" | strides with open arms, delighted grin, glances left and right at his reflections | soft laugh |
| C13 | snapped irritation, then swoon on "what a profile" | head snaps to the courtier, glare, then turns to the mirror and melts, hand to the cheek | breathy "Ah..." |
| C14 | mock-generous, firm "Do not stare", sly conspiratorial "a little", then imperious "Subscribe to my stunning channel" | open palm, stern finger, a wink and a tiny smile, then a regal point at the lens | small laugh |
| C15 | imperious commands ("Like it. Ring the bell."), a rich delighted villainous laugh, dismissive boredom ("do what you like"), gleeful hunger ("off to the table to feast") | commands with a finger, head thrown back laughing, waves the audience away with the back of the hand, turns and strides to the table with a look back over his shoulder | the laugh itself, footsteps, cutlery |

## Voice rules for emotion
- Stability: Natural (0.5) is the safe default; Creative (0.0) gives the tags more effect but can hallucinate. Test both on C01-C05, pick one, lock it. (Lumean accepts only multiples of 0.5.)
- No flat reads: every line starts with a tag; keep the tags short (one or two words); never read a tag aloud (checked by transcription).
- Pace about 0.95, long pauses before the self-praise ("Magnificent", "Me.", "what a profile").
- The face must match the voice: the clip prompt names the emotion on each phrase, and the QC checks the face against the emotion (not only the identity).
