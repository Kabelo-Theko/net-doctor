"""Walk a diagnostic flow.

Two ways to drive it:
  - walk(flow, answer_fn): interactive, where answer_fn(step) returns True/False
  - run_flow(flow, answers): non-interactive, replaying a list of True/False
Both return a result: the conclusion reached plus the path of step ids taken.
This split keeps the logic testable without typing at a prompt.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .flows import get_flow


@dataclass
class Result:
    flow_key: str
    path: list[str] = field(default_factory=list)
    conclusion: dict | None = None

    @property
    def reached_conclusion(self) -> bool:
        return self.conclusion is not None


def _resolve(flow: dict) -> dict:
    return flow if isinstance(flow, dict) and "steps" in flow else get_flow(flow)


def walk(flow, answer_fn: Callable[[dict], bool], flow_key: str = "") -> Result:
    """Walk the tree, calling answer_fn(step) at each check to get pass/fail."""
    flow = _resolve(flow)
    result = Result(flow_key=flow_key or flow.get("title", ""))
    step_id = flow["start"]
    seen: set[str] = set()

    while True:
        if step_id in seen:
            raise RuntimeError(f"Loop detected at step '{step_id}'")
        seen.add(step_id)
        step = flow["steps"][step_id]
        result.path.append(step_id)

        if step["kind"] == "conclusion":
            result.conclusion = step
            return result

        passed = answer_fn(step)
        step_id = step["on_pass"] if passed else step["on_fail"]


def run_flow(flow, answers: list[bool], flow_key: str = "") -> Result:
    """Replay a fixed list of pass/fail answers. Useful for tests and demos."""
    it = iter(answers)

    def answer_fn(_step):
        try:
            return next(it)
        except StopIteration:
            raise ValueError("Ran out of answers before reaching a conclusion")

    return walk(flow, answer_fn, flow_key=flow_key)


def validate_flow(flow) -> list[str]:
    """Return a list of integrity problems (empty list means the tree is sound)."""
    flow = _resolve(flow)
    problems: list[str] = []
    steps = flow["steps"]
    if flow["start"] not in steps:
        problems.append(f"start '{flow['start']}' is not a defined step")
    for sid, step in steps.items():
        if step["kind"] == "check":
            for branch in ("on_pass", "on_fail"):
                target = step.get(branch)
                if target not in steps:
                    problems.append(f"step '{sid}' {branch} -> missing '{target}'")
        elif step["kind"] == "conclusion":
            for key in ("cause", "fix", "escalate"):
                if not step.get(key):
                    problems.append(f"conclusion '{sid}' is missing '{key}'")
        else:
            problems.append(f"step '{sid}' has unknown kind '{step.get('kind')}'")
    return problems
