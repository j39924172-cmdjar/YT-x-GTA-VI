# Procedimiento: producir un Short a partir de un título

Lo sigue la sesión que se lanza desde la oficina (tarea programada **"Producir Short"**). Recibe el título que escribe Antonio y entrega el vídeo listo para subir.
Cumple siempre `docs/vicecity-estado.md` (fuente de verdad) y `CLAUDE.md`. Cada trabajador sigue su parte del **manual magistral** `docs/manual-shorts.md`, y el Short solo se entrega si aprueba el examen (`shorts/examen.py`).

**Cómo llega el encargo.** En la oficina (https://claude.ai/artifact/WdZBBpgqbXUEDL1Wk3kFRC), Adam elige título y voz y pulsa "Producir Short"; la página envía un comentario "Send to Claude" con el texto `Producir Short — TÍTULO: … / Voz: … / Encargo: <id>`. Ese comentario despierta a la sesión de producción (la que vigila la oficina). También puede llegar pegado en el chat.

**Progreso en la oficina.** Si el encargo trae `<id>`, al empezar cada paso actualiza el documento `encargos/<id>` con ArtifactData (`url` de la oficina, `collection` "encargos", `action` "update" con `if_version`): `{"estado": "en marcha", "paso": n}`. Al terminar: `{"estado": "entregado", "paso": 8, "nota": "<título final o cambio>"}`; si hay que parar (sin saldo, datos imposibles): `{"estado": "error", "nota": "<motivo corto>"}`. La oficina lo muestra al momento. Escribe también en el chat una línea que empiece por `[PASO n/8]`.
**Registro de actividad.** Al terminar cada paso, añade una entrada a la colección `actividad` de la oficina (ArtifactData `set`, doc_id `aAAAAMMDD-HHMM-n`, sin if_version porque es nueva): `{"ts": <ms>, "quien": ["<ids>"], "texto": "<qué hizo, en pasado y en español, ≤ 90 caracteres>"}`. Los ids son: jarvis, nobita, chapo, torrente, pablito, victillor, nil, cristiano, georgina, guerrero, almudena, taison. La oficina lo enseña en "Actividad" y en la ficha de cada persona.
**Notas del examen.** Tras el paso 6, ejecuta `python shorts/examen.py --todos --oficina /tmp/estado_equipo.json` y guarda ese archivo en el documento `estado/equipo` (get + set con if_version). La oficina lo usa para "Listos para subir" y para la nota de cada persona.
Al recibir el encargo, contesta en el hilo del comentario (ArtifactComments `reply`) diciendo que el equipo ha empezado; al terminar, contesta con el título final y márcalo resuelto.

**Si el título ya está preproducido** (carpeta en `shorts/` con "Estado: preproducción"), usa esa carpeta: repasa rápido que los datos sigan vigentes y salta al paso 4 (voz).

## [PASO 1/8] Investigación y verificación (Jarvis + Nobita)
1. Prepara el repositorio `j39924172-cmdjar/YT-x-GTA-VI` en la rama `claude/youtube-gta6-automation-team-aua7ki`. Si no está en la sesión, añádelo con `add_repo` y clónalo. Luego `git pull`.
2. Instala las dependencias si faltan: `pip install -r shorts/requirements.txt` (ffmpeg debe existir).
3. Busca el título en `docs/banco-ideas.md`: si ya está, parte de sus datos y fuentes.
4. Verifica 3 datos que cumplan la promesa del título:
   - Primero la fuente primaria: web de Rockstar (`curl` a https://www.rockstargames.com/VI, `/VI/only-in-leonida`, `/VI/launch-gallery`, `/VI/media`, https://www.rockstargames.com/newswire). El texto está en los bloques `self.__next_f.push`; `python shorts/herramientas.py textos-rockstar` los extrae.
   - Después, medios fiables con WebSearch (IGN, GameSpot, Eurogamer, VGC, Polygon, Forbes, PC Gamer).
   - Un dato vale si está en la fuente primaria o en 2 medios fiables que coinciden. Los rumores no se usan como hechos.
5. **Si el título promete algo que no se puede verificar** (o es falso), ajusta el título a lo que sí es cierto (como "…except ONE place") y explica el cambio en la entrega. Nunca inventes.
6. Crea `shorts/NN-<nombre>/investigacion.md` con las citas literales, las URL, la fecha y lo descartado. NN es el siguiente número libre en `shorts/`.

## [PASO 2/8] Guion y gancho (El Chapo + Torrente + Pablito)
- Inglés, **25–35 s** (unas 75–95 palabras): gancho → 3 datos → "Follow for more GTA 6 secrets".
- Gancho concreto en el primer segundo, NUEVO: comprueba "Ganchos usados" en `docs/banco-ideas.md`. Primera frase de 3 s o menos, con contraste, negación, número o pregunta, y un bucle abierto que se cierre en el dato 3.
- Da prioridad a los formatos que mejor funcionan en el canal (tabla de lecciones de `docs/manual-shorts.md`).
- Frases cortas para leer en voz alta. Nada de "in this video".
- Guarda `guion.md` (gancho, voz, textos de pantalla y visual por bloque) y `voz.txt` (solo el texto de la voz, en una línea).

## [PASO 3/8] Visuales (Nil)
- Elige en `docs/catalogo-imagenes.md` las capturas oficiales que DEMUESTRAN cada dato (lee la descripción de Rockstar).
- **Clips de vídeo oficiales** (desde el 19/11): `docs/catalogo-videos.md` lista los planos de los tráileres que Rockstar publica para descargar (Launch Trailer, Pre-Load). Si no están en `videos/oficiales/`, `python shorts/clips.py descargar`. En `plan.json` una escena puede ser `{"video": "../../videos/oficiales/GTAVI_Launch_Trailer.mp4", "inicio": 47.1, "desde": …, "hasta": …, "foco": [x, y]}`. Reglas: planos de 1-3,5 s que no pasen del final de su plano, nunca los marcados ❌ (logo oficial, club, arma a cámara, muy oscuros), ni cinemáticas enteras ni spoilers; con vídeo, la fuente es "Footage: Rockstar Games". Lo ideal: mezclar clips (movimiento) con capturas (datos con flecha).
- Descárgalas: `python shorts/herramientas.py descargar shorts/NN-x Grupo_NN Grupo_NN …`.
- Haz una hoja de contacto (`python shorts/herramientas.py hoja shorts/NN-x/capturas`) y mírala con Read para decidir encuadres (foco x, y entre 0 y 1) y a qué apuntan las flechas rojas.
- Evita los clubes, los desnudos, las armas apuntando a cámara y los animales muertos en el primer segundo. Nada de fondos genéricos ni vídeo IA sin dato.

## [PASO 4/8] Voz (Cristiano)
**Qué voz:** la que diga el encargo (`Voz: Fenrir (gratis)` o `Voz: Dylan (Higgsfield)`; Adam la elige en la oficina). Si no dice nada, Fenrir.
- **Fenrir (gratis):** `python shorts/voz_gratis.py shorts/NN-x/voz.txt shorts/NN-x/voz.mp3 am_fenrir 29` y salta al punto 5. No gasta créditos.
- **Dylan (Higgsfield):** puntos 1-4.
1. Saldo: `balance` de Higgsfield. Cada voz cuesta unos 1,6 créditos (`estimate_audio_cost`). **Si no hay saldo suficiente, para y avisa a Antonio**; no compres nada.
2. `generate_audio` con `{"model": "text2speech_v2", "variant": "elevenlabs", "voice_type": "preset", "voice_id": "b847bc29-f184-583a-8ad9-d1f1e16d1a60", "prompt": <voz.txt>}`. Si responde `unlim_choice`, elige `use_unlim: true`, que no gasta créditos.
3. `jobs_wait` hasta que termine y descarga el mp3 a `voz.mp3` con curl (los CDN de Higgsfield están permitidos).
4. Duración entre 25 y 35 s (`ffprobe`). Si se pasa de 35 s, recorta el guion y repite.
5. Tiempos palabra a palabra: `HF_HUB_DISABLE_XET=1 python shorts/tiempos.py voz.mp3 voz.txt palabras.json "<nombres propios>"`.

## [PASO 5/8] Montaje (Georgina)
- Escribe `plan.json` siguiendo los de `shorts/03-jason-lucia/` y `shorts/04-florida-real/`:
  - Cortes cada ~2,2 s, cuadrados con los tiempos de `palabras.json`.
  - Capa "titulo" en el gancho; "fact" n/3 por cada dato; "tarjeta" para cifras (con "contar"); "pastillas" ✅/❌; "cta" al final; "comparativa" si hay foto real de dominio público.
  - Etiquetas con flecha roja apuntando a lo que demuestra el dato.
  - `palabras_clave` en amarillo y `fuente` con las fuentes.
- `python shorts/montaje.py shorts/NN-x/plan.json` → `final.mp4`.

## [PASO 6/8] Revisión de calidad (Almudena)
- `python shorts/herramientas.py fotogramas shorts/NN-x/final.mp4` saca 12 fotogramas en una hoja: míralos con Read.
- Comprueba que no haya subtítulos cortados, que nada tape las caras, que las flechas apunten bien, que no haya textos encima de otros y que nada quede en las zonas que tapa YouTube (arriba, abajo y a la derecha).
- Volumen: `ffmpeg -i final.mp4 -af ebur128=framelog=quiet -f null -` debe dar unos −14 LUFS.
- **Examen:** `python shorts/examen.py shorts/NN-x`. Tiene que salir **APTO** (0 ✗). Arregla también los ⚠ que se puedan arreglar sin rehacer la voz.
- Corrige `plan.json` y vuelve a montar hasta que esté bien (máximo 3 vueltas).

## [PASO 7/8] Publicación y SEO (Guerrero)
`publicacion.md` con:
- Título con curiosidad (máx. 70 caracteres) y 2 alternativos.
- Descripción: datos con ✅/❌, fuentes, créditos de fotos reales, "Unofficial fan-made channel. Not affiliated with Rockstar Games or Take-Two Interactive." y `#GTA6 #GTAVI #Shorts`.
- Comentario fijado con pregunta.
- `**Formato:**` uno de: juego vs real, noticia, personajes, secreto, lista, comparativa, curiosidad (Taison compara por formato). Ajustes: privado, Entretenimiento, inglés, Contenido alterado: No (salvo que se use IA realista), Hecho para niños: No.

## [PASO 8/8] Entrega (Almudena)
1. Copia el vídeo como `shorts/NN-x/VCDT_NN_<Titulo_corto>.mp4`.
2. **SendUserFile** con ese mp4 (`status: "proactive"`, `display: "render"`) para que llegue al móvil de Antonio.
3. Actualiza `docs/banco-ideas.md`: márcalo 🎬 en "Producidos" y añade el gancho a "Ganchos usados". Añade también una entrada a `docs/registro-cambios.md`.
4. `git add` de todo menos los mp4 y las capturas (ya están en .gitignore), commit y push a `claude/youtube-gta6-automation-team-aua7ki`. Si el push falla, `git pull --no-edit` y vuelve a intentarlo.
5. Último mensaje, listo para copiar y pegar: **título**, **descripción** y **comentario fijado** en bloques de código, más una línea con lo que hayas cambiado del título original y por qué.
