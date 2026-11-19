// Pruebas de la oficina VICECITY DAYS TV HQ (producir un Short desde un título).
// Uso: node oficina/test_oficina.js   (requiere Playwright con Chromium)
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), os = require("os");
const PAGE = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
const FILE = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "hq-")), "index.html");
fs.writeFileSync(FILE, `<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body style="margin:0">${PAGE}</body></html>`);
const SHOTS = process.env.SHOTS_DIR || path.dirname(FILE);
const results = [];
const ok = (name, cond, detail = "") => results.push({ name, pass: !!cond, detail });

// Simula la base de datos de la página (db) y los comentarios "Send to Claude"
function mock({ modo }) {
  window.__sent = []; window.__docs = {}; const subs = [];
  const emit = () => { const docs = Object.entries(window.__docs).map(([id, d]) => ({ id, exists: true, data: () => d, metadata: {} })).sort((x, y) => y.data().ts - x.data().ts); subs.forEach(f => f({ docs, size: docs.length, empty: !docs.length, docChanges: () => [], metadata: {} })); };
  window.__claudeActualiza = (id, cambios) => { Object.assign(window.__docs[id], cambios); emit(); };
  let n = 0;
  const ref = id => ({ id, set: async d => { window.__docs[id] = { ...d }; emit(); }, update: async d => { Object.assign(window.__docs[id], d); emit(); } });
  const query = { orderBy: () => query, limit: () => query, onSnapshot: f => { subs.push(f); setTimeout(emit, 0); return () => {}; } };
  window.__estado = {}; const docSubs = {};
  window.__claudeEstado = (path, d) => { window.__estado[path] = d; (docSubs[path] || []).forEach(f => f({ exists: true, data: () => d, metadata: {} })); };
  const db = {
    collection: () => ({ ...query, doc: id => ref(id || "enc" + (++n)) }),
    doc: path => ({ onSnapshot: f => { (docSubs[path] = docSubs[path] || []).push(f); setTimeout(() => f(path in window.__estado ? { exists: true, data: () => window.__estado[path], metadata: {} } : { exists: false, data: () => undefined, metadata: {} }), 0); return () => {}; } }),
  };
  const comments = {
    anchorFor: async () => ({ path: "#nuevo", x: 0.5, y: 0.5 }),
    canSendToClaude: async () => (modo === "sin_sesion" ? "no_session" : "available"),
    sendToClaude: async t => { window.__sent.push(t); if (modo === "sin_sesion") throw { code: "claude_unavailable", message: "no" }; return { threadId: "t1", commentId: "c1" }; },
  };
  if (modo !== "fuera") window.claude = { use: async name => (name === "db" ? db : name === "comments" ? comments : null) };
}
async function abrir(browser, modo, width = 1024) {
  const ctx = await browser.newContext({ viewport: { width, height: 1300 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  page.on("console", m => { if (m.type() === "error" && !/fonts\.|ERR_/.test(m.text())) errors.push(m.text()); });
  await page.addInitScript(mock, { modo });
  await page.goto("file://" + FILE);
  await page.waitForTimeout(300);
  return { page, ctx, errors };
}
const estado = (page, id) => page.evaluate(id => window.__vshDebug().status[id], id);
const docs = page => page.evaluate(() => window.__docs);

(async () => {
  const browser = await chromium.launch();

  { // 1. Enviar un encargo y seguir los pasos que anota Claude
    const { page, ctx, errors } = await abrir(browser, "ok");
    ok("Hay 4 ideas del banco", (await page.$$eval("#ideas .idea", e => e.length)) === 4);
    await page.click("#ideas .idea >> nth=0");
    ok("Tocar una idea rellena el título", /Best-Reviewed/.test(await page.inputValue("#titulo")));
    await page.click("#goBtn");
    await page.waitForFunction(() => window.__sent.length === 1);
    const sent = await page.evaluate(() => window.__sent[0]);
    const d = await docs(page); const id = Object.keys(d)[0];
    ok("Guarda el encargo en la base de datos", d[id].titulo === "GTA 6 Just Became the Best-Reviewed Game Ever" && d[id].estado === "enviado");
    ok("Lo envía a Claude con título e id del encargo", sent.text === `Producir Short — TÍTULO: GTA 6 Just Became the Best-Reviewed Game Ever\nEncargo: ${id}` && !!sent.anchor);
    await page.waitForTimeout(100);
    ok("Aparece como recibido en cola", /recibido, en cola/.test(await page.textContent("#prodChip")));
    await page.evaluate(id => window.__claudeActualiza(id, { estado: "en marcha", paso: 3 }), id);
    await page.waitForTimeout(150);
    ok("Lee el paso que anota Claude (3/8)", /paso 3\/8/.test(await page.textContent("#prodChip")));
    ok("Nil trabaja y Jarvis está hecho", (await estado(page, "nil")) === "working" && (await estado(page, "jarvis")) === "done");
    ok("La lista marca 2 hechos y 1 actual", (await page.$$eval("#pasos li.hecho", e => e.length)) === 2 && (await page.$$eval("#pasos li.ahora", e => e.length)) === 1);
    ok("El trabajo viaja de mesa en mesa", (await page.evaluate(() => window.__vshDebug().packets)) > 0);
    await page.evaluate(id => window.__claudeActualiza(id, { estado: "entregado", paso: 8, nota: "título ajustado" }), id);
    await page.waitForTimeout(150);
    ok("Al terminar: entregado y equipo libre", /entregado/.test(await page.textContent("#prodChip")) && (await estado(page, "almudena")) === "idle");
    ok("El historial muestra la nota de Claude", /título ajustado/.test(await page.textContent("#historial")));
    ok("Sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 2. No hay sesión escuchando: NO queda nada en cola
    const { page, ctx, errors } = await abrir(browser, "sin_sesion");
    await page.waitForTimeout(200);
    ok("Avisa al cargar de que la sesión no escucha", /no está escuchando/.test(await page.textContent("#capNote")));
    await page.fill("#titulo", "GTA 6 test title here");
    await page.click("#goBtn");
    await page.waitForSelector("#fallback:not([hidden])");
    const d = await docs(page);
    ok("El encargo queda como NO enviado (no en cola)", Object.values(d).every(x => x.estado === "no enviado") && !/en cola/.test(await page.textContent("#historial")));
    ok("Da la frase para pegar en el chat", /TÍTULO: GTA 6 test title here/.test(await page.textContent("#fallbackTxt")) && /No se ha encargado nada/.test(await page.textContent("#capNote")));
    ok("Sin sesión: sin errores", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 3. Fuera de Claude
    const { page, ctx, errors } = await abrir(browser, "fuera");
    await page.waitForTimeout(200);
    ok("Fuera de Claude: lo explica", /Abre esta página dentro de Claude/.test(await page.textContent("#capNote")));
    await page.fill("#titulo", "GTA 6 offline title test");
    await page.click("#goBtn");
    ok("Fuera de Claude: ofrece la frase para el chat", !(await page.$eval("#fallback", e => e.hidden)));
    ok("Fuera de Claude: sin errores", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 6. Pantallas
    for (const w of [390, 768, 1024, 1366]) {
      const { page, ctx } = await abrir(browser, "ok", w);
      await page.fill("#titulo", "Every GTA 6 Gang Leader in 30 Seconds");
      await page.click("#goBtn");
      await page.waitForFunction(() => window.__sent.length === 1);
      await page.evaluate(() => window.__claudeActualiza(Object.keys(window.__docs)[0], { estado: "en marcha", paso: 2 }));
      await page.waitForTimeout(200);
      ok(`${w}px: sin desplazamiento lateral`, (await page.evaluate(() => document.documentElement.scrollWidth)) <= w);
      const tags = await page.evaluate(() => window.__vshDebug().tags);
      let n = 0;
      for (let i = 0; i < tags.length; i++) for (let j = i + 1; j < tags.length; j++) { const a = tags[i], b = tags[j]; if (a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h) n++; }
      ok(`${w}px: nombres y bocadillos no se pisan`, n === 0, `${n} solapes`);
      ok(`${w}px: todo dentro de la oficina`, tags.every(t => t.y >= 0 && t.x >= 0 && t.x + t.w <= w));
      if (w === 1024) await page.screenshot({ path: path.join(SHOTS, "hq_ipad.png"), fullPage: true });
      if (w === 390) await page.screenshot({ path: path.join(SHOTS, "hq_phone.png"), fullPage: false });
      await ctx.close();
    }
  }

    { // Piloto automático: temporizadores, canal e investigación
    const { page, ctx, errors } = await abrir(browser, "ok", 1366);
    const t1 = await page.textContent("#tInvT"); await page.bringToFront(); await page.waitForTimeout(2300); const t2 = await page.textContent("#tInvT");
    ok("Temporizador de investigación en marcha", /^\d\d:\d\d:\d\d$/.test(t2) && t1 !== t2 || /Trabajando/.test(t2), t1 + " → " + t2);
    const tc = await page.textContent("#tCanT");
    const [hh] = tc.split(":").map(Number);
    ok("Repaso del canal en menos de 6 h", /Trabajando/.test(tc) || hh < 6, tc);
    const prox = await page.evaluate(() => { const r = window.__vshDebug().proxima({ horas: [10], minuto: 23 }, new Date("2026-11-19T08:00:00Z")); return new Date(r).toISOString(); });
    ok("Calcula la hora de Madrid (10:23 = 09:23 UTC en invierno)", prox === "2026-11-19T09:23:00.000Z", prox);
    const prox2 = await page.evaluate(() => new Date(window.__vshDebug().proxima({ horas: [0, 6, 12, 18], minuto: 47 }, new Date("2026-07-01T10:00:00Z"))).toISOString());
    ok("Cambio de hora: 12:47 Madrid = 10:47 UTC en verano", prox2 === "2026-07-01T10:47:00.000Z", prox2);
    await page.evaluate(() => window.__claudeEstado("estado/canal", { ts: Date.now(), suscriptores: 12, cambio_suscriptores: 3, visualizaciones: 1660, cambio_visualizaciones: 100, shorts: [{ titulo: "GTA 6's Map Is Real Florida", vistas: 1200, cambio: 100 }] }));
    await page.waitForTimeout(100);
    ok("Muestra suscriptores y visualizaciones", (await page.textContent("#kSubs")) === "12" && /1\.660|1660/.test(await page.textContent("#kViews")) && /\+100/.test(await page.textContent("#kViewsC")));
    ok("Lista los Shorts del canal", /Real Florida/.test(await page.textContent("#canalShorts")));
    await page.evaluate(() => window.__claudeEstado("estado/investigacion", { ts: Date.now(), resumen: "GTA 6 sale hoy", ideas: [{ titulo: "Idea nueva verificada", recomendada: true, porque: "noticia" }, { titulo: "Otra idea" }] }));
    await page.waitForTimeout(100);
    ok("Las ideas del banco se actualizan solas", (await page.$$eval("#ideas .idea", e => e.map(x => x.textContent))).join("|") === "Idea nueva verificada|Otra idea");
    ok("Marca las ideas para producir hoy", /producir hoy/.test(await page.textContent("#invIdeas")));
    ok("Piloto automático: sin errores", !errors.length, errors.join(" | "));
    for (const w of [390, 768]) {
      await page.setViewportSize({ width: w, height: 1000 }); await page.waitForTimeout(150);
      ok(`${w}px: temporizadores sin desbordar`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
    }
    await page.setViewportSize({ width: 1366, height: 1000 });
    await page.screenshot({ path: path.join(SHOTS, "piloto.png") });
    await ctx.close();
  }

await browser.close();
  for (const r of results) console.log(`${r.pass ? "✓" : "✗"} ${r.name}${r.pass || !r.detail ? "" : "  → " + r.detail}`);
  const f = results.filter(r => !r.pass).length;
  console.log(`\n${results.length - f}/${results.length} pruebas superadas`);
  process.exit(f ? 1 : 0);
})().catch(e => { for (const r of results) console.log(`${r.pass ? "✓" : "✗"} ${r.name}`); console.error(e); process.exit(2); });
