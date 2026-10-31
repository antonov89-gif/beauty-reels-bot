"""Episode 1 "My Morning", full cut (owner 30.10 "Делай"): 14 clips + the dressing burst + end card, sound v4 (real recordings, no music), grade, AI mark, fact plates.
Clips: C01 Kling 4.0 + our voice (owner "Нормально") | C02-C05 Lite remakes with our v3 voice | C06-C08 earlier finals | C09, C10 r2v | C11 burst of stills B1-B8 | C12-C15 r2v (model voice, trial v4; C13 kept as is, owner "Нет пусть так").
Sound per clip = scene bed (BigSoundBank recordings, see ../sfx/SOURCES.md) ducked under speech + foley + phone knocks on the real camera jerks + the video model's own sounds (htdemucs non-speech stem)
+ the voice through the phone-mic chain of build_sound_v4.py. Whole episode to -15 LUFS with ONE gain, one soft limiter on the final mix (no per-clip hard clip: it clicked before).
Picture: GRADE_LITE on the Seedance Lite / Kling clips, GRADE on the earlier Seedance 2.5 finals and the stills (values from grade_ep.py). Overlays: "AI-GENERATED" mark all the time, fact plates, end card.
Usage: python3 build_ep1.py [tag] -> frames/EP1_full_<tag>.mp4 (not committed). Inputs from prep_ep1_clips.py. Free (local)."""
import os, subprocess, sys, numpy as np
import build_sound_v4 as S
TAG = sys.argv[1] if len(sys.argv) > 1 else "A"
SR = 48000; F = "frames/"; SC = S.SC
GRADE = "eq=gamma=0.86:contrast=1.06:saturation=0.80,huesaturation=colors=y:saturation=-0.25,unsharp=5:5:0.85:5:5:0,noise=c0s=9:c0f=t+u:c1s=3:c1f=t+u:c2s=3:c2f=t+u"
GRADE_LITE = "eq=gamma=0.92:contrast=1.04:saturation=0.90,huesaturation=colors=y:saturation=-0.15,noise=c0s=3:c0f=t+u"
# id, file, scene, voice f32 (None = the file's own track), model sounds f32 (None = none), grade, phone distance keys (time, 0 close .. 1 far)
CLIPS = [("C01", "C01K_final_A", "A", SC + "C01K_final_A_voice48.f32", SC + "C01K_final_A_rest48.f32", GRADE_LITE, [(0, .75), (1.8, .75), (2.4, .15)]),
         ("C02", "C02L_final_A", "A", None, SC + "lite_c02_rest_A.f32", GRADE_LITE, [(0, .1)]),
         ("C03", "C03L_final_A", "A", None, SC + "lite_c03_rest_A.f32", GRADE_LITE, [(0, .15)]),
         ("C04", "C04L_final_A", "B", None, SC + "lite_c04_rest_A.f32", GRADE_LITE, [(0, .35)]),
         ("C05", "C05L_final_A", "B", None, SC + "lite_c05_rest_A.f32", GRADE_LITE, [(0, .3)]),
         ("C06", "C06_final", "B", None, None, GRADE, [(0, .7), (1.4, .7), (3.0, .15)]),
         ("C07", "C07_final", "C", None, None, GRADE, [(0, .2)]),
         ("C08", "C08_final_lcut", "C", None, None, GRADE, [(0, .25)])]
CLIPS += [(c, f"{c}R_final", "C" if c in ("C09", "C10") else "D", SC + f"{c}R_final_voice48.f32", SC + f"{c}R_final_rest48.f32", GRADE_LITE, [(0, d)])
          for c, d in (("C09", .2), ("C10", .25))]
