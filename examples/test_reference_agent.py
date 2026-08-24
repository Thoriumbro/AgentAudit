from agentaudit.agents.reference_agent import ReferenceAgent


def main():
    agent = ReferenceAgent()
    result = agent.run(
        "What is 125 * 37?"
    )

    print("Response:")
    print(result.response)

    print("\nMetadata:")
    print(result.tool_calls)


if __name__ == "__main__":
    main()