import os
from typing import override
import unittest
import fnmatch
import re

from simulator.interpreter.runtime.classes import ArduinoInstance
from simulator.interpreter.lex.scanner import Scanner
from simulator.interpreter.report.diagnostic import printable_diagnostics
from simulator.interpreter.runtime.environment import Value
from simulator.interpreter.runtime.interpreter import Interpreter
from simulator.interpreter.sema.types import ArduinoBuiltinType, ArduinoObjType

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
                print(actual, key)
                return False
            if not match_structure(getattr(actual, key), val):
                print(getattr(actual, key))
                print(val)
                return False
        return True
    else:
        return spec is None or spec == actual


results_pattern = re.compile(
    r"^(?P<type>[A-Za-z_]+)\s+(?P<identifier>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<paren>\"?)(?P<value>.+)(?P=paren)$"
)


input_test_dir = "./tests/interpreter/expected/inputs/"
output_test_dir = "./tests/interpreter/expected/outputs/"
input_test_filenames = os.listdir(input_test_dir)
output_test_filenames = os.listdir(output_test_dir)
test_failures_filenames = [
    filename for filename in input_test_filenames if filename.rfind("_fails") != -1
]
scanner_output_filenames = [
    filename for filename in output_test_filenames if filename.rfind(".tok") != -1
]

input_test_filenames = set(input_test_filenames).difference(test_failures_filenames)


class ExpectedOutputCase(unittest.TestCase):
    def __init__(self, methodName, code="", ir="", filename="unknown"):
        super(ExpectedOutputCase, self).__init__(methodName)

        self.code: str = code
        self.ir: str = ir
        self.filename: str = filename

    @override
    def shortDescription(self) -> str | None:
        return f"Compare AST for sketch '{self.filename}'"

    def runTest(self):
        interpreter = Interpreter(self.code)
        interpreter.compile(None, None)
        stmts = interpreter.statements
        diags = interpreter.diagnostics

        spec_stmts: list[StmtSpec] = eval(self.ir)

        self.assertEqual(
            len(diags),
            0,
            f"No error diagnostics for {self.filename} expected but found: {printable_diagnostics(diags, self.code)}",
        )
        self.assertTrue(
            match_structure(stmts, spec_stmts), f"Match error for file '{self.filename}'"
        )


class ExpectedFailureCase(unittest.TestCase):
    def __init__(self, methodName, code="", filename="unknown"):
        super(ExpectedFailureCase, self).__init__(methodName)

        self.code: str = code
        self.filename: str = filename

    @override
    def shortDescription(self) -> str | None:
        return f"Expect faiilure for sketch '{self.filename}'"

    def runTest(self):
        interpreter = Interpreter(self.code)
        interpreter.compile(None, None)
        diags = interpreter.diagnostics

        self.assertNotEqual(
            len(diags),
            0,
            f"Expected some error diagnostics for {self.filename} but found none",
        )


class ScannerOutputCase(unittest.TestCase):
    def __init__(self, methodName, code="", tok="", filename="unknown"):
        super(ScannerOutputCase, self).__init__(methodName)

        self.code: str = code
        self.tok: str = tok
        self.filename: str = filename

    @override
    def shortDescription(self) -> str | None:
        return f"Compare scanner output for sketch '{self.filename}'"

    def runTest(self):
        scanner = Scanner(self.code)
        tokens = [token for token in scanner]
        spec_tokens: list[StmtSpec] = eval(self.tok)

        self.assertEqual(
            len(scanner.diagnostics),
            0,
            f"No error diagnostics for {self.filename} expected but found: {scanner.diagnostics}",
        )
        self.assertTrue(
            match_structure(tokens, spec_tokens), f"Match error for file '{self.filename}'"
        )


