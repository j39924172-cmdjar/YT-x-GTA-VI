"""Radar de VÍDEOS LARGOS de GTA 6 (4-20 min) en YouTube: qué vídeos largos funcionan ahora y de qué canales.

  python shorts/largos.py --oficina salida.json

Busca en YouTube (filtro de duración 4-20 min) varias consultas de GTA 6 y guarda los vídeos con más
visualizaciones: título, canal, duración, antigüedad y un formato detectado. Marca si el formato se puede
hacer SIN grabar partidas (con información oficial, capturas y clips de Rockstar), que es lo que hacemos nosotros.
Sirve para aprender formatos, NUNCA para copiar títulos, guiones ni imágenes.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

CONSULTAS = ["gta 6 explained", "gta 6 everything you need to know", "gta 6 secrets details", "gta 6 map",
             "gta 6 easter eggs", "gta 6 vs gta 5", "gta 6 lore", "gta 6 real life locations", "gta 6 tips"]
FORMATOS = [  # (patrón, formato, ¿lo podemos hacer sin grabar partidas?)
    (r"situation|record|sales|insane news|psyop|controvers", "Noticia / polémica", True),
    (r"real life|in real|florida|miami", "Juego contra vida real", True),
    (r"map explained|entire .*map|all locations", "Mapa explicado", True),
    (r"deep dive|hiding|story in plain sight|lore|theory", "Análisis / teoría", True),
    (r"need to know|wish i knew|tips|tricks|guide|head start", "Guía de consejos", True),
    (r"easter egg|secrets|details|things changed|little details", "Lista de secretos y detalles", True),
    (r"review", "Análisis crítico", True),
    (r"ending", "Finales (spoilers)", False),
    (r"testing|i downloaded|crossing|flying|funny|wtf|what happens if|survived|first day", "Partida grabada", False),
]


def curl(u: str) -> str:
    return subprocess.run(["curl", "-sS", "-m", "40", "-A", "Mozilla/5.0", "-H", "Accept-Language: en-US", "-b", "CONSENT=YES+1", u],
                          capture_output=True, text=True).stdout


def numero(t: str) -> int:
    t = t.lower().replace(",", "")
    m = re.search(r"([\d.]+)\s*(k|m|b)?", t)
    return int(float(m.group(1)) * {"k": 1e3, "m": 1e6, "b": 1e9}.get(m.group(2) or "", 1)) if m else 0


def formato(titulo: str) -> tuple[str, bool]:
    t = titulo.lower()
    for pat, nombre, ok in FORMATOS:
        if re.search(pat, t):
            return nombre, ok
    return "Otro", True


def buscar(q: str) -> list[dict]:
    html = curl("https://www.youtube.com/results?sp=EgIYAw%253D%253D&search_query=" + urllib.parse.quote(q))
    out = []
    for tr in html.split('"videoRenderer":')[1:]:
        tr = tr[:8000]
        v = re.match(r'\{"videoId":"([\w-]+)"', tr)
        t = re.search(r'"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', tr)
        c = re.search(r'"viewCountText":\{"simpleText":"([^"]*)"', tr)
        d = re.search(r'"lengthText":\{"accessibility":\{"accessibilityData":\{"label":"[^"]*"\}\},"simpleText":"([\d:]+)"', tr)
        ch = re.search(r'"canonicalBaseUrl":"(/@[^"]+)"', tr)
        p = re.search(r'"publishedTimeText":\{"simpleText":"([^"]*)"', tr)
        if v and t and c:
            titulo = json.loads(f'"{t.group(1)}"')
            f, ok = formato(titulo)
            out.append({"titulo": titulo, "vistas": numero(c.group(1)), "duracion": d.group(1) if d else "",
                        "canal": ch.group(1)[1:] if ch else "", "hace": p.group(1) if p else "",
                        "formato": f, "sin_partida": ok, "url": f"https://www.youtube.com/watch?v={v.group(1)}"})
    return out


def main(args: list[str]) -> None:
    salida = args[args.index("--oficina") + 1] if "--oficina" in args else None
    vistos = {}
    for q in CONSULTAS:
        for x in buscar(q):
            vistos.setdefault(x["url"], x)
    videos = sorted(vistos.values(), key=lambda x: -x["vistas"])
    rank: dict[str, list[int]] = {}
    for x in videos[:40]:
        rank.setdefault(x["formato"], []).append(x["vistas"])
    formatos = sorted(({"formato": f, "vistas": sum(v), "n": len(v), "sin_partida": formato_ok(f)} for f, v in rank.items()),
                      key=lambda r: -r["vistas"])
    for x in videos[:20]:
        print(f'{x["vistas"]:>11,} {x["duracion"]:>6} {"✅" if x["sin_partida"] else "🎮"} {x["canal"]:<22} {x["titulo"][:60]}')
    if salida:
        Path(salida).write_text(json.dumps({"ts": int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000),
                                            "videos": videos[:20], "formatos": formatos}, ensure_ascii=False))


def formato_ok(nombre: str) -> bool:
    return next((ok for _, n, ok in FORMATOS if n == nombre), True)


if __name__ == "__main__":
    main(sys.argv[1:])
