"""Examen de calidad de un Short: cada trabajador del equipo tiene sus pruebas medibles.

  python shorts/examen.py shorts/NN-nombre [--rapido]      # --rapido: sin medir el volumen (más lento)
  python shorts/examen.py --todos                          # examina todos los Shorts de shorts/
  python shorts/examen.py --todos --oficina salida.json    # además prepara estado/equipo para la oficina

Las reglas salen de docs/manual-shorts.md (manual magistral del equipo) y del documento maestro.
Un Short solo se entrega si NO tiene fallos (✗). Los avisos (⚠) son mejoras recomendadas.
Devuelve código 1 si hay algún fallo, para poder usarlo en el paso 6 (Revisión de calidad).
"""
from __future__ import annotations

import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BANCO = RAIZ / "docs" / "banco-ideas.md"
CATALOGO = RAIZ / "docs" / "catalogo-imagenes.json"
CTA = "follow for more gta 6 secrets"
AVISO = "Unofficial fan-made channel. Not affiliated with Rockstar Games or Take-Two Interactive."
MULETILLAS = ["in this video", "hey guys", "welcome back", "what's up", "make sure to", "don't forget to", "smash", "let's dive"]
RUMOR = ["leak", "leaked", "rumor", "rumour", "insider", "reportedly", "allegedly"]
CURIOSIDAD = re.compile(r"(\d|\?|…|\.\.\.|\bONE\b|\bexcept\b|\bonly\b|\bjust\b|\bsecret|\breal\b|\bnever\b|\bwhy\b|\bhow\b)", re.I)
EVITAR_1A = re.compile(r"\b(club|nightclub|dancer|strip|nude|topless|dead|corpse|blood)\b", re.I)
FORMATOS = ["juego vs real", "noticia", "personajes", "secreto", "lista", "comparativa", "curiosidad", "truco"]

EQUIPO = {
    "jarvis": "Jarvis · tendencias",
    "nobita": "Nobita · verificación y derechos",
    "torrente": "Torrente · títulos y ganchos",
    "chapo": "El Chapo · guion",
    "pablito": "Pablito · retención",
    "victillor": "Victillor · formato Short",
    "nil": "Nil · visuales",
    "cristiano": "Cristiano · voz",
    "georgina": "Georgina · montaje",
    "guerrero": "Guerrero · publicación y SEO",
    "taison": "Taison · datos",
    "almudena": "Almudena · calidad final",
}


