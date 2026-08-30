class InstructionConflict:
    """
    Injects a conflicting instruction into the agent's prompt.
    """

    def __init__(self, conflicting_instruction: str):
        self.conflicting_instruction = conflicting_instruction

    def intercept(self, prompt: str) -> str:
        return (
            prompt
            + "\n\n"
            + "Additional instruction:\n"
            + self.conflicting_instruction
        )