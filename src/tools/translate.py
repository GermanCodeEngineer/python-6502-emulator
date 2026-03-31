from __future__ import annotations
import sys; from pathlib import Path
sys.path.append(
    str(Path(__file__).parent.parent)
)

import argparse
import dcst
from tools.translate_utils import InputValue, utils
from gceutils import AbstractTreePath
from pathlib import Path
import pmp_manip as p
from typing import Any, Iterable


class RestrictedTranslator(dcst.NodeTransformer):
    def get_ancestor_of_types[_T: dcst.DCST](self, path: AbstractTreePath, node_types: Iterable[type[_T]]) -> _T | None:
        """Get the nearest ancestor of the current node that is an instance of one of the given types."""
        node_types = tuple(node_types)
        current_path = path.go_up(1) # Start at parent
        while len(current_path) > 0:
            parent_node = self.get_path(current_path)
            if isinstance(parent_node, node_types):
                return parent_node
            current_path = current_path.go_up(1)
        return None

    def visit_ClassDef(self, node: dcst.ClassDef, path: AbstractTreePath) -> p.SRBlock:
        self.generic_visit(node, path)
        #ancestor = self.get_ancestor_of_types(path, dcst.SUBDEFINITION_ALLOWING_CLASSES)
        return utils.create_class_at(
            name=InputValue(node.name),
            substack=InputValue(node.body),
            #substack=InputValue([item for item in node.body if isinstance(item, p.SRBlock)]),
        )

    def visit_Constant(self, node: dcst.Constant, path: AbstractTreePath) -> InputValue:
        self.generic_visit(node, path)
        if isinstance(node.value, (str, bool)):
            return InputValue(node.value)
        else:
            return node

    def visit_Expr(self, node: dcst.Expr, path: AbstractTreePath) -> p.SRBlock:
        self.generic_visit(node, path)
        return utils.execute_expression(node.value)

    def visit_FunctionDef(self, node: dcst.FunctionDef, path: AbstractTreePath) -> p.SRBlock:
        self.generic_visit(node, path)
        ancestor = self.get_ancestor_of_types(path, dcst.SUBDEFINITION_ALLOWING_CLASSES)
        name = InputValue(node.name)
        substack = InputValue(node.body)
        if isinstance(ancestor, dcst.ClassDef):
            return utils.define_instance_method(name, substack)
        else:
            return utils.create_function_at(name, substack)

    def visit_Module(self, node: dcst.Module, path: AbstractTreePath) -> p.SRProject:
        project = p.SRProject.create_empty()
        sprite = p.SRSprite.create_empty(name="Translated Python")
        project.sprites = [sprite]
        project.sprite_layer_stack = [sprite.uuid for sprite in project.sprites]
        project.extensions = [p.SRCustomExtension(
            id="gceClassesOOP",
            url=("https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/"+
            "refs/heads/main/extensions/classes.js"),
        )]

        self.generic_visit(node, path)
        sprite.scripts.append(p.SRScript(
            position=(0, 0),
            blocks=node.body,
        ))
        sprite.local_variables.append(p.SRVariable(name="__VOID__", current_value=""))

        # Currently failes because of moreTypesPlus
        project.add_all_extensions_to_info_api(p.info_api)
        return project


class TemporaryCleaner(dcst.NodeTransformer):
    def generic_visit(self, node: dcst.DCST | Any, path: AbstractTreePath) -> Any:
        for field, old_value in dcst.iter_fields(node):
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if not isinstance(value, dcst.DCST):
                        new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, dcst.DCST):
                delattr(node, field)
        return node

def translate(filename: Path) -> None:
    cfg = p.get_default_config()
    handler = lambda url: url.startswith("https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/")
    cfg.ext_info_gen.is_trusted_extension_origin_handler = handler
    p.init_config(cfg)

    text = filename.read_text()
    tree = dcst.parse(text)
    translator = RestrictedTranslator()
    project: p.SRProject = translator.set_root_and_visit(tree)

    if False:
        project = TemporaryCleaner().set_root_and_visit(project)

    print(50*"=", "Translated Project", 50*"=")
    print(project)
    project.validate(AbstractTreePath(), p.info_api)
    frproject = project.to_first(p.info_api)
    frproject.to_file("generated.pmp")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path, help="The path to the file to translate.")
    args = parser.parse_args()

    translate(args.filename)

if __name__ == "__main__":
    main()