class Examen:
    def __init__(self, carpeta: Path, rapido: bool):
        self.c = carpeta
        self.rapido = rapido
        self.res: list[tuple[str, str, str, str]] = []   # (quien, estado ok|aviso|fallo, prueba, detalle)

    def r(self, quien, cond, prueba, detalle="", aviso=False):
        self.res.append((quien, "ok" if cond else ("aviso" if aviso else "fallo"), prueba, detalle))

    def leer(self, nombre):
        p = self.c / nombre
        return p.read_text(encoding="utf-8") if p.exists() else ""

    # ------------------------------------------------------------------ datos
    def cargar(self):
        self.inv = self.leer("investigacion.md")
        self.guion = self.leer("guion.md")
        self.voz = self.leer("voz.txt").strip()
        self.pub = self.leer("publicacion.md")
        self.plan = json.loads(self.leer("plan.json") or "{}")
        pal = self.c / self.plan.get("palabras", "palabras.json")
        self.pal = json.loads(pal.read_text()) if pal.exists() else []
        vid = self.c / self.plan.get("salida", "final.mp4")
        self.video = vid if vid.exists() else None
        m = re.search(r"\*\*Título[^*]*:\*\*\s*(.+)", self.pub)
        self.titulo = m.group(1).strip() if m else ""
        bloques = re.findall(r"```\n?(.*?)```", self.pub, flags=re.S)
        self.desc = bloques[0] if bloques else ""
        m = re.search(r"\*\*Comentario fijado:?\*\*:?\s*(?:```\n?(.*?)```|(.+))", self.pub, flags=re.S)
        self.fijado = ((m.group(1) or m.group(2)) if m else "").strip()
        cab = self.pub.split("**Descripción")[0]
        self.alternativos = re.findall(r"^\s*[-·]\s+.+$", cab, flags=re.M)
        for linea in re.findall(r"Alternativos?[^:]*:\*?\*?\s*(.+)", cab):   # "A" · "B" en una sola línea
            self.alternativos += [x for x in re.split(r"\s+·\s+", linea) if len(x.strip(' "“”')) > 8]
        self.frases = [f.strip() for f in re.split(r"(?<=[.!?])\s+", self.voz) if f.strip()]

    def info_video(self):
        if not self.video:
            return {}
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                              "stream=width,height,r_frame_rate:format=duration", "-of", "json", str(self.video)],
                             capture_output=True, text=True).stdout
        d = json.loads(out)
        st, fmt = d["streams"][0], d["format"]
        n, den = st["r_frame_rate"].split("/")
        info = {"w": st["width"], "h": st["height"], "fps": float(n) / float(den), "dur": float(fmt["duration"])}
        if not self.rapido:
            log = subprocess.run(["ffmpeg", "-nostats", "-i", str(self.video), "-af", "ebur128=peak=true:framelog=quiet",
                                  "-f", "null", "-"], capture_output=True, text=True).stderr
            i = re.findall(r"I:\s+(-?[\d.]+) LUFS", log)
            p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", log)
            info["lufs"] = float(i[-1]) if i else None
            info["pico"] = float(p[-1]) if p else None
        return info

    # ------------------------------------------------------------------ pruebas
    def pruebas(self):
        self.cargar()
        v = self.info_video()
        voz_l = self.voz.lower()
        palabras = re.findall(r"[A-Za-z0-9']+", self.voz)
        fin_voz = self.pal[-1]["e"] if self.pal else 0

        # Jarvis · tendencias
        self.r("jarvis", bool(re.search(r"20\d\d|\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4}", self.inv)), "La investigación lleva fecha")
        self.r("jarvis", any(k in self.inv.lower() for k in ["banco", "encargo", "tendencia", "noticia", "lanzamiento", "descartado"]),
               "Explica de dónde sale la idea o qué se descartó", aviso=True)

        # Nobita · verificación y derechos
        urls = set(re.findall(r"(?:https?://)?(?:www\.)?[a-z0-9-]+\.(?:com|org|gov|net|co\.uk)[/\w.-]*", self.inv))
        self.r("nobita", len(urls) >= 1 and ("rockstargames.com" in self.inv or len(urls) >= 2), "Datos con fuente (Rockstar o 2 medios)", f"{len(urls)} fuentes")
        citas = re.findall(r"[\"“][^\"”]{15,}[\"”]", self.inv)
        self.r("nobita", len(citas) >= 3, "Al menos 3 citas literales en investigacion.md", f"{len(citas)} citas")
        malas = [w for w in RUMOR if re.search(rf"\b{w}\b", voz_l)]
        self.r("nobita", not malas, "La voz no da rumores como hechos", ", ".join(malas))
        self.r("nobita", AVISO in self.desc, "Aviso de canal no oficial en la descripción")
        imgs = [e.get("img") or f"{e.get('video')}@{e.get('inicio')}" for e in self.plan.get("escenas", [])]
        clips = [e for e in self.plan.get("escenas", []) if e.get("video")]
        if clips:
            vcat = json.loads((RAIZ / "docs" / "catalogo-videos.json").read_text()) if (RAIZ / "docs" / "catalogo-videos.json").exists() else []
            malos = [c["id"] for c in vcat if c["evitar"] and any(Path(e["video"]).stem == c["video"] and c["inicio"] - 0.2 <= e.get("inicio", 0) <= c["fin"] for e in clips)]
            self.r("nobita", not malos, "Ningún plano prohibido (logo oficial, club, arma a cámara…)", ", ".join(malos))
            self.r("nobita", "rockstar games" in self.desc.lower(), "Crédito de Rockstar Games en la descripción (footage)")
            largos = [round(e["hasta"] - e["desde"], 1) for e in clips if e["hasta"] - e["desde"] > 3.5 and e["hasta"] < 90]
            self.r("nobita", not largos, "Planos de vídeo cortos (≤ 3,5 s): nada de escenas enteras", str(largos))
        n_esc = len(self.plan.get("escenas", []))
        self.r("nil", n_esc and len(clips) / n_esc >= 0.5, "Opinión de Adam: al menos la mitad de las escenas son clips en movimiento", f"{len(clips)} de {n_esc}", aviso=True)
        self.r("nobita", not any("Vice_City_07" in i for i in imgs), "No usa Vice_City_07")
        self.r("nobita", "logo" not in json.dumps(self.plan).lower(), "Sin logo oficial de GTA VI")

        # Torrente · títulos y ganchos
        t = self.titulo
        self.r("torrente", 0 < len(t) <= 70, "Título de 70 caracteres o menos", f"{len(t)}: {t}")
        self.r("torrente", len(t) <= 50, "Título corto (≤ 50, se lee entero en el móvil)", f"{len(t)} caracteres", aviso=True)
        self.r("torrente", bool(CURIOSIDAD.search(t)), "El título abre curiosidad (número, ONE, except, ?, …)")
        self.r("torrente", len(self.alternativos) >= 2, "2 títulos alternativos para probar", f"{len(self.alternativos)}")
        gancho = self.frases[0] if self.frases else ""
        usados = self.leer_ganchos_usados()
        repetido = [u for u in usados if gancho and similar(gancho, u) > 0.8 and not self.es_propio(u)]
        self.r("torrente", not repetido, "Gancho nuevo (no está en Ganchos usados)", repetido[0] if repetido else "")
        self.r("torrente", bool(re.search(r"\d|\b(one|only|never|real|secret|just|didn't|isn't|wasn't|not|no|nobody|every)\b|\?", gancho, re.I)),
               "Gancho concreto (número, contraste, negación o pregunta)", gancho[:70])

        # El Chapo · guion
        # Duración según formato (decisión de Adam, 21/11/2026): trucos 25-35 s; listas, «cómo funciona» y GTA 6 contra GTA 5 hasta 55 s.
        fmt_pub = (re.search(r"\*\*Formato:\*\*\s*(.+)", self.pub or "") or [None, ""])[1].lower()
        largo = bool(re.match(r"\s*[3-5]\s", t)) or any(k in fmt_pub for k in ("lista", "comparativa", "cómo funciona", "como funciona", "gran pregunta"))
        lo, hi, ilo, ihi, txt = (65, 165, 95, 150, "25-55 s, formato largo") if largo else (65, 100, 75, 95, "25-35 s")
        self.r("chapo", lo <= len(palabras) <= hi, f"Guion de {lo} a {hi} palabras ({txt})", f"{len(palabras)} palabras")
        self.r("chapo", ilo <= len(palabras) <= ihi, f"Guion ideal de {ilo} a {ihi} palabras", f"{len(palabras)} palabras", aviso=True)
        self.r("chapo", voz_l.rstrip(". !").endswith(CTA), "Termina con 'Follow for more GTA 6 secrets'")
        tu = len(re.findall(r"\byou(r|'re|'ll)?\b", voz_l))
        giro = bool(re.search(r"\b(but|catch|actually|wait|crazy|no joke|here's the)\b", voz_l))
        self.r("chapo", tu >= 3 and giro, "Guion con personalidad: habla a 'you' (3+) y tiene un giro (but, catch, wait…)", f"you×{tu}, giro: {'sí' if giro else 'no'}", aviso=True)
        mul = [m for m in MULETILLAS if m in voz_l]
        self.r("chapo", not mul, "Sin muletillas ('in this video', 'hey guys'…)", ", ".join(mul))
        largas = [f for f in self.frases if len(f.split()) > 22]
        self.r("chapo", not largas, "Frases cortas para leer en voz alta (≤ 22 palabras)", largas[0][:60] if largas else "")
        facts = [c for c in self.plan.get("capas", []) if c.get("tipo") == "fact"]
        # Las listas («5 Things…», formato de los canales que explotan) llevan tantos datos como diga el título (3 a 5).
        n_lista = re.match(r"\s*([3-5])\s", t)
        esperados = int(n_lista.group(1)) if n_lista else 3
        self.r("chapo", len(facts) == esperados, f"Estructura gancho → {esperados} datos → CTA", f"{len(facts)} datos")

        # Pablito · retención
        if self.pal:
            self.r("pablito", self.pal[0]["s"] <= 0.3, "La voz empieza en el primer 0,3 s", f"{self.pal[0]['s']:.2f} s")
            n1 = len(re.findall(r"[A-Za-z0-9']+", gancho))
            fin_gancho = self.pal[min(n1, len(self.pal)) - 1]["e"] if n1 else 0
            self.r("pablito", fin_gancho <= 3.0, "La primera frase del gancho dura 3 s o menos", f"{fin_gancho:.1f} s")
            huecos = [b["s"] - a["e"] for a, b in zip(self.pal, self.pal[1:])]
            self.r("pablito", max(huecos) <= 0.9, "Sin silencios de más de 0,9 s", f"máx. {max(huecos):.2f} s")
        titulo_capa = [c for c in self.plan.get("capas", []) if c.get("tipo") == "titulo"]
        self.r("pablito", bool(titulo_capa) and titulo_capa[0]["desde"] <= 0.05, "Texto en pantalla desde el fotograma 0")
        cortes = [min(e["hasta"], fin_voz or e["hasta"]) - e["desde"] for e in self.plan.get("escenas", []) if e["desde"] < (fin_voz or 99)]
        if cortes:
            media = statistics.mean(cortes[:-1] or cortes)
            self.r("pablito", media <= 2.6, "Cambio de imagen cada ~2,2 s (media ≤ 2,6 s)", f"media {media:.2f} s")
            mx = max(cortes[:-1] or cortes)
            self.r("pablito", mx <= 4.0, "Ninguna imagen dura más de 4 s (sin contar el CTA)", f"máx. {mx:.2f} s")
            self.r("pablito", mx <= 3.2, "Ideal: ninguna imagen más de 3,2 s", f"máx. {mx:.2f} s", aviso=True)
        # bucle perfecto: la última frase antes del CTA retoma palabras del gancho, para que el final enlace con el principio
        if len(self.frases) >= 3:
            claves = {w for w in re.findall(r"[a-z']{4,}", gancho.lower())} - {"this", "that", "with", "your", "there", "have", "just"}
            penultima = self.frases[-2].lower()
            self.r("pablito", any(w in penultima for w in claves), "Bucle perfecto: la última frase antes del CTA retoma el gancho", self.frases[-2][:60], aviso=True)
        bucle = bool(re.search(r"\b(except|but|one|which|who|guess|wait)\b|\?", gancho + " " + t, re.I))
        self.r("pablito", bucle, "Abre un bucle que se cierra al final (except/but/one/pregunta)", aviso=True)

        # Victillor · formato Short
        if v:
            self.r("victillor", v["w"] == 1080 and v["h"] == 1920, "Vertical 1080×1920", f"{v['w']}×{v['h']}")
            self.r("victillor", abs(v["fps"] - 30) < 0.5, "30 fotogramas por segundo", f"{v['fps']:.1f}")
            dmax = 55 if largo else 35
            self.r("victillor", 25 <= v["dur"] <= dmax, f"Dura entre 25 y {dmax} s", f"{v['dur']:.1f} s")
        else:
            self.r("victillor", False, "Existe el vídeo final", "falta final.mp4")
        cta = [c for c in self.plan.get("capas", []) if c.get("tipo") == "cta"]
        self.r("victillor", bool(cta) and fin_voz - cta[0]["desde"] <= 4.0, "CTA en pantalla solo los últimos 4 s", f"{fin_voz - cta[0]['desde']:.1f} s" if cta else "sin CTA")

        # Nil · visuales
        self.r("nil", len(set(imgs)) >= 8, "Al menos 8 capturas distintas", f"{len(set(imgs))}")
        rep = max((imgs.count(i) for i in set(imgs)), default=0)
        self.r("nil", rep <= 2, "Ninguna captura se repite más de 2 veces", f"máx. {rep}")
        flechas = sum(1 for e in self.plan.get("escenas", []) if e.get("etiqueta", {}).get("flecha"))
        self.r("nil", flechas >= 2, "Al menos 2 flechas rojas que señalan la prueba del dato", f"{flechas}")
        etiquetas = sum(1 for e in self.plan.get("escenas", []) if e.get("etiqueta"))
        self.r("nil", etiquetas >= 5, "Etiquetas en pantalla en 5 escenas o más", f"{etiquetas}", aviso=True)
        primera = imgs[0] if imgs else ""
        alt = self.alt_de(primera)
        self.r("nil", not EVITAR_1A.search(alt), "Primera imagen apta (sin clubes, desnudos ni muertos)", alt[:70])

        # Cristiano · voz
        if self.pal and fin_voz:
            ritmo = len(self.pal) / fin_voz
            # calibrado con el canal: el Short que más funciona (04, Florida) va a 2,5 palabras/s
            self.r("cristiano", 2.3 <= ritmo <= 3.8, "Ritmo de voz entre 2,3 y 3,8 palabras/s", f"{ritmo:.2f} palabras/s")
        vozf = self.c / self.plan.get("voz", "voz.mp3")
        self.r("cristiano", vozf.exists(), "Existe la locución", vozf.name)

        # Georgina · montaje
        if v and "lufs" in v and v["lufs"] is not None:
            self.r("georgina", abs(v["lufs"] + 14) <= 1.0, "Volumen −14 LUFS (±1)", f"{v['lufs']} LUFS")
            self.r("georgina", v["pico"] is None or v["pico"] <= -0.5, "Sin saturar (pico ≤ −0,5 dBFS)", f"{v['pico']} dBFS")
        self.r("georgina", len(self.plan.get("palabras_clave", [])) >= 8, "Palabras clave en amarillo (≥ 8)", f"{len(self.plan.get('palabras_clave', []))}")
        self.r("georgina", bool(self.plan.get("marca")), "Marca VICECITY DAYS TV arriba a la derecha")
        self.r("georgina", not self.plan.get("mostrar_fuente"), "Pantalla limpia: sin línea de fuentes ni créditos abajo (van en la descripción)")
        self.r("georgina", bool(self.plan.get("musica")), "Ritmo de fondo con sidechain")

        # Guerrero · publicación y SEO
        self.r("guerrero", all(h in self.desc for h in ["#GTA6", "#GTAVI", "#Shorts"]), "Hashtags #GTA6 #GTAVI #Shorts")
        self.r("guerrero", self.desc.count("✅") + self.desc.count("❌") >= 3, "Los 3 datos en la descripción con ✅/❌")
        self.r("guerrero", bool(re.search(r"Sources?:", self.desc)), "Fuentes en la descripción")
        self.r("guerrero", "?" in self.fijado, "Comentario fijado con pregunta", self.fijado[:60])
        self.r("guerrero", "Contenido alterado" in self.pub and "niños" in self.pub, "Ajustes: contenido alterado y hecho para niños")
        primera_linea = self.desc.strip().split("\n")[0] if self.desc else ""
        self.r("guerrero", 0 < len(primera_linea) <= 160, "La 1.ª línea de la descripción engancha (≤ 160 caracteres)", f"{len(primera_linea)}", aviso=True)

        # Taison · datos
        fmt = re.search(r"\*\*Formato:\*\*\s*(.+)", self.pub)
        self.r("taison", bool(fmt) and any(f in fmt.group(1).lower() for f in FORMATOS),
               "Formato etiquetado en publicacion.md (para comparar qué funciona)", fmt.group(1) if fmt else f"añade **Formato:** ({', '.join(FORMATOS)})")
        self.r("taison", "Gancho:" in self.pub or "**Gancho" in self.pub or "Gancho" in self.guion, "Gancho anotado para medir 'vistos frente a deslizados'", aviso=True)

        # Almudena · calidad final
        entregable = list(self.c.glob("VCDT_*.mp4"))
        self.r("almudena", bool(entregable), "Copia VCDT_NN_<Título>.mp4 lista para subir")
        self.r("almudena", all((self.c / f).exists() for f in ["investigacion.md", "guion.md", "publicacion.md", "plan.json"]),
               "Carpeta completa (investigación, guion, publicación y plan)")

    # ------------------------------------------------------------------ ayudas
    def leer_ganchos_usados(self):
        s = BANCO.read_text(encoding="utf-8") if BANCO.exists() else ""
        parte = s.split("## Ganchos usados")[-1] if "## Ganchos usados" in s else ""
        return [re.sub(r'^[-\s"“]+|["”\s]+$', "", l) for l in parte.splitlines() if l.strip().startswith("-")]

    def es_propio(self, gancho_usado):
        return similar(gancho_usado, self.frases[0] if self.frases else "") > 0.8 and \
            any(similar(gancho_usado, " ".join(self.frases[:k])) > 0.8 for k in (1, 2, 3))

    def alt_de(self, img):
        nombre = Path(img).stem
        try:
            cat = json.loads(CATALOGO.read_text())
            for it in cat:
                if f"{it['grupo']}_{it['num']}" == nombre:
                    return it.get("alt", "")
        except Exception:
            pass
        return nombre.replace("_", " ")

    # ------------------------------------------------------------------ informe
    def informe(self):
        print(f"\n=== Examen · {self.c.name} ===")
        total = len(self.res)
        bien = sum(1 for x in self.res if x[1] == "ok")
        for quien, nombre in EQUIPO.items():
            mias = [x for x in self.res if x[0] == quien]
            if not mias:
                continue
            ok = sum(1 for x in mias if x[1] == "ok")
            print(f"{nombre:<34} {ok}/{len(mias)}")
            for _, est, prueba, det in mias:
                if est != "ok":
                    print(f"   {'✗' if est == 'fallo' else '⚠'} {prueba}" + (f"  → {det}" if det else ""))
        fallos = sum(1 for x in self.res if x[1] == "fallo")
        nota = round(10 * bien / total, 1) if total else 0
        print(f"NOTA: {nota}/10 · {bien}/{total} pruebas · {fallos} fallos · " + ("APTO para entregar" if not fallos else "NO APTO: corregir los ✗"))
        return fallos, nota


