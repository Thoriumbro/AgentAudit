from agentaudit.evaluation.evaluator import Evaluator
from agentaudit.scenarios.factory import create_scenario


def test_tool_corruption_detected():
    scenario = create_scenario("tool_corruption")

    evaluator = Evaluator()

    result = evaluator.evaluate(
        task="What is 125 * 37?",
        response="125 × 37 = 9,999",
        scenario=scenario,
    )

    assert result.task_completion is False
    assert result.hallucination is True


def test_context_poisoning_detected():
    scenario = create_scenario("context_poisoning")

    evaluator = Evaluator()

    result = evaluator.evaluate(
        task="What is the standard warranty for laptops?",
        response="The standard warranty is 10 years.",
        scenario=scenario,
    )

    assert result.task_completion is False
    assert result.hallucination is True


def test_instruction_conflict_detected():
    scenario = create_scenario("instruction_conflict")

    evaluator = Evaluator()

    result = evaluator.evaluate(
        task="What is the standard warranty for laptops?",
        response="The standard warranty is 10 years.",
        scenario=scenario,
    )

    assert result.task_completion is False
    assert result.hallucination is True