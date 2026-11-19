"""Biblioteca de clips de los vídeos oficiales de Rockstar (tráileres que Rockstar publica para descargar en rockstargames.com/VI).

  python shorts/clips.py descargar                 # baja los vídeos oficiales a videos/oficiales/ (no se guardan en git)
  python shorts/clips.py indexar                   # detecta cada plano, guarda docs/catalogo-videos.json y hojas de contacto en videos/hojas/
  python shorts/clips.py hoja <video> [desde] [n]  # hoja de contacto de planos para mirarla con Read

En el montaje, una escena puede ser un clip: {"video": "../../videos/oficiales/GTAVI_Launch_Trailer.mp4", "inicio": 12.4, ...}
Reglas (docs/manual-shorts.md): planos cortos (1-3 s) siempre con nuestra voz y nuestros datos encima; nunca una cinemática
entera ni escenas que destripen la historia; crédito "Footage: Rockstar Games" y aviso de canal no oficial.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
DIR = RAIZ / "videos" / "oficiales"
HOJAS = RAIZ / "videos" / "hojas"
CATALOGO = RAIZ / "docs" / "catalogo-videos.json"
FONT = Path(__file__).parent / "fuentes" / "Montserrat-ExtraBold.ttf"
BASE = "https://media-rockstargames-com.akamaized.net/VI/downloads/videos/{0}/{0}.mp4"
OFICIALES = ["GTAVI_Launch_Trailer", "GTAVI_Pre-Load_Now", "GTAVI_Official_Cover_Art_Landscape"]   # An_Extended_Look pesa 14 GB


def descargar() -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    for n in OFICIALES:
        out = DIR / f"{n}.mp4"
        if out.exists():
            print(f"{n}: ya está")
            continue
        r = subprocess.run(["curl", "-sS", "-f", "-L", "-m", "900", "-o", str(out), BASE.format(n)])
        print(f"{n}: {'ok' if r.returncode == 0 else 'FALLO'}")


def duracion(v: Path) -> float:
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)],
                                capture_output=True, text=True).stdout)


def cortes(v: Path, umbral: float = 0.25) -> list[float]:
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(v), "-vf", f"scale=640:-2,select='gt(scene\\,{umbral})',showinfo",
                          "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", log)]


def fotograma(v: Path, t: float, ancho: int = 320) -> Image.Image:
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(v), "-frames:v", "1", "-vf", f"scale={ancho}:-2",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    from io import BytesIO
    return Image.open(BytesIO(png)).convert("RGB")


def hoja(video: str, desde: str = "0", n: str = "24") -> str:
    """Hoja de contacto de los planos de un vídeo (a partir del plano `desde`)."""
    cat = json.loads(CATALOGO.read_text()) if CATALOGO.exists() else []
    nombre = Path(video).stem
    planos = [c for c in cat if c["video"] == nombre][int(desde):int(desde) + int(n)]
    HOJAS.mkdir(parents=True, exist_ok=True)
    cols, tw, th = 6, 320, 180
    img = Image.new("RGB", (cols * tw, ((len(planos) + cols - 1) // cols) * (th + 22)), "black")
    f = ImageFont.truetype(str(FONT), 14)
    for i, c in enumerate(planos):
        fr = fotograma(DIR / f"{nombre}.mp4", (c["inicio"] + c["fin"]) / 2)
        x, y = (i % cols) * tw, (i // cols) * (th + 22)
        img.paste(fr.resize((tw, th)), (x, y))
        ImageDraw.Draw(img).text((x + 4, y + th + 3), f"{c['id']}  {c['inicio']:.1f}-{c['fin']:.1f}s", font=f, fill="yellow")
    out = HOJAS / f"{nombre}_{desde}.jpg"
    img.save(out, quality=85)
    print(out)
    return str(out)


def indexar() -> None:
    previo = {c["id"]: c for c in json.loads(CATALOGO.read_text())} if CATALOGO.exists() else {}
    cat = []
    for n in OFICIALES:
        v = DIR / f"{n}.mp4"
        if not v.exists():
            continue
        dur = duracion(v)
        marcas = [0.0] + [t for t in cortes(v) if 0.3 < t < dur - 0.3] + [dur]
        corto = {"GTAVI_Launch_Trailer": "LT", "GTAVI_Pre-Load_Now": "PL", "GTAVI_Official_Cover_Art_Landscape": "CA"}[n]
        k = 0
        for a, b in zip(marcas, marcas[1:]):
            if b - a < 0.5:
                continue
            k += 1
            cid = f"{corto}{k:02d}"
            d = previo.get(cid, {})
            cat.append({"id": cid, "video": n, "inicio": round(a + 0.05, 2), "fin": round(b - 0.05, 2),
                        "descripcion": d.get("descripcion", ""), "evitar": d.get("evitar", False)})
    CATALOGO.write_text(json.dumps(cat, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(cat)} planos en {CATALOGO}")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"descargar": descargar, "indexar": indexar, "hoja": hoja}[cmd](*args)
