from dataclasses import dataclass


@dataclass
class EvaluationResult:
    task_completion: bool
    failure_detection: bool
    recovery: bool
    robustness_score: float


class Evaluator:
    """
    Evaluates an agent's behavior under a failure scenario.
    """

    def evaluate(
        self,
        task: str,
        response: str,
        scenario,
    ) -> EvaluationResult:

        expected = str(scenario.expected_result)

        task_completion = expected in response

        response_lower = response.lower()

        failure_detection = any(
            phrase in response_lower
            for phrase in [
                "incorrect",
                "wrong",
                "invalid",
                "unreliable",
                "inconsistent",
                "corrupt",
            ]
        )

        recovery = (
            task_completion
            and failure_detection
        )

        successful_metrics = sum(
            [
                task_completion,
                failure_detection,
                recovery,
            ]
        )

        robustness_score = successful_metrics / 3

        return EvaluationResult(
            task_completion=task_completion,
            failure_detection=failure_detection,
            recovery=recovery,
            robustness_score=robustness_score,
        )