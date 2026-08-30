import json
from pathlib import Path

from agentaudit.tracing.trace import ExecutionTrace

class JSONReporter:

    def save(self, trace: ExecutionTrace, path: str) -> None:
        output = trace.to_dict()

        Path(path).write_text(
            json.dumps(output, indent=2),
            encoding="utf-8",
        )