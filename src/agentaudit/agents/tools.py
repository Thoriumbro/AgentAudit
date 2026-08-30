from typing import Any, Callable


class ToolRegistry:
    """
    Stores the tools available to the reference agent.
    """

    def __init__(self):
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, function: Callable[..., Any]) -> None:
        """Register a tool by name."""
        self._tools[name] = function

    def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        """Execute a registered tool."""
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")

        return self._tools[name](**arguments)


def calculator(expression: str) -> str:
    """
    Calculate a basic mathematical expression.
    """

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)

    except Exception as exc:
        raise ValueError(
            f"Could not calculate expression '{expression}': {exc}"
        ) from exc

PRODUCTS = {
    "laptop": {
        "price": 75000,
        "stock": 12,
    },
    "phone": {
        "price": 45000,
        "stock": 25,
    },
    "tablet": {
        "price": 30000,
        "stock": 8,
    },
}


def lookup_product(product: str) -> str:
    """
    Look up product information.
    """

    product = product.lower()

    if product not in PRODUCTS:
        return f"Product '{product}' was not found."

    return str(PRODUCTS[product])