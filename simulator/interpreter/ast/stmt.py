from __future__ import annotations

from typing import TYPE_CHECKING, override
from dataclasses import dataclass

if TYPE_CHECKING:
    import simulator.interpreter.ast.expr as expr

from simulator.interpreter.debugger.adb import Action, DebugState
from simulator.interpreter.runtime.classes import ArduinoClass
from simulator.interpreter.sema.resolver import (
    ControlFlowState,
    FunctionState,
    FunctionType,
)
import simulator.interpreter.sema.scope as scope
from simulator.interpreter.runtime.functions import Function, ReturnException
from simulator.interpreter.diagnostic import (
    ArduinoRuntimeError,
    Diagnostic,
    diagnostic_from_token,
)
from simulator.interpreter.environment import Environment, Value
from simulator.interpreter.lex.token import Token, TokenType
from simulator.interpreter.sema.types import (
    ArduinoArray,
    ArduinoBuiltinType,
    ArduinoObjType,
    ArduinoType,
    token_to_arduino_type,
    type_from_specifier_list,
    types_compatibility,
)


class Stmt:
    def __init__(self) -> None:
        pass

    def run(
        self,
        env: Environment,
        stmt_exec_fn: str = "execute",
        expr_eval_fn: str = "evaluate",
        *eval_args,
    ) -> Value | None:
        """
        Evaluation wrapper.
        """

        pass

    def to_string(self, ntab: int, name: str = "") -> str:
        return ""

    def debug(self, env: Environment, dbg_state: DebugState) -> Value | None:
        dbg_state.current_node = self

        match dbg_state.action:
            case Action.STEP | Action.NEXT:
                dbg_state.lock.release()
            case _:
                pass

        self.run(env, "debug", "debug", dbg_state)

    def execute(self, env: Environment):
        self.run(env)


def evaluate(expr, expr_eval_fn, env, *eval_args):
    expr_eval = getattr(expr, expr_eval_fn)
    value = expr_eval(env, *eval_args)
    return value


def execute(stmt, stmt_exec_fn, env, *eval_args):
    stmt_exec = getattr(stmt, stmt_exec_fn)
    stmt_exec(env, *eval_args)


@dataclass
class BlockStmt(Stmt):
    stmts: list[Stmt]

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        block_env = Environment(enclosing=env)

        for stmt in self.stmts:
            execute(stmt, stmt_exec_fn, block_env, *eval_args)

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

    @override
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
class ExpressionStmt(Stmt):
    expr: expr.Expr

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        evaluate(self.expr, expr_eval_fn, env, *eval_args)

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

    @override
    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.expr.to_string(ntab + 2, "expr") + "\n"
        result += f"{' ' * ntab})\n"
        return result


@dataclass
class ReturnStmt(Stmt):
    expr: expr.Expr
    ttype: ArduinoType

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        value = evaluate(self.expr, expr_eval_fn, env, *eval_args)

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

    @override
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
class BreakStmt(Stmt):
    brk: Token

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
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

    @override
    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="
        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}()\n"
        return result


@dataclass
class ContinueStmt(Stmt):
    cont: Token

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
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

    @override
    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="
        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}()\n"
        return result


@dataclass
class DeclarationListStmt(Stmt):
    declarations: list[VariableStmt]

    @override
    def __repr__(self):
        return self.to_string()

    @override
    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += f"{' ' * (ntab + 2)}declarations=[\n"
        result += ",\n".join([decl.to_string(ntab + 4) for decl in self.declarations])
        result += f"{' ' * (ntab + 2)}],\n"
        result += f"{' ' * ntab})\n"
        return result

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        for decl in self.declarations:
            execute(decl, stmt_exec_fn, env, *eval_args)

    def resolve(
        self,
        scope_chain: scope.ScopeChain,
        diagnostics: list[Diagnostic],
        fn_type: FunctionType,
        breakable: ControlFlowState,
    ):
        for decl in self.declarations:
            decl.resolve(scope_chain, diagnostics, fn_type, breakable)


class ArrayDeclStmt(Stmt):
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

    @override
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

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        init_value = None
        dimensions = []
        for dimension in self.dimensions:
            if dimension is not None:
                dimensions.append(evaluate(dimension, expr_eval_fn, env, *eval_args))
            else:
                dimensions.append(None)

        if self.initializer is not None and self.initializer.ttype is not None:
            init_value = evaluate(self.initializer, expr_eval_fn, env, *eval_args)
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

        env.define(self.name.lexeme, init_value)

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


class VariableStmt(Stmt):
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

    @override
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

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        init_value = None
        if self.initializer is None and isinstance(self.ttype, ArduinoObjType):
            if (fn := env.get(self.ttype.classname, 0)) is None:
                raise ArduinoRuntimeError(
                    "Trying to initialize an object without default constructor or outside of top level scope."
                )
            elif isinstance(fn.value, ArduinoClass):
                init_value = fn.value.call([], self.ttype)
                init_value = Value(self.ttype, init_value)
            else:
                init_value = None

            env.define(self.name.lexeme, init_value)

        elif self.initializer is not None and self.initializer.ttype is not None:
            init_value = evaluate(self.initializer, expr_eval_fn, env, *eval_args)
            if init_value:
                init_value.coerce(self.ttype)

            env.define(self.name.lexeme, init_value)
        else:
            env.define(self.name.lexeme, None)

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
class IfStmt(Stmt):
    condition: expr.Expr
    then_branch: Stmt
    else_branch: Stmt | None

    @override
    def __repr__(self):
        return self.to_string()

    @override
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

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        condition_value = evaluate(self.condition, expr_eval_fn, env, *eval_args)
        if (
            isinstance(condition_value, Value)
            and condition_value.value_type == ArduinoBuiltinType.BOOL
            and condition_value.value
        ):
            execute(self.then_branch, stmt_exec_fn, env, *eval_args)
        elif self.else_branch is not None:
            execute(self.else_branch, stmt_exec_fn, env, *eval_args)

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


