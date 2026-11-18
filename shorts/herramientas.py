"""Herramientas de apoyo para producir Shorts.

  python shorts/herramientas.py descargar <carpeta> Grupo_NN [Grupo_NN ...]   # capturas oficiales del catálogo
  python shorts/herramientas.py hoja <carpeta_capturas>                        # hoja de contacto con regla de 0 a 1
  python shorts/herramientas.py fotogramas <video.mp4> [n=12]                   # hoja de fotogramas para revisar
  python shorts/herramientas.py textos-rockstar [ruta=/VI/only-in-leonida]       # textos oficiales de una página de Rockstar
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
CATALOGO = RAIZ / "docs" / "catalogo-imagenes.json"
FONT = Path(__file__).parent / "fuentes" / "Montserrat-ExtraBold.ttf"


def descargar(carpeta: str, *claves: str) -> None:
    cat = json.loads(CATALOGO.read_text())
    destino = Path(carpeta) / "capturas"
    destino.mkdir(parents=True, exist_ok=True)
    for clave in claves:
        grupo, _, num = clave.rpartition("_")
        it = next((x for x in cat if x["grupo"] == grupo and (x["num"] or "") == num), None)
        if not it:
            # respaldo: galería de prensa de VGC con el mismo nombre
            url = f"https://www.videogameschronicle.com/files/2025/05/{clave}.jpg"
        else:
            url = it["url"]
        out = destino / f"{clave}.jpg"
        r = subprocess.run(["curl", "-sS", "-f", "-o", str(out), url], capture_output=True, text=True)
        print(f"{clave}: {'ok' if r.returncode == 0 else 'FALLO ' + r.stderr.strip()[:80]}" + (f"  — {it['alt'][:90]}" if it else ""))


def hoja(carpeta: str, salida: str | None = None) -> str:
    files = sorted(Path(carpeta).glob("*.jpg"))
    tw, th = 384, 216
    sheet = Image.new("RGB", (tw * 4, (th + 24) * ((len(files) + 3) // 4)), "black")
    f = ImageFont.truetype(str(FONT), 14)
    for i, p in enumerate(files):
        im = Image.open(p)
        im.thumbnail((tw, th))
        x, y = (i % 4) * tw, (i // 4) * (th + 24)
        sheet.paste(im, (x, y))
        d = ImageDraw.Draw(sheet)
        for k in range(1, 10):  # marcas de 0,1 en 0,1 para estimar el foco
            d.line([(x + k * tw // 10, y), (x + k * tw // 10, y + 8)], fill="white", width=2)
            d.line([(x, y + k * th // 10), (x + 8, y + k * th // 10)], fill="white", width=2)
        d.text((x + 4, y + th + 4), p.name, font=f, fill="yellow")
    out = salida or str(Path(carpeta).parent / "hoja.jpg")
    sheet.save(out, quality=85)
    print(out)
    return out


def fotogramas(video: str, n: str = "12") -> str:
    n = int(n)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], capture_output=True, text=True).stdout)
    tiempos = [round(dur * (i + 0.5) / n, 2) for i in range(n)]
    tmp = Path(video).parent / "_frames"
    tmp.mkdir(exist_ok=True)
    cols = 6
    sheet = Image.new("RGB", (270 * cols, 500 * ((n + cols - 1) // cols)), "black")
    f = ImageFont.truetype(str(FONT), 16)
    for i, t in enumerate(tiempos):
        out = tmp / f"{i:02d}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf", "scale=270:480", str(out)], check=True)
        x, y = (i % cols) * 270, (i // cols) * 500
        sheet.paste(Image.open(out), (x, y))
        ImageDraw.Draw(sheet).text((x + 5, y + 481), f"{t} s", font=f, fill="yellow")
    salida = str(Path(video).parent / "fotogramas.jpg")
    sheet.save(salida, quality=85)
    for p in tmp.glob("*.png"):
        p.unlink()
    tmp.rmdir()
    print(salida)
    return salida


def textos_rockstar(ruta: str = "/VI/only-in-leonida") -> None:
    url = "https://www.rockstargames.com" + ruta
    s = subprocess.run(["curl", "-sS", "-L", url], capture_output=True, text=True).stdout
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', s, flags=re.S)
    data = "".join(json.loads('"' + c + '"') for c in chunks)
    vistos = set()
    for t in re.findall(r'"(?:children|alt)":"([^"]{25,})"', data):
        t = html.unescape(t)
        ruido = ("could not be found", "history.scrollRestoration", "{", "function(")
        if t not in vistos and not t.startswith("$") and "http" not in t and not any(r in t for r in ruido):
            vistos.add(t)
            print("·", t)


if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)   # permite usar | head sin errores
    cmd, *args = sys.argv[1:]
    {"descargar": descargar, "hoja": hoja, "fotogramas": fotogramas, "textos-rockstar": textos_rockstar}[cmd](*args)
