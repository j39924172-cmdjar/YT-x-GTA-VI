# Registro de cambios (para pasar a la otra sesión de Claude)

## 18/11/2026 — Sesión de Claude Code
- Documento maestro guardado en `docs/vicecity-estado.md` y resumen en `CLAUDE.md`.
- Reparto por departamentos en `docs/departamentos.md`.
- **Short 03 "Meet GTA 6's 2 Criminals in 30 Seconds" producido** (29,6 s, 1080×1920, 30 fps, −14,7 LUFS integrado). Carpeta `shorts/03-jason-lucia/`.
  - Datos verificados en la **fuente primaria**: rockstargames.com/VI/only-in-leonida (las antiguas URL /VI/people/... ya no existen). Detalle y citas literales en `investigacion.md`.
  - Dato nuevo con gancho: la madre de Lucia sueña con una vida mejor "since their days in Liberty City" (la ciudad de GTA IV).
  - Descartado por no estar en la fuente: "primera protagonista femenina de la saga" y el cambio de personaje en cualquier momento.
  - Voz: Higgsfield `text2speech_v2` / `elevenlabs` / Dylan (1,65 créditos o ilimitado, según la prueba Ultra). Lista en menos de 1 minuto.
  - Capturas usadas: Jason_Duval_01/02/03/04/06, Lucia_Caminos_01/02/03/04/05, Leonida_Keys_01/02/04. Evitada Lucia_Caminos_06 (discoteca), por el mismo criterio que Vice_City_07.
- **Plantilla de montaje reutilizable** `shorts/montaje.py` + `shorts/tiempos.py` (cada Short se define en un `plan.json`):
  - Implementa la sección 4.4: Ken Burns con cortes de ~2,2 s, degradados, "FACT n/3" con contador de barra, pastillas rosa/amarillo con ✅/❌, flechas rojas animadas que apuntan a un punto de la captura, tarjeta de ruta animada, subtítulos de 1-2 palabras con la palabra clave en amarillo (tiempos de faster-whisper y texto tomado del guion, así que no hay erratas), destello en cada corte, marca arriba a la derecha y fuente en pantalla.
  - Ritmo electrónico **generado por código** (sin derechos de terceros), con sidechain bajo la voz y loudnorm −14 LUFS.
  - Tipografías libres (OFL): Anton y Montserrat, en `shorts/fuentes/`.
  - El montaje se hace en este entorno de Claude Code (≈45 s por Short) en lugar del sandbox de Higgsfield: misma tecnología (Python + Pillow + ffmpeg) y sin colas.
- **Entorno de nube "YT-x-GTA-VI"** con acceso a videogameschronicle.com, rockstargames.com, el CDN de Higgsfield y Hugging Face (para faster-whisper).

## 18/11/2026 (tarde) — Sesión de Claude Code
- **Short 04 "GTA 6's Map Is Real Florida… Except ONE Place" producido** (31,7 s, −14,3 LUFS). Carpeta `shorts/04-florida-real/`.
  - Gancho del banco corregido para que sea 100 % cierto: en vez de "They copied a real state" (no demostrable), "Their own website calls Leonida 'the sunshine state'" (cita literal de rockstargames.com/VI/only-in-leonida; es el apodo de Florida).
  - Datos: Grassrivers ↔ Everglades, "River of Grass" (NPS); Ambrosia (refinería Allied Crystal, según Rockstar) ↔ Clewiston "America's Sweetest Town" y la quema de caña antes de la cosecha; Mount Kalaga ↔ Florida no tiene montañas: Britton Hill mide 345 ft y es el punto más alto más bajo de los 50 estados.
  - Primera **comparativa IN GAME / REAL LIFE**: Leonida_Keys_01 frente a una foto real del Seven Mile Bridge (U.S. DOT, dominio público, con crédito en el vídeo y en la descripción).
- **Hallazgo:** las capturas oficiales en 4K también están en rockstargames.com (`/VI/_next/static/media/...jpg`), cada una con la descripción de Rockstar. Catálogo de 86 imágenes en `docs/catalogo-imagenes.md`, incluidas las nuevas de la galería de lanzamiento (Vice_City_13–27, Grassrivers_07–08, Leonida_Keys_07…).
- **Plantilla** `shorts/montaje.py`: capas nuevas "tarjeta" (dato con contador animado, p. ej. 0 → 345 FT) y "comparativa" (pantalla partida juego/real).
- **Banco de ideas** `docs/banco-ideas.md` con 4 ideas verificadas en la web oficial: Vercetti Estate (Vintage Vice City Pack), Cal Hampton y los pájaros, Brian Heder el contrabandista, y los jefes de banda.
- **Investigación automática cada 2 días** (Jarvis + Nobita): tarea programada "Investigación GTA 6 cada 2 días", a las 10:23 hora de Madrid, que añade ideas verificadas al banco y hace push. Procedimiento en `docs/departamentos.md`.
- Wikimedia Commons limita mucho las descargas (error 429): solo se pudo bajar 1 de 5 fotos reales. Para fotos reales, mejor pocas y elegidas.

