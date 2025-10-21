class FinTabloError(Exception):
    """Base exception for FinTablo client errors."""
    def __init__(self, message, status_code=None, body=None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body
