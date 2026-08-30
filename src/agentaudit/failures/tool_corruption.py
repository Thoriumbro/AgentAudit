from typing import Any


class ToolCorruption:
    """
    Modifies a tool's result to simulate unreliable tool output.
    """

    def __init__(self, corrupted_value: Any):
        self.corrupted_value = corrupted_value

    def apply(self, original_result: Any) -> Any:
        """
        Replace the original tool result with corrupted data.
        """
        return self.corrupted_value

    def intercept(self, name, arguments, result):
        return self.apply(result)