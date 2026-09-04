import pytest

from agentaudit.scenarios.factory import create_scenario


def test_tool_corruption_scenario():
    scenario = create_scenario("tool_corruption")

    assert scenario.failure_type == "tool_corruption"
    assert scenario.target == "calculator"


def test_context_poisoning_scenario():
    scenario = create_scenario("context_poisoning")

    assert scenario.failure_type == "context_poisoning"
    assert scenario.target == "retrieved_context"


def test_instruction_conflict_scenario():
    scenario = create_scenario("instruction_conflict")

    assert scenario.failure_type == "instruction_conflict"
    assert scenario.target == "system_prompt"


def test_invalid_failure_type():
    with pytest.raises(ValueError):
        create_scenario("invalid_failure")