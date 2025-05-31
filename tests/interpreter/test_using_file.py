from simulator.interpreter.parser import Parser
from simulator.interpreter.token import TokenType
from tests.interpreter.ast import (
    BinaryExprSpec,
    ExpressionStmtSpec,
    ExprSpec,
    LiteralExprSpec,
    TokenSpec,
    VariableExprSpec,
    VariableStmtSpec,
)


def match_structure(actual: object, spec: object):
    if isinstance(spec, list):
        return (isinstance(actual, list) and 
            all(match_structure(a, s) for a, s in zip(actual, spec)))
    elif (hasattr(spec, '__dict__') and 
         (str.rstrip(spec.__class__.__name__, "Spec") ==
         actual.__class__.__name__)):
        for key, val in spec.__dict__.items():
            if not hasattr(actual, key):
                return False
            if not match_structure(getattr(actual, key), val):
                print(getattr(actual, key))
                print(val)
                return False
        return True
    else:
        return spec is None or spec == actual

with open("./tests/interpreter/outputs/variable_assignment.ir", "r") as ir_file:
    ir = ir_file.read()

with open("./tests/interpreter/inputs/variable_assignment.ino", "r") as ino_file:
    code = ino_file.read()

parser = Parser(code, [])
stmts = parser.parse()

spec_stmts = eval(ir)
print(match_structure(stmts, spec_stmts))
