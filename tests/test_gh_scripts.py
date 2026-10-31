"""The Grasshopper scripts must run in Rhino 7 (IronPython 2.7) as well as Rhino 8 (Python 3).

We can't run them here, but we can make sure they parse and use no Python-3-only syntax.
"""
import ast
from pathlib import Path

import pytest

from kit.paths import ROOT

SCRIPTS = [ROOT / "kit" / "gh" / "listener.py", ROOT / "kit" / "gh" / "writer.py", ROOT / "examples" / "tower" / "unpack.py"]

PY3_ONLY = (ast.JoinedStr, ast.Nonlocal, ast.AnnAssign, ast.AsyncFunctionDef, ast.YieldFrom, ast.NamedExpr, ast.Await)


@pytest.mark.parametrize("path", SCRIPTS, ids=lambda p: p.name)
def test_script_is_ironpython_compatible(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        assert not isinstance(node, PY3_ONLY), f"{path.name}:{node.lineno} uses {type(node).__name__}"
        if isinstance(node, (ast.FunctionDef, ast.Lambda)):
            args = node.args
            assert not args.kwonlyargs, f"{path.name}:{node.lineno} keyword-only arguments"
            assert not any(a.annotation for a in args.args), f"{path.name}:{node.lineno} annotations"
        if isinstance(node, ast.FunctionDef):
            assert node.returns is None, f"{path.name}:{node.lineno} return annotation"
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == "print":
            assert not node.keywords, f"{path.name}:{node.lineno} print(..., end=/file=)"
        if isinstance(node, (ast.Assign, ast.For)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for t in targets:
                assert not any(isinstance(n, ast.Starred) for n in ast.walk(t)), f"{path.name}:{node.lineno} starred unpacking"


def test_unpack_handles_every_tower_parameter():
    from examples.tower.params import PARAMS

    source = (ROOT / "examples" / "tower" / "unpack.py").read_text(encoding="utf-8")
    for p in PARAMS:
        assert f"slider_{p.name}" in source
        assert f"\n{p.name} = " in source
