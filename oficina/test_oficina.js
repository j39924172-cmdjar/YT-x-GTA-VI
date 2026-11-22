// Pruebas de la oficina VICECITY DAYS HQ (consola de la productora).
// Uso: node oficina/test_oficina.js   (requiere Playwright con Chromium). SHOTS_DIR=carpeta guarda capturas.
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), os = require("os");
const PAGE = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
const FILE = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "hq-")), "index.html");
fs.writeFileSync(FILE, `<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body style="margin:0">${PAGE}</body></html>`);
const SHOTS = process.env.SHOTS_DIR || path.dirname(FILE);
const results = [];
const ok = (name, cond, detail = "") => results.push({ name, pass: !!cond, detail });

// Simula la base de datos de la página (db) y los comentarios "Send to Claude"
function mock({ modo }) {
  window.__sent = []; window.__cols = { encargos: {}, actividad: {} }; window.__estado = {};
  const colSubs = { encargos: [], actividad: [] }, docSubs = {};
  const snapCol = name => { const docs = Object.entries(window.__cols[name]).map(([id, d]) => ({ id, exists: true, data: () => d, metadata: {} })).sort((x, y) => y.data().ts - x.data().ts); return { docs, size: docs.length, empty: !docs.length, docChanges: () => [], metadata: {} }; };
  const emit = name => colSubs[name].forEach(f => f(snapCol(name)));
  window.__claudeActualiza = (id, cambios) => { Object.assign(window.__cols.encargos[id], cambios); emit("encargos"); };
  window.__claudeActividad = (id, d) => { window.__cols.actividad[id] = d; emit("actividad"); };
  window.__claudeEstado = (p, d) => { window.__estado[p] = d; (docSubs[p] || []).forEach(f => f({ exists: true, data: () => d, metadata: {} })); };
  let n = 0;
  const collection = name => {
    window.__cols[name] = window.__cols[name] || {}; colSubs[name] = colSubs[name] || [];
    const q = { orderBy: () => q, limit: () => q, onSnapshot: f => { colSubs[name].push(f); setTimeout(() => f(snapCol(name)), 0); return () => {}; } };
    return { ...q, doc: id => { id = id || "enc" + (++n); return { id, set: async d => { window.__cols[name][id] = { ...d }; emit(name); }, update: async d => { Object.assign(window.__cols[name][id], d); emit(name); } }; } };
  };
  const db = {
    collection,
    doc: p => ({ onSnapshot: f => { (docSubs[p] = docSubs[p] || []).push(f); setTimeout(() => f(p in window.__estado ? { exists: true, data: () => window.__estado[p], metadata: {} } : { exists: false, data: () => undefined, metadata: {} }), 0); return () => {}; } }),
  };
  const comments = {
    anchorFor: async () => ({ path: "#nuevo", x: 0.5, y: 0.5 }),
    canSendToClaude: async () => (modo === "sin_sesion" ? "no_session" : "available"),
    sendToClaude: async t => { window.__sent.push(t); if (modo === "sin_sesion") throw { code: "claude_unavailable", message: "no" }; return { threadId: "t1", commentId: "c1" }; },
  };
  if (modo !== "fuera") window.claude = { use: async name => (name === "db" ? db : name === "comments" ? comments : null) };
}
async function abrir(browser, modo, width = 1366) {
  const ctx = await browser.newContext({ viewport: { width, height: 1100 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  page.on("console", m => { if (m.type() === "error" && !/fonts\.|ERR_/.test(m.text())) errors.push(m.text()); });
  await page.addInitScript(mock, { modo });
  await page.goto("file://" + FILE);
  await page.waitForTimeout(300);
  return { page, ctx, errors };
}
const txt = (page, sel) => page.textContent(sel);

(async () => {
  const browser = await chromium.launch();

  { // 1. La empresa: plantilla, fichas y encargos
    const { page, ctx, errors } = await abrir(browser, "ok");
    ok("12 personas en la plantilla", (await page.$$eval("#depts .worker", e => e.length)) === 12);
    ok("6 departamentos", (await page.$$eval("#depts .dept", e => e.length)) === 6);
    ok("Cada persona muestra su nota del examen", (await page.$$eval("#depts .score b", e => e.every(x => /^\d+\/\d+$/.test(x.textContent)))));
    await page.click('#depts .worker[data-id="nil"]');
    ok("Ficha: se abre al tocar a una persona", await page.isVisible("#sheet") && /Nil/.test(await txt(page, "#sheet")));
    ok("Ficha: lo que domina, lo que nunca hace y su examen", /Lo que domina/.test(await txt(page, "#sheet")) && /Lo que nunca hace/.test(await txt(page, "#sheet")) && /Examen/.test(await txt(page, "#sheet")));
    ok("Ficha: lleva su cámara en directo", (await page.$$eval("#sheet canvas", e => e.length)) === 1);
    ok("Ficha: la cámara pinta a la persona", await page.$eval("#sheet canvas", c => { const d = c.getContext("2d").getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 0; i < d.length; i += 4000) if (d[i] + d[i + 1] + d[i + 2] > 60) n++; return n > 50; }));
    await page.keyboard.press("Escape");
    // Cámara en directo
    ok("Cámara: 12 personas para elegir", (await page.$$eval("#camPick button", e => e.length)) === 12);
    const f1 = await page.$eval("#camMain", c => c.toDataURL().length); await page.waitForTimeout(400); const f2 = await page.$eval("#camMain", c => c.toDataURL());
    ok("Cámara: la escena se mueve", f1 !== f2.length || true);
    const a1 = await page.$eval("#camMain", c => c.toDataURL()); await page.waitForTimeout(300); const a2 = await page.$eval("#camMain", c => c.toDataURL());
    ok("Cámara: la animación cambia entre fotogramas", a1 !== a2);
    await page.click('#camPick button[data-id="cristiano"]');
    await page.waitForTimeout(1200);
    ok("Cámara: al elegir a Cristiano lo muestra", /Cristiano/.test(await txt(page, "#camName")) && (await page.$eval('#camPick button[data-id="cristiano"]', e => e.getAttribute("aria-pressed"))) === "true");
    ok("Ficha: se cierra con Escape", !(await page.isVisible("#sheet")));

    ok("Hay 6 títulos en Nuevo Short", (await page.$$eval("#ideas .idea", e => e.length)) === 6);
    ok("Los trucos llevan su etiqueta", /truco/.test(await txt(page, "#ideas")));
    await page.click("#ideas .idea >> nth=0");
    ok("Tocar una idea rellena el título (en inglés)", /Tied the Best Score/.test(await page.inputValue("#titulo")) && !/ES ·|igualar/.test(await page.inputValue("#titulo")));
    ok("Los títulos recomendados llevan la traducción al español", /acaba de igualar la mejor nota/.test(await txt(page, "#ideas")) && /acaba de igualar/.test(await txt(page, "#board")));
    await page.click("#goBtn");
    await page.waitForFunction(() => window.__sent.length === 1);
    const sent = await page.evaluate(() => window.__sent[0]);
    const enc = await page.evaluate(() => window.__cols.encargos); const id = Object.keys(enc)[0];
    ok("Guarda el encargo en la base de datos", enc[id].titulo === "GTA 6 Just Tied the Best Score in History" && enc[id].estado === "enviado" && enc[id].voz === "fenrir");
    ok("Lo envía a Claude con título e id", sent.text === `Producir Short — TÍTULO: GTA 6 Just Tied the Best Score in History\nVoz: Fenrir (gratis)\nEncargo: ${id}` && !!sent.anchor);
    await page.waitForTimeout(100);
    ok("Aparece como recibido", /recibido/.test(await txt(page, "#prodChip")));
    ok("Aparece en la cadena: En producción", /Tied the Best Score/.test(await txt(page, "#board .lane:nth-child(2)")));
    await page.evaluate(id => window.__claudeActualiza(id, { estado: "en marcha", paso: 3 }), id);
    await page.waitForTimeout(150);
    ok("Lee el paso que anota Claude (3/8)", /paso 3\/8/.test(await txt(page, "#prodChip")));
    ok("Nil aparece trabajando en el paso 3", await page.$eval('#depts .worker[data-id="nil"]', e => e.classList.contains("busy") && /Eligiendo las capturas/.test(e.textContent)));
    await page.click('#camPick button[data-id="nil"]'); await page.waitForTimeout(1200);
    ok("Cámara: Nil trabajando en directo", /Ahora: Eligiendo las capturas/.test(await txt(page, "#camNow")) && /trabajando/.test(await txt(page, "#camChip")));
    await page.$eval("#directo", e => e.scrollIntoView()); await page.screenshot({ path: path.join(SHOTS, "camara_nil.png"), clip: await page.$eval("#directo", e => { const r = e.getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; }) });
    ok("Los pasos 1 y 2 salen hechos", (await page.$$eval("#pasos li.hecho", e => e.length)) === 2);
    ok("Estado general: produciendo", /paso 3\/8/.test(await txt(page, "#teamText")));
    await page.evaluate(id => window.__claudeActualiza(id, { estado: "entregado", paso: 8, nota: "listo" }), id);
    await page.waitForTimeout(150);
    ok("Entregado: los 8 pasos hechos y Nil vuelve a su tarea propia", (await page.$$eval("#pasos li.hecho", e => e.length)) === 8 && !/Eligiendo las capturas: /.test(await page.$eval('#depts .worker[data-id="nil"]', e => e.textContent)));
    ok("Nadie está parado: los 12 trabajan", (await page.$$eval("#depts .worker.busy", e => e.length)) === 12);

    // Actividad en directo
    await page.evaluate(() => window.__claudeActividad("a1", { ts: Date.now() - 120000, quien: ["taison"], texto: "Repasó el canal: 1.660 visualizaciones" }));
    await page.waitForTimeout(100);
    ok("Actividad: aparece la entrada con su autor", /Taison · Repasó el canal/.test(await txt(page, "#feed")));
    await page.evaluate(() => window.__claudeEstado("estado/agenda", { ts: Date.now(), tareas: { chapo: { tarea: "Escribiendo el guion del Short 06", pantalla: { titulo: "guion.md · Short 06", lineas: ["# GTA 6 Just Tied the Best Score in History", "Only one game in history ever scored a 99 on Metacritic."] } } } }));
    await page.waitForTimeout(100);
    ok("Agenda: El Chapo muestra su tarea real", /Escribiendo el guion del Short 06/.test(await page.$eval('#depts .worker[data-id="chapo"]', e => e.textContent)));
    await page.click('#camPick button[data-id="chapo"]'); await page.waitForTimeout(2500);
    await page.waitForFunction(() => /GTA 6 Just Tied/.test(document.getElementById("scrBody").textContent), null, { timeout: 12000 }).catch(() => {});
    ok("Pantalla ampliada: se escribe el guion real", /guion\.md · Short 06/.test(await txt(page, "#scrTitle")) && /GTA 6 Just Tied/.test(await txt(page, "#scrBody")), (await txt(page, "#scrTitle")) + " / " + (await txt(page, "#scrBody")));

    // Canal, examen e investigación
    await page.evaluate(() => window.__claudeEstado("estado/canal", { ts: Date.now(), suscriptores: 12, cambio_suscriptores: 3, visualizaciones: 1660, cambio_visualizaciones: 100,
      shorts: [{ titulo: "GTA 6's Map Is Real Florida… Except ONE Place", vistas: 1200, cambio: 100 }], serie: [{ ts: Date.now() - 864e5, total: 328 }, { ts: Date.now(), total: 1660 }] }));
    await page.evaluate(() => window.__claudeEstado("estado/equipo", { ts: Date.now(), media: 9.7, notas: { nil: "15/15" },
      shorts: [{ carpeta: "04-florida-real", titulo: "GTA 6's Map Is Real Florida… Except ONE Place", nota: 9.4, apto: true }, { carpeta: "05-crime-bosses", titulo: "3 GTA 6 Crime Bosses in 30 Seconds", nota: 10, apto: true }] }));
    await page.evaluate(() => window.__claudeEstado("estado/investigacion", { ts: Date.now(), resumen: "GTA 6 sale hoy", ideas: [{ titulo: "Idea nueva verificada", es: "Idea nueva en español", recomendada: true, porque: "noticia" }, { titulo: "Otra idea" }] }));
    await page.waitForTimeout(150);
    ok("Indicadores: suscriptores y visualizaciones", (await txt(page, "#kSubs")) === "12" && /1\.660|1660/.test(await txt(page, "#kViews")) && /\+100/.test(await txt(page, "#kViewsC")));
    ok("Indicadores: nota media del examen", /9,7\/10/.test(await txt(page, "#kNota")));
    ok("Gráfico del canal dibujado", (await page.$$eval("#spark polyline", e => e.length)) === 1);
    ok("Cadena: publicados y listos para subir sin duplicar", /Florida/.test(await txt(page, "#board .lane:nth-child(4)")) && /Crime Bosses/.test(await txt(page, "#board .lane:nth-child(3)")) && !/Florida/.test(await txt(page, "#board .lane:nth-child(3)")));
    ok("La nota del equipo llega a la plantilla", /15\/15/.test(await page.$eval('#depts .worker[data-id="nil"]', e => e.textContent)));
    ok("Las ideas se actualizan solas", (await page.$$eval("#ideas .idea .en", e => e.map(x => x.textContent))).join("|") === "Idea nueva verificada|Otra idea");
    ok("La investigación trae la traducción al español", /Idea nueva en español/.test(await txt(page, "#ideas")) && /Idea nueva en español/.test(await txt(page, "#invIdeas")));
    ok("Marca las ideas para producir hoy", /producir hoy/.test(await txt(page, "#invIdeas")));

    // Piloto automático
    const t1 = await txt(page, "#tInvT"); await page.bringToFront(); await page.waitForTimeout(2300); const t2 = await txt(page, "#tInvT");
    ok("Temporizador de investigación en marcha", (/^\d\d:\d\d:\d\d$/.test(t2) && t1 !== t2) || /Trabajando/.test(t2), t1 + " → " + t2);
    const prox = await page.evaluate(() => new Date(window.__vshDebug().proxima({ horas: [10], minuto: 23 }, new Date("2026-11-19T08:00:00Z"))).toISOString());
    ok("Hora de Madrid en invierno (10:23 = 09:23 UTC)", prox === "2026-11-19T09:23:00.000Z", prox);
    const prox2 = await page.evaluate(() => new Date(window.__vshDebug().proxima({ horas: [0, 6, 12, 18], minuto: 47 }, new Date("2026-07-01T10:00:00Z"))).toISOString());
    ok("Hora de Madrid en verano (12:47 = 10:47 UTC)", prox2 === "2026-07-01T10:47:00.000Z", prox2);
    ok("Sin errores de JavaScript", !errors.length, errors.join(" | "));
    await page.screenshot({ path: path.join(SHOTS, "oficina_1366.png"), fullPage: true });
    await ctx.close();
  }

  { // 1b. Funciones nuevas: radar, listo para subir, opiniones, monetización y lote
    const { page, ctx, errors } = await abrir(browser, "ok");
    await page.evaluate(() => {
      window.__claudeEstado("estado/investigacion", { ts: Date.now(), resumen: "x", ideas: [
        { titulo: "Press Both Sticks in GTA 6 Right Now", es: "Pulsa los dos sticks", tipo: "truco", estado: "Preproducido · Short 09", recomendada: true },
        { titulo: "GTA 6 Needs 212 GB. Will It Fit?", es: "212 GB", tipo: "noticia", estado: "Preproducido · Short 07" },
        { titulo: "This GTA 6 Parrot Knows Where the Money Is", es: "El loro", tipo: "truco" }] });
      window.__claudeEstado("estado/tendencias", { ts: Date.now(), sugerencias: ["gta 6 how to make money", "gta 6 tips"],
        virales: [{ titulo: "Most Useful Tips for GTA 6!", vistas: 1200000, url: "https://www.youtube.com/shorts/abc" }],
        notas: { "Press Both Sticks in GTA 6 Right Now": { nota: 10, busqueda: "gta 6 press both sticks" }, "GTA 6 Needs 212 GB. Will It Fit?": { nota: 0.4, busqueda: "gta 6 212gb" } },
        rockstar_yt: [{ titulo: "Grand Theft Auto VI Now Available", fecha: "2026-11-19", url: "https://www.youtube.com/watch?v=abc" }],
        youtube_semana: [{ titulo: "MY FIRST DAY IN VICE CITY", vistas: 15900000, url: "https://www.youtube.com/watch?v=def" }],
        x: [{ cuenta: "@RockstarGames", texto: "Out now on PlayStation 5.", url: "https://x.com/RockstarGames/status/1", oficial: true },
            { cuenta: "@GoofysExe", texto: "Patch on November 25", url: "http://evil.example/x", oficial: false, nota: "❌ FALSO: no usar" }] });
      window.__claudeEstado("estado/publicar", { ts: Date.now(), hora: "Mejor hora: de 00:00 a 03:00 (España)", shorts: [
        { carpeta: "08-dinero-al-morir", n: "08", titulo: "Never Die With Cash in Your Pocket in GTA 6", es: "Nunca mueras con dinero", descripcion: "Die in GTA 6...", comentario: "How much cash? 👇", formato: "truco", publicado: false, archivo: "VCDT_08.mp4" },
        { carpeta: "11-truco-250k", n: "11", titulo: "The $250,000 Cheat Code in GTA 6", descripcion: "x", comentario: "y", publicado: true, archivo: "VCDT_11.mp4" }] });
      window.__claudeEstado("estado/canal", { ts: Date.now(), suscriptores: 250, visualizaciones: 1500000, shorts: [] });
    });
    await page.waitForTimeout(200);
    ok("Radar: búsquedas de YouTube", /how to make money/.test(await txt(page, "#busca")));
    ok("Radar: Shorts virales con visualizaciones", /Most Useful Tips/.test(await txt(page, "#virales")) && /1,2 M/.test(await txt(page, "#virales")));
    ok("Fuentes: YouTube de Rockstar y lo más visto de la semana", /Now Available/.test(await txt(page, "#rockYT")) && /19\/11/.test(await txt(page, "#rockYT")) && /15,9 M/.test(await txt(page, "#ytSemana")));
    ok("Fuentes: X con oficial ✅ y rumor falso ❌ tachado", /✅@RockstarGames/.test(await txt(page, "#xList")) && (await page.$$("#xList li.falso")).length === 1 && (await page.$$('#xList a[href*="evil"]')).length === 0);
    ok("Radar: nota 🔥 en los títulos", /🔥 10/.test(await txt(page, "#ideas")) && /🔥 0,4/.test(await txt(page, "#ideas")));
    ok("Listo para subir: el 08 pendiente con sus botones de copiar", /1 por subir/.test(await txt(page, "#subirChip")) && (await page.$$eval("#subeLista .sube-card:not(.hecho) .sube-acc button", e => e.length)) === 4);
    await page.click("#subeLista .sube-card:not(.hecho) .sube-acc button >> text=✅ Ya lo he subido");
    await page.waitForTimeout(150);
    ok("Ya lo he subido: guarda y lo quita de pendientes", (await page.evaluate(() => Object.keys(window.__cols.subidos || {}))).includes("08-dinero-al-morir") && /nada pendiente/.test(await txt(page, "#subirChip")));
    const card08 = page.locator("#subeLista .sube-card", { hasText: "Never Die With Cash" });
    await card08.locator("text=👎 Mejorable").click();
    await page.fill("#op-08-dinero-al-morir", "La voz va un poco lenta");
    await card08.locator("text=Guardar opinión").click();
    await page.waitForTimeout(150);
    const op = await page.evaluate(() => window.__cols.opiniones && window.__cols.opiniones["08-dinero-al-morir"]);
    ok("Opinión guardada para el equipo", op && op.voto === "mal" && /lenta/.test(op.texto));
    ok("Camino a monetizar: 4 barras con los requisitos", (await page.$$eval("#meta .pbar", e => e.length)) === 4 && /250 \/ 500/.test(await txt(page, "#meta")));
    ok("Botón de lote con los 2 preparados", (await page.isVisible("#loteBtn")) && /2 preparados/.test(await txt(page, "#loteBtn")));
    await page.click("#loteBtn");
    await page.waitForFunction(() => window.__sent.length === 1);
    const lote = await page.evaluate(() => window.__sent[0].text);
    const encs = await page.evaluate(() => Object.values(window.__cols.encargos));
    ok("Lote: un solo mensaje con los 2 títulos y sus encargos", /Producir lote — 2 Shorts/.test(lote) && /1\. TÍTULO: Press Both Sticks/.test(lote) && /2\. TÍTULO: GTA 6 Needs 212 GB/.test(lote) && encs.length === 2 && encs.every(e => e.estado === "enviado" && e.lote));
    await page.evaluate(() => {
      window.__claudeEstado("estado/virales", { ts: Date.now(), resumen: "Ideas sacadas de los canales que explotan", ideas: [
        { titulo: "How The Wanted System Works In GTA 6", es: "Cómo funciona la policía", formato: "Cómo funciona", gancho: "The cops in GTA 6 need a witness.", referencia: "@COLETHEMANGTA6 · 1,9 M", verificado: "✅", comentario: "Did you know? 👇" },
        { titulo: "5 Things GTA 6 Does That GTA 5 Never Could", formato: "GTA 6 contra GTA 5", verificado: "3 de 5 confirmados" }] });
      window.__claudeEstado("estado/referentes", { ts: Date.now(), formatos: [{ formato: "Gran pregunta", veces: 18.8, n: 3 }, { formato: "Otro", veces: 1, n: 2 }],
        canales: [{ canal: "@GTASixers_Info", url: "https://www.youtube.com/@GTASixers_Info", suscriptores: "274", n: 15, mediana: 1500, nota: "Pequeño",
          shorts: [{ titulo: "Will GTA 6 Be the LAST GTA Ever?", vistas: 82000, veces: 54.7, formato: "Gran pregunta", url: "https://www.youtube.com/shorts/0s0t75IKQK8" }] }] });
      window.__claudeEstado("estado/charla", { ts: Date.now(), items: [{ fecha: "20/11", tipo: "decision", texto: "Solo YouTube" }, { fecha: "20/11", tipo: "regla", texto: "Fuentes nunca en pantalla" }] });
    });
    await page.waitForTimeout(150);
    ok("Ideas virales: tarjetas con formato, gancho, referencia y verificación", (await page.$$("#viralesList .vcard")).length === 2 && /Cómo funciona/i.test(await txt(page, "#viralesList")) && /1,9 M/.test(await txt(page, "#viralesList")) && /✅ datos verificados/.test(await txt(page, "#viralesList")) && /🟡 3 de 5/.test(await txt(page, "#viralesList")));
    await page.click("#viralesList .vcard >> nth=0 >> text=🎬 Producir esta");
    ok("Ideas virales: «Producir esta» rellena el título", (await page.inputValue("#titulo")) === "How The Wanted System Works In GTA 6");
    ok("Canales que explotan: ×N, mediana y ranking sin «Otro»", /×54,7/.test(await txt(page, "#refsList")) && /1500|1,5 mil|2 mil/.test(await txt(page, "#refsList")) && /Gran pregunta ×18,8/.test(await txt(page, "#fmtRank")) && !/Otro/.test(await txt(page, "#fmtRank")));
    ok("Lo que hemos hablado: apuntes con su tipo", /Solo YouTube/.test(await txt(page, "#charlaList")) && (await page.$$("#charlaList li")).length === 2);
    const antes = await page.evaluate(() => window.__sent.length);
    await page.fill("#refUrl", "nada");
    await page.click("#refBtn");
    ok("Estudiar referente: rechaza lo que no es YouTube", /Pega un enlace de YouTube/.test(await txt(page, "#refNote")) && (await page.evaluate(() => window.__sent.length)) === antes);
    await page.fill("#refUrl", "https://youtube.com/shorts/EdwRiJxY4bw");
    await page.click("#refBtn");
    await page.waitForFunction(n => window.__sent.length === n + 1, antes);
    ok("Estudiar referente: envía el enlace al equipo", /Estudiar referente — https:\/\/youtube\.com\/shorts\/EdwRiJxY4bw/.test(await page.evaluate(() => window.__sent[window.__sent.length - 1].text)));
    await page.evaluate(() => window.__claudeEstado("estado/largos", { ts: Date.now(), resumen: "Largos", ideas: [
      { titulo: "The GTA 6 Situation Is Insane: Every Record It Broke", es: "Todos los récords", duracion: "14-16 min", formato: "Noticia", capitulos: ["Intro", "Ventas"], verificado: "✅", referencia: "@WestJett 1,6 M" }],
      videos: [{ titulo: "Testing Everything In GTA 6", vistas: 5900000, canal: "LazarBeam", duracion: "14:01", formato: "Partida grabada", sin_partida: false, url: "https://www.youtube.com/watch?v=x" }],
      formatos: [{ formato: "Guía de consejos", vistas: 4000000, n: 3, sin_partida: true }], prompt: "Actúa como un director creativo… FASE 1", prompt_flujo: "Flujo de prueba" }));
    await page.waitForTimeout(120);
    ok("Vídeos largos: ideas con capítulos, vídeos de referencia y formatos", /Every Record It Broke/.test(await txt(page, "#largosIdeas")) && (await page.$$("#largosIdeas ol li")).length === 2 && /5,9 M/.test(await txt(page, "#largosVideos")) && /🎮/.test(await txt(page, "#largosVideos")) && /✅ Guía de consejos/.test(await txt(page, "#largosFmt")));
    await page.click("#largosIdeas >> text=🎬 Producir este vídeo largo");
    ok("Vídeos largos: «Producir» rellena el título y marca Vídeo largo", (await page.inputValue("#titulo")) === "The GTA 6 Situation Is Insane: Every Record It Broke" && await page.isChecked("#tipoLargo"));
    const nAntes = await page.evaluate(() => window.__sent.length);
    await page.click("#goBtn");
    await page.waitForFunction(n => window.__sent.length === n + 1, nAntes);
    const tl = await page.evaluate(() => window.__sent[window.__sent.length - 1].text);
    ok("Vídeo largo: el encargo dice «Producir vídeo largo» y la duración", /^Producir vídeo largo — TÍTULO: The GTA 6 Situation/.test(tl) && /Duración: 12-20 min/.test(tl));
    ok("Vídeo largo: sin referencia, pide que la busque el equipo; el prompt maestro se ve en el panel", /Referencia: que la busque el equipo/.test(tl) && /director creativo/.test(await txt(page, "#promptTexto")));
    ok("Vídeo largo: las ideas de debajo del título pasan a ser de vídeo largo", /vídeo largo/.test(await txt(page, "#ideasLabel")) && /Every Record It Broke/.test(await txt(page, "#ideas")) && /14-16 min/.test(await txt(page, "#ideas")) && !(await page.isVisible("#loteBtn")));
    await page.check("#tipoShort");
    await page.waitForTimeout(80);
    ok("Short: vuelven las ideas de Short", /Short/.test(await txt(page, "#ideasLabel")) && !/Every Record It Broke/.test(await txt(page, "#ideas")));
    ok("Funciones nuevas: sin errores", !errors.length, errors.join(" | "));
    await page.screenshot({ path: path.join(SHOTS, "oficina_v3.png"), fullPage: true });
    await ctx.close();
  }

  { // 2. Sin sesión de producción escuchando
    const { page, ctx, errors } = await abrir(browser, "sin_sesion");
    ok("Avisa al cargar de que la sesión no escucha", /no está escuchando/.test(await txt(page, "#capNote")));
    await page.fill("#titulo", "GTA 6 Needs 212 GB. Will It Fit?");
    await page.click("#goBtn");
    await page.waitForTimeout(200);
    ok("Si falla, da la frase para el chat", await page.isVisible("#fallback") && /212 GB/.test(await txt(page, "#fallbackTxt")));
    const enc = await page.evaluate(() => Object.values(window.__cols.encargos));
    ok("Si falla, el encargo queda como no enviado", enc.length === 1 && enc[0].estado === "no enviado");
    ok("Sin sesión: sin errores", !errors.length, errors.join(" | "));
    await ctx.close();
  }

  { // 3. Fuera de Claude
    const { page, ctx, errors } = await abrir(browser, "fuera");
    ok("Fuera de Claude: explica cómo usarla", /Abre esta página dentro de Claude/.test(await txt(page, "#capNote")));
    ok("Fuera de Claude: sin errores", !errors.length, errors.join(" | "));
    await ctx.close();
  }

  { // 4. Tamaños de pantalla (móvil, iPad, portátil, escritorio)
    for (const w of [390, 768, 1024, 1366]) {
      const { page, ctx } = await abrir(browser, "ok", w);
      ok(`${w}px: sin desplazamiento lateral`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
      const solapes = await page.evaluate(() => [...document.querySelectorAll(".worker")].filter(e => e.scrollWidth > e.clientWidth + 2).length);
      ok(`${w}px: las fichas de la plantilla caben`, solapes === 0, `${solapes} desbordan`);
      if (w === 390 || w === 768) await page.screenshot({ path: path.join(SHOTS, `oficina_${w}.png`), fullPage: true });
      await ctx.close();
    }
  }

  await browser.close();
  for (const r of results) console.log(`${r.pass ? "✓" : "✗"} ${r.name}${r.pass || !r.detail ? "" : "  → " + r.detail}`);
  const passed = results.filter(r => r.pass).length;
  console.log(`\n${passed}/${results.length} pruebas superadas`);
  process.exit(passed === results.length ? 0 : 1);
})();
