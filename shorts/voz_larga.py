"""Voz gratuita (Kokoro) para vídeos largos: genera párrafo a párrafo y los une con pausas.

  python shorts/voz_larga.py <voz.txt> <salida.mp3> [voz=am_fenrir] [velocidad=1.0]

- Un párrafo por línea en blanco. Los párrafos que empiezan por "Part " (capítulos) llevan más pausa delante.
- Mismo tratamiento de sonido que shorts/voz_gratis.py.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from voz_gratis import FX, preparar  # noqa: E402


def main(txt: str, salida: str, voz: str = "am_fenrir", vel: str = "1.0") -> None:
    import soundfile as sf
    k = preparar(voz)
    trozos, sr = [], 24000
    for par in [p.strip() for p in Path(txt).read_text().split("\n\n") if p.strip()]:
        capitulo = par.startswith("Part ") or par.startswith("Before we keep going")
        if trozos:
            trozos.append(np.zeros(int(sr * (1.1 if capitulo else 0.6)), np.float32))
        for frase in [par]:
            a, sr = k.create(frase, voice=voz, speed=float(vel), lang="en-us")
            trozos.append(a.astype(np.float32))
    audio = np.concatenate(trozos)
    crudo = Path(salida).with_suffix(".crudo.wav")
    sf.write(crudo, audio, sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(crudo), "-af", FX, "-ar", "44100", "-ac", "1",
                    "-b:a", "192k", salida], check=True)
    crudo.unlink()
    print(f"{salida}: {len(audio) / sr:.1f} s · voz {voz} · velocidad {vel}")


if __name__ == "__main__":
    main(*sys.argv[1:])
