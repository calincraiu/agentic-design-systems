// Course app widgets. A slide asks for one with <div data-widget="name" data-...></div>.
// Every widget that runs a tool shows "Behind the scenes": the command and the tool's raw answer.

const el = (tag, attrs = {}, ...kids) => {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v);
  }
  for (const k of kids.flat()) if (k != null) e.append(k.nodeType ? k : document.createTextNode(k));
  return e;
};

const getJSON = async (url, opts) => {
  const r = await fetch(url, opts);
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(data.detail || r.statusText);
  return data;
};

function behind(result) {
  const out = [result.stdout, result.stderr].filter(Boolean).join("\n").trim() || "(no output)";
  return el("details", { class: "behind" },
    el("summary", {}, "Behind the scenes: what the agent would run, and what the tool said"),
    el("pre", {}, el("code", { class: "prompt-line" }, result.command)),
    el("pre", {}, out));
}

// ---------------------------------------------------------------- dice
function dice(root) {
  const sides = el("input", { type: "number", min: 2, value: root.dataset.sides || 6 });
  const count = el("input", { type: "number", min: 1, max: 20, value: root.dataset.count || 2 });
  const faces = el("div", { class: "dice" });
  const total = el("p", { class: "muted" });
  const extra = el("div");
  const button = el("button", { onclick: roll }, "Roll");
  async function roll() {
    button.disabled = true;
    try {
      const r = await getJSON(`/api/dice?sides=${sides.value}&count=${count.value}`);
      faces.replaceChildren(...r.rolls.map(n => el("div", { class: "die" }, String(n))));
      total.textContent = r.code === 0 ? `Total: ${r.rolls.reduce((a, b) => a + b, 0)}` : "";
      extra.replaceChildren(r.code !== 0 ? el("p", { class: "err" }, r.stderr) : "", behind(r));
    } catch (e) { extra.replaceChildren(el("p", { class: "err" }, e.message)); }
    button.disabled = false;
  }
  root.append(el("h4", {}, "Dice tool"),
    el("div", { class: "row" }, el("label", {}, "sides", sides), el("label", {}, "count", count), button),
    faces, total, extra);
}

// ---------------------------------------------------------------- llm vs tool
function llmVsTool(root) {
  const input = el("textarea", { rows: 2, placeholder: "Type the class's answers here, e.g. 17 7 17 13 7 17 ..." });
  const classHist = el("div", { class: "hist" }), toolHist = el("div", { class: "hist tool" });
  const classNote = el("p", { class: "muted" }), toolNote = el("p", { class: "muted" }), extra = el("div");
  const axis = () => el("div", { class: "axis" }, ...Array.from({ length: 20 }, (_, i) => el("span", {}, String(i + 1))));
  const draw = (hist, note, nums, who) => {
    const counts = Array(20).fill(0);
    nums.forEach(n => { if (n >= 1 && n <= 20) counts[n - 1]++; });
    const max = Math.max(1, ...counts);
    hist.replaceChildren(...counts.map((c, i) => el("div", { style: `height:${(c / max) * 100}%`, title: `${i + 1}: ${c}` })));
    const top = counts.indexOf(Math.max(...counts));
    const n = counts.reduce((a, b) => a + b, 0);
    note.textContent = n ? `${who}: ${n} numbers. Most common: ${top + 1} (${counts[top]} times, ${Math.round(100 * counts[top] / n)}%). Never chosen: ${counts.filter(c => !c).length} of 20.` : "";
  };
  input.addEventListener("input", () => draw(classHist, classNote, (input.value.match(/\d+/g) || []).map(Number), "The class (an LLM, many times)"));
  const button = el("button", { onclick: async () => {
    button.disabled = true;
    const r = await getJSON("/api/dice?sides=20&count=200");
    draw(toolHist, toolNote, r.rolls, "The dice tool (200 real rolls of a d20)");
    extra.replaceChildren(behind({ ...r, stdout: r.stdout.slice(0, 400) + (r.stdout.length > 400 ? " …" : "") }));
    button.disabled = false;
  } }, "Roll 200 real d20s");
  root.append(el("h4", {}, "An LLM's 'random' numbers vs a tool's"),
    input, classHist, axis(), classNote,
    el("div", { class: "row" }, button), toolHist, axis(), toolNote, extra);
}

