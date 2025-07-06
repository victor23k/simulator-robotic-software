from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum

from simulator.interpreter.diagnostic import Diagnostic, diagnostic_from_token
from simulator.interpreter.token import Token
from simulator.interpreter.types import (
    ArduinoBuiltinType,
    ArduinoType,
    token_to_arduino_type,
)

class VarState(Enum):
    DECLARED = 1
    DEFINED = 2
    USED = 3


@dataclass
class Var:
    """
    The entity that represents a variable inside a Scope. It has a type and a
    state, which can be one of:

        - Declared
        - Defined
        - Used
    """

    var_type: ArduinoType
    state: VarState


class Scope:
    """
    A scope defines a region where a name maps to a certain entity (Cratfing
    Interpreters, Robert Nystrom).

    In this intepreter, the entity is Var, that contains the type and state of
    the variable.
    """

    variables: dict[str, Var]

    def __init__(self):
        self.variables = {}

class ScopeChain:
    scopes: deque[Scope]
    diagnostics: list[Diagnostic]

    def __init__(self, diagnostics: list[Diagnostic]):
        self.scopes = deque()
        self.scopes.append(Scope())
        self.diagnostics = diagnostics

    def __len__(self):
        return len(self.scopes)

    def __getitem__(self, index: int):
        return self.scopes[index]

    def begin_scope(self):
        self.scopes.append(Scope())

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name_token: Token, vtype: ArduinoType):
        var = Var(vtype, VarState.DECLARED)
        # if shadowing is not allowed, check all scopes.
        if self.scopes[-1].variables.get(name_token.lexeme) is not None:
            diag = diagnostic_from_token("Redeclaration of variable.",
                                         name_token)
            self.diagnostics.append(diag)
            return

        self.scopes[-1].variables[name_token.lexeme] = var

    def define(self, name_token: Token):
        for depth in range(len(self.scopes), 0, -1):
            depth -= 1
            if self.scopes[depth].variables.get(name_token.lexeme) is not None:
                self.scopes[depth].variables[name_token.lexeme].state = VarState.DEFINED
                return

        diag = diagnostic_from_token("Variable defined before declaration", name_token)
        self.diagnostics.append(diag)

    def use(self, name_token: Token) -> int:
        for depth in range(len(self.scopes), 0, -1):
            depth -= 1
            var = self.scopes[depth].variables.get(name_token.lexeme)
            if var is not None:
                var.state = VarState.USED
                return len(self.scopes) - 1 - depth

        diag = diagnostic_from_token("Variable used before declaration",
                                     name_token)
        self.diagnostics.append(diag)

        return 0


    def get_type(self, name_token: Token) -> ArduinoType:
        var = self.scopes[-1].variables.get(name_token.lexeme)
        if var is not None:
            return var.var_type

        return ArduinoBuiltinType.ERR

