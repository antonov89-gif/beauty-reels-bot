# Emotion map, ep.1 "My Morning" (owner 29.10: "use emotions, this is important")
Rule for the whole series: the king is never flat. Every line carries a named emotion in the VOICE (tags in voice/lines_ep1_emotion.json, pace, pauses, vowel stretching, small non-verbal sounds) AND in the FACE and body of the clip prompt. Emotional arc of the episode: irritated command -> smug welcome (the one self-praise line) -> proud conspiracy -> smug satisfaction -> mock-tragic wound -> prophetic joke -> bored regality -> petty outrage -> flirtation with his own ankle -> showman glee -> snapped irritation then swoon -> sly generosity -> gleeful exit to the feast.

| Clip | Voice emotion (tags, delivery) | Face and body (put into the Kling/Veo prompt) | Non-verbal beat |
|--|--|--|--|
| C01 | irritated and sharp "Marcel, down!", then regal command, drawling smug welcome, self-admiring "that handsome", sneering amusement on "faint" | eyes roll up to the ceiling, jaw tight, then chin lifts, slow smirk, one eyebrow up on "faint" | short exasperated exhale after "down" |
| C02 | conspiratorial pride, a soft laugh into "opening night" | leans in toward the lens as if sharing a secret, eyes sparkle, tiny head tilt | small satisfied "hm" |
| C03 | dry boredom for the doctor, then smug pleasure that everyone came for him, a satisfied "naturally" | glances at the doctor and away, eyelids heavy, then eyes shining at the crowd, a pleased smile | a satisfied breath before "Naturally" |
| C04 | brisk, mock-tragic sigh, wounded pride, dry resolve | hand on the chest, lower lip pushes out, brow knits, then lifts chin | a sigh on "falling out" |
| C05 | smug, lofty, a soft sigh of contentment (no praise line) | strokes the tall wig, closes his eyes for a moment, opens them to the lens | contented sigh |
| C06 | theatrical savouring of each word, prophetic, mock-modest chuckle | holds the white wig up like a relic, eyes shine, a modest lowered gaze on "early" with a sly smile | chuckle |
| C07 | regal boredom, then proud showman of the new wig | slow blink, a shimmy of the shoulders, shows off the wig with an open hand | delighted "mm" |
| C08 | contemptuous, then tender on "I love listening", snort of laughter on "to myself" | sweeps a withering look over the court, softens to a fond smile at the lens | snort-laugh |
| C09 | sharp scandalised "Lower", outraged whisper "that is a hat", recovering haughtiness | eyes widen, nostrils flare, mouth tight, then smooths his face and lifts his nose | a sharp inhale |
| C10 | flirtatious, teasing; proud on "the tallest" | turns the foot like a jewel, eyebrow raised | proud sniff |
| C12 | showman grandeur, gleeful, soft laugh on "every single one" | strides with open arms, delighted grin, glances left and right at his reflections | soft laugh |
| C13 | snapped irritation, then imperious dismissal | head snaps to the courtier, glare, flicks a hand: go, further | sharp exhale |
| C14 | mock-generous, firm "Do not stare", sly conspiratorial "a little", then imperious "Subscribe to my stunning channel" | open palm, stern finger, a wink and a tiny smile, then a regal point at the lens | small laugh |
| C15 | imperious commands ("Hit like. Ring the bell."), dismissive boredom ("do what you like"), THEN a cold, arrogant, haughty laugh (owner 29.10: the laugh comes after "do what you like"), gleeful hunger ("off to the table to feast") | commands with a finger, waves the audience away with the back of the hand, then chin lifted, eyes half-closed, looks down his nose and laughs with contempt, turns and strides to the table with a look back over his shoulder | the laugh itself, footsteps, cutlery |

## Voice rules for emotion
- Stability: Natural (0.5) is the safe default; Creative (0.0) gives the tags more effect but can hallucinate. Test both on C01-C05, pick one, lock it. (Lumean accepts only multiples of 0.5.)
- No flat reads: every line starts with a tag; keep the tags short (one or two words); never read a tag aloud (checked by transcription).
- Pace about 0.95, long pauses before the self-praise ("Magnificent", "Me.", "what a profile").
- The face must match the voice: the clip prompt names the emotion on each phrase, and the QC checks the face against the emotion (not only the identity).
