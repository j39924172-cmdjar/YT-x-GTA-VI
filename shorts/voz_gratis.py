"""Voz gratuita para los Shorts (Kokoro, código abierto, sin créditos ni cuentas).

  python shorts/voz_gratis.py <voz.txt> <salida.mp3> [voz=am_fenrir] [duracion_objetivo=29]

- Descarga el modelo la primera vez desde Hugging Face (onnx-community/Kokoro-82M-v1.0-ONNX)
  a shorts/.modelos/ (no se guarda en git).
- Ajusta la velocidad para que la locución dure unos `duracion_objetivo` segundos (entre 1.0 y 1.35).
- Aplica el tratamiento de sonido del canal: limpieza de graves, presencia, compresión y volumen.
Voces masculinas de EE. UU. probadas: am_fenrir (por defecto), am_michael, am_puck.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = "https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX/resolve/main"
MODELOS = Path(__file__).parent / ".modelos"
FX = ("highpass=f=70,equalizer=f=200:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=3,"
      "acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-16:TP=-1.5")


def bajar(url: str, destino: Path) -> None:
    if not destino.exists():
        destino.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sS", "-L", "-f", "-o", str(destino), url], check=True)


def preparar(voz: str):
    from kokoro_onnx import Kokoro
    bajar(f"{REPO}/onnx/model.onnx", MODELOS / "model.onnx")
    bin_ = MODELOS / f"{voz}.bin"
    bajar(f"{REPO}/voices/{voz}.bin", bin_)
    npz = MODELOS / f"{voz}.npz"
    if not npz.exists():
        np.savez(npz, **{voz: np.fromfile(bin_, dtype=np.float32).reshape(-1, 1, 256)})
    return Kokoro(str(MODELOS / "model.onnx"), str(npz))


def main(txt: str, salida: str, voz: str = "am_fenrir", objetivo: str = "29") -> None:
    import soundfile as sf
    texto = Path(txt).read_text().strip()
    k = preparar(voz)
    vel = 1.15
    for _ in range(3):  # acerca la duración al objetivo
        audio, sr = k.create(texto, voice=voz, speed=vel, lang="en-us")
        dur = len(audio) / sr
        nueva = min(max(vel * dur / float(objetivo), 1.0), 1.35)
        if abs(dur - float(objetivo)) < 0.8 or abs(nueva - vel) < 0.01:
            break
        vel = nueva
    crudo = Path(salida).with_suffix(".crudo.wav")
    sf.write(crudo, audio, sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(crudo), "-af", FX, "-ar", "44100", "-ac", "1",
                    "-b:a", "192k", salida], check=True)
    crudo.unlink()
    print(f"{salida}: {dur:.1f} s · voz {voz} · velocidad {vel:.2f}")


if __name__ == "__main__":
    main(*sys.argv[1:])
