from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentResult:
    """
    Standard result returned after an agent executes a task.
    """

    # The agent's final answer
    response: str

    # Tools used by the agent
    tool_calls: list[dict[str, Any]] = field(default_factory=list)

    # Results returned by those tools
    tool_results: list[dict[str, Any]] = field(default_factory=list)

    # Documents/context retrieved by the agent
    retrieved_context: list[dict[str, Any]] = field(default_factory=list)

    # Events that happened during execution
    events: list[dict[str, Any]] = field(default_factory=list)

    # Additional information about the execution
    metadata: dict[str, Any] = field(default_factory=dict)


class AgentInterface(ABC):
    """
    Interface that every agent adapter must implement.

    AgentAudit talks to agents through this interface instead
    of depending on a specific agent implementation.
    """

    @abstractmethod
    def run(self, task: str) -> AgentResult:
        """
        Execute a task using the agent.

        Args:
            task: The task given to the agent.

        Returns:
            AgentResult containing the agent's response
            and execution information.
        """
        pass