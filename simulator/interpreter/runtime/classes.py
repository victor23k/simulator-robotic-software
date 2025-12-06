from __future__ import annotations

from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from simulator.interpreter.lex.token import Token

from simulator.interpreter.environment import Value
from simulator.interpreter.sema.types import ArduinoType
from simulator.interpreter.runtime.functions import LibFn


class ArduinoClass:
    name: str
    python_class: type
    methods: dict[str, Value]
    constructor_arity: int
    constructor_params: list[str]

    def __init__(
        self, python_class: type, name: str, methods: dict[str, Value], params
    ) -> None:
        self.python_class = python_class
        self.name = name
        self.methods = methods
        self.constructor_arity = len(params)
        self.constructor_params = params

    def arity(self):
        return self.constructor_arity

    def call(self, arguments: list[Value], return_type: ArduinoType) -> ArduinoInstance:
        constructor = LibFn(self.python_class, "__init__", self.constructor_arity)
        obj = constructor.call(list(arguments), return_type)
        return ArduinoInstance(self, obj)

    def find_method(self, method_name: str) -> Value:
        return self.methods[method_name]

    @override
    def __repr__(self) -> str:
        return f"ArduinoClass: name={self.name}, python_class={self.python_class}, constructor_arity={self.constructor_arity}, constructor_params={self.constructor_params}"


class ArduinoInstance:
    klass: ArduinoClass
    value: Value
    fields: dict[str, Value]

    def __init__(self, klass: ArduinoClass, value: Value):
        self.klass = klass
        self.fields = dict()
        self.value = value

    @override
    def __repr__(self) -> str:
        return f"ArduinoInstance(klass={self.klass}, value={self.value})"

    def get(self, name: Token) -> Value:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        else:
            method = self.klass.find_method(name.lexeme)
            return Value(
                method.value_type,
                LibFn(self.value.value, name.lexeme, method.value.arity()),
            )

    def set(self, name: Token, value: Value):
        self.fields[name.lexeme] = value
