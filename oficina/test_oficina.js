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

// Simula el conector "Claude Code Remote" (window.claude.use("mcp"))
function mock({ modo }) {
  window.__calls = []; window.__watch = {};
  const mcp = {
    callTool: async (server, tool, input) => {
      window.__calls.push({ server, tool, input });
      if (modo === "sin_conector") throw { code: "server_not_connected", message: "no" };
      if (modo === "dudoso") throw { code: "upstream_error", message: "timeout" };
      return { content: [], payload: { session_id: "cse_x" } };
    },
    watchTool: (server, tool, input, handler) => { window.__watch[tool] = handler; return () => {}; },
  };
  if (modo !== "fuera") window.claude = { use: async n => (n === "mcp" ? mcp : null) };
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
const emitir = (page, tool, payload) => page.evaluate(([tool, payload]) => window.__watch[tool]?.({ type: "data", result: { payload } }), [tool, payload]);
const estado = (page, id) => page.evaluate(id => window.__vshDebug().status[id], id);

(async () => {
  const browser = await chromium.launch();

  { // 1. Producir desde un título y seguir los pasos
    const { page, ctx, errors } = await abrir(browser, "ok");
    ok("Hay 4 ideas del banco", (await page.$$eval("#ideas .idea", e => e.length)) === 4);
    await page.click("#ideas .idea >> nth=0");
    ok("Tocar una idea rellena el título", /Vercetti/.test(await page.inputValue("#titulo")));
    await page.click("#goBtn");
    await page.waitForFunction(() => window.__calls.length === 1);
    const call = await page.evaluate(() => window.__calls[0]);
    ok("Lanza la tarea Producir Short", call.server === "Claude Code Remote" && call.tool === "fire_trigger" && call.input.trigger_id === "trig_01474VhdtHa3mfx4H2mcy5p8");
    ok("Envía el título con el prefijo TÍTULO:", call.input.text === "TÍTULO: GTA 6 Just Name-Dropped Tommy Vercetti's Estate");
    ok("El encargo aparece en el historial y en cola", /Vercetti/.test(await page.textContent("#historial")) && /en cola/.test(await page.textContent("#prodChip")));
    ok("Empieza a seguir la conversación de producción", await page.evaluate(() => !!window.__watch.list_events && !!window.__watch.get_session));
    await emitir(page, "list_events", { data: [{ text: "TÍTULO: GTA 6 Just Name-Dropped Tommy Vercetti's Estate" }, { text: "[PASO 1/8] Investigación" }, { text: "[PASO 2/8] Guion" }, { text: "[PASO 3/8] Visuales" }] });
    await page.waitForTimeout(150);
    ok("Lee el paso actual (3/8)", /paso 3\/8/.test(await page.textContent("#prodChip")));
    ok("Nil trabaja y Jarvis está hecho", (await estado(page, "nil")) === "working" && (await estado(page, "jarvis")) === "done");
    ok("La lista de pasos marca hechos y actual", (await page.$$eval("#pasos li.hecho", e => e.length)) === 2 && (await page.$$eval("#pasos li.ahora", e => e.length)) === 1);
    await page.waitForTimeout(80);
    ok("El trabajo viaja de mesa en mesa", (await page.evaluate(() => window.__vshDebug().packets)) > 0);
    await emitir(page, "list_events", { data: [{ text: "TÍTULO: GTA 6 Just Name-Dropped Tommy Vercetti's Estate" }, { text: "[PASO 8/8] Entrega" }] });
    await emitir(page, "get_session", { status_bucket: "SESSION_STATUS_BUCKET_REVIEW_READY" });
    await page.waitForTimeout(150);
    ok("Al terminar queda como entregado", /entregado/.test(await page.textContent("#prodChip")) && (await estado(page, "almudena")) === "idle");
    await page.reload(); await page.waitForTimeout(300);
    ok("El historial se recuerda al recargar", /entregado/.test(await page.textContent("#historial")));
    ok("Sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 2. Marcadores antiguos de otro encargo no cuentan
    const { page, ctx } = await abrir(browser, "ok");
    await page.fill("#titulo", "Every GTA 6 Gang Leader in 30 Seconds");
    await page.click("#goBtn");
    await page.waitForFunction(() => window.__calls.length === 1);
    await emitir(page, "list_events", { data: [{ text: "TÍTULO: Otro encargo anterior" }, { text: "[PASO 7/8] Publicación" }] });
    await page.waitForTimeout(150);
    ok("No confunde los pasos de un encargo anterior", /en cola/.test(await page.textContent("#prodChip")));
    await ctx.close();
  }

  { // 3. Sin conector
    const { page, ctx, errors } = await abrir(browser, "sin_conector");
    await page.fill("#titulo", "GTA 6 test title here");
    await page.click("#goBtn");
    await page.waitForSelector("#fallback:not([hidden])");
    ok("Sin conector: da la frase para pegar en el chat", /TÍTULO: GTA 6 test title here/.test(await page.textContent("#fallbackTxt")) && /conector/.test(await page.textContent("#capNote")));
    ok("Sin conector: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 4. Respuesta dudosa
    const { page, ctx } = await abrir(browser, "dudoso");
    await page.fill("#titulo", "GTA 6 another test title");
    await page.click("#goBtn");
    await page.waitForTimeout(200);
    ok("Dudoso: avisa de comprobar antes de repetir", /comprueba la producción/.test(await page.textContent("#capNote")) && /another test/.test(await page.textContent("#historial")));
    await ctx.close();
  }

  { // 5. Fuera de Claude
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
      await page.waitForFunction(() => window.__calls.length === 1);
      await emitir(page, "list_events", { data: [{ text: "TÍTULO: Every GTA 6 Gang Leader in 30 Seconds" }, { text: "[PASO 2/8] Guion" }] });
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
