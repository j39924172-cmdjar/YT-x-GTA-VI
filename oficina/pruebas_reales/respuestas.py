import json
guion = json.load(open("guion.json"))
R = {}
R["trends"] = {"resumen": "A días del lanzamiento, lo que más se busca es saber qué hacer primero y qué hay en el mapa; las noticias concretas hay que verificarlas.",
 "temas": [
  {"tema": "Qué hacer en las primeras horas de GTA 6", "por_que": "Todo el mundo va a empezar a la vez y busca una guía de inicio.", "fiabilidad": "evergreen", "potencial": 10},
  {"tema": "Las zonas del mapa de Leonida explicadas", "por_que": "Rockstar ha mostrado seis zonas y la gente quiere saber qué hay en cada una.", "fiabilidad": "evergreen", "potencial": 9},
  {"tema": "Secretos y easter eggs de los tráileres", "por_que": "Las listas de secretos retienen hasta el final y se comparten mucho.", "fiabilidad": "evergreen", "potencial": 9},
  {"tema": "Cómo ganar dinero rápido al empezar", "por_que": "Es la pregunta número uno en cada GTA durante las primeras semanas.", "fiabilidad": "evergreen", "potencial": 8},
  {"tema": "Coches más rápidos y dónde encontrarlos", "por_que": "Tema muy visual y fácil de enseñar con gameplay propio.", "fiabilidad": "evergreen", "potencial": 8},
  {"tema": "Lucia y Jason: lo que sabemos de su historia", "por_que": "Los protagonistas generan teorías y debate en comentarios.", "fiabilidad": "probable", "potencial": 7},
  {"tema": "GTA 6 frente a GTA 5: lo que cambia", "por_que": "Comparativa clásica que atrae a jugadores veteranos.", "fiabilidad": "evergreen", "potencial": 7},
  {"tema": "Cómo rinde en cada consola", "por_que": "Mucha gente decide cómo jugar según estos datos.", "fiabilidad": "verificar", "potencial": 6},
  {"tema": "GTA 6 Online: qué se sabe", "por_que": "Interés enorme, pero casi todo son rumores hasta que Rockstar lo confirme.", "fiabilidad": "verificar", "potencial": 6},
  {"tema": "Precio y ediciones del juego", "por_que": "Búsqueda puntual alrededor del lanzamiento.", "fiabilidad": "verificar", "potencial": 5}]}
R["plan"] = {"tema": "Las 6 zonas de Leonida y qué explorar primero",
 "angulo": "Guía para el primer día: qué hay en cada zona y en qué orden explorarlas, separando lo confirmado por Rockstar de lo que es suposición.",
 "promesa": "Sabrás qué hay en cada una de las 6 zonas de Leonida y qué explorar primero para no perderte nada.",
 "publico": "Jugadores que van a empezar GTA 6 en los primeros días y no quieren perderse nada",
 "shorts_previstos": ["La zona que casi nadie está mirando", "Vice City cambia por completo de noche", "Muévete por los Cayos en barco", "La zona con más pinta de esconder la historia"],
 "dia_hora": "Viernes a las 18:00 en España (11:00 en México, 13:00 en Argentina)",
 "razon": "Es el tema evergreen con más búsquedas justo al empezar y abre una serie: una zona por vídeo."}
R["titles"] = {"promesa": "Qué hay en cada zona de Leonida y por dónde empezar",
 "titulos": [
  {"titulo": "GTA 6: las 6 zonas de Leonida que tienes que conocer", "por_que": "Número + claridad: funciona en búsquedas."},
  {"titulo": "GTA 6: qué explorar primero en Leonida (guía del día 1)", "por_que": "Beneficio inmediato para quien va a empezar."},
  {"titulo": "GTA 6: la zona del mapa que casi nadie está mirando", "por_que": "Curiosidad concreta que cumple el final del vídeo."}]}
R["thumbs"] = {"miniaturas": [
  {"texto": "6 MUNDOS", "composicion": "Mapa de Leonida partido en seis zonas de colores saturados, texto enorme arriba a la izquierda", "prompt_imagen": "Bold stylized map of an original tropical state divided into six saturated neon regions, high contrast, no text", "color": "#FFE14D"},
  {"texto": "EMPIEZA AQUÍ", "composicion": "Mapa oscuro con una flecha rosa gigante señalando una zona iluminada; texto a la izquierda", "prompt_imagen": "Dark map with a single glowing coastal region and a huge pink arrow pointing at it, cinematic lighting, no text", "color": "#FF4FA3"},
  {"texto": "NADIE MIRA AQUÍ", "composicion": "Montaña con bosque al amanecer y un círculo rojo sobre un punto escondido entre los árboles", "prompt_imagen": "Sunrise over a forested mountain with mist, a small mysterious structure hidden among trees, high contrast, no text", "color": "#33E1D6"}]}
