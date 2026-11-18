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

## Investigación periódica cada 2 días (Jarvis + Nobita)
Tarea programada en Claude Code: **"Investigación GTA 6 cada 2 días"** (10:23 hora de Madrid). Se ejecuta en la sesión principal de producción, la que tiene permiso para guardar en GitHub. Cada vez:
1. Lee `CLAUDE.md`, `docs/vicecity-estado.md` y `docs/banco-ideas.md`.
2. Busca novedades de las últimas 48-72 h: Rockstar Newswire y web oficial (fuente primaria), medios fiables (IGN, GameSpot, Eurogamer, VGC, Polygon, Forbes) y lo que más se comenta.
3. Verifica cada dato: fuente primaria, o dos medios fiables que coincidan. Los rumores se marcan como rumores y no se usan como hechos.
4. Añade 3-5 ideas nuevas a `docs/banco-ideas.md` con gancho NUEVO, 3 datos con fuente e imágenes del catálogo.
5. Actualiza `docs/catalogo-imagenes.md` si Rockstar ha publicado imágenes nuevas.
6. Anota el resumen en `docs/registro-cambios.md`, hace commit y push, y avisa con un resumen corto.
No produce vídeos ni gasta créditos: eso lo decide Antonio.
