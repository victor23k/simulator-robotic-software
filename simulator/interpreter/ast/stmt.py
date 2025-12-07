from __future__ import annotations

from typing import TYPE_CHECKING, override
from dataclasses import dataclass

if TYPE_CHECKING:
    import simulator.interpreter.ast.expr as expr

from simulator.interpreter.runtime.classes import ArduinoClass
from simulator.interpreter.sema.resolver import (
    ControlFlowState,
    FunctionState,
    FunctionType,
)
import simulator.interpreter.sema.scope as scope
from simulator.interpreter.runtime.functions import Function, LibFn, ReturnException
from simulator.interpreter.diagnostic import ArduinoRuntimeError, Diagnostic, diagnostic_from_token
from simulator.interpreter.environment import Environment, Value
from simulator.interpreter.lex.token import Token, TokenType
from simulator.interpreter.sema.types import (
    ArduinoArray,
    ArduinoBuiltinType,
    ArduinoObjType,
    ArduinoType,
    coerce_types,
    token_to_arduino_type,
    type_from_specifier_list,
    types_compatibility,
)

type Stmt = (
    ArrayDeclStmt
    | BlockStmt
    | ExpressionStmt
    | FunctionStmt
    | ReturnStmt
    | DeclarationListStmt
    | VariableStmt
    | IfStmt
    | BreakStmt
    | ContinueStmt
    | SwitchStmt
    | CaseStmt
    | WhileStmt
    | DoWhileStmt
    | ForStmt
)


@dataclass
class BlockStmt:
    stmts: list[Stmt]

    def execute(self, env: Environment):
        block_env = Environment(enclosing=env)

        for stmt in self.stmts:
            stmt.execute(block_env)

        del block_env

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        scope_chain.begin_scope()

        for stmt in self.stmts:
            stmt.resolve(scope_chain, diagnostics, fn_type, breakable)

        scope_chain.end_scope()

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += f"{' ' * (ntab + 2)}stmts=[\n"
        result += ",\n".join([stmt.to_string(ntab + 4) for stmt in self.stmts])
        result += f"{' ' * (ntab + 2)}],\n"

        result += f"{' ' * ntab})\n"
        return result


@dataclass
class ExpressionStmt:
    expr: expr.Expr

    def execute(self, env: Environment):
        self.expr.evaluate(env)

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        _fn_type: FunctionType,
        _breakable: ControlFlowState,
    ):
        self.expr.resolve(scope_chain, diagnostics)

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.expr.to_string(ntab + 2, "expr") + "\n"
        result += f"{' ' * ntab})\n"
        return result


@dataclass
class ReturnStmt:
    expr: expr.Expr
    ttype: ArduinoType

    def execute(self, env: Environment):
        value = self.expr.evaluate(env)
        raise ReturnException(value)

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        _breakable: ControlFlowState,
    ):
        self.expr.resolve(scope_chain, diagnostics)
        self.ttype = self.expr.ttype

        if (
            fn_type.fn_state is FunctionState.FUNCTION
            and fn_type.return_type != self.ttype
        ):
            diag = self.expr.gen_diagnostic(
                f"Function type '{fn_type.return_type}' and actual return type '{self.ttype}' are incompatible",
            )
            diagnostics.append(diag)

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.expr.to_string(ntab + 2, "expr")

        if self.ttype is not None:
            result += ",\n" + f"{' ' * (ntab + 2)}ttype={self.ttype}"

        result += f"{' ' * ntab})"
        return result


@dataclass
class BreakStmt:
    brk: Token

    def execute(self, _env: Environment):
        raise BreakException()

    def resolve(
        self,
        _scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        _fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        if breakable not in [ControlFlowState.LOOP, ControlFlowState.SWITCH]:
            diag = diagnostic_from_token(
                "Break statement outside of a loop or switch", self.brk
            )
            diagnostics.append(diag)

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="
        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}()\n"
        return result


