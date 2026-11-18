// Pruebas de la oficina con respuestas de Claude simuladas.
// Uso: node oficina/test_oficina.js   (requiere Playwright con Chromium)
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const os = require("os");

const PAGE = fs.readFileSync(path.join(__dirname, "index.html"), "utf8");
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), "oficina-"));
const FILE = path.join(TMP, "index.html");
fs.writeFileSync(FILE, `<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body style="margin:0">${PAGE}</body></html>`);
const SHOTS = process.env.SHOTS_DIR || TMP;

// ------------------------------------------------------------------ respuestas simuladas
const scene = (i, n) => ({
  narracion: i === n - 1 ? "Suscríbete y cuéntame en comentarios cuál no conocías." : `Secreto número ${i + 1}: en esta zona de Vice City hay algo que casi nadie ha visto todavía.`,
  texto_pantalla: i === 0 ? "SOLO DE NOCHE" : `SECRETO ${i + 1}`,
  visual: "Gameplay de la playa al anochecer",
  prompt_ia: "Cinematic aerial shot of a neon tropical beach city at dusk, palm trees",
});
const FIX = {
  trends: { resumen: "Secretos y dinero dominan.", tendencias: [
    { tema: "Secretos de Vice City", por_que: "Retienen.", fiabilidad: "evergreen" },
    { tema: "Dinero rápido", por_que: "Búsquedas constantes.", fiabilidad: "evergreen" },
    { tema: "Coches ocultos", por_que: "Muy visual.", fiabilidad: "probable" },
    { tema: "Próxima actualización online", por_que: "Depende de anuncios.", fiabilidad: "verificar" }] },
  idea: { ideas: [
    { titulo: "5 secretos de Vice City", angulo: "Ubicaciones exactas", gancho: "Este sitio solo aparece de noche.", pilar: "secretos" },
    { titulo: "Dinero rápido en GTA 6", angulo: "Método paso a paso", gancho: "Así hice un millón en una hora.", pilar: "guías" }], elegida: 0, razon: "Gancho fuerte." },
  script: n => ({ titulo: "5 secretos de Vice City", gancho: "Este sitio solo aparece de noche.", escenas: Array.from({ length: n }, (_, i) => scene(i, n)), cta: "Suscríbete", fuentes: "Ubicaciones a comprobar jugando." }),
  seo: { titulo: "GTA 6: 5 secretos de Vice City que casi nadie ha visto", descripcion: "Secretos de GTA 6.\nContenido no oficial hecho por fans. GTA VI es una marca de Rockstar Games.",
    etiquetas: Array.from({ length: 16 }, (_, i) => `gta 6 etiqueta ${i}`), hashtags: ["#GTA6", "#Shorts", "#ViceCity"], miniatura: { texto: "Solo de noche", prompt_imagen: "Neon skyline", color: "#FFE14D" } },
  ok: { aprobado: true, declarar_ia: true, avisos: [] },
  block: { aprobado: false, declarar_ia: true, avisos: [{ nivel: "bloquea", tema: "Título", detalle: "El título promete algo que no se ve.", arreglo: "Cambiar el título." }] },
};

// Se inyecta en la página: simula window.claude.use("sample")
function mockInit({ scenario }) {
  window.__prompts = [];
  let complianceCalls = 0, scriptCalls = 0;
  const delay = scenario === "slow" ? 1500 : 40;
  const F = window.__FIX;
  async function json(prompt, opts) {
    window.__prompts.push(prompt);
    await new Promise((res, rej) => {
      const t = setTimeout(res, delay);
      opts?.signal?.addEventListener("abort", () => { clearTimeout(t); rej({ code: "cancelled" }); });
    });
    if (scenario === "deny") throw { code: "not_granted", message: "no" };
    const isLong = /10 escenas/.test(prompt);
    if (/Eres Valeria/.test(prompt)) return scenario === "messy" ? { tendencias: "Secretos de Vice City\nDinero rápido\nCoches" } : F.trends;
    if (/Eres Tomás/.test(prompt)) return scenario === "messy" ? { ideas: [{ titulo: "Secretos", gancho: "Mira esto" }], elegida: "7" } : F.idea;
    if (/Sois Irene \(guionista\) y Bruno/.test(prompt)) {
      scriptCalls++;
      if (scenario === "bad_script" && scriptCalls === 1) return { titulo: "x", escenas: [] };
      if (scenario === "messy") return { titulo: "Secretos", escenas: [1, 2, 3, 4, 5].map(i => ({ narracion: "Texto " + i, texto_pantalla: "UN TEXTO DEMASIADO LARGO PARA PANTALLA" })) };
      return isLong ? F.script10 : F.script6;
    }
    if (/Sois Carla/.test(prompt)) return scenario === "messy" ? { titulo: "Un título larguísimo ".repeat(6), descripcion: "sin aviso", etiquetas: "gta 6, gta vi", hashtags: "GTA6", miniatura: "nada" } : F.seo;
    if (/Eres Andrés/.test(prompt)) { complianceCalls++; return scenario === "reject_then_fix" && complianceCalls === 1 ? F.block : F.ok; }
    if (/Sois Irene \(guionista\) y Carla/.test(prompt)) return { guion: F.script6, seo: { ...F.seo, titulo: "GTA 6: secretos de Vice City (corregido)" } };
    throw { code: "upstream_error" };
  }
  const sample = Object.assign(async (p, o) => ({ text: JSON.stringify(await json(p, o)) }), { json });
  if (scenario !== "no_claude") window.claude = { use: async name => (name === "sample" ? sample : null) };
}