CLIPS += [("C11", "C11_burst", "C", "SILENT", None, GRADE, [(0, .2)])]
CLIPS += [(c, f"{c}R_final", "D", SC + f"{c}R_final_voice48.f32", SC + f"{c}R_final_rest48.f32", GRADE_LITE, [(0, d)]) for c, d in (("C12", .2), ("C13", .1), ("C14", .2), ("C15", .2))]
END = 2.0                                                               # end card length, s
AI_MARK = os.environ.get("AI_MARK", "0") == "1"                         # owner 31.10 "Убери надпись Аи генератор": no corner mark; AI disclosure stays on the end card, in the description and the YouTube altered/synthetic flag
BED = dict(S.BED); BED["D"] = [("3433", 100.0, -43)]                   # D = Hall of Mirrors: a later, calmer part of Chambord Castle #3 (3432 was tried: steady 1050/1570 Hz tones in 7-8 % of frames, possibly music: not used)
BED["A"] = [("3431", 20.0, -43)]; BED["B"] = [("2855", 30.0, -45), ("3431", 90.0, -54)]   # cut D: +4 dB (cut C bedroom/dressing floor -52...-56 dB vs reference -49.5, near-silent 0.5-s windows)
LEVEL = {"C11": -31.0}                                                  # per-clip mix loudness before the one episode gain: speech clips to -17.8 LUFS (gain clamped +-4 dB), the wordless burst lower
FOLEY = [f for f in S.FOLEY if f[0] != "C01"]                           # C02-C08 foley as in the C01-C08 cut; C01 is the new Kling take
FOLEY += [("C01", 0.15, "1104", None, 0.6, -30, 0), ("C01", 1.95, "1104", 3.0, 0.5, -31, 0)]            # grip rubs before and during the phone turn (Kling's own knock at 3.0 s stays)
FOLEY += [("C11", i + 0.04, "0013", float(i * 0.7), 0.55, -31 - (i % 3), (-1) ** i * .3) for i in range(8)]   # a silk swish on every cut of the burst
FOLEY += [("C11", 3.1, "2017", 0, 0.4, -33, 0), ("C11", 6.2, "1104", 2.0, 0.5, -33, 0)]                 # the hand mirror tapped, the comb
FOLEY += [("C12", 0.3, "0376", 4.0, 8.3, -38, .3)]                                                     # his steps on the gallery parquet under the model's own sounds
# fact plates: clip, start, end (s in the clip), text (lines split by |); [n] in script_ru.md = number of sources
# cut D (owner 31.10 "С референсом"): silent heads trimmed toward the reference length (128 s), picture darker toward the reference brightness 86 and more texture on the smooth clips
TRIM = {"C02": (1.2, 0), "C05": (0.3, 0), "C06": (0.6, 0), "C07": (0.8, 0), "C09": (0.5, 0), "C10": (0.3, 0), "C12": (0.3, 0)}   # (head, tail) s: only silence before the first word, never the action
BRIGHT_C = {"C01": 99, "C02": 103, "C03": 99, "C07": 99, "C08": 106, "C09": 110, "C10": 97, "C11": 98, "C12": 104, "C13": 123, "C14": 107, "C15": 109}   # cut C brightness (compare_ep1_full_ref.py)
TARGET_BRIGHT = 90
def extra_v(cid):
    f = []
    if cid in BRIGHT_C:
        m = BRIGHT_C[cid]; g = max(0.75, float(np.log(m / 255) / np.log(TARGET_BRIGHT / 255))); f.append(f"eq=gamma={g:.3f}")
    if cid in ("C06", "C08"): f.append("unsharp=7:7:1.0:5:5:0,noise=c0s=6:c0f=t+u")
    if cid in ("C13", "C14", "C15"): f.append("unsharp=5:5:0.7:5:5:0,noise=c0s=6:c0f=t+u")
    return ("," + ",".join(f)) if f else ""
PLATES = [("C01", 2.7, 6.2, "VERSAILLES, FRANCE · 1685"), ("C02", 0.8, 4.8, "LE LEVER (THE RISING):|UP TO ~100 PEOPLE"),
          ("C03", 0.8, 5.0, "A DOCTOR AND A SURGEON WERE|IN THE ROOM BEFORE HE GOT UP"), ("C04", 2.0, 6.5, "HAIR LOSS FROM AGE ~17|(ABOUT 1655), THEN WIGS"),
          ("C05", 0.6, 3.8, "TALL WIGS ADDED HEIGHT"), ("C07", 0.8, 4.5, "COURTIERS CAME IN|BY ORDER OF PRIVILEGE"), ("C10", 0.8, 4.8, "RED HEELS:|A COURT PRIVILEGE, 1670s"),
          ("C11", 1.0, 6.5, "AT 14 HE DANCED|THE SUN GOD APOLLO (1653)"), ("C12", 1.0, 5.0, "HALL OF MIRRORS:|357 MIRRORS · 1678–1684"), ("C14", 0.8, 4.5, "NEXT: DINNER, IN PUBLIC")]
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"; SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def f32(path, ch):
    return np.frombuffer(open(path, "rb").read(), np.float32).reshape(-1, ch).T.copy()


