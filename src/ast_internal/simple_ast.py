from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional

# Simple, auto-generated dataclasses for AST node names
# Fields are annotated as Optional[Any] for simplicity.


@dataclass
class AST:
    pass

@dataclass
class alias(AST):
    name: str = None
    asname: Optional[AST] = None

@dataclass
class arg(AST):
    arg: str = None
    annotation: Optional[AST] = None
    type_comment: Optional[str] = None

@dataclass
class arguments(AST):
    posonlyargs: list[AST] = None
    args: list[AST] = None
    vararg: Optional[AST] = None
    kwonlyargs: list[AST] = None
    kw_defaults: list[AST] = None
    kwarg: Optional[AST] = None
    defaults: list[AST] = None

@dataclass
class boolop(AST):
    pass

@dataclass
class cmpop(AST):
    pass

@dataclass
class comprehension(AST):
    target: Optional[AST] = None
    iter: Optional[AST] = None
    ifs: list[AST] = None
    is_async: Optional[AST] = None

@dataclass
class excepthandler(AST):
    pass

@dataclass
class expr(AST):
    pass

@dataclass
class expr_context(AST):
    pass

@dataclass
class keyword(AST):
    arg: str = None
    value: Optional[AST] = None

@dataclass
class match_case(AST):
    pattern: Optional[AST] = None
    guard: Optional[AST] = None
    body: list[AST] = None

@dataclass
class mod(AST):
    pass

@dataclass
class operator(AST):
    pass

@dataclass
class pattern(AST):
    pass

@dataclass
class stmt(AST):
    pass

@dataclass
class type_ignore(AST):
    pass

@dataclass
class type_param(AST):
    pass

@dataclass
class unaryop(AST):
    pass

@dataclass
class withitem(AST):
    context_expr: Optional[AST] = None
    optional_vars: list[AST] = None

@dataclass
class Add(operator):
    pass

@dataclass
class And(boolop):
    pass

@dataclass
class AnnAssign(stmt):
    target: Optional[AST] = None
    annotation: Optional[AST] = None
    value: Optional[AST] = None
    simple: Optional[AST] = None

@dataclass
class Assert(stmt):
    test: Optional[AST] = None
    msg: Optional[AST] = None

@dataclass
class Assign(stmt):
    targets: list[AST] = None
    value: Optional[AST] = None
    type_comment: Optional[str] = None

@dataclass
class AsyncFor(stmt):
    target: Optional[AST] = None
    iter: Optional[AST] = None
    body: list[AST] = None
    orelse: list[AST] = None
    type_comment: Optional[str] = None

@dataclass
class AsyncFunctionDef(stmt):
    name: str = None
    args: list[AST] = None
    body: list[AST] = None
    decorator_list: list[AST] = None
    returns: list[AST] = None
    type_comment: Optional[str] = None
    type_params: list[AST] = None

@dataclass
class AsyncWith(stmt):
    items: list[AST] = None
    body: list[AST] = None
    type_comment: Optional[str] = None

@dataclass
class Attribute(expr):
    value: Optional[AST] = None
    attr: str = None
    ctx: expr_context = None

@dataclass
class AugAssign(stmt):
    target: Optional[AST] = None
    op: Optional[AST] = None
    value: Optional[AST] = None

@dataclass
class Await(expr):
    value: Optional[AST] = None

@dataclass
class BinOp(expr):
    left: Optional[AST] = None
    op: Optional[AST] = None
    right: Optional[AST] = None

@dataclass
class BitAnd(operator):
    pass

@dataclass
class BitOr(operator):
    pass

@dataclass
class BitXor(operator):
    pass

@dataclass
class BoolOp(expr):
    op: Optional[AST] = None
    values: list[AST] = None

@dataclass
class Break(stmt):
    pass

@dataclass
class Call(expr):
    func: Optional[AST] = None
    args: list[AST] = None
    keywords: list[AST] = None