@dataclass
class ContinueStmt:
    cont: Token

    def execute(self, _env: Environment):
        raise ContinueException()

    def resolve(
        self,
        _scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        _fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        if breakable is not ControlFlowState.LOOP:
            diag = diagnostic_from_token(
                "Continue statement outside of a loop.", self.cont
            )
            diagnostics.append(diag)

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="
        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}()\n"
        return result


@dataclass
class DeclarationListStmt:
    declarations: list[VariableStmt]

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += f"{' ' * (ntab + 2)}declarations=[\n"
        result += ",\n".join([decl.to_string(ntab + 4) for decl in self.declarations])
        result += f"{' ' * (ntab + 2)}],\n"
        result += f"{' ' * ntab})\n"
        return result

    def execute(self, environment: Environment):
        for decl in self.declarations:
            decl.execute(environment)

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        for decl in self.declarations:
            decl.resolve(scope_chain, diagnostics, fn_type, breakable)


class ArrayDeclStmt:
    const: bool
    dimensions: list[expr.Expr | None]
    array_type: Token
    name: Token
    initializer: expr.Expr | None
    ttype: ArduinoType

    def __init__(
        self,
        specifiers: list[Token],
        dimensions: list[expr.Expr | None],
        name: Token,
        initializer: expr.Expr | None,
    ):
        self.dimensions = dimensions
        self.array_type = type_from_specifier_list(specifiers)
        self.const = TokenType.CONST in [spec.token for spec in specifiers]
        self.name = name
        self.initializer = initializer
        self.ttype = None

    @override
    def __repr__(self) -> str:
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += ",\n" + f"{' ' * (ntab + 2)}array_type={self.array_type}"
        result += ",\n" + self.name.to_string(ntab + 2, "name")
        result += ",\n".join([dim.to_string(ntab + 4) for dim in self.dimensions])

        if self.initializer is not None:
            result += ",\n" + self.initializer.to_string(ntab + 2, "initializer")

        if self.ttype is not None:
            result += ",\n" + f"{' ' * (ntab + 2)}ttype={self.ttype}"

        result += f"{' ' * ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

    def execute(self, environment: Environment):
        init_value = None
        dimensions = []
        for dimension in self.dimensions:
            if dimension is not None:
                dimensions.append(dimension.evaluate(environment))
            else:
                dimensions.append(None)

        if self.initializer is not None and self.initializer.ttype is not None:
            init_value = self.initializer.evaluate(environment)
            if (
                init_value
                and isinstance(init_value, Value)
                and init_value.value_type is not self.ttype
            ):
                init_value.coerce(self.ttype)
            if (
                self.ttype == ArduinoArray(ArduinoBuiltinType.CHAR)
                and dimensions[0] is not None
                and (offset := dimensions[0].value - len(init_value.value)) > 0
            ):
                init_value.value.extend([None] * offset)

        else:

            def init_array(dimensions, value=None):
                if len(dimensions) == 1:
                    return [value] * dimensions[0].value
                return [
                    init_array(dimensions[1:], value)
                    for _ in range(dimensions[0].value)
                ]

            init_value = Value(self.ttype, init_array(dimensions))

        environment.define(self.name.lexeme, init_value)

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        _fn_type: FunctionType,
        _breakable: ControlFlowState,
    ):
        if self.initializer:
            self.initializer.resolve(scope_chain, diagnostics)

        self.ttype = self._compute_type(scope_chain, diagnostics)
        scope_chain.declare(self.name, self.ttype)

        if self.initializer:
            scope_chain.define(self.name)

        if self.const:
            scope_chain.non_modifiable(self.name)

    def _compute_type(
        self, _scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]
    ) -> ArduinoType:
        var_arduino_type = token_to_arduino_type(self.array_type)

        for _dim in self.dimensions:
            var_arduino_type = ArduinoArray(var_arduino_type)

        if not self.initializer:
            return var_arduino_type

        if self.initializer and types_compatibility(
            var_arduino_type, self.initializer.ttype
        ):
            return var_arduino_type

        diag = self.gen_diagnostic(
            "Initializer expression has incompatible types. Initializer: "
            + f"{self.initializer.ttype}. Array: {var_arduino_type}"
        )
        diagnostics.append(diag)
        return ArduinoBuiltinType.ERR


