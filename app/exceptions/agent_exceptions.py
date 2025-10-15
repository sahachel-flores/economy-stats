class AgentExecutionError(Exception):
    def __init__(self, message="Agent failed to execute"):
        super().__init__(message)
