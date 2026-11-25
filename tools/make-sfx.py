#!/usr/bin/env python3
"""
make-sfx.py — Synthesize SFX for the VOX Interstellar Remotion video.

No external downloads: everything is generated locally with numpy and
written as 16-bit mono WAV (44100 Hz). Peak-normalized to ~-4.4 dBFS
(peak amplitude 0.6) so nothing clips.

Outputs (into ../public/sfx/):
  paper-flip.wav      ~0.5s  — paper flip: swept bandpass noise + fast decay
  highlighter.wav     ~0.6s  — highlighter stroke: low bandpass friction noise
  pop.wav             ~0.25s — card pop: sine burst 800 -> 200 Hz + click
  camera-shutter.wav  ~0.3s  — two short clicks + low thump
  chime.wav           ~1.2s  — win chime: sine chord 880/1320/1760 Hz, long decay
  whoosh.wav          ~0.7s  — transition whoosh: bandpass sweep up

Usage:  python3 make-sfx.py
Re-run any time to regenerate all files deterministically (seed fixed).
"""

import os
import wave

import numpy as np

SR = 44100
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "public", "sfx")
PEAK_TARGET = 0.6  # ~ -4.4 dBFS, safely inside the -6..-3 dB window

rng = np.random.default_rng(20261118)


def write_wav(path: str, audio: np.ndarray) -> None:
    """Write float audio in [-1, 1] as 16-bit mono WAV, peak-normalized."""
    audio = np.asarray(audio, dtype=np.float64)
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * PEAK_TARGET
    pcm = np.clip(audio, -1.0, 1.0)
    pcm16 = (pcm * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm16.tobytes())
    dur = len(pcm16) / SR
    rms = float(np.sqrt(np.mean(pcm.astype(np.float64) ** 2)))
    print(f"wrote {path}  dur={dur:.3f}s  peak={20*np.log10(PEAK_TARGET):.1f} dBFS  "
          f"rms={20*np.log10(max(rms, 1e-12)):.1f} dBFS")


def t_axis(dur: float) -> np.ndarray:
    return np.arange(int(SR * dur)) / SR


def swept_bandpass_noise(dur: float, f_start: float, f_end: float,
                         bw: float, chunk: int = 1024) -> np.ndarray:
    """White noise through a time-varying Gaussian bandpass (chunked FFT,
    Hann window, 50% overlap-add). Center frequency sweeps f_start -> f_end."""
    n = int(SR * dur)
    noise = rng.standard_normal(n)
    hop = chunk // 2
    window = np.hanning(chunk)
    out = np.zeros(n + chunk)
    freqs = np.fft.rfftfreq(chunk, 1 / SR)
    pos = 0
    while pos < n:
        seg = noise[pos:pos + chunk]
        if len(seg) < chunk:
            seg = np.pad(seg, (0, chunk - len(seg)))
        t_mid = (pos + chunk / 2) / SR
        frac = min(max(t_mid / dur, 0.0), 1.0)
        fc = f_start + (f_end - f_start) * frac
        # Gaussian bandpass in frequency domain
        resp = np.exp(-0.5 * ((freqs - fc) / max(bw, 1.0)) ** 2)
        spec = np.fft.rfft(seg * window) * resp
        filt = np.fft.irfft(spec, chunk) * window
        out[pos:pos + chunk] += filt
        pos += hop
    return out[:n]


def exp_decay(t: np.ndarray, tau: float, attack: float = 0.005) -> np.ndarray:
    """Fast attack, exponential decay envelope."""
    env = np.exp(-t / tau)
    a = np.clip(t / max(attack, 1e-6), 0.0, 1.0)
    return env * a


# ---------------------------------------------------------------- 1. paper flip
def paper_flip() -> np.ndarray:
    dur = 0.5
    t = t_axis(dur)
    body = swept_bandpass_noise(dur, f_start=3200, f_end=700, bw=1100)
    # Slight flutter (paper stiffness) on top of the decay
    flutter = 1.0 + 0.25 * np.sin(2 * np.pi * 55 * t)
    env = exp_decay(t, tau=0.11, attack=0.004)
    return body * env * flutter


# ------------------------------------------------------------ 2. highlighter
def highlighter() -> np.ndarray:
    dur = 0.6
    t = t_axis(dur)
    body = swept_bandpass_noise(dur, f_start=320, f_end=750, bw=380)
    # Friction texture: slow random amplitude wobble (smoothed noise)
    wob = rng.standard_normal(len(t))
    k = np.ones(220) / 220  # ~5 ms moving average
    wob = np.convolve(wob, k, mode="same")
    wob = wob / (np.max(np.abs(wob)) + 1e-12)
    texture = 1.0 + 0.45 * wob
    env = np.clip(t / 0.03, 0, 1) * np.clip((dur - t) / 0.12, 0, 1)
    return body * env * texture


