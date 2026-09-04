from agentaudit.agents.reference_agent import ReferenceAgent
from agentaudit.evaluation.evaluator import Evaluator
from agentaudit.failures.tool_corruption import ToolCorruption
from agentaudit.harness import AgentAudit
from agentaudit.scenarios.scenario import FailureScenario


def test_tool_corruption_end_to_end():

    agent = ReferenceAgent()

    scenario = FailureScenario(
        name="corrupt_calculator",
        failure_type="tool_corruption",
        target="calculator",
        injection_point="tool_result",
        failure=ToolCorruption("9999"),
        expected_result="4625",
    )

    audit = AgentAudit(
        agent=agent,
        scenario=scenario,
        evaluator=Evaluator(),
    )

    result = audit.run("What is 125 * 37?")

    assert result is not None
    assert audit.last_trace is not None
    assert audit.last_trace.evaluation is not None

    assert len(result.tool_calls) > 0
    assert len(result.tool_results) > 0

    assert (
        audit.last_trace.injected_failure["failure_type"]
        == "tool_corruption"
    )