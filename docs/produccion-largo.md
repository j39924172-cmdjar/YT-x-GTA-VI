# Procedimiento: producir un VÍDEO LARGO (12-20 min)

Petición de Adam (22/11/2026): además de Shorts, vídeos de 12-20 minutos. Llegan desde la oficina como `Producir vídeo largo — TÍTULO: … / Duración: 12-20 min / Voz: … / Encargo: <id>`.
Mismas reglas que los Shorts (datos verificados, nada inventado, sin spoilers de misiones, sin logo oficial, fuentes solo en la descripción, aviso no oficial), más estas:

## 1. Investigación (Jarvis + Nobita)
- Parte de las ideas del panel «🎬 Vídeos largos» (`estado/largos`) y de lo ya verificado en `docs/banco-ideas.md` y en las carpetas de los Shorts.
- 6-10 capítulos; cada capítulo con 2-4 datos verificados (fuente primaria o 2 medios). Lo que no se verifique, fuera.
- Referentes: `python shorts/largos.py --oficina /tmp/largos.json` (qué formatos largos funcionan ahora). Solo formatos ✅ (sin grabar partidas).

## 2. Guion (El Chapo + Torrente + Pablito)
- Inglés, 1.800-2.800 palabras (12-20 min). Gancho de 15 s que promete el final, «lo mejor al final» para la retención, un mini-gancho cada 60-90 s ("but the next one is even crazier").
- Capítulos con título corto; personalidad (hablar a "you", reacciones, giros). Sin relleno.
- Guarda `guion.md`, `voz.txt` y `capitulos.json` ([{"titulo", "desde"}]).

## 3. Voz (Cristiano)
- Fenrir (gratis): `python shorts/voz_gratis.py` por capítulos y se unen con ffmpeg. Dylan solo si hay créditos (un vídeo largo cuesta mucho más que un Short).

## 4. Montaje (Georgina)
- **Horizontal 1920×1080**, 30 fps. Capturas oficiales 4K (176 en el catálogo) + clips oficiales + mapas y tarjetas animadas; cambio de plano cada 3-5 s; modo show (efectos, zooms) más suave que en Shorts.
- Tarjeta de capítulo al empezar cada uno, contadores y comparativas, barra de progreso.
- ⚠️ La plantilla `shorts/montaje.py` es vertical: el primer vídeo largo necesita su versión horizontal (`shorts/montaje_largo.py`, por hacer).

## 5. Publicación (Guerrero)
- Título con curiosidad (≤ 70), miniatura 1280×720 (captura oficial + texto grande, sin logo oficial), descripción con **capítulos con minutos** (00:00 …), fuentes, créditos de Rockstar y aviso no oficial.
- Comentario fijado con pregunta. Fin de vídeo y tarjeta hacia un Short relacionado.

## 6. Derechos
- Contenido transformador: análisis y datos propios con nuestra voz; clips oficiales cortos; nada de partidas ni vídeos de otros canales.
