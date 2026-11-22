# PROMPT MAESTRO DE VÍDEOS LARGOS (de Adam, 22/11/2026)

**Regla fija:** este prompt se aplica a TODOS los vídeos de larga duración (12-20 min) de VICECITY DAYS TV.
Lo guardamos palabra por palabra (abajo) y, después, cómo lo aplica el equipo con nuestras herramientas y reglas.

---

## Texto original de Adam (literal, no editar)

Actúa como un director creativo, editor audiovisual senior y especialista en motion graphics, composición visual y storytelling. Analiza los vídeos de referencia que adjunto para trasladar su lenguaje visual, ritmo de edición y calidad de producción a una idea diferente.

FASE 1 — ANÁLISIS DEL VÍDEO DE REFERENCIA
Analiza cuidadosamente el vídeo, escena por escena y segundo por segundo cuando las herramientas disponibles lo permitan, prestando atención a:
1. Estilo visual: estética general, paleta de colores, tipografías, iluminación, texturas, fondos, profundidad, sombras y tratamiento de imagen.
2. Motion graphics: animaciones, movimientos de elementos, gráficos 2D/3D, keyframes, easing, transiciones, partículas, máscaras y efectos visuales.
3. Composición: distribución de elementos, jerarquía visual, encuadres, capas, perspectivas, uso del espacio y relación entre texto, imágenes y gráficos.
4. Edición y ritmo: duración de planos, frecuencia de cortes, velocidad, sincronización con la narración, zooms, movimientos de cámara y cambios visuales.
5. Narrativa visual: representación de conceptos, metáforas visuales, recursos de atención y conexión entre escenas.
6. Identidad audiovisual: patrones recurrentes, recursos distintivos y transiciones características.
Identifica los patrones que se repiten y separa los elementos esenciales del estilo de los que dependen del tema original. Si hay varias referencias, explica qué aporta cada una.
Antes de analizar, comprueba que puedes acceder a los archivos y examinar su contenido visual con las herramientas disponibles. No afirmes haber visto vídeo que no has podido inspeccionar. Si trabajas con fotogramas muestreados, indica los intervalos y las limitaciones del análisis de movimiento.

FASE 2 — ADAPTACIÓN A MI IDEA
Cuando te proporcione mi título, guion y narración, desarrolla una propuesta audiovisual coherente con el estilo analizado, con escenarios, objetos, personajes y composiciones originales adaptados a mi temática.
No copies literalmente las escenas: reproduce los principios de composición, dinamismo, sofisticación y ritmo, construyendo una identidad propia. Cada escena debe representar lo que se narra y estar ambientada en el contexto de mi vídeo.

FASE 3 — DESARROLLO ESCENA POR ESCENA
Una vez recibas mis materiales, incluye para cada escena:
- Tiempo de inicio y finalización, sincronizado con la duración real del audio.
- Fragmento exacto de narración correspondiente.
- Descripción visual detallada.
- Composición, ambientación, elementos y distribución de capas.
- Motion graphics, animaciones, movimientos de cámara y transiciones.
- Efectos visuales, iluminación, colores, tipografías y profundidad.
- Instrucciones precisas para construir, animar y conectar la escena con las herramientas disponibles.

REGLAS OBLIGATORIAS
- Mantén una identidad visual coherente y respeta la lógica de composición y movimiento de la referencia.
- Evita escenas genéricas, imágenes estáticas innecesarias y recursos que rompan el estilo.
- Prioriza fluidez, legibilidad y sincronización con la narración.
- Distingue lo observado de lo inferido; no inventes detalles de la referencia.
- No cambies el significado del guion ni añadas información innecesaria.
- Cada escena debe tener una justificación narrativa y visual.
- Si una técnica no se puede reproducir exactamente, propone la alternativa más fiel y viable.
- Evita repetir composiciones idénticas salvo que sea una decisión narrativa deliberada.

IMPORTANTE: Primero entrega solo el desglose técnico y la guía de estilo audiovisual. Espera a que te envíe mi título, guion y narración antes de desarrollar o renderizar las escenas.
OBJETIVO FINAL: Crear una edición original inspirada en la calidad, el ritmo y el lenguaje audiovisual de las referencias, adaptada por completo a mi contenido.
ADEMAS me pasará después de pasarme el vídeo completo, un prompt para ChatGPT me crea una miniatura del vídeo potente y viral.

