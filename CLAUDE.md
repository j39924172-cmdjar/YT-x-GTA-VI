# CLAUDE.md — VICECITY DAYS TV

**Lee primero `docs/vicecity-estado.md`.** Es la FUENTE DE VERDAD del proyecto (documento maestro de Antonio).
Si algo de este repositorio lo contradice, manda el documento maestro. Si ves una forma mejor de hacer algo
o algo no se puede aplicar, avisa a Antonio ANTES de cambiarlo.

## Resumen del proyecto
- Canal: **VICECITY DAYS TV**. YouTube Shorts de **GTA VI**, en **inglés** (EE. UU., Reino Unido, Canadá, Australia). Faceless.
- Prioridad: Shorts y, desde el 22/11/2026, también vídeos largos de 12-20 min (decisión de Adam). Un solo canal hasta que funcione.
- Antonio no juega ni graba: los visuales los consigue el equipo (capturas oficiales de Rockstar de la galería de VGC).
- Presupuesto 30–100 €/mes. No se usan InVideo, CapCut ni ElevenLabs directamente. La voz es Higgsfield (`text2speech_v2`, variante `elevenlabs`, voz preset "Dylan", `b847bc29-f184-583a-8ad9-d1f1e16d1a60`).
- Marca: negro y morado/rosa neón. #080810, #8B35FF, #C77DFF, #F4F1FF, más #FF2E8C y #FFCE28 en los Shorts. Marca "VICECITY DAYS TV". Nunca el logo oficial de GTA VI.

## Sistema de producción de un Short (sección 4 del documento maestro)
1. Guion en inglés, **40–60 s en TODOS los Shorts** (decisión de Adam, 22/11/2026: nada de 30 s): **gancho → 3 datos verificados contados como historia con giro (sin «Fact 1/2/3» ni tarjetas FACT: Adam, 24/11/2026) → bucle → CTA "Follow for more GTA 6 secrets"**. Cada dato con fuente; nada inventado; los rumores no se dan como hechos. Fuentes válidas: web oficial de Rockstar, medios fiables, **X** (cuentas oficiales = primaria; el resto, rumor) y **YouTube** (canal oficial de Rockstar). Las fuentes van solo en la descripción, nunca en pantalla.
2. Voz: Dylan en Higgsfield.
3. Visuales: clips de los tráileres oficiales de Rockstar (`docs/catalogo-videos.md`, `shorts/clips.py`) y capturas oficiales 4K `https://www.videogameschronicle.com/files/2025/05/<Nombre>_NN.jpg`. Evitar `Vice_City_07`.
4. Montaje 1080×1920 a 30 fps: Ken Burns con cambio cada ~2,2 s, degradados, «golpes» de texto enorme en los momentos clave (nada de "FACT n/3"), pastillas rosa/amarillo, flechas rojas, subtítulos palabra a palabra (faster-whisper), destello blanco en cada corte, marca arriba a la derecha, ritmo electrónico con sidechain y loudnorm −14 LUFS. Plantilla: `shorts/montaje.py`.
5. Publicación: título con curiosidad; descripción con datos, fuente, aviso no oficial y #GTA6 #GTAVI #Shorts; comentario fijado con pregunta; "Contenido alterado: No"; "Hecho para niños: No".

## Vídeos largos (Adam, 22/11/2026)
- Además de Shorts, vídeos de **12-20 min** (horizontal 1920×1080). Encargo desde la oficina: «Producir vídeo largo — TÍTULO: … / Duración: 12-20 min / Referencia: …».
- **Todo vídeo largo sigue el PROMPT MAESTRO de Adam: `docs/prompt-largos.md`** (FASE 1 guía de estilo de la referencia → ESPERAR título, guion y narración de Adam → FASE 2-3 escena por escena → montaje → prompt de miniatura para ChatGPT). Si Adam no pasa referencia, el equipo la busca con `python shorts/largos.py` y lo dice. No afirmar haber visto un vídeo que no se ha podido inspeccionar.
- **Un clic (Adam, 22/11/2026):** Adam solo pulsa «Producir»; el equipo hace todo (guion, voz, montaje, publicación, miniatura) sin esperarle. Plantilla: `shorts/montaje_largo.py`; voz larga: `shorts/voz_larga.py`.
- Procedimiento: `docs/produccion-largo.md`. Radar de largos → `estado/largos` en la oficina.

