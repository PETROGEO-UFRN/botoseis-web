class WorkflowRunningError(Exception):
    def __init__(self, message):
        self.message = message
        self.statusCode = 500
