"""
Mostly auto-generated dataclasss wrapper for ast.
"""

from __future__ import annotations; del annotations
from ast import (
    copy_location, fix_missing_locations, iter_fields, iter_child_nodes,
    get_source_segment, walk, compare,
)

# External Imports
import ast as _ast
from _collections_abc import Buffer
from gceutils import grepr_dataclass, field, AbstractTreePath
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

# Added onto ast: get_code_reference_fields
def get_code_reference_fields(node: DCST) -> dict[str, int]:
    """Return a dict containing the fields of the node that are used for code references."""
    d = {}
    for attribute in ["lineno", "col_offset", "end_lineno", "end_col_offset"]:
        if hasattr(node, attribute):
            d[attribute] = getattr(node, attribute)
    return d

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

@grepr_dataclass()
class NodeVisitor(object):
    """
    A node visitor base class that walks the dataclass syntax tree and calls a
    visitor function for every node found.  This function may return a value
    which is forwarded by the `visit` method.

    This class is meant to be subclassed, with the subclass adding visitor
    methods.

    Per default the visitor functions for the nodes are ``'visit_'`` +
    class name of the node.  So a `TryFinally` node visit function would
    be `visit_TryFinally`.  This behavior can be changed by overriding
    the `visit` method.  If no visitor function exists for a node
    (return value `None`) the `generic_visit` visitor is used instead.

    Don't use the `NodeVisitor` if you want to apply changes to nodes during
    traversing.  For this a special visitor exists (`NodeTransformer`) that
    allows modifications.
    """
    root_node: DCST | None = field(default=None, init=False)

    def set_root_and_visit(self, node: DCST) -> DCST | Any:
        self.root_node = node
        return self.visit(node, AbstractTreePath())

    def visit(self, node: DCST | Any, path_to_node: AbstractTreePath = AbstractTreePath()) -> DCST | Any:
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, path_to_node)

    def generic_visit(self, node: DCST | Any, path_to_node: AbstractTreePath) -> None:
        """Called if no explicit visitor function exists for a node."""
        for field, value in iter_fields(node):
            attribute_path = path_to_node.add_attribute(field)
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, DCST):
                        self.visit(item, attribute_path.add_index_or_key(i))
            elif isinstance(value, DCST):
                self.visit(value, attribute_path)

    def get_path(self, path_to_node: AbstractTreePath) -> DCST | Any:
        if self.root_node is None:
            raise ValueError("Root node is not set. Call set_root_and_visit first.")
        return path_to_node.get_in_tree(self.root_node)

@grepr_dataclass()
class NodeTransformer(NodeVisitor):
    """
    A :class:`NodeVisitor` subclass that walks the abstract syntax tree and
    allows modification of nodes.

    The `NodeTransformer` will walk the DCST and use the return value of the
    visitor methods to replace or remove the old node.  If the return value of
    the visitor method is ``None``, the node will be removed from its location,
    otherwise it is replaced with the return value.  The return value may be the
    original node in which case no replacement takes place.

    Here is an example transformer that rewrites all occurrences of name lookups
    (``foo``) to ``data['foo']``::

       class RewriteName(NodeTransformer):

           def visit_Name(self, node):
               return Subscript(
                   value=Name(id='data', ctx=Load()),
                   slice=Constant(value=node.id),
                   ctx=node.ctx
               )

    Keep in mind that if the node you're operating on has child nodes you must
    either transform the child nodes yourself or call the :meth:`generic_visit`
    method for the node first.

    For nodes that were part of a collection of statements (that applies to all
    statement nodes), the visitor may also return a list of nodes rather than
    just a single node.

    Usually you use the transformer like this::

       node = YourTransformer().visit(node, AbstractTreePath())
    """

    def generic_visit(self, node: DCST, path_to_node: AbstractTreePath = AbstractTreePath()) -> DCST | Any:
        for field, old_value in iter_fields(node):
            attribute_path = path_to_node.add_attribute(field)
            if isinstance(old_value, list):
                new_values = []
                for i, value in enumerate(old_value):
                    if isinstance(value, DCST):
                        value = self.visit(value, attribute_path.add_index_or_key(i))
                        if value is None:
                            pass
                        elif isinstance(value, list):
                            new_values.extend(value)
                        else:
                            new_values.append(value)
                    else:
                        new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, DCST):
                new_node = self.visit(old_value, attribute_path)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node

    def set_path(self, path_to_node: AbstractTreePath, value: DCST | Any) -> None:
        if self.root_node is None:
            raise ValueError("Root node is not set. Call set_root_and_visit first.")
        path_to_node.set_in_tree(self.root_node, value)

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


