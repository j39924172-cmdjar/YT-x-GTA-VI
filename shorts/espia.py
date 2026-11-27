"""Espía de canales: qué formatos explotan en canales de GTA 6 (datos públicos de YouTube, sin claves).

  python shorts/espia.py --oficina salida.json [@canal1 @canal2 …]

Sin canales, usa los referentes guardados en docs/referentes.json (los que Adam va pasando por el chat).
Para cada canal: suscriptores, Shorts con visualizaciones, la mediana del canal y los que explotan
(×N veces su mediana), con el formato detectado por el título. Sirve para aprender formatos,
NUNCA para copiar títulos, guiones ni imágenes.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REFERENTES = RAIZ / "docs" / "referentes.json"

FORMATOS = [  # (patrón en el título, nombre del formato en español)
    (r"\bhow (the )?.+ works?\b|\bexplained\b", "Cómo funciona"),
    (r"\b(gta ?5|gta ?v)\b|can'?t do in", "GTA 6 contra GTA 5"),
    (r"^\s*\d+\s|\btop \d+\b", "Lista de N"),
    (r"realistic|too real|real life|irl", "Realismo"),
    (r"\?\s*$|^(will|could|what if|is|should)\b", "Gran pregunta"),
    (r"need to know|before you (play|start)|tips|guide|how to", "Guía / consejos"),
    (r"steal|stole|stealing|tried|stop a|caught", "Momento jugando"),
    (r"secret|hidden|easter egg|nobody|no one", "Secreto"),
]


def curl(url: str) -> str:
    return subprocess.run(["curl", "-sS", "-m", "40", "-A", "Mozilla/5.0", "-H", "Accept-Language: en-US", "-b", "CONSENT=YES+1", url],
                          capture_output=True, text=True).stdout


def numero(txt: str) -> int:
    t = txt.lower().replace(",", "")
    m = re.search(r"([\d.]+)\s*(thousand|million|billion|k|m|b)?", t)
    if not m:
        return 0
    mult = {"thousand": 1e3, "k": 1e3, "million": 1e6, "m": 1e6, "billion": 1e9, "b": 1e9}.get(m.group(2) or "", 1)
    return int(float(m.group(1)) * mult)


def formato(titulo: str) -> str:
    t = re.sub(r"#\w+", "", titulo.lower()).strip()
    for pat, nombre in FORMATOS:
        if re.search(pat, t):
            return nombre
    return "Otro"


def canal(handle: str, todos: bool = False) -> dict:
    handle = handle if handle.startswith("@") else "@" + handle
    html = curl(f"https://www.youtube.com/{handle}/shorts")
    subs = re.search(r"([\d.,]+[KM]?) subscribers", html)
    shorts, vistos = [], set()
    for vid, acc in re.findall(r'"shortsLockupViewModel":\{"entityId":"shorts-shelf-item-([\w-]+)","accessibilityText":"((?:[^"\\]|\\.)*)"', html):
        if vid in vistos:
            continue
        vistos.add(vid)
        texto = json.loads(f'"{acc}"')
        m = re.match(r"(.*), ([\d.,]+ (?:thousand |million |billion )?views?)", texto)
        titulo, vistas = (m.group(1), numero(m.group(2))) if m else (texto.split(" - play")[0], 0)
        titulo = re.sub(r"\s*#\w+", "", titulo).strip()
        shorts.append({"titulo": titulo, "vistas": vistas, "formato": formato(titulo), "url": f"https://www.youtube.com/shorts/{vid}"})
    med = statistics.median([s["vistas"] for s in shorts]) if shorts else 0
    for s in shorts:
        s["veces"] = round(s["vistas"] / med, 1) if med else 0
    shorts.sort(key=lambda s: -s["vistas"])
    return {"canal": handle, "url": f"https://www.youtube.com/{handle}", "suscriptores": subs.group(1) if subs else "?",
            "n": len(shorts), "mediana": int(med), "shorts": shorts if todos else shorts[:12]}


def ranking_formatos(canales: list[dict]) -> list[dict]:
    """Formatos ordenados por cuántas veces superan la mediana de su canal (media de ×N)."""
    acc: dict[str, list[float]] = {}
    for c in canales:
        for s in c["shorts"]:
            acc.setdefault(s["formato"], []).append(s["veces"])
    out = [{"formato": f, "veces": round(statistics.mean(v), 1), "n": len(v)} for f, v in acc.items()]
    return sorted(out, key=lambda x: -x["veces"])


def main(args: list[str]) -> None:
    salida = args[args.index("--oficina") + 1] if "--oficina" in args else None
    handles = [a for a in args if a.startswith("@")]
    refs = json.loads(REFERENTES.read_text()) if REFERENTES.exists() else []
    if not handles:
        handles = [r["canal"] for r in refs]
    notas = {r["canal"]: r.get("nota", "") for r in refs}
    canales = []
    for h in handles:
        c = canal(h)
        c["nota"] = notas.get(c["canal"], "")
        canales.append(c)
        print(f"{c['canal']}: {c['suscriptores']} subs · {c['n']} Shorts · mediana {c['mediana']:,}")
        for s in c["shorts"][:4]:
            print(f"   ×{s['veces']:<5} {s['vistas']:>10,}  [{s['formato']}] {s['titulo'][:60]}")
    rank = ranking_formatos(canales)
    for r in rank:
        print(f"  {r['formato']:<20} ×{r['veces']} ({r['n']} Shorts)")
    if salida:
        Path(salida).write_text(json.dumps({"ts": int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000),
                                            "canales": canales, "formatos": rank}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1:])