class VariableStmt:
    const: bool
    var_type: Token
    name: Token
    initializer: expr.Expr | None
    ttype: ArduinoType

    def __init__(
        self,
        specifiers: list[Token],
        ident: Token,
        initializer: expr.Expr | None = None,
    ):
        self.name = ident
        self.initializer = initializer
        self.var_type = type_from_specifier_list(specifiers)
        self.const = TokenType.CONST in [spec.token for spec in specifiers]
        self.ttype = None

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += ",\n" + f"{' ' * (ntab + 2)}var_type={self.var_type}"
        result += ",\n" + self.name.to_string(ntab + 2, "name")

        if self.initializer is not None:
            result += ",\n" + self.initializer.to_string(ntab + 2, "initializer")

        if self.ttype is not None:
            result += ",\n" + f"{' ' * (ntab + 2)}ttype={self.ttype}"

        result += f"{' ' * ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

    def execute(self, environment: Environment):
        init_value = None
        if self.initializer is None and isinstance(self.ttype, ArduinoObjType):
            if (fn := environment.get(self.ttype.classname, 0)) is None:
                raise ArduinoRuntimeError("Trying to initialize an object without default constructor or outside of top level scope.")
            elif isinstance(fn.value, ArduinoClass):
                init_value = fn.value.call([], self.ttype)
                init_value = Value(self.ttype, init_value)
            else:
                init_value = None

            environment.define(self.name.lexeme, init_value)

        elif self.initializer is not None and self.initializer.ttype is not None:
            init_value = self.initializer.evaluate(environment)
            if init_value:
                init_value.coerce(self.ttype)

            environment.define(self.name.lexeme, init_value)
        else:
            environment.define(self.name.lexeme, None)

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        _fn_type: FunctionType,
        _breakable: ControlFlowState,
    ):
        if self.initializer:
            self.initializer.resolve(scope_chain, diagnostics)

        self.ttype = self._compute_type(scope_chain, diagnostics)
        scope_chain.declare(self.name, self.ttype)

        if self.initializer:
            scope_chain.define(self.name)

        if self.const:
            scope_chain.non_modifiable(self.name)

    def _compute_type(
        self, _scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]
    ) -> ArduinoType:
        var_arduino_type = token_to_arduino_type(self.var_type)

        if not self.initializer:
            return var_arduino_type

        if self.initializer and types_compatibility(
            var_arduino_type, self.initializer.ttype
        ):
            return var_arduino_type

        diag = self.gen_diagnostic(
            "Initializer expression has incompatible types. Initializer: "
            + f"{self.initializer.ttype}. Variable: {var_arduino_type}"
        )
        diagnostics.append(diag)
        return ArduinoBuiltinType.ERR


@dataclass
class IfStmt:
    condition: expr.Expr
    then_branch: Stmt
    else_branch: Stmt | None

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += "\n" + self.condition.to_string(ntab + 2, "condition")
        result += ",\n" + self.then_branch.to_string(ntab + 2, "then_branch")

        if self.else_branch is not None:
            result += ",\n" + self.else_branch.to_string(ntab + 2, "else_branch")

        result += f"{' ' * ntab})\n"
        return result

    def execute(self, environment: Environment):
        condition_value = self.condition.evaluate(environment)
        if (
            isinstance(condition_value, Value)
            and condition_value.value_type == ArduinoBuiltinType.BOOL
            and condition_value.value
        ):
            self.then_branch.execute(environment)
        elif self.else_branch is not None:
            self.else_branch.execute(environment)

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        self.condition.resolve(scope_chain, diagnostics)
        self.then_branch.resolve(scope_chain, diagnostics, fn_type, breakable)
        if self.else_branch is not None:
            self.else_branch.resolve(scope_chain, diagnostics, fn_type, breakable)


