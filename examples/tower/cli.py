"""`uv run tower ...`: the Tower Toy's tools, as the agent (or you) calls them.

  tower params                 the parameters and metrics: the tools' contract
  tower check-brief BRIEF      is this structured brief valid for the tower?
  tower generate [options]     build one variant, measure it, save it as a run

Run any command with --help to see exactly what it accepts.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from kit import brief as briefs
from kit import bridge, gallery, runs
from kit.paths import rel
from kit.render import render_floors

from . import SYSTEM
from .evaluate import METRICS, evaluate
from .generate import build
from .params import PARAMS, BY_NAME, resolve


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    return 2


def show_params():
    print("PARAMETERS (what the generator accepts)")
    for p in PARAMS:
        print(f"  --{p.name.replace('_', '-'):<14} {p.low:g} to {p.high:g} {p.unit:<4} default {p.default:g}. {p.meaning}")
    print("\nMETRICS (what the evaluator measures; usable in brief constraints and priorities)")
    for name, m in METRICS.items():
        print(f"  {name:<17} {m.unit:<4} {m.meaning}")
    return 0


def tower_problems(brief):
    """Schema problems plus tower-specific ones: unknown parameters or metrics."""
    found = briefs.problems(brief)
    if found:
        return found
    for q in brief["qualities"]:
        for name in q["parameters"]:
            if name not in BY_NAME:
                found.append(f"quality '{q['phrase']}' mentions unknown parameter '{name}'")
    for kind in ("constraints", "priorities"):
        for item in brief[kind]:
            if item["metric"] not in METRICS:
                found.append(f"{kind}: unknown metric '{item['metric']}' (see `uv run tower params`)")
    return found


def check_brief(path):
    try:
        brief = briefs.load(path)
    except (OSError, json.JSONDecodeError) as e:
        return fail(f"Could not read {path}: {e}")
    found = tower_problems(brief)
    if found:
        print(f"Brief has {len(found)} problem(s):")
        for f in found:
            print(f"  - {f}")
        return 1
    unanswered = [q["question"] for q in brief["open_questions"] if not q.get("answer")]
    print(f"Brief OK: '{brief['title']}' with {len(brief['qualities'])} qualities, "
          f"{len(brief['constraints'])} constraints, {len(brief['priorities'])} priorities.")
    if unanswered:
        print(f"{len(unanswered)} open question(s) still unanswered:")
        for q in unanswered:
            print(f"  ? {q}")
    return 0


def generate(args):
    given = {p.name: getattr(args, p.name) for p in PARAMS if getattr(args, p.name) is not None}
    try:
        params = resolve(given)
    except ValueError as e:
        return fail(f"Invalid parameters: {e}")

    brief = None
    if args.brief:
        try:
            brief = briefs.load(args.brief)
        except (OSError, json.JSONDecodeError) as e:
            return fail(f"Could not read the brief {args.brief}: {e}")
        found = tower_problems(brief)
        if found:
            return fail("The brief is not valid, fix it first (`uv run tower check-brief`): " + "; ".join(found))

    label = args.label or f"{params['floors']} floors, twist {params['twist']:g}"
    run = runs.new_run(label)
    warnings = []
    try:
        if args.backend == "python":
            geometry = build(params)
        else:
            bridge.generate(SYSTEM, params, run, timeout=args.timeout)
            geometry = runs.read_json(run / "geometry.json")
            if "floor_height" not in geometry:
                raise ValueError("Grasshopper sent no floor_height: check the Writer's keys/values inputs.")
            reference = evaluate(build(params))["metrics"]["gfa_m2"]
        result = evaluate(geometry, brief)
    except (bridge.BridgeError, ValueError, KeyError, OSError) as e:
        runs.discard(run)
        return fail(str(e))

    if args.backend == "grasshopper" and abs(result["metrics"]["gfa_m2"] - reference) > 0.01 * reference:
        warnings.append("Grasshopper's tower differs from the reference Python generator by more than 1% in floor area. "
                        "Check the definition against examples/tower/GH_SPEC.md.")

    m = result["metrics"]
    plot = (brief["site"]["plot_width_m"], brief["site"]["plot_depth_m"]) if brief else None
    render_floors(geometry["curves"], geometry["floor_height"], run / "image.png", plot=plot, shadow=result["shadow"],
                  caption=f"{label}\nH {m['height_m']:g} m  |  GFA {m['gfa_m2']:,.0f} m2")

    runs.write_json(run / "meta.json", {
        "run_id": run.name,
        "system": SYSTEM,
        "label": label,
        "skill": args.skill,
        "why": args.why or "",
        "backend": args.backend,
        "brief_path": rel(args.brief) if args.brief else None,
        "brief_title": brief["title"] if brief else None,
        "created": datetime.now().isoformat(timespec="seconds"),
    })
    if brief:
        runs.write_json(run / "brief.json", brief)
    runs.write_json(run / "params.json", params)
    runs.write_json(run / "geometry.json", geometry)
    runs.write_json(run / "metrics.json", {k: result[k] for k in ("metrics", "labels", "units", "better", "priorities", "constraints", "sun")})

    summary = {
        "run": rel(run),
        "label": label,
        "backend": args.backend,
        "params": params,
        "defaults_used": sorted(set(BY_NAME) - set(given)),
        "metrics": m,
        "constraints": [{k: c[k] for k in ("metric", "op", "value", "actual", "pass")} for c in result["constraints"]],
        "image": rel(run / "image.png"),
        "warnings": warnings,
    }
    if not args.no_gallery:
        summary["gallery"] = rel(gallery.build())
    print(json.dumps(summary, indent=2))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tower", description="Tower Toy tools: generate, measure and compare stacked-floor towers.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("params", help="Show the parameters and metrics (the tools' contract).")
    p_check = sub.add_parser("check-brief", help="Check a structured brief against the schema and the tower's parameters and metrics.")
    p_check.add_argument("brief", help="Path to the brief JSON, e.g. studio/briefs/lighthouse-keeper.json")

    p_gen = sub.add_parser("generate", help="Build one tower variant, measure it and save it as a run.",
                           description="Build one tower variant, measure it and save it as a run. "
                                       "Parameters left out use their defaults. Prints a JSON summary.")
    for p in PARAMS:
        p_gen.add_argument("--" + p.name.replace("_", "-"), dest=p.name, type=p.kind, metavar=p.unit.upper() or "N",
                           help=f"{p.meaning} {p.low:g} to {p.high:g}, default {p.default:g}.")
    p_gen.add_argument("--brief", help="Structured brief to measure the result against (constraints, plot, sun).")
    p_gen.add_argument("--skill", default="manual", help="Name of the skill producing this run, for the gallery (default: manual).")
    p_gen.add_argument("--label", help="Short name for this variant, e.g. 'A: slim beacon'.")
    p_gen.add_argument("--why", help="One or two sentences on why this variant: the design intent.")
    p_gen.add_argument("--backend", choices=["grasshopper", "python"], default="grasshopper",
                       help="Who builds the geometry: Grasshopper via the bridge (default) or the Python generator.")
    p_gen.add_argument("--timeout", type=float, default=30.0, help="Seconds to wait for Grasshopper (default 30).")
    p_gen.add_argument("--no-gallery", action="store_true", help="Don't rebuild runs/gallery.html afterwards.")

    args = parser.parse_args(argv)
    if args.command == "params":
        return show_params()
    if args.command == "check-brief":
        return check_brief(Path(args.brief))
    return generate(args)


if __name__ == "__main__":
    sys.exit(main())
