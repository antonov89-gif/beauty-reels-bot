import json, re, sys
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8", download_root="/tmp/claude-0/whisper")
segs, info = m.transcribe("voice_raw.wav", language="en", word_timestamps=True, beam_size=5, vad_filter=False)
words = []
for s in segs:
    for w in s.words:
        words.append((w.start, w.end, w.word.strip(), w.probability))
json.dump(words, open("asr_words.json", "w"))
print(len(words), "words", info.duration)