class FunctionStmt:
    name: Token
    params: list[VariableStmt]
    body: list[Stmt]
    return_type: Token
    ttype: ArduinoType

    def __init__(
        self,
        name: Token,
        params: list[VariableStmt],
        body: list[Stmt],
        specifiers: list[Token],
    ):
        self.name = name
        self.params = params
        self.body = body
        self.return_type = type_from_specifier_list(specifiers)
        self.ttype = None

    def execute(self, env: Environment):
        fn = Function(self.params, self.body, env)
        env.define(self.name.lexeme, Value(self.ttype, fn))

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        scope_chain.begin_scope()

        self.ttype = token_to_arduino_type(self.return_type)
        fn_type = FunctionType()
        fn_type.fn_state = FunctionState.FUNCTION
        fn_type.return_type = self.ttype

        for param in self.params:
            param.resolve(scope_chain, diagnostics, fn_type, breakable)
        for stmt in self.body:
            stmt.resolve(scope_chain, diagnostics, fn_type, breakable)

        scope_chain.end_scope()

        scope_chain.declare(self.name, self.ttype)

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += "\n" + self.name.to_string(ntab + 2, "name")

        result += f"{' ' * (ntab + 2)}params=["
        result += ",\n".join([param.to_string(ntab + 4) for param in self.params])
        result += f"{' ' * (ntab + 2)}],\n"

        result += f"{' ' * (ntab + 2)}body=[\n"
        result += ",\n".join([stmt.to_string(ntab + 4) for stmt in self.body])
        result += f"{' ' * (ntab + 2)}],\n"
        result += self.return_type.to_string(ntab + 2, "return_type")

        if self.ttype is not None:
            result += ",\n" + f"{' ' * (ntab + 2)}ttype={self.ttype}"

        result += f"{' ' * ntab})\n"
        return result


@dataclass
class CaseStmt:
    label: expr.LiteralExpr | expr.VariableExpr
    stmts: list[Stmt]

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += "\n" + self.label.to_string(ntab + 2, "label")
        result += f"{' ' * (ntab + 2)}stmts=[\n"
        result += ",\n".join([stmt.to_string(ntab + 4) for stmt in self.stmts])
        result += f"{' ' * (ntab + 2)}],\n"
        result += f"{' ' * ntab})"
        return result

    def execute(self, environment: Environment):
        for stmt in self.stmts:
            stmt.execute(environment)

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        self.label.resolve(scope_chain, diagnostics)
        for stmt in self.stmts:
            stmt.resolve(scope_chain, diagnostics, fn_type, breakable)


@dataclass
class DefaultStmt:
    stmts: list[Stmt]

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += f"{' ' * (ntab + 2)}stmts=[\n"
        result += ",\n".join([stmt.to_string(ntab + 4) for stmt in self.stmts])
        result += f"{' ' * (ntab + 2)}],\n"
        result += f"{' ' * ntab})\n"
        return result

    def execute(self, environment: Environment):
        for stmt in self.stmts:
            stmt.execute(environment)

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        for stmt in self.stmts:
            stmt.resolve(scope_chain, diagnostics, fn_type, breakable)


@dataclass
class SwitchStmt:
    var: expr.LiteralExpr | expr.VariableExpr
    cases: list[CaseStmt]
    default: DefaultStmt | None

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += "\n" + self.var.to_string(ntab + 2, "var")
        result += f"{' ' * (ntab + 2)}cases=[\n"
        result += ",\n".join([case.to_string(ntab + 4) for case in self.cases])
        result += f"{' ' * (ntab + 2)}],\n"
        result += f"{' ' * ntab})\n"
        return result

    def execute(self, environment: Environment):
        var = self.var.evaluate(environment)

        matching_case_idx = next(
            (
                idx
                for (idx, case) in enumerate(self.cases)
                if case.label.evaluate(environment) == var
            ),
            None,
        )

        try:
            if matching_case_idx is None and self.default is not None:
                self.default.execute(environment)
            else:
                for case in self.cases[matching_case_idx:]:
                    for stmt in case.stmts:
                        stmt.execute(environment)

        except BreakException:
            pass

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        self.var.resolve(scope_chain, diagnostics)
        if breakable is ControlFlowState.NONE:
            breakable = ControlFlowState.SWITCH

        for case in self.cases:
            case.resolve(scope_chain, diagnostics, fn_type, breakable)
        if self.default is not None:
            self.default.resolve(scope_chain, diagnostics, fn_type, breakable)


