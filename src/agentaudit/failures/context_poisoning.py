class ContextPoisoning:
    """
    Injects misleading information into the agent's context.
    """

    def __init__(self, poisoned_context: str):
        self.poisoned_context = poisoned_context

    def intercept(self, context: str) -> str:
        """
        Modify the context before it reaches the model.
        """
        return context + "\n\n" + self.poisoned_context