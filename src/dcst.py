"""
Mostly auto-generated dataclasss wrapper for ast.
"""

from __future__ import annotations; del annotations
from ast import (
    copy_location, fix_missing_locations, iter_fields, iter_child_nodes,
    get_source_segment, walk, compare,
    NodeVisitor, NodeTransformer,
)

# External Imports
import ast as _ast
from _collections_abc import Buffer
from gceutils import grepr_dataclass, field
from os import PathLike
from typing import Any, Literal, overload
from types import EllipsisType

#================================================================================================================#
#                                              AST Wrapped Functions                                             #
#================================================================================================================#

def parse(
        source: str | Buffer,
        filename: str | bytes | PathLike[Any] = "<unknown>",
        mode: str = "exec",
        *,
        type_comments: bool = False,
        feature_version:  int | tuple[int, int] | None = None,
        optimize: Literal[-1, 0, 1, 2] = -1,
    ) -> Module:
    """
    Parse the source into an DCST node.
    Pass type_comments=True to get back type comments where the syntax allows.
    """
    ast_tree = _ast.parse(
        source, filename, mode,
        type_comments=type_comments, feature_version=feature_version, optimize=optimize
    )
    return DCST.from_ast_tree(ast_tree)

def literal_eval(node_or_string: str | DCST) -> Any:
    """
    Evaluate an expression node or a string containing only a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, bytes, numbers, tuples, lists, dicts,
    sets, booleans, and None.

    Caution: A complex expression can overflow the C stack and cause a crash.
    """
    if isinstance(node_or_string, DCST):
        node_or_string = node_or_string.to_ast_tree()
    return _ast.literal_eval(node_or_string)

copy_location # copy_location is reused
fix_missing_locations # fix_missing_locations is reused
iter_fields # iter_fields is reused
iter_child_nodes # iter_child_nodes is reused

def get_docstring(node: AsyncFunctionDef | FunctionDef | ClassDef | Module, clean: bool = True):
    """
    Return the docstring for the given node or None if no docstring can
    be found.  If the node provided does not have docstrings a TypeError
    will be raised.

    If *clean* is `True`, all tabs are expanded to spaces and any whitespace
    that can be uniformly removed from the second line onwards is removed.
    """
    return _ast.get_docstring(node.to_ast_tree(), clean=clean)

get_source_segment # get_source_segment is reused
walk # walk is reused
compare # compare is reused
NodeVisitor # NodeVisitor is reused
NodeTransformer # NodeTransformer is reused

def unparse(ast_obj: DCST) -> str:
    return _ast.unparse(ast_obj.to_ast_tree())

#================================================================================================================#
#                                                AST Node Classes                                                #
#================================================================================================================#

class _DCSTMeta(type):
    @property # To allow _ast.iter_fields to work on DCST classes
    def _fields(cls) -> tuple[str, ...]:
        from dataclasses import fields as get_fields
        return tuple(field.name for field in get_fields(cls))


@grepr_dataclass()
class DCST(_ast.AST, metaclass=_DCSTMeta):
    @property # To allow _ast.iter_fields to work on DCST nodes
    def _fields(self) -> tuple[str, ...]:
        return type(self)._fields

    @overload
    @staticmethod
    def from_ast_tree[T: DCST](ast_tree: T) -> T: ...

    @overload
    @staticmethod
    def from_ast_tree(ast_tree: _ast.AST) -> DCST: ...

    @overload
    @staticmethod
    def from_ast_tree[T](ast_tree: T) -> T: ...

    @overload
    @staticmethod
    def from_ast_tree[T: DCST](ast_tree: list[T]) -> list[T]: ...

    @overload
    @staticmethod
    def from_ast_tree(ast_tree: list[_ast.AST]) -> list[DCST]: ...

    @overload
    @staticmethod
    def from_ast_tree[T](ast_tree: list[T]) -> list[T]: ...

    @overload
    @staticmethod
    def from_ast_tree[T](ast_tree: list[_ast.AST | T]) -> list[DCST | T]: ...

    @staticmethod
    def from_ast_tree[T](ast_tree: DCST | _ast.AST | T | list[DCST | _ast.AST | T]) -> DCST | T | list[DCST | T]:
        if isinstance(ast_tree, DCST):
            return ast_tree

        elif isinstance(ast_tree, _ast.AST):
            dcst_class: type[DCST] = globals()[type(ast_tree).__name__]
            kwargs = {}
            for field_name, value in iter_fields(ast_tree):
                if isinstance(value, _ast.AST):
                    value = DCST.from_ast_tree(value)
                elif isinstance(value, list):
                    value = [DCST.from_ast_tree(item) if isinstance(item, _ast.AST) else item for item in value]
                kwargs[field_name] = value

            for field_name in ["lineno", "col_offset", "end_lineno", "end_col_offset"]:
                if field_name not in dcst_class._fields:
                    continue
                if field_name in kwargs:
                    continue
                if hasattr(ast_tree, field_name):
                    kwargs[field_name] = getattr(ast_tree, field_name)

            return dcst_class(**kwargs)

        elif isinstance(ast_tree, list):
            return [DCST.from_ast_tree(item) for item in ast_tree]

        else:
            return ast_tree

    def to_ast_tree(self) -> _ast.AST:
        ast_class: type[_ast.AST] = getattr(_ast, type(self).__name__)
        kwargs = {}
        for field_name, value in iter_fields(self):
            if isinstance(value, DCST):
                value = value.to_ast_tree()
            elif isinstance(value, list):
                value = [item.to_ast_tree() if isinstance(item, DCST) else item for item in value]
            kwargs[field_name] = value

        return ast_class(**kwargs)


