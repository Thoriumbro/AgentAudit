from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from agentaudit.adapters.context import ExecutionContext


@dataclass
class AgentResult:
    response: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    retrieved_context: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class AgentInterface(ABC):

    @abstractmethod
    def run(self, task: str, context: ExecutionContext | None = None) -> AgentResult:
        """
        Execute a task using the agent.

        context contains execution-specific information supplied
        by the AgentAudit harness.
        """
        pass