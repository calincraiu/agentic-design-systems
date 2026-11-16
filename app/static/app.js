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

// ---------------------------------------------------------------- add (calculator, or a room poll with data-poll)
// Plain: type numbers, the add tool totals them. With data-poll: the room pastes the answers Chat gave
// for the sum in data-numbers, then the tool adds it once and every answer is checked against it.
const sameNumber = (a, b) => {
  const norm = t => {
    let x = String(t).replace(/[\s,'’_]/g, "").replace(/^\+/, "");
    if (x.includes(".")) x = x.replace(/0+$/, "").replace(/\.$/, "");
    return x;
  };
  return norm(a) !== "" && norm(a) === norm(b);
};
function addWidget(root) {
  const poll = "poll" in root.dataset;
  const numbers = el("input", { type: "text", value: root.dataset.numbers || "2 2", size: 34 });
  const answers = el("textarea", { rows: 3, placeholder: "Paste or type the answers Chat gave, one per line" });
  const out = el("div"), extra = el("div");
  const button = el("button", { onclick: add }, "Add with the tool");
  async function add() {
    button.disabled = true;
    try {
      const r = await getJSON(`/api/add?numbers=${encodeURIComponent(numbers.value)}`);
      extra.replaceChildren(behind(r));
      if (r.code !== 0) { out.replaceChildren(el("p", { class: "err" }, r.stderr)); return; }
      const kids = [el("p", { class: "sum" }, el("span", { class: "muted" }, "Total "), el("strong", {}, r.total))];
      if (poll) {
        const given = answers.value.split("\n").map(t => t.trim()).filter(Boolean);
        const right = given.filter(g => sameNumber(g, r.total)).length;
        kids.push(el("ul", { class: "answers" }, ...given.map(g => {
          const ok = sameNumber(g, r.total);
          return el("li", { class: ok ? "pass" : "fail" }, `${ok ? "✓" : "✗"}  ${g}`);
        })));
        kids.push(el("p", { class: "muted" }, given.length
          ? `${right} of ${given.length} answers match the tool. Right or wrong, none of them showed how it got there. The tool shows its command.`
          : "Type the room's answers above to check them against the tool."));
      }
      out.replaceChildren(...kids);
    } catch (e) { out.replaceChildren(el("p", { class: "err" }, e.message)); }
    finally { button.disabled = false; }
  }
  if (poll) {
    numbers.readOnly = true;
    root.append(el("h4", {}, "In your head, or with a tool?"),
      el("p", {}, "The sum: ", el("code", {}, numbers.value.trim().split(/\s+/).join(" + "))),
      answers, el("div", { class: "row" }, button), out, extra);
  } else {
    root.append(el("h4", {}, "Add tool"),
      el("div", { class: "row" }, el("label", {}, "numbers", numbers), button), out, extra);
  }
}

// ---------------------------------------------------------------- llm vs tool: is it fair?
// The room asks Chat to pick one option "fairly", and the instructor clicks each answer called out.
// Then the dice tool rolls the same number of times, so both tallies are the same size.
function llmVsTool(root) {
  let options = (root.dataset.options || "A,B,C,D,E,F").split(",").map(t => t.trim()).filter(Boolean);
  let room = [], tool = null, rolls = 0;
  const roomChart = el("div"), toolChart = el("div");
  const roomNote = el("p", { class: "muted" }), toolNote = el("p", { class: "muted" }), extra = el("div");
  const point = el("p", { class: "point", hidden: "" },
    "A small sample wobbles at random: roll again and the tallest bar moves. A lean that comes back every time is a bias. " +
    "Where fairness matters (crit order, a lottery, a random sample of sites), use a tool.");
  const counts = picks => options.map((_, i) => picks.filter(p => p === i).length);
  const chart = (target, picks, who, clickable) => {
    const c = counts(picks), n = picks.length, fair = n / options.length, max = Math.max(1, fair, ...c);
    const cols = `grid-template-columns:repeat(${options.length},1fr)`;
    const scale = f => `calc((100% - 1.5em) * ${f})`;  // leave room above the tallest bar for its count
    target.replaceChildren(el("div", { class: `tally${clickable ? "" : " tool"}` },
      el("div", { class: "bars", style: cols },
        ...c.map(v => el("div", { class: "col" }, el("span", {}, String(v)), el("div", { class: "fill", style: `height:${scale(v / max)}` }))),
        n ? el("div", { class: "fair", style: `bottom:${scale(fair / max)}` }, el("span", {}, `fair ${Math.round(fair * 10) / 10}`)) : null),
      el("div", { class: "names", style: cols },
        ...options.map((name, i) => clickable
          ? el("button", { class: "ghost", title: `One more answer: ${name}`, onclick: () => { room.push(i); redraw(); } }, `+ ${name}`)
          : el("span", {}, name)))));
    if (!n) return "";
    const top = c.indexOf(Math.max(...c));
    return `${who}: ${n} picks. Fair would be about ${Math.round(fair * 10) / 10} each. Most picked: ${options[top]}, ${c[top]} times (${Math.round(100 * c[top] / n)}%).`;
  };
  const rollBtn = el("button", { onclick: async () => {
    rollBtn.disabled = true;
    try {
      const r = await getJSON(`/api/dice?sides=${options.length}&count=${room.length}`);
      tool = r.rolls.map(n => n - 1); rolls++;
      extra.replaceChildren(behind(r));
      point.hidden = rolls < 2;
    } catch (e) { extra.replaceChildren(el("p", { class: "err" }, e.message)); }
    redraw();
  } });
  const redraw = () => {
    roomNote.textContent = chart(roomChart, room, "The room (each pick a separate conversation with an LLM)", true)
      || "Click a name for each answer the room calls out.";
    if (tool && tool.length !== room.length) { tool = null; rolls = 0; point.hidden = true; }
    toolNote.textContent = tool ? chart(toolChart, tool, `The dice tool, roll ${rolls}`, false) : "";
    if (!tool) toolChart.replaceChildren(el("p", { class: "muted empty" }, "The dice tool's tally appears here, with as many rolls as the room gave answers."));
    rollBtn.disabled = !room.length;
    rollBtn.textContent = tool ? "Roll again" : "Roll the dice the same number of times";
  };
  const reset = () => { room = []; tool = null; rolls = 0; point.hidden = true; extra.replaceChildren(); redraw(); };
  const undo = el("button", { class: "ghost", onclick: () => { room.pop(); redraw(); } }, "Undo");
  const clear = el("button", { class: "ghost", onclick: reset }, "Clear");
  const edit = el("input", { type: "text", value: options.join(", "), size: 40 });
  edit.addEventListener("change", () => {
    const next = edit.value.split(",").map(t => t.trim()).filter(Boolean);
    if (next.length >= 2) { options = next; reset(); }
  });
  root.append(el("h4", {}, "Is an LLM fair? The room against the dice"),
    el("div", { class: "vs" }, el("div", {}, roomChart, roomNote), el("div", {}, toolChart, toolNote)),
    el("div", { class: "row" }, rollBtn, undo, clear), point, extra,
    el("details", {}, el("summary", { class: "muted" }, "Change the options"), el("div", { class: "row" }, edit)));
  redraw();
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
  const buildBtn = el("button", { onclick: () => build(false) }, "Build with the tool");
  const againBtn = el("button", { class: "ghost", onclick: () => build(true) }, "Build the same again");

  // Live preview: the floor outlines from the tool's own build(), without the drawing or the metrics.
  const previewBox = el("div");
  const preview = el("figure", { class: "preview" }, previewBox,
    el("figcaption", {}, "Preview · plan of every floor, ground in ink, top in terracotta. Build runs the full tool."));
  let timer;
  const updatePreview = () => {
    clearTimeout(timer);
    timer = setTimeout(async () => {
      try {
        const r = await getJSON("/api/tower/preview?" + new URLSearchParams(values));
        previewBox.innerHTML = planSvg(r.curves, parsePlot(plot.value));
      } catch (e) { previewBox.replaceChildren(el("p", { class: "err" }, e.message)); }
    }, 60);
  };
  rows.forEach(r => r.querySelector("input").addEventListener("input", updatePreview));
  plot.addEventListener("input", updatePreview);
  updatePreview();

  root.append(el("h4", {}, "Tower tool"), el("div", { class: "tower" },
    el("div", {}, ...rows,
      el("div", { class: "row" }, el("label", {}, "plot", plot), label),
      require, el("div", { class: "row" }, buildBtn, againBtn)),
    el("div", {}, preview, result)));
}
const parsePlot = text => {
  const m = text.trim().match(/^([\d.]+)\s*[xX]\s*([\d.]+)$/);
  return m && +m[1] > 0 && +m[2] > 0 ? [+m[1], +m[2]] : null;
};
function planSvg(curves, plot) {
  const xs = curves.flat().map(p => p[0]), ys = curves.flat().map(p => p[1]);
  if (plot) xs.push(-plot[0] / 2, plot[0] / 2), ys.push(-plot[1] / 2, plot[1] / 2);
  const pad = 3, x0 = Math.min(...xs) - pad, x1 = Math.max(...xs) + pad, y0 = Math.min(...ys) - pad, y1 = Math.max(...ys) + pad;
  const n = curves.length, d = f => f.map((p, j) => `${j ? "L" : "M"}${p[0].toFixed(2)} ${(-p[1]).toFixed(2)}`).join("") + "Z";
  const floors = curves.map((f, i) => `<path d="${d(f)}" style="stroke:color-mix(in srgb, var(--accent) ${n > 1 ? (100 * i) / (n - 1) : 0}%, var(--ink))"/>`).join("");
  const site = plot ? `<rect x="${-plot[0] / 2}" y="${-plot[1] / 2}" width="${plot[0]}" height="${plot[1]}" style="stroke:var(--muted);stroke-dasharray:6 4"/>` : "";
  return `<svg viewBox="${x0} ${-y1} ${x1 - x0} ${y1 - y0}" style="max-height:230px" fill="none" stroke-width="1.2">` +
    `<g style="vector-effect:non-scaling-stroke">${site}${floors}</g>` +
    `<style>path,rect{vector-effect:non-scaling-stroke}</style></svg>`;
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
    win.replaceChildren(...ids.map(id => el("details", { class: `chipbox ${C[id].when}${shown.has(id) ? "" : " new"}` },
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
// data-kit="dice", or several kits in one prompt: data-kit="add,dice"
// data-mode="manual": no prompt. A zip to download and unzip, and the kit folders to copy from, for copying by hand.
async function takeaway(root) {
  const k = await getJSON(`/api/kits/${root.dataset.kit}`);
  if (root.dataset.mode === "manual") {
    const s = k.folder.length > 1 ? "s" : "";
    root.classList.add("takeaway");
    root.append(el("h4", {}, `Take-away: the ${k.name} kit${s}`),
      el("p", {}, el("a", { href: k.zip }, `Download the kit${s} as a zip`), ", unzip it, and copy what's inside into ", el("strong", {}, "your own folder"), "."),
      el("details", {}, el("summary", {}, `What's in it (${k.files.length} files)`), el("ul", {}, ...k.files.map(f => el("li", {}, f)))),
      el("p", { class: "muted" }, "Or copy straight from the course folder. The contents of:"),
      el("ul", { class: "muted" }, ...k.folder.map(f => el("li", {}, f))));
    return;
  }
  const pre = el("pre", {}, k.prompt);
  const copy = el("button", { onclick: async () => {
    await navigator.clipboard.writeText(k.prompt).catch(() => {});
    copy.textContent = "Copied"; setTimeout(() => (copy.textContent = "Copy"), 1500);
  } }, "Copy");
  const s = k.folder.length > 1 ? "s" : "";
  root.classList.add("takeaway");
  root.append(el("h4", {}, `Take-away: the ${k.name} kit${s}`),
    el("p", {}, "In the Code tab, with ", el("strong", {}, "your own folder"), " open, paste this:"),
    el("div", { class: "copy" }, pre, copy),
    el("p", { class: "muted" }, "Copy it from the course app on ", el("strong", {}, "your own computer"),
      ", not from the projector: the path in it is different on every computer."),
    el("details", {}, el("summary", {}, `What's in it (${k.files.length} files)`), el("ul", {}, ...k.files.map(f => el("li", {}, f)))),
    el("p", { class: "muted" }, "If that doesn't work: ", el("a", { href: k.zip }, `download the kit${s} as a zip`), " and unzip it into your folder."));
}

// ---------------------------------------------------------------- gallery
function galleryWidget(root) {
  const frame = el("iframe", { src: "/runs/gallery.html", title: "Gallery of design runs" });
  root.classList.add("gallery");
  root.append(el("div", { class: "row" }, el("h4", {}, "Gallery of runs"),
    el("button", { class: "ghost", onclick: () => (frame.src = "/runs/gallery.html?" + Date.now()) }, "Refresh")), frame);
}

// ---------------------------------------------------------------- figures and click-to-reveal steps
// A figure is an SVG in slides/figures/. Anything in it marked data-step="n" appears on the n-th key press.
// data-start="3" on the widget means steps 1 to 3 are already showing when the slide opens, so one figure
// can grow across several slides.
const steps = { levels: [], at: 0, start: 0 };
const showSteps = upTo => {
  steps.at = upTo;
  document.querySelectorAll("[data-step]").forEach(e => e.classList.toggle("shown", +e.dataset.step <= upTo));
};
const revealNext = () => {
  const next = steps.levels.find(n => n > steps.at);
  if (next == null) return false;
  showSteps(next);
  return true;
};
const hideLast = () => {
  const before = [...steps.levels].reverse().find(n => n < steps.at && n >= steps.start);
  if (steps.at <= steps.start) return false;
  showSteps(before ?? steps.start);
  return true;
};
async function figure(root) {
  root.classList.add("fig");
  const r = await fetch(`/api/figure/${root.dataset.name}`);
  if (!r.ok) throw new Error(`No figure called ${root.dataset.name}`);
  root.innerHTML = await r.text();
  // data-focus="n": a "you are here" map. Parts before n stay lit, part n is highlighted by one key press (the next press
  // moves on), and parts after n stay faint.
  if (root.dataset.focus) root.querySelectorAll("[data-step]").forEach(e => {
    const n = +e.dataset.step, focus = +root.dataset.focus;
    if (n === focus) return;
    e.removeAttribute("data-step");
    e.setAttribute(n < focus ? "data-lit" : "data-faint", "");
  });

}
// Called once every widget and figure is in the page: find the steps and show the starting ones.
function initSteps() {
  if (!document.body.classList.contains("slides")) { showSteps(Infinity); return; }  // reading mode shows everything
  steps.levels = [...new Set([...document.querySelectorAll("[data-step]")].map(e => +e.dataset.step))].sort((a, b) => a - b);
  steps.start = Math.max(0, ...[...document.querySelectorAll("[data-start]")].map(e => +e.dataset.start));
  showSteps(steps.start);
}

// ---------------------------------------------------------------- contact sheet (hook slide)
function contact(root) {
  root.append(el("div", { class: "contact" }, ...root.dataset.images.split(",").map(name =>
    el("figure", {}, el("img", { src: `/static/img/${name.trim()}.png`, alt: name.trim() }),
      el("figcaption", {}, name.trim().replace(/-/g, " "))))));
}

// ---------------------------------------------------------------- wiring
const WIDGETS = { add: addWidget, dice, "llm-vs-tool": llmVsTool, tower: towerWidget, file: fileWidget, skill: skillWidget,
  context: contextWidget, takeaway, gallery: galleryWidget, figure, contact };
const UNBOXED = new Set(["figure", "contact"]);
const loading = [...document.querySelectorAll("[data-widget]")].map(root => {
  const make = WIDGETS[root.dataset.widget];
  if (!UNBOXED.has(root.dataset.widget)) root.classList.add("w");
  if (!make) { root.textContent = `Unknown widget: ${root.dataset.widget}`; return null; }
  return Promise.resolve(make(root)).catch(e => root.append(el("p", { class: "err" }, e.message)));
});
Promise.all(loading).then(initSteps);

// ---------------------------------------------------------------- notes (N), overview (G), theme (D), keys (?)
const toggleNotes = () => { const n = document.getElementById("notes"); if (n) n.hidden = !n.hidden; };
async function toggleOverview() {
  const open = document.querySelector(".overview");
  if (open) { open.remove(); return; }
  const deck = document.getElementById("deck");
  if (!deck) return;
  const outline = await getJSON(`/api/deck/${deck.dataset.deck}`);
  const WHERE = { chat: "Chat tab", "code-yours": "Your folder", "code-course": "Course folder", app: "This app" };
  document.body.append(el("div", { class: "overview" }, el("h2", {}, "All slides · press G or Esc to close"),
    el("div", { class: "grid" }, ...outline.map(s =>
      el("a", { href: `/d/${deck.dataset.deck}/${s.n}`, class: s.n === +deck.dataset.n ? "here" : "" },
        el("span", { class: "n" }, String(s.n).padStart(2, "0")), el("span", { class: "t" }, s.title),
        s.where ? el("span", { class: `chip where-${s.where}` }, WHERE[s.where]) : null)))));
}
const toggleTheme = () => {
  const root = document.documentElement;
  const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark";
  try { localStorage.setItem("ads-theme", root.dataset.theme); } catch (e) { /* private window: just don't remember */ }
};

const follow = key => { const a = document.querySelector(`[data-key="${key}"]`); if (a) location.href = a.href; return !!a; };
const fullScreen = () => document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen();
const inSlides = () => document.body.classList.contains("slides");
const closeAll = () => {
  document.querySelector(".overview")?.remove();
  document.querySelector(".keys-panel")?.remove();
  const n = document.getElementById("notes"); if (n) n.hidden = true;
};
// One list of keys, used by the keyboard and by the "? Keys" button: [keys, what it does, action, when it applies]
const KEYS = [
  ["→ Space", "Next: the next part of a diagram, then the next slide", () => { if (!revealNext()) follow("next"); }, inSlides],
  ["←", "Back", () => { if (!hideLast()) follow("prev"); }, inSlides],
  ["N", "More on this slide: notes to read now, or after class", () => toggleNotes(), () => !!document.getElementById("notes")],
  ["G", "All slides", () => toggleOverview(), () => !!document.getElementById("deck")],
  ["R", "Reading mode: the whole session as one page, notes included. Press again to go back", () => follow("r"), () => !!document.querySelector('[data-key="r"]')],
  ["D", "Dark or light", () => toggleTheme(), () => true],
  ["F", "Full screen", fullScreen, () => true],
  ["Esc", "Close whatever is open", closeAll, () => true],
  ["?", "This list", () => toggleKeys(), () => true],
];
function toggleKeys() {
  const open = document.querySelector(".keys-panel");
  if (open) { open.remove(); return; }
  const rows = KEYS.filter(k => k[3]()).map(([keys, what, act]) => el("button", { type: "button", class: "key-row", onclick: () => {
    document.querySelector(".keys-panel")?.remove();
    act();
  } }, el("span", { class: "k" }, ...keys.split(" ").map(t => el("kbd", {}, t))), el("span", {}, what)));
  document.body.append(el("div", { class: "keys-panel", role: "dialog", "aria-label": "Keyboard shortcuts" },
    el("h4", {}, "Keys · press one, or click a line"), ...rows));
}
document.addEventListener("click", e => {
  if (e.target.closest("[data-keys]")) { toggleKeys(); return; }
  const panel = document.querySelector(".keys-panel");
  if (panel && !e.target.closest(".keys-panel")) panel.remove();
});

document.addEventListener("keydown", e => {
  if (e.target.closest("input, textarea, select") || e.ctrlKey || e.metaKey || e.altKey) return;
  if (e.key === "Escape") { closeAll(); return; }
  if (e.key === "?") { e.preventDefault(); toggleKeys(); return; }
  if (document.querySelector(".overview") && !["g", "G"].includes(e.key)) return;
  const k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
  const i = ["ArrowRight", "PageDown", " "].includes(k) ? 0 : ["ArrowLeft", "PageUp"].includes(k) ? 1
    : { n: 2, g: 3, r: 4, d: 5, f: 6 }[k];
  if (i == null || !KEYS[i][3]()) return;
  e.preventDefault();
  KEYS[i][2]();
});
