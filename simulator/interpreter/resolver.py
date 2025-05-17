from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.expr import BinaryExpr, Expr, LiteralExpr, VariableExpr
from simulator.interpreter.interpreter import Interpreter
from simulator.interpreter.scope import ScopeChain
from simulator.interpreter.stmt import ExpressionStmt, Stmt, VariableStmt
from simulator.interpreter.types import (
    ArduinoType,
    TypeException,
    token_to_arduino_type,
)


class Resolver:
    """
    This interpreter pass performs type checking and resolves the scopes for
    variables.
    """

    interpreter: Interpreter
    diagnostics: list[Diagnostic]
    scope_chain: ScopeChain

    def __init__(self, interpreter: Interpreter):
        self.diagnostics = interpreter.diagnostics
        self.scope_chain = ScopeChain(self.diagnostics, interpreter)
        self.interpreter = interpreter

    def resolve(self, stmts: list[Stmt]):
        for stmt in stmts:
            match stmt:
                case VariableStmt(var_type, name, initializer):
                    var_arduino_type = token_to_arduino_type(var_type)
                    self.scope_chain.declare(name, var_type)
                    if initializer is not None:
                        try:
                            init_type = self._resolve_expr(initializer)
                            self._check_types(var_arduino_type, init_type)
                            self.scope_chain.define(name)
                        except TypeException:
                            diag = stmt.gen_diagnostic("Initializer expression has incompatible types.")
                            self.diagnostics.append(diag)
                case ExpressionStmt():
                    self._resolve_expr(stmt.expr)

    def _resolve_expr(self, expr: Expr) -> ArduinoType:
        match expr:
            case VariableExpr():
                distance = self.scope_chain.use(expr.vname)
                expr.scope_distance = distance
                expr.check_type(self.scope_chain)
                return expr.ttype
            case LiteralExpr():
                expr.check_type(self.scope_chain)
                return expr.ttype
            case BinaryExpr():
                lhs_type = self._resolve_expr(expr.lhs)
                rhs_type = self._resolve_expr(expr.rhs)
                try:
                    return self._check_types(lhs_type, rhs_type)
                except TypeException as e:
                    diag = expr.gen_diagnostic(repr(e))
                    self.diagnostics.append(diag)
                    raise

    def _check_types(self, type_a: ArduinoType, type_b: ArduinoType) -> ArduinoType:
        if type_a == type_b:
            return type_a
        else:
            raise TypeException(f"Types '{type_a}' and '{type_b}' not compatible.")
