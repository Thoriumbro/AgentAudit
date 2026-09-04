from agentaudit.evaluation.aggregator import MetricsAggregator
from agentaudit.evaluation.evaluator import EvaluationResult


def test_aggregator():
    aggregator = MetricsAggregator()

    aggregator.add(
        EvaluationResult(
            task_completion=True,
            failure_detection=True,
            recovery=True,
            hallucination=False,
            robustness_score=1.0,
            latency=1.0,
            tool_call_count=2,
            tool_call_error_rate=0.5,
        )
    )

    aggregator.add(
        EvaluationResult(
            task_completion=False,
            failure_detection=False,
            recovery=False,
            hallucination=True,
            robustness_score=0.0,
            latency=2.0,
            tool_call_count=0,
            tool_call_error_rate=0.0,
        )
    )

    metrics = aggregator.calculate()

    assert metrics.total_runs == 2
    assert metrics.task_success_rate == 0.5
    assert metrics.failure_detection_rate == 0.5
    assert metrics.recovery_rate == 0.5
    assert metrics.hallucination_rate == 0.5
    assert metrics.average_latency == 1.5
    assert metrics.average_tool_calls == 1.0