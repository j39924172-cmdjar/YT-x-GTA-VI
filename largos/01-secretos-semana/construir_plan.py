"""Construye plan.json del vídeo largo 01 a partir de palabras.json (tiempos reales de la voz).

  python largos/01-secretos-semana/construir_plan.py
"""
import json
import re
from pathlib import Path

B = Path(__file__).parent
P = json.loads((B / "palabras.json").read_text())
LT, PL = "../../videos/oficiales/GTAVI_Launch_Trailer.mp4", "../../videos/oficiales/GTAVI_Pre-Load_Now.mp4"
CL = {  # planos ✅ del catálogo (inicio, fin)
    "LT03": (LT, 7.02, 9.92), "LT05": (LT, 11.95, 14.15), "LT06": (LT, 14.25, 15.12), "LT09": (LT, 26.42, 27.78),
    "LT10": (LT, 27.88, 29.35), "LT12": (LT, 32.85, 33.58), "LT17": (LT, 39.05, 40.38), "LT18": (LT, 40.48, 42.28),
    "LT21": (LT, 47.02, 48.85), "LT23": (LT, 55.22, 57.02), "LT25": (LT, 58.55, 59.85), "LT27": (LT, 63.22, 63.98),
    "LT29": (LT, 67.12, 68.48), "LT30": (LT, 68.58, 72.72), "LT32": (LT, 73.85, 76.4), "PL02": (PL, 5.25, 6.72),
    "PL06": (PL, 11.25, 12.62), "LT02": (LT, 2.72, 6.92),
}
NUM = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen".split()
COLORES = ["morado", "rosa", "amarillo", "lila", "rosa"]

SECRETOS = [  # título, capítulo, visuales
    ("THE $250K CHEAT", 1, ["VINTAGE_VICE_CITY_WEAPON_PATTERN_01", "Boobie_Ike_01", "Raul_Bautista_02", "ULTIMATE_EDITION_GROTTI_CHEETAH_01"]),
    ("SECRET FIRST-PERSON", 1, ["Jason_Duval_02", "LT09", "Lucia_Caminos_12", "Jason_Duval_19", "Jason_Duval_04"]),
    ("A LITERAL EASTER EGG", 1, ["Vice_City_03", "LT27", "Vice_City_27", "Mount_Kalaga_National_Park_02", "Vice_City_08"]),
    ("THE WAY DOWN", 1, ["LT30", "Vice_City_27", "LT17"]),
    ("PAUL WALKER'S CAR", 2, ["ULTIMATE_EDITION_02", "Vice_City_24", "ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_01", "LT18", "ULTIMATE_EDITION_WYMAN_CAR_COLLECTION_03"]),
    ("THE SNAKE IN THE TRUNK", 2, ["Grassrivers_07", "ULTIMATE_EDITION_02", "Grassrivers_03"]),
    ("DEXTER'S APARTMENT", 2, ["Vice_City_02", "Vice_City_26", "Vice_City_15", "LT32"]),
    ("THE KILL KIT & THE BOAT", 2, ["Vice_City_15", "PL06", "Raul_Bautista_03", "Grassrivers_02"]),
    ("MICHAEL'S BOAT?", 3, ["LT03", "Brian_Heder_04", "Brian_Heder_02", "LT05", "Brian_Heder_01"]),
    ("RED DEAD MONEY", 3, ["VINTAGE_VICE_CITY_WEAPON_PATTERN_01", "Raul_Bautista_02", "Boobie_Ike_01"]),
    ("A BOAT CALLED LEONIDA", 3, ["Leonida_Keys_05", "Grassrivers_02", "Leonida_Keys_01", "LT12"]),
    ("THE VERCETTI ESTATE", 3, ["ULTIMATE_EDITION_HAWK_AND_LITTLE_MORGAN_REVOLVERS_01", "VINTAGE_VICE_CITY_PACK_01", "ULTIMATE_EDITION_HAWK_AND_LITTLE_MORGAN_REVOLVERS_02", "VINTAGE_VICE_CITY_PACK_02"]),
    ("GAMES INSIDE THE GAME", 3, ["LT25", "Cal_Hampton_03", "Brian_Heder_02", "Real_Dimez_04"]),
    ("THE FIGHTER JET", 4, ["Vice_City_01", "LT17", "Jason_Duval_11", "Mount_Kalaga_National_Park_02"]),
    ("COOL DOG", 4, ["Leonida_Keys_01", "LT06", "Vice_City_19", "Leonida_Keys_05", "Leonida_Keys_04"]),
    ("SKUNK APE", 4, ["Grassrivers_08", "LT10", "Mount_Kalaga_National_Park_05", "Grassrivers_03", "Mount_Kalaga_National_Park_03"]),
    ("HE KNOWS IT'S A GAME", 5, ["Ambrosia_02", "Raul_Bautista_01", "Mount_Kalaga_National_Park_04", "Port_Gellhorn_02"]),
    ("THE UFO", 5, ["Port_Gellhorn_01", "Ambrosia_02", "Port_Gellhorn_05", "Mount_Kalaga_National_Park_04"]),
]
CAPITULOS = ["Hidden in plain sight", "Movie & TV tributes", "Rockstar's own history", "Leonida's wild side", "The truth is out there"]
GANCHO = ["LT30", "Vice_City_27", "Leonida_Keys_01", "Ambrosia_02", "LT23"]
FINAL = ["Jason_and_Lucia_16", "LT29", "ULTIMATE_EDITION_01", "Vice_City_08"]

norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())


def buscar(frase, desde=0.0):
    f = [norm(x) for x in frase.split()]
    for i in range(len(P) - len(f) + 1):
        if P[i]["s"] >= desde and [norm(P[i + k]["w"]) for k in range(len(f))] == f:
            return P[i]["s"]
    raise SystemExit(f"no encuentro: {frase}")


fin = P[-1]["e"] + 1.2
ini_cap = [buscar(f"Part {w}.") - 0.2 for w in ["one", "two", "three", "four", "five"]]
ini_sec = [buscar(f"Number {NUM[i]}.", ini_cap[0]) - 0.15 for i in range(18)]
fin_ultimo = buscar("That is eighteen secrets") - 0.2

escenas, usados = [], {}
FOCOS = [[0.5, 0.5], [0.4, 0.45], [0.6, 0.5], [0.5, 0.4], [0.45, 0.55]]


def tramo(desde, hasta, lista):
    t, k = desde, 0
    while t < hasta - 0.05:
        v = lista[k % len(lista)]
        k += 1
        if v in CL:
            ruta, a, b = CL[v]
            d = min(b - a, 3.6, hasta - t)
            escenas.append({"video": ruta, "inicio": a, "desde": round(t, 3), "hasta": round(t + d, 3), "zoom": [1.0, 1.0]})
        else:
            d = min(5.2, hasta - t)
            if hasta - (t + d) < 1.5:      # no dejar restos cortos
                d = hasta - t
            n = usados.get(v, 0); usados[v] = n + 1
            z = [1.04, 1.16] if (len(escenas) % 2 == 0) else [1.16, 1.04]
            f0 = FOCOS[(len(escenas) + n) % len(FOCOS)]
            f1 = [min(max(f0[0] + (0.06 if n % 2 else -0.06), 0.3), 0.7), f0[1]]
            escenas.append({"img": f"capturas/{v}.jpg", "desde": round(t, 3), "hasta": round(t + d, 3), "foco": f0, "foco_fin": f1, "zoom": z})
        t += d


tramo(0, ini_cap[0], GANCHO)
secretos = []
for i, (tit, cap, vis) in enumerate(SECRETOS):
    a = ini_sec[i]
    sig = [x for x in ini_sec[i + 1:i + 2] + [c for c in ini_cap if c > a] + [fin_ultimo]]
    b = min(sig)
    if i + 1 < 18 and cap != SECRETOS[i + 1][1]:
        b = min(b, ini_cap[cap])
    if a > ini_cap[cap - 1] and (i == 0 or SECRETOS[i - 1][1] != cap):
        tramo(ini_cap[cap - 1], a, vis[-1:])     # la tarjeta de capítulo va sobre una imagen del primer secreto
    tramo(a, b, vis)
    secretos.append({"n": i + 1, "titulo": tit, "desde": round(a, 3), "hasta": round(b, 3), "color": COLORES[cap - 1]})
tramo(fin_ultimo, fin, FINAL)

