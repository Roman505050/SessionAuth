class EmailCodeExpiredException(Exception):
    def __init__(self, message: str = "Code expired.") -> None:
        super().__init__(message)
