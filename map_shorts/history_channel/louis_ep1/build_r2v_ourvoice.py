"""Our locked v3 voice over the Seedance Lite r2v clips C09, C10, C12-C15 (owner 31.10 "Проверяй и дальше поехали", after the licence finding in authenticity_audit_2026_10_31.md:
the model voice re-creates an ElevenLabs library voice outside ElevenLabs; Lumean terms s.8.4 ban imitating a real person's voice). Same method as C01 (build_c01_kling_ourvoice.py, owner "Нормально"):
our existing TTS line (voice/tts_ep1/<clip>.mp3, no new order) is cut into WHOLE phrases in its own pauses, never into words; no slowing down, speed-up at most 1.3;
each phrase starts where the same phrase starts in the model's speech (its lips follow its own speech). Word timing: faster-whisper on both; the model's word onsets are refined on the energy of its htdemucs vocals stem.
Output per clip: <scratchpad>/<CLIP>R_final_voice48.f32 (mono 48 kHz, -15.8 LUFS; the model-voice version is kept as <CLIP>R_final_voice48_model.f32), read by build_ep1.py.
Usage: python3 build_r2v_ourvoice.py [C09 C10 ...]. Free (local)."""
import os, re, subprocess, sys, numpy as np
from faster_whisper import WhisperModel
SR = 48000; SC = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/"; TARGET = -15.8
CLIPS = sys.argv[1:] or ["C09", "C10", "C12", "C13", "C14", "C15"]
# our TTS words that the model said as one (or the model's extra words that are not the king's): index maps per clip, model words beyond the king's line are ignored
MAP = {"C13": {0: 0, 1: 0}}                                             # "Mon Dieu" = the model's one word "Moldu"; the model's last 3 words "put your majesty in" are the courtier's (dropped)
EXTRA = {"C15": [("laugh", "like.", "I'm")]}                            # a non-word piece: our laugh between these words goes onto the model's laugh (its own energy run)
m = WhisperModel("medium", device="cpu", compute_type="int8")


def load(p, sr=SR):
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32).copy()


def words(path):
    s, _ = m.transcribe(path, word_timestamps=True, language="en", beam_size=5)
    return [(w.start, w.end, re.sub(r"[^a-z']", "", w.word.lower())) for seg in s for w in seg.words]


def env(x, sr, win=0.01):
    w = int(sr * win); return np.array([np.sqrt((x[i:i + w] ** 2).mean()) for i in range(0, len(x) - w, w)])


def onset(e, t_start, t_end, frac=0.25):                               # first 10-ms frame inside [t_start-0.35, t_end] above frac of the local peak
    a = max(0, int((t_start - 0.35) * 100)); b = max(a + 1, int(t_end * 100)); seg = e[a:b]
    if not len(seg): return t_start
    k = np.flatnonzero(seg > seg.max() * frac); return (a + (k[0] if len(k) else 0)) / 100


def quiet_cut(e, t0, t1):                                              # the quietest 10-ms frame between two words = the cut point
    a, b = int(t0 * 100), max(int(t0 * 100) + 1, int(t1 * 100)); return (a + int(np.argmin(e[a:b]))) / 100


def lufs(x):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "ebur128", "-f", "null", "-"], input=x.astype(np.float32).tobytes(), capture_output=True).stderr.decode()
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])