def similar(a: str, b: str) -> float:
    import difflib
    norm = lambda x: re.sub(r"[^a-z0-9 ]", "", x.lower())
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def titulo_de(carpeta: Path) -> str:
    pub = (carpeta / "publicacion.md").read_text(encoding="utf-8") if (carpeta / "publicacion.md").exists() else ""
    m = re.search(r"\*\*Título[^*]*:\*\*\s*(.+)", pub)
    return m.group(1).strip() if m else carpeta.name


def main(args):
    oficina = args[args.index("--oficina") + 1] if "--oficina" in args else None
    if oficina:
        args = [a for a in args if a != oficina]
    rapido = "--rapido" in args
    args = [a for a in args if not a.startswith("--")] if "--todos" not in sys.argv else \
        sorted(str(p) for p in (RAIZ / "shorts").glob("[0-9][0-9]-*") if (p / "plan.json").exists())
    total_fallos = 0
    por_quien: dict[str, list[int]] = {}
    shorts = []
    for a in args:
        e = Examen(Path(a), rapido)
        e.pruebas()
        f, nota = e.informe()
        total_fallos += f
        for q, est, *_ in e.res:
            t = por_quien.setdefault(q, [0, 0])
            t[0] += est == "ok"
            t[1] += 1
        shorts.append({"carpeta": Path(a).name, "titulo": titulo_de(Path(a)), "nota": nota, "apto": not f})
    if oficina:
        import datetime as dt
        notas = {q: f"{ok}/{n}" for q, (ok, n) in por_quien.items()}
        media = round(sum(s["nota"] for s in shorts) / len(shorts), 1) if shorts else None
        Path(oficina).write_text(json.dumps({"ts": int(dt.datetime.now(dt.timezone.utc).timestamp() * 1000),
                                             "notas": notas, "media": media, "shorts": shorts}, ensure_ascii=False))
    sys.exit(1 if total_fallos else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
