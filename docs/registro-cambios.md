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

## 19/11/2026 — Investigación diaria nº 1 (día de lanzamiento de GTA 6)
- **Canal:** 1 suscriptor (+0). 1.560 visualizaciones (+1.232 desde ayer). El Short de Florida ("…Except ONE Place") pasa de 22 a **1.100** visualizaciones: el formato "juego frente a mundo real" es el que mejor funciona. Horarios de lanzamiento: 403 (+105). Jason y Lucia: 57 (+49).
- **Novedades:** GTA 6 sale hoy (19/11) en PS5 y Xbox Series X|S. Metacritic 99 y "best-reviewed video game ever" según Bloomberg; IGN y GameSpot 10/10. Hasta 212 GB; 79,99 $ / 99,99 $ en EE. UU. (Forbes).
- **Banco:** ideas 7 (mejor valorado de la historia), 8 (212 GB) y 9 (Real Dimez). Recomendadas para hoy: 7 y 8 (noticias del lanzamiento, caducan rápido).
- El Newswire de Rockstar se carga con JavaScript: `curl` no ve los artículos. Las novedades se verifican con medios fiables.
- **Voz gratuita:** `shorts/voz_gratis.py` (Kokoro, voz `am_fenrir`). Short 05 rehecho con ella (`plan_gratis.json`, `final_gratis.mp4`) para que Adam lo compare con Dylan. El sistema sigue con Dylan hasta que Adam decida.

## 19/11/2026 — Piloto automático en la oficina
- Arriba a la derecha de la oficina hay dos **temporizadores**: "Nueva investigación" (cada día a las 10:23, Madrid) y "Repaso del canal" (cada 6 h: 00:47, 06:47, 12:47, 18:47). Al llegar a cero muestran "Trabajando ahora…" y el equipo lo hace solo, sin pedir permiso.
- Paneles nuevos: **"Cómo va el canal"** (suscriptores, visualizaciones y cada Short, con el cambio desde el repaso anterior) y **"Última investigación"** (resumen e ideas; las ideas recomendadas pasan solas a los botones de "Nuevo Short").
- Datos en la base de datos de la oficina: `estado/canal` y `estado/investigacion` (solo los ve Adam).
- Tareas programadas: "Investigación GTA 6 (diaria)" (`trig_01KUgBNkFNc643SCwefs2Pif`) y nueva "Repaso del canal (cada 6 h)" (`trig_017hV7C4vxR4x2DuzQiHRZGF`). `shorts/canal.py --oficina` prepara el documento para la oficina.
- Oficina: 42 pruebas automáticas, incluido el cambio de hora de verano.

## 19/11/2026 — Entrenamiento del equipo: manual magistral y examen
- **Manual magistral** `docs/manual-shorts.md`: las 10 reglas de oro y, para cada uno de los 12 trabajadores, lo que domina, lo que nunca hace y su examen. Incluye la tabla de lecciones con los datos reales del canal: "juego vs real" (Florida, 1.200 visualizaciones) > noticia útil (403) > personajes (57).
- **Examen automático** `shorts/examen.py` (52 pruebas repartidas entre los 12): `python shorts/examen.py shorts/NN-x` o `--todos`. Con un solo ✗ el Short no se entrega. Probado con un Short malo hecho a propósito: lo suspende (6,2/10, 15 fallos).
- **Calibrado con datos reales:** el Short de Florida (el que más funciona) suspendía "ritmo de voz" (2,5 palabras/s) y "gancho concreto" (negación). Las reglas se ajustaron a lo que funciona.
- Resultados: Short 03 9,6 · Short 04 9,4 · Short 05 10. Los tres APTOS. Se añadió `**Formato:**` a sus fichas.
- `docs/produccion-short.md`: el paso 6 exige aprobar el examen y el paso 7 anota el formato.
- Oficina: la ficha de cada trabajador tiene sus nuevos conocimientos para Shorts (antes eran de la fase de vídeos largos en español) y su nota en el examen.

