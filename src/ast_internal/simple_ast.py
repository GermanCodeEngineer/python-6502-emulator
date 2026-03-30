from __future__ import annotations
from gceutils import grepr_dataclass

# Simple, auto-generated dataclasses for AST node names
# Fields are annotated as Optional[Any] for simplicity.


@grepr_dataclass()
class AST:
    pass

@grepr_dataclass()
class alias(AST):
    name: str = None
    asname: str | None = None
    lineno: int = None
    col_offset: int = None
    end_lineno: int | None = None
    end_col_offset: int | None = None

@grepr_dataclass()
class arg(AST):
    lineno: int = None
    col_offset: int = None
    end_lineno: int | None = None
    end_col_offset: int | None = None
    arg: str = None
    annotation: expr | None = None
    type_comment: str | None = None

@grepr_dataclass()
class arguments(AST):
    posonlyargs: list[arg] = None
    args: list[arg] = None
    vararg: arg | None = None
    kwonlyargs: list[arg] = None
    kw_defaults: list[expr | None] = None
    kwarg: arg | None = None
    defaults: list[expr] = None

@grepr_dataclass()
class boolop(AST):
    pass

@grepr_dataclass()
class cmpop(AST):
    pass

@grepr_dataclass()
class comprehension(AST):
    target: expr = None
    iter: expr = None
    ifs: list[expr] = None
    is_async: int = None

@grepr_dataclass()
class excepthandler(AST):
    lineno: int = None
    col_offset: int = None
    end_lineno: int | None = None
    end_col_offset: int | None = None

@grepr_dataclass()
class expr(AST):
    lineno: int = None
    col_offset: int = None
    end_lineno: int | None = None
    end_col_offset: int | None = None

@grepr_dataclass()
class expr_context(AST):
    pass

@grepr_dataclass()
class keyword(AST):
    lineno: int = None
    col_offset: int = None
    end_lineno: int | None = None
    end_col_offset: int | None = None
    arg: str | None = None
    value: expr = None

@grepr_dataclass()
class match_case(AST):
    pattern: pattern = None
    guard: expr | None = None
    body: list[stmt] = None

@grepr_dataclass()
class mod(AST):
    pass

@grepr_dataclass()
class operator(AST):
    pass

@grepr_dataclass()
class pattern(AST):
    lineno: int = None
    col_offset: int = None
    end_lineno: int = None
    end_col_offset: int = None

@grepr_dataclass()
class stmt(AST):
    lineno: int = None
    col_offset: int = None
    end_lineno: int | None = None
    end_col_offset: int | None = None

@grepr_dataclass()
class type_ignore(AST):
    pass

@grepr_dataclass()
class type_param(AST):
    lineno: int = None
    col_offset: int = None
    end_lineno: int = None
    end_col_offset: int = None

@grepr_dataclass()
class unaryop(AST):
    pass

@grepr_dataclass()
class withitem(AST):
    context_expr: expr = None
    optional_vars: expr | None = None

@grepr_dataclass()
class Add(operator):
    pass

@grepr_dataclass()
class And(boolop):
    pass

@grepr_dataclass()
class AnnAssign(stmt):
    target: Name | Attribute | Subscript = None
    annotation: expr = None
    value: expr | None = None
    simple: int = None

@grepr_dataclass()
class Assert(stmt):
    test: expr = None
    msg: expr | None = None

@grepr_dataclass()
class Assign(stmt):
    targets: list[expr] = None
    value: expr = None
    type_comment: str | None = None

@grepr_dataclass()
class AsyncFor(stmt):
    target: expr = None
    iter: expr = None
    body: list[stmt] = None
    orelse: list[stmt] = None
    type_comment: str | None = None

@grepr_dataclass()
class AsyncFunctionDef(stmt):
    name: str = None
    args: arguments = None
    body: list[stmt] = None
    decorator_list: list[expr] = None
    returns: expr | None = None
    type_comment: str | None = None
    type_params: list[type_param] = None

@grepr_dataclass()
class AsyncWith(stmt):
    items: list[withitem] = None
    body: list[stmt] = None
    type_comment: str | None = None