@grepr_dataclass()
class alias(DCST):
    name: str
    asname: str | None
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass()
class arg(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)
    arg: str
    annotation: expr | None
    type_comment: str | None

@grepr_dataclass()
class arguments(DCST):
    posonlyargs: list[arg]
    args: list[arg]
    vararg: arg | None
    kwonlyargs: list[arg]
    kw_defaults: list[expr | None]
    kwarg: arg | None
    defaults: list[expr]

@grepr_dataclass()
class boolop(DCST):
    pass

@grepr_dataclass()
class cmpop(DCST):
    pass

@grepr_dataclass()
class comprehension(DCST):
    target: expr
    iter: expr
    ifs: list[expr]
    is_async: int

@grepr_dataclass()
class excepthandler(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass()
class expr(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass()
class expr_context(DCST):
    pass

@grepr_dataclass()
class keyword(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)
    arg: str | None
    value: expr

@grepr_dataclass()
class match_case(DCST):
    pattern: pattern
    guard: expr | None
    body: list[stmt]

@grepr_dataclass()
class mod(DCST):
    pass

@grepr_dataclass()
class operator(DCST):
    pass

@grepr_dataclass()
class pattern(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass()
class stmt(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass()
class type_ignore(DCST):
    pass

@grepr_dataclass()
class type_param(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass()
class unaryop(DCST):
    pass

@grepr_dataclass()
class withitem(DCST):
    context_expr: expr
    optional_vars: expr | None

@grepr_dataclass()
class Add(operator):
    pass

@grepr_dataclass()
class And(boolop):
    pass

@grepr_dataclass()
class AnnAssign(stmt):
    target: Name | Attribute | Subscript
    annotation: expr
    value: expr | None
    simple: int

@grepr_dataclass()
class Assert(stmt):
    test: expr
    msg: expr | None

@grepr_dataclass()
class Assign(stmt):
    targets: list[expr]
    value: expr
    type_comment: str | None

@grepr_dataclass()
class AsyncFor(stmt):
    target: expr
    iter: expr
    body: list[stmt]
    orelse: list[stmt]
    type_comment: str | None

@grepr_dataclass()
class AsyncFunctionDef(stmt):
    name: str
    args: arguments
    body: list[stmt]
    decorator_list: list[expr]
    returns: expr | None
    type_comment: str | None
    type_params: list[type_param]

@grepr_dataclass()
class AsyncWith(stmt):
    items: list[withitem]
    body: list[stmt]
    type_comment: str | None

@grepr_dataclass()
class Attribute(expr):
    value: expr
    attr: str
    ctx: expr_context

@grepr_dataclass()
class AugAssign(stmt):
    target: Name | Attribute | Subscript
    op: operator
    value: expr

@grepr_dataclass()
class Await(expr):
    value: expr

@grepr_dataclass()
class BinOp(expr):
    left: expr
    op: operator
    right: expr

@grepr_dataclass()
class BitAnd(operator):
    pass

@grepr_dataclass()
class BitOr(operator):
    pass

@grepr_dataclass()
class BitXor(operator):
    pass

@grepr_dataclass()
class BoolOp(expr):
    op: boolop
    values: list[expr]

@grepr_dataclass()
class Break(stmt):
    pass

@grepr_dataclass()
class Call(expr):
    func: expr
    args: list[expr]
    keywords: list[keyword]

@grepr_dataclass()
class ClassDef(stmt):
    name: str
    bases: list[expr]
    keywords: list[keyword]
    body: list[stmt]
    decorator_list: list[expr]
    type_params: list[type_param]

@grepr_dataclass()
class Compare(expr):
    left: expr
    ops: list[cmpop]
    comparators: list[expr]

@grepr_dataclass()
class Constant(expr):
    value: str | bytes | bool | int | float | complex | None | EllipsisType
    kind: str | None

@grepr_dataclass()
class Continue(stmt):
    pass

@grepr_dataclass()
class Del(expr_context):
    pass

@grepr_dataclass()
class Delete(stmt):
    targets: list[expr]

@grepr_dataclass()
class Dict(expr):
    keys: list[expr | None]
    values: list[expr]

@grepr_dataclass()
class DictComp(expr):
    key: expr
    value: expr
    generators: list[comprehension]

@grepr_dataclass()
class Div(operator):
    pass

@grepr_dataclass()
class Eq(cmpop):
    pass

@grepr_dataclass()
class ExceptHandler(excepthandler):
    type: expr | None
    name: str | None
    body: list[stmt]

@grepr_dataclass()
class Expr(stmt):
    value: expr

@grepr_dataclass()
class Expression(mod):
    body: expr

@grepr_dataclass()
class FloorDiv(operator):
    pass

@grepr_dataclass()
class For(stmt):
    target: expr
    iter: expr
    body: list[stmt]
    orelse: list[stmt]
    type_comment: str | None

@grepr_dataclass()
class FormattedValue(expr):
    value: expr
    conversion: int
    format_spec: expr | None

@grepr_dataclass()
class FunctionDef(stmt):
    name: str
    args: arguments
    body: list[stmt]
    decorator_list: list[expr]
    returns: expr | None
    type_comment: str | None
    type_params: list[type_param]

@grepr_dataclass()
class FunctionType(mod):
    argtypes: list[expr]
    returns: expr

@grepr_dataclass()
class GeneratorExp(expr):
    elt: expr
    generators: list[comprehension]

@grepr_dataclass()
class Global(stmt):
    names: list[str]

@grepr_dataclass()
class Gt(cmpop):
    pass

@grepr_dataclass()
class GtE(cmpop):
    pass

@grepr_dataclass()
class If(stmt):
    test: expr
    body: list[stmt]
    orelse: list[stmt]

@grepr_dataclass()
class IfExp(expr):
    test: expr
    body: expr
    orelse: expr

@grepr_dataclass()
class Import(stmt):
    names: list[alias]

@grepr_dataclass()
class ImportFrom(stmt):
    module: str | None
    names: list[alias]
    level: int

@grepr_dataclass()
class In(cmpop):
    pass

@grepr_dataclass()
class Interactive(mod):
    body: list[stmt]

@grepr_dataclass()
class Invert(unaryop):
    pass

@grepr_dataclass()
class Is(cmpop):
    pass

@grepr_dataclass()
class IsNot(cmpop):
    pass

@grepr_dataclass()
class JoinedStr(expr):
    values: list[expr]

@grepr_dataclass()
class LShift(operator):
    pass

@grepr_dataclass()
class Lambda(expr):
    args: arguments
    body: expr

@grepr_dataclass()
class List(expr):
    elts: list[expr]
    ctx: expr_context

@grepr_dataclass()
class ListComp(expr):
    elt: expr
    generators: list[comprehension]

@grepr_dataclass()
class Load(expr_context):
    pass

@grepr_dataclass()
class Lt(cmpop):
    pass

@grepr_dataclass()
class LtE(cmpop):
    pass

@grepr_dataclass()
class MatMult(operator):
    pass

@grepr_dataclass()
class Match(stmt):
    subject: expr
    cases: list[match_case]

@grepr_dataclass()
class MatchAs(pattern):
    pattern: pattern | None
    name: str | None

@grepr_dataclass()
class MatchClass(pattern):
    cls: expr
    patterns: list[pattern]
    kwd_attrs: list[str]
    kwd_patterns: list[pattern]

@grepr_dataclass()
class MatchMapping(pattern):
    keys: list[expr]
    patterns: list[pattern]
    rest: str | None

@grepr_dataclass()
class MatchOr(pattern):
    patterns: list[pattern]

@grepr_dataclass()
class MatchSequence(pattern):
    patterns: list[pattern]

@grepr_dataclass()
class MatchSingleton(pattern):
    value: bool | None

@grepr_dataclass()
class MatchStar(pattern):
    name: str | None

@grepr_dataclass()
class MatchValue(pattern):
    value: expr

@grepr_dataclass()
class Mod(operator):
    pass

@grepr_dataclass()
class Module(mod):
    body: list[stmt]
    type_ignores: list[TypeIgnore]

@grepr_dataclass()
class Mult(operator):
    pass

@grepr_dataclass()
class Name(expr):
    id: str
    ctx: expr_context

@grepr_dataclass()
class NamedExpr(expr):
    target: Name
    value: expr

@grepr_dataclass()
class Nonlocal(stmt):
    names: list[str]

@grepr_dataclass()
class Not(unaryop):
    pass

@grepr_dataclass()
class NotEq(cmpop):
    pass

@grepr_dataclass()
class NotIn(cmpop):
    pass

@grepr_dataclass()
class Or(boolop):
    pass

@grepr_dataclass()
class ParamSpec(type_param):
    name: str
    default_value: expr | None

@grepr_dataclass()
class Pass(stmt):
    pass

@grepr_dataclass()
class Pow(operator):
    pass

@grepr_dataclass()
class RShift(operator):
    pass

@grepr_dataclass()
class Raise(stmt):
    exc: expr | None
    cause: expr | None

@grepr_dataclass()
class Return(stmt):
    value: expr | None

@grepr_dataclass()
class Set(expr):
    elts: list[expr]

@grepr_dataclass()
class SetComp(expr):
    elt: expr
    generators: list[comprehension]

@grepr_dataclass()
class Slice(expr):
    lower: expr | None
    upper: expr | None
    step: expr | None

@grepr_dataclass()
class Starred(expr):
    value: expr
    ctx: expr_context

@grepr_dataclass()
class Store(expr_context):
    pass

@grepr_dataclass()
class Sub(operator):
    pass

@grepr_dataclass()
class Subscript(expr):
    value: expr
    slice: expr
    ctx: expr_context

@grepr_dataclass()
class Try(stmt):
    body: list[stmt]
    handlers: list[ExceptHandler]
    orelse: list[stmt]
    finalbody: list[stmt]

@grepr_dataclass()
class Tuple(expr):
    elts: list[expr]
    ctx: expr_context
    dims: list[expr]

@grepr_dataclass()
class TypeAlias(stmt):
    name: Name
    type_params: list[type_param]
    value: expr

@grepr_dataclass()
class TypeIgnore(type_ignore):
    lineno: int | None = field(grepr=False)
    tag: str

@grepr_dataclass()
class TypeVar(type_param):
    name: str
    bound: expr | None
    default_value: expr | None

@grepr_dataclass()
class TypeVarTuple(type_param):
    name: str
    default_value: expr | None

@grepr_dataclass()
class UAdd(unaryop):
    pass

@grepr_dataclass()
class USub(unaryop):
    pass

@grepr_dataclass()
class UnaryOp(expr):
    op: unaryop
    operand: expr

@grepr_dataclass()
class While(stmt):
    test: expr
    body: list[stmt]
    orelse: list[stmt]

@grepr_dataclass()
class With(stmt):
    items: list[withitem]
    body: list[stmt]
    type_comment: str | None

@grepr_dataclass()
class Yield(expr):
    value: expr | None

@grepr_dataclass()
class YieldFrom(expr):
    value: expr

# Create a proper __all__
__all__ = list(globals().keys())
for name in __all__.copy():
    obj = globals()[name]
    try:
        if (obj.__module__ not in (DCST.__module__, "ast")) or name.startswith("_"):
            __all__.remove(name)
    except AttributeError:
        __all__.remove(name)

# Make a list of DCST clsasses
DCST_CLASSES: list[type[DCST]] = [globals()[name] for name in __all__ if isinstance(globals()[name], type) and issubclass(globals()[name], DCST)]
