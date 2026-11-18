"""Repaso diario del canal (datos públicos de YouTube, sin contraseñas ni claves).

  python shorts/canal.py            # lee el canal, lo guarda en docs/canal-estadisticas.json y muestra los cambios

Solo usa lo que ve cualquiera en https://www.youtube.com/@vicecitydaystv/shorts:
suscriptores, número de vídeos y visualizaciones de cada Short. Las estadísticas
privadas (vistos frente a deslizados, retención) las pasa Adam con capturas de YouTube Studio.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from pathlib import Path

CANAL = "https://www.youtube.com/@vicecitydaystv/shorts"
RAIZ = Path(__file__).resolve().parent.parent
HISTORIAL = RAIZ / "docs" / "canal-estadisticas.json"


def numero(txt: str) -> int:
    """'1.2K views' → 1200 · '298 views' → 298 · 'No views' → 0"""
    m = re.search(r"([\d.,]+)\s*([KM]?)", txt.replace(" ", " "))
    if not m:
        return 0
    n = float(m.group(1).replace(",", ""))
    return int(n * {"": 1, "K": 1_000, "M": 1_000_000}[m.group(2)])


def leer() -> dict:
    html = subprocess.run(
        ["curl", "-sS", "-m", "40", "-A", "Mozilla/5.0", "-H", "Accept-Language: en-US", "-b", "CONSENT=YES+1", CANAL],
        capture_output=True, text=True, check=True).stdout
    subs = re.search(r'"content":"([^"]*?) subscribers?"', html)
    shorts = []
    for vid, titulo, vistas in re.findall(
            r'"shortsLockupViewModel":\{"entityId":"shorts-shelf-item-([\w-]+)".*?"primaryText":\{"content":"([^"]+)"\},"secondaryText":\{"content":"([^"]+)"',
            html, flags=re.S):
        if vid not in {s["id"] for s in shorts}:
            shorts.append({"id": vid, "titulo": json.loads(f'"{titulo}"'), "vistas": numero(vistas)})
    if not shorts:  # respaldo si cambia el formato de la página
        for titulo, vistas in re.findall(r'"overlayMetadata":\{"primaryText":\{"content":"([^"]+)"\},"secondaryText":\{"content":"([^"]+)"', html):
            shorts.append({"id": "", "titulo": json.loads(f'"{titulo}"'), "vistas": numero(vistas)})
    if not subs and not shorts:
        raise SystemExit("No se pudo leer el canal (¿www.youtube.com bloqueado o la página cambió?)")
    return {"fecha": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "suscriptores": numero(subs.group(1)) if subs else None,
            "shorts": shorts}


def main() -> None:
    hoy = leer()
    hist = json.loads(HISTORIAL.read_text()) if HISTORIAL.exists() else []
    antes = hist[-1] if hist else None
    hist.append(hoy)
    HISTORIAL.write_text(json.dumps(hist, indent=1, ensure_ascii=False) + "\n")

    def delta(a, b):
        return "" if a is None or b is None else f" ({b - a:+d})"

    print(f"Canal VICECITY DAYS TV · {hoy['fecha']}")
    print(f"Suscriptores: {hoy['suscriptores']}" + (delta(antes["suscriptores"], hoy["suscriptores"]) if antes else ""))
    previas = {s["titulo"]: s["vistas"] for s in (antes or {}).get("shorts", [])}
    total = sum(s["vistas"] for s in hoy["shorts"])
    print(f"Shorts públicos: {len(hoy['shorts'])} · visualizaciones totales: {total}")
    for s in sorted(hoy["shorts"], key=lambda s: -s["vistas"]):
        print(f"  {s['vistas']:>8}{delta(previas.get(s['titulo']), s['vistas']):>8}  {s['titulo']}")


if __name__ == "__main__":
    main()
