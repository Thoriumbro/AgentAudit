from dataclasses import dataclass, field, asdict
from typing import Any

@dataclass
class ExecutionTrace:
    task: str

    tool_calls: list[dict[str, Any]] = field(default_factory=list)

    tool_results: list[dict[str, Any]] = field(default_factory=list)

    retrieved_context: list[dict[str, Any]] = field(default_factory=list)

    injected_failure: dict[str, Any] | None = None

    agent_response: str = ""

    evaluation: Any = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)