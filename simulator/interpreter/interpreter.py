from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.environment import EnvError, Environment, Value
from simulator.interpreter.expr import Expr
from simulator.interpreter.stmt import Stmt
from simulator.interpreter.token import TokenType
from simulator.interpreter.types import token_to_arduino_type


class Interpreter:
    """
    Runs an Arduino Language AST by evaluating expressions and executing
    statements.
    """

    statements: list[Stmt]
    environment: Environment

    def __init__(self, statements: list[Stmt]):
        self.statements = statements
        self.environment = Environment()

    def print_diagnostics(self, diagnostics: list[Diagnostic]):
        pass

    def run(self) -> None:
        for statement in self.statements:
            return statement.execute(self.environment)

    def resolve(self, expr: Expr, depth: int):
        # todo
        pass

    def resolve_global(self, expr: Expr):
        pass


    # def _execute(self, statement: Stmt) -> None:
    #     match statement:
    #         case ExpressionStmt(expr):
    #             self._evaluate(expr)
    #         case VariableStmt(var_type, name, initializer):
    #             init_value = None
    #             if initializer:
    #                 init_value = self._evaluate(initializer)
    #
    #             value = Value(var_type.token, init_value)
    #             self.environment.define(name, value)
    #         case _:
    #             pass
    #
    # def _evaluate(self, expr: Expr) -> Value:
    #     match expr:
    #         case LiteralExpr():
    #             return Value(expr.value.token, token_to_arduino_type(expr.value))
    #         case VariableExpr(name):
    #             return self.environment.get(name)
    #         case BinaryExpr(lhs, token, rhs):
    #             left = self._evaluate(lhs)
    #             right = self._evaluate(rhs)
    #
    #             match token.token:
    #                 # at this point, types have been checked and ops should work
    #                 case TokenType.PLUS:
    #                     return left.value + right.value
    #                 case TokenType.MINUS:
    #                     return left.value - right.value
    #                 case TokenType.STAR:
    #                     return left.value * right.value
    #                 case TokenType.SLASH:
    #                     if right == 0:
    #                         # error, can`t divide by 0
    #                         return EnvError.VariableDoesNotExist
    #                     else:
    #                         return left / right
    #                 case TokenType.PERCENTAGE:
    #                     return left % right
    #         case _:
    #             return EnvError.VariableDoesNotExist
