"""Generate simplified dataclass definitions for AST node names listed
in src/ast_internal/restore_ast.py and write them to
src/ast_internal/simple_ast.py.

Run from repository root:

    python tools/generate_simple_ast.py
"""
from __future__ import annotations
import ast as pyast
from pathlib import Path
from typing import Any, Optional
import ast

ROOT = Path(__file__).resolve().parent.parent
RESTORE = ROOT / "src" / "ast_internal" / "restore_ast.py"
OUT = ROOT / "src" / "ast_internal" / "simple_ast.py"


def load_names(path: Path):
    text = path.read_text(encoding="utf8")
    # restore_ast.py contains a bare list literal; evaluate it safely
    try:
        names = pyast.literal_eval(text)
    except Exception:
        # fallback: parse lines that look like strings
        names = []
        for line in text.splitlines():
            line = line.strip().strip(',')
            if line.startswith('"') and line.endswith('"'):
                names.append(line.strip('"'))
    return names


def get_declared_base_name(name: str, names_set: set[str]) -> str:
    cls = getattr(ast, name, None)
    if cls is None:
        return "AST"
    bases = getattr(cls, "__bases__", ())
    for base in bases:
        base_name = getattr(base, "__name__", None)
        if base_name in names_set:
            return base_name
    # no known base within our list -> use AST as the generated root
    return "AST"


def generate_dataclasses(names: list[str]) -> str:
    header = """from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

# Simple, auto-generated dataclasses for AST node names
# Fields are annotated as Optional[Any] for simplicity.

"""
    names = [n for n in names if n.isidentifier()]
    names_set = set(names)

    # determine declared base (within our generated set) for each name
    declared_base: dict[str, str] = {n: get_declared_base_name(n, names_set) for n in names}

    # compute levels (AST -> 0)
    levels: dict[str, int] = {}
    if "AST" in names_set:
        levels["AST"] = 0
    # iteratively assign levels where base level is known
    remaining = set(names)
    while remaining:
        progressed = False
        for n in list(remaining):
            base = declared_base.get(n, "AST")
            if n == base:
                levels[n] = levels.get(base, 0)
                remaining.remove(n)
                progressed = True
                continue
            if base in levels:
                levels[n] = levels[base] + 1
                remaining.remove(n)
                progressed = True
        if not progressed:
            # break cycles / unknowns: assign next available level
            max_level = max(levels.values(), default=0)
            for n in sorted(remaining):
                levels[n] = max_level + 1
                remaining.remove(n)
            break

    # sort names by level then alphabetically
    ordered = sorted(names, key=lambda n: (levels.get(n, 999), n))

    def infer_annotation(field: str) -> str:
        # common scalar names
        if field in {"name", "id", "attr", "arg"}:
            return "str"
        if field in {"lineno", "col_offset", "end_lineno", "end_col_offset"}:
            return "int"
        if field == "ctx":
            return "expr_context"
        if field in {"type_comment", "kind"}:
            return "Optional[str]"

        # plural fields -> lists of AST nodes
        plurals = {
            "body",
            "orelse",
            "finalbody",
            "decorator_list",
            "targets",
            "args",
            "keywords",
            "elts",
            "names",
            "keys",
            "values",
            "comparators",
            "bases",
            "generators",
            "kw_defaults",
            "defaults",
            "kwonlyargs",
            "posonlyargs",
            "type_ignores",
            "cases",
            "patterns",
        }
        if field in plurals or field.endswith("s"):
            # try to infer element type from singular form
            # common irregulars
            irregular = {
                "names": "alias",
                "keywords": "keyword",
                "args": "arg",
                "generators": "comprehension",
                "cases": "match_case",
                "patterns": "pattern",
                "type_ignores": "type_ignore",
                "type_params": "type_param",
            }
            elem = irregular.get(field, None)
            if elem is None:
                if field.endswith("s"):
                    elem = field[:-1]
            if elem and elem in names_set:
                return f"list[{elem}]"
            return "list[AST]"

        # if the field name matches a generated class, use it
        if field in names_set:
            return f"Optional[{field}]"

        # likely single AST node
        return "Optional[AST]"

    out_lines = [header]
    for name in ordered:
        out_lines.append("@dataclass")
        base = declared_base.get(name, "AST")
        # special-case the root AST class: emit no base
        if name == "AST":
            out_lines.append(f"class {name}:")
        else:
            # if the base would be the same as the class (rare), fallback to AST
            if base == name:
                base = "AST"
            out_lines.append(f"class {name}({base}):")
        cls = getattr(ast, name, None)
        fields = getattr(cls, "_fields", ()) or () if cls is not None else ()
        if not fields:
            out_lines.append("    pass\n")
        else:
            for f in fields:
                attr = f if f.isidentifier() else f"field_{f}"
                ann = infer_annotation(f)
                out_lines.append(f"    {attr}: {ann} = None")
            out_lines.append("")
    return "\n".join(out_lines)


def main() -> None:
    if not RESTORE.exists():
        print(f"restore list not found at {RESTORE}")
        return
    names = load_names(RESTORE)
    code = generate_dataclasses(names)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(code, encoding="utf8")
    print(f"Wrote simplified AST dataclasses to {OUT}")


if __name__ == "__main__":
    main()