@dataclass
class ClassDef(stmt):
    name: str = None
    bases: list[AST] = None
    keywords: list[AST] = None
    body: list[AST] = None
    decorator_list: list[AST] = None
    type_params: list[AST] = None

@dataclass
class Compare(expr):
    left: Optional[AST] = None
    ops: list[AST] = None
    comparators: list[AST] = None

@dataclass
class Constant(expr):
    value: Optional[AST] = None
    kind: Optional[str] = None

@dataclass
class Continue(stmt):
    pass

@dataclass
class Del(expr_context):
    pass

@dataclass
class Delete(stmt):
    targets: list[AST] = None

@dataclass
class Dict(expr):
    keys: list[AST] = None
    values: list[AST] = None

@dataclass
class DictComp(expr):
    key: Optional[AST] = None
    value: Optional[AST] = None
    generators: list[AST] = None

@dataclass
class Div(operator):
    pass

@dataclass
class Eq(cmpop):
    pass

@dataclass
class ExceptHandler(excepthandler):
    type: Optional[AST] = None
    name: str = None
    body: list[AST] = None

@dataclass
class Expr(stmt):
    value: Optional[AST] = None

@dataclass
class Expression(mod):
    body: list[AST] = None

@dataclass
class FloorDiv(operator):
    pass

@dataclass
class For(stmt):
    target: Optional[AST] = None
    iter: Optional[AST] = None
    body: list[AST] = None
    orelse: list[AST] = None
    type_comment: Optional[str] = None

@dataclass
class FormattedValue(expr):
    value: Optional[AST] = None
    conversion: Optional[AST] = None
    format_spec: Optional[AST] = None

@dataclass
class FunctionDef(stmt):
    name: str = None
    args: list[AST] = None
    body: list[AST] = None
    decorator_list: list[AST] = None
    returns: list[AST] = None
    type_comment: Optional[str] = None
    type_params: list[AST] = None

@dataclass
class FunctionType(mod):
    argtypes: list[AST] = None
    returns: list[AST] = None

@dataclass
class GeneratorExp(expr):
    elt: Optional[AST] = None
    generators: list[AST] = None

@dataclass
class Global(stmt):
    names: list[AST] = None

@dataclass
class Gt(cmpop):
    pass

@dataclass
class GtE(cmpop):
    pass

@dataclass
class If(stmt):
    test: Optional[AST] = None
    body: list[AST] = None
    orelse: list[AST] = None

@dataclass
class IfExp(expr):
    test: Optional[AST] = None
    body: list[AST] = None
    orelse: list[AST] = None

@dataclass
class Import(stmt):
    names: list[AST] = None

@dataclass
class ImportFrom(stmt):
    module: Optional[AST] = None
    names: list[AST] = None
    level: Optional[AST] = None

@dataclass
class In(cmpop):
    pass

@dataclass
class Interactive(mod):
    body: list[AST] = None

@dataclass
class Invert(unaryop):
    pass

@dataclass
class Is(cmpop):
    pass

@dataclass
class IsNot(cmpop):
    pass

@dataclass
class JoinedStr(expr):
    values: list[AST] = None

@dataclass
class LShift(operator):
    pass

@dataclass
class Lambda(expr):
    args: list[AST] = None
    body: list[AST] = None

@dataclass
class List(expr):
    elts: list[AST] = None
    ctx: expr_context = None

@dataclass
class ListComp(expr):
    elt: Optional[AST] = None
    generators: list[AST] = None

@dataclass
class Load(expr_context):
    pass

@dataclass
class Lt(cmpop):
    pass

@dataclass
class LtE(cmpop):
    pass

@dataclass
class MatMult(operator):
    pass

@dataclass
class Match(stmt):
    subject: Optional[AST] = None
    cases: list[AST] = None

@dataclass
class MatchAs(pattern):
    pattern: Optional[AST] = None
    name: str = None

