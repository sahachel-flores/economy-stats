class PipelineError(Exception):
    """
    Base class for all pipeline-related exceptions.
    Use this as the parent for more specific error types.
    """

    def __init__(self, message: str = "Pipeline error occurred"):
        super().__init__(message)


class FetchError(PipelineError):
    """
    Raised when fetching or storing articles fails.
    Examples:
        - No data from API
        - Failed HTTP request
        - DB insert failure
    """

    def __init__(self, message: str = "Failed to fetch articles"):
        super().__init__(message)


class AgentExecutionError(PipelineError):
    """
    Raised when any pipeline agent (selector, editor, summarizer, etc.) fails.
    Examples:
        - Agent returns False
        - Exception inside agent logic
    """

    def __init__(self, message: str = "Agent execution failed"):
        super().__init__(message)
