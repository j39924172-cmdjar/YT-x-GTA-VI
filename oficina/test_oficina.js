// Pruebas de Vice Studio HQ con respuestas de Claude simuladas.
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
const filler = n => Array.from({ length: n }, (_, i) => ["Vice", "City", "esconde", "algo", "que", "casi", "nadie", "ha", "visto", "todavía"][i % 10]).join(" ") + ".";
const scene = (i, n, perScene) => ({
  narracion: i === n - 1 ? `Suscríbete y dime en comentarios cuál no conocías. ${filler(perScene - 9)}` : `Secreto ${i + 1}. ${filler(perScene - 2)}`,
  texto_pantalla: i === 0 ? "SOLO DE NOCHE" : `SECRETO ${i + 1}`,
  visual: "Gameplay de la playa al anochecer",
  prompt_ia: "Cinematic aerial shot of a neon tropical beach city at dusk, palm trees",
});
const script = (n, perScene) => ({ titulo: "7 secretos de Vice City", gancho: "Este sitio solo aparece de noche.", escenas: Array.from({ length: n }, (_, i) => scene(i, n, perScene)), cta: "Suscríbete", fuentes: "Ubicaciones a comprobar jugando." });
const FIX = {
  trends: { resumen: "Secretos y dinero dominan.", temas: Array.from({ length: 10 }, (_, i) => ({ tema: ["Secretos de Vice City", "Dinero rápido", "Coches ocultos", "Easter eggs", "Récords", "Teorías", "Comparativa GTA 5", "Mapa completo", "Armas", "Próxima actualización"][i], por_que: "Interés alto.", fiabilidad: i === 9 ? "verificar" : i % 3 ? "probable" : "evergreen", potencial: 10 - i })) },
  plan: { tema: "Secretos de Vice City", angulo: "Ubicaciones exactas", promesa: "Descubrirás 7 lugares ocultos y cómo llegar.", publico: "Jugadores que ya han terminado la historia", shorts_previstos: ["Solo de noche", "Coche del puerto", "Faro"], dia_hora: "Viernes 18:00 (España)", razon: "Tema con más potencial." },
  titles: { promesa: "7 lugares ocultos", titulos: [{ titulo: "GTA 6: 7 secretos de Vice City que casi nadie ha encontrado", por_que: "Curiosidad + número" }, { titulo: "GTA 6: el lugar que solo aparece de noche", por_que: "Curiosidad" }, { titulo: "GTA 6: encontré 7 sitios ocultos en Vice City", por_que: "Resultado" }] },
  thumbs: { miniaturas: [{ texto: "Solo de noche", composicion: "Faro iluminado", prompt_imagen: "Neon lighthouse", color: "#FFE14D" }, { texto: "Nadie lo vio", composicion: "Puerta oculta", prompt_imagen: "Hidden door", color: "#33E1D6" }, { texto: "Sitio oculto", composicion: "Mapa con X", prompt_imagen: "Map with X", color: "#FF4FA3" }] },
  scriptWeek: script(10, 130),
  scriptExpress: script(6, 18),
  retention: { nota: 7, gancho_mejorado: "Este sitio de Vice City solo aparece de noche, y es el menos raro de los 7.", cambios: [{ escena: 1, problema: "Gancho lento", nuevo_texto: "TEXTO MEJORADO POR PABLITO. " + filler(120) }, { escena: 99, problema: "No existe", nuevo_texto: "ignorar" }], consejo_montaje: "Corta rápido al principio." },
  ok: { aprobado: true, declarar_ia: true, avisos: [] },
  block: { aprobado: false, declarar_ia: true, avisos: [{ nivel: "bloquea", tema: "Título", detalle: "El título promete algo que no se ve.", arreglo: "Cambiar el título." }] },
  shorts: { shorts: Array.from({ length: 4 }, (_, i) => ({ titulo: `Short ${i + 1}`, gancho: "Este lugar no existe de día.", narracion: filler(90) + " Tienes el resto en el vídeo completo.", textos_pantalla: ["SOLO DE NOCHE"], cierre: "Los otros 6, en el vídeo completo." })) },
  launchWeek: { descripcion: "Los 7 secretos de Vice City en GTA 6.\nContenido no oficial hecho por fans. GTA VI es una marca de Rockstar Games.", etiquetas: Array.from({ length: 16 }, (_, i) => `gta 6 ${i}`), hashtags: ["#GTA6", "#ViceCity"], capitulos: [{ tiempo: "0:00", titulo: "Intro" }, { tiempo: "1:10", titulo: "Secreto 2" }, { tiempo: "2:20", titulo: "Secreto 3" }], comentario_fijado: "¿Cuál no conocías?", dia_hora: "Viernes 18:00", pantalla_final: "Coches ocultos", lista: "Secretos GTA 6" },
  launchExpress: { descripcion: "Novedad de GTA 6.\nContenido no oficial hecho por fans. GTA VI es una marca de Rockstar Games.", etiquetas: Array.from({ length: 12 }, (_, i) => `gta 6 ${i}`), hashtags: ["#GTA6", "#Shorts"], capitulos: [], comentario_fijado: "¿Qué opinas?", dia_hora: "Hoy 20:00" },
  green: { notas: { clic: 8, retencion: 8, shorts: 8, publicacion: 9 }, luz_verde: true, rehacer_desde: "", motivo: "Paquete sólido.", titulo_final: "GTA 6: el lugar que solo aparece de noche", miniatura_final: "B", consejo: "Responde comentarios la primera hora." },
  redo: { notas: { clic: 5, retencion: 8, shorts: 8, publicacion: 8 }, luz_verde: false, rehacer_desde: "titles", motivo: "Los títulos no generan curiosidad suficiente.", titulo_final: "", miniatura_final: "A" },
  obs: { resumen: "Los vídeos de secretos tienen el doble de clics.", repetir: ["Secretos con número en el título"], evitar: ["Miniaturas con mucho texto"], ideas_de_comentarios: ["Coches ocultos"], siguiente_paso: "Haz una serie de secretos." },
};

