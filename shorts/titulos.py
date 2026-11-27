"""La Bestia: elige el título que más va a pegar.

  python shorts/titulos.py --entrenar                # aprende de los Shorts de GTA 6 de los canales referentes (datos públicos)
  python shorts/titulos.py "Título 1" "Título 2" …   # puntúa y ordena títulos (nota 0-10 y por qué)
  python shorts/titulos.py --json "T1" "T2" …        # lo mismo en JSON (para la oficina y la fábrica)

Cómo aprende: para cada Short de GTA 6 de los referentes calcula cuántas veces supera la mediana de SU canal
(×N, así un canal pequeño cuenta igual que uno grande) y mide cuánto sube o baja ese ×N cuando el título tiene
cada rasgo (personaje, mayúsculas, emoji, «what happens if», aviso, cifra…). Guarda el modelo en
docs/titulos-modelo.json. Con pocos datos, cada rasgo se mezcla con una regla previa (lo aprendido a mano de los
Shorts que pasó Adam) para no exagerar. Nunca sustituye al criterio: el título tiene que ser verdad.
"""
from __future__ import annotations

import json
import math
import re
import statistics
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELO = RAIZ / "docs" / "titulos-modelo.json"
DATOS = RAIZ / "docs" / "titulos-datos.json"
sys.path.insert(0, str(Path(__file__).parent))

EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
PAL = re.compile(r"[\w$#'’]+")
GTA = re.compile(r"gta ?(6|vi)\b|\bjason\b|\blucia\b|leonida|vice city", re.I)

# rasgo: (cómo se detecta, peso previo en log(×N) aprendido de los virales que pasó Adam, explicación)
RASGOS = {
    "personaje":   (lambda t: bool(re.search(r"\b(jason|lucia|cool dog|randy|moses)\b", t, re.I)), 0.35, "nombra a un personaje"),
    "mayusculas":  (lambda t: 1 <= sum(1 for w in re.findall(r"[A-Za-z']+", t) if len(w) > 2 and w.isupper() and w not in ("GTA",)) <= 3, 0.25, "1-3 palabras en MAYÚSCULAS"),
    "todo_mayus":  (lambda t: sum(1 for w in re.findall(r"[A-Za-z']+", t) if len(w) > 2 and w.isupper() and w != "GTA") >= 5, -0.3, "demasiadas MAYÚSCULAS"),
    "emoji":       (lambda t: bool(EMOJI.search(t)), 0.2, "lleva emoji"),
    "que_pasa_si": (lambda t: bool(re.search(r"what happens if|what if|qu[eé] pasa si|que se passe", t, re.I)), 0.5, "«What happens if…?»"),
    "aviso":       (lambda t: bool(re.search(r"\b(don'?t|never|stop|run|avoid|warning|before you)\b", t, re.I)), 0.3, "aviso u orden"),
    "como":        (lambda t: bool(re.search(r"\bhow to\b|\bc[oó]mo\b", t, re.I)), 0.25, "«How to…» (promesa útil)"),
    "cifra":       (lambda t: bool(re.search(r"\$\s?\d|\d[\d,.]*\s?(k|m|million|billion|mil)\b|\b\d{3,}\b", t, re.I)), 0.2, "cifra llamativa"),
    "pregunta":    (lambda t: "?" in t, 0.15, "pregunta"),
    "suspense":    (lambda t: "..." in t or "…" in t, 0.2, "suspense (…)"),
    "secreto":     (lambda t: bool(re.search(r"secret|hidden|nobody|no one|easter egg|sab[ií]as", t, re.I)), 0.1, "secreto / ¿sabías que?"),
    "lista":       (lambda t: bool(re.match(r"^\s*\d+\s", t)), 0.0, "lista de N"),
    "serie":       (lambda t: bool(re.search(r"#\d", t)), 0.1, "serie numerada"),
    "corto":       (lambda t: 3 <= len(PAL.findall(t)) <= 8, 0.3, "corto (3-8 palabras)"),
    "largo":       (lambda t: len(PAL.findall(t)) >= 11, -0.3, "largo (11+ palabras)"),
}


def rasgos(t: str) -> list[str]:
    return [k for k, (f, _, _) in RASGOS.items() if f(t)]


