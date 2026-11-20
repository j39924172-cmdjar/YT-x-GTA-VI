"""Radar de tendencias de YouTube para GTA 6 (datos públicos, sin claves).

  python shorts/tendencias.py --oficina salida.json [--ideas investigacion.json]

1) Sugerencias de búsqueda de YouTube (lo que la gente escribe: "gta 6 how to make money"…).
2) Shorts de GTA 6 de otros canales con más visualizaciones ahora (para detectar formatos que suben; nunca para copiarlos).
3) Nota de demanda 0-10 para cada título del banco: visualizaciones de los Shorts que salen al buscar ese tema
   (escala logarítmica: 1.000 → 0, 1.000.000+ → 10) + 1 punto si el tema sale en las sugerencias.
4) FUENTE YouTube: últimos vídeos del canal oficial de Rockstar (RSS) y vídeos de GTA 6 más vistos de esta semana.
5) FUENTE X (Twitter): la red no deja entrar en x.com, así que la investigación busca con WebSearch
   (allowed_domains ["x.com"]) y guarda lo encontrado en un JSON que se mezcla con --x x.json:
   [{"cuenta": "@RockstarGames", "texto": "…", "url": "https://x.com/…", "fecha": "2026-11-19", "oficial": true}, …]
   Las cuentas oficiales de Rockstar son fuente primaria; el resto (insiders, fans) es rumor 🟡 hasta que lo
   confirmen 2 medios fiables. Las fuentes van SOLO en la descripción del Short, nunca en pantalla.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import re
import statistics
import subprocess
import sys
import urllib.parse
from pathlib import Path

SEMILLAS = ["gta 6 how to", "gta 6 money", "gta 6 secret", "gta 6 tips", "gta 6 easter egg", "gta 6 cheat", "gta 6 best", "gta 6 hidden"]
BUSQUEDAS_VIRALES = ["gta 6 tips", "gta 6 secrets", "gta 6 money", "gta 6 easter eggs"]
ROCKSTAR_YT = "UC6VcWc1rAoWdBCM0JxrRQ3A"  # canal oficial de Rockstar Games en YouTube
VACIAS = {"gta", "6", "vi", "in", "the", "a", "an", "of", "is", "to", "your", "you", "this", "that", "it", "just", "and", "on", "for", "has", "can", "s", "it's", "gta6"}


def curl(url: str) -> str:
    return subprocess.run(["curl", "-sS", "-m", "40", "-A", "Mozilla/5.0", "-H", "Accept-Language: en-US", "-b", "CONSENT=YES+1", url],
                          capture_output=True, text=True).stdout


def sugerencias(q: str) -> list[str]:
    raw = curl("https://suggestqueries.google.com/complete/search?client=youtube&ds=yt&hl=en&gl=us&q=" + urllib.parse.quote(q))
    m = re.search(r"\((\[.*\])\)\s*$", raw.strip(), flags=re.S)
    if not m:
        return []
    try:
        return [x[0] for x in json.loads(m.group(1))[1]]
    except (ValueError, IndexError, TypeError):
        return []


def numero(txt: str) -> int:
    t = txt.lower().replace(",", "")
    m = re.search(r"([\d.]+)\s*(thousand|million|billion|k|m|b)?", t)
    if not m:
        return 0
    mult = {"thousand": 1e3, "k": 1e3, "million": 1e6, "m": 1e6, "billion": 1e9, "b": 1e9}.get(m.group(2) or "", 1)
    return int(float(m.group(1)) * mult)


def shorts_de_busqueda(q: str) -> list[dict]:
    html = curl("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q))
    out, vistos = [], set()
    for vid, acc in re.findall(r'"shortsLockupViewModel":\{"entityId":"shorts-shelf-item-([\w-]+)","accessibilityText":"((?:[^"\\]|\\.)*)"', html):
        if vid in vistos:
            continue
        vistos.add(vid)
        texto = json.loads(f'"{acc}"')
        m = re.match(r"(.*), ([\d.,]+ (?:thousand |million |billion )?views?)", texto)
        titulo, vistas = (m.group(1), numero(m.group(2))) if m else (texto.split(" - play")[0], 0)
        out.append({"titulo": titulo, "vistas": vistas, "url": f"https://www.youtube.com/shorts/{vid}"})
    return out


def rockstar_youtube(n: int = 6) -> list[dict]:
    xml = curl("https://www.youtube.com/feeds/videos.xml?channel_id=" + ROCKSTAR_YT)
    out = []
    for e in re.findall(r"<entry>(.*?)</entry>", xml, flags=re.S)[:n]:
        t = re.search(r"<title>(.*?)</title>", e)
        f = re.search(r"<published>(\d{4}-\d\d-\d\d)", e)
        v = re.search(r"<yt:videoId>([\w-]+)</yt:videoId>", e)
        vis = re.search(r'<media:statistics views="(\d+)"', e)
        if t and v:
            out.append({"titulo": html_txt(t.group(1)), "fecha": f.group(1) if f else "", "url": f"https://www.youtube.com/watch?v={v.group(1)}",
                        "vistas": int(vis.group(1)) if vis else 0})
    return out


def html_txt(s: str) -> str:
    return s.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'").replace("&lt;", "<").replace("&gt;", ">")


def youtube_semana(q: str = "gta 6", n: int = 10) -> list[dict]:
    """Vídeos de GTA 6 subidos esta semana, ordenados por visualizaciones (filtro sp de YouTube)."""
    html = curl("https://www.youtube.com/results?sp=CAMSAggD&search_query=" + urllib.parse.quote(q))
    out = []
    for trozo in html.split('"videoRenderer":')[1:]:
        trozo = trozo[:6000]
        v = re.match(r'\{"videoId":"([\w-]+)"', trozo)
        t = re.search(r'"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', trozo)
        c = re.search(r'"viewCountText":\{"simpleText":"([^"]*)"', trozo)
        if v and t:
            out.append({"titulo": json.loads(f'"{t.group(1)}"'), "vistas": numero(c.group(1)) if c else 0,
                        "url": f"https://www.youtube.com/watch?v={v.group(1)}"})
        if len(out) >= n:
            break
    return sorted(out, key=lambda x: -x["vistas"])


def palabras_clave(titulo: str) -> str:
    w = [x for x in re.findall(r"[a-z0-9$']+", titulo.lower()) if x not in VACIAS]
    return "gta 6 " + " ".join(w[:4])


def nota(vistas: list[int], en_sugerencias: bool) -> float:
    if not vistas:
        return 0.0
    med = statistics.median(sorted(vistas, reverse=True)[:8])
    n = max(0.0, min(10.0, (math.log10(max(med, 1)) - 3) * 10 / 3))
    return round(min(10.0, n + (1 if en_sugerencias else 0)), 1)


def main(args: list[str]) -> None:
    salida = args[args.index("--oficina") + 1] if "--oficina" in args else None
    ideas_f = args[args.index("--ideas") + 1] if "--ideas" in args else None
    sug = []
    for s in SEMILLAS:
        for x in sugerencias(s):
            if x not in sug:
                sug.append(x)
    virales, vistos = [], set()
    for q in BUSQUEDAS_VIRALES:
        for v in shorts_de_busqueda(q):
            if v["url"] not in vistos:
                vistos.add(v["url"])
                virales.append(v)
    virales.sort(key=lambda v: -v["vistas"])
    notas = {}
    if ideas_f and Path(ideas_f).exists():
        d = json.loads(Path(ideas_f).read_text())
        d = d.get("data", d)
        texto_sug = " ".join(sug)
        for idea in d.get("ideas", []):
            q = palabras_clave(idea["titulo"])
            res = shorts_de_busqueda(q)
            clave = [w for w in q.split()[2:] if len(w) > 3]
            en_sug = any(w in texto_sug for w in clave)
            notas[idea["titulo"]] = {"nota": nota([r["vistas"] for r in res], en_sug), "busqueda": q,
                                     "mejor": max((r["vistas"] for r in res), default=0)}
    x_f = args[args.index("--x") + 1] if "--x" in args else None
    x = json.loads(Path(x_f).read_text()) if x_f and Path(x_f).exists() else []
    resultado = {"ts": int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000), "sugerencias": sug[:24],
                 "virales": virales[:10], "notas": notas,
                 "rockstar_yt": rockstar_youtube(), "youtube_semana": youtube_semana(), "x": x[:10]}
    print(f"{len(sug)} sugerencias · {len(virales)} Shorts virales · {len(notas)} ideas puntuadas")
    for s in sug[:10]:
        print("  ·", s)
    for v in virales[:5]:
        print(f"  {v['vistas']:>10,}  {v['titulo'][:70]}")
    for v in resultado["rockstar_yt"][:3]:
        print(f"  ▶ Rockstar {v['fecha']}  {v['titulo']}")
    for v in resultado["youtube_semana"][:3]:
        print(f"  ▶ {v['vistas']:>12,}  {v['titulo'][:70]}")
    print(f"  𝕏 {len(x)} publicaciones de X")
    for t, n in sorted(notas.items(), key=lambda x: -x[1]["nota"]):
        print(f"  🔥 {n['nota']:>4}  {t}")
    if salida:
        Path(salida).write_text(json.dumps(resultado, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
