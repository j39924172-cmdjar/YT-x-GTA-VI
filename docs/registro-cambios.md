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