// ------------------------------------------------------------------ utilidades
const results = [];
function ok(name, cond, detail = "") { results.push({ name, pass: !!cond, detail }); }

async function open(browser, scenario, { width = 1024, storage } = {}) {
  const ctx = await browser.newContext({ viewport: { width, height: 1200 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  page.on("console", m => { if (m.type() === "error" && !/fonts\.(googleapis|gstatic)/.test(m.text()) && !/ERR_/.test(m.text())) errors.push(m.text()); });
  await page.addInitScript(`window.__FIX = ${JSON.stringify({ ...FIX, script6: FIX.script(6), script10: FIX.script(10) })};`);
  await page.addInitScript(mockInit, { scenario });
  if (storage) await page.addInitScript(s => { try { localStorage.setItem("vice-studio-hq:last", s); } catch {} }, storage);
  await page.goto("file://" + FILE);
  await page.waitForFunction(() => !/Conectando/.test(document.getElementById("goBtn").textContent));
  return { page, ctx, errors };
}
const go = async (page, { long = false, topic = "" } = {}) => {
  if (long) await page.click("#fmtLong");
  if (topic) await page.fill("#topic", topic);
  await page.click("#goBtn");
};
const idle = page => page.waitForFunction(() => document.getElementById("stopBtn").hidden, null, { timeout: 15000 });
const steps = page => page.$$eval(".stage[data-step]", els => els.map(e => ({ step: e.dataset.step, cls: e.className, qc: [...e.querySelectorAll(".qc .chip")].map(c => c.textContent) })));
const card = page => page.textContent("#agentCard");
const statusOf = (page, id) => page.evaluate(id => window.__vshDebug?.().status[id], id);

// ------------------------------------------------------------------ escenarios
(async () => {
  const browser = await chromium.launch();

  { // 1. Short completo
    const { page, ctx, errors } = await open(browser, "ok");
    ok("Arranca mostrando el ejemplo", /Ejemplo de producción/.test(await page.textContent("#results")));
    await go(page, { topic: "secretos de Vice City" });
    await page.waitForSelector('.stage.live[data-step="trends"]');
    ok("Valeria trabaja en el paso 1", (await statusOf(page, "valeria")) === "working");
    await idle(page);
    const st = await steps(page);
    ok("Short: los 5 pasos terminan", st.filter(s => ["trends", "idea", "script", "seo", "compliance"].includes(s.step) && !/pending|failed/.test(s.cls)).length === 5);
    ok("Short: aparece el paso de voz y montaje", st.some(s => s.step === "handoff"));
    ok("Short: control de calidad sin fallos graves", st.every(s => !s.qc.some(q => q.startsWith("✗"))), JSON.stringify(st.map(s => s.qc)));
    ok("Short: 6 escenas en pantalla", (await page.$$eval('[data-step="script"] .scene', e => e.length)) === 6);
    const prompts = await page.evaluate(() => window.__prompts);
    ok("Se hacen exactamente 5 llamadas", prompts.length === 5, String(prompts.length));
    ok("El tema llega a Valeria", /secretos de Vice City/.test(prompts[0]));
    ok("Guion pide 6 escenas", /Exactamente 6 escenas/.test(prompts[2]));
    ok("Tomás recibe las tendencias de Valeria", /Dinero rápido/.test(prompts[1]));
    ok("Mateo, Julia y Lola esperan en el chat", (await statusOf(page, "mateo")) === "waiting" && (await statusOf(page, "lola")) === "waiting");
    ok("Andrés queda en 'hecho'", (await statusOf(page, "andres")) === "done");
    await ctx.grantPermissions(["clipboard-read", "clipboard-write"]);
    await page.click('[data-step="handoff"] button');
    const clip = await page.evaluate(() => navigator.clipboard.readText());
    ok("Copiar encargo incluye título, guion y formato", /TÍTULO: GTA 6: 5 secretos/.test(clip) && /Escena 6/.test(clip) && /9:16/.test(clip));
    // persistencia
    await page.reload();
    await page.waitForFunction(() => !/Conectando/.test(document.getElementById("goBtn").textContent));
    ok("Al recargar se recupera la producción", /Tu producción/.test(await page.textContent("#results")) && (await page.$('[data-step="handoff"]')) !== null);
    ok("Al recargar los estados se mantienen", (await statusOf(page, "mateo")) === "waiting");
    // ficha del puesto desde el organigrama y desde la oficina
    await page.click(".org .post:nth-child(5)");
    ok("Organigrama abre la ficha de Andrés", /Andrés Molina/.test(await card(page)) && /Se lo pasa a/.test(await card(page)));
    const hit = await page.evaluate(() => window.__vshDebug().hits.find(h => h.id === "gael"));
    const box = await page.$eval("#office", e => e.getBoundingClientRect().toJSON());
    await page.mouse.click(box.x + hit.x, box.y + hit.y);
    ok("Tocar a Gael en la oficina abre su ficha", /Gael Ortiz/.test(await card(page)));
    await page.screenshot({ path: path.join(SHOTS, "t1_ipad.png"), fullPage: false });
    ok("Short: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 2. Vídeo largo
    const { page, ctx, errors } = await open(browser, "ok");
    await go(page, { long: true });
    await idle(page);
    const prompts = await page.evaluate(() => window.__prompts);
    ok("Largo: el guion pide 10 escenas", /Exactamente 10 escenas/.test(prompts[2]));
    ok("Largo: 10 escenas en pantalla", (await page.$$eval('[data-step="script"] .scene', e => e.length)) === 10);
    ok("Largo: no exige #Shorts", !(await steps(page)).find(s => s.step === "seo").qc.some(q => /Shorts/.test(q)));
    ok("Largo: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 3. Respuestas mal formadas
    const { page, ctx, errors } = await open(browser, "messy");
    await go(page);
    await idle(page);
    const st = await steps(page);
    ok("Desordenado: no se rompe la página", errors.length === 0, errors.join(" | "));
    ok("Desordenado: tendencias en texto se convierten en lista", (await page.$$eval('[data-step="trends"] li', e => e.length)) === 3);
    ok("Desordenado: idea elegida fuera de rango usa la primera", /elegida/.test(await page.textContent('[data-step="idea"]')));
    ok("Desordenado: avisa de textos largos y falta de prompts", st.find(s => s.step === "script").qc.some(q => q.startsWith("!")));
    ok("Desordenado: avisa título largo y falta de #Shorts", st.find(s => s.step === "seo").qc.filter(q => q.startsWith("!")).length >= 3);
    await ctx.close();
  }

  { // 4. Guion vacío → se para en el paso 3 y se puede seguir
    const { page, ctx, errors } = await open(browser, "bad_script");
    await go(page);
    await idle(page);
    ok("Guion vacío: se para en el paso 3", /failed/.test((await steps(page)).find(s => s.step === "script").cls));
    ok("Guion vacío: Irene y Bruno en rojo", (await statusOf(page, "irene")) === "error" && (await statusOf(page, "bruno")) === "error");
    ok("Guion vacío: no aparece el encargo", !(await page.$('[data-step="handoff"]')));
    await page.click('[data-step="script"] button.strong');
    await idle(page);
    ok("Seguir desde el paso 3 completa el encargo", !!(await page.$('[data-step="handoff"]')));
    const prompts = await page.evaluate(() => window.__prompts);
    ok("Al seguir no repite los pasos 1 y 2", prompts.filter(p => /Eres Valeria/.test(p)).length === 1);
    ok("Guion vacío: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 5. Sin permiso
    const { page, ctx } = await open(browser, "deny");
    await go(page);
    await idle(page);
    ok("Sin permiso: explica qué hacer", /permiso/.test(await page.textContent("#capNote")));
    ok("Sin permiso: el botón queda desactivado", await page.$eval("#goBtn", b => b.disabled));
    await ctx.close();
  }

  { // 6. Parar a mitad y seguir
    const { page, ctx, errors } = await open(browser, "slow");
    await go(page);
    await page.waitForFunction(() => window.__prompts.length === 2);
    await page.click("#stopBtn");
    await idle(page);
    ok("Parar: se queda en el paso 2", /failed/.test((await steps(page)).find(s => s.step === "idea").cls));
    ok("Parar: dice que lo has parado", /Has parado/.test(await page.textContent('[data-step="idea"]')));
    ok("Parar: nadie sigue trabajando", !(await page.evaluate(() => Object.values(window.__vshDebug().status).includes("working"))));
    await page.click('[data-step="idea"] button.strong');
    await idle(page);
    ok("Parar: al seguir termina", !!(await page.$('[data-step="handoff"]')));
    ok("Parar: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 7. Andrés frena el vídeo → correcciones → aprobado
    const { page, ctx, errors } = await open(browser, "reject_then_fix");
    await go(page);
    await idle(page);
    ok("Frenado: aparece el aviso de Andrés", !!(await page.$('[data-step="fix-box"]')));
    ok("Frenado: Andrés en rojo", (await statusOf(page, "andres")) === "error");
    ok("Frenado: no deja copiar el encargo", !(await page.$('[data-step="handoff"]')));
    await page.click('[data-step="fix-box"] button');
    await idle(page);
    ok("Corrección: después queda aprobado", !!(await page.$('[data-step="handoff"]')));
    ok("Corrección: el título cambia", /corregido/.test(await page.textContent('[data-step="seo"]')));
    ok("Corrección: se marca como corregido", /corregido ×1/.test(await page.textContent('[data-step="script"]')));
    ok("Corrección: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 8. Encargo a medias guardado (página cerrada mientras trabajaba)
    const half = JSON.stringify({ format: "short", topic: "", createdAt: 1, stages: { trends: FIX.trends }, checks: {}, revisions: 0, stopAt: null });
    const { page, ctx, errors } = await open(browser, "ok", { storage: half });
    ok("A medias: ofrece seguir desde el paso 2", /Seguir desde el paso 2/.test(await page.textContent("#results")));
    await page.click('[data-step="idea"] button.strong');
    await idle(page);
    ok("A medias: al seguir termina", !!(await page.$('[data-step="handoff"]')));
    ok("A medias: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 9. Fuera de Claude
    const { page, ctx, errors } = await open(browser, "no_claude");
    ok("Fuera de Claude: avisa y desactiva", (await page.$eval("#goBtn", b => b.disabled)) && /Abre esta página dentro de Claude/.test(await page.textContent("#capNote")));
    ok("Fuera de Claude: el ejemplo se ve igual", !!(await page.$('[data-step="handoff"]')));
    ok("Fuera de Claude: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 10. Tamaños de pantalla
    for (const w of [390, 768, 1024, 1366]) {
      const { page, ctx } = await open(browser, "ok", { width: w });
      const sw = await page.evaluate(() => document.documentElement.scrollWidth);
      ok(`Ancho ${w}px: sin desplazamiento lateral`, sw <= w, `scrollWidth ${sw}`);
      const countOverlaps = tags => {
        let n = 0;
        for (let i = 0; i < tags.length; i++) for (let j = i + 1; j < tags.length; j++) {
          const a = tags[i], b = tags[j];
          if (a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h) n++;
        }
        return n;
      };
      await go(page);
      await page.waitForSelector('.stage.live[data-step="script"]');
      await page.waitForTimeout(100);
      const busyTags = await page.evaluate(() => window.__vshDebug().tags);
      ok(`Ancho ${w}px: nombres y bocadillos no se pisan mientras trabajan`, countOverlaps(busyTags) === 0, `${countOverlaps(busyTags)} solapes`);
      await idle(page);
      await page.waitForTimeout(100);
      const tags = await page.evaluate(() => window.__vshDebug().tags);
      ok(`Ancho ${w}px: todo dentro de la oficina`, tags.every(t => t.y >= 0 && t.x >= 0 && t.x + t.w <= w), JSON.stringify(tags.filter(t => t.y < 0 || t.x < 0)));
      let overlaps = 0;
      for (let i = 0; i < tags.length; i++) for (let j = i + 1; j < tags.length; j++) {
        const a = tags[i], b = tags[j];
        if (a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h) overlaps++;
      }
      ok(`Ancho ${w}px: al terminar, nombres y bocadillos no se pisan`, overlaps === 0, `${overlaps} solapes`);
      if (w === 390) await page.screenshot({ path: path.join(SHOTS, "t10_phone.png"), fullPage: true });
      await ctx.close();
    }
  }

  await browser.close();
  const failed = results.filter(r => !r.pass);
  for (const r of results) console.log(`${r.pass ? "✓" : "✗"} ${r.name}${r.pass || !r.detail ? "" : "  → " + r.detail}`);
  console.log(`\n${results.length - failed.length}/${results.length} pruebas superadas`);
  process.exit(failed.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
