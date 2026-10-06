import numpy as np, soundfile as sf, subprocess, json
SR = 44100
tm = json.load(open("timing.json"))
v, sr = sf.read("voice_kokoro.wav")
if sr != SR:
    v = np.interp(np.arange(int(len(v) * SR / sr)) * sr / SR, np.arange(len(v)), v)
TOTAL = len(v) / SR + 2.5
N = int(TOTAL * SR)
t = np.arange(N) / SR
# warm documentary bed: slow chord pads + soft plucked arpeggio, A minor / F / C / G at 84 bpm
bar = 60 / 84 * 4
prog = [(220.0, [1, 1.189, 1.498]), (174.61, [1, 1.26, 1.498]), (261.63, [1, 1.26, 1.498]), (196.0, [1, 1.26, 1.498])]
mus = np.zeros(N)
rng = np.random.default_rng(2)
for b in range(int(TOTAL / bar) + 2):
    root, iv = prog[b % 4]
    i0 = int(b * bar * SR); n = int(bar * 1.25 * SR)
    tt = np.arange(n) / SR
    env = np.minimum(1, tt / 0.8) * np.exp(-tt / 4.5)
    pad = sum(np.sin(2 * np.pi * root * k * tt) + 0.25 * np.sin(4 * np.pi * root * k * tt) for k in iv) * env * 0.10
    pad += np.sin(2 * np.pi * root / 2 * tt) * env * 0.18
    for j in range(8):
        st = int(j * bar / 8 * SR); m = int(0.6 * SR)
        f = root * iv[j % 3] * (2 if j % 4 == 3 else 1)
        pt = np.arange(m) / SR
        seg = np.sin(2 * np.pi * f * 2 * pt) * np.exp(-pt * 7) * 0.05
        e = min(n, st + m); pad[st:e] += seg[: e - st]
    e = min(N, i0 + n)
    if e > i0: mus[i0:e] += pad[: e - i0]
mus *= np.minimum(1, t / 2.0) * np.clip((TOTAL - t) / 3.0, 0, 1)
mus = mus / np.abs(mus).max() * 0.7
voice = np.zeros(N); voice[: len(v)] = v[:N]
sf.write("voice44.wav", voice, SR); sf.write("music.wav", mus, SR)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", "voice44.wav", "-i", "music.wav", "-filter_complex",
  "[0:a]asplit=2[v][vsc];[1:a]volume=0.28[m];[m][vsc]sidechaincompress=threshold=0.05:ratio=6:attack=10:release=450[md];"
  "[v][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.95,aresample=44100[a]",
  "-map", "[a]", "mix.wav"], check=True)
print("mix", TOTAL)