function mockInit({ scenario }) {
  window.__prompts = []; window.__tiers = [];
  let complianceCalls = 0, scriptCalls = 0;
  const delay = scenario === "slow" ? 1500 : 40;
  const F = window.__FIX;
  async function json(prompt, opts) {
    window.__prompts.push(prompt); window.__tiers.push(opts?.modelTier);
    (window.__working = window.__working || []).push(Object.entries(window.__vshDebug().status).filter(([, v]) => v === "working").map(([k]) => k).join("+"));
    await new Promise((res, rej) => {
      const t = setTimeout(res, delay);
      opts?.signal?.addEventListener("abort", () => { clearTimeout(t); rej({ code: "cancelled" }); });
    });
    if (scenario === "paced" && /Eres El Chapo/.test(prompt)) await new Promise(r => { window.__release = r; });  // espera a la prueba
    if (scenario === "deny") throw { code: "not_granted", message: "no" };
    if (scenario === "real") {
      const MARK = [["greenlight", /Antes de publicar revisas el paquete/], ["trends", /Eres Jarvis/], ["plan", /Eres Almudena/], ["titles", /Eres Torrente/], ["thumbs", /Eres Nil/], ["script", /Eres El Chapo/], ["retention", /Eres Pablito/], ["compliance", /Eres Nobita/], ["shorts", /Eres Victillor/], ["launch", /Eres Guerrero/]];
      const m = MARK.find(([, re]) => re.test(prompt));
      return JSON.parse(JSON.stringify(window.__REAL[m[0]]));
    }
    const express = /Short vertical 9:16 de unos 45 segundos/.test(prompt);
    if (/Eres Jarvis/.test(prompt)) return scenario === "messy" ? { tendencias: "Secretos de Vice City\nDinero rápido\nCoches\nArmas\nMapa" } : F.trends;
    if (/Antes de publicar revisas el paquete/.test(prompt)) {
      const n = Number(sessionStorage.getItem("greenCalls") || 0) + 1;
      sessionStorage.setItem("greenCalls", String(n));
      return (scenario === "redo" || scenario === "redo_override") && n === 1 ? F.redo : F.green;
    }
    if (/Eres Almudena/.test(prompt)) return scenario === "messy" ? { tema: "Secretos", promesa: "Ver secretos", shorts_previstos: "uno, dos" } : F.plan;
    if (/Eres Torrente/.test(prompt)) return scenario === "messy" ? { titulos: ["Un título larguísimo sin la palabra clave que se pasa de los setenta caracteres de largo"] } : F.titles;
    if (/Eres Nil/.test(prompt)) return scenario === "messy" ? { miniaturas: [{ texto: "Un texto de miniatura demasiado largo", color: "rojo" }] } : F.thumbs;
    if (/Eres El Chapo/.test(prompt)) {
      scriptCalls++;
      if (scenario === "bad_script" && scriptCalls === 1) return { titulo: "x", escenas: [] };
      if (scenario === "messy") return { titulo: "Secretos", escenas: Array.from({ length: 8 }, (_, i) => ({ narracion: "Texto corto " + i, texto_pantalla: "UN TEXTO DEMASIADO LARGO PARA PANTALLA" })) };
      return express ? F.scriptExpress : F.scriptWeek;
    }
    if (/Eres Pablito/.test(prompt)) return scenario === "messy" ? { nota: "8", cambios: "nada" } : F.retention;
    if (scenario === "paced") scenario = "ok";
    if (/Eres Nobita/.test(prompt)) {
      // el contador sobrevive a las recargas, como lo haría la conversación real
      complianceCalls = Number(sessionStorage.getItem("complianceCalls") || 0) + 1;
      sessionStorage.setItem("complianceCalls", String(complianceCalls));
      return scenario === "reject_then_fix" && complianceCalls === 1 ? F.block : F.ok;
    }
    if (/Eres Victillor/.test(prompt)) return scenario === "messy" ? { shorts: [{ narracion: "muy corto" }] } : F.shorts;
    if (/Eres Guerrero/.test(prompt)) return scenario === "messy" ? { descripcion: "sin aviso", etiquetas: "gta 6, gta vi", comentario_fijado: "Comenta" } : (express ? F.launchExpress : F.launchWeek);
    if (/Sois El Chapo \(guionista\) y Torrente/.test(prompt)) return { titulos: { ...F.titles, titulos: [{ titulo: "GTA 6: 7 secretos de Vice City (corregido)" }, ...F.titles.titulos.slice(1)] }, guion: F.scriptWeek };
    if (/Eres Taison/.test(prompt)) return F.obs;
    throw { code: "upstream_error" };
  }
  const sample = Object.assign(async (p, o) => ({ text: JSON.stringify(await json(p, o)) }), { json });
  if (scenario !== "no_claude") window.claude = { use: async name => (name === "sample" ? sample : null) };
}