---

## Cómo lo aplica el equipo (lectura de Claude, 22/11/2026)

### Flujo de un vídeo largo con este prompt
1. **Referencia.**
   - **A) Adam pasa el vídeo** (archivo adjunto en el chat o enlace en el encargo de la oficina, campo «Vídeo de referencia»).
   - **B) Adam no pasa nada:** el equipo elige la referencia con `python shorts/largos.py` (vídeos largos de GTA 6 que más funcionan, solo formatos ✅ que se pueden hacer sin grabar partidas) y dice cuál ha elegido y por qué.
2. **FASE 1 — Guía de estilo** (`largos/<nº>-<nombre>/fase1-estilo.md`): los 6 puntos del prompt, patrones que se repiten, qué es esencial del estilo y qué depende del tema original, y **qué se ha podido ver realmente** (ver límites). Se entrega a Adam y **se para**.
3. **Espera** al título, guion y narración de Adam. Si Adam solo da el título, el equipo propone guion y narración (datos verificados, como siempre) y Adam los aprueba antes de seguir.
4. **FASE 2 — Propuesta audiovisual** adaptada a GTA 6 con imágenes y clips oficiales de Rockstar (escenarios, objetos y composiciones propias, nada copiado de la referencia).
5. **FASE 3 — Desglose escena por escena** (`fase3-escenas.md`): inicio y fin sincronizados con el audio real (tiempos de `shorts/tiempos.py`), fragmento exacto de narración, descripción visual, capas, animación, transiciones, efectos, color, tipografía e instrucciones para construirla con nuestras herramientas.
6. **Montaje** (horizontal 1920×1080) siguiendo la FASE 3 y **revisión** con fotogramas.
7. **Miniatura:** con el vídeo terminado, un **prompt para ChatGPT** de miniatura potente y viral (ver abajo).

### Límites reales (para no prometer lo que no se puede)
- **Ver la referencia:** si Adam adjunta el archivo, se extraen fotogramas (1 cada 0,5-1 s; más densos en transiciones) y se transcribe el audio para medir planos, cortes y sincronía. El movimiento (easing, keyframes, partículas) se **infiere** de fotogramas seguidos: se dice siempre el intervalo y que es inferido.
- **Solo con enlace de YouTube:** no se descarga el vídeo de otro canal. Se analiza lo público (título, duración, capítulos, miniatura, descripción) y se dice claramente que el vídeo no se ha visto. Para un análisis escena por escena, Adam debe adjuntar el archivo (por ejemplo, una grabación de pantalla).
- **Herramientas de montaje:** nuestra plantilla es Python (PIL + ffmpeg): capas 2D, máscaras, zooms, parallax 2,5D, brillos, partículas sencillas, tipografía animada. 3D real o efectos de After Effects avanzados no: se propone la alternativa más fiel (regla del prompt).

### Reglas del canal que siguen mandando
- Datos verificados (fuente primaria o 2 medios), nada inventado, sin spoilers de misiones.
- Solo imágenes y clips oficiales de Rockstar; nunca partidas ni vídeos de otros canales; sin el logo oficial de GTA VI.
- Fuentes solo en la descripción; aviso "Unofficial fan-made channel. Not affiliated with Rockstar Games or Take-Two Interactive.".

### Prompt de miniatura para ChatGPT (después del vídeo completo)
Se entrega en inglés, listo para copiar, con: formato 1280×720 (16:9); una idea en 1 segundo; 1 sujeto principal grande + 2-4 palabras ENORMES con contraste (paleta del canal: #080810, #8B35FF, #FF2E8C, #FFCE28); emoción o tensión clara; fondo de Vice City/Leonida; **sin el logo oficial de GTA VI ni marcas de Rockstar**; sin texto pequeño; que prometa lo que el vídeo cumple (nada engañoso).
⚠️ ChatGPT puede negarse a dibujar personajes con copyright (Jason, Lucia): el prompt describe personajes y lugares "inspirados" o se pide usar como base una captura oficial que Adam suba.
