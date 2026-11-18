# VICECITY DAYS TV — Documento maestro del proyecto
Actualizado: 18/11/2026, 19:15 (Madrid). Fuente: chat de claude.ai con Antonio + brief maestro previo.

> FUENTE DE VERDAD del proyecto. Copia literal del documento que Antonio trajo de la sesión de claude.ai.
> Si algo de este repositorio contradice este documento, manda este documento.
> Los cambios que se hagan aquí se registran en `docs/registro-cambios.md` para pasárselos a la otra sesión.

## 1. Objetivo y decisiones confirmadas
- Negocio: monetizar YouTube Shorts a gran escala con GTA VI. Empezar con UN canal; abrir más solo cuando el primero funcione (visitas + ingresos consistentes).
- Canal: VICECITY DAYS TV. Faceless (Antonio no sale). Idioma inglés; público EE. UU., Reino Unido, Canadá, Australia.
- Temática inicial: exclusivamente GTA VI.
- Formatos: Shorts (prioridad ahora) y más adelante vídeos largos (documentales/recopilaciones estilo Guffi, adaptado, nunca copiado).
- Narración: voz masculina inglés EE. UU., energética, estilo entretenimiento.
- Producción: IA + automatización con criterio humano (investigación, guion, edición, revisión). Nada de contenido automático sin aporte propio.
- Presupuesto: 30–100 €/mes en herramientas, probando antes de pagar.
- Antonio NO juega a GTA y NO grabará gameplay ni clips: los visuales los consigue el equipo.

## 2. Marca
- Estética: negro + morado/rosa neón, gaming futurista. Paleta: #080810, #8B35FF, #C77DFF, #F4F1FF (+ rosa #FF2E8C y amarillo #FFCE28 en los Shorts).
- Canal de YouTube creado y configurado (banner 2560×1440, marca de agua 150×150, descripción en inglés con aviso "Unofficial fan-made channel. Not affiliated with Rockstar Games or Take-Two Interactive.", palabras clave, funciones estándar e intermedias activas, verificación avanzada enviada y pendiente de confirmar, valores de subida: privado, Entretenimiento, inglés).
- Pendiente: confirmar el handle (@ViceCityDaysTV sugerido) y la disponibilidad en otras redes.
- Riesgos: "Vice City" es un nombre de Rockstar y la foto de perfil actual recrea a Lucia/Jason con estilo GTA. Conviene valorar un avatar original. No usar el logo oficial de GTA VI.

## 3. Qué funciona en Shorts de GTA 6 (análisis de referencias de Antonio)
Referencias: @COLETHEMANGTA6 ("5 CRAZY THINGS in GTA 6 That You CAN'T Do In GTA 5", 46K likes); @gta.vice6 ("GTA 6 Trailer 2: 5 Realistic Details You Missed"); @Lonutico ("GTA 6 es tan real que Rockstar tuvo que cambiar el tiempo", 51K likes); @GodcaYT ("En GTA 6 con 6 estrellas no hay dónde esconderse"); @universogtavix ("¿A qué hora sale GTA 6 en tu país?").
Patrones que hay que aplicar:
1. GANCHO con promesa concreta o curiosidad en el primer segundo (texto grande + voz). Ej.: "5 crazy things…", "¿Escapar con 6 estrellas?", "You missed this…".
2. FORMATO LISTA/DATOS: títulos numerados ("2. SIX-STAR WANTED LEVEL"), contador "FACT 1/3", fuente en pantalla ("Source: Rockstar Games").
3. IMÁGENES REALES DE GTA 6 (tráiler/capturas) que demuestran el dato; flechas rojas señalando detalles; comparativas GTA V vs GTA 6; a veces clip real de Florida vs juego.
4. SUBTÍTULOS de 1–2 palabras, grandes, centrados, contorno negro, palabra clave en color.
5. Gráficos animados (relojes, calendarios, diagramas) para datos sin imágenes.
Lo que Antonio rechazó (no repetir): fondos synthwave/genéricos sin imágenes del juego; vídeo IA "bonito" sin dato concreto.
Preferencia de Antonio sobre ganchos: no repetir los mismos; buscar ganchos nuevos, investigados en lo que funciona ahora, y algunos originales que casi nadie usa.

## 4. Sistema de producción (lo que hemos probado y funciona)
1. GUION en inglés, 25–35 s: gancho → 3 datos verificados → CTA "Follow for more GTA 6 secrets". Cada dato con fuente fiable; no inventar ni dar rumores como hechos.
2. VOZ: Higgsfield, modelo text2speech_v2, variante elevenlabs, voz preset "Dylan" (voice_id b847bc29-f184-583a-8ad9-d1f1e16d1a60).
3. VISUALES: capturas oficiales de Rockstar en 4K desde la galería de prensa de VGC: https://www.videogameschronicle.com/files/2025/05/<Nombre>_NN.jpg
   Disponibles: Vice_City_01..09, Leonida_Keys_01..05, Grassrivers_01..04, Port_Gellhorn_01..05, Ambrosia_01..05, Mount_Kalaga_National_Park_01..06, Jason_Duval_01..06 (y Lucia en la misma galería). Evitar Vice_City_07 (club).
