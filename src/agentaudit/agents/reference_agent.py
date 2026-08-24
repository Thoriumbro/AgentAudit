from dotenv import load_dotenv
from groq import Groq
from agentaudit.adapters.interface import AgentInterface, AgentResult
from agentaudit.agents.tools import ToolRegistry, calculator
from agentaudit.failures.tool_executor import ToolExecutor
from agentaudit.failures.tool_corruption import ToolCorruption
import json
import os

load_dotenv()


class ReferenceAgent(AgentInterface):
    """
    Minimal reference agent powered by the Groq API.
    """

    TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Calculate a mathematical expression.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "The mathematical expression to calculate.",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. "
                "Add it to your .env file."
            )

        self.client = Groq(api_key=api_key)
        self.model = "openai/gpt-oss-20b"
        self.tools = ToolRegistry()
        self.tools.register("calculator", calculator)
        self.tool_executor = ToolExecutor(
            self.tools,
            failure=ToolCorruption("5555"),
        )

    def run(self, task: str) -> AgentResult:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Use the calculator tool whenever mathematical "
                    "calculation is required."
                ),
            },
            {
                "role": "user",
                "content": task,
            },
        ]

        tool_calls = []
        tool_results = []
        events = []

        try:
            while True:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.TOOLS,
                    tool_choice="auto",
                    temperature=0,
                )

                message = response.choices[0].message

                if not message.tool_calls:
                    return AgentResult(
                        response=message.content or "",
                        tool_calls=tool_calls,
                        tool_results=tool_results,
                        events=events,
                        metadata={
                            "model": self.model,
                        },
                    )

                messages.append(message)

                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    arguments = tool_call.function.arguments

                    tool_calls.append(
                        {
                            "id": tool_call.id,
                            "name": name,
                            "arguments": arguments,
                        }
                    )

                    args = json.loads(arguments)

                    result = self.tool_executor.execute(
                        name,
                        args,
                    )

                    tool_results.append(
                        {
                            "tool_call_id": tool_call.id,
                            "name": name,
                            "result": result,
                        }
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result,
                        }
                    )

        except Exception as exc:
            raise RuntimeError(
                f"Reference agent failed during execution: {exc}"
            ) from exc