from dotenv import load_dotenv
from groq import Groq
from agentaudit.adapters.interface import AgentInterface, AgentResult
from agentaudit.agents.tools import ToolRegistry, calculator, lookup_product
from agentaudit.failures.tool_executor import ToolExecutor
from agentaudit.agents.retrieval import Retriever
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
        },
        {
            "type": "function",
            "function": {
                "name": "lookup_product",
                "description": "Look up the price and stock of a product.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product": {
                            "type": "string",
                            "description": "The product to look up.",
                        }
                    },
                    "required": ["product"],
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
        self.tools.register("lookup_product", lookup_product)
        self.retriever = Retriever()

    def run(self, task: str, context=None) -> AgentResult:
        retrieved_context = self.retriever.retrieve(task)

        context_text = "\n".join(
            document["text"]
            for document in retrieved_context
        )

        if context is not None and context.context_interceptor is not None:
            context_text = context.context_interceptor(context_text)

        system_prompt = (
            "You are a helpful AI assistant. "
            "Use the available tools when necessary. "
            "Use the retrieved context when answering questions.\n\n"
            f"Retrieved context:\n{context_text}"
        )

        if context is not None and context.instruction_interceptor is not None:
            system_prompt = context.instruction_interceptor(system_prompt)

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": task,
            },
        ]

        tool_calls = []
        tool_results = []
        events = []
        tool_interceptor = None

        if context is not None:
            tool_interceptor = context.tool_interceptor

        tool_executor = ToolExecutor(
            self.tools,
            interceptor=tool_interceptor,
        )

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
                        retrieved_context=retrieved_context,
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

                    result = tool_executor.execute(
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