// ---------------------------------------------------------------- tower explorer
async function towerWidget(root) {
  const spec = await getJSON("/api/tower/spec");
  const preset = JSON.parse(root.dataset.params || "{}");
  const values = {}, rows = [];
  for (const p of spec.params) {
    values[p.name] = preset[p.name] ?? p.default;
    const out = el("output", {}, fmt(values[p.name], p.unit));
    const step = p.int ? 1 : (p.high - p.low > 50 ? 1 : 0.1);
    const slider = el("input", { type: "range", min: p.low, max: p.high, step, value: values[p.name], title: p.meaning });
    slider.addEventListener("input", () => { values[p.name] = Number(slider.value); out.textContent = fmt(values[p.name], p.unit); });
    rows.push(el("div", { class: "param", title: p.meaning }, el("span", {}, p.name), slider, out));
  }
  const plot = el("input", { type: "text", value: root.dataset.plot || "", placeholder: "e.g. 20x20", size: 8 });
  const require = el("textarea", { rows: 2, placeholder: 'one limit per line, e.g. height_m>60' });
  require.value = (root.dataset.require || "").split(";").filter(Boolean).join("\n");
  const label = el("input", { type: "text", placeholder: "label, e.g. A: slim beacon", size: 22 });
  const result = el("div", {}, el("p", { class: "muted" }, "Set the eight numbers, then build. These sliders are everything the tool can be asked to do."));
  let last = null;
  const build = async (again) => {
    buildBtn.disabled = againBtn.disabled = true;
    try {
      const r = await getJSON("/api/tower", { method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ params: values, plot: plot.value, require: require.value.split("\n"), label: label.value }) });
      showTower(r, again ? last : null);
      if (r.run) last = r.run;
    } catch (e) { result.replaceChildren(el("p", { class: "err" }, e.message)); }
    buildBtn.disabled = againBtn.disabled = false;
  };
  const showTower = (r, previous) => {
    if (!r.run) { result.replaceChildren(el("p", { class: "err" }, r.stderr || "The tool refused."), behind(r)); return; }
    const m = r.run.metrics;
    const table = el("table", { class: "metrics" }, ...spec.metrics.filter(x => m[x.name] != null).map(x =>
      el("tr", { title: x.meaning }, el("td", {}, x.label), el("td", {}, fmt(m[x.name], x.unit)))));
    const checks = r.run.limits.map(c => el("div", { class: c.pass ? "pass" : "fail" },
      `${c.pass ? "PASS" : "FAIL"}  ${c.metric} ${c.op} ${c.value} (actual ${c.actual})`));
    let same = null;
    if (previous) {
      const identical = JSON.stringify(previous.metrics) === JSON.stringify(m);
      same = el("p", { class: "same" }, identical ? "Same numbers in, same tower out: every metric is identical to the last build." : "Different from the last build: did a number change?");
    }
    result.replaceChildren(el("div", { class: "cols" }, el("img", { src: r.image, alt: r.run.label }),
      el("div", {}, same, table, ...checks)), behind(r));
  };
  const buildBtn = el("button", { onclick: () => build(false) }, "Build");
  const againBtn = el("button", { class: "ghost", onclick: () => build(true) }, "Build the same again");
  root.append(el("h4", {}, "Tower tool"), el("div", { class: "tower" },
    el("div", {}, ...rows,
      el("div", { class: "row" }, el("label", {}, "plot", plot), label),
      require, el("div", { class: "row" }, buildBtn, againBtn)),
    result));
}
const fmt = (v, unit = "") => {
  const s = Math.abs(v) >= 100 ? Math.round(v).toLocaleString() : String(Math.round(v * 100) / 100);
  return unit && unit !== "x" ? `${s} ${unit}` : unit === "x" ? `${s}×` : s;
};

// ---------------------------------------------------------------- file viewer
async function fileWidget(root) {
  const f = await getJSON(`/api/file?path=${encodeURIComponent(root.dataset.path)}&render_md=${root.dataset.render === "markdown"}`);
  root.classList.add("file");
  root.append(el("h4", {}, root.dataset.title || f.path));
  if (root.dataset.render === "markdown") { const d = el("div"); d.innerHTML = f.html; root.append(d); return; }
  const hl = new Set();
  for (const part of (root.dataset.highlight || "").split(",").filter(Boolean)) {
    const [a, b] = part.split("-").map(Number);
    for (let i = a; i <= (b || a); i++) hl.add(i);
  }
  const lines = f.text.replace(/\n$/, "").split("\n");
  root.append(el("pre", {}, ...lines.map((t, i) => el("span", { class: "ln" + (hl.has(i + 1) ? " hl" : "") }, t || " "))));
}

