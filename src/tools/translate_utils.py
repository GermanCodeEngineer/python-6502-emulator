from __future__ import annotations
from gceutils import grepr_dataclass
from typing import Any
import pmp_manip as p


@grepr_dataclass()
class InputValue:
    value: list[p.SRBlock] | p.SRBlock | str | bool | p.SRDropdownValue

    # TODO: add copy?
    def as_type[_T: p.SRInputValue](self, input_type: type[_T]) -> _T:
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
    def try_as_type[_T: p.SRInputValue](value: InputValue | Any, input_type: type[_T]) -> _T | Any:
        if isinstance(value, InputValue):
            return value.as_type(input_type)
        else:
            return value


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

    # Helper for standard dropdown values
    @staticmethod
    def dd_standard(value: str) -> p.SRDropdownValue:
        return p.SRDropdownValue(p.DropdownValueKind.STANDARD, value)

    # ---------------------- Class manipulation ----------------------
    @staticmethod
    def create_class_at(name: InputValue, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create class at (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(InputValue(utils.class_being_created()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def create_subclass_at(name: InputValue, superclass: InputValue, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create subclass at (NAME) with superclass (SUPERCLASS) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SUPERCLASS": InputValue.try_as_type(superclass, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(InputValue(utils.nothing()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def create_class_named(name: InputValue, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create class named (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(InputValue(utils.class_being_created()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def create_subclass_named(name: InputValue, superclass: InputValue, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create subclass named (NAME) with superclass (SUPERCLASS) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SUPERCLASS": InputValue.try_as_type(superclass, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(InputValue(utils.class_being_created()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def on_class(class_name: InputValue, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on class (CLASS) {:SHADOW:} {SUBSTACK}",
            inputs={
                "CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(InputValue(utils.class_being_created()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def class_being_created() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::class being created")

    @staticmethod
    def set_class(name: InputValue, clazz: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::set class (NAME) to (CLASS)",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "CLASS": InputValue.try_as_type(clazz, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def get_class(name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get class (NAME)",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def class_exists(name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::class (NAME) exists?",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def all_classes() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::all classes")

    @staticmethod
    def delete_class(name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::delete class (NAME)",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def delete_all_classes() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::delete all classes")

    @staticmethod
    def is_subclass(subclass: InputValue, superclass: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::is (SUBCLASS) a subclass of (SUPERCLASS) ?",
            inputs={
                "SUBCLASS": InputValue.try_as_type(subclass, p.SRBlockAndTextInputValue),
                "SUPERCLASS": InputValue.try_as_type(superclass, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def get_superclass(class_name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get superclass of (CLASS)",
            inputs={"CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue)},
        )

    # ---------------------- Methods / Functions ----------------------
    @staticmethod
    def define_instance_method(name: InputValue, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define instance method (NAME) {:SHADOW1:} {:SHADOW2:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW1": InputValue.try_as_type(InputValue(utils.self_block()), p.SREmbeddedBlockInputValue),
                "SHADOW2": InputValue.try_as_type(InputValue(utils.all_function_args()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def define_special_method(special: str, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define [SPECIAL_METHOD] method {:SHADOW1:} {:SHADOW2:} {SUBSTACK}",
            inputs={
                "SHADOW1": InputValue.try_as_type(InputValue(utils.self_block()), p.SREmbeddedBlockInputValue),
                "SHADOW2": InputValue.try_as_type(InputValue(utils.all_function_args()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={"SPECIAL_METHOD": utils.dd_standard(special)},
        )

    @staticmethod
    def self_block() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::self")

    @staticmethod
    def call_super_method(name: InputValue, posargs: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::call super method (NAME) with positional args (POSARGS)",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def call_super_init_method(posargs: InputValue, ) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::call super init method with positional args (POSARGS)",
            inputs={"POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def define_getter(name: InputValue, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define getter (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(InputValue(utils.self_block()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def define_setter(name: InputValue, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define setter (NAME) {:SHADOW1:} {:SHADOW2:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW1": InputValue.try_as_type(InputValue(utils.self_block()), p.SREmbeddedBlockInputValue),
                "SHADOW2": InputValue.try_as_type(InputValue(utils.define_setter_value()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def define_setter_value() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::value")

    @staticmethod
    def define_operator_method(operator_kind: str, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define operator method [OPERATOR_KIND] {:SHADOW:} {SUBSTACK}",
            inputs={
                "SHADOW": InputValue.try_as_type(InputValue(utils.operator_other_value()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={"OPERATOR_KIND": utils.dd_standard(operator_kind)},
        )

    @staticmethod
    def operator_other_value() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::other value")

    # ---------------------- Class variables / attributes ----------------------
    @staticmethod
    def set_class_variable(class_name: InputValue, name: InputValue, value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (CLASS) set class variable (NAME) to (VALUE)",
            inputs={
                "CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def get_class_variable(name: InputValue, class_name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get class variable (NAME) of (CLASS)",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def delete_class_variable(class_name: InputValue, name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (CLASS) delete class variable (NAME)",
            inputs={
                "CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def define_static_method(name: InputValue, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define static method (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(InputValue(utils.all_function_args()), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def property_names_of_class(property_name: str, class_name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::[PROPERTY] names of class (CLASS)",
            inputs={"CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue)},
            dropdowns={"PROPERTY": utils.dd_standard(property_name)},
        )

    # ---------------------- Instances / attributes ----------------------
    @staticmethod
    def create_instance(class_name: InputValue, posargs: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create instance of class (CLASS) with positional args (POSARGS)",
            inputs={
                "CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def is_instance(instance: InputValue, class_name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::is (INSTANCE) an instance of (CLASS) ?",
            inputs={
                "INSTANCE": InputValue.try_as_type(instance, p.SRBlockAndTextInputValue),
                "CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def get_class_of_instance(instance: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get class of (INSTANCE)",
            inputs={"INSTANCE": InputValue.try_as_type(instance, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def set_attribute(instance: InputValue, name: InputValue, value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (INSTANCE) set attribute (NAME) to (VALUE)",
            inputs={
                "INSTANCE": InputValue.try_as_type(instance, p.SRBlockAndTextInputValue),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def get_attribute(name: InputValue, instance: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::attribute (NAME) of (INSTANCE)",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "INSTANCE": InputValue.try_as_type(instance, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def get_all_attributes(instance: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::all attributes of (INSTANCE)",
            inputs={"INSTANCE": InputValue.try_as_type(instance, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def call_method(instance: InputValue, name: InputValue, posargs: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (INSTANCE) call method (NAME) with positional args (POSARGS)",
            inputs={
                "INSTANCE": InputValue.try_as_type(instance, p.SRBlockAndTextInputValue),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def call_static_method(class_name: InputValue, name: InputValue, posargs: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (CLASS) call static method (NAME) with positional args (POSARGS)",
            inputs={
                "CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def get_static_method_func(name: InputValue, class_name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get static method (NAME) of (CLASS) as function",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "CLASS": InputValue.try_as_type(class_name, p.SRBlockAndTextInputValue),
            },
        )

    # ---------------------- Function configuration / calls ----------------------
    @staticmethod
    def configure_next_function_args(argnames: InputValue, argdefaults: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::configure next function: argument names (ARGNAMES) defaults (ARGDEFAULTS)",
            inputs={
                "ARGNAMES": InputValue.try_as_type(argnames, p.SRBlockAndTextInputValue),
                "ARGDEFAULTS": InputValue.try_as_type(argdefaults, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def create_function_at(name: InputValue, shadow: InputValue | None = None, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create function at (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(shadow if shadow is not None else utils.all_function_args(), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def create_function_named(name: InputValue, shadow: InputValue | None = None, substack: InputValue | None = None) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create function named (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(shadow if shadow is not None else utils.all_function_args(), p.SREmbeddedBlockInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
        )

    @staticmethod
    def all_function_args() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::function arguments")

    @staticmethod
    def function_arg(name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::function arg (NAME)",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def return_(value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::return (VALUE)",
            inputs={"VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def transfer_function_args_to_temp_vars() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::transfer arguments to temporary variables")

    @staticmethod
    def call_function(func: InputValue, posargs: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::call function (FUNC) with positional args (POSARGS)",
            inputs={
                "FUNC": InputValue.try_as_type(func, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def get_function(name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get function (NAME)",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def function_exists(name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::function (NAME) exists?",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def all_functions() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::all functions")

    @staticmethod
    def delete_function(name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::delete function (NAME)",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def delete_all_functions() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::delete all functions")

    # ---------------------- Misc / Utilities ----------------------
    @staticmethod
    def object_as_string(value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::(VALUE) as string",
            inputs={"VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def typeof(value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::typeof (VALUE)",
            inputs={"VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue)},
        )

    @staticmethod
    def check_identity(v1: InputValue, v2: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::(VALUE1) is (VALUE2) ?",
            inputs={
                "VALUE1": InputValue.try_as_type(v1, p.SRBlockAndTextInputValue),
                "VALUE2": InputValue.try_as_type(v2, p.SRBlockAndTextInputValue),
            },
        )

    @staticmethod
    def nothing() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::Nothing")

    @staticmethod
    def execute_expression(expr: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::execute expression (EXPR)",
            inputs={"EXPR": InputValue.try_as_type(expr, p.SRBlockAndTextInputValue)},
        )