R["script"] = guion
new2 = "El mapa en diez segundos: Leonida es el estado ficticio de GTA 6, inspirado en Florida, con Lucia y Jason como protagonistas. Seis zonas: Vice City, los Cayos, Grassrivers, Port Gellhorn, Ambrosia y el Monte Kalaga. Y cada una cambia cómo juegas: vehículos, negocios y hasta la radio. Te las enseño de la que más vas a visitar a la que más te puede sorprender. Y atento a la cuarta, porque tiene una pista sobre la historia que casi nadie ha visto."
new7 = "Zona cinco, y aquí cambia todo: Ambrosia. Se acabaron la playa y el neón. Es el interior industrial y agrícola, con fábricas, campos y carreteras larguísimas. Según la web oficial, aquí manda la industria: más camiones, más trabajadores y casi ningún turista. ¿Y eso qué significa para ti? Persecuciones largas por carretera y negocios que no tienen nada que ver con la playa. Recórrela de día y mira cada nave y cada granja: los detalles del interior son los que más tarda la comunidad en encontrar. Quien sabe dónde mirar, los encuentra antes que nadie."
R["retention"] = {"nota": 7,
 "gancho_mejorado": "Leonida no es un mapa: son seis mundos distintos, y la última zona es la que casi nadie está mirando.",
 "cambios": [
  {"escena": 2, "problema": "Promete “el contexto en diez segundos” y dura unos 50: aquí se pierde gente.", "nuevo_texto": new2},
  {"escena": 7, "problema": "Ambrosia llega en mitad del vídeo sin nada nuevo que enganche; la sexta zona queda lejos.", "nuevo_texto": new7}],
 "consejo_montaje": "Cambia de plano en cada frase durante el primer minuto y pon el número de zona grande al empezar cada bloque."}
R["compliance"] = {"aprobado": True, "declarar_ia": True, "avisos": [
  {"nivel": "mejora", "tema": "Veracidad", "detalle": "Las descripciones de Ambrosia y Kalaga dependen de la web oficial; si algo cambia en el juego final, hay que corregirlo.", "arreglo": "Revisa esas dos zonas jugando antes de publicar o añade “según la web oficial” en pantalla."},
  {"nivel": "mejora", "tema": "Contenido con IA", "detalle": "Si se usan los clips generados con IA de los prompts, son realistas.", "arreglo": "Marca “Contenido alterado o sintético: Sí” al subir el vídeo."}]}
R["shorts"] = {"shorts": [
  {"titulo": "La zona de GTA 6 que nadie está mirando", "gancho": "Todo el mundo habla de Vice City, y se está olvidando de esto.",
   "narracion": "Todo el mundo habla de Vice City, y se está olvidando de esto. En el mapa de GTA 6 hay una zona que apenas sale en los tráileres, con bosques, montaña y ríos. Rockstar le ha dado nombre de parque nacional, y eso no se hace por casualidad. Si quieres saber cuál es y por qué creo que esconde más secretos que ninguna otra, te lo cuento con todo detalle en el vídeo completo del canal.",
   "textos_pantalla": ["NADIE MIRA AQUÍ", "NOMBRE DE PARQUE NACIONAL"], "cierre": "La zona y sus secretos, en el vídeo completo."},
  {"titulo": "Vice City cambia por completo de noche", "gancho": "Esta calle de día parece tranquila. Ahora mírala de noche.",
   "narracion": "Esta calle de día parece tranquila. Ahora mírala de noche. En los tráileres de GTA 6, Vice City se transforma cuando se pone el sol: neón, discotecas y fiestas que dan pistas de actividades. Mi consejo para tus primeras horas es que recorras la ciudad dos veces, una de día y otra de noche, porque no parecen el mismo sitio. En el vídeo completo te enseño qué buscar en las otras cinco zonas del mapa.",
   "textos_pantalla": ["DE DÍA", "DE NOCHE"], "cierre": "Las otras 5 zonas, en el vídeo completo."},
  {"titulo": "En GTA 6 consigue un barco cuanto antes", "gancho": "En esta zona de GTA 6 el coche no te va a servir.",
   "narracion": "En esta zona de GTA 6 el coche no te va a servir. Los Cayos de Leonida son una cadena de islas con puentes larguísimos y aguas turquesas, y aquí el protagonista es el agua. En otros juegos de Rockstar los mejores escondites estaban en sitios a los que solo se llega navegando; en GTA 6 está por confirmar, pero yo no me la jugaría. Tienes mi plan de inicio completo en el vídeo largo del canal.",
   "textos_pantalla": ["CONSIGUE UN BARCO", "POR CONFIRMAR"], "cierre": "Mi plan de inicio, en el vídeo completo."},
  {"titulo": "La zona de GTA 6 con más pinta de historia", "gancho": "Esta es la zona menos bonita de GTA 6, y puede que la más importante.",
   "narracion": "Esta es la zona menos bonita de GTA 6, y puede que la más importante. Port Gellhorn es un puerto olvidado: moteles, carteles viejos y calles vacías. Aun así, aparece una y otra vez en el material oficial. Y cuando Rockstar enseña tanto un sitio tan poco glamuroso, suele ser porque pesa en la historia. Es una teoría mía, no un dato confirmado, y te explico por qué en el vídeo completo.",
   "textos_pantalla": ["LA MENOS BONITA", "TEORÍA"], "cierre": "La teoría completa, en el vídeo completo."}]}