## 19/11/2026 — Rediseño profesional de la oficina (VICECITY DAYS HQ)
- Nueva oficina con aspecto de **consola de productora**. Sustituye a la oficina isométrica con muñecos.
  - Barra superior con la marca, la hora de Madrid y el estado del equipo.
  - Indicadores del día: los 2 temporizadores del piloto automático, suscriptores, visualizaciones, Shorts publicados y nota media del examen.
  - **Plantilla** por los 6 departamentos: cada persona con su avatar, su rol, **qué está haciendo ahora mismo** (según el paso del encargo, el piloto automático o su último trabajo) y su nota del examen. Al tocarla se abre su ficha: su trabajo, lo que domina, lo que nunca hace, su examen y sus últimos trabajos.
  - **Cadena de producción** en 4 columnas: Ideas → En producción → Listos para subir → Publicados.
  - **Cómo va el canal**, con gráfico de visualizaciones; **Actividad** en directo; **Última investigación**.
- Mejoras internas:
  - Colección `actividad` en la base de datos de la oficina: el equipo anota cada trabajo (`docs/produccion-short.md`) y las dos tareas automáticas también.
  - `estado/equipo` con las notas del examen (`shorts/examen.py --todos --oficina`) y la serie del canal para el gráfico (`shorts/canal.py`).
  - Todo es privado: solo lo ve Adam.
- 44 pruebas automáticas en móvil, iPad, portátil y escritorio (`node oficina/test_oficina.js`).

## 19/11/2026 — Cámara en directo en la oficina
- Nueva sección **"Cámara en directo"** (arriba de la oficina) y cámara dentro de la ficha de cada persona: escena animada de la persona en su mesa de la productora (ventana con Vice City de noche, letrero de neón, reloj con la hora real).
- Cuando trabaja, teclea y su pantalla muestra su tarea: radar de tendencias (Jarvis), fuentes verificándose (Nobita), guion escribiéndose (El Chapo), títulos (Torrente), curva de retención (Pablito), móvil vertical (Victillor), capturas con flecha roja (Nil), onda de voz (Cristiano, que además habla al micro), línea de tiempo (Georgina), subida con hashtags (Guerrero), fotogramas aprobados (Almudena) y gráficas (Taison). Un bocadillo dice lo que hace.
- Cuando no tiene trabajo, se recuesta, parpadea, se queda pensando y el café humea; la pantalla muestra el salvapantallas de la marca.
- Respeta "reducir movimiento" del sistema. 51 pruebas automáticas.

## 19/11/2026 — Cámara en directo más realista: cada uno con su puesto de trabajo
- Personas mejor dibujadas: proporciones, cuello, oreja, ojos con brillo, cejas, barba en algunos, gafas (Nobita, Taison), cascos (Cristiano, Georgina) y auricular de dirección (Almudena). Ambos brazos con manos; silla de oficina con ruedas; flexo, sombras, brillo de la pantalla en la cara y viñeta.
- Equipo de cada puesto:
  - Jarvis: dos monitores (radar y noticias), móvil que vibra y mapa de Leonida en la pared.
  - Nobita: documentos, lupa y estantería.
  - El Chapo: portátil, libreta y corcho con el guion.
  - Torrente: pizarra con pósits de títulos.
  - Pablito: dos monitores y tele con gráficas.
  - Victillor: trípode con aro de luz y móvil grabando.
  - Nil: tableta gráfica con lápiz y muestras de color.
  - Cristiano: cabina con paneles acústicos, micro de estudio con filtro antipop e interfaz de audio.
  - Georgina: mesa de edición con dos monitores y altavoces.
  - Guerrero: portátil, monitor y calendario de publicación.
  - Almudena: claqueta y tele.
  - Taison: dos monitores y tele de estadísticas.