## Patrones que funcionan (sección 3)
Gancho concreto en el primer segundo; formato de lista o datos con contador (las fuentes van en la descripción, nunca en pantalla: decisión de Adam, 19/11/2026); imágenes reales del juego que demuestran el dato; subtítulos de 1–2 palabras con la palabra clave en color; gráficos animados para los datos sin imagen.
**No repetir:** fondos synthwave o genéricos sin imágenes del juego, vídeo de IA "bonito" sin dato, ganchos ya usados.

## Derechos y monetización (sección 6)
Fragmentos cortos, voz y datos propios, sin logo oficial, con el aviso "Unofficial fan-made channel. Not affiliated with Rockstar Games or Take-Two Interactive." Cada Short aporta algo propio: nada repetitivo ni producido en masa. Requisitos del Programa de Socios: verificar en la documentación oficial. No falsear el país de la cuenta.

## Organización
- Reparto por departamentos: `docs/departamentos.md`.
- Registro de cambios para la otra sesión: `docs/registro-cambios.md`. Añade una entrada cada vez que termines algo.
- Cada Short vive en `shorts/<nº>-<nombre>/`: `investigacion.md` (datos y fuentes), `guion.md`, `publicacion.md` y el montaje.

## Producir un Short desde un título
- Antonio escribe el título en la oficina virtual (https://claude.ai/artifact/WdZBBpgqbXUEDL1Wk3kFRC) y pulsa **Producir Short**.
- La oficina guarda el encargo en su base de datos (`encargos/<id>`) y lo envía como comentario "Send to Claude" a la sesión de producción, la que vigila la oficina y tiene Higgsfield conectado. No usa conectores: el del conector "Claude Code Remote" falló en la cuenta de Antonio y esa tarea está desactivada.
- Esa sesión sigue `docs/produccion-short.md` y anota el paso en `encargos/<id>` con ArtifactData; la oficina lo muestra en directo.
- Herramientas: `shorts/herramientas.py` (descargar capturas del catálogo, hoja de contacto, fotogramas, textos de Rockstar), `shorts/tiempos.py` y `shorts/montaje.py`.

## Todo lo hablado va a la oficina (petición de Adam, 20/11/2026)
- Cada vez que Adam decida, pida o proponga algo en el chat, apúntalo en la oficina: ArtifactData `get` de `estado/charla` y `set` (if_version) con el apunte nuevo DELANTE en `items` = {"fecha": "DD/MM", "tipo": "decision|regla|idea|pendiente", "texto": "<en español, ≤ 160 caracteres>"}. Cuando un pendiente se resuelva, cámbialo a decision.
- Si Adam pasa un Short o un canal de referencia (en el chat o con el botón «🕵️ Que lo estudie el equipo», que llega como comentario "Estudiar referente — <url>"): añádelo a `docs/referentes.json` con su nota, ejecuta `python shorts/espia.py --oficina /tmp/ref.json` y `set` de `estado/referentes`; saca 2-3 ideas con datos verificados para `estado/virales` y apúntalo en `estado/charla`. Solo para aprender formatos: nunca copiar títulos, guiones ni imágenes.
- Las ideas virales (`estado/virales`) llevan: titulo, es, formato, gancho, referencia, porque (datos con fuentes), comentario (fijado) y verificado ("✅" o lo que falta).

## Partes antiguas del repositorio (antes del documento maestro)
`gta6_studio/` (pipeline en español con ElevenLabs y vídeos largos) es de una fase anterior y **no sigue** el documento maestro: español en vez de inglés, ElevenLabs, prioridad al vídeo largo. No los uses para VICECITY DAYS TV hasta que Antonio decida si se adaptan o se retiran.