4. MONTAJE (sandbox de Higgsfield, Python + Pillow + ffmpeg, 1080×1920, 30 fps):
   - Fondo: captura en movimiento (barrido Ken Burns), cambio cada ~2,2 s, degradado oscuro arriba y abajo.
   - Encima: tarjetas animadas (pastillas rosa/amarillo, "FACT n/3", calendario, reloj, tablas, ✅/❌, contador con barra).
   - Subtítulos palabra a palabra con tiempos de faster-whisper (corregir tokens: "p .m." → "PM", "disk" → "disc").
   - Destello blanco en cada corte, marca "VICECITY DAYS TV" arriba a la derecha.
   - Audio: voz + ritmo electrónico de fondo con sidechain y loudnorm −14 LUFS.
5. ENTREGA: media_upload → curl PUT → media_confirm → enlace cloudfront. En iPad: copiar el enlace, abrirlo en Safari → Compartir → Guardar en Archivos o Fotos.
6. PUBLICACIÓN: título con curiosidad, descripción con datos + fuente + aviso no oficial + #GTA6 #GTAVI #Shorts, comentario fijado con pregunta, "Contenido alterado: No", "Hecho para niños: No".

## 5. Herramientas y cuenta
- Higgsfield conectado a Claude por MCP (https://mcp.higgsfield.ai/mcp). Prueba Ultra con generaciones ilimitadas hasta 21/11/2026 13:42 UTC; renovación automática CANCELADA (no cobrará 79 €); saldo: 10 créditos.
- Coste orientativo con créditos: clip Kling 3.0 de 10 s = 15 créditos; Seedance 2.5 de 15 s a 720p = 105 créditos. Paquete de 500 créditos ≈ 10 Shorts con clips Kling.
- InVideo AI descartado (bloquea GTA/Rockstar). CapCut y ElevenLabs no se usan (Antonio no quiere).
- Limitaciones: la cola gratuita de Higgsfield es muy lenta (vídeo ~2 h, voz 10–20 min, análisis de vídeo de YouTube sin terminar en más de 1 h) y solo permite 1–2 trabajos a la vez. No se pueden descargar vídeos de YouTube ni la web de Rockstar desde el entorno. La app de Claude en iPad no descarga enlaces directos.

## 6. Derechos y monetización
- Capturas y clips de Rockstar pueden recibir reclamaciones de Content ID. Mitigar con fragmentos cortos, voz y datos propios, sin logo oficial y con aviso de canal no oficial.
- YouTube no monetiza contenido repetitivo o producido en masa: cada Short debe aportar algo propio.
- Programa de Socios: verificar requisitos vigentes en la documentación oficial antes de decidir.
- No falsear el país de la cuenta (Antonio reside en España).

## 7. Shorts producidos
1. Piloto "This city doesn't exist" (Seedance IA + voz). Descartado por no tener imágenes del juego.
2. "Who plays GTA 6 first?" (33 s), versión final con capturas oficiales:
   https://d2ol7oe51mr4n9.cloudfront.net/user_3MHWhJdpOs6JErhKJcdXwPnwUD6/c93d50c0-1303-48f9-8f12-5d480412325c.mp4
   Datos (soporte de Rockstar vía Forbes, 12/11/2026): desbloqueo a medianoche hora local del 19/11 en todas las regiones; EE. UU. cuenta como una región con hora del Este → Hawái 19:00, Alaska 20:00, Pacífico 21:00, Montaña 22:00 y Centro 23:00 del 18/11; solo PS5 y Xbox Series X|S, sin PC; edición física con código de descarga, sin disco; hasta 212 GB; precarga desde el 10/11.
   Título recomendado: "Why Hawaii Plays GTA 6 First (Rockstar Confirmed)". Alternativas: "Some Americans Get GTA 6 Before Everyone Else 🕛", "GTA 6 Unlocks TONIGHT… But Not For Everyone".
   Valoración de Antonio: "no está mal, más adelante lo mejoraremos".

## 8. Próximos pasos
- SIGUIENTE SHORT (elegido por Antonio): Jason y Lucia — "Meet the 2 criminals of GTA 6 in 30 seconds", con capturas oficiales de los personajes. Verificar todos los datos antes de guionizar.
- Banco de ideas: "Every place in GTA 6 is a REAL place in Florida" (IN GAME → REAL LIFE), gancho "Rockstar didn't invent this map. They copied a real state."; "5 things GTA 6 does that GTA 5 never could".
- Mejoras: más movimiento en las imágenes, flechas rojas señalando detalles, plantilla reutilizable de montaje, calendario de publicación, avatar original del canal.
- Coordinación: el equipo de Claude Code de Antonio usa este documento como fuente de verdad; se actualiza tras cada avance.
