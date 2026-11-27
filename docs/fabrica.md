# Fábrica automática — Ford (jefe de fábrica)

Creado el 27/11/2026 a petición de Adam («quiero más, mucho más»). Objetivo: que salgan **2 Shorts al día** sin esperar a que nadie pulse «Producir».
Motivo (datos del canal): con Shorts nuevos el canal sube ~+2.000 visualizaciones cada 6 h; del 25 al 27/11, sin Shorts nuevos, bajó a +100.

## Cuándo
Dos veces al día, a las **14:17 y 20:17 hora de Madrid** (antes de la franja de subida de 00:00-03:00 en España). Tarea programada «Fábrica automática (Ford)».

## Qué hace en cada turno
1. **Antes de nada, mira la cola:** si en «Listo para subir» (`estado/publicar`) ya hay **4 o más** Shorts sin subir, NO produce (Adam no da abasto): anota «cola llena» en `actividad` y termina.
2. **Elige** entre los preproducidos (`shorts/*/investigacion.md` con «Estado: preproducción») el de **mayor 🔥** en `estado/tendencias`, que no repita el formato del último Short producido. Si no hay ninguno, toma la idea ✅ del banco con más 🔥 que no tenga carpeta y la preproduce primero.
3. **Produce** con `docs/produccion-short.md` (pasos 1-8) SIN cambiar sus reglas: historia con giro, 40-60 s, voz **Fenrir gratis** (`shorts/voz_gratis.py`, objetivo ~46 s), nunca créditos de Higgsfield, mayoría de clips oficiales, golpes con giro, examen APTO (0 ✗) y −14 LUFS.
4. **Títulos (La Bestia):** 3 títulos con lo aprendido de los virales (personaje, 4-8 palabras, 1-2 MAYÚSCULAS, emoji, «What happens if…», aviso o contraste). Nunca un título que el vídeo no cumpla.
5. **Entrega:** «Listo para subir» (vista previa como asset y `estado/publicar` conservando los `video` existentes), `estado/equipo`, una entrada en `actividad` con quien = ["ford", …], SendUserFile al móvil, banco 🎬, registro de cambios, commit y push.
6. **Mensaje para Adam:** 2-3 líneas en español con el título, la duración, la nota del examen y el recordatorio de subirlo; los textos de subida están en la oficina.

## Reglas
- No produce si la verificación de datos falla: prefiere saltar un turno a inventar.
- Si llega un encargo de Adam mientras trabaja, el encargo va primero.
- Nunca sube nada a YouTube (lo sube Adam) y nunca pide la contraseña.
