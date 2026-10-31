# The Grasshopper bridge

Python tools and Grasshopper talk through two small files in `<repo>/.exchange/`:

```
Python tool  ── writes ──►  job.json     ──► Listener (polls every 500 ms)
Python tool  ◄── reads ───  result.json  ◄── Writer (or the Listener, for pings and errors)
                            runs/<run>/geometry.json  ◄── Writer
```

These components are generic. Any design system (the tower now, the students' own systems in Session 3) uses the same Listener and Writer. Only the middle of the definition changes.

## Protocol

**job.json** (written by `kit/bridge.py`)

```json
{"job_id": "231502-a1b2c3", "kind": "generate", "system": "tower",
 "params": {"floors": 20, "twist": 90},
 "run_dir": "D:/.../runs/20261027-231502-a-slim-beacon",
 "exchange_dir": "D:/.../.exchange", "created": 1793142902.5}
```

`kind` is `"ping"` or `"generate"`. Jobs older than 120 s are ignored.

**result.json** (written by Grasshopper)

```json
{"job_id": "231502-a1b2c3", "status": "ok", "message": "20 curves sent."}
```

`status` is `"ok"`, `"error"` (with a message for the student) or `"pong"`. A pong also includes `system`, `active` and `rhino`.

**geometry.json** (written into the run folder by the Writer)

```json
{"system": "tower", "source": "grasshopper", "rhino": "7.x",
 "curves": [[[x, y, z], ...], ...], "floor_height": 3.5}
```

Each curve becomes its list of corner points (or 64 sample points if it isn't a polyline). Extra values arrive through the Writer's `keys`/`values` inputs.

## Assembling the components

Use **GhPython Script** (Rhino 7: Maths › Script) or **Python 3 Script** (Rhino 8). Paste the file's code, then zoom in on the component to set its inputs and outputs:

| Component | Inputs | Outputs |
|---|---|---|
| [listener.py](listener.py) | `active` bool, `system` str, `interval` int, all Item access | `job`, `status` |
| [writer.py](writer.py) | `job` str (Item), `curves` Curve (**List**), `keys` str (List), `values` float (List) | `status` |

Set the type hints by right-clicking each input. `curves` must be hinted as **Curve**, or the Writer receives object IDs instead of geometry.

## Design decisions

- **Files, not a server.** Nothing to install in Rhino, nothing that works only on Windows, and every message can be opened and read. Students can watch `job.json` change.
- **Grasshopper returns data, not pictures.** Metrics and images are made in Python from `geometry.json`, so runs look identical whichever backend made them, and viewport capture (fragile across platforms) is avoided.
- **Polling happens on a background timer.** It only re-runs the Listener (and so the whole definition) when a new job arrives, so editing the definition with Agent control OFF is undisturbed.
- **Written for IronPython 2.7 and Python 3.** That means no f-strings, and file access goes through .NET `System.IO`. `tests/test_gh_scripts.py` guards this.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `kit ping` gets no answer | Rhino or the definition isn't open; or the .gh file was opened from outside the repo folder; or it was never saved (the Listener needs a saved file path) |
| Listener status says *Save this definition inside the course repo* | Save the .gh somewhere under the repo folder |
| *Agent control is OFF* | Set the toggle to True |
| *The open Grasshopper definition is 'x'* | The wrong .gh is open, or the `system` Panel text is wrong |
| Generate times out, but ping works | The definition has an error between the Listener and the Writer: look for red or orange components |
| Warning that floor area differs by more than 1% | The tower definition doesn't match `examples/tower/GH_SPEC.md` |