@grepr_dataclass()
class Attribute(expr):
    value: expr = None
    attr: str = None
    ctx: expr_context = None

@grepr_dataclass()
class AugAssign(stmt):
    target: Name | Attribute | Subscript = None
    op: operator = None
    value: expr = None

@grepr_dataclass()
class Await(expr):
    value: expr = None

@grepr_dataclass()
class BinOp(expr):
    left: expr = None
    op: operator = None
    right: expr = None

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
    op: boolop = None
    values: list[expr] = None

@grepr_dataclass()
class Break(stmt):
    pass

@grepr_dataclass()
class Call(expr):
    func: expr = None
    args: list[expr] = None
    keywords: list[keyword] = None

@grepr_dataclass()
class ClassDef(stmt):
    name: str = None
    bases: list[expr] = None
    keywords: list[keyword] = None
    body: list[stmt] = None
    decorator_list: list[expr] = None
    type_params: list[type_param] = None

@grepr_dataclass()
class Compare(expr):
    left: expr = None
    ops: list[cmpop] = None
    comparators: list[expr] = None

@grepr_dataclass()
class Constant(expr):
    value: _ConstantValue = None
    kind: str | None = None

@grepr_dataclass()
class Continue(stmt):
    pass

@grepr_dataclass()
class Del(expr_context):
    pass

@grepr_dataclass()
class Delete(stmt):
    targets: list[expr] = None

@grepr_dataclass()
class Dict(expr):
    keys: list[expr | None] = None
    values: list[expr] = None

@grepr_dataclass()
class DictComp(expr):
    key: expr = None
    value: expr = None
    generators: list[comprehension] = None

@grepr_dataclass()
class Div(operator):
    pass

@grepr_dataclass()
class Eq(cmpop):
    pass

@grepr_dataclass()
class ExceptHandler(excepthandler):
    type: expr | None = None
    name: str | None = None
    body: list[stmt] = None

@grepr_dataclass()
class Expr(stmt):
    value: expr = None

@grepr_dataclass()
class Expression(mod):
    body: expr = None

@grepr_dataclass()
class FloorDiv(operator):
    pass

@grepr_dataclass()
class For(stmt):
    target: expr = None
    iter: expr = None
    body: list[stmt] = None
    orelse: list[stmt] = None
    type_comment: str | None = None

@grepr_dataclass()
class FormattedValue(expr):
    value: expr = None
    conversion: int = None
    format_spec: expr | None = None

@grepr_dataclass()
class FunctionDef(stmt):
    name: str = None
    args: arguments = None
    body: list[stmt] = None
    decorator_list: list[expr] = None
    returns: expr | None = None
    type_comment: str | None = None
    type_params: list[type_param] = None

@grepr_dataclass()
class FunctionType(mod):
    argtypes: list[expr] = None
    returns: expr = None

@grepr_dataclass()
class GeneratorExp(expr):
    elt: expr = None
    generators: list[comprehension] = None

@grepr_dataclass()
class Global(stmt):
    names: list[str] = None

@grepr_dataclass()
class Gt(cmpop):
    pass

@grepr_dataclass()
class GtE(cmpop):
    pass

@grepr_dataclass()
class If(stmt):
    test: expr = None
    body: list[stmt] = None
    orelse: list[stmt] = None

@grepr_dataclass()
class IfExp(expr):
    test: expr = None
    body: expr = None
    orelse: expr = None

@grepr_dataclass()
class Import(stmt):
    names: list[alias] = None

@grepr_dataclass()
class ImportFrom(stmt):
    module: str | None = None
    names: list[alias] = None
    level: int = None

@grepr_dataclass()
class In(cmpop):
    pass

@grepr_dataclass()
class Interactive(mod):
    body: list[stmt] = None

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
    values: list[expr] = None

@grepr_dataclass()
class LShift(operator):
    pass

@grepr_dataclass()
class Lambda(expr):
    args: arguments = None
    body: expr = None

