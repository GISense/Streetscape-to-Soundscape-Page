const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
const RESPONSES_DIR = path.join(__dirname, "responses");

app.use(express.json());

app.use(express.static(__dirname, {
  index: false,
  extensions: ["html"]
}));

app.get("/", (_req, res) => {
  res.sendFile(path.join(__dirname, "user_study.html"));
});

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function timestamp() {
  return new Date().toISOString().replace(/[:.]/g, "-");
}

// S2S endpoint — expects: [{ trial, scene_id, selected_option }, ...]
app.post("/api/s2s", (req, res) => {
  const rows = req.body;
  if (!Array.isArray(rows) || rows.length === 0) {
    return res.status(400).json({ error: "Invalid payload" });
  }

  const dir = path.join(RESPONSES_DIR, "s2s");
  ensureDir(dir);

  const header = "trial,scene_id,selected_option";
  const csv = [header, ...rows.map(r => `${r.trial},${r.scene_id},${r.selected_option}`)].join("\n");

  const file = path.join(dir, `s2s_${timestamp()}.csv`);
  fs.writeFileSync(file, csv, "utf-8");
  console.log("Saved:", file);
  res.json({ ok: true, file: path.basename(file) });
});

// Q2 endpoint — expects: [{ q: "Q2", questionNumber, option }, ...]
app.post("/api/q2", (req, res) => {
  const rows = req.body;
  if (!Array.isArray(rows) || rows.length === 0) {
    return res.status(400).json({ error: "Invalid payload" });
  }

  const dir = path.join(RESPONSES_DIR, "q2");
  ensureDir(dir);

  const header = "question_number,selected_option";
  const csv = [header, ...rows.map(r => `${r.questionNumber},${r.option}`)].join("\n");

  const file = path.join(dir, `q2_${timestamp()}.csv`);
  fs.writeFileSync(file, csv, "utf-8");
  console.log("Saved:", file);
  res.json({ ok: true, file: path.basename(file) });
});

// Q1 endpoint — expects: [{ q: "Q1", questionNumber, options: [...] }, ...]
app.post("/api/q1", (req, res) => {
  const rows = req.body;
  if (!Array.isArray(rows) || rows.length === 0) {
    return res.status(400).json({ error: "Invalid payload" });
  }

  const dir = path.join(RESPONSES_DIR, "q1");
  ensureDir(dir);

  const header = "question_number,selected_options";
  const csv = [header, ...rows.map(r => {
    const opts = Array.isArray(r.options) ? r.options.join(";") : r.options;
    return `${r.questionNumber},${opts}`;
  })].join("\n");

  const file = path.join(dir, `q1_${timestamp()}.csv`);
  fs.writeFileSync(file, csv, "utf-8");
  console.log("Saved:", file);
  res.json({ ok: true, file: path.basename(file) });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
  console.log(`Responses will be saved to: ${RESPONSES_DIR}`);
});
