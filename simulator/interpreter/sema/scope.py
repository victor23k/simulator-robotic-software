from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import override

from simulator.interpreter.diagnostic import Diagnostic, diagnostic_from_token
from simulator.interpreter.lex.token import Token
from simulator.interpreter.sema.types import (
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

    @override
    def __repr__(self) -> str:
        return f"Scope=({self.variables.__repr__()})"


class ScopeChain:
    scopes: deque[Scope]
    diagnostics: list[Diagnostic]

    def __init__(self, diagnostics: list[Diagnostic]):
        self.scopes = deque()
        self.scopes.append(Scope())
        self.diagnostics = diagnostics

    @override
    def __repr__(self) -> str:
        return f"ScopeChain=({self.scopes.__repr__()})"

    def __len__(self):
        return len(self.scopes)

    def __getitem__(self, index: int):
        return self.scopes[index]

    def _at_distance(self, distance: int) -> Scope:
        return self.scopes[-(distance + 1)]

    def begin_scope(self):
        self.scopes.append(Scope())

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name_token: Token, vtype: ArduinoType):
        var = Var(vtype, VarState.DECLARED)
        # if shadowing is not allowed, check all scopes.
        if self._at_distance(0).variables.get(name_token.lexeme) is not None:
            diag = diagnostic_from_token("Redeclaration of variable.", name_token)
            self.diagnostics.append(diag)
            return

        self._at_distance(0).variables[name_token.lexeme] = var

    def define(self, name_token: Token):
        for depth in range(0, len(self.scopes)):
            if self._at_distance(depth).variables.get(name_token.lexeme) is not None:
                self._at_distance(depth).variables[
                    name_token.lexeme
                ].state = VarState.DEFINED
                return

        diag = diagnostic_from_token("Variable defined before declaration", name_token)
        self.diagnostics.append(diag)

    def use(self, name_token: Token) -> int:
        for depth in range(0, len(self.scopes)):
            var = self._at_distance(depth).variables.get(name_token.lexeme)
            if var is not None:
                var.state = VarState.USED
                return depth

        diag = diagnostic_from_token("Variable used before declaration", name_token)
        self.diagnostics.append(diag)

        return 0

    def get_type(self, name_token: Token) -> ArduinoType:
        for depth in range(0, len(self.scopes)):
            var = self._at_distance(depth).variables.get(name_token.lexeme)
            if var is not None:
                return var.var_type

        return ArduinoBuiltinType.ERR

    def get_type_at(self, name_token: Token, depth: int) -> ArduinoType:
        var = self._at_distance(depth).variables.get(name_token.lexeme)
        if var is not None:
            return var.var_type

        return ArduinoBuiltinType.ERR