@dataclass
class MatchClass(pattern):
    cls: list[AST] = None
    patterns: list[AST] = None
    kwd_attrs: list[AST] = None
    kwd_patterns: list[AST] = None

@dataclass
class MatchMapping(pattern):
    keys: list[AST] = None
    patterns: list[AST] = None
    rest: Optional[AST] = None

@dataclass
class MatchOr(pattern):
    patterns: list[AST] = None

@dataclass
class MatchSequence(pattern):
    patterns: list[AST] = None

@dataclass
class MatchSingleton(pattern):
    value: Optional[AST] = None

@dataclass
class MatchStar(pattern):
    name: str = None

@dataclass
class MatchValue(pattern):
    value: Optional[AST] = None

@dataclass
class Mod(operator):
    pass

@dataclass
class Module(mod):
    body: list[AST] = None
    type_ignores: list[AST] = None

@dataclass
class Mult(operator):
    pass

@dataclass
class Name(expr):
    id: str = None
    ctx: expr_context = None

@dataclass
class NamedExpr(expr):
    target: Optional[AST] = None
    value: Optional[AST] = None

@dataclass
class Nonlocal(stmt):
    names: list[AST] = None

@dataclass
class Not(unaryop):
    pass

@dataclass
class NotEq(cmpop):
    pass

@dataclass
class NotIn(cmpop):
    pass

@dataclass
class Or(boolop):
    pass

@dataclass
class ParamSpec(type_param):
    name: str = None
    default_value: Optional[AST] = None

@dataclass
class Pass(stmt):
    pass

@dataclass
class Pow(operator):
    pass

@dataclass
class RShift(operator):
    pass

@dataclass
class Raise(stmt):
    exc: Optional[AST] = None
    cause: Optional[AST] = None

@dataclass
class Return(stmt):
    value: Optional[AST] = None

@dataclass
class Set(expr):
    elts: list[AST] = None

@dataclass
class SetComp(expr):
    elt: Optional[AST] = None
    generators: list[AST] = None

@dataclass
class Slice(expr):
    lower: Optional[AST] = None
    upper: Optional[AST] = None
    step: Optional[AST] = None

@dataclass
class Starred(expr):
    value: Optional[AST] = None
    ctx: expr_context = None

@dataclass
class Store(expr_context):
    pass

@dataclass
class Sub(operator):
    pass

@dataclass
class Subscript(expr):
    value: Optional[AST] = None
    slice: Optional[AST] = None
    ctx: expr_context = None

@dataclass
class Try(stmt):
    body: list[AST] = None
    handlers: list[AST] = None
    orelse: list[AST] = None
    finalbody: list[AST] = None

@dataclass
class Tuple(expr):
    elts: list[AST] = None
    ctx: expr_context = None

@dataclass
class TypeAlias(stmt):
    name: str = None
    type_params: list[AST] = None
    value: Optional[AST] = None

@dataclass
class TypeIgnore(type_ignore):
    lineno: int = None
    tag: Optional[AST] = None

@dataclass
class TypeVar(type_param):
    name: str = None
    bound: Optional[AST] = None
    default_value: Optional[AST] = None

@dataclass
class TypeVarTuple(type_param):
    name: str = None
    default_value: Optional[AST] = None

@dataclass
class UAdd(unaryop):
    pass

@dataclass
class USub(unaryop):
    pass

@dataclass
class UnaryOp(expr):
    op: Optional[AST] = None
    operand: Optional[AST] = None

@dataclass
class While(stmt):
    test: Optional[AST] = None
    body: list[AST] = None
    orelse: list[AST] = None

@dataclass
class With(stmt):
    items: list[AST] = None
    body: list[AST] = None
    type_comment: Optional[str] = None

@dataclass
class Yield(expr):
    value: Optional[AST] = None

@dataclass
class YieldFrom(expr):
    value: Optional[AST] = None