@dataclass
class WhileStmt:
    condition: expr.Expr
    statement: Stmt

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += "\n" + self.condition.to_string(ntab + 2, "condition")
        result += "\n" + self.statement.to_string(ntab + 2, "statement")
        result += f"{' ' * ntab})\n"
        return result

    def execute(self, environment: Environment):
        try:
            while (condition := self.condition.evaluate(environment)) and (
                (condition.value_type is ArduinoBuiltinType.BOOL and condition.value)
                or condition.value != 0
            ):
                try:
                    self.statement.execute(environment)
                except ContinueException:
                    continue

        except BreakException:
            pass

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        _breakable: ControlFlowState,
    ):
        self.condition.resolve(scope_chain, diagnostics)
        self.statement.resolve(scope_chain, diagnostics, fn_type, ControlFlowState.LOOP)


@dataclass
class DoWhileStmt:
    statement: Stmt
    condition: expr.Expr

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += "\n" + self.statement.to_string(ntab + 2, "statement")
        result += "\n" + self.condition.to_string(ntab + 2, "condition")
        result += f"{' ' * ntab})\n"
        return result

    def execute(self, environment: Environment):
        try:
            self.statement.execute(environment)
            while (condition := self.condition.evaluate(environment)) and (
                (condition.value_type is ArduinoBuiltinType.BOOL and condition.value)
                or condition.value != 0
            ):
                try:
                    self.statement.execute(environment)
                except ContinueException:
                    continue

        except BreakException:
            pass

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        _breakable: ControlFlowState,
    ):
        self.statement.resolve(scope_chain, diagnostics, fn_type, ControlFlowState.LOOP)
        self.condition.resolve(scope_chain, diagnostics)


@dataclass
class ForStmt:
    init_expr: expr.Expr | VariableStmt | None
    condition: expr.Expr | None
    loop_expr: expr.Expr | None
    statement: Stmt

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        if self.init_expr is not None:
            result += "\n" + self.init_expr.to_string(ntab + 2, "init_expr")
        if self.condition is not None:
            result += "\n" + self.condition.to_string(ntab + 2, "condition")
        if self.loop_expr is not None:
            result += "\n" + self.loop_expr.to_string(ntab + 2, "loop_expr")
        result += "\n" + self.statement.to_string(ntab + 2, "statement")
        result += f"{' ' * ntab})\n"
        return result

    def execute(self, environment: Environment):
        if isinstance(self.init_expr, VariableStmt):
            self.init_expr.execute(environment)
        elif self.init_expr is not None:
            self.init_expr.evaluate(environment)

        try:
            if self.condition is None:
                self._infinite_loop(environment)
            else:
                condition = self.condition.evaluate(environment)

                while (condition := self.condition.evaluate(environment)) and (
                    (
                        condition.value_type is ArduinoBuiltinType.BOOL
                        and condition.value
                    )
                    or condition.value != 0
                ):
                    try:
                        self.statement.execute(environment)
                        if self.loop_expr is not None:
                            self.loop_expr.evaluate(environment)
                    except ContinueException:
                        if self.loop_expr is not None:
                            self.loop_expr.evaluate(environment)
                        continue

        except BreakException:
            pass

    def _infinite_loop(self, environment: Environment):
        while True:
            try:
                self.statement.execute(environment)
            except ContinueException:
                continue

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        if isinstance(self.init_expr, VariableStmt):
            self.init_expr.resolve(scope_chain, diagnostics, fn_type, breakable)
        elif self.init_expr is not None:
            self.init_expr.resolve(scope_chain, diagnostics)
        if self.condition is not None:
            self.condition.resolve(scope_chain, diagnostics)
        if self.loop_expr is not None:
            self.loop_expr.resolve(scope_chain, diagnostics)

        self.statement.resolve(scope_chain, diagnostics, fn_type, ControlFlowState.LOOP)


class BreakException(Exception):
    pass


class ContinueException(Exception):
    pass
