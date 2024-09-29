from enum import StrEnum


class Purpose(StrEnum):
    """
    Enum for the purpose of the verification code.
    """

    REGISTRATION = "registration"
    CHANGE_PASSWORD = "change_password"
