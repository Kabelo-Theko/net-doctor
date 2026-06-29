// net-doctor — AI error-code explainer (Vercel serverless function).
//
// The browser POSTs { input: "<error code or message>" } and gets back
// { explanation, layer } where layer is one of Link / IP / Gateway / DNS / App.
// The NVIDIA API key lives ONLY in the NVIDIA_API_KEY environment variable
// (set in the Vercel project settings) — never in the repo or the client.
// If the key is absent, the function returns 503 and the UI falls back to the
// rule-based diagnostics, so the static demo keeps working without a backend.

const ENDPOINT = "https://integrate.api.nvidia.com/v1/chat/completions";
const MODEL = "deepseek-ai/deepseek-v4-flash";

const SYSTEM = `You are a first-line IT network support assistant.
Given an error code or short message a user reports, respond ONLY with compact JSON:
{"explanation":"<2 plain-English sentences: what this usually means>","layer":"<one of: Link, IP, Gateway, DNS, App>"}
Pick the layer where a technician should START checking. No markdown, no extra text.`;

module.exports = async (req, res) => {
  if (req.method !== "POST") { res.status(405).json({ error: "POST only" }); return; }
  const key = process.env.NVIDIA_API_KEY;
  if (!key) { res.status(503).json({ error: "AI backend not configured" }); return; }

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }
  if (!body) {
    body = await new Promise((resolve) => {
      let raw = ""; req.on("data", (c) => (raw += c)); req.on("end", () => { try { resolve(JSON.parse(raw || "{}")); } catch { resolve({}); } });
    });
  }
  const input = (body.input || "").toString().slice(0, 400).trim();
  if (!input) { res.status(400).json({ error: "no input" }); return; }

  const payload = {
    model: MODEL,
    messages: [{ role: "system", content: SYSTEM }, { role: "user", content: input }],
    max_tokens: 400, temperature: 0.2, top_p: 0.95, stream: false,
    chat_template_kwargs: { thinking: false },
  };

  try {
    const r = await fetch(ENDPOINT, {
      method: "POST",
      headers: { Authorization: "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!r.ok) { res.status(502).json({ error: "upstream " + r.status }); return; }
    const data = await r.json();
    const text = data.choices?.[0]?.message?.content?.trim() || "";
    let out = { explanation: text, layer: "" };
    const m = text.match(/\{[\s\S]*\}/);
    if (m) { try { const j = JSON.parse(m[0]); out = { explanation: j.explanation || text, layer: j.layer || "" }; } catch {} }
    res.status(200).json(out);
  } catch (e) {
    res.status(502).json({ error: "request failed" });
  }
};
