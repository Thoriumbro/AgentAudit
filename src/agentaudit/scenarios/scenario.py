from dataclasses import dataclass
from typing import Any


@dataclass
class FailureScenario:
    """
    Describes a failure that AgentAudit should inject.
    """

    name: str
    failure_type: str
    target: str
    injection_point: str
    failure: Any

    expected_result: Any = None
    expected_behavior: str | None = None