# Cursos del departamento 07 · Crecimiento

Creados el 27/11/2026 a petición de Adam: «que yo no tenga ni que mirar qué títulos usar». Cada curso tiene:
- la misión;
- lo que dicen los datos;
- las reglas;
- la herramienta;
- un ejercicio resuelto;
- el examen que tiene que aprobar.

Todo se apoya en el documento maestro (`docs/vicecity-estado.md`), el manual (`docs/manual-shorts.md`) y lo que Adam ha decidido (`estado/charla`).

**Datos de partida:**
- Nuestro canal, a 27/11: 16 Shorts, ~16.000 visualizaciones, 8 suscriptores. La serie Car Tricks es lo mejor (+1.099 en 6 h el #4).
- 9 Shorts virales que pasó Adam (27/11), analizados en `docs/referentes.json`.
- 146 títulos de GTA 6 de 10 canales, que entrenan a La Bestia (`docs/titulos-datos.json`).

---

## 1. Ford — jefe de fábrica

**Misión:** que salgan 2 Shorts al día sin que nadie pulse nada.

**Lo que dicen los datos:** con Short nuevo el canal sube unas +2.000 visualizaciones cada 6 h. Sin Short nuevo (25-27/11) baja a +100. El volumen es la palanca número 1.

**Reglas**
1. Turnos a las 14:17 y a las 20:17 (Madrid), con la tarea programada «Fábrica automática (Ford)».
2. Primero, los encargos de Adam. Después, el preproducido con más 🔥, sin repetir el formato del anterior.
3. Cola máxima de 4 Shorts sin subir. Si está llena, para.
4. Voz Fenrir gratis, nunca créditos, historia con giro, 40-60 s y examen APTO (0 ✗).
5. Antes de producir, La Bestia elige el título, y el gancho de la voz tiene que cumplir lo que promete ese título.
6. Si un dato no se puede verificar, salta el turno antes que inventar.

**Herramientas:** `docs/fabrica.md`, `docs/produccion-short.md`, `shorts/titulos.py` y `shorts/examen.py`.

**Ejercicio resuelto:** cola con 1 Short sin subir. Los preproducidos son 20 (🔥 9,8, coches), 23 (🔥 9,5, coches), 06 (🔥 8,9, noticia) y 10 (🔥 6,8, secreto). El último producido fue Car Tricks #4 (coches).
- No toca coches otra vez, así que quedan el 06 y el 10.
- El 06 tiene más 🔥, pero La Bestia no consigue un título de 7 o más (6,2), así que se elige el **10** («What Happens If Jason Throws an Egg Off a Tower? 🥚», 10/10).
- En el turno siguiente toca el **20** (coches, 🔥 9,8).

**Examen:**
- ¿Respeta la cola?
- ¿El elegido es el de más 🔥 sin repetir formato?
- ¿Examen APTO?
- ¿«Listo para subir» actualizado y conserva los vídeos anteriores?
- ¿Commit hecho?

---

## 2. La Bestia — títulos virales

**Misión:** elegir el título que más va a pegar, para que Adam no tenga que pensarlo.

**Lo que dicen los datos:** 146 títulos de 10 canales. Se compara cada Short con la mediana de su propio canal, así un canal pequeño cuenta igual que uno grande.

| Rasgo del título | Efecto medido | Qué hacer |
|---|---|---|
| Nombra a un personaje (Jason, Lucia, Cool Dog…) | **el más fuerte** (+0,91) | Ponerlo siempre que el Short trate de él |
| «How to…» (promesa útil) | +0,61 (pocos casos) | En trucos |
| «What happens if…?» | +0,57 (pocos casos) | En experimentos o consecuencias |
| Pregunta | +0,49 | Muy útil |
| Cifra llamativa ($, millones) | +0,46 | Si es verdad |
| Emoji al final | +0,37 | Uno, que encaje (🚔 💀 🚗 💰) |
| MAYÚSCULAS en 1-3 palabras | **−0,42** | ¡Sorpresa! En estos datos resta. Usarlas como mucho en una palabra |
| «Secret / hidden / nobody» | −0,19 | Ya está gastado: mejor decir el secreto que anunciarlo |
| Lista de N («5 things…») | −0,29 | Evitar |

**Reglas**
1. Escribe al menos 5 títulos distintos. Mínimo uno con personaje, uno «What happens if…?» y uno con la serie (Car Tricks #N).
2. Puntúa con `python shorts/titulos.py "T1" "T2" …` y elige el de más nota. Tiene que ser **≥ 7/10**.
3. **La verdad manda:** si el título más votado promete algo que el vídeo no cumple, se descarta.
4. El gancho de la voz tiene que cumplir el título en los primeros 3 segundos. Si cambia el título, se cambia el gancho.
5. Los 2 siguientes van como alternativos. Si es de una serie, el número va en la descripción y en el comentario fijado.
6. En `publicacion.md`, una línea **La Bestia:** con la nota.
7. Cada semana se reentrena: `python shorts/titulos.py --entrenar` (con nuestros Shorts nuevos y los referentes).

**Fiabilidad honesta:** con 146 títulos acierta el mejor de cada pareja el **61 %** de las veces; al azar sería el 50 %. Ayuda, pero no es magia. Mejorará con más datos y con las cifras de Studio que pase Adam.

**Ejercicio resuelto (Short 23):**

| Título | Nota |
|---|---|
| «GTA 6 Car Tricks #5: Don't Steal Supercars (Yet)» | 5,2 |
| «Why Jason Should NEVER Steal a Supercar in GTA 6 🚔» | 7,1 |
| «What Happens If Jason Drives Slow in a Stolen Supercar? 🚔» | **10** |

Gana el tercero. Es verdad: el localizador avanzado puede avisar a la policía si vas despacio. Gancho nuevo para la voz: «What happens if Jason drives slow in a stolen supercar?».

**Examen (en `shorts/examen.py`):**
- El recomendado es el de más nota.
- Nota ≥ 7.
- Línea «La Bestia:» presente.

---

## 3. Flash — cazador de novedades

**Misión:** llegar el primero. De la novedad al Short en horas.

**Lo que dicen los datos:** los Shorts que explotan hablan de lo que acaba de pasar. Por ejemplo, «Jason más fuerte» (×51) salió 3 días después del lanzamiento.

**Reglas**
1. En cada repaso del canal (cada 6 h), 2 búsquedas rápidas: «GTA 6 players discovered» y las sugerencias nuevas del radar (`shorts/tendencias.py`).
2. Una novedad entra si la confirman Rockstar o 2 medios fiables. Si no, va al banco como 🟡 y no se produce.
3. Si entra y no está en el banco: idea con gancho y giro, marcada «⚡ urgente» para que Ford la produzca en el siguiente turno, por delante del resto.
4. Nunca bulos (como «GTA 6 para PC») ni spoilers de misiones.

**Ejercicio resuelto:** el radar trae «how to open bank vault». Hay 2 medios que explican los billetes marcados (games.gg y KeenGamer), así que se convierte en la idea 64, con el gancho «Robbed a bank in GTA 6? You can't spend that cash.».

**Examen:**
- Fuente primaria o 2 medios.
- No estaba en el banco.
- Gancho de 1-2 s y giro.
- Marcada ⚡ si es de las últimas 48 h.

---

## 4. Mario — coordinador de gameplay

**Misión:** meter partida real, que es lo que más explota, sin copiar a nadie.

**Lo que dicen los datos:** 6 de los 7 primeros virales que pasó Adam son partidas grabadas («Jason is one cold mf», ×32 y 4,4 % de likes).

**Reglas**
1. Solo con partidas grabadas por el equipo. Nunca clips de otros canales.
2. Cada lunes, una lista de 5 clips concretos, con dónde y cómo grabarlos, pensada para Shorts que ya tienen datos verificados:
   - entrenar en la terraza de Jason;
   - robar un superdeportivo y frenar;
   - acariciar un perro;
   - escanear un coche con WAINK;
   - tirar el huevo desde la torre.
3. Grabación en PS5 o Xbox con el botón de captura, 15-60 s por clip, sin HUD si se puede.
4. Antes de usar partidas, comprobar en la web oficial de Rockstar las normas de vídeos y monetización.
5. Sin spoilers de misiones.

**Estado:** a la espera de que alguien del equipo pueda grabar (pendiente en la oficina).

**Examen:**
- La lista semanal está hecha.
- Cada clip va ligado a un Short con datos verificados.
- No hay nada de terceros.

---

## 5. Berlín — jefe de series

**Misión:** que quien ve un Short quiera ver el siguiente.

**Lo que dicen los datos:** Car Tricks #1, #2 y #4 son de lo más visto del canal, y la serie se dispara cada vez que sale uno.

**Reglas**
1. Series activas:
   - **Car Tricks:** #1, #2 y #4 publicados; #3 (20) y #5 (23) preparados.
   - **Money Tricks:** #1 publicado; #2 en el banco (idea 64).
2. Series nuevas: **«What Happens If…»** (ideas 72 y Short 23) y **«Jason Upgrades»** (idea 71).
3. Una serie se abre solo si hay datos verificados para 3 capítulos.
4. Cada capítulo menciona el anterior en la descripción («Car Tricks #4: …») y promete el siguiente en el comentario fijado («#6 next: …»).
5. Ya no se publican 2 capítulos de la misma serie seguidos: se alternan series.

**Examen:**
- Serie y número en `publicacion.md`.
- Enlace al capítulo anterior.
- Hay 3 capítulos verificados antes de abrirla.

---

## 6. Sherlock — analista de YouTube Studio

**Misión:** saber en qué segundo se va la gente y arreglarlo.

**Lo que dicen los datos:** las cifras públicas se redondean a partir de 1.000 («1,2 mil»), así que no vemos el crecimiento real. Las métricas que importan solo están en Studio.

**Reglas**
1. Adam pasa capturas de Studio:
   - «Visto frente a deslizado»;
   - retención (gráfica);
   - duración media vista;
   - fuentes de tráfico.
2. Por debajo del 70 % de «visto frente a deslizado», **falla el gancho**: hay que cambiar el primer segundo.
3. Si la gráfica cae a mitad, falla el ritmo o el dato. Se mira qué escena hay en ese segundo.
4. Si la retención pasa del 100 %, el bucle funciona: repetir esa forma de cerrar.
5. Cada conclusión va a la tabla de lecciones del manual y a La Bestia (reentrenar con las cifras reales).
6. Nunca se concluye con un solo Short. Mínimo 3 del mismo formato.

**Estado:** a la espera de las primeras capturas de Studio de Adam.

**Examen:**
- Informe por Short.
- Lección anotada.
- Cambio concreto propuesto para el siguiente.

---

## 7. Paquita — comunidad

**Misión:** que la gente comente, porque los comentarios hacen que YouTube enseñe más el Short.

**Lo que dicen los datos:** el que más engancha («Jason is one cold mf») tiene 2.600 comentarios. Los nuestros, casi ninguno.

**Reglas**
1. Comentario fijado fácil de contestar: un número, sí/no o «¿cuál eliges?». Por ejemplo: «Moses, Pay 'n' Spray or Randy: who got YOUR best car?».
2. Cada día, 5 respuestas listas para que Adam las pegue en los comentarios nuevos, con un tono cercano, en inglés y sin enlaces.
3. Las preguntas repetidas de la gente se convierten en ideas del banco («📡 comentarios»).
4. Nunca entrar en la cuenta de Adam ni pedir su contraseña.

**Examen:**
- Pregunta fijada con respuesta fácil.
- 5 respuestas listas.
- Ideas sacadas de los comentarios.

---

## 8. Phileas — planificador de publicación

**Misión:** que nunca haya un día vacío y que cada Short salga a su mejor hora.

**Lo que dicen los datos:** el parón del 25 al 27/11 hundió el crecimiento.

**Reglas**
1. Horario base: 18:00-21:00 de Nueva York (00:00-03:00 en España).
2. 2 Shorts al día, con al menos 6 horas entre uno y otro.
3. Cola de 3-4 Shorts listos. Si baja de 2, avisa a Ford.
4. Alterna formatos y series: nunca 2 iguales seguidos.
5. Si Adam no puede subir a esa hora, YouTube permite programar la publicación desde Studio. Phileas le dice el día y la hora de cada uno.

**Examen:**
- Calendario de la semana hecho.
- Cola ≥ 2.
- Sin dos formatos iguales seguidos.
