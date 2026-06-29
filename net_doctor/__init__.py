"""net_doctor: a structured network troubleshooting assistant.

This is not a chatbot. It is a decision tree that follows the same layered
method I use by hand: work up from the physical link to IP, gateway, DNS and
finally the application, one check at a time, and stop at the first thing that
is actually broken. Each step tells you what to check, the command to run, and
how to read the result.
"""
from .engine import run_flow, walk
from .flows import FLOWS, get_flow

__all__ = ["FLOWS", "get_flow", "run_flow", "walk"]
__version__ = "0.1.0"