class InterpretCase(unittest.TestCase):
    def __init__(self, methodName, code="", expected="", filename="unknown"):
        super(InterpretCase, self).__init__(methodName)

        self.code: str = code
        self.expected_results: str = expected
        self.filename: str = filename

    @override
    def shortDescription(self) -> str | None:
        return f"Interpret sketch '{self.filename}'"

    def runTest(self):
        interpreter = Interpreter(self.code)
        interpreter.compile(None, None)
        interpreter.run_test()

        for line in self.expected_results.splitlines():
            matches = results_pattern.match(line)
            if matches:
                results = matches.groupdict()
                with self.subTest(f"{self.filename}: {line}"):
                    value = interpreter.environment.get(results["identifier"], 0)
                    self.assertIsInstance(value, Value)

                    if results["type"] in ArduinoBuiltinType.__members__:
                        expected_result_type = ArduinoBuiltinType[results["type"]]
                    else:
                        expected_result_type = ArduinoObjType(results["type"])

                    self.assertEqual(value.value_type, expected_result_type)

                    if isinstance(value.value, ArduinoInstance):
                        instance = value.value.instance
                        self.assertEqual(str(instance), results["value"])
                    else:
                        self.assertEqual(str(value.value), results["value"])


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    # Helper to check if test name matches -k pattern
    def matches_pattern(test_name):
        if not loader.testNamePatterns:
            return True
        return fnmatch.fnmatchcase(test_name, loader.testNamePatterns[0])

    # Expected output and interpreter tests
    for input_filename in input_test_filenames:
        input_file_path = os.path.join(input_test_dir, input_filename)
        with open(input_file_path, "r") as ino_file:
            code = ino_file.read()

        code, *results = re.split(r"^>>>>*$", code, maxsplit=1, flags=re.MULTILINE)

        output_filename_noext, _ext = os.path.splitext(input_filename)
        if output_filename_noext + ".ir" in output_test_filenames:
            output_file_path = os.path.join(
                output_test_dir, output_filename_noext + ".ir"
            )
            with open(output_file_path, "r") as ir_file:
                ir = ir_file.read()

            test_name = f"ExpectedOutputCase.{output_filename_noext}"
            if matches_pattern(test_name):
                suite.addTest(
                    ExpectedOutputCase("runTest", code, ir, output_filename_noext)
                )

        if len(results) == 1:
            test_name = f"InterpretCase.{output_filename_noext}"
            if matches_pattern(test_name):
                suite.addTest(
                    InterpretCase("runTest", code, results[0], output_filename_noext)
                )

    # Expected failure tests
    for failure_filename in test_failures_filenames:
        input_file_path = os.path.join(input_test_dir, failure_filename)
        with open(input_file_path, "r") as ino_file:
            code = ino_file.read()

        code, *results = re.split(r"^>>>>*$", code, maxsplit=1, flags=re.MULTILINE)

        test_name = f"ExpectedFailureCase.{failure_filename}"
        if matches_pattern(test_name):
            suite.addTest(ExpectedFailureCase("runTest", code, failure_filename))

    # Scanner output tests
    for scanner_output_filename in scanner_output_filenames:
        output_filename_noext, _ext = os.path.splitext(scanner_output_filename)
        if output_filename_noext + ".ino" not in input_test_filenames:
            raise Exception(
                f"No input file for test '{scanner_output_filename}' found."
            )

        input_file_path = os.path.join(input_test_dir, output_filename_noext + ".ino")
        with open(input_file_path, "r") as ino_file:
            code = ino_file.read()

        code, *results = re.split(r"^>>>>*$", code, maxsplit=1, flags=re.MULTILINE)

        output_file_path = os.path.join(output_test_dir, scanner_output_filename)
        with open(output_file_path, "r") as tok_file:
            tokens = tok_file.read()

        test_name = f"ScannerOutputCase.{output_filename_noext}"
        if matches_pattern(test_name):
            suite.addTest(
                ScannerOutputCase("runTest", code, tokens, output_filename_noext)
            )

    return suite
