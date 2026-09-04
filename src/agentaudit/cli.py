import argparse
import os

from agentaudit.agents.reference_agent import ReferenceAgent
from agentaudit.evaluation.evaluator import Evaluator
from agentaudit.harness import AgentAudit
from agentaudit.scenarios.factory import create_scenario

from agentaudit.reporting.json_reporter import JSONReporter


def main():
    parser = argparse.ArgumentParser(
        description="AgentAudit - Failure Injection Testing Framework"
    )

    parser.add_argument(
        "task",
        help="Task to give to the agent",
    )

    parser.add_argument(
        "--failure",
        choices=[
            "tool_corruption",
            "context_poisoning",
            "instruction_conflict",
        ],
        required=True,
        help="Failure type to inject",
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of times to run the audit",
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Path for the JSON report",
    )

    args = parser.parse_args()

    if args.runs < 1:
        parser.error("--runs must be at least 1")

    scenario = create_scenario(args.failure)

    audit = AgentAudit(
        agent=ReferenceAgent(),
        scenario=scenario,
        evaluator=Evaluator(),
    )

    for i in range(args.runs):
        print(f"\n{'=' * 60}")
        print(f"RUN {i + 1}/{args.runs}")
        print(f"{'=' * 60}")

        audit.run(args.task)

    metrics = audit.metrics.calculate()

    if args.output is None:
        os.makedirs("results", exist_ok=True)
        output_path = f"results/{args.failure}.json"
    else:
        output_path = args.output

    JSONReporter().save(
        audit.last_trace,
        output_path,
        metrics=metrics,
    )

    print("\n" + "=" * 60)
    print("AGGREGATE METRICS")
    print("=" * 60)

    print(f"Runs:                    {metrics.total_runs}")
    print(f"Task success rate:       {metrics.task_success_rate:.2f}")
    print(f"Failure detection rate:  {metrics.failure_detection_rate:.2f}")
    print(f"Recovery rate:           {metrics.recovery_rate:.2f}")
    print(f"Hallucination rate:      {metrics.hallucination_rate:.2f}")
    print(f"Average latency:         {metrics.average_latency:.3f}s")
    print(f"Average tool calls:      {metrics.average_tool_calls:.2f}")
    print(f"Tool error rate:         {metrics.tool_error_rate:.2f}")
    print(f"Robustness score:        {metrics.average_robustness_score:.2f}")

    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()