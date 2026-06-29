"""Interactive command-line front end for net_doctor.

Run it, pick a symptom, and answer each check with y/n. It stops at the first
real fault and prints a structured conclusion: likely cause, the fix, and when
to escalate. No external services; it is the decision tree, nothing more.
"""
from __future__ import annotations

import sys

from .engine import walk
from .flows import FLOWS, get_flow


def _print(s: str = "") -> None:
    print(s)


def _choose_flow() -> str:
    _print("net-doctor — structured network troubleshooting")
    _print("=" * 46)
    _print("Pick the symptom that best matches:\n")
    keys = list(FLOWS)
    for i, key in enumerate(keys, 1):
        _print(f"  {i}. {FLOWS[key]['title']}")
    _print()
    while True:
        choice = input("Number (or q to quit): ").strip().lower()
        if choice in ("q", "quit", "exit"):
            sys.exit(0)
        if choice.isdigit() and 1 <= int(choice) <= len(keys):
            return keys[int(choice) - 1]
        _print("Please enter a valid number.")


def _ask(step: dict) -> bool:
    _print()
    _print(f"CHECK: {step['text']}")
    if step.get("command"):
        _print(f"  run:        {step['command']}")
    if step.get("interpret"):
        _print(f"  read it as: {step['interpret']}")
    while True:
        ans = input("  Did this pass / look healthy? (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        _print("  Please answer y or n.")


def _show_conclusion(step: dict) -> None:
    _print()
    _print("-" * 46)
    _print("LIKELY CAUSE")
    _print(f"  {step['cause']}")
    _print()
    _print("FIX")
    _print(f"  {step['fix']}")
    _print()
    _print("WHEN TO ESCALATE")
    _print(f"  {step['escalate']}")
    _print("-" * 46)


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    if "--list" in argv:
        for key in FLOWS:
            _print(f"{key}\t{FLOWS[key]['title']}")
        return 0

    if "--flow" in argv:
        key = argv[argv.index("--flow") + 1]
        flow = get_flow(key)
    else:
        flow = get_flow(_choose_flow())

    result = walk(flow, _ask, flow_key=flow["title"])
    _show_conclusion(result.conclusion)
    _print(f"\npath: {' -> '.join(result.path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
