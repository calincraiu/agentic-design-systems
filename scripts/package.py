"""Build the student copy of the course folder: dist/ads-course.zip.

  uv run scripts/package.py

It zips what is committed (git archive HEAD), so commit first. Folders marked
export-ignore in .gitattributes (instructor/, tests/, packaging/, scripts/) are
left out. The files in packaging/student/ then replace their repo versions:
CLAUDE.md tells Claude not to edit the course folder, and .claude/settings.json
denies edits to it.
"""
import argparse
import io
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLACE = ROOT / "packaging" / "student"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=str(ROOT / "dist" / "ads-course.zip"), help="Where to write the zip.")
    parser.add_argument("--folder", default="ads-course", help="Name of the folder inside the zip.")
    parser.add_argument("--ref", default="HEAD", help="Commit (or tree) to package (default HEAD).")
    args = parser.parse_args()

    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if dirty and args.ref == "HEAD":
        print("WARNING: uncommitted changes are NOT in the zip:\n" + dirty, file=sys.stderr)

    archive = subprocess.run(["git", "archive", "--format=zip", f"--prefix={args.folder}/", args.ref],
                             cwd=ROOT, capture_output=True, check=True).stdout
    replacements = {f"{args.folder}/{p.relative_to(REPLACE).as_posix()}": p for p in REPLACE.rglob("*") if p.is_file()}

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(archive)) as src, zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as dst:
        for info in src.infolist():
            data = replacements[info.filename].read_bytes() if info.filename in replacements else src.read(info)
            dst.writestr(info, data)  # keeps permissions, so the Mac launcher stays executable
        missing = set(replacements) - set(src.namelist())
        for name in sorted(missing):
            dst.write(replacements[name], name)

    print(f"Wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    print("Replaced with student versions: " + ", ".join(sorted(n.split("/", 1)[1] for n in replacements)))


if __name__ == "__main__":
    main()
