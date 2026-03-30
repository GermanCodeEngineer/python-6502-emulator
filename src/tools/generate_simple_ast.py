"""Generate simplified dataclass definitions for AST node names listed
in src/ast_internal/restore_ast.py and write them to
src/ast_internal/simple_ast.py.

Run from repository root:

    python tools/generate_simple_ast.py
"""
from __future__ import annotations
import ast as pyast
import re
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[2]
RESTORE = ROOT / "src" / "ast_internal" / "restore_ast.py"
OUT = ROOT / "src" / "ast_internal" / "simple_ast.py"
PYI = ROOT / "src" / "ast_internal" / "ast_pyi.pyi"


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


def _normalize_pyi_annotation(annotation: str) -> str:
    ann = annotation.strip()
    if "#" in ann:
        ann = ann.split("#", 1)[0].rstrip()

    # Strip module qualifiers used in stubs where possible.
    ann = re.sub(r"\bbuiltins\.([A-Za-z_]\w*)\b", r"\1", ann)
    ann = re.sub(r"\bast_py\.([A-Za-z_]\w*)\b", r"\1", ann)

    return ann.strip()


def load_pyi_field_annotations(path: Path) -> dict[str, dict[str, str]]:
    """Read class field annotations from ast_pyi.pyi.

    The parser is intentionally simple and line-based. It captures class-level
    annotated attributes (e.g. "body: list[stmt]") and ignores methods and
    overloads. When a field is repeated across version guards, first seen wins.
    """
    text = path.read_text(encoding="utf8")
    lines = text.splitlines()

    result: dict[str, dict[str, str]] = {}
    current_class: str | None = None
    class_indent = 0

    class_re = re.compile(r"^(?P<indent>\s*)class\s+(?P<name>[A-Za-z_]\w*)\b")
    field_re = re.compile(r"^(?P<indent>\s*)(?P<name>[A-Za-z_]\w*)\s*:\s*(?P<ann>.+)$")

    for raw_line in lines:
        line = raw_line.rstrip("\n")
        stripped = line.strip()

        class_match = class_re.match(line)
        if class_match:
            current_class = class_match.group("name")
            class_indent = len(class_match.group("indent"))
            result.setdefault(current_class, {})
            continue

        if current_class is None:
            continue

        if stripped:
            indent = len(line) - len(line.lstrip(" "))
            if indent <= class_indent:
                current_class = None
                class_indent = 0
                continue

        if not stripped or stripped.startswith("def ") or stripped.startswith("@"):
            continue
        if stripped.startswith("if ") or stripped.startswith("elif ") or stripped.startswith("else"):
            continue

        field_match = field_re.match(line)
        if not field_match:
            continue

        field_name = field_match.group("name")
        ann = _normalize_pyi_annotation(field_match.group("ann"))
        if not ann:
            continue
        # __match_args__ assignment and similar are not field annotations.
        if "=" in ann:
            ann = ann.split("=", 1)[0].strip()
        if not ann:
            continue

        result[current_class].setdefault(field_name, ann)

    return result


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


def generate_dataclasses(
    names: list[str],
    pyi_field_annotations: dict[str, dict[str, str]],
) -> str:
    header = """from __future__ import annotations
from gceutils import grepr_dataclass

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

    def annotation_for(name: str, field: str) -> str:
        cls_annotations = pyi_field_annotations.get(name, {})
        ann = cls_annotations.get(field)
        if ann:
            return ann
        return "Any"

    def class_fields(name: str) -> list[str]:
        cls = getattr(ast, name, None)

        # pyi fields include attributes like lineno/col_offset that do not
        # necessarily appear in runtime _fields.
        pyi_fields = [
            field_name
            for field_name in pyi_field_annotations.get(name, {}).keys()
            if field_name.isidentifier() and not field_name.startswith("_")
        ]

        runtime_fields = list(getattr(cls, "_fields", ()) or ()) if cls is not None else []
        combined: list[str] = []
        for field_name in [*pyi_fields, *runtime_fields]:
            if field_name.isidentifier() and field_name not in combined:
                combined.append(field_name)
        return combined

    out_lines = [header]
    for name in ordered:
        out_lines.append("@grepr_dataclass()")
        base = declared_base.get(name, "AST")
        # special-case the root AST class: emit no base
        if name == "AST":
            out_lines.append(f"class {name}:")
        else:
            # if the base would be the same as the class (rare), fallback to AST
            if base == name:
                base = "AST"
            out_lines.append(f"class {name}({base}):")
        fields = class_fields(name)
        if not fields:
            out_lines.append("    pass\n")
        else:
            for f in fields:
                attr = f if f.isidentifier() else f"field_{f}"
                ann = annotation_for(name, f)
                out_lines.append(f"    {attr}: {ann} = None")
            out_lines.append("")
    return "\n".join(out_lines)


def main() -> None:
    if not RESTORE.exists():
        print(f"restore list not found at {RESTORE}")
        return
    if not PYI.exists():
        print(f"stub file not found at {PYI}")
        return
    names = load_names(RESTORE)
    pyi_field_annotations = load_pyi_field_annotations(PYI)
    code = generate_dataclasses(names, pyi_field_annotations)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(code, encoding="utf8")
    print(f"Wrote simplified AST dataclasses to {OUT}")


if __name__ == "__main__":
    main()
