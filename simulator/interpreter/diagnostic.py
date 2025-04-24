from dataclasses import dataclass

@dataclass
class Diagnostic:
    """
    Diagnostics about parsing errors with line and column information.
    """

    message: str
    line: int
    col_start: int
    col_end: int
