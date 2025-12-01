import unittest

from simulator.interpreter.preprocessor import Preprocessor
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
        self.assertEqual(libraryManager.get_available_libs(), ["Servo", "Serial"])