// ------------------------------------------------------------------ utilidades
const results = [];
function ok(name, cond, detail = "") { results.push({ name, pass: !!cond, detail }); }
async function open(browser, scenario, { width = 1024, storage, insights, real } = {}) {
  const ctx = await browser.newContext({ viewport: { width, height: 1200 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on("pageerror", e => errors.push(e.message));
  page.on("console", m => { if (m.type() === "error" && !/fonts\.(googleapis|gstatic)|ERR_/.test(m.text())) errors.push(m.text()); });
  await page.addInitScript(`window.__FIX = ${JSON.stringify(FIX)};`);
  await page.addInitScript(mockInit, { scenario });
  if (real) await page.addInitScript(R => { window.__REAL = R; }, real);
  if (storage) await page.addInitScript(s => { try { if (!sessionStorage.getItem("seeded")) { localStorage.setItem("vice-studio-hq:v3:last", s); sessionStorage.setItem("seeded", "1"); } } catch {} }, storage);
  if (insights) await page.addInitScript(s => { try { localStorage.setItem("vice-studio-hq:v3:insights", s); } catch {} }, insights);
  await page.goto("file://" + FILE);
  await page.waitForFunction(() => !/Conectando/.test(document.getElementById("goBtn").textContent));
  return { page, ctx, errors };
}
const go = async (page, { express = false, topic = "" } = {}) => {
  if (express) await page.click("#modeExpress");
  if (topic) await page.fill("#topic", topic);
  await page.click("#goBtn");
};
const idle = page => page.waitForFunction(() => document.getElementById("stopBtn").hidden, null, { timeout: 20000 });
const steps = page => page.$$eval(".stage[data-step]", els => els.map(e => ({ step: e.dataset.step, cls: e.className, qc: [...e.querySelectorAll(".qc .chip")].map(c => c.textContent) })));
const stepOf = async (page, key) => (await steps(page)).find(s => s.step === key);
const statusOf = (page, id) => page.evaluate(id => window.__vshDebug().status[id], id);
const card = page => page.textContent("#agentCard");
const reloadPage = async page => { await page.reload(); await page.waitForFunction(() => !/Conectando/.test(document.getElementById("goBtn").textContent)); };
const KEYS_WEEK = ["trends", "plan", "titles", "thumbs", "script", "retention", "compliance", "shorts", "launch", "greenlight"];

(async () => {
  const browser = await chromium.launch();

  { // 1. Vídeo de la semana completo
    const { page, ctx, errors } = await open(browser, "ok");
    ok("Equipo: 12 puestos en el organigrama", (await page.$$eval(".org .post", e => e.length)) === 12);
    const orgText = await page.textContent("#org");
    ok("Equipo: los 12 nombres aparecen", ["Jarvis", "Almudena", "Torrente", "Nil", "El Chapo", "Pablito", "Nobita", "Cristiano", "Georgina", "Victillor", "Guerrero", "Taison"].every(n => orgText.includes(n)));
    ok("Equipo: los 12 departamentos aparecen", ["El Radar", "La Sala de Mando", "El Escaparate", "Estudio Neón", "La Fábrica de Guiones", "Laboratorio de Retención", "El Escudo", "Estudio Ocean Drive", "La Sala de Montaje", "La Fábrica de Shorts", "Torre de Lanzamiento", "El Observatorio"].every(n => orgText.includes(n)));
    ok("Equipo: 12 personas dibujadas en la oficina", (await page.evaluate(() => window.__vshDebug().hits.length)) === 12);
    await go(page, { topic: "secretos de Vice City" });
    await page.waitForFunction(() => (window.__working || []).length >= 1);
    await page.waitForFunction(() => window.__prompts.length >= 3);
    ok("Oficina: el trabajo viaja de una mesa a otra", (await page.evaluate(() => window.__vshDebug().packets)) > 0);
    await idle(page);
    const st = await steps(page);
    ok("Semana: los 10 pasos automáticos terminan", KEYS_WEEK.every(k => st.find(s => s.step === k && !/pending|failed/.test(s.cls))), JSON.stringify(st.map(s => s.step + ":" + s.cls)));
    ok("Semana: control de calidad sin fallos graves", st.every(s => !s.qc.some(q => q.startsWith("✗"))), JSON.stringify(st.map(s => s.qc)));
    ok("Semana: sin avisos de calidad", st.every(s => !s.qc.some(q => q.startsWith("!"))), JSON.stringify(st.filter(s => s.qc.some(q => q.startsWith("!"))).map(s => s.step + " " + s.qc)));
    const prompts = await page.evaluate(() => window.__prompts);
    const working = await page.evaluate(() => window.__working);
    ok("Oficina: en cada llamada trabaja la persona correcta (y solo ella)", working.join(",") === "jarvis,almudena,torrente,nil,chapo,pablito,nobita,victillor,guerrero,almudena", working.join(","));
    ok("Semana: 10 llamadas, en orden", prompts.length === 10 && ["Jarvis", "Almudena", "Torrente", "Nil", "El Chapo", "Pablito", "Nobita", "Victillor", "Guerrero", "Almudena"].every((n, i) => prompts[i].includes("Eres " + n)), prompts.map(p => (p.match(/Eres (\w+( \w+)?)/) || [])[1]).join(","));
    ok("Experiencia: cada puesto recibe la suya", ["Jarvis", "Almudena", "Torrente", "Nil", "El Chapo", "Pablito", "Nobita", "Victillor", "Guerrero", "Almudena"].every((n, i) => prompts[i].includes("Experiencia de " + n) && prompts[i].includes("nunca comete")));
    ok("Experiencia: va antes del formato de respuesta", prompts.every(p => p.indexOf("Experiencia de") < p.indexOf("Responde solo con JSON")));
    const tiers = await page.evaluate(() => window.__tiers);
    ok("Modelo: títulos, guion, retención y luz verde usan el más capaz", [2, 4, 5, 9].every(i => tiers[i] === "complex") && [0, 1, 3, 6, 7, 8].every(i => tiers[i] === "default"), tiers.join(","));
    ok("Prompts: ninguno supera el límite de 256 KB", prompts.every(p => new TextEncoder().encode(p).length < 250000));
    ok("Semana: el tema llega a Jarvis", /secretos de Vice City/.test(prompts[0]));
    ok("Semana: Almudena recibe los temas de Jarvis", /Comparativa GTA 5/.test(prompts[1]));
    ok("Semana: títulos antes del guion (El Chapo recibe títulos y miniaturas)", /7 secretos de Vice City que casi nadie/.test(prompts[4]) && /Solo de noche/.test(prompts[4]));
    ok("Semana: el guion pide 10 escenas", /Exactamente 10 escenas/.test(prompts[4]));
    ok("Semana: Nobita revisa el guion mejorado por Pablito", /TEXTO MEJORADO POR PABLITO/.test(prompts[6]));
    ok("Semana: Victillor parte del guion mejorado", /TEXTO MEJORADO POR PABLITO/.test(prompts[7]));
    ok("Semana: Guerrero recibe tiempos de escena", /escena 2 empieza en/.test(prompts[8]));
    ok("Semana: Pablito ignora cambios en escenas que no existen", (await page.textContent('[data-step="retention"]')).includes("1 mejoras aplicadas"));
    ok("Semana: 3 miniaturas y 4 Shorts en pantalla", (await page.$$eval('[data-step="thumbs"] .thumb', e => e.length)) === 3 && (await page.$$eval('[data-step="shorts"] .scene', e => e.length)) === 4);
    ok("Luz verde: Almudena revisa todo el paquete", /Pablito: 7\/10/.test(prompts[9]) && /Shorts:/.test(prompts[9]) && /Miniaturas \(A, B, C\)/.test(prompts[9]));
    ok("Luz verde: se muestran las notas", (await page.$$eval('[data-step="greenlight"] .scorebox', e => e.length)) === 4);
    ok("Semana: Cristiano y Georgina esperan en el chat", (await statusOf(page, "cristiano")) === "waiting" && (await statusOf(page, "georgina")) === "waiting");
    ok("Semana: Taison libre (sin datos aún)", (await statusOf(page, "taison")) === "idle");
    await ctx.grantPermissions(["clipboard-read", "clipboard-write"]);
    await page.click('[data-step="handoff"] .actions button');
    const clip = await page.evaluate(() => navigator.clipboard.readText());
    ok("Encargo: usa el título y la miniatura que eligió Almudena", /TÍTULO PRINCIPAL: GTA 6: el lugar que solo aparece de noche/.test(clip) && /MINIATURA PRINCIPAL: opción B/.test(clip) && /CONSEJO DE ALMUDENA/.test(clip));
    ok("Encargo: los otros títulos quedan para probar", /TÍTULOS PARA PROBAR: GTA 6: 7 secretos[^\n]*encontré 7 sitios/.test(clip) && !/PROBAR:[^\n]*solo aparece de noche/.test(clip));
    ok("Encargo: incluye miniaturas A, B y C", /A\) "Solo de noche"/.test(clip) && /C\) "Sitio oculto"/.test(clip));
    ok("Encargo: usa el guion mejorado por Pablito", /TEXTO MEJORADO POR PABLITO/.test(clip));
    ok("Encargo: incluye los 4 Shorts y la descripción con capítulos", /SHORT 4:/.test(clip) && /0:00 Intro/.test(clip));
    ok("Encargo: pide avisar del coste de créditos", /cuántos créditos/.test(clip));
    await reloadPage(page);
    ok("Recarga: se recupera el encargo y los estados", !!(await page.$('[data-step="handoff"]')) && (await statusOf(page, "cristiano")) === "waiting");
    await page.click(".org .post:nth-child(7)");
    ok("Ficha: el organigrama abre la de Nobita", /Nobita/.test(await card(page)) && /Guardián de normas/.test(await card(page)) && /Se lo pasa a/.test(await card(page)));
    await page.$eval("#office", e => e.scrollIntoView({ block: "center" }));
    const hit = await page.evaluate(() => window.__vshDebug().hits.find(h => h.id === "taison"));
    const box = await page.$eval("#office", e => e.getBoundingClientRect().toJSON());
    await page.mouse.click(box.x + hit.x, box.y + hit.y);
    ok("Ficha: tocar a Taison en la oficina abre la suya", /Taison/.test(await card(page)) && /Analista y comunidad/.test(await card(page)));
    ok("Semana: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 2. Short exprés
    const { page, ctx, errors } = await open(browser, "ok");
    await go(page, { express: true });
    await idle(page);
    const prompts = await page.evaluate(() => window.__prompts);
    ok("Exprés: 8 llamadas (sin miniaturas ni Shorts)", prompts.length === 8 && !prompts.some(p => /Eres Nil|Eres Victillor/.test(p)), String(prompts.length));
    ok("Exprés: el guion pide 6 escenas", prompts.some(p => /Exactamente 6 escenas/.test(p)));
    const st = await steps(page);
    ok("Exprés: no muestra puestos que no tocan", !st.some(s => s.step === "thumbs" || s.step === "shorts"));
    ok("Exprés: sin fallos de calidad", st.every(s => !s.qc.some(q => q.startsWith("✗") || q.startsWith("!"))), JSON.stringify(st.map(s => s.qc)));
    ok("Exprés: aparece el encargo para el chat", !!(await page.$('[data-step="handoff"]')));
    ok("Exprés: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 3. Respuestas desordenadas
    const { page, ctx, errors } = await open(browser, "messy");
    await go(page);
    await idle(page);
    const st = await steps(page);
    ok("Desordenado: la página no se rompe", errors.length === 0, errors.join(" | "));
    ok("Desordenado: la lista en texto se convierte en temas", (await page.$$eval('[data-step="trends"] li', e => e.length)) === 5);
    ok("Desordenado: avisa de títulos largos y sin GTA 6", (await stepOf(page, "titles")).qc.filter(q => q.startsWith("!")).length >= 2);
    ok("Desordenado: avisa de miniaturas largas", (await stepOf(page, "thumbs")).qc.some(q => q.startsWith("!")));
    ok("Desordenado: avisa de guion corto y textos largos", (await stepOf(page, "script")).qc.filter(q => q.startsWith("!")).length >= 2);
    ok("Desordenado: un Short demasiado corto se avisa", (await stepOf(page, "shorts")).qc.some(q => q.startsWith("!")));
    ok("Desordenado: avisa de falta de aviso no oficial y de capítulos", (await stepOf(page, "launch")).qc.filter(q => q.startsWith("!")).length >= 3);
    ok("Desordenado: todos los puestos terminan", st.filter(s => KEYS_WEEK.includes(s.step)).every(s => !/failed|pending/.test(s.cls)));
    await ctx.close();
  }

  { // 4. Guion vacío
    const { page, ctx, errors } = await open(browser, "bad_script");
    await go(page);
    await idle(page);
    ok("Guion vacío: se para en El Chapo", /failed/.test((await stepOf(page, "script")).cls) && (await statusOf(page, "chapo")) === "error");
    ok("Guion vacío: los siguientes quedan pendientes", /pending/.test((await stepOf(page, "retention")).cls));
    await page.click('[data-step="script"] button.strong');
    await idle(page);
    const prompts = await page.evaluate(() => window.__prompts);
    ok("Guion vacío: seguir completa el encargo sin repetir a Jarvis", !!(await page.$('[data-step="handoff"]')) && prompts.filter(p => /Eres Jarvis/.test(p)).length === 1);
    ok("Guion vacío: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 5. Sin permiso
    const { page, ctx } = await open(browser, "deny");
    await go(page);
    await idle(page);
    ok("Sin permiso: explica qué hacer y desactiva botones", /permiso/.test(await page.textContent("#capNote")) && await page.$eval("#goBtn", b => b.disabled) && await page.$eval("#obsBtn", b => b.disabled));
    await ctx.close();
  }

  { // 6. Parar y seguir
    const { page, ctx, errors } = await open(browser, "slow");
    await go(page);
    await page.waitForFunction(() => window.__prompts.length === 3);
    await page.click("#stopBtn");
    await idle(page);
    ok("Parar: se queda en Torrente", /failed/.test((await stepOf(page, "titles")).cls) && /Has parado/.test(await page.textContent('[data-step="titles"]')));
    ok("Parar: nadie sigue trabajando", !(await page.evaluate(() => Object.values(window.__vshDebug().status).includes("working"))));
    await page.click('[data-step="titles"] button.strong');
    await idle(page);
    ok("Parar: al seguir termina", !!(await page.$('[data-step="handoff"]')));
    ok("Parar: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 7. Nobita frena → correcciones
    const { page, ctx, errors } = await open(browser, "reject_then_fix");
    await go(page);
    await idle(page);
    const n1 = await page.evaluate(() => window.__prompts.length);
    ok("Frenado: no se hacen Shorts, ficha ni luz verde hasta corregir", n1 === 7, String(n1));
    ok("Frenado: aparece el aviso justo después de Nobita", (await steps(page)).map(s => s.step).join(",").includes("compliance,fix-box"));
    ok("Frenado: Nobita en rojo y sin encargo", (await statusOf(page, "nobita")) === "error" && !(await page.$('[data-step="handoff"]')));
    await reloadPage(page);
    ok("Frenado: tras recargar sigue mostrando 'Pedir correcciones'", !!(await page.$('[data-step="fix-box"]')));
    await page.click('[data-step="fix-box"] button');
    await idle(page);
    ok("Corrección: queda aprobado y se completan Shorts y ficha", !!(await page.$('[data-step="handoff"]')) && !/pending/.test((await stepOf(page, "launch")).cls),
      JSON.stringify({ steps: (await steps(page)).map(s => s.step + ":" + s.cls + ":" + s.qc.join("/")), prompts: await page.evaluate(() => window.__prompts.map(p => (p.match(/(Eres|Sois) \S+/) || [])[0])), note: await page.textContent("#capNote") }));
    ok("Corrección: el título cambia y se marca corregido", /corregido/.test(await page.textContent('[data-step="titles"]')) && /corregido ×1/.test(await page.textContent('[data-step="titles"]')));
    ok("Corrección: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 8. Encargo a medias guardado
    const half = JSON.stringify({ mode: "week", topic: "", createdAt: 1, stages: { trends: FIX.trends, plan: { ...FIX.plan } }, checks: {}, revisions: 0, stopAt: null });
    const { page, ctx, errors } = await open(browser, "ok", { storage: half });
    ok("A medias: ofrece seguir desde Torrente", /Seguir desde Torrente/.test(await page.textContent("#results")));
    await page.click('[data-step="titles"] button.strong');
    await idle(page);
    ok("A medias: al seguir termina", !!(await page.$('[data-step="handoff"]')));
    ok("A medias: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 9. Fuera de Claude
    const { page, ctx, errors } = await open(browser, "no_claude");
    ok("Fuera de Claude: avisa y desactiva", (await page.$eval("#goBtn", b => b.disabled)) && /Abre esta página dentro de Claude/.test(await page.textContent("#capNote")));
    ok("Fuera de Claude: el ejemplo se ve completo", !!(await page.$('[data-step="handoff"]')) && (await page.$$eval(".stage[data-step]", e => e.length)) === 11);
    ok("Fuera de Claude: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 10. El Observatorio
    const { page, ctx, errors } = await open(browser, "ok");
    await page.fill("#obsData", "corto");
    await page.click("#obsBtn");
    ok("Observatorio: pide datos si están vacíos", /al menos un vídeo/.test(await page.textContent("#obsOut")));
    await page.fill("#obsData", "5 secretos de Vice City — 12.400 visualizaciones — clics 7,8 % — vista media 3:10 de 9:00 — +210 suscriptores");
    await page.click("#obsBtn");
    await idle(page);
    ok("Observatorio: Taison entrega conclusiones", /doble de clics/.test(await page.textContent("#obsOut")) && (await statusOf(page, "taison")) === "done");
    await go(page);
    await idle(page);
    const prompts = await page.evaluate(() => window.__prompts);
    ok("Observatorio: Jarvis, Almudena y Torrente usan las conclusiones", ["Jarvis", "Almudena", "Torrente"].every(n => prompts.find(p => p.includes("Eres " + n))?.includes("Conclusiones de Taison")));
    await reloadPage(page);
    ok("Observatorio: las conclusiones se guardan", /doble de clics/.test(await page.textContent("#obsOut")));
    ok("Observatorio: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 11. Almudena pide rehacer
    const { page, ctx, errors } = await open(browser, "redo");
    await go(page);
    await idle(page);
    ok("Rehacer: aparece el aviso de Almudena", !!(await page.$('[data-step="redo-box"]')) && /Rehacer desde Torrente/.test(await page.textContent('[data-step="redo-box"]')));
    ok("Rehacer: Almudena en rojo y sin encargo", (await statusOf(page, "almudena")) === "error" && !(await page.$('[data-step="handoff"]')));
    ok("Rehacer: la nota baja se marca", (await page.$$eval('[data-step="greenlight"] .scorebox.low', e => e.length)) === 1);
    const before = await page.evaluate(() => window.__prompts.length);
    await page.click('[data-step="redo-box"] button.strong');
    await idle(page);
    const prompts = await page.evaluate(() => window.__prompts);
    ok("Rehacer: repite desde Torrente sin volver a Jarvis ni al plan", prompts.length - before === 8 && prompts.filter(p => /Eres Jarvis/.test(p)).length === 1, String(prompts.length - before));
    ok("Rehacer: después hay luz verde y encargo", !!(await page.$('[data-step="handoff"]')));
    ok("Rehacer: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 12. Seguir igualmente
    const { page, ctx, errors } = await open(browser, "redo_override");
    await go(page);
    await idle(page);
    await page.click('[data-step="redo-box"] button:not(.strong)');
    ok("Seguir igualmente: aparece el encargo", !!(await page.$('[data-step="handoff"]')) && (await statusOf(page, "cristiano")) === "waiting");
    await reloadPage(page);
    ok("Seguir igualmente: se recuerda al recargar", !!(await page.$('[data-step="handoff"]')));
    ok("Seguir igualmente: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 13. Ficha con experiencia
    const { page, ctx } = await open(browser, "ok");
    for (const [i, name] of [[1, "Jarvis"], [6, "Pablito"], [12, "Taison"]]) {
      await page.click(`.org .post:nth-child(${i})`);
      const txt = await card(page);
      ok(`Ficha de ${name}: experiencia, saberes y errores`, txt.includes(name) && /Experiencia/.test(txt) && /Lo que sabe y aplica/.test(txt) && /Errores que nunca comete/.test(txt));
    }
    await ctx.close();
  }

  { // 14. Encargo real (respuestas escritas por Claude siguiendo cada instrucción)
    const REAL = JSON.parse(fs.readFileSync(path.join(__dirname, "pruebas_reales", "respuestas.json"), "utf8"));
    const { page, ctx, errors } = await open(browser, "real", { real: REAL });
    await go(page, { topic: "qué explorar primero en Leonida" });
    await idle(page);
    const st = await steps(page);
    ok("Real: los 10 pasos pasan el control de calidad sin avisos", KEYS_WEEK.every(k => { const s = st.find(x => x.step === k); return s && !/failed|pending/.test(s.cls) && s.qc.every(q => q.startsWith("✓")); }), JSON.stringify(st.map(s => s.step + ":" + s.qc.filter(q => !q.startsWith("✓")).join("/"))));
    ok("Real: aparece el encargo final", !!(await page.$('[data-step="handoff"]')));
    ok("Real: sin errores de JavaScript", errors.length === 0, errors.join(" | "));
    await ctx.close();
  }

  { // 15. Pantallas
    const countOverlaps = tags => {
      let n = 0;
      for (let i = 0; i < tags.length; i++) for (let j = i + 1; j < tags.length; j++) {
        const a = tags[i], b = tags[j];
        if (a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h) n++;
      }
      return n;
    };
    for (const w of [390, 768, 1024, 1366]) {
      const { page, ctx } = await open(browser, "paced", { width: w });
      ok(`${w}px: sin desplazamiento lateral`, (await page.evaluate(() => document.documentElement.scrollWidth)) <= w);
      await go(page);
      await page.waitForFunction(() => typeof window.__release === "function");
      await page.waitForTimeout(120);
      await page.waitForTimeout(80);
      const busyTags = await page.evaluate(() => window.__vshDebug().tags);
      ok(`${w}px: nombres y bocadillos no se pisan mientras trabajan`, countOverlaps(busyTags) === 0 && busyTags.some(t => t.id === "chapo:bubble"), `${countOverlaps(busyTags)} solapes`);
      await page.evaluate(() => window.__release());
      await idle(page);
      await page.waitForTimeout(80);
      const tags = await page.evaluate(() => window.__vshDebug().tags);
      ok(`${w}px: al terminar no se pisan`, countOverlaps(tags) === 0, `${countOverlaps(tags)} solapes`);
      ok(`${w}px: todo dentro de la oficina`, tags.every(t => t.y >= 0 && t.x >= 0 && t.x + t.w <= w), JSON.stringify(tags.filter(t => t.y < 0 || t.x < 0 || t.x + t.w > w)));
      if (w === 1024) await page.screenshot({ path: path.join(SHOTS, "v3_ipad.png") });
      if (w === 390) await page.screenshot({ path: path.join(SHOTS, "v3_phone.png") });
      await ctx.close();
    }
  }

  await browser.close();
  const failed = results.filter(r => !r.pass);
  for (const r of results) console.log(`${r.pass ? "✓" : "✗"} ${r.name}${r.pass || !r.detail ? "" : "  → " + r.detail}`);
  console.log(`\n${results.length - failed.length}/${results.length} pruebas superadas`);
  process.exit(failed.length ? 1 : 0);
})().catch(e => {
  for (const r of results) console.log(`${r.pass ? "✓" : "✗"} ${r.name}${r.pass || !r.detail ? "" : "  → " + r.detail}`);
  console.error(e); process.exit(2);
});
