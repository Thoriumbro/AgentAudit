from agentaudit.adapters.interface import AgentInterface, AgentResult
from agentaudit.scenarios.scenario import FailureScenario
from agentaudit.tracing.trace import ExecutionTrace
from agentaudit.adapters.context import ExecutionContext


class AgentAudit:
    """
    Main testing harness for running an agent under a failure scenario.
    """

    def __init__(self, agent: AgentInterface, scenario: FailureScenario | None = None, evaluator=None):
        self.agent = agent
        self.scenario = scenario
        self.evaluator = evaluator
        self.last_trace = None

    def run(self, task: str) -> AgentResult:
        """
        Run the agent with the configured failure scenario.
        """

        interceptor = None
        context_interceptor = None

        if self.scenario is not None:
            if self.scenario.failure_type == "tool_corruption":
                interceptor = self.scenario.failure.intercept

            elif self.scenario.failure_type == "context_poisoning":
                context_interceptor = self.scenario.failure.intercept

            elif self.scenario.failure_type == "instruction_conflict":
                instruction_interceptor = self.scenario.failure.intercept

        context = ExecutionContext(
            tool_interceptor=interceptor,
            context_interceptor=context_interceptor,
            instruction_interceptor=instruction_interceptor,
        )

        result = self.agent.run(
            task,
            context=context,
        )

        evaluation = None

        if self.evaluator is not None:
            evaluation = self.evaluator.evaluate(
                task=task,
                response=result.response,
                scenario=self.scenario,
            )

        trace = ExecutionTrace(
            task=task,
            tool_calls=result.tool_calls,
            tool_results=result.tool_results,
            retrieved_context=result.retrieved_context,
            agent_response=result.response,
            evaluation=evaluation,
            metadata=result.metadata,
        )

        self.last_trace = trace

        if self.scenario is not None:
            trace.injected_failure = {
                "name": self.scenario.name,
                "failure_type": self.scenario.failure_type,
                "target": self.scenario.target,
                "injection_point": self.scenario.injection_point,
            }

        print("\nExecution Trace:")
        print(trace)

        print("\nEvaluation:")
        print(evaluation)

        return result