@grepr_dataclass(init=False)
class DCST(_ast.AST, metaclass=_DCSTMeta):
    def __init__(self, **kwargs):
        STUPID_FIELDS = {
            "lineno": 0,
            "col_offset": 0,
            "end_lineno": 0,
            "end_col_offset": 0,
        }

        for field_name, default_value in STUPID_FIELDS.items():
            if field_name not in type(self)._fields:
                continue
            if field_name in kwargs:
                continue
            kwargs[field_name] = default_value

        for key, value in kwargs.items():
            setattr(self, key, value)

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
                if isinstance(value, _ast.Tuple) and (field_name == "dims"):
                    continue # I removed the deprecated dims field
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


@grepr_dataclass(init=False)
class alias(DCST):
    name: str
    asname: str | None
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass(init=False)
class arg(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)
    arg: str
    annotation: expr | None
    type_comment: str | None

@grepr_dataclass(init=False)
class arguments(DCST):
    posonlyargs: list[arg]
    args: list[arg]
    vararg: arg | None
    kwonlyargs: list[arg]
    kw_defaults: list[expr | None]
    kwarg: arg | None
    defaults: list[expr]

@grepr_dataclass(init=False)
class boolop(DCST):
    pass

@grepr_dataclass(init=False)
class cmpop(DCST):
    pass

@grepr_dataclass(init=False)
class comprehension(DCST):
    target: expr
    iter: expr
    ifs: list[expr]
    is_async: int

