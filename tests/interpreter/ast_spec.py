from dataclasses import dataclass

from simulator.interpreter.lex.token import TokenType

type StmtSpec = (
    BlockStmtSpec
    | ExpressionStmtSpec
    | VariableStmtSpec
    | FunctionStmtSpec
    | ReturnStmtSpec
    | IfStmtSpec
    | SwitchStmtSpec
    | BreakStmtSpec
    | DefaultStmtSpec
    | WhileStmtSpec
    | ForStmtSpec
)
type ExprSpec = (
    AssignExprSpec | CallExprSpec | VariableExprSpec | BinaryExprSpec | LiteralExprSpec
)


@dataclass
class TokenSpec:
    token: TokenType
    lexeme: str | None = None
    literal: object | None = None


@dataclass
class BlockStmtSpec:
    stmts: list[StmtSpec]


@dataclass
class ExpressionStmtSpec:
    expr: ExprSpec


@dataclass
class VariableStmtSpec:
    var_type: TokenSpec
    name: TokenSpec
    initializer: ExprSpec | None = None


@dataclass
class FunctionStmtSpec:
    name: TokenSpec
    params: list[VariableStmtSpec]
    body: BlockStmtSpec
    return_type: TokenSpec


@dataclass
class ReturnStmtSpec:
    expr: ExprSpec


@dataclass
class IfStmtSpec:
    condition: ExprSpec
    then_branch: StmtSpec
    else_branch: StmtSpec


@dataclass
class WhileStmtSpec:
    condition: ExprSpec
    statement: StmtSpec


@dataclass
class ForStmtSpec:
    init_expr: ExprSpec | VariableStmtSpec | None
    condition: ExprSpec | None
    loop_expr: ExprSpec | None
    statement: StmtSpec


@dataclass
class AssignExprSpec:
    l_value: ExprSpec
    op: TokenSpec
    r_value: ExprSpec


@dataclass
class CallExprSpec:
    callee: ExprSpec
    arguments: list[ExprSpec]


@dataclass
class VariableExprSpec:
    vname: TokenSpec


@dataclass
class LiteralExprSpec:
    value: TokenSpec


@dataclass
class BinaryExprSpec:
    lhs: ExprSpec
    op: TokenSpec
    rhs: ExprSpec


@dataclass
class UnaryExprSpec:
    prefix: bool
    op: TokenSpec
    variable: VariableExprSpec


@dataclass
class SwitchStmtSpec:
    var: ExprSpec
    cases: list["CaseStmtSpec"]


@dataclass
class CaseStmtSpec:
    label: ExprSpec | None
    stmts: list[StmtSpec]


@dataclass
class DefaultStmtSpec:
    stmts: list[StmtSpec]


class BreakStmtSpec:
    pass
