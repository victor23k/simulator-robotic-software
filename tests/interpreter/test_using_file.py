import os

from simulator.interpreter.interpreter import Interpreter
from simulator.interpreter.parser import Parser
from simulator.interpreter.resolver import Resolver
from simulator.interpreter.token import TokenType
from tests.interpreter.ast import (
    BinaryExprSpec,
    ExpressionStmtSpec,
    ExprSpec,
    LiteralExprSpec,
    StmtSpec,
    TokenSpec,
    VariableExprSpec,
    VariableStmtSpec,
)


def match_structure(actual: object, spec: object):
    if isinstance(spec, list):
        return isinstance(actual, list) and all(
            match_structure(a, s) for a, s in zip(actual, spec)
        )
    elif hasattr(spec, "__dict__") and (
        str.rstrip(spec.__class__.__name__, "Spec") == actual.__class__.__name__
    ):
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


input_test_dir = "./tests/interpreter/inputs/"
output_test_dir = "./tests/interpreter/outputs/"
input_test_filenames = os.listdir(input_test_dir)
output_test_filenames = os.listdir(output_test_dir)
test_failures_filenames = [filename for filename in input_test_filenames if
    filename.rfind("_fails") != -1]

input_test_filenames = set(input_test_filenames).difference(test_failures_filenames)

for input_filename in input_test_filenames:
    input_file_path = os.path.join(input_test_dir, input_filename)
    with open(input_file_path, "r") as ino_file:
        code = ino_file.read()

        diags = []
        parser = Parser(code, diags)
        stmts = parser.parse()

    output_filename_noext, _ext = os.path.splitext(input_filename)
    if output_filename_noext + ".ir" not in output_test_filenames:
        raise Exception(f"No expected output file for test '{input_filename}' found.")

    output_file_path = os.path.join(output_test_dir, output_filename_noext + ".ir")

    with open(output_file_path, "r") as ir_file:
        ir = ir_file.read()
        spec_stmts: list[StmtSpec] = eval(ir)

    if not match_structure(stmts, spec_stmts):
        raise Exception(f"Parser error in test case '{input_filename}'")

    interpreter = Interpreter(stmts, diags)
    resolver = Resolver(interpreter)
    resolver.resolve(stmts)

    if len(diags) > 0:
        raise Exception(f"Error in test case '{input_filename}'. {diags}")

for failure_filename in test_failures_filenames:
    input_file_path = os.path.join(input_test_dir, failure_filename)
    with open(input_file_path, "r") as ino_file:
        code = ino_file.read()
        diags = []

        parser = Parser(code, diags)
        stmts = parser.parse()
        interpreter = Interpreter(stmts, diags)
        resolver = Resolver(interpreter)
        resolver.resolve(stmts)

        if len(diags) == 0:
            raise Exception(f"Error in test case '{failure_filename}'")
