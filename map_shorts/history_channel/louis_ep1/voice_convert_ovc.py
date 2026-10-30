"""Voice conversion test (owner 30.10: "Kling с нашим голосом. Можно на наш изменить?"): the voice of a finished clip is converted into our locked v3 timbre with OpenVoice V2's tone-color converter
(MIT code https://github.com/myshell-ai/OpenVoice + MIT checkpoint myshell-ai/OpenVoiceV2/converter, run locally on CPU, no watermark module, no paid call). The converter keeps the content, timing, pauses and intonation of the source speech and swaps the timbre only,
so the lips stay in sync with the video. It does NOT change the accent or the acting of the source (the French accent and delivery stay Kling's).
Usage: python3 -I voice_convert_ovc.py <src_vocals.f32 (stereo 44.1 kHz float32, htdemucs vocals)> <out.wav 48 kHz mono> [tau=0.3] [ref1.mp3 ref2.mp3 ...]
Target timbre = the average embedding of the given reference takes (default: our v3 locked-voice TTS takes C01, C12-C15 in voice/tts_ep1/).
Needs: the OpenVoice repo cloned to <scratchpad>/ovc/src and converter/{config.json,checkpoint.pth} in <scratchpad>/ovc/ckpt (see the log in reference_check.md)."""
import subprocess, sys, os, numpy as np
SP = "/tmp/claude-0/-home-user-beauty-reels-bot/bb7f8515-f5d4-586a-94a3-df9db5a7e320/scratchpad/ovc/"
sys.path.insert(0, SP + "src")
import torch, librosa, soundfile
from openvoice import utils
from openvoice.models import SynthesizerTrn
from openvoice.mel_processing import spectrogram_torch

src, out = sys.argv[1], sys.argv[2]
tau = float(sys.argv[3]) if len(sys.argv) > 3 else 0.3
V = "../voice/tts_ep1/"
refs = sys.argv[4:] or [V + f"{c}.mp3" for c in ("C01", "C12", "C13", "C14", "C15")]
hps = utils.get_hparams_from_file(SP + "ckpt/converter/config.json")
model = SynthesizerTrn(len(getattr(hps, "symbols", [])), hps.data.filter_length // 2 + 1, n_speakers=hps.data.n_speakers, **hps.model).eval()
ck = torch.load(SP + "ckpt/converter/checkpoint.pth", map_location="cpu", weights_only=True)
print("load:", model.load_state_dict(ck["model"], strict=False))
SR = hps.data.sampling_rate


def spec_of(y):
    y = torch.FloatTensor(y).unsqueeze(0)
    return spectrogram_torch(y, hps.data.filter_length, SR, hps.data.hop_length, hps.data.win_length, center=False)


def embed(y):
    with torch.no_grad():
        return model.ref_enc(spec_of(y).transpose(1, 2)).unsqueeze(-1)


def load_mono(p):                     # any file -> mono float at the converter's rate
    return np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout, np.float32).copy()


v = np.frombuffer(open(src, "rb").read(), np.float32).reshape(-1, 2).mean(1)
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", "44100", "-ac", "1", "-i", "-", "-ar", str(SR), "-f", "f32le", "-"], input=v.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32).copy()
src_se = embed(x)
tgt_se = torch.stack([embed(load_mono(r)) for r in refs]).mean(0)
with torch.no_grad():
    y = model.voice_conversion(spec_of(x), torch.LongTensor([spec_of(x).size(-1)]), sid_src=src_se, sid_tgt=tgt_se, tau=tau)[0][0, 0].float().numpy()
print(f"converted {len(x) / SR:.2f} s -> {len(y) / SR:.2f} s at {SR} Hz, tau {tau}, refs {len(refs)}")
y = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ar", "48000", "-f", "f32le", "-"], input=y.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, np.float32)
soundfile.write(out, y, 48000, subtype="PCM_16")
print("wrote", out, f"peak {np.abs(y).max():.2f}")