def detone(ms, cid):
    """Notch out steady tones in the video model's own sounds (a held 222 Hz in C04 read like a note; owner on v3: "будто музыка какая-то"):
    every 80-3000 Hz bin that is a strong spectral peak (12 dB over its neighbourhood) in >= 15 % of the frames gets a narrow notch (Q 30), at most 6."""
    import scipy.signal as ss
    f, _, Z = ss.stft(ms.mean(0), SR, nperseg=8192, noverlap=6144); A = 20 * np.log10(np.abs(Z) + 1e-9); pk = (A - ss.medfilt(A, [41, 1])) > 12
    m = (f > 80) & (f < 3000); per = pk[m].mean(1); f2 = f[m]; out = ms.copy(); done = []
    for i in np.argsort(per)[::-1][:12]:
        if per[i] < 0.15 or len(done) >= 6 or any(abs(f2[i] - d) < 12 for d in done): continue
        b, a = ss.iirnotch(f2[i], 30, SR); out = ss.filtfilt(b, a, out, axis=1).astype(np.float32); done.append(float(f2[i]))
    if done: print(f"  {cid}: notched model-sound tones at {', '.join(f'{d:.0f}' for d in done)} Hz", flush=True)
    return out


def clip_mix(cid, name, sc, vsrc, msrc, dist_keys, t_scene, rng):
    p = F + name + ".mp4"; d = S.dur(p); L = int(SR * d)
    voice = np.zeros(L, np.float32) if vsrc == "SILENT" else (S.load(p)[0] if vsrc is None else f32(vsrc, 1)[0]); voice = np.pad(voice[:L], (0, max(0, L - len(voice))))
    bed = np.zeros((2, L), np.float32); t0 = t_scene.get(sc, 0.0)
    for i, st, lvl in BED[sc]:
        y = S.src(i)[:, int((st + t0) * SR):int((st + t0) * SR) + L]; y = np.pad(y, ((0, 0), (0, L - y.shape[1])))
        bed += y / (np.sqrt((y ** 2).mean()) + 1e-9) * S.db(lvl)
    t_scene[sc] = t0 + d
    bed *= S.duck_curve(voice, L, 4)[None, :]
    fol = np.zeros((2, L + SR * 3), np.float32); n = 0
    for c, t, i, st, ln, pk, pan in FOLEY:
        if c == cid: S.put(fol, S.piece(i, st, ln), t, pk, pan); n += 1
    speed, zoom = S.camera(p); last = -9
    if cid != "C11":                                                    # no phone knocks on the burst of stills (its motion is a synthetic push-in)
        for k in range(2, len(speed) - 2):
            if speed[k] > 0.012 and speed[k] == speed[max(0, k - 12):k + 12].max() and k / 24 - last > 0.6 and not any(c == cid and abs(t - k / 24) < .5 for c, t, *_ in FOLEY):
                last = k / 24; S.put(fol, S.piece(S.TAPS[rng.integers(4)], 0, 0.5), k / 24, -30 + rng.uniform(-2, 2), 0); n += 1
    dk = np.interp(np.arange(L) / SR, [q[0] for q in dist_keys] + [d + 1], [q[1] for q in dist_keys] + [dist_keys[-1][1]])
    zs = np.interp(np.arange(L) / SR, np.arange(len(zoom)) / 24, zoom); dist = np.clip(dk - 0.8 * zs, 0, 1)
    if msrc:
        ms = detone(f32(msrc, 2)[:, :L], cid); bed = bed * S.db(-6) + np.pad(ms, ((0, 0), (0, L - ms.shape[1]))) * S.db(3)
    room = bed + fol[:, :L]
    for ch in range(2):
        r_ = room[ch]; hi = S.sosfilt(S.butter(2, 3000, "hp", fs=SR, output="sos"), r_)
        room[ch] = S.sosfilt(S.butter(2, 7000, "lp", fs=SR, output="sos"), S.sosfilt(S.butter(2, 60, "hp", fs=SR, output="sos"), r_ - 0.6 * hi))
    mix = room + S.phone_voice(voice, dist)[None, :] * S.db(-2.6)
    f = int(SR * .015); mix[:, :f] *= np.linspace(0, 1, f); mix[:, -f:] *= np.linspace(1, 0, f)
    return p, d, mix, n


