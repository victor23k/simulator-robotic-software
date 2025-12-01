import re

from simulator.libraries.libs import LibraryManager


class Preprocessor:
    """
    Preprocesses an Arduino sketch by including header files.
    """

    code: str

    def __init__(self, code: str):
        self.code = code

    def process(self, libraryManager: LibraryManager):
        internal_libraries_regex = re.compile(
            r"^\s*#include\s*<([\w\/\.-]+\.h)>\s*$", re.MULTILINE
        )
        external_libraries_regex = re.compile(
            r"^\s*#include\s*\"([\w\/\.-]+\.h)\"\s*$", re.MULTILINE
        )

        internal_libraries: list[str] = re.findall(internal_libraries_regex, self.code)
        external_libraries: list[str] = re.findall(external_libraries_regex, self.code)
        self.code = re.sub(internal_libraries_regex, "", self.code)
        self.code = re.sub(external_libraries_regex, "", self.code)

        for lib in internal_libraries + external_libraries:
            libraryManager.add_library(lib)

        return self.code
