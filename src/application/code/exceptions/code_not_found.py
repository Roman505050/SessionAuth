from shared.exceptions.not_found import NotFoundException


class CodeNotFoundException(NotFoundException):
    def __init__(self, message: str = "Code not found"):
        super().__init__(message)
