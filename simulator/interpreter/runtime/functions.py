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

    def arity(self) -> range:
        "Returns the function's number of parameters"

        return range(len(self.params), len(self.params) + 1)

    def call(
        self, arguments: list[Value | None], _ret_type, debug: bool = False, *extra_args
    ) -> Value | None:
        "Call the function and return."

        fn_env = Environment(self.closure)

        for param, arg in zip(self.params, arguments):
            fn_env.define(param.name.lexeme, arg)

        try:
            for stmt in self.body:
                if debug:
                    stmt.debug(fn_env, *extra_args)
                else:
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
    module: type | object
    fn_name: str
    fn_arity: range

    @override
    def __repr__(self) -> str:
        return f"LibFn(module={self.module}, fn_name={self.fn_name}, fn_arity={self.fn_arity})"

    def __init__(self, module: type, fn_name: str, fn_arity: range) -> None:
        self.module = module
        self.fn_name = fn_name
        self.fn_arity = fn_arity

    def call(
        self,
        arguments: list[Value],
        return_type: ArduinoType,
        _debug: bool = False,
        *_extra_args,
    ) -> Value | None:
        call_args = []
        for arg in arguments:
            arg_val = arg.value
            # Checking the ArduinoInstance type with isinstance would cause a circular import
            if hasattr(arg_val, "instance"):
                arg_val = arg_val.instance
            call_args.append(arg_val)

        if self.fn_name == "__init__":
            return Value(return_type, self.module(*call_args))

        method = getattr(self.module, self.fn_name)
        return Value(return_type, method(*call_args))

    def arity(self) -> range:
        return self.fn_arity
