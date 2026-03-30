import sys; from pathlib import Path
sys.path.append(
    str(Path(__file__).parent.parent)
)

from __future__ import annotations
import argparse
import dcst
from gceutils import grepr_dataclass
from pathlib import Path
import pmp_manip as p
from typing import Any



@grepr_dataclass()
class TNode:
    type: str
    attributes: dict[str, Any]

    @staticmethod
    def from_ast_node(node: dcst.DCST | TNode) -> TNode:
        if isinstance(node, TNode):
            return node
        attrs = {field: getattr(node, field) for field in node._fields}
        for key, value in attrs.items():
            if isinstance(value, dcst.DCST):
                attrs[key] = TNode.from_ast_node(value)
            elif isinstance(value, list):
                attrs[key] = [TNode.from_ast_node(item) if isinstance(item, dcst.DCST) else item for item in value]
        return TNode(
            type=type(node).__name__,
            attributes=attrs,
        )

    @staticmethod
    def try_convert(value: dcst.DCST | TNode | Any) -> TNode | Any:
        return TNode.from_ast_node(value) if isinstance(value, dcst.DCST) else value

@grepr_dataclass()
class InputValue:
    value: list[p.SRBlock] | p.SRBlock | str | bool | p.SRDropdownValue

    # TODO: add precise typing
    def as_type(self, input_type: type[p.SRInputValue]) -> p.SRInputValue:
        blocks = self.value if isinstance(self.value, list) else []
        block = self.value if isinstance(self.value, p.SRBlock) else None
        immediate = self.value if isinstance(self.value, (str, bool)) else (
            "" if input_type is p.SRBlockAndTextInputValue
            else False if input_type is p.SRBlockAndBoolInputValue
            else None
        )
        dropdown = self.value if isinstance(self.value, p.SRDropdownValue) else None

        match input_type:
            case p.SRBlockAndTextInputValue:
                return p.SRBlockAndTextInputValue(block=block, immediate=immediate)
            case p.SRBlockAndDropdownInputValue:
                return p.SRBlockAndDropdownInputValue(block=block, dropdown=dropdown)
            case p.SRBlockAndBoolInputValue:
                return p.SRBlockAndBoolInputValue(block=block, immediate=immediate)
            case p.SRBlockOnlyInputValue:
                return p.SRBlockOnlyInputValue(block=block)
            case p.SRScriptInputValue:
                return p.SRScriptInputValue(blocks=blocks)
            case p.SREmbeddedBlockInputValue:
                return p.SREmbeddedBlockInputValue(block=block)
            case _:
                raise ValueError()

    # TODO: remove temporary
    @staticmethod
    def try_as_type(value: InputValue | Any, input_type: type[p.SRInputValue]) -> p.SRInputValue | TNode:
        if isinstance(value, InputValue):
            return value.as_type(input_type)
        else:
            return TNode.from_ast_node(value)


class utils:
    @staticmethod
    def var_dd(name: str) -> p.SRDropdownValue:
        return p.SRDropdownValue(p.DropdownValueKind.VARIABLE, name)

    @staticmethod
    def var(name: str) -> p.SRBlock:
        return p.SRBlock(
            opcode="&variables::value of [VARIABLE]",
            dropdowns={"VARIABLE": utils.var_dd(name)}
        )

    @staticmethod
    def set_var(name: str, value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&variables::set [VARIABLE] to (VALUE)",
            inputs={"VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue)},
            dropdowns={"VARIABLE": utils.var_dd(name)}
        )


class Translator(dcst.NodeTransformer):
    def visit_Expr(self, node: dcst.Expr) -> p.SRBlock:
        return utils.set_var("__VOID__", self.visit(node.value))

    def visit_Module(self, node: dcst.Module) -> p.SRProject:
        #self.generic_visit(node)
        project = p.SRProject.create_empty()

        project.sprites = [TNode.try_convert(self.visit(each)) for each in node.body]
        #project.sprite_layer_stack = [sprite.uuid for sprite in project.sprites]
        project.extensions = [p.SRCustomExtension(
            id="moreTypesPlus",
            url=("https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/"+
            "refs/heads/main/extensions/moreTypesPlus.js"),
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
    tree = dcst.parse(text)
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
