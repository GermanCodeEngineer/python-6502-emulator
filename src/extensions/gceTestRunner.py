from __future__ import annotations
import pmp_manip as p
from utils import InputValue


class gceTestRunner:

    @staticmethod
    def describe(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::describe (NAME) {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def runTest(name: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::test (NAME) {SUBSTACK}",
            inputs={
                "NAME": InputValue.try_as_type(name, p.SRBlockAndTextInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def assert_(condition: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::assert <CONDITION>",
            inputs={
                "CONDITION": InputValue.try_as_type(
                    condition, p.SRBlockAndBoolInputValue
                )
            },
            dropdowns={},
        )

    @staticmethod
    def assertNot(condition: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::assert not <CONDITION>",
            inputs={
                "CONDITION": InputValue.try_as_type(
                    condition, p.SRBlockAndBoolInputValue
                )
            },
            dropdowns={},
        )

    @staticmethod
    def assertMsg(condition: InputValue, msg: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::assert <CONDITION> message (MSG)",
            inputs={
                "CONDITION": InputValue.try_as_type(
                    condition, p.SRBlockAndBoolInputValue
                ),
                "MSG": InputValue.try_as_type(msg, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def assertEqual(a: InputValue, b: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::assert (A) = (B)",
            inputs={
                "A": InputValue.try_as_type(a, p.SRBlockAndTextInputValue),
                "B": InputValue.try_as_type(b, p.SRBlockAndTextInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def assertThrows(msg: InputValue, substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::assert throws (MSG) {SUBSTACK}",
            inputs={
                "MSG": InputValue.try_as_type(msg, p.SRBlockAndTextInputValue),
                "SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue),
            },
            dropdowns={},
        )

    @staticmethod
    def assertDoesNotThrow(substack: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::assert does not throw {SUBSTACK}",
            inputs={"SUBSTACK": InputValue.try_as_type(substack, p.SRScriptInputValue)},
            dropdowns={},
        )

    @staticmethod
    def fail(msg: InputValue) -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::fail (MSG)",
            inputs={"MSG": InputValue.try_as_type(msg, p.SRBlockAndTextInputValue)},
            dropdowns={},
        )

    @staticmethod
    def reportResults() -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::report results", inputs={}, dropdowns={}
        )

    @staticmethod
    def resetResults() -> p.SRBlock:
        return p.SRBlock(
            opcode="&gceTestRunner::reset results", inputs={}, dropdowns={}
        )

    @staticmethod
    def getPassed() -> p.SRBlock:
        return p.SRBlock(opcode="&gceTestRunner::passed", inputs={}, dropdowns={})

    @staticmethod
    def getFailed() -> p.SRBlock:
        return p.SRBlock(opcode="&gceTestRunner::failed", inputs={}, dropdowns={})
