from __future__ import annotations

from typing import TYPE_CHECKING, override
from dataclasses import dataclass

if TYPE_CHECKING:
    from simulator.interpreter.ast.stmt import Stmt, VariableStmt
    from simulator.interpreter.sema.types import ArduinoType

from simulator.interpreter.environment import Environment, Value


@dataclass
class Function:
    """
    Function in the Arduino language.
    """

    params: list[VariableStmt]
    body: list[Stmt]
    closure: Environment

    def arity(self) -> int:
        "Returns the function's number of parameters"

        return len(self.params)

    def call(self, arguments: list[Value | None], _ret_type) -> Value | None:
        "Call the function and return."

        fn_env = Environment(self.closure)

        for param, arg in zip(self.params, arguments):
            fn_env.define(param.name.lexeme, arg)

        try:
            for stmt in self.body:
                stmt.execute(fn_env)
        except ReturnException as ret:
            return ret.value

        return None


class ReturnException(Exception):
    value: Value | None

    def __init__(self, ret_value: Value | None):
        super().__init__()
        self.value = ret_value


class LibFn:
    module: type
    fn_name: str
    fn_arity: int

    @override
    def __repr__(self) -> str:
        return f"LibFn(module={self.module}, fn_name={self.fn_name}, fn_arity={self.fn_arity})"

    def __init__(self, module: type, fn_name: str, fn_arity: int) -> None:
        self.module = module
        self.fn_name = fn_name
        self.fn_arity = fn_arity

    def call(self, arguments: list[Value], return_type: ArduinoType) -> Value | None:
        call_args = []
        for arg in arguments:
            arg_val = arg.value
            arg_val = arg_val.value if isinstance(arg_val, Value) else arg_val
            call_args.append(arg_val)

        if self.fn_name == "__init__":
            return Value(return_type, self.module(*call_args))

        method = getattr(self.module, self.fn_name)
        return Value(return_type, method(*call_args))

    def arity(self) -> int:
        return self.fn_arity