@grepr_dataclass(init=False)
class excepthandler(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass(init=False)
class expr(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass(init=False)
class expr_context(DCST):
    pass

@grepr_dataclass(init=False)
class keyword(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)
    arg: str | None
    value: expr

@grepr_dataclass(init=False)
class match_case(DCST):
    pattern: pattern
    guard: expr | None
    body: list[stmt]

@grepr_dataclass(init=False)
class mod(DCST):
    pass

@grepr_dataclass(init=False)
class operator(DCST):
    pass

@grepr_dataclass(init=False)
class pattern(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass(init=False)
class stmt(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass(init=False)
class type_ignore(DCST):
    pass

@grepr_dataclass(init=False)
class type_param(DCST):
    lineno: int | None = field(grepr=False)
    col_offset: int | None = field(grepr=False)
    end_lineno: int | None = field(grepr=False)
    end_col_offset: int | None = field(grepr=False)

@grepr_dataclass(init=False)
class unaryop(DCST):
    pass

@grepr_dataclass(init=False)
class withitem(DCST):
    context_expr: expr
    optional_vars: expr | None

@grepr_dataclass(init=False)
class Add(operator):
    pass

@grepr_dataclass(init=False)
class And(boolop):
    pass

@grepr_dataclass(init=False)
class AnnAssign(stmt):
    target: Name | Attribute | Subscript
    annotation: expr
    value: expr | None
    simple: int

@grepr_dataclass(init=False)
class Assert(stmt):
    test: expr
    msg: expr | None

@grepr_dataclass(init=False)
class Assign(stmt):
    targets: list[expr]
    value: expr
    type_comment: str | None

@grepr_dataclass(init=False)
class AsyncFor(stmt):
    target: expr
    iter: expr
    body: list[stmt]
    orelse: list[stmt]
    type_comment: str | None

@grepr_dataclass(init=False)
class AsyncFunctionDef(stmt):
    name: str
    args: arguments
    body: list[stmt]
    decorator_list: list[expr]
    returns: expr | None
    type_comment: str | None
    type_params: list[type_param]

@grepr_dataclass(init=False)
class AsyncWith(stmt):
    items: list[withitem]
    body: list[stmt]
    type_comment: str | None

@grepr_dataclass(init=False)
class Attribute(expr):
    value: expr
    attr: str
    ctx: expr_context

@grepr_dataclass(init=False)
class AugAssign(stmt):
    target: Name | Attribute | Subscript
    op: operator
    value: expr

@grepr_dataclass(init=False)
class Await(expr):
    value: expr

@grepr_dataclass(init=False)
class BinOp(expr):
    left: expr
    op: operator
    right: expr

@grepr_dataclass(init=False)
class BitAnd(operator):
    pass

@grepr_dataclass(init=False)
class BitOr(operator):
    pass

@grepr_dataclass(init=False)
class BitXor(operator):
    pass

@grepr_dataclass(init=False)
class BoolOp(expr):
    op: boolop
    values: list[expr]

@grepr_dataclass(init=False)
class Break(stmt):
    pass

@grepr_dataclass(init=False)
class Call(expr):
    func: expr
    args: list[expr]
    keywords: list[keyword]

@grepr_dataclass(init=False)
class ClassDef(stmt):
    name: str
    bases: list[expr]
    keywords: list[keyword]
    body: list[stmt]
    decorator_list: list[expr]
    type_params: list[type_param]

@grepr_dataclass(init=False)
class Compare(expr):
    left: expr
    ops: list[cmpop]
    comparators: list[expr]

@grepr_dataclass(init=False)
class Constant(expr):
    value: str | bytes | bool | int | float | complex | None | EllipsisType
    kind: str | None

@grepr_dataclass(init=False)
class Continue(stmt):
    pass

@grepr_dataclass(init=False)
class Del(expr_context):
    pass

@grepr_dataclass(init=False)
class Delete(stmt):
    targets: list[expr]

@grepr_dataclass(init=False)
class Dict(expr):
    keys: list[expr | None]
    values: list[expr]

@grepr_dataclass(init=False)
class DictComp(expr):
    key: expr
    value: expr
    generators: list[comprehension]

@grepr_dataclass(init=False)
class Div(operator):
    pass

@grepr_dataclass(init=False)
class Eq(cmpop):
    pass

@grepr_dataclass(init=False)
class ExceptHandler(excepthandler):
    type: expr | None
    name: str | None
    body: list[stmt]

@grepr_dataclass(init=False)
class Expr(stmt):
    value: expr

@grepr_dataclass(init=False)
class Expression(mod):
    body: expr

@grepr_dataclass(init=False)
class FloorDiv(operator):
    pass

@grepr_dataclass(init=False)
class For(stmt):
    target: expr
    iter: expr
    body: list[stmt]
    orelse: list[stmt]
    type_comment: str | None

@grepr_dataclass(init=False)
class FormattedValue(expr):
    value: expr
    conversion: int
    format_spec: expr | None

@grepr_dataclass(init=False)
class FunctionDef(stmt):
    name: str
    args: arguments
    body: list[stmt]
    decorator_list: list[expr]
    returns: expr | None
    type_comment: str | None
    type_params: list[type_param]

@grepr_dataclass(init=False)
class FunctionType(mod):
    argtypes: list[expr]
    returns: expr

@grepr_dataclass(init=False)
class GeneratorExp(expr):
    elt: expr
    generators: list[comprehension]

@grepr_dataclass(init=False)
class Global(stmt):
    names: list[str]

@grepr_dataclass(init=False)
class Gt(cmpop):
    pass

@grepr_dataclass(init=False)
class GtE(cmpop):
    pass

@grepr_dataclass(init=False)
class If(stmt):
    test: expr
    body: list[stmt]
    orelse: list[stmt]

@grepr_dataclass(init=False)
class IfExp(expr):
    test: expr
    body: expr
    orelse: expr

@grepr_dataclass(init=False)
class Import(stmt):
    names: list[alias]

@grepr_dataclass(init=False)
class ImportFrom(stmt):
    module: str | None
    names: list[alias]
    level: int

@grepr_dataclass(init=False)
class In(cmpop):
    pass

@grepr_dataclass(init=False)
class Interactive(mod):
    body: list[stmt]

@grepr_dataclass(init=False)
class Invert(unaryop):
    pass

@grepr_dataclass(init=False)
class Is(cmpop):
    pass

@grepr_dataclass(init=False)
class IsNot(cmpop):
    pass

@grepr_dataclass(init=False)
class JoinedStr(expr):
    values: list[expr]

@grepr_dataclass(init=False)
class LShift(operator):
    pass

@grepr_dataclass(init=False)
class Lambda(expr):
    args: arguments
    body: expr

@grepr_dataclass(init=False)
class List(expr):
    elts: list[expr]
    ctx: expr_context

@grepr_dataclass(init=False)
class ListComp(expr):
    elt: expr
    generators: list[comprehension]

@grepr_dataclass(init=False)
class Load(expr_context):
    pass

@grepr_dataclass(init=False)
class Lt(cmpop):
    pass

@grepr_dataclass(init=False)
class LtE(cmpop):
    pass

@grepr_dataclass(init=False)
class MatMult(operator):
    pass

@grepr_dataclass(init=False)
class Match(stmt):
    subject: expr
    cases: list[match_case]

@grepr_dataclass(init=False)
class MatchAs(pattern):
    pattern: pattern | None
    name: str | None

@grepr_dataclass(init=False)
class MatchClass(pattern):
    cls: expr
    patterns: list[pattern]
    kwd_attrs: list[str]
    kwd_patterns: list[pattern]

@grepr_dataclass(init=False)
class MatchMapping(pattern):
    keys: list[expr]
    patterns: list[pattern]
    rest: str | None

@grepr_dataclass(init=False)
class MatchOr(pattern):
    patterns: list[pattern]

@grepr_dataclass(init=False)
class MatchSequence(pattern):
    patterns: list[pattern]

@grepr_dataclass(init=False)
class MatchSingleton(pattern):
    value: bool | None

@grepr_dataclass(init=False)
class MatchStar(pattern):
    name: str | None

@grepr_dataclass(init=False)
class MatchValue(pattern):
    value: expr

@grepr_dataclass(init=False)
class Mod(operator):
    pass

@grepr_dataclass(init=False)
class Module(mod):
    body: list[stmt]
    type_ignores: list[TypeIgnore]

@grepr_dataclass(init=False)
class Mult(operator):
    pass

@grepr_dataclass(init=False)
class Name(expr):
    id: str
    ctx: expr_context

@grepr_dataclass(init=False)
class NamedExpr(expr):
    target: Name
    value: expr

@grepr_dataclass(init=False)
class Nonlocal(stmt):
    names: list[str]

@grepr_dataclass(init=False)
class Not(unaryop):
    pass

@grepr_dataclass(init=False)
class NotEq(cmpop):
    pass

@grepr_dataclass(init=False)
class NotIn(cmpop):
    pass

@grepr_dataclass(init=False)
class Or(boolop):
    pass

@grepr_dataclass(init=False)
class ParamSpec(type_param):
    name: str
    default_value: expr | None

@grepr_dataclass(init=False)
class Pass(stmt):
    pass

@grepr_dataclass(init=False)
class Pow(operator):
    pass

@grepr_dataclass(init=False)
class RShift(operator):
    pass

@grepr_dataclass(init=False)
class Raise(stmt):
    exc: expr | None
    cause: expr | None

@grepr_dataclass(init=False)
class Return(stmt):
    value: expr | None

@grepr_dataclass(init=False)
class Set(expr):
    elts: list[expr]

@grepr_dataclass(init=False)
class SetComp(expr):
    elt: expr
    generators: list[comprehension]

@grepr_dataclass(init=False)
class Slice(expr):
    lower: expr | None
    upper: expr | None
    step: expr | None

@grepr_dataclass(init=False)
class Starred(expr):
    value: expr
    ctx: expr_context

@grepr_dataclass(init=False)
class Store(expr_context):
    pass

@grepr_dataclass(init=False)
class Sub(operator):
    pass

@grepr_dataclass(init=False)
class Subscript(expr):
    value: expr
    slice: expr
    ctx: expr_context

@grepr_dataclass(init=False)
class Try(stmt):
    body: list[stmt]
    handlers: list[ExceptHandler]
    orelse: list[stmt]
    finalbody: list[stmt]

@grepr_dataclass(init=False)
class Tuple(expr):
    elts: list[expr]
    ctx: expr_context
    # I removed the deprecated dims field

@grepr_dataclass(init=False)
class TypeAlias(stmt):
    name: Name
    type_params: list[type_param]
    value: expr

@grepr_dataclass(init=False)
class TypeIgnore(type_ignore):
    lineno: int | None = field(grepr=False)
    tag: str

@grepr_dataclass(init=False)
class TypeVar(type_param):
    name: str
    bound: expr | None
    default_value: expr | None

@grepr_dataclass(init=False)
class TypeVarTuple(type_param):
    name: str
    default_value: expr | None

@grepr_dataclass(init=False)
class UAdd(unaryop):
    pass

@grepr_dataclass(init=False)
class USub(unaryop):
    pass

@grepr_dataclass(init=False)
class UnaryOp(expr):
    op: unaryop
    operand: expr

@grepr_dataclass(init=False)
class While(stmt):
    test: expr
    body: list[stmt]
    orelse: list[stmt]

@grepr_dataclass(init=False)
class With(stmt):
    items: list[withitem]
    body: list[stmt]
    type_comment: str | None

@grepr_dataclass(init=False)
class Yield(expr):
    value: expr | None

@grepr_dataclass(init=False)
class YieldFrom(expr):
    value: expr

#================================================================================================================#
#                                                    Variables                                                   #
#================================================================================================================#

# Relevant groups of nodes
SCOPE_PROVIDING_CLASSES: list[type[DCST]] = [Module, FunctionDef, AsyncFunctionDef, ClassDef, Lambda, ListComp, SetComp, DictComp, GeneratorExp]
SUBDEFINITION_ALLOWING_CLASSES: list[type[DCST]] = [Module, FunctionDef, AsyncFunctionDef, ClassDef]

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
__all__.append("DCST_CLASSES")
