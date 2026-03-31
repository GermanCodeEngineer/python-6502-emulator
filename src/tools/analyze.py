import sys; from pathlib import Path
sys.path.append(
    str(Path(__file__).parent.parent)
)

import dcst
import argparse
from itertools import combinations, product
from pathlib import Path


def _format_type(value: object) -> str:
    if isinstance(value, dcst.DCST):
        return type(value).__name__

    if isinstance(value, list):
        if not value:
            return "list[empty]"

        item_types = sorted({_format_type(item) for item in value})
        return f"list[{'|'.join(item_types)}]"

    if value is None:
        return "None"

    return type(value).__name__


def _list_type_variations(values: list[object]) -> list[str]:
    if not values:
        return ["list[empty]"]

    unique_types = sorted({_format_type(item) for item in values})
    variations: set[str] = set()

    # Include every non-empty subset, e.g. list[A], list[B], list[A|B].
    for subset_size in range(1, len(unique_types) + 1):
        for subset in combinations(unique_types, subset_size):
            variations.add(f"list[{'|'.join(subset)}]")

    return sorted(variations, key=lambda item: (item.count("|") + 1, item))


def _format_line_range(node: dcst.DCST) -> str:
    start = getattr(node, "lineno", None)
    end = getattr(node, "end_lineno", start)

    if start is None:
        return "[l.?]"

    if end is None or end == start:
        return f"[l.{start}]"

    return f"[l.{start}-{end}]"


def _signature_variations(node: dcst.DCST) -> set[str]:
    field_names: list[str] = []
    field_variations: list[list[str]] = []

    for field_name, value in dcst.iter_fields(node):
        field_names.append(field_name)
        if isinstance(value, list):
            field_variations.append(_list_type_variations(value))
        else:
            field_variations.append([_format_type(value)])

    if not field_names:
        return {f"{type(node).__name__}()"}

    signatures: set[str] = set()
    for variation in product(*field_variations):
        fields = [f"{name}:{field_type}" for name, field_type in zip(field_names, variation)]
        signatures.add(f"{type(node).__name__}({', '.join(fields)})")

    return signatures


def _collect_node_signatures(tree: dcst.DCST) -> tuple[list[tuple[str, str]], list[str]]:
    found: dict[str, str] = {}
    all_node_types: set[str] = set()

    for node in dcst.walk(tree):
        all_node_types.add(type(node).__name__)

        for signature in _signature_variations(node):
            found.setdefault(signature, _format_line_range(node))

    return sorted(found.items()), sorted(all_node_types)

def analyze(filename: Path) -> None:
    text = filename.read_text()

    tree = dcst.parse(text)
    print(tree)
    print()
    print(50*"=", "Node Types", 50*"=")
    signatures, all_node_types = _collect_node_signatures(tree)
    for signature, line_range in signatures:
        print(f"{signature} {line_range}")

    print()
    print(50*"=", "All Node Types (No Signature Distinction)", 50*"=")
    for node_type in all_node_types:
        print(node_type)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path, help="The path to the file to analyze.")
    args = parser.parse_args()

    analyze(args.filename)

if __name__ == "__main__":
    main()
