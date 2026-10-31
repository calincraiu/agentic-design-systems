"""`uv run kit ...`: commands for the course plumbing itself.

  kit doctor            is this computer ready for the course?
  kit ping              is Grasshopper listening?
  kit gallery [--open]  rebuild (and open) runs/gallery.html
"""
import argparse
import importlib
import platform
import sys

from . import bridge, gallery
from .paths import ROOT, exchange_dir, rel, runs_dir


def ping(timeout):
    try:
        result = bridge.ping(timeout)
    except bridge.BridgeError as e:
        print(f"[!!] {e}")
        return 1
    control = "ON" if result.get("active") else "OFF (sliders in control)"
    print(f"[ok] Grasshopper is listening: system '{result.get('system')}', Agent control {control}, Rhino {result.get('rhino', '?')}")
    return 0


def doctor():
    ok = True
    print(f"[ok] Python {platform.python_version()} on {platform.system()} {platform.release()}")
    print(f"[ok] Repo folder: {ROOT}")
    for package in ("matplotlib", "jsonschema"):
        try:
            importlib.import_module(package)
            print(f"[ok] Package '{package}' is installed")
        except ImportError:
            ok = False
            print(f"[!!] Package '{package}' is missing: run `uv sync`")
    for folder in (runs_dir(), exchange_dir()):
        try:
            folder.mkdir(parents=True, exist_ok=True)
            probe = folder / ".write-test"
            probe.write_text("ok")
            probe.unlink()
            print(f"[ok] Can write to {rel(folder)}/")
        except OSError as e:
            ok = False
            print(f"[!!] Cannot write to {folder}: {e}")
    try:
        result = bridge.ping(2.0)
        print(f"[ok] Grasshopper is listening (system '{result.get('system')}')")
    except bridge.BridgeError:
        print("[--] Grasshopper is not listening. That's fine if Rhino isn't open yet; "
              "see `uv run kit ping` once it is.")
    print("Ready." if ok else "Not ready yet: fix the [!!] lines above.")
    return 0 if ok else 1


def main(argv=None):
    parser = argparse.ArgumentParser(prog="kit", description="Course plumbing: check the setup, talk to Grasshopper, browse runs.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Check that this computer is ready for the course.")
    p_ping = sub.add_parser("ping", help="Check that Grasshopper is listening.")
    p_ping.add_argument("--timeout", type=float, default=3.0, help="Seconds to wait for an answer (default 3).")
    p_gallery = sub.add_parser("gallery", help="Rebuild runs/gallery.html.")
    p_gallery.add_argument("--open", action="store_true", help="Also open it in the browser.")
    args = parser.parse_args(argv)

    if args.command == "doctor":
        return doctor()
    if args.command == "ping":
        return ping(args.timeout)
    if args.command == "gallery":
        path = gallery.build(open_browser=args.open)
        print(f"Gallery: {rel(path)}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
