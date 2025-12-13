"""
Arduino debugger.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from threading import Lock, Thread
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

    def __init__(
        self,
        start_node: Stmt,
        environment: Environment,
        lock: Lock,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = None,
        *,
        daemon: bool | None = None,
    ) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.debug_state = DebugState(start_node, lock)
        self.environment = environment

    @override
    def run(self) -> None:
        while self.debug_state.lock.acquire():
            self.debug_state.current_node.debug(
                self.environment,
                self.debug_state
            )

class DebugState:
    current_node: Stmt | Expr | None
    action: Action
    lock: Lock

    def __init__(self, start_node: Stmt, lock: Lock) -> None:
        self.current_node = start_node
        self.action = Action.CONTINUE
        self.lock = lock
