class SessionNotValidException(Exception):
    def __init__(self, message: str = "Session not valid."):
        super().__init__(message)
