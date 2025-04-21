from simulator.interpreter.scanner import Diagnostic
from simulator.interpreter.stmt import Stmt, ExpressionStmt
from simulator.interpreter.expr import Expr, BinaryExpr, LiteralExpr
from simulator.interpreter.token import TokenType

class Interpreter:
    """
    Runs an Arduino Language AST by evaluating expressions and executing
    statements.
    """
    statements: [Stmt]

    def __init__(self, statements: [Stmt]):
        self.statements = statements

    def print_diagnostics(self, diagnostics: [Diagnostic]):
        pass

    def run(self):
        for statement in self.statements:
            return self._execute(statement)

    def _execute(self, statement: Stmt):
        match statement:
            case ExpressionStmt(expr):
                return self._evaluate(expr)
            case _:
                pass


    def _evaluate(self, expression: Expr):
        match expression:
            case LiteralExpr(value):
                return value
            case BinaryExpr(lhs, token, rhs):
                left = self._evaluate(lhs)
                right = self._evaluate(rhs)

                match token.token:
                    case TokenType.PLUS:
                        return left + right
                    case TokenType.MINUS:
                        return left - right
                    case TokenType.STAR:
                        return left * right
                    case TokenType.SLASH:
                        if right == 0:
                            # error, can`t divide by 0
                            pass
                        else:
                            return left / right
                    case TokenType.PERCENTAGE:
                        return left % right
