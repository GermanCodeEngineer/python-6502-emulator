from __future__ import annotations
import argparse
import ast
from gceutils import grepr_dataclass
from pathlib import Path
import pmp_manip as p
from typing import Any


@grepr_dataclass()
class TNode:
    type: str
    attributes: dict[str, Any]

    def from_ast_node(node: ast.AST) -> TNode:
        attrs = {field: getattr(node, field) for field in node._fields}
        for key, value in attrs.items():
            if isinstance(value, ast.AST):
                attrs[key] = TNode.from_ast_node(value)
            elif isinstance(value, list):
                attrs[key] = [TNode.from_ast_node(item) if isinstance(item, ast.AST) else item for item in value]
        return TNode(
            type=type(node).__name__,
            attributes=attrs,
        )


class Translator(ast.NodeTransformer):
    def visit_Module(self, node: ast.Module) -> None:
        self.generic_visit(node)
        project = p.SRProject.create_empty()

        project.sprites = [TNode.from_ast_node(self.visit(each)) for each in node.body]
        #project.sprite_layer_stack = [sprite.uuid for sprite in project.sprites]
        project.extensions = [p.SRCustomExtension(
            id="moreTypesPlus",
            url="https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/refs/heads/main/extensions/moreTypesPlus.js",
        )]
        # Currently failes because of moreTypesPlus
        #project.add_all_extensions_to_info_api(p.info_api)
        return project

def translate(filename: Path) -> None:
    cfg = p.get_default_config()
    handler = lambda url: url.startswith("https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/")
    cfg.ext_info_gen.is_trusted_extension_origin_handler = handler
    p.init_config(cfg)

    text = filename.read_text()
    tree = ast.parse(text)
    translator = Translator()
    project: p.SRProject = translator.visit(tree)
    #project.validate(gceutils.AbstractTreePath(), p.info_api)
    print(50*"=", "Translated Project", 50*"=")
    print(project)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path, help="The path to the file to translate.")
    args = parser.parse_args()

    translate(args.filename)

if __name__ == "__main__":
    main()