# capítulos con los tiempos reales del guion final (2,5 palabras por segundo)
esc = [dict(e) for e in guion["escenas"]]
esc[1]["narracion"] = new2; esc[6]["narracion"] = new7
t = 0; caps = []
nombres = ["Seis mundos", "El mapa en 10 segundos", "Vice City", "Cayos de Leonida", "Grassrivers", "Port Gellhorn", "Ambrosia", "Monte Kalaga", "Tu plan para empezar", "¿Cuál exploras primero?"]
for i, e in enumerate(esc):
    caps.append({"tiempo": f"{int(t)//60}:{int(t)%60:02d}", "titulo": nombres[i]}); t += len(e["narracion"].split()) / 2.5
R["launch"] = {"descripcion": "GTA 6: las 6 zonas de Leonida explicadas y qué explorar primero el día 1.\nVice City, los Cayos, Grassrivers, Port Gellhorn, Ambrosia y el Monte Kalaga: lo confirmado por Rockstar y lo que es suposición, separado.\nSerie “Leonida zona por zona”: suscríbete para no perderte ninguna.\nContenido no oficial hecho por fans. GTA VI es una marca de Rockstar Games.",
 "etiquetas": ["gta 6", "gta vi", "gta 6 mapa", "gta 6 leonida", "leonida", "vice city", "gta 6 vice city", "cayos de leonida", "grassrivers", "port gellhorn", "ambrosia gta 6", "monte kalaga", "gta 6 guia", "gta 6 que hacer primero", "gta seis", "gta 6 español"],
 "hashtags": ["#GTA6", "#GTAVI", "#Leonida", "#ViceCity"],
 "capitulos": caps,
 "comentario_fijado": "¿Cuál de las 6 zonas vas a explorar primero? La más votada tendrá su propio vídeo 👇",
 "dia_hora": "Viernes a las 18:00 en España (11:00 en México, 13:00 en Argentina)",
 "pantalla_final": "Siguiente vídeo de la serie: todo lo que se sabe de Lucia y Jason",
 "lista": "GTA 6: Leonida zona por zona"}
R["greenlight"] = {"notas": {"clic": 8, "retencion": 8, "shorts": 8, "publicacion": 9}, "luz_verde": True, "rehacer_desde": "",
 "motivo": "Promesa clara y útil justo al empezar el juego, título y miniatura alineados, y Pablito ha arreglado el bache del minuto 1.",
 "titulo_final": "GTA 6: qué explorar primero en Leonida (guía del día 1)", "miniatura_final": "B",
 "consejo": "Fija el comentario de la zona favorita y contesta todo lo que puedas en la primera hora: esas respuestas deciden el siguiente vídeo."}
json.dump(R, open("respuestas.json", "w"), ensure_ascii=False, indent=1)
print("capítulos:", [(c["tiempo"], c["titulo"]) for c in caps])
print("palabras por short:", [len(s["narracion"].split()) for s in R["shorts"]["shorts"]])
