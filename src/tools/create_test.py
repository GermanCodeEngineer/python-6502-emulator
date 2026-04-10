from __future__ import annotations
import sys; from pathlib import Path
sys.path.append(
    str(Path(__file__).parent.parent)
)

import argparse
from tools.translate_blocks import CBlocks as c, PMBlocks
from utils import InputValue
from gceutils import AbstractTreePath
from pathlib import Path
import pmp_manip as p

def create_class_test():
    return p.SRScript(
        position=(0, 0),
        blocks=[
            c.create_class_at(
                name="Greeter",
                substack=[
                    c.define_instance_method(
                        name="greet", substack=[
                            c.return_("Hello, World!")
                        ]
                    )
                ]
            )
        ]
    )

def create_test() -> None:
    cfg = p.get_default_config()
    handler = lambda url: url.startswith("https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/")
    cfg.ext_info_gen.is_trusted_extension_origin_handler = handler
    p.init_config(cfg)

    project = p.SRProject.create_empty()
    project.stage.scripts = [create_class_test()]
    project.extensions = [p.SRCustomExtension(
        id="gceClassesOOP",
        url=("https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/"+
        "refs/heads/main/extensions/classes.js"),
    )]

    print(50*"=", "Created Project", 50*"=")
    print(project)
    project.add_all_extensions_to_info_api(p.info_api)
    project.validate(AbstractTreePath(), p.info_api)
    frproject = project.to_first(p.info_api)
    frproject.to_file("classes_test.pmp")


def main() -> None:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    create_test()

if __name__ == "__main__":
    main()