def lufs2(mix):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", "ebur128", "-f", "null", "-"], input=mix.T.astype(np.float32).tobytes(), capture_output=True).stderr.decode()
    return float([l for l in r.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def main():
    if os.environ.get("OVERLAY_ONLY"):                                  # re-render only the overlays from the last run's picture, mix and timeline (scratchpad)
        starts = {l.split()[0]: float(l.split()[1]) for l in open(SC + "ep1_starts.txt")}; raw = SC + "ep1_mix.f32"
        r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        I = float(r.split("I:")[-1].split("LUFS")[0]); return render(SC + "ep1_v.mp4", raw, starts, -15.0 - I, I, starts["END"] + END)
    DUB = os.environ.get("DUB")                                         # dub audio track (build_dub.py voices): same sound design, the picture of cut E is reused (stream copy)
    rng = np.random.default_rng(4); t_scene = {}; mixes = []; segs = []; starts = {}; t = 0.0
    for cid, name, sc, vsrc, msrc, grade, dk in CLIPS:
        if DUB and vsrc != "SILENT": vsrc = SC + f"dub_{DUB}_{cid}.f32"
        p, d, mix, n = clip_mix(cid, name, sc, vsrc, msrc, dk, t_scene, rng)
        h0, t0_ = (round(x * 24) / 24 for x in TRIM.get(cid, (0, 0)))   # whole frames, so picture and sound stay in step over 15 segments
        mix = mix[:, int(round(h0 * SR)):int(round((d - t0_) * SR))]; d = mix.shape[1] / SR
        f = int(SR * .015); mix[:, :f] *= np.linspace(0, 1, f); mix[:, -f:] *= np.linspace(1, 0, f)
        li = lufs2(mix); lg = float(np.clip(LEVEL.get(cid, -17.8) - li, -4, 4)) if cid not in LEVEL else LEVEL[cid] - li; mix = mix * S.db(lg)
        mixes.append(mix); starts[cid] = t; t += d
        g = SC + f"ep1_{cid}_g.mp4"                                     # graded picture, same encoder settings for every segment (concat by stream copy)
        if DUB: print(f"{cid}: {d:.2f} s, mix {li:.1f} LUFS, level {lg:+.1f} dB", flush=True); continue
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{h0:.3f}", "-t", f"{d:.3f}", "-i", p, "-an", "-vf", f"scale=1080:1920,setsar=1,fps=24,{grade}{extra_v(cid)},format=yuv420p", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-r", "24", g], check=True)
        segs.append(g); print(f"{cid} {name}: {d:.2f} s at {starts[cid]:.2f}, foley/knocks {n}, mix {li:.1f} LUFS, level {lg:+.1f} dB", flush=True)
    # end card: the gallery bed fades out under the text on black
    L = int(SR * END); bi, bst, blv = BED["D"][0]; y = S.src(bi)[:, int((bst + t_scene["D"]) * SR):int((bst + t_scene["D"]) * SR) + L]
    endmix = y / (np.sqrt((y ** 2).mean()) + 1e-9) * S.db(blv - 4) * np.linspace(1, 0, L)[None, :]; mixes.append(endmix.astype(np.float32)); starts["END"] = t; t += END
    ge = SC + "ep1_END_g.mp4"
    if DUB:
        allmix = np.concatenate(mixes, axis=1); raw = SC + f"ep1_mix_{DUB}.f32"; open(raw, "wb").write(allmix.T.astype(np.float32).tobytes())
        r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        I = float(r.split("I:")[-1].split("LUFS")[0]); a_out = F + f"EP1_{TAG}_audio_{DUB}.m4a"; v_out = F + f"EP1_full_{TAG}_{DUB}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-af", f"volume={-15.0 - I:.2f}dB,alimiter=limit=0.89:attack=5:release=80:level=disabled",
                        "-c:a", "aac", "-b:a", "256k", "-ar", "48000", a_out], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", F + f"EP1_full_{TAG}.mp4", "-i", a_out, "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest", "-movflags", "+faststart",
                        "-metadata:s:a:0", f"language={ {'fr': 'fra', 'es': 'spa', 'ru': 'rus'}.get(DUB, DUB) }", v_out], check=True)
        print(a_out, v_out, f"{t:.2f} s; mix {I:.1f} LUFS -> -15"); return
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r=24:d={END}", "-vf", "format=yuv420p", "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-r", "24", ge], check=True); segs.append(ge)
    allmix = np.concatenate(mixes, axis=1); raw = SC + "ep1_mix.f32"; open(raw, "wb").write(allmix.T.astype(np.float32).tobytes())
    r = subprocess.run(["ffmpeg", "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = float(r.split("I:")[-1].split("LUFS")[0]); gain = -15.0 - I
    lst = SC + "ep1_list.txt"; open(lst, "w").write("".join(f"file '{s}'\n" for s in segs)); vcat = SC + "ep1_v.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vcat], check=True)
    open(SC + "ep1_starts.txt", "w").write("\n".join(f"{k} {v:.3f}" for k, v in starts.items()))
    render(vcat, raw, starts, gain, I, t)


def render(vcat, raw, starts, gain, I, t):
    dt = [f"drawtext=fontfile={SANS}:text='AI-GENERATED':fontsize=28:fontcolor=white@0.85:x=60:y=210:box=1:boxcolor=black@0.45:boxborderw=8:enable='lt(t,{starts['END']:.2f})'"] if AI_MARK else []
    for i, (cid, a, b, text) in enumerate(PLATES):
        tf = SC + f"ep1_plate_{i}.txt"; open(tf, "w").write(text.replace("|", "\n"))
        dt.append(f"drawtext=fontfile={SERIF}:textfile={tf}:expansion=none:fontsize=50:line_spacing=10:fontcolor=white:x=(w-text_w)/2:y=1250:box=1:boxcolor=black@0.55:boxborderw=18"
                  f":enable='between(t,{starts[cid] + a - round(TRIM.get(cid, (0, 0))[0] * 24) / 24:.2f},{starts[cid] + b - round(TRIM.get(cid, (0, 0))[0] * 24) / 24:.2f})'")
    tf = SC + "ep1_endcard.txt"; open(tf, "w").write("THE SUN IS NEVER LATE.")
    dt.append(f"drawtext=fontfile={SERIF}:textfile={tf}:expansion=none:fontsize=72:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='gte(t,{starts['END'] + 0.15:.2f})'")
    tf2 = SC + "ep1_endcard2.txt"; open(tf2, "w").write("AI-generated comedy reconstruction")
    dt.append(f"drawtext=fontfile={SANS}:textfile={tf2}:expansion=none:fontsize=30:fontcolor=white@0.7:x=(w-text_w)/2:y=(h/2)+90:enable='gte(t,{starts['END'] + 0.15:.2f})'")
    out = F + f"EP1_full_{TAG}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", vcat, "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", raw, "-filter_complex",
                    f"[0:v]{','.join(dt)}[v];[1:a]volume={gain:.2f}dB,alimiter=limit=0.89:attack=5:release=80:level=disabled[a]", "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-crf", os.environ.get("CRF", "21"), "-preset", "medium", "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
    print(out, f"{t:.2f} s; mix {I:.1f} LUFS, gain {gain:+.2f} dB; corner AI mark {'ON' if AI_MARK else 'OFF'}")


if __name__ == "__main__":
    main()
