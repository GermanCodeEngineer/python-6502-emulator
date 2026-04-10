from __future__ import annotations
import sys; from pathlib import Path
sys.path.append(
    str(Path(__file__).parent.parent)
)

import argparse
import black
import dcst as d
import keyword
from pathlib import Path
import pmp_manip as p
from pmp_manip.opcode_info import api as info


PMP_MANIP_NAME = d.Name(id="p", ctx=d.Load())
INPUT_VALUE_NAME = d.Name(id="InputValue", ctx=d.Load())
DROPDOWN_VALUE_NAME = d.Name(id="SRDropdownValue", ctx=d.Load())
DROPDOWN_VALUE_KIND_NAME = d.Name(id="DropdownValueKind", ctx=d.Load())
STR_NAME = d.Name(id="str", ctx=d.Load())
STATICMETHOD_NAME = d.Name(id="staticmethod", ctx=d.Load())

def pick_legal_name(target_name: str) -> str:
    if keyword.iskeyword(target_name):
        return target_name + "_"
    return target_name


def create_imports() -> list[d.Import | d.ImportFrom]:
    return [
        d.ImportFrom(
            module="__future__",
            names=[
                d.alias(name="annotations", asname=None),
            ],
            level=0,
        ),
        d.Import(
            names=[
                d.alias(name="pmp_manip", asname=PMP_MANIP_NAME.id),
            ],
        ),
        d.ImportFrom(
            module="utils",
            names=[
                d.alias(name=INPUT_VALUE_NAME.id, asname=None),
            ],
            level=0,
        ),
    ]

def create_input_value_call(input_id: str, input_info: info.InputInfo, class_name: str) -> d.Call:
    if input_info.type.mode is info.InputMode.FORCED_EMBEDDED_BLOCK:
        # Use constant blocks for shadow inputs
        shadow_opcode = input_info.type.embedded_block_opcode.split("_")[1]
        try_as_type_arg = d.Call(
            func=INPUT_VALUE_NAME,
            args=[
                d.Call(
                    func=d.Attribute(
                        value=d.Name(id=class_name, ctx=d.Load()),
                        attr=pick_legal_name(shadow_opcode),
                        ctx=d.Load(),
                    ),
                    args=[],
                    keywords=[],
                ),
            ],
            keywords=[],
        )
    else:
        try_as_type_arg = d.Name(id=pick_legal_name(input_id.lower()), ctx=d.Load())

    example_input_value = p.SRInputValue.from_mode(input_info.type.mode)

    return d.Call(
        func=d.Attribute(
            value=INPUT_VALUE_NAME,
            attr="try_as_type",
            ctx=d.Load(),
        ),
        args=[
            try_as_type_arg,
            d.Attribute(
                value=PMP_MANIP_NAME,
                attr=pick_legal_name(type(example_input_value).__name__),
                ctx=d.Load(),
            ),
        ],
        keywords=[],
    )

def create_dropdown_value_call(dropdown_id: str) -> d.Call:
    return d.Call(
        func=d.Attribute(
            value=PMP_MANIP_NAME,
            attr=DROPDOWN_VALUE_NAME.id,
            ctx=d.Load(),
        ),
        args=[
            d.Attribute(
                value=d.Attribute(
                    value=PMP_MANIP_NAME,
                    attr=DROPDOWN_VALUE_KIND_NAME.id,
                    ctx=d.Load(),
                ),
                attr="STANDARD",
                ctx=d.Load(),
            ),
            d.Name(id=pick_legal_name(dropdown_id.lower()), ctx=d.Load()),
        ],
        keywords=[],
    )