# ------------------------------------------------------------------- 3. pop
def pop() -> np.ndarray:
    dur = 0.25
    t = t_axis(dur)
    # Pitch drops 800 -> 200 Hz exponentially over the burst
    f0, f1 = 800.0, 200.0
    phase = 2 * np.pi * np.cumsum(
        f1 + (f0 - f1) * np.exp(-t / 0.045)) / SR
    burst = np.sin(phase)
    env = exp_decay(t, tau=0.055, attack=0.001)
    # Initial click: 4 ms of highpassed noise
    click = rng.standard_normal(len(t))
    click[: int(0.004 * SR)] *= 1.0
    click[int(0.004 * SR):] = 0.0
    click = np.convolve(click, np.array([1.0, -0.9]), mode="same")
    return burst * env + 0.5 * click * exp_decay(t, tau=0.008, attack=0.0005)


# --------------------------------------------------------- 4. camera shutter
def camera_shutter() -> np.ndarray:
    dur = 0.3
    t = t_axis(dur)
    out = np.zeros_like(t)

    def click(t0: float, amp: float) -> np.ndarray:
        local = t - t0
        seg = np.zeros_like(t)
        m = (local >= 0) & (local < 0.05)
        seg[m] = rng.standard_normal(int(m.sum()))
        # Bandpass-ish: differentiate to kill lows, then shape
        seg = np.convolve(seg, np.array([1.0, -0.7]), mode="same")
        env = np.exp(-np.clip(local, 0, None) / 0.012)
        env[local < 0] = 0.0
        thump = np.sin(2 * np.pi * 130 * np.clip(local, 0, None)) \
            * np.exp(-np.clip(local, 0, None) / 0.03)
        thump[local < 0] = 0.0
        return amp * (seg * env + 0.6 * thump)

    out += click(0.0, 1.0)
    out += click(0.12, 0.85)
    return out


# ------------------------------------------------------------------ 5. chime
def chime() -> np.ndarray:
    dur = 1.2
    t = t_axis(dur)
    out = np.zeros_like(t)
    # Bell-like chord: fundamental + harmonics, staggered attacks
    partials = [
        (880.0, 1.00, 0.00, 0.55),
        (1320.0, 0.70, 0.06, 0.45),
        (1760.0, 0.50, 0.12, 0.40),
        (2640.0, 0.22, 0.18, 0.30),
    ]
    for freq, amp, delay, tau in partials:
        local = t - delay
        m = local >= 0
        tone = np.zeros_like(t)
        # Slight shimmer: gentle vibrato on the top partials
        tone[m] = np.sin(2 * np.pi * freq * local[m]
                         + 0.6 * np.sin(2 * np.pi * 5.5 * local[m]))
        env = np.exp(-np.clip(local, 0, None) / tau) \
            * np.clip(local / 0.006, 0, 1)
        env[~m] = 0.0
        out += amp * tone * env
    return out


# ----------------------------------------------------------------- 6. whoosh
def whoosh() -> np.ndarray:
    dur = 0.7
    t = t_axis(dur)
    body = swept_bandpass_noise(dur, f_start=280, f_end=4200, bw=900)
    # Rise-then-fall envelope (swell), plus a low airy bed
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    bed = swept_bandpass_noise(dur, f_start=180, f_end=500, bw=220) * 0.35
    return body * env + bed * env


# ----------------------------------------------------------------- 7. stamp
def stamp() -> np.ndarray:
    """Red ink stamp: low thud + short noise smack, ~0.35s."""
    dur = 0.35
    t = t_axis(dur)
    thud = np.sin(2 * np.pi * 90 * t) * np.exp(-t / 0.045)
    noise = rng.standard_normal(len(t))
    smack = swept_bandpass_noise(dur, f_start=900, f_end=300, bw=500) * 0.6
    env = np.exp(-t / 0.09)
    return (thud * 0.9 + smack * env) * np.clip(1 - t / dur, 0, 1)


SOUNDS = {
    "paper-flip.wav": paper_flip,
    "highlighter.wav": highlighter,
    "pop.wav": pop,
    "camera-shutter.wav": camera_shutter,
    "chime.wav": chime,
    "whoosh.wav": whoosh,
    "stamp.wav": stamp,
}


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    for name, fn in SOUNDS.items():
        write_wav(os.path.join(OUT_DIR, name), fn())
    print(f"\nDone. {len(SOUNDS)} files in {os.path.abspath(OUT_DIR)}")


if __name__ == "__main__":
    main()
