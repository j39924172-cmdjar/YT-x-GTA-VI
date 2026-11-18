# GTA 6 Studio: equipo automatizado para YouTube

Un equipo de agentes de IA que produce vídeos sobre GTA 6 para tu canal, desde detectar la idea hasta subir el vídeo. Cada miembro del equipo tiene un único trabajo, y un "productor ejecutivo" (el orquestador) los coordina y guarda el estado de cada paso para poder pausar, revisar y reanudar.

```
 Scout de tendencias ─► Estratega ─► Guionista / Dir. de arte ─► Locutor ─► Investigador visual
   (Claude + búsqueda     (elige la     (guion escena a escena     (ElevenLabs)  (clips IA ▸ tu gameplay
    web, YouTube, Reddit)   mejor idea)   + prompts de vídeo IA)                   ▸ tarjetas de título)
                                                                                         │
 Analista ◄── Publicador ◄── Cumplimiento ◄── Diseñador de miniatura ◄── SEO ◄── Editor (ffmpeg)
 (estadísticas  (YouTube API,   (derechos, políticas   (1280x720)          (título,   (voz, textos,
  que alimentan  privado hasta    de YouTube, rumores                       tags,      subtítulos, música)
  la siguiente   que apruebes)    vs. hechos)                               capítulos)
  ronda)
```

| Rol | Archivo | Herramienta de IA |
|---|---|---|
| Scout de tendencias | `agents/trend_scout.py` | Claude con búsqueda web en vivo + YouTube Data API + Reddit r/GTA6 |
| Estratega | `agents/strategist.py` | Claude (5 ideas, elige 1, aprende del historial) |
| Guionista y director de arte | `agents/scriptwriter.py` | Claude (narración + prompts para Higgsfield/Kling/Seedance) |
| Locutor | `agents/voice.py` | ElevenLabs (voz multilingüe) |
| Investigador visual | `agents/visuals.py` | Clips IA generados y tu propio gameplay |
| Editor | `agents/editor.py` | ffmpeg (9:16 para Shorts y 16:9 para vídeos largos) |
| SEO | `agents/seo.py` | Claude |
| Miniaturas | `agents/thumbnail.py` | Pillow (+ fondo IA opcional) |
| Cumplimiento | `agents/compliance.py` | Claude |
| Publicador | `agents/publisher.py` | YouTube Data API v3 |
| Analista | `agents/analytics.py` | YouTube Data API v3 |

## Puesta en marcha

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # también necesitas ffmpeg instalado
cp .env.example .env                   # rellena tus claves

# Prueba sin gastar nada (sin APIs, voz muda, no publica):
python -m gta6_studio --dry-run run --format short
```

Claves necesarias en `.env`:

| Variable | Para qué | Dónde se consigue |
|---|---|---|
| `ANTHROPIC_API_KEY` | Ideas, guion, SEO, cumplimiento | console.anthropic.com |
| `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID` | Voz en off | elevenlabs.io |
| `YOUTUBE_API_KEY` | Tendencias (opcional) | Google Cloud Console → YouTube Data API v3 |
| `YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN` | Subir vídeos | `python -m gta6_studio auth-youtube --client-secret client_secret.json` |

## Uso diario

```bash
# Producción completa (si publishing.enabled=true, se sube en PRIVADO)
python -m gta6_studio run --format short
python -m gta6_studio run --format long --topic "todos los coches secretos de Vice City"

# Flujo con clips de vídeo IA:
python -m gta6_studio run --format short --stop-after script
#   → revisa runs/<id>/guion.md y genera los clips con runs/<id>/ai_prompts.json
#     (Higgsfield, Kling, Seedance...). Guárdalos en assets/ai_clips/<id>/scene_00.mp4, scene_01.mp4...
#     Opcional: assets/ai_clips/<id>/thumbnail.png como fondo de miniatura.
python -m gta6_studio resume <id>

# Rehacer el montaje tras añadir gameplay o clips
python -m gta6_studio render <id>

# Aprobar un vídeo subido en privado
python -m gta6_studio approve <id>

