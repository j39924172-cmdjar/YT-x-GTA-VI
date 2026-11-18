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
  const db = { collection: () => ({ ...query, doc: id => ref(id || "enc" + (++n)) }) };
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
    ok("Tocar una idea rellena el título", /Vercetti/.test(await page.inputValue("#titulo")));
    await page.click("#goBtn");
    await page.waitForFunction(() => window.__sent.length === 1);
    const sent = await page.evaluate(() => window.__sent[0]);
    const d = await docs(page); const id = Object.keys(d)[0];
    ok("Guarda el encargo en la base de datos", d[id].titulo === "GTA 6 Just Name-Dropped Tommy Vercetti's Estate" && d[id].estado === "enviado");
    ok("Lo envía a Claude con título e id del encargo", sent.text === `Producir Short — TÍTULO: GTA 6 Just Name-Dropped Tommy Vercetti's Estate\nEncargo: ${id}` && !!sent.anchor);
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

  await browser.close();
  for (const r of results) console.log(`${r.pass ? "✓" : "✗"} ${r.name}${r.pass || !r.detail ? "" : "  → " + r.detail}`);
  const f = results.filter(r => !r.pass).length;
  console.log(`\n${results.length - f}/${results.length} pruebas superadas`);
  process.exit(f ? 1 : 0);
})().catch(e => { for (const r of results) console.log(`${r.pass ? "✓" : "✗"} ${r.name}`); console.error(e); process.exit(2); });
