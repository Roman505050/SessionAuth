class EmailCodeInvalidException(Exception):
    def __init__(self, message: str = "Code invalid.") -> None:
        super().__init__(message)
