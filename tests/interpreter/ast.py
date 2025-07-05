from dataclasses import dataclass

from simulator.interpreter.token import TokenType

type StmtSpec = ExpressionStmtSpec | VariableStmtSpec
type ExprSpec = VariableExprSpec | BinaryExprSpec | LiteralExprSpec


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
    initializer: ExprSpec


@dataclass
class VariableExprSpec:
    vname: TokenSpec


@dataclass
class LiteralExprSpec:
    value: TokenSpec


@dataclass
class AssignExpr:
    name: TokenSpec
    value: ExprSpec


@dataclass
class BinaryExprSpec:
    lhs: ExprSpec
    op: TokenSpec
    rhs: ExprSpec
