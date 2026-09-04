from dataclasses import dataclass


@dataclass
class AggregateMetrics:
    total_runs: int
    task_success_rate: float
    failure_detection_rate: float
    recovery_rate: float
    average_latency: float
    average_tool_calls: float
    tool_error_rate: float
    average_robustness_score: float
    hallucination_rate: float


class MetricsAggregator:
    """
    Aggregates evaluation results across multiple agent executions.
    """

    def __init__(self):
        self.results = []

    def add(self, result):
        self.results.append(result)

    def calculate(self) -> AggregateMetrics:
        if not self.results:
            return AggregateMetrics(
                total_runs=0,
                task_success_rate=0.0,
                failure_detection_rate=0.0,
                recovery_rate=0.0,
                average_latency=0.0,
                average_tool_calls=0.0,
                tool_error_rate=0.0,
                average_robustness_score=0.0,
                hallucination_rate=0.0,
            )

        total_runs = len(self.results)

        
        hallucination_rate = (
            sum(result.hallucination for result in self.results)
            / total_runs
        )

        task_success_rate = (
            sum(result.task_completion for result in self.results)
            / total_runs
        )

        failure_detection_rate = (
            sum(result.failure_detection for result in self.results)
            / total_runs
        )

        recovery_rate = (
            sum(result.recovery for result in self.results)
            / total_runs
        )

        average_latency = (
            sum(result.latency for result in self.results)
            / total_runs
        )

        average_tool_calls = (
            sum(result.tool_call_count for result in self.results)
            / total_runs
        )

        total_tool_calls = sum(
            result.tool_call_count
            for result in self.results
        )

        total_tool_errors = sum(
            result.tool_call_error_rate * result.tool_call_count
            for result in self.results
        )

        tool_error_rate = (
            total_tool_errors / total_tool_calls
            if total_tool_calls > 0
            else 0.0
        )

        average_robustness_score = (
            sum(result.robustness_score for result in self.results)
            / total_runs
        )

        return AggregateMetrics(
            total_runs=total_runs,
            task_success_rate=task_success_rate,
            failure_detection_rate=failure_detection_rate,
            recovery_rate=recovery_rate,
            average_latency=average_latency,
            average_tool_calls=average_tool_calls,
            tool_error_rate=tool_error_rate,
            average_robustness_score=average_robustness_score,
            hallucination_rate=hallucination_rate,
        )