"""
Arduino debugger.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from threading import Event, Thread
from typing import TYPE_CHECKING, Any, Callable, override
from enum import Enum

from simulator.interpreter.environment import Environment

if TYPE_CHECKING:
    from simulator.interpreter.ast.stmt import Stmt
    from simulator.interpreter.ast.expr import Expr


class Action(Enum):
    STEP = 1
    NEXT = 2
    CONTINUE = 3
    INSPECT = 4


class Debugger(Thread):
    debug_state: DebugState
    environment: Environment
    breakpoints: dict[int, Stmt]
    program: list[Stmt]
    loop_callback: Callable[..., object] | None

    def __init__(
        self,
        program: list[Stmt],
        environment: Environment,
        input_event: Event,
        stopped: Event,
        loop_callback: Callable[..., object] | None = None,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = None,
        *,
        daemon: bool | None = None,
    ) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.debug_state = DebugState(program[0], input_event, stopped)
        self.program = program
        self.environment = environment
        self.breakpoints = {}
        self.loop_callback = loop_callback

    @override
    def run(self) -> None:
        for stmt in self.program:
            stmt.debug(self.environment, self.debug_state)

        setup_fn = self.environment.get("setup", 0)
        if setup_fn:
            setup_fn.value.call([], setup_fn.value_type, True, self.debug_state)

        loop_fn = self.environment.get("loop", 0)
        if loop_fn:
            while not self.debug_state.finished:
                loop_fn.value.call([], loop_fn.value_type, True, self.debug_state)
                if self.loop_callback:
                    self.loop_callback()

        self.stop()
        self.debug_state.stopped.set()

    def step(self):
        self.debug_state.action = Action.STEP
        self.debug_state.stopped.clear()
        self.debug_state.input_event.set()

    def next(self):
        self.debug_state.action = Action.NEXT
        self.debug_state.stopped.clear()
        self.debug_state.input_event.set()

    def cont(self):
        self.debug_state.action = Action.CONTINUE
        self.debug_state.stopped.clear()
        self.debug_state.input_event.set()

    def stop(self):
        self.debug_state.finished = True

    def print(self):
        print(self.debug_state.current_node)

    def toggle_breakpoint(self, line_number: int) -> bool:
        if line_number in self.breakpoints:
            stmt = self.breakpoints.pop(line_number)
            stmt.breakpoint = False
        else:
            for stmt in self.program:
                if brk_stmt := stmt.set_breakpoint(line_number):
                    self.breakpoints[line_number] = brk_stmt
                    return True

        return False


class DebugState:
    current_node: Stmt | Expr
    action: Action
    input_event: Event
    stopped: Event
    finished: bool

    def __init__(self, start_node: Stmt, input_event: Event, stopped: Event) -> None:
        self.current_node = start_node
        self.input_event = input_event
        self.stopped = stopped
        self.action = Action.STEP
        self.finished = False
