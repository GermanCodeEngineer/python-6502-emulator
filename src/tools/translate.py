from __future__ import annotations
import sys; from pathlib import Path
sys.path.append(
    str(Path(__file__).parent.parent)
)

import argparse
import dcst
from tools.translate_utils import InputValue, CBlocks, PMBlocks
from gceutils import AbstractTreePath
from pathlib import Path
import pmp_manip as p
from typing import Iterable


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

    def visit_Assign(self, node: dcst.Assign, path: AbstractTreePath) -> p.SRBlock:
        self.generic_visit(node, path)
        if len(node.targets) > 1:
            raise NotImplementedError("Multiple assignment is not supported yet.")
        return CBlocks.set_var(
            name=node.targets[0],
            value=node.value,
        )

    def visit_ClassDef(self, node: dcst.ClassDef, path: AbstractTreePath) -> p.SRBlock:
        self.generic_visit(node, path)
        #ancestor = self.get_ancestor_of_types(path, dcst.SUBDEFINITION_ALLOWING_CLASSES)
        return CBlocks.create_class_at(
            name=InputValue(node.name),
            substack=InputValue(node.body),
            #substack=InputValue([item for item in node.body if isinstance(item, p.SRBlock)]),
        )

    def visit_Compare(self, node: dcst.Compare, path: AbstractTreePath) -> p.SRBlock:
        self.generic_visit(node, path)
        if len(node.ops) > 1:
            raise NotImplementedError("Chained comparisons are not supported yet.")
            # This implementation reevaluates the middle expression multiple times, which is not ideal.
            line_numbers_etc = dcst.get_code_reference_fields(node)
            new_node = dcst.BoolOp(
                op=dcst.And(),
                values=[
                    dcst.Compare(
                        left=node.left,
                        ops=node.ops[:1],
                        comparators=[node.comparators[0]],
                        **line_numbers_etc,
                    ),
                    dcst.Compare(
                        left=node.comparators[0],
                        ops=node.ops[1:],
                        comparators=node.comparators[1:],
                        **line_numbers_etc,
                    ),
                ],
                **line_numbers_etc,
            )
            return self.visit(new_node, path)

        left = node.left
        right = node.comparators[0]

        match type(node.ops[0]):
            case dcst.Eq: return CBlocks.operator_equals(left, right)
            case dcst.Gt: return CBlocks.operator_gt(left, right)
            case dcst.GtE: return CBlocks.operator_gte(left, right)
            case dcst.In: return CBlocks.operator_contains(left, right)
            case dcst.Is: return CBlocks.is_block(left, right)
            case dcst.IsNot: return CBlocks.operator_not(CBlocks.is_block(left, right))
            case dcst.Lt: return CBlocks.operator_lt(left, right)
            case dcst.LtE: return CBlocks.operator_lte(left, right)
            case dcst.NotEq: return CBlocks.operator_notequal(left, right)
            case dcst.NotIn: return CBlocks.operator_not(CBlocks.operator_contains(left, right))

        print(node)
        raise NotImplementedError(f"Comparison operator {type(node.ops[0])} is not supported yet.")

    def visit_Constant(self, node: dcst.Constant, path: AbstractTreePath) -> InputValue:
        self.generic_visit(node, path)
        if isinstance(node.value, (str, bool)):
            return InputValue(node.value)
        elif node.value is None:
            return InputValue(CBlocks.nothing())
        else:
            return node

    def visit_Expr(self, node: dcst.Expr, path: AbstractTreePath) -> p.SRBlock:
        self.generic_visit(node, path)
        return CBlocks.execute_expression(node.value)

    def visit_FunctionDef(self, node: dcst.FunctionDef, path: AbstractTreePath) -> p.SRBlock:
        self.generic_visit(node, path)
        ancestor = self.get_ancestor_of_types(path, dcst.SUBDEFINITION_ALLOWING_CLASSES)
        name = InputValue(node.name)
        substack = InputValue(node.body)
        if isinstance(ancestor, dcst.ClassDef):
            return CBlocks.define_instance_method(name, substack)
        else:
            return CBlocks.create_function_at(name, substack)

    def visit_If(self, node: dcst.If, path: AbstractTreePath) -> p.SRBlock:
        self.generic_visit(node, path)
        return PMBlocks.if_else_block(
            condition=node.test,
            if_substack=InputValue(node.body),
            else_substack=InputValue(node.orelse),
        )

    def visit_BoolOp(self, node: dcst.BoolOp, path: AbstractTreePath) -> InputValue:
        self.generic_visit(node, path)

        # Start with the first value (already visited/transformed)
        result = node.values[0]
        for val in node.values[1:]:
            match type(node.op):
                case dcst.And:
                    result = InputValue(CBlocks.operator_and(result, val))
                case dcst.Or:
                    result = InputValue(CBlocks.operator_or(result, val))

        return result

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

    def visit_Name(self, node: dcst.Name, path: AbstractTreePath) -> InputValue:
        self.generic_visit(node, path)
        # TODO # Temporarily just return the variable name
        return InputValue(node.id)


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