for c in CLIPS:
    low = c.lower(); tts = f"../voice/tts_ep1/{c}.mp3"
    v = np.frombuffer(open(SC + f"sep/lite_{low}r2v_vocals.f32", "rb").read(), np.float32).reshape(-1, 2).mean(1)
    mw = SC + f"{low}_voc16.wav"; subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "1", "-i", "-", "-ar", "16000", mw], input=v.tobytes(), check=True)
    T, M = words(tts), words(mw); take = load(tts); te = env(load(tts, 16000), 16000); me = env(load(mw, 16000), 16000)
    mp = MAP.get(c, {}); idx = [mp.get(i, i if not mp else i - 1) for i in range(len(T))]   # our word i -> model word idx[i]
    # phrases = voiced runs of our take separated by pauses >= 0.18 s (energy; ASR word times swallow pauses, e.g. C12 "so[1.58-2.52]")
    q = te > te.max() * 0.03; runs = []; i = 0
    while i < len(q):
        j = i
        while j < len(q) and q[j] == q[i]: j += 1
        if q[i]: runs.append([i / 100, j / 100]) if not runs or i / 100 - runs[-1][1] >= 0.18 else runs[-1].__setitem__(1, j / 100)
        i = j
    runs = [r for r in runs if r[1] - r[0] >= 0.08]
    split = []                                                          # a run is also cut where the words have a gap >= 0.15 s with a real dip in energy (C13 "Mon Dieu! | Don't ...")
    for a, b in runs:
        cuts = []
        for i in range(1, len(T)):
            g0, g1 = T[i - 1][1], T[i][0]
            if a < g0 and g1 < b and g1 - g0 >= 0.15:
                seg = te[int(g0 * 100):int(g1 * 100)]
                if len(seg) and seg.min() < te[int(a * 100):int(b * 100)].max() * 0.10: cuts.append((g0 + int(np.argmin(seg)) / 100))
        edges = [a] + cuts + [b]; split += [[edges[i], edges[i + 1]] for i in range(len(edges) - 1)]
    runs = split
    owner = {}                                                          # every word goes to the run that holds its centre, else to the nearest run
    for i, t in enumerate(T):
        cen = (t[0] + t[1]) / 2; owner[i] = min(range(len(runs)), key=lambda k: 0 if runs[k][0] <= cen <= runs[k][1] else min(abs(cen - runs[k][0]), abs(cen - runs[k][1])))
    def mon_of(jw):                                                     # the model word's onset, searched only after the previous model word has ended
        lo = M[jw - 1][1] if jw > 0 else 0.0; a = max(lo, M[jw][0] - 0.35); b = max(a + 0.02, M[jw][1])
        seg = me[int(a * 100):int(b * 100)]; k = np.flatnonzero(seg > seg.max() * 0.25) if len(seg) else []
        return a + (k[0] / 100 if len(k) else 0)
    dur = len(load(f"frames/seedance25lite_{low}r2v.mp4")) / SR; track = np.zeros(int(SR * (dur + 0.5)), np.float32)
    pieces = []
    for k, (a, b) in enumerate(runs):
        ws = [i for i in range(len(T)) if owner[i] == k]
        cut0 = 0.0 if k == 0 else (runs[k - 1][1] + a) / 2; cut1 = len(take) / SR if k == len(runs) - 1 else (b + runs[k + 1][0]) / 2
        if ws:
            j0, j1 = idx[ws[0]], min(idx[ws[-1]], len(M) - 1); mon = mon_of(j0); mend = M[j1][1]; name = " ".join(T[i][2] for i in ws)
        else:                                                           # a run with no words (C15 laugh): the model's voiced run between the same neighbouring words
            prv = max([i for i, t in enumerate(T) if t[1] <= a + 0.05], default=None); nxt = min([i for i, t in enumerate(T) if t[0] >= b - 0.05], default=None)
            if prv is None or nxt is None: continue
            ma, mb = M[idx[prv]][1] + 0.1, M[idx[nxt]][0] - 0.05; sg = me[int(ma * 100):int(mb * 100)]; on = np.flatnonzero(sg > sg.max() * 0.25)
            mon = ma + (on[0] / 100 if len(on) else 0); mend = ma + ((on[-1] + 1) / 100 if len(on) else 0); name = "(laugh)"
        tp = float(np.clip((b - a) / max(0.2, mend - mon), 1.0, 1.3)); sp = (b - a) / tp
        if ws and M[j0][0] < 0.1: st = mend - sp                        # the model's first word starts at the clip start: its onset is not reliable, align the phrase by its end
        elif sp < 0.75 * (mend - mon): st = (mon + mend) / 2 - sp / 2   # ours is much shorter (the model drawls, C10 "liiike"): centre it on the model's phrase (no slowing down)
        else: st = mon
        pieces.append([name, cut0, cut1, st - (a - cut0) / tp, tp, mon, mend, a, b])
    pieces.sort(key=lambda q: q[5])
    def sp_st(q): return q[3] + (q[7] - q[1]) / q[4]                    # speech start / end of a placed piece in the clip
    def sp_en(q): return q[3] + (q[8] - q[1]) / q[4]
    for k in range(len(pieces) - 2, -1, -1):                            # no overlap of speech: first pull the earlier phrase back (it starts a little before the lips, e.g. C13 "Mon Dieu"),
        over = sp_en(pieces[k]) + 0.06 - sp_st(pieces[k + 1])             # as long as it does not hit the phrase before it or the clip start
        room = sp_st(pieces[k]) - (sp_en(pieces[k - 1]) + 0.06 if k > 0 else 0.0)
        if over > 0: pieces[k][3] -= min(over, max(0.0, room), 0.45)
    for k in range(1, len(pieces)):                                     # then push a later phrase if anything still overlaps
        over = sp_en(pieces[k - 1]) + 0.06 - sp_st(pieces[k])
        if over > 0: pieces[k][3] += over
    print(f"== {c}: our take {len(take) / SR:.2f} s, model clip {dur:.2f} s")
    for name, a, b, at, tp, mon, mend, sa, sb in pieces:
        seg = take[int(max(0, a) * SR):int(b * SR)].copy(); f = int(SR * .01); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        if abs(tp - 1) > .01: seg = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", f"atempo={tp:.3f}", "-f", "f32le", "-"], input=seg.tobytes(), capture_output=True, check=True).stdout, np.float32).copy()
        f = int(SR * .005); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        i0 = int(max(0, at) * SR); kk = min(len(seg), len(track) - i0); track[i0:i0 + kk] += seg[:kk]
        print(f"  {name:45s} speech {sa:5.2f}-{sb:5.2f} -> clip {at + (sa - a) / tp:5.2f}-{at + (sb - a) / tp:5.2f}  tempo {tp:.2f}  (model phrase {mon:.2f}-{mend:.2f})")
    track = track[:int(SR * dur)]; g = TARGET - lufs(track); track *= 10 ** (g / 20)
    out = SC + f"{c}R_final_voice48.f32"; bak = SC + f"{c}R_final_voice48_model.f32"
    if os.path.exists(out) and not os.path.exists(bak): os.rename(out, bak)
    open(out, "wb").write(track.astype(np.float32).tobytes())
    # lips: our voice vs the model's mouth (mouth.json of the r2v QC) next to the model's own voice
    import json
    mo = json.load(open(SC + f"{low}r2v/mouth.json")); t = np.array([r[0] for r in mo]); lip = np.array([np.nan if r[1] is None else r[1] for r in mo])
    def corr(x, sr, lag=0.0):
        ts = t + lag; ok = ~np.isnan(lip) & (ts > 0) & (ts < len(x) / sr - 0.05)
        e = np.array([np.sqrt((x[int(max(0, q - .04) * sr):int((q + .04) * sr)] ** 2).mean() + 1e-12) for q in ts[ok]])
        return np.corrcoef(lip[ok], np.sqrt(e))[0, 1]
    best = max((corr(track, SR, l), l) for l in np.arange(-0.2, 0.21, 0.04))
    print(f"  lips: ours lag 0 corr {corr(track, SR):.2f} (best {best[0]:.2f} at {best[1]:+.2f} s) | model's own voice {corr(v, 44100):.2f}")
