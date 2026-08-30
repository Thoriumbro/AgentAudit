from typing import Any

from agentaudit.agents.tools import ToolRegistry


class ToolExecutor:
    def __init__(self, registry, interceptor=None):
        self.registry = registry
        self.interceptor = interceptor

    def execute(self, name, arguments):
        result = self.registry.execute(name, arguments)

        if self.interceptor is not None:
            result = self.interceptor(
                name,
                arguments,
                result,
            )

        return result