def entrenar() -> None:
    import espia
    canales = [r["canal"] for r in json.loads((RAIZ / "docs" / "referentes.json").read_text())]
    filas = []
    for h in canales:
        try:
            c = espia.canal(h, todos=True)
        except Exception as e:   # un canal que falla no para el entrenamiento
            print("  ✗", h, e); continue
        gta = [s for s in c["shorts"] if GTA.search(s["titulo"]) and s["vistas"]]
        if len(gta) < 3:
            print(f"  · {h}: {len(gta)} Shorts de GTA 6, se salta"); continue
        med = statistics.median(s["vistas"] for s in gta)   # mediana de sus Shorts de GTA 6
        for s in gta:
            filas.append({"canal": h, "titulo": s["titulo"], "vistas": s["vistas"], "veces": round(s["vistas"] / med, 2)})
        print(f"  ✓ {h}: {len(gta)} Shorts de GTA 6 (mediana {int(med):,})")
    try:   # nuestro canal también cuenta
        hist = json.loads((RAIZ / "docs" / "canal-estadisticas.json").read_text())[-1]["shorts"]
        nuestros = [s for s in hist if s["vistas"]]
        med = statistics.median(s["vistas"] for s in nuestros)
        filas += [{"canal": "@vicecitydaystv", "titulo": s["titulo"], "vistas": s["vistas"], "veces": round(s["vistas"] / med, 2)} for s in nuestros]
    except Exception:
        pass
    DATOS.write_text(json.dumps(filas, ensure_ascii=False, indent=1))
    pesos = {}
    for k, (f, previo, txt) in RASGOS.items():
        con = [math.log(max(r["veces"], 0.05)) for r in filas if f(r["titulo"])]
        sin = [math.log(max(r["veces"], 0.05)) for r in filas if not f(r["titulo"])]
        if len(con) >= 3 and sin:
            dif = statistics.mean(con) - statistics.mean(sin)
            n = len(con); w = n / (n + 15)              # cuanto más datos, más manda lo medido
            pesos[k] = {"peso": round(w * dif + (1 - w) * previo, 3), "medido": round(dif, 3), "n": n, "previo": previo}
        else:
            pesos[k] = {"peso": previo, "medido": None, "n": len(con), "previo": previo}
    # acierto: de cada par de títulos del MISMO canal, ¿pone por delante al que de verdad tuvo más ×N?
    def sc(t): return sum(pesos[k]["peso"] for k in rasgos(t))
    bien = total = 0
    for i, a in enumerate(filas):
        for b in filas[i + 1:]:
            if a["canal"] != b["canal"] or a["veces"] == b["veces"] or sc(a["titulo"]) == sc(b["titulo"]):
                continue
            total += 1; bien += (sc(a["titulo"]) > sc(b["titulo"])) == (a["veces"] > b["veces"])
    acierto = round(100 * bien / total) if total else None
    MODELO.write_text(json.dumps({"filas": len(filas), "canales": len({r['canal'] for r in filas}), "acierto": acierto, "pares": total, "pesos": pesos}, ensure_ascii=False, indent=1))
    print(f"Acierto: elige el mejor de cada pareja el {acierto} % de las veces ({total} parejas; al azar sería el 50 %)")
    print(f"Modelo: {len(filas)} títulos de {len({r['canal'] for r in filas})} canales → {MODELO.relative_to(RAIZ)}")
    for k, v in sorted(pesos.items(), key=lambda x: -x[1]["peso"]):
        print(f"  {v['peso']:+.2f}  {k:12} (medido {v['medido']}, n={v['n']})")


def puntuar(t: str) -> dict:
    m = json.loads(MODELO.read_text())["pesos"] if MODELO.exists() else {k: {"peso": p} for k, (_, p, _) in RASGOS.items()}
    rs = rasgos(t)
    s = sum(m[k]["peso"] for k in rs)
    nota = round(max(0.0, min(10.0, 5 + 2.5 * s)), 1)        # 5 = título normal; cada +0,4 de log(×N) (×1,5) suma 1 punto
    falta = [RASGOS[k][2] for k in sorted(m, key=lambda k: -m[k]["peso"])[:5] if k not in rs and m[k]["peso"] > 0.2]
    return {"titulo": t, "nota": nota, "tiene": [RASGOS[k][2] for k in rs if m[k]["peso"] > 0],
            "resta": [RASGOS[k][2] for k in rs if m[k]["peso"] < -0.05], "le_falta": falta, "chars": len(t)}


def main(a: list[str]) -> None:
    if a and a[0] == "--entrenar":
        return entrenar()
    js = a and a[0] == "--json"
    tits = a[1:] if js else a
    res = sorted((puntuar(t) for t in tits), key=lambda r: -r["nota"])
    if js:
        print(json.dumps(res, ensure_ascii=False)); return
    for i, r in enumerate(res):
        print(f"{'🏆' if i == 0 else '  '} {r['nota']:>4}/10  {r['titulo']}")
        print(f"        + {', '.join(r['tiene']) or '—'}" + (f"  · − {', '.join(r['resta'])}" if r['resta'] else "") + (f"  · le falta: {', '.join(r['le_falta'])}" if r['le_falta'] else ""))


if __name__ == "__main__":
    main(sys.argv[1:])
