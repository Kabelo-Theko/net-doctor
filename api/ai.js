// net-doctor — AI error-code explainer (Vercel serverless function).
// Model toggle: "flash" (default), "pro", "minimax". One NVIDIA_API_KEY powers
// all three (optional per-model overrides). Key stays server-side only.

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

const SYSTEM = `You are a first-line IT network support assistant.
Given an error code or short message a user reports, respond ONLY with compact JSON:
{"explanation":"<2 plain-English sentences: what this usually means>","layer":"<one of: Link, IP, Gateway, DNS, App>"}
Pick the layer where a technician should START checking. No markdown, no extra text.`;

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ error: "POST only" }); return; }
  const body = await readBody(req);
  const cfg = cfgFor(body.model);
  const key = keyFor(cfg);
  if (!key) { res.status(503).json({ error: "AI backend not configured" }); return; }
  const input = (body.input || "").toString().slice(0, 400).trim();
  if (!input) { res.status(400).json({ error: "no input" }); return; }

  const payload = { model: cfg.id, messages: [{ role: "system", content: SYSTEM }, { role: "user", content: input }], max_tokens: 400, temperature: 0.2, top_p: 0.95, stream: false, ...cfg.extra };
  const ctrl = new AbortController(); const to = setTimeout(() => ctrl.abort(), 55000);
  try {
    const r = await fetch(ENDPOINT, { method: "POST", headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" }, body: JSON.stringify(payload), signal: ctrl.signal });
    clearTimeout(to);
    if (!r.ok) { res.status(502).json({ error: "upstream " + r.status }); return; }
    const d = await r.json();
    const text = (d.choices?.[0]?.message?.content || "").trim();
    const j = jsonFrom(text) || {};
    res.status(200).json({ explanation: j.explanation || text, layer: j.layer || "", model: cfg.id });
  } catch (e) { clearTimeout(to); res.status(502).json({ error: "request failed" }); }
};
