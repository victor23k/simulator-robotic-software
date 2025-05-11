from dataclasses import dataclass

import simulator.interpreter.scope as scope
import simulator.interpreter.expr as expr
from simulator.interpreter.diagnostic import Diagnostic, diagnostic_from_token
from simulator.interpreter.environment import Environment, Value
from simulator.interpreter.token import Token

type Stmt = ExpressionStmt | VariableStmt

@dataclass
class ExpressionStmt:
    expr: expr.Expr

    def execute(self, env: Environment):
        self.expr.evaluate(env)

# declaration = type identifier [ array ] [ "=" expression ] ";"

# type = "bool"
#      | "boolean"
#      | "byte"
#      | "char"
#      | "double"
#      | "float"
#      | "int"
#      | "long"
#      | "short"
#      | "size_t"
#      | "unsigned char"
#      | "unsigned int"
#      | "unsigned long"
#      | "word"

# array = "[" number "]"


@dataclass
class VariableStmt:
    var_type: Token
    name: Token
    initializer: expr.Expr | None

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

    def execute(self, environment: Environment):
        init_value = None
        if self.initializer is not None and self.initializer.ttype is not None:
            init_value = self.initializer.evaluate(environment)
            value = Value(self.initializer.ttype, init_value)
            environment.define(self.name, value)
        else:
            environment.define(self.name, None)

    def compute_type(self, scope_chain: scope.ScopeChain):
        scope_chain.declare(self.name, self.var_type)
        if self.initializer is not None:
            self.initializer.check_type(scope_chain)
            if self.initializer.ttype is not self.var_type:
                # add diag
                pass
