import json

from agentaudit.evaluation.evaluator import EvaluationResult
from agentaudit.reporting.json_reporter import JSONReporter


def test_json_reporter(tmp_path):
    result = EvaluationResult(
        task_completion=False,
        failure_detection=False,
        recovery=False,
        hallucination=True,
        robustness_score=0.0,
        latency=1.2,
        tool_call_count=1,
        tool_call_error_rate=0.0,
    )

    class MockTrace:
        def to_dict(self):
            return {
                "task": "What is 125 * 37?",
                "evaluation": {
                    "task_completion": result.task_completion,
                    "hallucination": result.hallucination,
                },
            }

    output_path = tmp_path / "report.json"

    JSONReporter().save(
        MockTrace(),
        str(output_path),
    )

    with open(output_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert "trace" in data
    assert data["trace"]["task"] == "What is 125 * 37?"
    assert data["trace"]["evaluation"]["hallucination"] is True