def create_block_call(
        old_opcode: str, class_name: str,
        input_infos: dict[str, info.InputInfo],
        dropdown_infos: dict[str, info.DropdownInfo],
    ) -> d.Call:
    new_opcode = p.info_api.get_new_by_old(old_opcode)

    input_keys = []
    input_values = []
    for input_id, input_info in input_infos.items():
        input_keys.append(d.Constant(value=input_id, kind=None))
        input_values.append(create_input_value_call(input_id, input_info, class_name))

    dropdown_keys = []
    dropdown_values = []
    for dropdown_id, dropdown_info in dropdown_infos.items():
        dropdown_keys.append(d.Constant(value=dropdown_id, kind=None))
        dropdown_values.append(create_dropdown_value_call(dropdown_id))

    return d.Call(
        func=d.Attribute(
            value=PMP_MANIP_NAME,
            attr="SRBlock",
            ctx=d.Load(),
        ),
        args=[],
        keywords=[
            d.keyword(
                arg="opcode",
                value=d.Constant(value=new_opcode, kind=None),
            ),
            d.keyword(
                arg="inputs",
                value=d.Dict(
                    keys=input_keys,
                    values=input_values,
                ),
            ),
            d.keyword(
                arg="dropdowns",
                value=d.Dict(
                    keys=dropdown_keys,
                    values=dropdown_values,
                ),
            ),
        ],
    )

def create_staticmethod(old_opcode: str, opcode_info: info.OpcodeInfo, class_name: str) -> d.FunctionDef:
    block_id = pick_legal_name(old_opcode.split("_")[1])
    input_infos = opcode_info.get_new_input_ids_infos(
        block=None, fti_if=None # hope that block is not needed
    )
    dropdown_infos = opcode_info.get_new_dropdown_ids_infos()

    args = []
    for input_id, input_info in input_infos.items():
        # Skip shadow blocks (not needed as inputs)
        if input_info.type.mode is info.InputMode.FORCED_EMBEDDED_BLOCK:
            continue
        arg = d.arg(
            arg=pick_legal_name(input_id.lower()),
            annotation=INPUT_VALUE_NAME,
            type_comment=None,
        )
        args.append(arg)

    for dropdown_id, dropdown_info in dropdown_infos.items():
        arg = d.arg(
            arg=pick_legal_name(dropdown_id.lower()),
            annotation=STR_NAME,
            type_comment=None,
        )
        args.append(arg)

    return d.FunctionDef(
        name=block_id,
        args=d.arguments(
            posonlyargs=[],
            args=args,
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        ),
        body=[
            d.Return(
                value=create_block_call(old_opcode, class_name, input_infos, dropdown_infos)
            ),
        ],
        decorator_list=[
            STATICMETHOD_NAME,
        ],
        returns=d.Attribute(
            value=PMP_MANIP_NAME,
            attr="SRBlock",
            ctx=d.Load(),
        ),
        type_comment=None,
        type_params=[],
    )

def create_module(extension_id: str) -> d.Module:
    opcode_prefix = extension_id + "_"
    class_name = pick_legal_name(extension_id)
    body = []
    for old_opcode in p.info_api.all_old:
        if not old_opcode.startswith(opcode_prefix):
            continue

        body.append(create_staticmethod(
            old_opcode=old_opcode,
            opcode_info=p.info_api.get_info_by_old(old_opcode),
            class_name=class_name,
        ))

    return d.Module(
        body=[
            *create_imports(),
            d.ClassDef(
                name=class_name,
                bases=[],
                keywords=[],
                body=body,
                decorator_list=[],
                type_params=[],
            ),
        ],
        type_ignores=[],
    )

def create_extension_file(extension_id: str, extension_source: str, output_path: Path) -> None:
    p.info_api.generate_and_add_extension(
        extension_id=extension_id,
        extension_source=extension_source,
    )

    module = create_module(extension_id)
    code = d.unparse(module)
    code = black.format_str(code, mode=black.Mode(line_length=88))
    output_path.write_text(code)

def create_helpers() -> None:
    cfg = p.get_default_config()
    handler = lambda url: url.startswith("https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/")
    cfg.ext_info_gen.is_trusted_extension_origin_handler = handler
    p.init_config(cfg)

    create_extension_file(
        extension_id="gceClassesOOP",
        extension_source=("https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/"+
        "refs/heads/main/extensions/classes.js"),
        output_path=Path("src/extensions/gceClassesOOP.py"),
    )
    create_extension_file(
        extension_id="gceTestRunner",
        extension_source=("https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/"+
        "refs/heads/main/extensions/testRunner.js"),
        output_path=Path("src/extensions/gceTestRunner.py"),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    create_helpers()

if __name__ == "__main__":
    main()