## 19/11/2026 — El equipo trabaja siempre y se ve su pantalla real
- **Preproducción real:** Shorts 06 "GTA 6 Just Tied the Best Score in History" (Metacritic 99 empatado con Ocarina of Time; IGN y GameSpot 10/10; GTA 5 se quedó en 97) y 07 "GTA 6 Needs 212 GB. Will It Fit?" (212 GB; PS5 con 667 GB útiles; 79,99 $ / 99,99 $). Cada uno con investigación verificada, guion, títulos, capturas y ficha. Falta voz y montaje.
- Verificación: las primeras búsquedas devolvían páginas anteriores a las críticas ("sin nota"); se descartaron y se confirmó el 99 con GameDaily, Vice, Bloomberg y otros.
- **Nueva tarea "Preproducción continua (sin esperar órdenes)"** 5 veces al día: mantiene hasta 4 Shorts preparados, actualiza la agenda y la actividad. No gasta créditos.
- **Oficina:** los 12 están siempre trabajando en su tarea real (`estado/agenda`). Su monitor y una **pantalla ampliada** junto a la cámara enseñan el contenido real escribiéndose (guion, títulos, fuentes con ✓, capturas, plan de montaje, ficha, números del canal). 53 pruebas automáticas.

## 19/11/2026 — Material oficial nuevo: clips de vídeo y 90 imágenes
- **Vídeos oficiales** que Rockstar publica para descargar en rockstargames.com/VI: Launch Trailer (89 s, 4K), Pre-Load Now (29 s) y Official Cover Art (33 s). `python shorts/clips.py descargar` los baja a `videos/oficiales/` (fuera de git). An Extended Look (14 GB) no cabe: pendiente.
- **Biblioteca de planos** `docs/catalogo-videos.md/.json`: 45 planos detectados automáticamente, 26 utilizables; 19 marcados ❌ (logo oficial de GTA VI o de Rockstar, clubes, ducha, arma a cámara, planos negros o muy oscuros).
- **Plantilla de montaje** `shorts/montaje.py`: nueva escena de vídeo (`"video"` + `"inicio"`), recorte vertical 9:16 alrededor del foco con empuje suave. Probada: 13 s en 1 minuto.
- **Examen**: 3 pruebas nuevas cuando hay vídeo (sin planos prohibidos, crédito "Footage: Rockstar Games", planos ≤ 3,5 s).
- **Catálogo de imágenes**: +90 oficiales tras el lanzamiento (personajes, Ultimate Edition, fondos en vertical *_phone/*_portrait*). Total 176.
- Política de Rockstar: permite usar su material en vídeos de fans "no comerciales" y se reserva retirarlo; se mantiene el crédito y el aviso de canal no oficial. No se usan clips de otros creadores ni filtraciones.

## 19/11/2026 — Títulos recomendados con traducción al español
- La sección de títulos recomendados de la oficina ("Nuevo Short", "Cadena de producción" y "Última investigación") se alimenta de `estado/investigacion` e incluye ya los Shorts preproducidos (06 y 07) y las mejores ideas del banco. Cada título va en inglés y, debajo, su traducción al español ("ES · …"), con su estado (p. ej. "Preproducido · Short 06").
- Las tareas de investigación diaria y de preproducción continua actualizan esa lista cada vez, siempre con la traducción (`es`).
- `docs/banco-ideas.md`: títulos con su traducción y estado 📝 preproducido. Oficina: 55 pruebas automáticas.
- Oficina: selector de **voz** en "Nuevo Short" (Fenrir gratis / Dylan de Higgsfield). El encargo lleva `Voz: …` y el procedimiento la respeta; si el título ya está preproducido se salta directamente a la voz.

## 19/11/2026 — Más títulos: trucos y curiosidades
- Investigación de trucos y curiosidades del lanzamiento (sin spoilers). 7 temas ✅ con 2 medios fiables o más: modo Focus (L3+R3), la policía sigue pistas, perder el dinero al morir, el huevo de Pascua de la torre, el piso de Dexter (hallazgo de fans), el perro en moto de agua y el truco de 250.000 $. 4 temas 🟡 esperan un segundo medio (edificios azul oscuro, empujar barcos, viaje rápido por 100 $, ovni). Bigfoot descartado por spoiler. El tope de 20.000 $ en mano no está confirmado: no se dice.
- Oficina: 13 títulos recomendados, cada uno con traducción al español y etiqueta de tipo (truco, curiosidad, noticia). Se ven hasta 8 en "Nuevo Short" y en la cadena; todos en "Última investigación".
- La investigación diaria prioriza trucos y curiosidades (mínimo 3 de cada 4-6 ideas) y repasa las 🟡. El examen acepta el formato "truco". 56 pruebas.

## 19/11/2026 — Short 08 (primer truco, primer Short con vídeo y voz gratis)
- Encargo de la oficina: "Never Die With Cash in Your Pocket in GTA 6" con voz Fenrir. 27,9 s, examen 9,8/10 (APTO). Carpeta `shorts/08-dinero-al-morir/`.
- Datos (2+ medios): perder el dinero en mano al morir o ser detenido; ingresarlo con la app BuckMe en cualquier cajero (buscador de cajeros); Family Savings no se puede sacar nunca.
- Primer montaje con clips del Launch Trailer. La revisión de fotogramas pilló el logo oficial al final del tráiler: el plano LT32 se separó en LT32 (piscina, ✅) y LT33 (logo, fecha y plataformas, ❌).
- `shorts/voz_gratis.py`: la velocidad puede bajar hasta 0,78 (mejor alargar el guion que hablar despacio). `shorts/montaje.py`: la capa "fact" admite `"etiqueta": "TIP"` para los trucos.
- 19/11 15:53 · Preproducción continua: preparados el **Short 09** "Press Both Sticks in GTA 6 Right Now" (modo Focus) y el **Short 10** "GTA 6 Hid a Real Easter Egg on Top of a Tower". Ya hay 4 preproducidos (06, 07, 09, 10). Agenda, títulos recomendados y actividad actualizados en la oficina.

## 19/11/2026 — Pantalla limpia: sin línea de fuentes ni créditos abajo
- Decisión de Adam: no quiere en los Shorts la línea pequeña de abajo ("Footage: Rockstar Games · Tips: …"). `shorts/montaje.py` ya no la pinta (solo con `"mostrar_fuente": true`). Las fuentes, el crédito de Rockstar y el aviso de canal no oficial siguen en la descripción.
- Nota para la otra sesión: el documento maestro hablaba de "fuente en pantalla" (sección 3); manda la decisión de Adam. CLAUDE.md, manual, procedimiento y examen actualizados (el examen ahora exige pantalla limpia y el crédito en la descripción).
- Re-montados sin la línea: Short 08 y Short 05 (las dos voces). Los 03 y 04 ya estaban subidos.
- 19/11 18:53 · Preproducción continua: ya hay 4 preproducidos (06, 07, 09, 10), no se preparan más. Repaso: datos vigentes; la nota del 06 se vuelve a comprobar justo antes de producir (las búsquedas mezclan páginas previas al lanzamiento).
- 19/11 21:53 · Preproducción continua: cola llena (06, 07, 09, 10). Repaso de las ideas 🟡: el viaje rápido pasa a ✅ reformulado ("GTA 6 Has Fast Travel. It's Hidden in Your Phone", app Ryde Me; sin el precio de 100 $, no confirmado). Los edificios azul oscuro siguen 🟡.

## 19/11/2026 (noche) — Short 11: The $250,000 Cheat Code in GTA 6
- Encargo de la oficina con voz Fenrir. 26,5 s, examen 9,8/10. Carpeta `shorts/11-truco-250k/`.
- Datos con 5 medios (Kotaku, Vice, Screen Rant, GTABase, Beebom): el código ↑ → ↓ ← ↑ ← ↓ →, se desbloquea al acabar la historia y usar trucos desactiva trofeos y guardado en esa sesión (el dinero no pasa a la partida principal).
- El examen pilló una frase de más de 22 palabras: se partió y se regeneró la voz (gratis). Gancho acortado ("a quarter million") para que dure menos de 3 s.
