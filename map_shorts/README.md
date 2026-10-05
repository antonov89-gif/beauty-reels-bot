# Map-animation Shorts (GeoGlobeTales style)

Code for 9:16 satellite-map history Shorts. Assets are downloaded, not committed:

- `assets/ne50/` Natural Earth 50m admin-0 countries
- `assets/B1.jpg`, `assets/C1.jpg` NASA Blue Marble 21600 tiles -> `python3 build_tex.py`
- `assets/Poppins-*.ttf`, Noto Color Emoji (apt `fonts-noto-color-emoji`)
- `assets/kokoro.onnx`, `assets/voices.bin` (kokoro-onnx v1.0), `pip install kokoro-onnx pyshp soundfile`

Pipeline: `tts10.py` -> `engine.py info` -> 6 parallel `engine.py video A B cK.mp4` -> `audio10.py` -> concat + mux -> `srt10.py`.
Finished episodes live in subfolders (videos are git-ignored).
