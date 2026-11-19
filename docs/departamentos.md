# Reparto del trabajo por departamentos — VICECITY DAYS TV

Basado en el documento maestro (`docs/vicecity-estado.md`). Las personas son las de la oficina virtual; aquí se reparten en los 6 departamentos que pide Antonio.

| Departamento | Quién | Responsable de | Entrega | Regla clave del documento |
|---|---|---|---|---|
| **1. Investigación y verificación de datos** | Jarvis (tendencias) y Nobita (verificación y derechos) — investigación automática cada 2 días | Elegir datos con tirón y comprobar cada uno en una fuente fiable: Rockstar primero, después medios serios (Forbes, IGN, VGC…) | `investigacion.md`: cada dato con su fuente, fecha y nivel (confirmado, oficial pero vago, o rumor descartado) | Sección 4.1 y 6: nada inventado; los rumores no son hechos |
| **2. Guiones y ganchos** | El Chapo (guion), Torrente (ganchos y títulos), Pablito (retención) y Victillor (formato Short) | Guion en inglés de 25-35 s con gancho → 3 datos → CTA. Banco de ganchos nuevos sin repetir | `guion.md` con tiempos, textos de pantalla y ganchos alternativos | Sección 3: gancho concreto en el 1er segundo; ganchos nuevos y algunos originales |
| **3. Visuales** | Nil | Elegir las capturas oficiales que DEMUESTRAN cada dato, encuadres, flechas rojas y tarjetas | Lista de capturas por escena y diseño de tarjetas | Sección 3.3 y 4.3: imágenes reales del juego; nada genérico; evitar Vice_City_07 |
| **4. Montaje** | Georgina (montaje) y Cristiano (voz Dylan) | Voz en Higgsfield, montaje 1080×1920 con la plantilla, subtítulos palabra a palabra y audio a −14 LUFS | `final.mp4` y miniatura | Sección 4.2 y 4.4 |
| **5. Publicación y SEO** | Guerrero | Título con curiosidad (más 2 alternativos), descripción con datos, fuente y aviso, hashtags, comentario fijado y ajustes de subida | `publicacion.md` | Sección 4.6 |
| **6. Estrategia y crecimiento** | Almudena (decide) y Taison (datos) | Calendario, banco de ideas, avatar original, handle, requisitos del Programa de Socios y lectura de las métricas | Plan semanal y decisiones | Secciones 1, 2, 6 y 8 |

## Flujo de un Short
Investigación verifica → Guiones escribe (solo con datos verificados) → Visuales asigna capturas → Montaje pone voz y monta → Publicación prepara la ficha → Estrategia revisa y da luz verde → Antonio aprueba y sube.

## Piloto automático (sin pedir permiso)
La oficina muestra arriba a la derecha dos temporizadores. Cuando llegan a cero, el equipo trabaja solo en la sesión principal de producción (la que tiene permiso para guardar en GitHub) y el resultado aparece en la oficina (documentos `estado/investigacion` y `estado/canal` de su base de datos, que solo ve Adam).

### Investigación diaria (Jarvis + Nobita) — 10:23 hora de Madrid
Tarea programada **"Investigación GTA 6 (diaria)"** (`trig_01KUgBNkFNc643SCwefs2Pif`). Ritmo de publicación: **2 Shorts al día**, así que hacen falta unas 14 ideas por semana. Cada vez:
1. Lee `CLAUDE.md`, `docs/vicecity-estado.md`, `docs/banco-ideas.md` y el último repaso en `docs/canal-estadisticas.json`.
2. Busca novedades de las últimas 24-48 h: web oficial de Rockstar (fuente primaria) y medios fiables (IGN, GameSpot, Eurogamer, VGC, Polygon, Forbes). El Newswire se carga con JavaScript: `curl` no lo ve.
3. Verifica cada dato: fuente primaria, o dos medios fiables que coincidan. Los rumores se marcan como rumores y no se usan como hechos.
4. Añade 3-5 ideas nuevas a `docs/banco-ideas.md` con gancho NUEVO, 3 datos con fuente e imágenes. Da prioridad al formato que mejor funciona en el canal.
5. Escribe `estado/investigacion` en la oficina: resumen e ideas (las 2 recomendadas primero). Las ideas pasan solas a los botones de "Nuevo Short".
6. Registro de cambios, commit y push, y resumen corto para Adam.

### Repaso del canal (Taison) — cada 6 h: 00:47, 06:47, 12:47 y 18:47 hora de Madrid
Tarea programada **"Repaso del canal (cada 6 h)"** (`trig_017hV7C4vxR4x2DuzQiHRZGF`). `python shorts/canal.py --oficina /tmp/estado_canal.json` lee los datos públicos de https://www.youtube.com/@vicecitydaystv, guarda el historial en `docs/canal-estadisticas.json` y prepara `estado/canal` para la oficina. Nunca se piden contraseñas: las estadísticas privadas (vistos frente a deslizados, retención) las pasa Adam con capturas de YouTube Studio una vez por semana.

Si se cambian estos horarios, hay que cambiar también `HORARIO` en `oficina/index.html`.
Las dos tareas anotan lo que hacen en la colección `actividad` de la oficina (ver `docs/produccion-short.md`).
### Preproducción continua (todo el equipo) — 09:53, 12:53, 15:53, 18:53 y 21:53 hora de Madrid
Tarea programada **"Preproducción continua (sin esperar órdenes)"** (`trig_016LhTmQUTHxZPPEQ5trCoJ1`). El equipo no espera órdenes: coge las mejores ideas ✅ del banco y deja preparados hasta 4 Shorts (investigación verificada, guion, títulos, capturas y ficha de publicación, con "Estado: preproducción"). Cuando ya hay 4, repasa y mejora los existentes. Cuando Adam pide uno, solo faltan la voz, el montaje y el examen.
Cada vez escribe en la oficina `estado/agenda`: la tarea de cada persona y el **contenido real de su pantalla** (el guion, los títulos, las fuentes, las capturas, el plan de montaje…), que la Cámara en directo enseña escribiéndose. Y anota en `actividad` lo que han hecho.

Ninguna de estas tareas genera voz, monta ni gasta créditos: eso lo decide Adam.