# Actualizar estadísticas (el estratega las usa en la siguiente idea)
python -m gta6_studio stats
```

Cada producción queda en `runs/<id>/`: `guion.md`, `metadata.md` (título, descripción, tags e informe de cumplimiento), `ai_prompts.json`, `final.mp4`, `thumbnail.jpg` y `state.json`.

### Tu gameplay
Pon tus grabaciones de GTA 6 en `assets/footage/` con nombres descriptivos (`vice_city_playa_noche.mp4`, `persecucion_policia_autopista.mp4`). El investigador visual elige el clip cuyo nombre coincide mejor con las palabras clave de cada escena y evita repetirlo. La música libre de derechos va en `assets/music/`.

## Automatización completa (GitHub Actions)

`.github/workflows/produccion-diaria.yml` produce un Short cada día y también se puede lanzar a mano desde la pestaña Actions eligiendo formato y tema. Añade las claves de `.env` como *Secrets* del repositorio. El vídeo queda como artefacto descargable durante 14 días y, si la publicación está activada, se sube a YouTube en privado. En ese modo apruébalo desde YouTube Studio.

Ten en cuenta que en la nube el equipo no tiene tu gameplay, porque los vídeos pesan demasiado para el repositorio. Sin él, las escenas usan tarjetas de título. Para vídeos con imagen real, produce en local con tu carpeta `assets/footage/` o usa el flujo de clips IA.

## Usarlo desde un iPad (sin ordenador)

En un iPad no se pueden instalar programas como Python o ffmpeg, así que el equipo trabaja **en los servidores de GitHub**. Todo se hace desde Safari:

1. **Llaves:** en github.com → tu repositorio → Settings → Secrets and variables → Actions → *New repository secret*, crea `ANTHROPIC_API_KEY`, `ELEVENLABS_API_KEY` y `ELEVENLABS_VOICE_ID`.
2. **Gameplay:** en el repositorio, abre `assets/footage` → *Add file* → *Upload files* y sube clips cortos (máx. 25 MB cada uno) con nombres descriptivos. La música libre de derechos va en `assets/music`.
3. **Hacer un vídeo:** pestaña *Actions* → "Producción diaria GTA 6" → *Run workflow* (elige `short` o `long` y, si quieres, un tema).
4. **Descargarlo:** cuando termine (unos 10 minutos), abre la ejecución y descarga el archivo de *Artifacts*. Ábrelo en la app Archivos (tócalo para descomprimir) y dentro de `runs/` tendrás `final.mp4`, `thumbnail.jpg` y `metadata.md`.
5. **Subirlo:** con la app de YouTube, copiando el título y la descripción de `metadata.md`.

## Configuración (`config.yaml`)
- `channel`: nombre, idioma, audiencia, tono y pilares temáticos.
- `claude`: modelo y nivel de esfuerzo.
- `formats`: duración y número de escenas de Shorts y vídeos largos.
- `publishing`: `enabled`, `require_approval` (recomendado: `true`), programación y declaración de contenido sintético.

## Reglas importantes (derechos y políticas)
- **GTA VI es propiedad de Rockstar Games/Take-Two.** La política de Rockstar suele permitir monetizar vídeos con gameplay propio y comentario. No subas tráileres ni banda sonora oficiales completos ni te presentes como canal oficial.
- **Contenido sintético:** si usas clips de IA realistas, YouTube exige declararlo. El publicador marca `containsSyntheticMedia` automáticamente.
- **Clips IA:** el guionista pide escenas originales con estética de Florida/neón, sin personajes, logotipos ni marcas de Rockstar.
- **Rumores:** el agente de cumplimiento bloquea la publicación si un rumor se presenta como hecho o hay metadatos engañosos.
- **Contenido repetitivo:** YouTube desmonetiza canales de "contenido producido en masa". Revisa los guiones, añade tu voz o tu cara cuando puedas y deja `require_approval: true`.

## Tests
```bash
pytest -q   # producción completa en dry-run con ffmpeg
```
