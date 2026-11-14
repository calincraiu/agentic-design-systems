# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""A tool: checks whether a straight stair fits and is comfortable. Built from tools/stair_check.md."""
import argparse
import math

parser = argparse.ArgumentParser(description="Check a straight stair between two floors.")
parser.add_argument("--floor-height", type=float, required=True, help="Floor to floor, in m (2 to 6).")
parser.add_argument("--run", type=float, required=True, help="Horizontal length available, in m (more than 0, up to 20).")
parser.add_argument("--max-riser", type=float, default=175, help="Highest step allowed, in mm (120 to 220, default 175).")
parser.add_argument("--min-going", type=float, default=250, help="Shallowest tread allowed, in mm (200 to 350, default 250).")
args = parser.parse_args()

if not 2 <= args.floor_height <= 6:
    parser.error("floor height must be between 2 and 6 m")
if not 0 < args.run <= 20:
    parser.error("run must be more than 0 and at most 20 m")
if not 120 <= args.max_riser <= 220:
    parser.error("max riser must be between 120 and 220 mm")
if not 200 <= args.min_going <= 350:
    parser.error("min going must be between 200 and 350 mm")

height_mm = args.floor_height * 1000
risers = math.ceil(height_mm / args.max_riser)
riser = height_mm / risers
treads = risers - 1
going = args.run * 1000 / treads
blondel = 2 * riser + going
pitch = math.degrees(math.atan(riser / going))

print(f"Risers: {risers} x {riser:.1f} mm")
print(f"Treads: {treads} x {going:.1f} mm")
print(f"Pitch: {pitch:.1f} deg")
print(f"Blondel 2R+G: {blondel:.1f} mm")
print(f"{'PASS' if riser <= args.max_riser else 'FAIL'}  riser {riser:.1f} <= {args.max_riser:g} mm")
print(f"{'PASS' if going >= args.min_going else 'FAIL'}  going {going:.1f} >= {args.min_going:g} mm")
print(f"{'PASS' if 600 <= blondel <= 650 else 'FAIL'}  Blondel {blondel:.1f} between 600 and 650 mm")
