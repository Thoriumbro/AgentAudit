from typing import Any, Callable

from agentaudit.agents.tools import ToolRegistry


class ToolExecutor:
    """
    Executes tools and optionally applies a failure to their results.
    """

    def __init__(self, registry: ToolRegistry, failure=None):
        self.registry = registry
        self.failure = failure

    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        """
        Execute a tool and optionally modify its result.
        """

        result = self.registry.execute(name, arguments)

        if self.failure is not None:
            result = self.failure.apply(result)

        return result