// Ejecuta un encargo completo en la oficina con las respuestas reales de respuestas.json
// y guarda lo que recibe cada departamento (prompts/) y el encargo final (encargo.txt).
const { chromium } = require("playwright");
const fs = require("fs"), path = require("path"), os = require("os");
const DIR = __dirname;
const PAGE = fs.readFileSync(path.join(DIR, "..", "index.html"), "utf8");
const FILE = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "real-")), "index.html");
fs.writeFileSync(FILE, `<!doctype html><html><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"></head><body style="margin:0">${PAGE}</body></html>`);
const R = JSON.parse(fs.readFileSync(path.join(DIR, "respuestas.json"), "utf8"));
const MARK = [["greenlight", /Antes de publicar revisas el paquete/], ["trends", /Eres Jarvis/], ["plan", /Eres Almudena/], ["titles", /Eres Torrente/], ["thumbs", /Eres Nil/],
  ["script", /Eres El Chapo/], ["retention", /Eres Pablito/], ["compliance", /Eres Nobita/], ["shorts", /Eres Victillor/], ["launch", /Eres Guerrero/]];
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1024, height: 1300 } });
  await ctx.grantPermissions(["clipboard-read", "clipboard-write"]);
  const page = await ctx.newPage();
  const errors = []; page.on("pageerror", e => errors.push(e.message));
  await page.exposeFunction("__answer", prompt => { const m = MARK.find(([, re]) => re.test(prompt)); return m ? { key: m[0], data: R[m[0]] } : null; });
  await page.addInitScript(() => {
    window.__log = [];
    const json = async (prompt, opts) => {
      const a = await window.__answer(prompt);
      window.__log.push({ key: a?.key, tier: opts?.modelTier, bytes: new TextEncoder().encode(prompt).length, prompt });
      await new Promise(r => setTimeout(r, 60));
      if (!a) throw { code: "upstream_error" };
      return JSON.parse(JSON.stringify(a.data));
    };
    window.claude = { use: async n => (n === "sample" ? Object.assign(async () => ({}), { json }) : null) };
  });
  await page.goto("file://" + FILE);
  await page.waitForFunction(() => !/Conectando/.test(document.getElementById("goBtn").textContent));
  await page.fill("#topic", "qué explorar primero en Leonida");
  await page.click("#goBtn");
  await page.waitForFunction(() => document.getElementById("stopBtn").hidden, null, { timeout: 30000 });
  const log = await page.evaluate(() => window.__log);
  fs.mkdirSync(path.join(DIR, "prompts"), { recursive: true });
  log.forEach((l, i) => fs.writeFileSync(path.join(DIR, "prompts", `${String(i + 1).padStart(2, "0")}-${l.key}.txt`), l.prompt));
  const steps = await page.$$eval(".stage[data-step]", els => els.map(e => ({ step: e.dataset.step, cls: e.className, qc: [...e.querySelectorAll(".qc .chip")].map(c => c.textContent) })));
  console.log("Llamadas:", log.map(l => `${l.key}(${l.tier}, ${(l.bytes / 1024).toFixed(1)} KB)`).join(" → "));
  for (const s of steps) console.log(`${/failed/.test(s.cls) ? "✗" : /pending/.test(s.cls) ? "…" : "•"} ${s.step.padEnd(11)} ${s.qc.join("  ")}`);
  const handoff = await page.$('[data-step="handoff"] .actions button');
  if (handoff) { await handoff.click(); fs.writeFileSync(path.join(DIR, "encargo.txt"), await page.evaluate(() => navigator.clipboard.readText())); console.log("Encargo copiado: encargo.txt"); }
  else console.log("SIN ENCARGO FINAL");
  await page.screenshot({ path: path.join(DIR, "captura.png"), fullPage: true });
  console.log("Errores JS:", errors.length ? errors : "ninguno");
  await b.close();
})();