T = lambda f, d=0: round(buscar(f, d), 3)
tarjetas = [
    {"tipo": "lista", "titulo": "The money cheat", "lineas": ["UP · RIGHT · DOWN · LEFT", "UP · LEFT · DOWN · RIGHT", "= $250,000", "Only after you finish the story"],
     "desde": T("Press up, right"), "hasta": T("Other cheats are earned")},
    {"tipo": "pastilla", "texto": "PLAYER WORKAROUND · NOT OFFICIAL", "fondo": "amarillo", "desde": T("One player found a way"), "hasta": T("One player found a way") + 5},
    {"tipo": "pastilla", "texto": "CLIMB: 6-7 MINUTES", "fondo": "amarillo", "desde": T("climbing it takes"), "hasta": T("climbing it takes") + 5},
    {"tipo": "lista", "titulo": "A literal Easter egg", "lineas": ["GTA Vice City · 2002", "GTA 6 · 2026", "24 years later, same joke"],
     "desde": T("GTA Vice City, back in 2002"), "hasta": T("Same joke, a whole new")+3},
    {"tipo": "pastilla", "texto": "VESPUCCI ISLAND · VICE CITY", "fondo": "amarillo", "desde": T("In a villa garage"), "hasta": T("In a villa garage") + 5},
    {"tipo": "lista", "titulo": "Two movie references", "lineas": ["Fast & Furious (2001): the green Eclipse", "Toy Story: \"There's a snake in my boot!\""],
     "desde": T("Two movie references"), "hasta": T("Two movie references") + 6},
    {"tipo": "pastilla", "texto": "WASHINGTON ISLAND · VICE CITY", "fondo": "amarillo", "desde": T("spotted a building on Washington"), "hasta": T("spotted a building on Washington") + 5},
    {"tipo": "pastilla", "texto": "FAN THEORY · NOT CONFIRMED", "fondo": "amarillo", "desde": T("Some fans point out small differences"), "hasta": T("Some fans point out small differences") + 5},
    {"tipo": "lista", "titulo": "On Leonida's cash", "lineas": ["President Hardin", "President Thaddeus Waxman", "Both from the Red Dead Redemption series"],
     "desde": T("The faces on the bills"), "hasta": T("So the money in Leonida")},
    {"tipo": "lista", "titulo": "Red Dead Redemption 2 files", "lineas": ["Unused boat texture (2018 game)", "Ship names include...", "\"THE LEONIDA\""],
     "desde": T("It lists several ship names"), "hasta": T("Red Dead 2 came out") + 3},
    {"tipo": "lista", "titulo": "Rockstar's own words", "lineas": ["Ultimate Edition revolvers with", "\"Vice City stylings sourced from", "the Vercetti Estate\""],
     "desde": T("Rockstar's own description says"), "hasta": T("The Vercetti Estate was Tommy")},
    {"tipo": "pastilla", "texto": "MILE ZERO AIR STATION · GOOSE KEY", "fondo": "amarillo", "desde": T("At Mile Zero Air Station"), "hasta": T("At Mile Zero Air Station") + 5},
    {"tipo": "pastilla", "texto": "5 STARS + 2 JETS ON YOUR TAIL", "fondo": "rosa", "desde": T("you instantly get five stars"), "hasta": T("you instantly get five stars") + 5},
    {"tipo": "pastilla", "texto": "REWARD: ABOUT $1,200", "fondo": "amarillo", "desde": T("Reports say you can find around"), "hasta": T("Reports say you can find around") + 5},
    {"tipo": "pastilla", "texto": "SOUTH OF COTTONMOUTH LAKE · BELOW HAMLET", "fondo": "amarillo", "desde": T("In the swamps south of"), "hasta": T("In the swamps south of") + 5},
    {"tipo": "pastilla", "texto": "BELVILLE · LEONARD COUNTY", "fondo": "amarillo", "desde": T("found that same house"), "hasta": T("found that same house") + 5},
    {"tipo": "lista", "titulo": "His notes", "lineas": ["People who look identical", "Neighbors who can't get into their homes", "People glitching through walls", "Locked doors with nothing behind them"],
     "desde": T("His notes list the clues"), "hasta": T("Nobody knows if Rockstar planned")},
    {"tipo": "pastilla", "texto": "KELLY COUNTY · AT NIGHT (CHAPTER 2+)", "fondo": "amarillo", "desde": T("Head to Kelly County"), "hasta": T("Head to Kelly County") + 6},
    {"tipo": "lista", "titulo": "Trophy unlocked", "lineas": ["\"The Truth Is Out There\"", "Hidden trophy"],
     "desde": T("Your reward is a hidden trophy"), "hasta": T("GTA 5 had its Mount Chiliad")},
]
plan = {"voz": "voz.mp3", "palabras": "palabras.json", "salida": "VCDT_L01_18_Secrets.mp4", "duracion": round(fin, 2), "bpm": 98, "musica": 0.09,
        "escenas": escenas, "secretos": secretos,
        "capitulos": [{"num": i + 1, "titulo": c, "desde": round(ini_cap[i], 3)} for i, c in enumerate(CAPITULOS)],
        "tarjetas": tarjetas}
(B / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False))
print(f"{len(escenas)} escenas, {fin / 60:.1f} min; imágenes distintas {len(usados)}")
cap = "\n".join(f"{int(x // 60)}:{int(x % 60):02d} {t}" for x, t in [(0, "Intro")] + [(ini_cap[i], f"Part {i + 1}: {c}") for i, c in enumerate(CAPITULOS)] + [(fin_ultimo, "Final")])
(B / "capitulos.txt").write_text(cap + "\n")
print(cap)
