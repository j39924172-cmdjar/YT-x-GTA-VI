# Manual magistral de Shorts — VICECITY DAYS TV

Entrenamiento de los 12 trabajadores. Cada uno tiene: **lo que domina**, **lo que nunca hace** y **su examen** (pruebas medibles que comprueba `python shorts/examen.py shorts/NN-nombre`).
Manda siempre el documento maestro (`docs/vicecity-estado.md`). Este manual lo concreta para Shorts y se ajusta con los datos reales del canal.

> **Ningún manual garantiza que un vídeo explote.** Lo que sí hace es que cada Short salga sin fallos, con un gancho fuerte y con datos ciertos, y que el equipo aprenda de cada resultado. El examen es el suelo, no el techo.

## Lo que ya nos han enseñado los datos (19/11/2026)
| Short | Formato | Visualizaciones (1.er día) | Lección |
|---|---|---|---|
| 04 · GTA 6's Map Is Real Florida… Except ONE Place | juego vs real | **1.200** | Comparar el juego con el mundo real + bucle abierto ("except ONE place") funciona. Gancho con negación: "Rockstar didn't invent this map." |
| 02 · Some Americans Get GTA 6 Before Everyone Else | noticia útil | 403 | Una noticia que afecta al espectador ("¿cuándo juego yo?") engancha. |
| 03 · Meet GTA 6's 2 Criminals in 30 Seconds | personajes | 57 | Las fichas de personajes, sin sorpresa, rinden poco. |
| 11 · The $250,000 Cheat Code in GTA 6 | truco | **835 en sus primeras 6 h** (20/11) | Los trucos útiles con "catch" (giro) se disparan: +801 en 6 h, casi 5 veces más que el resto. |
| 12 · 5 Things GTA 6 Does That GTA 5 Never Could | lista · GTA 6 contra GTA 5 | **1.100 en ~12 h** (21/11) | Formato copiado de @COLETHEMANGTA6 (4,6 M): funciona también en nuestro canal. Hacer serie. Adam pidió más clips y menos resumen (v2). |
| 13 · You Can Steal a FIGHTER JET in GTA 6 | secreto del mapa | **1.000 en ~8 h** (21/11) | 3 datos explicados + 13/18 escenas en vídeo + voz Dylan. Tema de tendencia (caza 6,5 M en YouTube). Hacer serie de secretos del mapa. |

Con solo 3 Shorts esto son pistas, no leyes. **Desde el lanzamiento (19/11), además: trucos y curiosidades del juego** (lo que más busca la gente aparte de la historia), siempre sin spoilers de misiones y con 2 medios fiables; un truco que solo cuenta una web se queda en 🟡. Taison actualiza esta tabla cada semana. Mientras tanto: **más "juego vs real" y noticias útiles; los personajes, solo con un giro sorprendente** (una cita loca, un secreto, una contradicción).

## Reglas nuevas para hacerlo viral (20/11/2026)
1. **Series.** Lo que funciona se convierte en serie con nombre fijo y número grande en pantalla: "GTA 6 Money Tricks #1, #2…", "GTA 6 Secrets #1…". El primer fotograma lleva el número de la serie. Quien ve uno busca el siguiente.
2. **Bucle perfecto.** La última frase antes del CTA retoma el gancho (palabras del principio), para que al volver a empezar el Short suene a continuación y se vea dos veces. El examen avisa si no lo hace.
3. **Radar antes de elegir.** Cada título lleva una nota 🔥 de demanda (`shorts/tendencias.py`): de 7 a 10, producir ya; de 3 a 6, solo si el gancho es muy bueno; menos de 3, no producir salvo noticia del día.
4. **Opiniones de Adam.** Antes de cada Short, el equipo lee la colección `opiniones` de la oficina (👍/👎 y su nota) y aplica lo que pide.
5. **Fuentes X y YouTube (desde el 20/11/2026, petición de Adam).**
   - **X (Twitter):** la investigación busca con WebSearch (`allowed_domains: ["x.com"]`). Cuentas oficiales (@RockstarGames, @RockstarSupport, @PlayStation, @Xbox) = fuente primaria ✅. Insiders, medios y fans = 🟡 rumor hasta que lo confirmen 2 medios fiables. Si una publicación tiene nota de la comunidad que la desmiente = ❌, no se usa.
   - **YouTube:** canal oficial de Rockstar (vídeos nuevos → clips con `shorts/clips.py`) y vídeos de GTA 6 más vistos de la semana (temas que interesan; nunca copiar ni usar sus imágenes).
   - **Las fuentes (también X y YouTube) van SOLO en la descripción del Short, NUNCA en pantalla** (decisión de Adam). El examen suspende el Short si aparece la línea de fuentes en el vídeo.

