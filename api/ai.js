// net-doctor — AI serverless harness (Vercel function). Tasks:
//   "explain" (default): error code/message -> {explanation, layer}
//   "route": free-text symptom -> {flow, layer, plan} (picks one of the 4 flows)
//   "narrative": a finished session -> {note} (a copyable escalation paragraph)
// Model toggle: flash (default) / pro / minimax. One NVIDIA_API_KEY powers all.

const ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions";
const MODELS = {
  flash:   { id: "deepseek-ai/deepseek-v4-flash", keys: ["NVIDIA_API_KEY_FLASH", "NVIDIA_API_KEY"], extra: { chat_template_kwargs: { thinking: false } } },
  pro:     { id: "deepseek-ai/deepseek-v4-pro",   keys: ["NVIDIA_API_KEY_PRO", "NVIDIA_API_KEY"],   extra: { chat_template_kwargs: { thinking: false } } },
  minimax: { id: "minimaxai/minimax-m3",          keys: ["NVIDIA_API_KEY_MINIMAX", "NVIDIA_API_KEY"], extra: {} },
};
const cfgFor = (m) => MODELS[m] || MODELS.flash;
const keyFor = (c) => { for (const e of c.keys) { if (process.env[e]) return process.env[e]; } return null; };
async function readBody(req) {
  let b = req.body;
  if (typeof b === "string") { try { b = JSON.parse(b); } catch { b = {}; } }
  if (!b) { b = await new Promise((res) => { let raw = ""; req.on("data", c => raw += c); req.on("end", () => { try { res(JSON.parse(raw || "{}")); } catch { res({}); } }); }); }
  return b || {};
}
const jsonFrom = (t) => { const m = t.match(/\{[\s\S]*\}/); if (!m) return null; try { return JSON.parse(m[0]); } catch { return null; } };
async function callModel(cfg, key, messages, max_tokens, temperature) {
  const payload = { model: cfg.id, messages, max_tokens, temperature, top_p: 0.95, stream: false, ...cfg.extra };
  const ctrl = new AbortController(); const to = setTimeout(() => ctrl.abort(), 55000);
  try {
    const r = await fetch(ENDPOINT, { method: "POST", headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" }, body: JSON.stringify(payload), signal: ctrl.signal });
    clearTimeout(to);
    if (!r.ok) return { error: "upstream " + r.status };
    const d = await r.json();
    return { text: (d.choices?.[0]?.message?.content || "").trim() };
  } catch (e) { clearTimeout(to); return { error: "request failed" }; }
}

const SYS_EXPLAIN = `You are a first-line IT network support assistant. Given an error code or short message, respond ONLY with compact JSON:
{"explanation":"<2 plain-English sentences>","layer":"<one of: Link, IP, Gateway, DNS, App>"}
Pick the layer to START at. No markdown, no extra text.`;
const SYS_ROUTE = `You route a user's plain-English network complaint to the right diagnostic. Respond ONLY with compact JSON:
{"flow":"<one of: one-pc-no-internet, site-down-whole-office, cant-reach-internal-vpn, wifi-drops>","layer":"<one of: Link, IP, Gateway, DNS, App>","plan":"<one sentence on where to start and why>"}
No markdown, no extra text.`;
const SYS_NARRATIVE = `You write a concise escalation note for second-line IT from a completed first-line diagnostic. Given the symptom, the checks done (each pass/fail) and the conclusion, write ONE short paragraph (50-90 words): what was checked, what failed, the probable cause, and what second-line should do next. Plain, factual, no markdown, no em dashes. Respond ONLY with compact JSON: {"note":"<paragraph>"}`;

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ error: "POST only" }); return; }
  const body = await readBody(req);
  const cfg = cfgFor(body.model);
  const key = keyFor(cfg);
  if (!key) { res.status(503).json({ error: "AI backend not configured" }); return; }
  const task = body.task || "explain";

  if (task === "route") {
    const input = (body.input || "").toString().slice(0, 500).trim();
    if (!input) { res.status(400).json({ error: "no input" }); return; }
    const out = await callModel(cfg, key, [{ role: "system", content: SYS_ROUTE }, { role: "user", content: input }], 250, 0.2);
    if (out.error) { res.status(502).json({ error: out.error }); return; }
    const j = jsonFrom(out.text) || {};
    res.status(200).json({ flow: j.flow || "", layer: j.layer || "", plan: j.plan || "", model: cfg.id });
    return;
  }
  if (task === "narrative") {
    const s = body.session || {};
    const steps = Array.isArray(s.steps) ? s.steps.map(x => `- ${x.passed ? "OK" : "FAIL"}: ${x.text}`).join("\n") : "";
    const user = `Symptom: ${s.title || ""}\nChecks:\n${steps}\nProbable cause: ${s.cause || ""}\nFix tried: ${s.fix || ""}\nEscalation guidance: ${s.escalate || ""}`;
    const out = await callModel(cfg, key, [{ role: "system", content: SYS_NARRATIVE }, { role: "user", content: user }], 320, 0.4);
    if (out.error) { res.status(502).json({ error: out.error }); return; }
    const j = jsonFrom(out.text) || { note: out.text };
    res.status(200).json({ note: j.note || out.text, model: cfg.id });
    return;
  }
  // default: explain
  const input = (body.input || "").toString().slice(0, 400).trim();
  if (!input) { res.status(400).json({ error: "no input" }); return; }
  const out = await callModel(cfg, key, [{ role: "system", content: SYS_EXPLAIN }, { role: "user", content: input }], 400, 0.2);
  if (out.error) { res.status(502).json({ error: out.error }); return; }
  const j = jsonFrom(out.text) || {};
  res.status(200).json({ explanation: j.explanation || out.text, layer: j.layer || "", model: cfg.id });
};
