import os
import unittest

from simulator.interpreter.interpreter import Interpreter
from simulator.interpreter.parse.parser import Parser
from simulator.interpreter.sema.resolver import Resolver
from simulator.interpreter.lex.scanner import Scanner
from simulator.interpreter.lex.token import TokenType
from tests.interpreter.ast_spec import *


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


input_test_dir = "./tests/interpreter/expected/inputs/"
output_test_dir = "./tests/interpreter/expected/outputs/"
input_test_filenames = os.listdir(input_test_dir)
output_test_filenames = os.listdir(output_test_dir)
test_failures_filenames = [filename for filename in input_test_filenames if
    filename.rfind("_fails") != -1]
scanner_output_filenames = [filename for filename in output_test_filenames if
    filename.rfind(".tok") != -1]

input_test_filenames = set(input_test_filenames).difference(test_failures_filenames)


class ExpectedOutputCase(unittest.TestCase):
    def __init__(self, methodName, code="", ir="", filename="unknown"):
        super(ExpectedOutputCase, self).__init__(methodName)

        self.code: str = code
        self.ir: str = ir
        self.filename: str = filename

    def runTest(self):
        diags = []
        parser = Parser(self.code, diags)
        stmts = parser.parse()
        spec_stmts: list[StmtSpec] = eval(self.ir)


        resolver = Resolver(diags)
        resolver.resolve(stmts)

        self.assertEqual(len(diags), 0, f"No error diagnostics for {self.filename} expected but found: {diags}")
        self.assertTrue(match_structure(stmts, spec_stmts), f"Match error for {self.filename}")


class ExpectedFailureCase(unittest.TestCase):
    def __init__(self, methodName, code="", filename="unknown"):
        super(ExpectedFailureCase, self).__init__(methodName)

        self.code: str = code
        self.filename: str = filename

    def runTest(self):
        diags = []
        parser = Parser(self.code, diags)
        stmts = parser.parse()

        resolver = Resolver(diags)
        resolver.resolve(stmts)

        self.assertNotEqual(len(diags), 0, f"Expected some error diagnostics for {self.filename} but found none")


class ScannerOutputCase(unittest.TestCase):
    def __init__(self, methodName, code="", tok="", filename="unknown"):
        super(ScannerOutputCase, self).__init__(methodName)

        self.code: str = code
        self.tok: str = tok
        self.filename: str = filename

    def runTest(self):
        scanner = Scanner(self.code)
        tokens = [token for token in scanner]
        spec_tokens: list[StmtSpec] = eval(self.tok)

        self.assertEqual(len(scanner.diagnostics), 0, f"No error diagnostics for {self.filename} expected but found: {scanner.diagnostics}")
        self.assertTrue(match_structure(tokens, spec_tokens), f"Match error for {self.filename}")


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    for input_filename in input_test_filenames:
        input_file_path = os.path.join(input_test_dir, input_filename)
        with open(input_file_path, "r") as ino_file:
            code = ino_file.read()

        output_filename_noext, _ext = os.path.splitext(input_filename)
        if output_filename_noext + ".ir" not in output_test_filenames:
            raise Exception(f"No expected output file for test '{input_filename}' found.")

        output_file_path = os.path.join(output_test_dir, output_filename_noext + ".ir")

        with open(output_file_path, "r") as ir_file:
            ir = ir_file.read()
        
        suite.addTest(ExpectedOutputCase('runTest', code, ir,
                                         output_filename_noext))


    for failure_filename in test_failures_filenames:
        input_file_path = os.path.join(input_test_dir, failure_filename)

        with open(input_file_path, "r") as ino_file:
            code = ino_file.read()

        suite.addTest(ExpectedFailureCase('runTest', code, failure_filename))

    for scanner_output_filename in scanner_output_filenames:
        output_filename_noext, _ext = os.path.splitext(scanner_output_filename)
        if output_filename_noext + ".ino" not in input_test_filenames:
            raise Exception(f"No input file for test '{scanner_output_filename}' found.")

        input_file_path = os.path.join(input_test_dir, output_filename_noext +
            ".ino")

        with open(input_file_path, "r") as ino_file:
            code = ino_file.read()

        output_file_path = os.path.join(output_test_dir, scanner_output_filename)

        with open(output_file_path, "r") as tok_file:
            tokens = tok_file.read()

        suite.addTest(ScannerOutputCase('runTest', code, tokens, output_filename_noext))

    return suite