@grepr_dataclass()
class List(expr):
    elts: list[expr] = None
    ctx: expr_context = None

@grepr_dataclass()
class ListComp(expr):
    elt: expr = None
    generators: list[comprehension] = None

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
    subject: expr = None
    cases: list[match_case] = None

@grepr_dataclass()
class MatchAs(pattern):
    pattern: pattern | None = None
    name: str | None = None

@grepr_dataclass()
class MatchClass(pattern):
    cls: expr = None
    patterns: list[pattern] = None
    kwd_attrs: list[str] = None
    kwd_patterns: list[pattern] = None

@grepr_dataclass()
class MatchMapping(pattern):
    keys: list[expr] = None
    patterns: list[pattern] = None
    rest: str | None = None

@grepr_dataclass()
class MatchOr(pattern):
    patterns: list[pattern] = None

@grepr_dataclass()
class MatchSequence(pattern):
    patterns: list[pattern] = None

@grepr_dataclass()
class MatchSingleton(pattern):
    value: bool | None = None

@grepr_dataclass()
class MatchStar(pattern):
    name: str | None = None

@grepr_dataclass()
class MatchValue(pattern):
    value: expr = None

@grepr_dataclass()
class Mod(operator):
    pass

@grepr_dataclass()
class Module(mod):
    body: list[stmt] = None
    type_ignores: list[TypeIgnore] = None

@grepr_dataclass()
class Mult(operator):
    pass

@grepr_dataclass()
class Name(expr):
    id: str = None
    ctx: expr_context = None

@grepr_dataclass()
class NamedExpr(expr):
    target: Name = None
    value: expr = None

@grepr_dataclass()
class Nonlocal(stmt):
    names: list[str] = None

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
    name: str = None
    default_value: expr | None = None

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
    exc: expr | None = None
    cause: expr | None = None

@grepr_dataclass()
class Return(stmt):
    value: expr | None = None

@grepr_dataclass()
class Set(expr):
    elts: list[expr] = None

@grepr_dataclass()
class SetComp(expr):
    elt: expr = None
    generators: list[comprehension] = None

@grepr_dataclass()
class Slice(expr):
    lower: expr | None = None
    upper: expr | None = None
    step: expr | None = None

@grepr_dataclass()
class Starred(expr):
    value: expr = None
    ctx: expr_context = None

@grepr_dataclass()
class Store(expr_context):
    pass

@grepr_dataclass()
class Sub(operator):
    pass

@grepr_dataclass()
class Subscript(expr):
    value: expr = None
    slice: expr = None
    ctx: expr_context = None

@grepr_dataclass()
class Try(stmt):
    body: list[stmt] = None
    handlers: list[ExceptHandler] = None
    orelse: list[stmt] = None
    finalbody: list[stmt] = None

@grepr_dataclass()
class Tuple(expr):
    elts: list[expr] = None
    ctx: expr_context = None
    dims: list[expr] = None

@grepr_dataclass()
class TypeAlias(stmt):
    name: Name = None
    type_params: list[type_param] = None
    value: expr = None

@grepr_dataclass()
class TypeIgnore(type_ignore):
    lineno: int = None
    tag: str = None

@grepr_dataclass()
class TypeVar(type_param):
    name: str = None
    bound: expr | None = None
    default_value: expr | None = None

@grepr_dataclass()
class TypeVarTuple(type_param):
    name: str = None
    default_value: expr | None = None

@grepr_dataclass()
class UAdd(unaryop):
    pass

@grepr_dataclass()
class USub(unaryop):
    pass

@grepr_dataclass()
class UnaryOp(expr):
    op: unaryop = None
    operand: expr = None

@grepr_dataclass()
class While(stmt):
    test: expr = None
    body: list[stmt] = None
    orelse: list[stmt] = None

@grepr_dataclass()
class With(stmt):
    items: list[withitem] = None
    body: list[stmt] = None
    type_comment: str | None = None

@grepr_dataclass()
class Yield(expr):
    value: expr | None = None

@grepr_dataclass()
class YieldFrom(expr):
    value: expr = None
