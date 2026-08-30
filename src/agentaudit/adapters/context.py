from dataclasses import dataclass
from typing import Any


@dataclass
class ExecutionContext:
    """
    Information supplied by AgentAudit for a single agent run.
    """

    tool_interceptor: Any = None
    context_interceptor: Any = None
    instruction_interceptor: Any = None