from __future__ import annotations
import pmp_manip as p
from utils import InputValue


class gceClassesOOP:

    @staticmethod
    def logStacks() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::logStacks", inputs={}, dropdowns={})

    @staticmethod
    def setScopeVar(name: InputValue, value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::set var (NAME) to (VALUE) in current scope",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def getScopeVar(name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get var (NAME)",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
            dropdowns={},
        )

    @staticmethod
    def scopeVarExists(name: InputValue, kind: str) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::var (NAME) exists in [KIND]?",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
            dropdowns={"KIND": p.SRDropdownValue(p.DropdownValueKind.STANDARD, kind)},
        )

    @staticmethod
    def deleteScopeVar(name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::delete var (NAME) in current scope",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
            dropdowns={},
        )

    @staticmethod
    def allVariables(kind: str) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::all variables in [KIND]",
            inputs={},
            dropdowns={"KIND": p.SRDropdownValue(p.DropdownValueKind.STANDARD, kind)},
        )

    @staticmethod
    def createVarScope(substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create local variable scope {SUBSTACK}",
            inputs={"SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue)},
            dropdowns={},
        )

    @staticmethod
    def bindVarToScope(name: InputValue, kind: str) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::bind [KIND] variable (NAME) to current scope",
            inputs={"NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue)},
            dropdowns={"KIND": p.SRDropdownValue(p.DropdownValueKind.STANDARD, kind)},
        )

    @staticmethod
    def createClassAt(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create class at var (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(
                    InputValue(gceClassesOOP.classBeingCreated()),
                    p.SREmbeddedBlockInputValue,
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def createSubclassAt(
        name: InputValue, superclass: InputValue, substack: InputValue
    ) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create subclass at var (NAME) with superclass (SUPERCLASS) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SUPERCLASS": InputValue.try_as_type(
                    superclass, p.SRBlockAndTextInputValue
                ),
                "SHADOW": InputValue.try_as_type(
                    InputValue(gceClassesOOP.classBeingCreated()),
                    p.SREmbeddedBlockInputValue,
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def createClassNamed(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create class named (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(
                    InputValue(gceClassesOOP.classBeingCreated()),
                    p.SREmbeddedBlockInputValue,
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def createSubclassNamed(
        name: InputValue, superclass: InputValue, substack: InputValue
    ) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create subclass named (NAME) with superclass (SUPERCLASS) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SUPERCLASS": InputValue.try_as_type(
                    superclass, p.SRBlockAndTextInputValue
                ),
                "SHADOW": InputValue.try_as_type(
                    InputValue(gceClassesOOP.classBeingCreated()),
                    p.SREmbeddedBlockInputValue,
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def onClass(class_: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on class (CLASS) {:SHADOW:} {SUBSTACK}",
            inputs={
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(
                    InputValue(gceClassesOOP.classBeingCreated()),
                    p.SREmbeddedBlockInputValue,
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def classBeingCreated() -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::class being created", inputs={}, dropdowns={}
        )

    @staticmethod
    def isSubclass(subclass: InputValue, superclass: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::is (SUBCLASS) a subclass of (SUPERCLASS) ?",
            inputs={
                "SUBCLASS": InputValue.try_as_type(
                    subclass, p.SRBlockAndTextInputValue
                ),
                "SUPERCLASS": InputValue.try_as_type(
                    superclass, p.SRBlockAndTextInputValue
                ),
            },
            dropdowns={},
        )

    @staticmethod
    def getSuperclass(class_: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get superclass of (CLASS)",
            inputs={
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue)
            },
            dropdowns={},
        )

    @staticmethod
    def defineInstanceMethod(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define instance method (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(
                    InputValue(gceClassesOOP.self()), p.SREmbeddedBlockInputValue
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def defineSpecialMethod(substack: InputValue, special_method: str) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define [SPECIAL_METHOD] instance method {:SHADOW:} {SUBSTACK}",
            inputs={
                "SHADOW": InputValue.try_as_type(
                    InputValue(gceClassesOOP.self()), p.SREmbeddedBlockInputValue
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={
                "SPECIAL_METHOD": p.SRDropdownValue(
                    p.DropdownValueKind.STANDARD, special_method
                )
            },
        )

    @staticmethod
    def self() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::self", inputs={}, dropdowns={})

    @staticmethod
    def callSuperMethod(name: InputValue, posargs: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::call super method (NAME) with positional args (POSARGS)",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def callSuperInitMethod(posargs: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::call super init method with positional args (POSARGS)",
            inputs={
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue)
            },
            dropdowns={},
        )

    @staticmethod
    def defineGetter(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define getter (NAME) {:SHADOW:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW": InputValue.try_as_type(
                    InputValue(gceClassesOOP.self()), p.SREmbeddedBlockInputValue
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def defineSetter(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define setter (NAME) {:SHADOW1:} {:SHADOW2:} {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SHADOW1": InputValue.try_as_type(
                    InputValue(gceClassesOOP.self()), p.SREmbeddedBlockInputValue
                ),
                "SHADOW2": InputValue.try_as_type(
                    InputValue(gceClassesOOP.defineSetterValue()),
                    p.SREmbeddedBlockInputValue,
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def defineSetterValue() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::value", inputs={}, dropdowns={})

    @staticmethod
    def defineOperatorMethod(substack: InputValue, operator_kind: str) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define operator method [OPERATOR_KIND] {:SHADOW:} {SUBSTACK}",
            inputs={
                "SHADOW": InputValue.try_as_type(
                    InputValue(gceClassesOOP.operatorOtherValue()),
                    p.SREmbeddedBlockInputValue,
                ),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={
                "OPERATOR_KIND": p.SRDropdownValue(
                    p.DropdownValueKind.STANDARD, operator_kind
                )
            },
        )

    @staticmethod
    def operatorOtherValue() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::other value", inputs={}, dropdowns={})

    @staticmethod
    def setClassVariable(
        class_: InputValue, name: InputValue, value: InputValue
    ) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (CLASS) set class variable (NAME) to (VALUE)",
            inputs={
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def getClassVariable(name: InputValue, class_: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get class variable (NAME) of (CLASS)",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def deleteClassVariable(class_: InputValue, name: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (CLASS) delete class variable (NAME)",
            inputs={
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def defineStaticMethod(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::define static method (NAME) {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def propertyNamesOfClass(class_: InputValue, property: str) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::[PROPERTY] names of class (CLASS)",
            inputs={
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue)
            },
            dropdowns={
                "PROPERTY": p.SRDropdownValue(p.DropdownValueKind.STANDARD, property)
            },
        )

    @staticmethod
    def createInstance(class_: InputValue, posargs: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create instance of class (CLASS) with positional args (POSARGS)",
            inputs={
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def isInstance(instance: InputValue, class_: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::is (INSTANCE) an instance of (CLASS) ?",
            inputs={
                "INSTANCE": InputValue.try_as_type(
                    instance, p.SRBlockAndTextInputValue
                ),
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def getClassOfInstance(instance: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get class of (INSTANCE)",
            inputs={
                "INSTANCE": InputValue.try_as_type(instance, p.SRBlockAndTextInputValue)
            },
            dropdowns={},
        )

    @staticmethod
    def setAttribute(
        instance: InputValue, name: InputValue, value: InputValue
    ) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (INSTANCE) set attribute (NAME) to (VALUE)",
            inputs={
                "INSTANCE": InputValue.try_as_type(
                    instance, p.SRBlockAndTextInputValue
                ),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def getAttribute(name: InputValue, instance: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::attribute (NAME) of (INSTANCE)",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "INSTANCE": InputValue.try_as_type(
                    instance, p.SRBlockAndTextInputValue
                ),
            },
            dropdowns={},
        )

    @staticmethod
    def getAllAttributes(instance: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::all attributes of (INSTANCE)",
            inputs={
                "INSTANCE": InputValue.try_as_type(instance, p.SRBlockAndTextInputValue)
            },
            dropdowns={},
        )

    @staticmethod
    def callMethod(
        instance: InputValue, name: InputValue, posargs: InputValue
    ) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (INSTANCE) call method (NAME) with positional args (POSARGS)",
            inputs={
                "INSTANCE": InputValue.try_as_type(
                    instance, p.SRBlockAndTextInputValue
                ),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def callStaticMethod(
        class_: InputValue, name: InputValue, posargs: InputValue
    ) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::on (CLASS) call static method (NAME) with positional args (POSARGS)",
            inputs={
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue),
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def getStaticMethodFunc(name: InputValue, class_: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::get static method (NAME) of (CLASS) as function",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "CLASS": InputValue.try_as_type(class_, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def configureNextFunctionArgs(
        argnames: InputValue, argdefaults: InputValue
    ) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::configure next function: argument names (ARGNAMES) defaults (ARGDEFAULTS)",
            inputs={
                "ARGNAMES": InputValue.try_as_type(
                    argnames, p.SRBlockAndTextInputValue
                ),
                "ARGDEFAULTS": InputValue.try_as_type(
                    argdefaults, p.SRBlockAndTextInputValue
                ),
            },
            dropdowns={},
        )

    @staticmethod
    def createFunctionAt(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create function at var (NAME) {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def createFunctionNamed(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::create function named (NAME) {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def return_(value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::return (VALUE)",
            inputs={"VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue)},
            dropdowns={},
        )

    @staticmethod
    def callFunction(func: InputValue, posargs: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::call function (FUNC) with positional args (POSARGS)",
            inputs={
                "FUNC": InputValue.try_as_type(func, p.SRBlockAndTextInputValue),
                "POSARGS": InputValue.try_as_type(posargs, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def objectAsString(value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::(VALUE) as string",
            inputs={"VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue)},
            dropdowns={},
        )

    @staticmethod
    def typeof(value: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::typeof (VALUE)",
            inputs={"VALUE": InputValue.try_as_type(value, p.SRBlockAndTextInputValue)},
            dropdowns={},
        )

    @staticmethod
    def checkIdentity(value1: InputValue, value2: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::(VALUE1) is (VALUE2) ?",
            inputs={
                "VALUE1": InputValue.try_as_type(value1, p.SRBlockAndTextInputValue),
                "VALUE2": InputValue.try_as_type(value2, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def nothing() -> p.SRBlock:
        return p.SRBlock(opcode="&gceClassesOOP::Nothing", inputs={}, dropdowns={})

    @staticmethod
    def executeExpression(expr: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::execute expression (EXPR)",
            inputs={"EXPR": InputValue.try_as_type(expr, p.SRBlockAndTextInputValue)},
            dropdowns={},
        )

    @staticmethod
    def menu() -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::#menu:variableAvailableKind",
            inputs={},
            dropdowns={},
        )

    @staticmethod
    def menu() -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::#menu:bindVarOriginKind", inputs={}, dropdowns={}
        )

    @staticmethod
    def menu() -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::#menu:classProperty", inputs={}, dropdowns={}
        )

    @staticmethod
    def menu() -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::#menu:operatorMethod", inputs={}, dropdowns={}
        )

    @staticmethod
    def menu() -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceClassesOOP::#menu:specialMethod", inputs={}, dropdowns={}
        )
