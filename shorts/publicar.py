"""Panel "Listo para subir" de la oficina: Shorts producidos con todo lo necesario para subirlos desde el iPad.

  python shorts/publicar.py --oficina salida.json [--previas]

- Busca en shorts/ las carpetas con un VCDT_*.mp4 (producidos) y lee su publicacion.md: título, traducción,
  descripción, comentario fijado, formato y nota del examen.
- Marca como publicados los que ya aparecen en el canal (docs/canal-estadisticas.json, por título).
- --previas crea una vista previa ligera (540x960, sin pasar de ~4 MB) en videos/previas/NN.mp4 para subirla
  como asset de la oficina; el vídeo bueno sigue siendo el VCDT_*.mp4 que se entrega por el chat.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PREVIAS = RAIZ / "videos" / "previas"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def ficha(carpeta: Path) -> dict | None:
    pub = carpeta / "publicacion.md"
    if not pub.exists():
        return None
    s = pub.read_text(encoding="utf-8")
    t = re.search(r"\*\*Título[^*]*:\*\*\s*(.+)", s)
    es = re.search(r"^\*ES:\s*(.+?)\*\s*$", s, flags=re.M)
    if not es:
        g = (carpeta / "guion.md").read_text(encoding="utf-8") if (carpeta / "guion.md").exists() else ""
        es = re.search(r"ES:\s*([^·\n]+)", g)
    bloques = re.findall(r"```\n?(.*?)```", s, flags=re.S)
    com = re.search(r"\*\*Comentario fijado:?\*\*:?\s*```\n?(.*?)```", s, flags=re.S) or re.search(r"\*\*Comentario fijado:?\*\*:?[ \t]*(.+)", s)
    fmt = re.search(r"\*\*Formato:\*\*\s*(.+)", s)
    alts = re.findall(r"^\s*-\s+(.+)$", s.split("**Descripción")[0], flags=re.M)
    return {
        "carpeta": carpeta.name, "n": carpeta.name[:2],
        "titulo": t.group(1).strip() if t else carpeta.name,
        "es": es.group(1).strip() if es else "",
        "alternativos": alts[:2],
        "descripcion": bloques[0].strip() if bloques else "",
        "comentario": (com.group(1) if com else "").strip(),
        "formato": fmt.group(1).strip() if fmt else "",
    }


def previa(video: Path, n: str) -> Path:
    PREVIAS.mkdir(parents=True, exist_ok=True)
    out = PREVIAS / f"{n}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", "scale=540:960", "-c:v", "libx264", "-preset", "veryfast",
                    "-b:v", "850k", "-maxrate", "1000k", "-bufsize", "2000k", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(out)],
                   check=True)
    return out


def main(args: list[str]) -> None:
    salida = args[args.index("--oficina") + 1] if "--oficina" in args else None
    hist = json.loads((RAIZ / "docs" / "canal-estadisticas.json").read_text()) if (RAIZ / "docs" / "canal-estadisticas.json").exists() else []
    publicados = {norm(s["titulo"]) for s in (hist[-1]["shorts"] if hist else [])}
    shorts = []
    for c in sorted((RAIZ / "shorts").glob("[0-9][0-9]-*")):
        vids = sorted(c.glob("VCDT_*.mp4"))
        if not vids:
            continue
        f = ficha(c)
        if not f:
            continue
        f["publicado"] = norm(f["titulo"]) in publicados
        f["archivo"] = vids[0].name
        if "--previas" in args and not f["publicado"]:
            f["previa"] = str(previa(vids[0], f["n"]).relative_to(RAIZ))
        shorts.append(f)
    datos = {"ts": int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000),
             "hora": "Mejor hora: de 00:00 a 03:00 (España) = de 18:00 a 21:00 en Nueva York",
             "shorts": shorts}
    for f in shorts:
        print(f"{'✓ publicado' if f['publicado'] else '→ por subir'}  {f['n']}  {f['titulo']}  {f.get('previa', '')}")
    if salida:
        Path(salida).write_text(json.dumps(datos, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
