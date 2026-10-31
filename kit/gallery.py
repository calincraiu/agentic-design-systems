"""Build runs/gallery.html: one self-contained page for comparing design runs.

It is rebuilt after every run, so refreshing the browser shows the latest designs.
Runs are grouped by brief and labelled by the skill that produced them, so the
same brief handled by two different skills can be compared side by side.
"""
import json
import webbrowser
from datetime import datetime

from .paths import runs_dir
from .runs import list_runs


def build(open_browser=False):
    folder = runs_dir()
    folder.mkdir(parents=True, exist_ok=True)
    data = json.dumps(list_runs(), ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__RUNS__", data).replace("__BUILT__", datetime.now().strftime("%d %b %Y, %H:%M"))
    path = folder / "gallery.html"
    path.write_text(html, encoding="utf-8")
    if open_browser:
        webbrowser.open(path.resolve().as_uri())
    return path


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Design Runs</title>
<style>
:root {
  --bg: #f6f4f0; --surface: #ffffff; --ink: #24211e; --muted: #6f6a63; --line: #e2ddd5;
  --accent: #b5522b; --pass: #2f7d4f; --fail: #b3261e; --chip: #efebe4; --best: #e7f2ea;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #171614; --surface: #211f1c; --ink: #ece8e1; --muted: #a39d94; --line: #36322d;
    --accent: #e0835a; --pass: #6cc28f; --fail: #f08a80; --chip: #2c2925; --best: #1f3326;
  }
}
:root[data-theme="dark"] {
  --bg: #171614; --surface: #211f1c; --ink: #ece8e1; --muted: #a39d94; --line: #36322d;
  --accent: #e0835a; --pass: #6cc28f; --fail: #f08a80; --chip: #2c2925; --best: #1f3326;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 14px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif; }
header { padding: 24px 16px 8px; max-width: 1400px; margin: 0 auto; }
h1 { margin: 0; font-size: 22px; letter-spacing: -0.01em; }
.sub { color: var(--muted); margin: 4px 0 16px; }
.controls { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
select { font: inherit; color: var(--ink); background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 4px 8px; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { display: inline-block; padding: 2px 8px; border-radius: 999px; background: var(--chip); color: var(--muted); font-size: 12px; border: 1px solid transparent; }
button.chip { cursor: pointer; font: inherit; font-size: 12px; }
button.chip.on { border-color: var(--accent); color: var(--ink); }
.chip.skill { color: var(--accent); }
main { padding: 0 16px 48px; max-width: 1400px; margin: 0 auto; }
section { margin-top: 28px; }
h2 { font-size: 16px; margin: 0 0 12px; border-bottom: 1px solid var(--line); padding-bottom: 6px; }
h2 small { color: var(--muted); font-weight: normal; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 14px; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; display: flex; flex-direction: column; }
.card img { width: 100%; aspect-ratio: 1; object-fit: contain; background: #fff; display: block; }
.card .body { padding: 10px 12px 12px; display: flex; flex-direction: column; gap: 6px; }
.card h3 { margin: 0; font-size: 15px; }
.why { margin: 0; color: var(--muted); font-style: italic; }
.checks { list-style: none; margin: 0; padding: 0; font-size: 12px; }
.checks .pass { color: var(--pass); } .checks .fail { color: var(--fail); }
dl { display: grid; grid-template-columns: 1fr auto; gap: 1px 10px; margin: 0; font-size: 12px; }
dt { color: var(--muted); } dd { margin: 0; text-align: right; font-variant-numeric: tabular-nums; }
details summary { cursor: pointer; color: var(--muted); font-size: 12px; }
.table-wrap { overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; }
table { border-collapse: collapse; width: 100%; font-size: 12px; font-variant-numeric: tabular-nums; }
th, td { padding: 6px 10px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; }
th:first-child, td:first-child, th:nth-child(2), td:nth-child(2) { text-align: left; }
th { color: var(--muted); font-weight: 600; }
td.best { background: var(--best); font-weight: 600; }
td.fail { color: var(--fail); }
.empty { color: var(--muted); padding: 40px 0; }
</style>
</head>
<body>
<header>
  <h1>Design runs</h1>
  <p class="sub" id="sub"></p>
  <div class="controls">
    <label>Sort <select id="sort"></select></label>
    <label>View <select id="view"><option value="cards">Cards</option><option value="table">Table</option></select></label>
    <div class="chips" id="skills"></div>
  </div>
</header>
<main id="groups"></main>
<script id="data" type="application/json">__RUNS__</script>
<script>
const runs = JSON.parse(document.getElementById('data').textContent);
const state = { sort: 'newest', view: 'cards', skills: new Set() };
try { Object.assign(state, JSON.parse(localStorage.getItem('gallery') || '{}'), { skills: new Set() }); } catch (e) {}
if (location.hash === '#table' || location.hash === '#cards') state.view = location.hash.slice(1);

function h(tag, attrs, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === 'class') el.className = v; else if (k.startsWith('on')) el.addEventListener(k.slice(2), v); else el.setAttribute(k, v);
  }
  for (const c of children.flat(Infinity)) if (c !== null && c !== undefined) el.append(c instanceof Node ? c : String(c));
  return el;
}
const skillOf = r => r.meta.skill || 'manual';
const metricsOf = r => (r.metrics && r.metrics.metrics) || {};
const info = {};
for (const r of runs) {
  const m = r.metrics || {};
  for (const k of Object.keys(m.metrics || {})) {
    if (!info[k]) info[k] = { label: (m.labels || {})[k] || k, unit: (m.units || {})[k] || '' };
  }
}
// "Better" comes from each brief's priorities, so it is decided per group of runs.
const betterIn = (list, k) => ((list[0].metrics || {}).better || {})[k] || null;
const prioritiesIn = list => (list[0].metrics || {}).priorities || [];
function fmt(v) {
  if (v === null || v === undefined) return '–';
  if (typeof v !== 'number') return String(v);
  if (Math.abs(v) >= 100) return Math.round(v).toLocaleString();
  return String(+v.toFixed(2));
}
const withUnit = (k, v) => fmt(v) + (info[k] && info[k].unit && v !== null && v !== undefined ? ' ' + info[k].unit : '');

document.getElementById('sub').textContent =
  runs.length + ' run' + (runs.length === 1 ? '' : 's') + ' · rebuilt __BUILT__ · refresh this page after new runs';

const sortSel = document.getElementById('sort');
sortSel.append(h('option', { value: 'newest' }, 'Newest first'));
for (const [k, i] of Object.entries(info)) sortSel.append(h('option', { value: k }, i.label));
sortSel.value = info[state.sort] || state.sort === 'newest' ? state.sort : 'newest';
sortSel.onchange = () => { state.sort = sortSel.value; save(); render(); };
const viewSel = document.getElementById('view');
viewSel.value = state.view;
viewSel.onchange = () => { state.view = viewSel.value; save(); render(); };

const skills = [...new Set(runs.map(skillOf))];
const skillBox = document.getElementById('skills');
if (skills.length > 1) {
  for (const s of skills) {
    const b = h('button', { class: 'chip', onclick: () => { state.skills.has(s) ? state.skills.delete(s) : state.skills.add(s); b.classList.toggle('on'); render(); } }, s);
    skillBox.append(b);
  }
}
function save() { try { localStorage.setItem('gallery', JSON.stringify({ sort: state.sort, view: state.view })); } catch (e) {} }

function sorted(list) {
  const out = [...list];
  if (state.sort === 'newest') return out.reverse();
  const k = state.sort, dir = betterIn(list, k) === 'lower' ? 1 : -1;
  return out.sort((a, b) => {
    const x = metricsOf(a)[k], y = metricsOf(b)[k];
    if (x === null || x === undefined) return 1;
    if (y === null || y === undefined) return -1;
    return dir * (x - y);
  });
}

function checks(r) {
  const cs = (r.metrics && r.metrics.constraints) || [];
  if (!cs.length) return null;
  return h('ul', { class: 'checks' }, cs.map(c => h('li', { class: c.pass ? 'pass' : 'fail' },
    (c.pass ? '✓ ' : '✗ ') + ((info[c.metric] || {}).label || c.metric) + ' ' + c.op + ' ' + fmt(c.value) + '  (' + withUnit(c.metric, c.actual) + ')')));
}

function card(r) {
  const m = metricsOf(r);
  return h('article', { class: 'card' },
    r.image ? h('a', { href: r.image, target: '_blank' }, h('img', { src: r.image, alt: r.meta.label || r.id, loading: 'lazy' })) : null,
    h('div', { class: 'body' },
      h('h3', {}, r.meta.label || r.id),
      h('div', { class: 'chips' }, h('span', { class: 'chip skill' }, skillOf(r)), h('span', { class: 'chip' }, r.meta.backend || ''), h('span', { class: 'chip' }, r.id.slice(9, 15).replace(/(..)(..)(..)/, '$1:$2:$3'))),
      r.meta.why ? h('p', { class: 'why' }, r.meta.why) : null,
      checks(r),
      h('dl', {}, Object.keys(m).map(k => [h('dt', {}, info[k].label), h('dd', {}, withUnit(k, m[k]))])),
      h('details', {}, h('summary', {}, 'Parameters'),
        h('dl', {}, Object.entries(r.params || {}).map(([k, v]) => [h('dt', {}, k), h('dd', {}, fmt(v))])))));
}

function table(list) {
  const keys = Object.keys(info);
  const best = {}, prios = prioritiesIn(list);
  for (const k of keys) {
    const vals = list.map(r => metricsOf(r)[k]).filter(v => typeof v === 'number'), b = betterIn(list, k);
    if (!vals.length || !b || new Set(vals).size < 2) continue;
    best[k] = b === 'lower' ? Math.min(...vals) : Math.max(...vals);
  }
  const failed = r => new Set(((r.metrics && r.metrics.constraints) || []).filter(c => c.pass === false).map(c => c.metric));
  return h('div', { class: 'table-wrap' }, h('table', {},
    h('thead', {}, h('tr', {}, h('th', {}, 'Run'), h('th', {}, 'Skill'), keys.map(k => h('th', { title: prios.includes(k) ? 'A priority in this brief' : info[k].unit }, (prios.includes(k) ? '★ ' : '') + info[k].label)))),
    h('tbody', {}, list.map(r => {
      const m = metricsOf(r), bad = failed(r);
      return h('tr', {}, h('td', {}, r.meta.label || r.id), h('td', {}, skillOf(r)),
        keys.map(k => h('td', { class: bad.has(k) ? 'fail' : (best[k] !== undefined && m[k] === best[k] ? 'best' : null) }, fmt(m[k]))));
    }))));
}

function render() {
  const root = document.getElementById('groups');
  root.replaceChildren();
  const groups = new Map();
  for (const r of runs) {
    if (state.skills.size && !state.skills.has(skillOf(r))) continue;
    const key = r.meta.brief_title || 'No brief';
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(r);
  }
  if (!groups.size) { root.append(h('p', { class: 'empty' }, 'No runs yet. Generate a design and refresh this page.')); return; }
  for (const [title, list] of [...groups.entries()].reverse()) {
    const ordered = sorted(list);
    root.append(h('section', {},
      h('h2', {}, title, ' ', h('small', {}, '· ' + list.length + ' run' + (list.length === 1 ? '' : 's'))),
      state.view === 'table' ? table(ordered) : h('div', { class: 'grid' }, ordered.map(card))));
  }
}
render();
</script>
</body>
</html>
"""