// ---------------------------------------------------------------- skill anatomy
const NOTES = {
  frontmatter: ["When to use it", "The name and description. At the start of every session Claude sees only these lines, for every skill. The description is how it decides when this skill fits. Vague description, wrong moments."],
  role: ["Role", "Who the agent is while using this skill, and the one thing it must keep in mind. Short and firm."],
  workflow: ["Workflow", "The steps, in order. Each one is a decision you made about how this kind of task should go. The agent follows them, but it still decides how to do each step."],
  rules: ["Guardrails", "What it must and must never do. The agent can still break a rule. That's why the tool exists: a skill can tell Claude not to make up a roll, but only the tool can actually roll."],
  stance: ["Design stance", "The values that shape the options. Change this and the same workflow gives different towers."],
  tool: ["The tool", "Which tool to use and how to call it. The skill can't give the tool new abilities: it can only use the ones listed by --help."],
  section: ["Supporting know-how", "Reference material the agent reads while working: formats, examples, tables of typical moves."],
};
async function skillWidget(root) {
  const f = await getJSON(`/api/file?path=${encodeURIComponent(root.dataset.path)}`);
  const segs = [];
  let text = f.text, section = "";
  const fm = text.match(/^---\n[\s\S]*?\n---\n/);
  if (fm) { segs.push({ kind: "frontmatter", text: fm[0].trim() }); text = text.slice(fm[0].length); }
  for (const block of text.split(/\n(?=#{1,3} )/)) {
    const heading = (block.match(/^#{1,3} (.+)/) || [])[1] || "";
    if (heading) section = heading.toLowerCase();
    const kind = /rule/.test(section) ? "rules" : /stance/.test(section) ? "stance" : /^tool/.test(section) ? "tool"
      : /workflow|steps/.test(section) ? "workflow" : /^#\s/.test(block) ? (/^\s*\d+\./m.test(block) ? "workflow" : "role") : "section";
    if (block.trim()) segs.push({ kind, text: block.trim() });
  }
  // Split a top-level block like "# Tie-breaker / intro / 1. 2. 3." into role and workflow
  const out = [];
  for (const s of segs) {
    const m = s.kind === "workflow" && /^# /.test(s.text) ? s.text.match(/^([\s\S]*?)\n(?=\d+\.)([\s\S]*)$/) : null;
    if (m) { out.push({ kind: "role", text: m[1].trim() }, { kind: "workflow", text: m[2].trim() }); } else out.push(s);
  }
  const note = el("div", { class: "box note" }, el("p", { class: "muted" }, "Click a part of the skill to see what it does."));
  const nodes = out.map(s => el("div", { class: "seg", onclick: e => {
    nodes.forEach(n => n.classList.toggle("on", n === e.currentTarget));
    const [tag, body] = NOTES[s.kind];
    note.replaceChildren(el("div", { class: "tag" }, tag), el("p", {}, body));
  } }, s.text));
  root.append(el("h4", {}, root.dataset.title || f.path), el("div", { class: "anatomy" }, el("div", {}, ...nodes), note));
}

// ---------------------------------------------------------------- context stepper
async function contextWidget(root) {
  const skill = (await getJSON("/api/file?path=kits/dice/.claude/skills/tie-breaker/SKILL.md")).text;
  const desc = (skill.match(/^---\n([\s\S]*?)\n---/) || [, ""])[1];
  const claudeMd = "# About me\nI'm an architecture student. Explain things with buildings, not code.\nNever make up a roll or a measurement: use the tools.";
  const C = {
    claude: { label: "CLAUDE.md", when: "start", text: claudeMd, note: "example: a student's own" },
    skills: { label: "Skill names and descriptions", when: "start", text: desc, note: "every skill, short" },
    ask: { label: "Your message", when: "added", text: "/tie-breaker pizza or noodles?" },
    body: { label: "The full tie-breaker skill", when: "demand", text: skill, note: "loaded only when used" },
    roll: { label: "The dice tool's answer", when: "added", text: "(rolling…)" },
    reply: { label: "Claude's reply", when: "added", text: "1. pizza  2. noodles\nRolled a 2: noodles." },
  };
  const STEPS = [
    ["1. You open a new session", ["claude", "skills"]],
    ["2. You type /tie-breaker", ["claude", "skills", "ask", "body"]],
    ["3. Claude runs the dice tool", ["claude", "skills", "ask", "body", "roll"]],
    ["4. Claude answers", ["claude", "skills", "ask", "body", "roll", "reply"]],
    ["5. You start a new session", ["claude", "skills"]],
  ];
  const WHEN = { start: "loaded at the start of every session", demand: "loaded when needed", added: "added as you work" };
  const win = el("div", { class: "window" });
  const caption = el("p", { class: "muted" });
  let shown = new Set();
  const go = async (i, buttons) => {
    buttons.forEach((b, j) => b.classList.toggle("on", i === j));
    const ids = STEPS[i][1];
    if (ids.includes("roll") && !shown.has("roll")) {
      const r = await getJSON("/api/dice?sides=2");
      C.roll.text = `$ ${r.command}\n${r.stdout.trim()}`;
      C.reply.text = `1. pizza  2. noodles\nRolled a ${r.rolls[0]}: ${r.rolls[0] === 1 ? "pizza" : "noodles"}.`;
    }
    win.replaceChildren(...ids.map(id => el("details", { class: `chip ${C[id].when}${shown.has(id) ? "" : " new"}` },
      el("summary", {}, C[id].label, el("small", {}, C[id].note || WHEN[C[id].when])), el("pre", {}, C[id].text))));
    caption.textContent = i === 4 ? "The conversation, the skill's full text and the tool's answer are gone. Only CLAUDE.md and the skill descriptions come back, every time." : "";
    shown = new Set(ids);
  };
  const buttons = STEPS.map((s, i) => el("button", { class: "ghost", onclick: () => go(i, buttons) }, s[0]));
  root.append(el("h4", {}, "What the agent knows, step by step"),
    el("div", { class: "ctx" }, el("div", { class: "steps" }, ...buttons, caption), win));
  go(0, buttons);
}

// ---------------------------------------------------------------- take-away
async function takeaway(root) {
  const k = await getJSON(`/api/kits/${root.dataset.kit}`);
  const pre = el("pre", {}, k.prompt);
  const copy = el("button", { onclick: async () => {
    await navigator.clipboard.writeText(k.prompt).catch(() => {});
    copy.textContent = "Copied"; setTimeout(() => (copy.textContent = "Copy"), 1500);
  } }, "Copy");
  root.classList.add("takeaway");
  root.append(el("h4", {}, `Take-away: the ${k.name} kit`),
    el("p", {}, "In the Code tab, with ", el("strong", {}, "your own folder"), " open, paste this:"),
    el("div", { class: "copy" }, pre, copy),
    el("details", {}, el("summary", {}, `What's in it (${k.files.length} files)`), el("ul", {}, ...k.files.map(f => el("li", {}, f)))),
    el("p", { class: "muted" }, "If that doesn't work: ", el("a", { href: k.zip }, "download the kit as a zip"), " and unzip it into your folder."));
}

// ---------------------------------------------------------------- gallery
function galleryWidget(root) {
  const frame = el("iframe", { src: "/runs/gallery.html", title: "Gallery of design runs" });
  root.classList.add("gallery");
  root.append(el("div", { class: "row" }, el("h4", {}, "Gallery of runs"),
    el("button", { class: "ghost", onclick: () => (frame.src = "/runs/gallery.html?" + Date.now()) }, "Refresh")), frame);
}

// ---------------------------------------------------------------- wiring
const WIDGETS = { dice, "llm-vs-tool": llmVsTool, tower: towerWidget, file: fileWidget, skill: skillWidget,
  context: contextWidget, takeaway, gallery: galleryWidget };
document.querySelectorAll("[data-widget]").forEach(root => {
  const make = WIDGETS[root.dataset.widget];
  root.classList.add("w");
  if (!make) { root.textContent = `Unknown widget: ${root.dataset.widget}`; return; }
  Promise.resolve(make(root)).catch(e => root.append(el("p", { class: "err" }, e.message)));
});

document.addEventListener("keydown", e => {
  if (e.target.closest("input, textarea, select") || e.ctrlKey || e.metaKey || e.altKey) return;
  const go = key => {
    const a = document.querySelector(`[data-key="${key}"]`);
    if (a) { e.preventDefault(); location.href = a.href; }
  };
  const slides = document.body.classList.contains("slides");
  if (slides && ["ArrowRight", "PageDown", " "].includes(e.key)) go("next");
  else if (slides && ["ArrowLeft", "PageUp"].includes(e.key)) go("prev");
  else if (e.key === "r" || e.key === "R") go("r");
  else if (e.key === "f" || e.key === "F") document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
});
