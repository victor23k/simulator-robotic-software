import unittest

from simulator.interpreter.preprocess.preprocessor import Preprocessor
from simulator.libraries.libs import LibraryManager


class TestPreprocessor(unittest.TestCase):

    def test_includes_internal_libraries(self):
        code = """
        #include <Servo.h>
        #include <Serial.h>
        """

        libraryManager = LibraryManager()
        preprocessor = Preprocessor(code)
        processed_code = preprocessor.process(libraryManager)

        self.assertEqual(processed_code.strip(), "")
        imported_libs = list(set([lib.get_name() for lib in libraryManager.get_available_libs()]))
        self.assertEqual(sorted(imported_libs), sorted(["Servo", "Serial", "String"]))