## 18/11/2026 (noche) — Producir un Short con solo escribir el título
- La **oficina virtual** pasa a ser la "HQ" de VICECITY DAYS TV, con la paleta de marca. Panel **Nuevo Short**: título, ideas del banco con un toque y botón **Producir Short**; seguimiento de los 8 pasos con el equipo animado e historial de encargos. Se retira el sistema antiguo en español (vídeos largos).
- Al pulsar Producir, la oficina lanza la tarea "Producir Short" (conector Claude Code), que manda el título a la sesión de producción de Claude Code (la que tiene Higgsfield, la plantilla y el entorno con acceso a Rockstar). Esa sesión sigue `docs/produccion-short.md`: verifica datos, escribe el guion, pone la voz de Dylan, monta, revisa fotogramas, entrega el MP4 al chat y al móvil con título, descripción y comentario fijado, y lo guarda en GitHub.
- Limitación descubierta: las tareas que abren una sesión NUEVA no pueden llevar conectores en esta organización (no tendrían Higgsfield). Por eso la producción va siempre a la misma sesión.
- **Coste real de la voz:** unos 1,6 créditos de Higgsfield por Short. La prueba ilimitada NO cubre `text2speech_v2`. Saldo tras los Shorts 03 y 04: 6,85 créditos (unos 4 Shorts más).
- Entorno de nube: script de preparación que instala Pillow, numpy y faster-whisper al arrancar.
- Oficina: 32 pruebas automáticas (`node oficina/test_oficina.js`).
- La investigación cada 2 días ahora se ejecuta en la sesión principal (tarea `trig_01KUgBNkFNc643SCwefs2Pif`). La primera prueba en una sesión nueva investigó bien, pero no pudo hacer push (repositorio no autorizado en sesiones nuevas). Esa investigación se perdió al borrar la tarea antigua: borrar una tarea programada borra también sus sesiones.
- **Arreglo del botón Producir:** el primer intento falló porque la página no podía usar el conector "Claude Code Remote" en la cuenta de Antonio. Además, la oficina apuntaba como "en cola" encargos que nunca salieron (el fallo estaba en cómo trataba los errores dudosos). Ahora el encargo va como comentario "Send to Claude" (sin conectores), el progreso se guarda en la base de datos de la página y, si el envío falla, el encargo queda "no enviado" con la frase para pegar en el chat. 31 pruebas automáticas.

## 18/11/2026 (noche) — Short 05 desde la oficina (primer encargo real)
- Antonio pidió desde la oficina "Every GTA 6 Gang Leader in 30 Seconds". El encargo llegó como comentario y la oficina mostró los 8 pasos en directo.
- **Título ajustado** a "3 GTA 6 Crime Bosses in 30 Seconds": Rockstar no llama "gang leader" a nadie y no hay lista oficial de "todos", así que "Every" no era verificable. Datos de Boobie Ike, Raul Bautista y Brian Heder, citados de rockstargames.com/VI/only-in-leonida.
- 27,9 s, −14,3 LUFS, 12 capturas oficiales de Rockstar (sin la de las bailarinas). Carpeta `shorts/05-crime-bosses/`. Voz: 1,6 créditos de Higgsfield.

## 18/11/2026 (noche) — Investigación diaria y repaso del canal
- El dueño del canal se llama **Adam** (no Antonio). Las tareas y los resúmenes van dirigidos a Adam.
- Ritmo decidido: **2 Shorts al día**. La investigación pasa de cada 2 días a **diaria** (10:23 Madrid) e incluye el repaso del canal.
- Nueva herramienta `shorts/canal.py`: lee los datos públicos de @vicecitydaystv (sin contraseñas ni claves) y guarda el historial en `docs/canal-estadisticas.json`. Primer registro: 1 suscriptor, 3 Shorts públicos, 328 visualizaciones (298 del Short de horarios de lanzamiento).
- Entorno de nube: se permite `www.youtube.com` para leer el canal.
- Las estadísticas privadas (vistos frente a deslizados, retención) las pasa Adam con capturas de YouTube Studio.

## 18/11/2026 (noche) — Prueba de voz gratuita
- Adam quiere no pagar nada aparte de Claude. Higgsfield: el plan Starter (19 $/mes, 270 créditos) no le aparece mientras dure la prueba de Ultra (hasta el 21/11); lo gratis de sus campañas no funciona desde Claude (MCP) y no incluye voz.
- Prueba con **Kokoro** (voz de código abierto, gratis, funciona en la sesión con kokoro-onnx y el modelo de Hugging Face). Comparativa `shorts/05-crime-bosses/comparativa_voces.mp3`: Dylan / Michael / Fenrir / Puck. Pendiente de que Adam elija; el sistema sigue con Dylan hasta entonces.