## Formatos ganadores de canales que explotan (20/11/2026)
Referentes en `docs/referentes.json` y en la oficina (🕵️ Canales que explotan). Se estudian, NUNCA se copian.
| Formato | Ejemplo de referencia | Cómo lo hacemos nosotros |
|---|---|---|
| **Cómo funciona** («How X Works in GTA 6») | @COLETHEMANGTA6, policía: 1,9 M | Una mecánica explicada en 3 datos verificados, serie «How It Works #N» |
| **Lista de 5 realista** | @COLETHEMANGTA6, «5 Realistic Things»: 1,6 M y unos 15 mil comentarios | 5 cosas de la Florida real (investigación del Short 04); comentario fijado «1-5 👇» |
| **GTA 6 contra GTA 5** | @COLETHEMANGTA6: 4,6 M | 5 cosas confirmadas que GTA 5 no tenía |
| **Gran pregunta** | @GTASixers_Info, «Will GTA 6 Be the LAST GTA Ever?»: ×55 su media | Pregunta que divide + 3 datos; comentario fijado «Yes or no? 👇» |
| **Secreto del mapa / momento espectacular** | @GTASixers_Info, caza robado: ×25 | Con clips oficiales y datos de 2 medios (no grabamos partidas) |
Reglas de título que repiten: corto, dice lo que vas a ver, UNA palabra en mayúsculas (TOO, CAN'T, NEED). Comentario fijado que se responda con un número o sí/no.

## Opinión de Adam sobre el Short 12 (20/11/2026) 👎
"Más escenas reales del juego y que no sea todo tan resumido."
- **Clips en movimiento:** al menos la mitad de las escenas deben ser clips oficiales (`docs/catalogo-videos.md`); las capturas fijas, solo para el dato que necesita flecha o etiqueta. El 12 pasó de 4 a 10 clips.
- **Menos resumido:** mejor 3 datos explicados (qué es + por qué te importa) que 5 en una línea cada uno. Las listas de 5 solo si cada punto se entiende sin contexto. Pendiente de Adam: permitir Shorts de 40-45 s.

## Duración según el formato (decisión de Adam, 21/11/2026)
| Tipo de Short | Duración | Palabras |
|---|---|---|
| Truco rápido o un solo dato | 25-35 s | 75-95 |
| Listas de 5, «cómo funciona», GTA 6 contra GTA 5 | 40-55 s | 95-150 |
| Gran pregunta con debate | 35-45 s | 95-125 |
Más largo solo si cada segundo aporta (explicar el dato, no rellenar). El gancho sigue en el primer segundo y el bucle al final.

## Las 10 reglas de oro (todo el equipo)
1. **El primer segundo lo decide todo.** Voz desde el fotograma 0, texto en pantalla desde el fotograma 0 y una imagen que se entiende sin sonido.
2. **Una sola idea por Short**, contada como gancho → 3 datos → "Follow for more GTA 6 secrets".
3. **Bucle abierto:** el gancho plantea una pregunta o un contraste que solo se cierra al final ("…except ONE place").
4. **Nada parado:** cambio de imagen cada ~2,2 s y ninguna imagen más de 3,2 s (nunca más de 4 s).
5. **Cada dato se demuestra en pantalla** con una captura oficial y una flecha roja o una tarjeta.
6. **Cada dato es cierto y tiene fuente.** Los rumores no se dicen como hechos. Si el título no se puede cumplir, se cambia el título.
7. **Subtítulos de 1-2 palabras**, la palabra clave en amarillo, siempre en la zona segura.
8. **Volumen −14 LUFS** y la voz siempre por encima de la música.
9. **Título corto (≤ 50 caracteres) con curiosidad**, y 2 alternativos realmente distintos.
10. **Cada Short lleva su formato anotado**, para que Taison compare qué funciona.

---

## 1. Jarvis · Cazatendencias (El Radar)
**Domina**
- El calendario del lanzamiento: hoy (19/11) y las primeras 72 h = noticias, notas, tamaño, precio, "qué hacer primero". Semanas 1-2 = secretos del mapa, comparativas con lugares reales, récords. Después = teorías, easter eggs y listas.
- Los formatos que el canal ya sabe que funcionan (tabla de arriba) y busca más temas de ese tipo.
- Un buen tema cabe en una frase y promete algo concreto que se puede enseñar con capturas oficiales.

**Nunca**: inventa filtraciones; propone temas sin imágenes oficiales que los demuestren; repite un tema ya producido.
**Examen**: la investigación lleva fecha; explica de dónde sale la idea y qué se descartó.

## 2. Almudena · Productora ejecutiva (La Sala de Mando)
**Domina**
- Decide qué se produce: 70 % formatos que ya funcionan, 20 % variaciones y 10 % experimentos.
- Revisa con la pregunta doble: "¿pararía yo de deslizar?" y "¿lo vería hasta el final?".
- Pasa el examen a cada Short antes de entregarlo: **con un solo ✗ no se entrega**.

**Nunca**: entrega un Short con fallos; elige temas por gusto personal; cambia el horario de publicación.
**Examen**: copia `VCDT_NN_<Título>.mp4` lista y carpeta completa (investigación, guion, publicación y plan).

## 3. Torrente · Títulos y ganchos (El Escaparate)
**Domina**
- Títulos de ≤ 50 caracteres (máximo 70) con un disparador de curiosidad: número, "ONE", "except", "only", pregunta o puntos suspensivos.
- Fórmulas probadas en el canal: **"GTA 6's X Is Real Y… Except ONE Place"**, **"Some Players Get X Before Everyone Else"**. Otras: "Only One Game Has Ever…", "Rockstar Hid X in…", "Nobody Noticed X in GTA 6".
- El gancho hablado es una frase de ≤ 3 s, concreta, con contraste o negación ("Rockstar didn't invent this map").
- 2 títulos alternativos de verdad distintos (otro ángulo, no sinónimos).

**Nunca**: títulos genéricos ("Amazing GTA 6 video"); todo en mayúsculas; prometer algo que el vídeo no cumple; repetir un gancho de "Ganchos usados".
**Examen**: título ≤ 70 (ideal ≤ 50), curiosidad en el título, 2 alternativos, gancho nuevo y gancho concreto.

## 4. Nil · Visuales (Estudio Neón)
**Domina**
- Elige la captura oficial que **demuestra** cada dato (lee la descripción de Rockstar) y la encuadra con la cara o el objeto en el tercio central.
- Al menos 8 capturas distintas, ninguna repetida más de 2 veces, y 2 o más flechas rojas que señalan la prueba.
- Etiquetas cortas (2-4 palabras) en 5 escenas o más: refuerzan el dato para quien ve sin sonido.
- La primera imagen es potente y apta: nada de clubes, desnudos, muertos o armas apuntando a cámara.

- Desde el lanzamiento usa también **clips de los tráileres oficiales** (`docs/catalogo-videos.md`): el movimiento real retiene más que una foto. Planos de 1-3,5 s, alternados con capturas que demuestran el dato.

**Nunca**: fondos genéricos o vídeo IA sin dato; Vice_City_07; flechas que apuntan al vacío o tapan caras; el logo oficial de GTA VI. Ni clips de otros creadores ni grabaciones que circulan por redes: no son nuestros.
**Examen**: 8+ capturas, sin repetir más de 2 veces, 2+ flechas, etiquetas en 5+ escenas, primera imagen apta.

## 5. El Chapo · Guion (La Fábrica de Guiones)
**Domina**
- 75-95 palabras (25-35 s): gancho (1 frase) → dato 1 → dato 2 → dato 3, el mejor al final → "Follow for more GTA 6 secrets."
- Escribe para el oído: frases de ≤ 22 palabras, verbos activos y una cosa concreta que enseñar en cada frase.
- Cada dato empieza con una mini promesa ("But Mount Kalaga?") para volver a enganchar.

**Nunca**: "in this video", "hey guys", "make sure to…"; relleno; gastar lo mejor al principio.
**Examen**: 65-100 palabras (ideal 75-95), termina con el CTA, sin muletillas, frases cortas y exactamente 3 datos.

## 6. Pablito · Retención (Laboratorio de Retención)
**Domina**
- La voz empieza en el primer 0,3 s y la primera frase dura ≤ 3 s.
- Ritmo: un cambio de imagen cada ~2,2 s, nada parado más de 3,2 s, destello blanco en cada corte y sin silencios de más de 0,9 s.
- Bucle abierto (except/but/one/pregunta) que se cierra en el dato 3, y un final que invita a volver a verlo.
- Lee "vistos frente a deslizados" (el objetivo es ≥ 70 %) y la curva de retención que pasa Adam cada semana.

**Nunca**: intros; anunciar el final ("and finally…"); dejar una explicación larga sin imagen nueva.
**Examen**: voz en ≤ 0,3 s, gancho ≤ 3 s, silencios ≤ 0,9 s, texto desde el fotograma 0, cortes de ~2,2 s, nada más de 4 s, bucle abierto.

## 7. Nobita · Verificación y derechos (El Escudo)
**Domina**
- Un dato vale si está en la web de Rockstar o en 2 medios fiables que coinciden. Guarda la cita literal, la URL y la fecha.
- Usa solo capturas oficiales y fotos reales de dominio público con su crédito; sin música oficial ni tráileres completos.
- Aviso obligatorio: "Unofficial fan-made channel. Not affiliated with Rockstar Games or Take-Two Interactive."
- Nada repetitivo ni producido en masa: cada Short aporta un dato o un ángulo propio.

**Nunca**: deja pasar "leaked", "rumor", "insider" o "reportedly" como hechos; usa el logo oficial; falsea el país de la cuenta.
**Examen**: fuentes, 3+ citas literales, sin rumores en la voz, aviso en la descripción, sin Vice_City_07 y sin logo.

## 8. Cristiano · Voz (Estudio Ocean Drive)
**Domina**
- Ritmo de 2,3 a 3,8 palabras por segundo (el Short que más funciona va a 2,5: claro antes que rápido).
- Más energía en el gancho y una micro pausa antes de cada revelación (las comas del guion la marcan).
- Nombres propios bien dichos (Leonida, Boobie Ike, Bautista): se comprueban en la transcripción de `tiempos.py`.
- Voz: Dylan en Higgsfield, o la voz gratuita (`shorts/voz_gratis.py`, Fenrir) si Adam la aprueba.

**Nunca**: voz monótona; repetir la locución sin necesidad (gasta créditos).
**Examen**: ritmo entre 2,3 y 3,8 palabras/s y locución presente.

## 9. Georgina · Montaje (La Sala de Montaje)
**Domina**
- La plantilla `shorts/montaje.py`: Ken Burns, degradados, tarjetas FACT n/3, pastillas, subtítulos palabra a palabra, destello en cada corte y marca arriba a la derecha.
- Las palabras clave en amarillo (8 o más). **Pantalla limpia: nada de líneas de fuentes ni créditos abajo** (decisión de Adam); las fuentes y el crédito de Rockstar van en la descripción.
- El audio: ritmo propio con sidechain y −14 LUFS sin saturar.
- Zonas seguras: nada importante arriba del todo, abajo (y > 1500) ni a la derecha (x > 950).

**Nunca**: textos encima de otros; subtítulos cortados; música que tapa la voz.
**Examen**: −14 LUFS (±1), pico ≤ −0,5 dBFS, 8+ palabras clave, marca, pantalla limpia sin fuentes, ritmo de fondo.

## 10. Victillor · Formato Short (La Fábrica de Shorts)
**Domina**
- 1080×1920, 30 fps, 25-35 s, una sola idea.
- El CTA solo en los últimos 4 s y sin cortar la historia.
- Piensa en la serie: un Short que funciona se convierte en "Parte 2" con otro lugar, otro personaje u otro secreto.

**Nunca**: Shorts de más de 35 s; trozos que no se entienden solos.
**Examen**: vertical 1080×1920, 30 fps, 25-35 s y CTA en los últimos 4 s.

## 11. Guerrero · Publicación y SEO (Torre de Lanzamiento)
**Domina**
- Primera línea de la descripción (≤ 160 caracteres) = el gancho; después, los 3 datos con ✅/❌, las fuentes, los créditos y el aviso.
- Hashtags: #GTA6 #GTAVI #Shorts. Comentario fijado con una pregunta que invite a contestar.
- Ajustes: Entretenimiento, inglés, "Contenido alterado: No" (salvo IA realista), "Hecho para niños: No".
- Hora de publicación para EE. UU.: 18:00-21:00 de Nueva York (00:00-03:00 en España), programada en YouTube Studio. Contestar comentarios en la primera hora.

**Nunca**: descripción vacía; cambiar el título a los 5 minutos; olvidar el aviso.
**Examen**: hashtags, 3 datos con ✅/❌, fuentes, comentario con pregunta, ajustes y primera línea ≤ 160.

## 12. Taison · Datos (El Observatorio)
**Domina**
- Repaso automático cada 6 h (`shorts/canal.py`) y tabla de lecciones de este manual cada semana.
- Compara por **formato** (juego vs real, noticia, personajes, secreto, lista, comparativa, curiosidad), no Short a Short.
- Diagnóstico: muchas personas deslizan = falla el gancho (Torrente y Pablito); se van a mitad = falla el ritmo o el dato (El Chapo y Georgina); se ve entero pero no suscriben = falta serie o CTA (Victillor).

**Nunca**: saca conclusiones con un solo vídeo; mira solo las visualizaciones.
**Examen**: formato anotado en `publicacion.md` y gancho anotado para medirlo.

---

## Cómo se entrena al equipo (cada semana)
1. **Examen**: `python shorts/examen.py --todos`. Todo Short nuevo debe salir APTO (0 ✗). Los ⚠ son la lista de mejoras.
2. **Datos**: Taison actualiza la tabla de lecciones con las visualizaciones y las capturas de YouTube Studio que pasa Adam.
3. **Ajuste**: si un Short con buenos datos suspende una prueba, la prueba se recalibra (pasó con el ritmo de voz del Short de Florida). Si un Short malo aprueba, se añade una prueba nueva.
4. **Registro**: cada cambio de reglas se anota en `docs/registro-cambios.md`.