class FunctionStmt(Stmt):
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

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
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

    @override
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
class CaseStmt(Stmt):
    label: expr.LiteralExpr | expr.VariableExpr
    stmts: list[Stmt]

    @override
    def __repr__(self):
        return self.to_string()

    @override
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

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        for stmt in self.stmts:
            execute(stmt, stmt_exec_fn, env, *eval_args)

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
class DefaultStmt(Stmt):
    stmts: list[Stmt]

    @override
    def __repr__(self):
        return self.to_string()

    @override
    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += f"{' ' * (ntab + 2)}stmts=[\n"
        result += ",\n".join([stmt.to_string(ntab + 4) for stmt in self.stmts])
        result += f"{' ' * (ntab + 2)}],\n"
        result += f"{' ' * ntab})\n"
        return result

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        for stmt in self.stmts:
            execute(stmt, stmt_exec_fn, env, *eval_args)

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
class SwitchStmt(Stmt):
    var: expr.LiteralExpr | expr.VariableExpr
    cases: list[CaseStmt]
    default: DefaultStmt | None

    @override
    def __repr__(self):
        return self.to_string()

    @override
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

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        var = evaluate(self.var, expr_eval_fn, env, *eval_args)

        matching_case_idx = next(
            (
                idx
                for (idx, case) in enumerate(self.cases)
                if evaluate(case.label, expr_eval_fn, env, *eval_args) == var
            ),
            None,
        )

        try:
            if matching_case_idx is None and self.default is not None:
                execute(self.default, stmt_exec_fn, env, *eval_args)
            else:
                for case in self.cases[matching_case_idx:]:
                    for stmt in case.stmts:
                        execute(stmt, stmt_exec_fn, env, *eval_args)

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
class WhileStmt(Stmt):
    condition: expr.Expr
    statement: Stmt

    @override
    def __repr__(self):
        return self.to_string()

    @override
    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += "\n" + self.condition.to_string(ntab + 2, "condition")
        result += "\n" + self.statement.to_string(ntab + 2, "statement")
        result += f"{' ' * ntab})\n"
        return result

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        try:
            while (
                condition := evaluate(self.condition, expr_eval_fn, env, *eval_args)
            ) and (
                (condition.value_type is ArduinoBuiltinType.BOOL and condition.value)
                or condition.value != 0
            ):
                try:
                    execute(self.statement, stmt_exec_fn, env, *eval_args)
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
class DoWhileStmt(Stmt):
    statement: Stmt
    condition: expr.Expr

    @override
    def __repr__(self):
        return self.to_string()

    @override
    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += "\n" + self.statement.to_string(ntab + 2, "statement")
        result += "\n" + self.condition.to_string(ntab + 2, "condition")
        result += f"{' ' * ntab})\n"
        return result

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        try:
            execute(self.statement, stmt_exec_fn, env, *eval_args)
            while (
                condition := evaluate(self.condition, expr_eval_fn, env, *eval_args)
            ) and (
                (condition.value_type is ArduinoBuiltinType.BOOL and condition.value)
                or condition.value != 0
            ):
                try:
                    execute(self.statement, stmt_exec_fn, env, *eval_args)
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
class ForStmt(Stmt):
    init_expr: expr.Expr | VariableStmt | None
    condition: expr.Expr | None
    loop_expr: expr.Expr | None
    statement: Stmt

    @override
    def __repr__(self):
        return self.to_string()

    @override
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

    @override
    def run(
        self,
        env: Environment,
        stmt_exec_fn="execute",
        expr_eval_fn="evaluate",
        *eval_args,
    ):
        if isinstance(self.init_expr, VariableStmt):
            execute(self.init_expr, stmt_exec_fn, env, *eval_args)
        elif self.init_expr is not None:
            evaluate(self.init_expr, expr_eval_fn, env, *eval_args)

        try:
            if self.condition is None:
                self._infinite_loop(env, stmt_exec_fn, *eval_args)
            else:
                condition = evaluate(self.condition, expr_eval_fn, env, *eval_args)

                while (
                    condition := evaluate(self.condition, expr_eval_fn, env, *eval_args)
                ) and (
                    (
                        condition.value_type is ArduinoBuiltinType.BOOL
                        and condition.value
                    )
                    or condition.value != 0
                ):
                    try:
                        execute(self.statement, stmt_exec_fn, env, *eval_args)
                        if self.loop_expr is not None:
                            evaluate(self.loop_expr, expr_eval_fn, env, *eval_args)
                    except ContinueException:
                        if self.loop_expr is not None:
                            evaluate(self.loop_expr, expr_eval_fn, env, *eval_args)
                        continue

        except BreakException:
            pass

    def _infinite_loop(self, env: Environment, stmt_exec_fn: str, *eval_args):
        while True:
            try:
                execute(self.statement, stmt_exec_fn, env, *eval_args)
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
